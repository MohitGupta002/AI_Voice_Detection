import sys
import os
import torch

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
sys.path.append(ROOT_DIR)

from ml.models.voice_classifier import VoiceClassifier
from ml.models.wav2vec2_extractor import Wav2Vec2Extractor

MODEL_PATH = "ml/models/voice_classifier.pt"
AUDIO_PATH = "ml/preprocessing/sample.mp3"

device = "cpu"

model = VoiceClassifier()
state = torch.load(MODEL_PATH, map_location=device)
model.load_state_dict(state)
model.eval()

extractor = Wav2Vec2Extractor()

with torch.no_grad():
    features = extractor.extract_from_file(AUDIO_PATH)
    features = features.unsqueeze(0)

    logit = model(features)
    prob_ai = torch.sigmoid(logit)[0].item()

print({
    "ai_probability": round(prob_ai, 4),
    "prediction": "AI" if prob_ai > 0.5 else "HUMAN"
})
