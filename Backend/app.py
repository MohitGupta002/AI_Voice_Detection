import os
import base64
from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel

api = FastAPI(title="Voice Detection API")

# Request schema (contract)
class VoiceRequest(BaseModel):
    audio_base64: str   # Base64 encoded audio (mp3/wav)
    language: str       # e.g. "en", "hi"

# ML Stub (temporary placeholder)
def dummy_ml_function(audio_bytes: bytes):
    return {
        "label": "Human",
        "confidenceScore": 0.85,
        "explanation": "Stub prediction (ML model not integrated yet)"
    }

@api.get("/")
def root():
    return {"status": "Backend running"}

@api.post("/api/voice-detection")
async def voice_detection(
    payload: VoiceRequest,
    x_api_key: str = Header(..., alias="x-api-key")
):
    # API key from environment variable
    API_KEY = os.getenv("API_KEY")
    if not API_KEY:
        raise HTTPException(status_code=500, detail="API_KEY not set in environment variables")

    # 1) API Key validation
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")

    # 2) Base64 validation & decode
    try:
        audio_bytes = base64.b64decode(payload.audio_base64)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid base64 audio data")

    if not audio_bytes:
        raise HTTPException(status_code=400, detail="Empty audio data")

    # Optional size limit (5 MB)
    if len(audio_bytes) > 5 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="Audio file too large (max 5MB)")

    # 3) Call ML stub
    result = dummy_ml_function(audio_bytes)

    # 4) Return response
    return result
