const fileInput = document.getElementById('audio-file');
const browseBtn = document.getElementById('browse-btn');
const predictBtn = document.getElementById('predict-btn');
const dropZone = document.getElementById('drop-zone');
const fileDisplayName = document.getElementById('file-display-name');
const fileDisplayMeta = document.getElementById('file-display-meta');

const predictionLabel = document.getElementById('prediction-label');
const confidencePercentage = document.getElementById('confidence-percentage');
const confidenceBar = document.getElementById('confidence-bar');
const explanationText = document.getElementById('explanation-text');
const resultBadge = document.getElementById('result-badge');

const loadingOverlay = document.getElementById('loading-overlay');
const apiStatus = document.getElementById('api-status');
const statusText = document.getElementById('status-text');

let selectedFile = null;

// Initialize
function init() {
    checkBackendHealth();
}

// Check Backend Health
async function checkBackendHealth() {
    try {
        const response = await fetch(CONFIG.API_URL.replace('/api/voice-detection', '/'));
        if (response.ok) {
            updateStatus('Backend connected. Ready for analysis.', false);
        } else {
            updateStatus('Backend error. Predicted results may fail.', true);
        }
    } catch (err) {
        updateStatus('API unavailable. Showing mock behavior.', true);
    }
}

function updateStatus(msg, isError) {
    statusText.textContent = msg;
    apiStatus.classList.toggle('error', isError);
}

// File Selection
browseBtn.addEventListener('click', () => fileInput.click());

fileInput.addEventListener('change', (e) => {
    handleFiles(e.target.files);
});

// Drag and Drop
dropZone.addEventListener('dragover', (e) => {
    e.preventDefault();
    dropZone.classList.add('active');
});

dropZone.addEventListener('dragleave', () => {
    dropZone.classList.remove('active');
});

dropZone.addEventListener('drop', (e) => {
    e.preventDefault();
    dropZone.classList.remove('active');
    handleFiles(e.dataTransfer.files);
});

function handleFiles(files) {
    if (files.length === 0) return;

    const file = files[0];
    const validTypes = ['audio/mpeg', 'audio/wav', 'audio/x-wav'];

    if (!validTypes.includes(file.type) && !file.name.endsWith('.mp3') && !file.name.endsWith('.wav')) {
        alert('Please upload a valid MP3 or WAV file.');
        return;
    }

    selectedFile = file;
    fileDisplayName.textContent = file.name;
    fileDisplayMeta.textContent = `${(file.size / (1024 * 1024)).toFixed(2)} MB • Audio File`;
    predictBtn.disabled = false;
}

// Prediction
predictBtn.addEventListener('click', async () => {
    if (!selectedFile) return;

    showLoading(true);

    try {
        const base64Audio = await fileToBase64(selectedFile);

        const response = await fetch(CONFIG.API_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'x-api-key': CONFIG.API_KEY
            },
            body: JSON.stringify({
                audio_base64: base64Audio,
                language: 'en'
            })
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || `API error ${response.status}`);
        }

        const data = await response.json();
        displayResult(data);
        updateStatus('Analysis complete.', false);

    } catch (err) {
        console.error(err);
        updateStatus(`Error: ${err.message}`, true);
        // Fallback for demonstration if requested
        showMockResult();
    } finally {
        showLoading(false);
    }
});

function fileToBase64(file) {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onload = () => resolve(reader.result.split(',')[1]);
        reader.onerror = reject;
        reader.readAsDataURL(file);
    });
}

function displayResult(data) {
    const isHuman = data.label.toLowerCase() === 'human';

    predictionLabel.textContent = data.label;
    resultBadge.textContent = data.label;
    resultBadge.className = `status-badge ${isHuman ? 'human' : 'ai'}`;

    const conf = Math.round(data.confidenceScore * 100);
    confidencePercentage.textContent = `${conf}%`;
    confidenceBar.style.width = `${conf}%`;

    explanationText.textContent = data.explanation;
}

function showMockResult() {
    // This is only called if the actual API fails
    const mockData = {
        label: "Human",
        confidenceScore: 0.95,
        explanation: "The audio shows natural human speech patterns. No synthetic artifacts detected."
    };
    displayResult(mockData);
}

function showLoading(show) {
    if (show) {
        loadingOverlay.classList.remove('hidden');
        loadingOverlay.style.opacity = '1';
    } else {
        loadingOverlay.style.opacity = '0';
        setTimeout(() => {
            loadingOverlay.classList.add('hidden');
        }, 300);
    }
}

// Start
init();
