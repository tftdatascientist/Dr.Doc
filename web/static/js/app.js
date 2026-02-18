// Dr.Doc Frontend Application

// State
const state = {
    inputText: '',
    inputFile: null,
    selectedFormat: 'auto',
    selectedDestination: null,
    projectName: '',
    author: '',
    description: '',
    license: 'MIT',
    previewMode: true
};

// DOM Elements
const elements = {
    inputText: document.getElementById('input-text'),
    charCount: document.getElementById('char-count'),
    fileInput: document.getElementById('file-input'),
    fileUploadArea: document.getElementById('file-upload-area'),
    fileInfo: document.getElementById('file-info'),
    fileName: document.getElementById('file-name'),
    removeFileBtn: document.getElementById('remove-file'),
    detectFormatBtn: document.getElementById('detect-format-btn'),
    detectedFormat: document.getElementById('detected-format'),
    formatName: document.getElementById('format-name'),
    confidence: document.getElementById('confidence'),
    formatSelect: document.getElementById('format-select'),
    destinationCards: document.querySelectorAll('.destination-card'),
    projectName: document.getElementById('project-name'),
    author: document.getElementById('author'),
    description: document.getElementById('description'),
    license: document.getElementById('license'),
    previewMode: document.getElementById('preview-mode'),
    transformBtn: document.getElementById('transform-btn'),
    resultsSection: document.getElementById('results-section'),
    loading: document.getElementById('loading'),
    errorMessage: document.getElementById('error-message'),
    errorText: document.getElementById('error-text'),
    resultsContent: document.getElementById('results-content'),
    filesCount: document.getElementById('files-count'),
    destinationType: document.getElementById('destination-type'),
    fileTree: document.getElementById('file-tree'),
    filesList: document.getElementById('files-list'),
    downloadBtn: document.getElementById('download-btn')
};

// Initialize
function init() {
    setupEventListeners();
    updateCharCount();
}

// Event Listeners
function setupEventListeners() {
    // Input text
    elements.inputText.addEventListener('input', () => {
        state.inputText = elements.inputText.value;
        updateCharCount();
    });

    // File upload
    elements.fileUploadArea.addEventListener('click', () => {
        elements.fileInput.click();
    });

    elements.fileInput.addEventListener('change', handleFileSelect);
    elements.removeFileBtn.addEventListener('click', removeFile);

    // Drag and drop
    elements.fileUploadArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        elements.fileUploadArea.classList.add('dragover');
    });

    elements.fileUploadArea.addEventListener('dragleave', () => {
        elements.fileUploadArea.classList.remove('dragover');
    });

    elements.fileUploadArea.addEventListener('drop', (e) => {
        e.preventDefault();
        elements.fileUploadArea.classList.remove('dragover');
        
        const file = e.dataTransfer.files[0];
        if (file) {
            handleFile(file);
        }
    });

    // Format detection
    elements.detectFormatBtn.addEventListener('click', detectFormat);
    elements.formatSelect.addEventListener('change', (e) => {
        state.selectedFormat = e.target.value;
    });

    // Destination selection
    elements.destinationCards.forEach(card => {
        card.addEventListener('click', () => selectDestination(card));
    });

    // Options
    elements.projectName.addEventListener('input', (e) => {
        state.projectName = e.target.value;
    });
    
    elements.author.addEventListener('input', (e) => {
        state.author = e.target.value;
    });
    
    elements.description.addEventListener('input', (e) => {
        state.description = e.target.value;
    });
    
    elements.license.addEventListener('change', (e) => {
        state.license = e.target.value;
    });
    
    elements.previewMode.addEventListener('change', (e) => {
        state.previewMode = e.target.checked;
    });

    // Transform button
    elements.transformBtn.addEventListener('click', transformData);

    // Download button
    elements.downloadBtn.addEventListener('click', downloadResults);
}

// Update character count
function updateCharCount() {
    const count = elements.inputText.value.length;
    elements.charCount.textContent = count.toLocaleString();
}

// Handle file selection
function handleFileSelect(e) {
    const file = e.target.files[0];
    if (file) {
        handleFile(file);
    }
}

function handleFile(file) {
    // Validate file type
    const validTypes = ['.txt', '.md', '.json', '.doc', '.docx'];
    const ext = '.' + file.name.split('.').pop().toLowerCase();
    
    if (!validTypes.includes(ext)) {
        alert('Nieprawidłowy format pliku. Obsługiwane: TXT, MD, JSON, DOC, DOCX');
        return;
    }

    state.inputFile = file;
    elements.fileName.textContent = file.name;
    
    // Show file info
    document.querySelector('.upload-placeholder').style.display = 'none';
    elements.fileInfo.style.display = 'flex';

    // Read file content
    const reader = new FileReader();
    reader.onload = (e) => {
        state.inputText = e.target.result;
        elements.inputText.value = state.inputText;
        updateCharCount();
    };
    reader.readAsText(file);
}

