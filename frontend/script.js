// Configurable API URL
const API_URL = 'http://localhost:5000/predict';

// Mock response for demo purposes
const mockResponse = {
    prediction: 'Human',
    confidence: 95,
    explanation: 'The audio shows natural human speech patterns.'
};

// DOM elements
const fileInput = document.getElementById('audio-file');
const predictBtn = document.getElementById('predict-btn');
const loadingDiv = document.getElementById('loading');
const resultDiv = document.getElementById('result');
const errorDiv = document.getElementById('error');
const predictionSpan = document.getElementById('prediction');
const confidenceSpan = document.getElementById('confidence');
const explanationSpan = document.getElementById('explanation');

// Enable/disable predict button based on file selection
fileInput.addEventListener('change', () => {
    const file = fileInput.files[0];
    if (file) {
        // Check if file is MP3
        const isMP3 = file.type === 'audio/mpeg' && file.name.toLowerCase().endsWith('.mp3');
        if (isMP3) {
            predictBtn.disabled = false;
            hideError();
        } else {
            predictBtn.disabled = true;
            showError('Only MP3 files are supported. Please select a valid MP3 file.');
        }
    } else {
        predictBtn.disabled = true;
        hideError();
    }
});

// Handle predict button click
predictBtn.addEventListener('click', async () => {
    const file = fileInput.files[0];
    if (!file) {
        showError('No file selected.');
        return;
    }

    // Show loading
    showLoading(true);
    hideResult();
    hideError();

    try {
        let data;

        if (CONFIG.USE_MOCK) {
            // Simulate API delay for mock
            await new Promise(resolve => setTimeout(resolve, 1000));
            data = mockResponse;
        } else {
            // Convert file to Base64
            const base64Audio = await fileToBase64(file);

            // Send POST request
            const response = await fetch(CONFIG.API_URL, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ audio: base64Audio })
            });

            if (!response.ok) {
                throw new Error(`API error: ${response.status}`);
            }

            data = await response.json();
        }

        displayResult(data);
    } catch (error) {
        console.error('Error:', error);
        // Use mock response if API fails
        displayResult(mockResponse);
        showError('API unavailable. Showing mock result.');
    } finally {
        showLoading(false);
    }
});

// Utility functions
function fileToBase64(file) {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onload = () => resolve(reader.result.split(',')[1]); // Remove data URL prefix
        reader.onerror = reject;
        reader.readAsDataURL(file);
    });
}

function showLoading(show) {
    loadingDiv.classList.toggle('hidden', !show);
}

function hideResult() {
    resultDiv.classList.add('hidden');
}

function hideError() {
    errorDiv.classList.add('hidden');
    errorDiv.textContent = '';
}

function showError(message) {
    errorDiv.textContent = message;
    errorDiv.classList.remove('hidden');
}

function displayResult(data) {
    predictionSpan.textContent = data.prediction;
    const confidenceFill = document.getElementById('confidence-fill');
    const confidenceText = document.getElementById('confidence-text');
    confidenceFill.style.width = `${data.confidence}%`;
    confidenceText.textContent = `${data.confidence}%`;
    explanationSpan.textContent = data.explanation;
    resultDiv.classList.remove('hidden');
}
