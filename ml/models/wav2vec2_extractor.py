import torch
from transformers import Wav2Vec2Model

class Wav2Vec2Extractor:
    def __init__(self, model_name: str = "facebook/wav2vec2-base"):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = Wav2Vec2Model.from_pretrained(
            model_name,
            use_safetensors=True
        )
        self.model.to(self.device)
        self.model.eval()

    @torch.no_grad()
    def extract(self, waveform) -> torch.Tensor:
        """
        waveform: np.ndarray or torch.Tensor, shape [T]
        returns: torch.Tensor, shape [T', 768]
        """
        if not torch.is_tensor(waveform):
            waveform = torch.from_numpy(waveform)

        if waveform.dim() == 1:
            waveform = waveform.unsqueeze(0)

        waveform = waveform.to(self.device)
        outputs = self.model(waveform)
        return outputs.last_hidden_state.squeeze(0)

    def mean_pool(self, features: torch.Tensor) -> torch.Tensor:
        """
        features: torch.Tensor of shape [T, 768]
        returns: torch.Tensor of shape [768]
        """
        return features.mean(dim=0)
