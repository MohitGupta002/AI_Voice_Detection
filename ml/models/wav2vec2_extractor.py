import torch
import librosa
from transformers import Wav2Vec2Model


class Wav2Vec2Extractor:
    def __init__(self, model_name="facebook/wav2vec2-base"):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = Wav2Vec2Model.from_pretrained(
            model_name,
            use_safetensors=True
        )

        self.model.to(self.device)
        self.model.eval()

    @torch.no_grad()
    def extract(self, waveform: torch.Tensor) -> torch.Tensor:
        if waveform.dim() == 1:
            waveform = waveform.unsqueeze(0)

        waveform = waveform.to(self.device)
        outputs = self.model(waveform)
        return outputs.last_hidden_state.squeeze(0)

    def mean_pool(self, features: torch.Tensor) -> torch.Tensor:
        return features.mean(dim=0)

    # ✅ ADD THIS METHOD (inside the class)
    def extract_from_file(self, file_path: str) -> torch.Tensor:
        waveform, sr = librosa.load(file_path, sr=16000, mono=True)
        waveform = torch.tensor(waveform, dtype=torch.float32)
        features = self.extract(waveform)
        return self.mean_pool(features)
