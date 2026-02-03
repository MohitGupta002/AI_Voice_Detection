from ml.models.wav2vec2_extractor import Wav2Vec2Extractor
from ml.models.voice_classifier import VoiceClassifier


def predict_voice(audio_bytes: bytes, language: str) -> dict:
    """
    Input:
      audio_bytes: raw MP3 bytes
      language: Tamil / English / Hindi / Malayalam / Telugu

    Output:
      {
        "classification": "AI_GENERATED" or "HUMAN",
        "confidenceScore": float (0.0 - 1.0),
        "explanation": str
      }
    """
    pass
