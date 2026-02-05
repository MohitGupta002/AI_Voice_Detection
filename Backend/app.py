import os
import base64
from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel

from fastapi.middleware.cors import CORSMiddleware

# FastAPI app
api = FastAPI(title="AI Voice Detection API")

# Add CORS middleware
api.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

import sys
import tempfile
import torch
import io
import soundfile as sf
import numpy as np

# Add project root to path for ML imports
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from ml.models.voice_classifier import VoiceClassifier
from ml.models.wav2vec2_extractor import Wav2Vec2Extractor

# --- Model Initialization ---
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
MODEL_PATH = os.path.join(ROOT_DIR, "ml/models/voice_classifier.pt")

import traceback

print(f"Loading ML models on {DEVICE}...")
model = VoiceClassifier()
try:
    state = torch.load(MODEL_PATH, map_location=DEVICE)
    model.load_state_dict(state)
    model.to(DEVICE)
    model.eval()
    print("Base model loaded. Loading feature extractor...")
    extractor = Wav2Vec2Extractor()
    print("All models loaded successfully.")
except Exception as e:
    print(f"--- ERROR LOADING MODELS ---")
    traceback.print_exc()
    print(f"-----------------------------")
    model = None
    extractor = None


# -------------------------------
# Request Schema
# -------------------------------
class VoiceRequest(BaseModel):
    audio_base64: str
    language: str


# -------------------------------
# ML Inference Function
# -------------------------------
def run_inference(audio_bytes: bytes):
    if not model or not extractor:
        return {
            "label": "Demo (Human)",
            "confidenceScore": 0.95,
            "explanation": "Models failed to load. Showing mock result."
        }

    # Detect if the audio is WAV and handle it appropriately
    file_suffix = ".mp3"  # Default
    try:
        # Try to detect WAV format (WAV files start with "RIFF" header)
        if audio_bytes[:4] == b'RIFF':
            print("Detected WAV format. Will process directly with librosa.")
            file_suffix = ".wav"
    except Exception as e:
        print(f"Warning: Could not detect audio format: {e}")

    # Save to temp file for librosa (librosa can handle both WAV and MP3)
    with tempfile.NamedTemporaryFile(delete=False, suffix=file_suffix) as tmp:
        tmp.write(audio_bytes)
        tmp_path = tmp.name

    try:
        with torch.no_grad():
            # extractor.extract_from_file already handles moving to its own device
            features = extractor.extract_from_file(tmp_path)
            features = features.unsqueeze(0).to(DEVICE) # Ensure same device as model
            logit = model(features)
            prob_ai = torch.sigmoid(logit)[0].item()

        is_ai = prob_ai > 0.5
        label = "AI-Generated" if is_ai else "Human"
        score = prob_ai if is_ai else (1 - prob_ai)
        
        explanation = (
            "High probability of AI-generated artifacts detected." if is_ai 
            else "Natural human speech patterns detected with no synthetic artifacts."
        )

        return {
            "label": label,
            "confidenceScore": round(score, 4),
            "explanation": explanation
        }
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)


# -------------------------------
# Health Check
# -------------------------------
@api.get("/")
def root():
    return {
        "status": "Backend running",
        "ml_loaded": model is not None
    }


# -------------------------------
# Voice Detection API
# -------------------------------
@api.post("/api/voice-detection")
async def voice_detection(
    payload: VoiceRequest,
    x_api_key: str | None = Header(default=None, alias="x-api-key")
):
    API_KEY = os.getenv("API_KEY", "my-secret-key")

    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")

    try:
        audio_bytes = base64.b64decode(payload.audio_base64)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid base64 audio")

    if not audio_bytes:
        raise HTTPException(status_code=400, detail="Empty audio data")

    # Call real inference
    try:
        result = run_inference(audio_bytes)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
