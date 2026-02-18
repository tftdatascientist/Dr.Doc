#!/usr/bin/env python3
"""
Dr.Doc Web Server
Flask API serving the web interface
"""

import sys
import os
from pathlib import Path
from flask import Flask, render_template, request, jsonify, send_from_directory

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.parsers import parse_content, detect_format
from src.transformers import transform_data
from src.generators.file_generator import FileGenerator

app = Flask(__name__, 
            template_folder='templates',
            static_folder='static')

# Configuration
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
OUTPUT_DIR = Path(__file__).parent.parent / 'data' / 'output'


@app.route('/')
def index():
    """Serve the main page"""
    return render_template('index.html')


@app.route('/api/detect', methods=['POST'])
def api_detect_format():
    """
    API endpoint to detect input format
    
    Request JSON:
    {
        "content": "string - content to analyze"
    }
    
    Response JSON:
    {
        "success": true/false,
        "format": "detected format",
        "confidence": 0.0-1.0,
        "error": "error message if any"
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'content' not in data:
            return jsonify({
                'success': False,
                'error': 'Missing content field'
            }), 400
        
        content = data['content']
        
        if not content or not content.strip():
            return jsonify({
                'success': False,
                'error': 'Empty content'
            }), 400
        
        # Detect format
        format_name, confidence = detect_format(content)
        
        return jsonify({
            'success': True,
            'format': format_name,
            'confidence': confidence
        })
        
    except Exception as e:
        app.logger.error(f"Error in detect_format: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/transform', methods=['POST'])
def api_transform():
    """
    API endpoint to transform data
    
    Request JSON:
    {
        "content": "string - input content",
        "format": "string - input format (auto/txt/md/json)",
        "destination": "string - destination type (github/chatgpt/project_brief)",
        "options": {
            "project_name": "string",
            "author": "string",
            "description": "string",
            "license": "string",
            "preview": true/false
        }
    }
    
    Response JSON:
    {
        "success": true/false,
        "result": {
            "files_count": int,
            "destination": "string",
            "file_tree": "string - ASCII tree",
            "files": {"path": "content", ...}
        },
        "error": "error message if any"
    }
    """
    try:
        data = request.get_json()
        
        # Validation
        if not data:
            return jsonify({
                'success': False,
                'error': 'No data provided'
            }), 400
        
        content = data.get('content', '')
        if not content or not content.strip():
            return jsonify({
                'success': False,
                'error': 'Empty content'
            }), 400
        
        format_hint = data.get('format', 'auto')
        if format_hint == 'auto':
            format_hint = None
        
        destination = data.get('destination')
        if not destination:
            return jsonify({
                'success': False,
                'error': 'Missing destination'
            }), 400
        
        if destination not in ['github', 'chatgpt', 'project_brief']:
            return jsonify({
                'success': False,
                'error': f'Unknown destination: {destination}'
            }), 400
        
        options = data.get('options', {})
        preview = options.get('preview', True)
        
        # Parse content
        parsed_data = parse_content(content, format_hint)
        
        if parsed_data.errors:
            app.logger.warning(f"Parse warnings: {parsed_data.errors}")
        
        # Transform data
        metadata = {
            'project_name': options.get('project_name', 'my-project'),
            'author': options.get('author', 'Unknown'),
            'description': options.get('description', 'Project description'),
            'license': options.get('license', 'MIT')
        }
        
        transformed_data = transform_data(destination, parsed_data, metadata=metadata)
        
        if transformed_data.errors:
            return jsonify({
                'success': False,
                'error': '; '.join(transformed_data.errors)
            }), 400
        
        # Generate file tree
        generator = FileGenerator(str(OUTPUT_DIR))
        file_tree = generator.get_file_tree(transformed_data)
        
        # Prepare response
        result = {
            'files_count': len(transformed_data.files),
            'destination': destination,
            'file_tree': file_tree,
            'files': transformed_data.files if preview else None
        }
        
        # If not preview mode, actually generate files
        if not preview:
            project_name = metadata['project_name']
            generated_files = generator.generate(transformed_data, project_name)
            result['output_path'] = str(OUTPUT_DIR / project_name)
            result['generated_files'] = list(generated_files.keys())
        
        return jsonify({
            'success': True,
            'result': result
        })
        
    except Exception as e:
        app.logger.error(f"Error in transform: {e}", exc_info=True)
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'Dr.Doc API',
        'version': '1.0.0'
    })


@app.errorhandler(413)
def request_entity_too_large(error):
    """Handle file too large error"""
    return jsonify({
        'success': False,
        'error': 'File too large. Maximum size is 16MB.'
    }), 413


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        'success': False,
        'error': 'Endpoint not found'
    }), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    app.logger.error(f"Internal error: {error}")
    return jsonify({
        'success': False,
        'error': 'Internal server error'
    }), 500


if __name__ == '__main__':
    print("=" * 60)
    print("🩺 Dr.Doc Web Server")
    print("=" * 60)
    print()
    print("Starting server...")
    print("Access the application at: http://localhost:5000")
    print()
    print("Press Ctrl+C to stop the server")
    print("=" * 60)
    
    # Create output directory if it doesn't exist
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    # Run the server
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )
