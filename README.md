# 🎙️ AI-Generated Voice Detection

## 📋 Problem Statement

With the rise of AI-generated audio tools, distinguishing between human and AI-created voices is becoming increasingly important for applications like content verification, security, and media authenticity. This project demonstrates a simple system to classify uploaded audio samples as either human or AI-generated, helping users identify potential synthetic content.

## 🚀 Demo Overview

The demo provides a straightforward web interface where users can:
- 📤 Upload an MP3 audio file
- 🔍 Click "Predict" to analyze the sample
- 📊 View the classification result, including prediction label, confidence percentage, and a brief explanation

The interface includes loading states and error handling for a smooth user experience.

## 🏗️ High-Level Approach

The system follows a client-server architecture:
- **Frontend**: Handles file upload, converts audio to Base64, sends requests to the backend
- **Backend**: Processes the audio data and interfaces with the machine learning model
- **Model**: Classifies the audio based on learned patterns (details not covered here)

No complex preprocessing or model training is performed in this demo.

## 📐 System Architecture

```
[User Browser]
     |
     | (Upload Audio)
     v
[Frontend (HTML/CSS/JS)]
     |
     | (POST /predict with Base64 audio)
     v
[Backend API (Flask/Python)]
     |
     | (Process audio, run model)
     v
[ML Model (Pre-trained)]
     |
     | (Return prediction)
     v
[Backend API]
     |
     | (JSON response: prediction, confidence, explanation)
     v
[Frontend]
     |
     | (Display result to user)
     v
[User Browser]
```

## 📁 Dataset Description

The dataset is organized into two main categories:
- **Human Samples**: Recordings of real human voices
- **AI-Generated Samples**: Synthetic audio created by AI tools

**Key principles:**
- **Same-Text Principle**: Both human and AI samples use identical text content to ensure fair comparison
- **Clean Structure**: Files are stored in clearly labeled folders (`human/` and `ai/`) with consistent naming conventions
- **Format Consistency**: All audio files are in WAV or MP3 format for easy processing

The dataset focuses on quality over quantity, with representative samples for demonstration purposes.

## ⚠️ Limitations

> This demo has several realistic constraints:
> - Limited to WAV and MP3 formats only
> - Requires a running backend server for full functionality (includes mock fallback for offline testing)
> - Classification accuracy depends on the backend model and may not generalize to all audio types
> - No real-time processing; analysis happens after upload
> - Designed for short audio clips; longer files may not perform well

## 🛠️ Tech Stack

| Component          | Technology                          |
|--------------------|-------------------------------------|
| Frontend           | HTML5, CSS3, Vanilla JavaScript     |
| API Integration    | Fetch API for HTTP requests         |
| Audio Handling     | Browser-based Base64 encoding       |
| Styling            | Clean, responsive design           |

## ▶️ How to Run the Demo

1. Configure the API settings in `config.js`:
   - Set `API_URL` to your backend endpoint (default: `http://localhost:5000/predict`)
   - Set `USE_MOCK` to `true` for offline demo or `false` for live API

2. Open `index.html` in a modern web browser.

3. Select an audio file (WAV or MP3) using the file input.

4. Click "Predict" to analyze the file.

5. View the result showing prediction, confidence bar, and explanation.

*If the backend is unavailable, the system automatically falls back to mock results for demonstration.*

## 🛡️ Ethical Note and Disclaimer

> This project is intended for educational and demonstration purposes only. AI voice detection technology should be used responsibly and with awareness of its limitations. False positives or negatives can occur, and this tool is not a substitute for professional verification methods. Always consider the broader implications of audio classification in real-world applications, including privacy concerns and potential misuse.

---

*This README reflects the frontend and organizational aspects of the project. Backend and model details are handled separately.*
