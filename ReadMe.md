# 🎙️ AI Voice Detection

A premium web application that uses machine learning to classify audio files as **Human** or **AI-Generated** voice.

![AI Voice Detection](https://img.shields.io/badge/AI-Voice%20Detection-blue)
![Python](https://img.shields.io/badge/Python-3.10+-green)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-teal)

## ✨ Features

- 🎯 **Real-time Audio Classification** - Detect AI-generated vs human voices
- 🎨 **Premium Dark UI** - Modern glassmorphism design with smooth animations
- 📁 **Multiple Format Support** - Accepts MP3 and WAV files (auto-converts WAV to MP3)
- 🔒 **Secure API** - API key authentication
- 🚀 **Fast Inference** - GPU-accelerated predictions (falls back to CPU)
- 📊 **Confidence Scores** - Detailed analysis with confidence percentages

## 🏗️ Project Structure

```
AI_Voice_Detection/
├── frontend/           # Premium web interface
│   ├── index.html     # Main HTML structure
│   ├── style.css      # Modern dark theme styling
│   ├── script.js      # Frontend logic & API calls
│   └── config.js      # API configuration
├── Backend/           # FastAPI server
│   └── app.py        # API endpoints & ML integration
├── ml/               # Machine learning models
│   ├── models/       # Trained model files
│   └── ...
└── requirements.txt  # Python dependencies
```

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- pip
- ffmpeg (for WAV to MP3 conversion)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/AI_Voice_Detection.git
   cd AI_Voice_Detection
   ```

2. **Create virtual environment**
   ```bash
   python -m venv .venv
   
   # Windows
   .\.venv\Scripts\activate
   
   # Linux/Mac
   source .venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install ffmpeg** (required for WAV conversion)
   
   **Windows (using Chocolatey):**
   ```bash
   choco install ffmpeg
   ```
   
   **Or download manually:** [ffmpeg.org/download.html](https://ffmpeg.org/download.html)
   
   **Linux:**
   ```bash
   sudo apt install ffmpeg
   ```
   
   **Mac:**
   ```bash
   brew install ffmpeg
   ```

5. **Download the ML model**
   
   The model file (`voice_classifier.pt`) is not included in the repo due to size.
   - Download it from [releases](https://github.com/YOUR_USERNAME/AI_Voice_Detection/releases)
   - Place it in `ml/models/voice_classifier.pt`

### Running Locally

1. **Start the backend**
   ```bash
   # From project root
   .\.venv\Scripts\python -m uvicorn Backend.app:api --reload
   ```
   
   The API will be available at `http://127.0.0.1:8000`

2. **Open the frontend**
   
   Open `frontend/index.html` in your browser, or use a local server:
   ```bash
   # Using Python's built-in server
   cd frontend
   python -m http.server 5500
   ```
   
   Then visit `http://localhost:5500`

## 🌐 Deployment Guide

### Option 1: Deploy on Render (Recommended for Backend)

1. **Create a `render.yaml`** in your project root (see below)
2. Push to GitHub
3. Go to [render.com](https://render.com) → New → Web Service
4. Connect your GitHub repo
5. Render will auto-deploy using the configuration

### Option 2: Deploy Frontend on Vercel/Netlify

**Frontend (Vercel):**
1. Push to GitHub
2. Go to [vercel.com](https://vercel.com)
3. Import your repo
4. Set build directory to `frontend`
5. Deploy!

**Frontend (Netlify):**
1. Go to [netlify.com](https://netlify.com)
2. Drag & drop the `frontend` folder
3. Done!

**Backend (Railway/Render):**
1. Push to GitHub
2. Connect to [railway.app](https://railway.app) or [render.com](https://render.com)
3. Deploy the backend service
4. Update `frontend/config.js` with your deployed backend URL

### Option 3: Deploy on Hugging Face Spaces

Perfect for ML projects!

1. Create a new Space on [huggingface.co/spaces](https://huggingface.co/spaces)
2. Choose "Gradio" or "Streamlit" SDK
3. Push your code
4. Add model files to the repo

## ⚙️ Configuration

### Backend Configuration

Edit `Backend/app.py` or set environment variables:

```bash
# API Key (default: "my-secret-key")
export API_KEY="your-secret-key"
```

### Frontend Configuration

Edit `frontend/config.js`:

```javascript
const CONFIG = {
    API_URL: 'http://127.0.0.1:8000/api/voice-detection',  // Change to your deployed backend URL
    API_KEY: 'my-secret-key'  // Match your backend API key
};
```

## 📝 API Documentation

### Endpoint: `/api/voice-detection`

**Method:** POST

**Headers:**
```json
{
  "Content-Type": "application/json",
  "x-api-key": "your-api-key"
}
```

**Request Body:**
```json
{
  "audio_base64": "base64_encoded_audio_data",
  "language": "en"
}
```

**Response:**
```json
{
  "label": "Human",
  "confidenceScore": 0.95,
  "explanation": "Natural human speech patterns detected with no synthetic artifacts."
}
```

## 🛠️ Technologies Used

### Frontend
- HTML5, CSS3, JavaScript (Vanilla)
- Google Fonts (Outfit)
- Glassmorphism UI Design

### Backend
- FastAPI
- PyTorch
- Transformers (Wav2Vec2)
- Librosa
- Pydub

### ML Model
- Wav2Vec2 (facebook/wav2vec2-base)
- Custom Voice Classifier

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📧 Contact

For questions or support, please open an issue on GitHub.

---

Made with ❤️ by [Your Name](https://github.com/YOUR_USERNAME)