function removeFile(e) {
    e.stopPropagation();
    
    state.inputFile = null;
    elements.fileInput.value = '';
    elements.fileName.textContent = '';
    
    document.querySelector('.upload-placeholder').style.display = 'block';
    elements.fileInfo.style.display = 'none';
}

// Detect format
async function detectFormat() {
    if (!state.inputText) {
        alert('Najpierw wprowadź dane!');
        return;
    }

    elements.detectFormatBtn.disabled = true;
    elements.detectFormatBtn.textContent = '🔍 Wykrywanie...';

    try {
        const response = await fetch('/api/detect', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                content: state.inputText
            })
        });

        const data = await response.json();

        if (data.success) {
            elements.formatName.textContent = data.format.toUpperCase();
            elements.confidence.textContent = Math.round(data.confidence * 100);
            elements.detectedFormat.style.display = 'block';
            elements.detectedFormat.classList.add('fade-in');
            
            // Update select
            elements.formatSelect.value = data.format;
            state.selectedFormat = data.format;
        }
    } catch (error) {
        console.error('Error detecting format:', error);
        alert('Błąd podczas wykrywania formatu');
    } finally {
        elements.detectFormatBtn.disabled = false;
        elements.detectFormatBtn.textContent = '🔍 Wykryj format automatycznie';
    }
}

// Select destination
function selectDestination(card) {
    // Remove previous selection
    elements.destinationCards.forEach(c => c.classList.remove('selected'));
    
    // Add selection
    card.classList.add('selected');
    state.selectedDestination = card.dataset.destination;
}

// Transform data
async function transformData() {
    // Validation
    if (!state.inputText) {
        alert('Wprowadź dane wejściowe!');
        return;
    }

    if (!state.selectedDestination) {
        alert('Wybierz destinację!');
        return;
    }

    // Show results section
    elements.resultsSection.style.display = 'block';
    elements.resultsSection.scrollIntoView({ behavior: 'smooth' });
    
    // Show loading
    elements.loading.style.display = 'block';
    elements.errorMessage.style.display = 'none';
    elements.resultsContent.style.display = 'none';

    try {
        const response = await fetch('/api/transform', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                content: state.inputText,
                format: state.selectedFormat,
                destination: state.selectedDestination,
                options: {
                    project_name: state.projectName || 'my-project',
                    author: state.author || 'Unknown',
                    description: state.description || 'Project description',
                    license: state.license,
                    preview: state.previewMode
                }
            })
        });

        const data = await response.json();

        if (data.success) {
            displayResults(data.result);
        } else {
            showError(data.error || 'Nieznany błąd');
        }
    } catch (error) {
        console.error('Error transforming data:', error);
        showError('Błąd połączenia z serwerem');
    } finally {
        elements.loading.style.display = 'none';
    }
}

// Display results
function displayResults(result) {
    elements.resultsContent.style.display = 'block';
    elements.resultsContent.classList.add('fade-in');

    // Stats
    elements.filesCount.textContent = result.files_count || 0;
    elements.destinationType.textContent = result.destination || '-';

    // File tree
    elements.fileTree.textContent = result.file_tree || '';

    // Files list
    elements.filesList.innerHTML = '';
    
    if (result.files) {
        Object.entries(result.files).forEach(([path, content]) => {
            const fileItem = createFilePreview(path, content);
            elements.filesList.appendChild(fileItem);
        });
    }
}

function createFilePreview(path, content) {
    const item = document.createElement('div');
    item.className = 'file-preview-item';

    const header = document.createElement('div');
    header.className = 'file-preview-header';
    header.innerHTML = `
        <span>📄 ${path}</span>
        <span>${content.length} bytes</span>
    `;

    const contentDiv = document.createElement('div');
    contentDiv.className = 'file-preview-content';
    contentDiv.style.display = 'none';
    
    const pre = document.createElement('pre');
    pre.textContent = content.substring(0, 1000) + (content.length > 1000 ? '\n\n[...truncated...]' : '');
    contentDiv.appendChild(pre);

    header.addEventListener('click', () => {
        const isHidden = contentDiv.style.display === 'none';
        contentDiv.style.display = isHidden ? 'block' : 'none';
    });

    item.appendChild(header);
    item.appendChild(contentDiv);

    return item;
}

function showError(message) {
    elements.errorMessage.style.display = 'block';
    elements.errorText.textContent = message;
}

// Download results
function downloadResults() {
    alert('Funkcja pobierania będzie dostępna wkrótce!\n\nW trybie preview pliki nie są fizycznie generowane.\nWyłącz "Tryb podglądu" aby zapisać pliki na serwerze.');
}

// Initialize app
document.addEventListener('DOMContentLoaded', init);
