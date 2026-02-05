import os
import torch
import librosa
from tqdm import tqdm
from ml.models.wav2vec2_extractor import Wav2Vec2Extractor

# =========================
# PATH CONFIG
# =========================

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../")
)

RAW_DATA_DIR = os.path.join(PROJECT_ROOT, "data", "raw")
FEATURE_DATA_DIR = os.path.join(PROJECT_ROOT, "data", "features")

SUPPORTED_EXT = (".mp3", ".wav")
TARGET_SR = 16000


# =========================
# AUDIO LOADER
# =========================

def load_audio(path: str) -> torch.Tensor:
    waveform, _ = librosa.load(path, sr=TARGET_SR, mono=True)
    return torch.tensor(waveform, dtype=torch.float32)


# =========================
# FEATURE EXTRACTION
# =========================

def extract_all_features():
    extractor = Wav2Vec2Extractor()
    os.makedirs(FEATURE_DATA_DIR, exist_ok=True)

    languages = sorted(os.listdir(RAW_DATA_DIR))

    for lang in languages:
        lang_raw_path = os.path.join(RAW_DATA_DIR, lang)
        if not os.path.isdir(lang_raw_path):
            continue

        print(f"\n=== LANGUAGE: {lang.upper()} ===")

        for label in ["ai", "human"]:
            input_dir = os.path.join(lang_raw_path, label)
            if not os.path.isdir(input_dir):
                print(f"[SKIP] Missing: {lang}/{label}")
                continue

            output_dir = os.path.join(FEATURE_DATA_DIR, lang, label)
            os.makedirs(output_dir, exist_ok=True)

            audio_files = [
                f for f in os.listdir(input_dir)
                if f.lower().endswith(SUPPORTED_EXT)
            ]

            print(f"{lang}/{label} → {len(audio_files)} files")

            for fname in tqdm(audio_files, desc=f"{lang}-{label}", ncols=100):
                audio_path = os.path.join(input_dir, fname)
                feature_path = os.path.join(
                    output_dir,
                    os.path.splitext(fname)[0] + ".pt"
                )

                # ===== SKIP IF ALREADY DONE =====
                if os.path.exists(feature_path):
                    continue

                try:
                    waveform = load_audio(audio_path)
                    features = extractor.extract(waveform)
                    pooled = extractor.mean_pool(features)

                    torch.save(pooled.cpu(), feature_path)

                except Exception as e:
                    print(f"[ERROR] {audio_path} → {str(e)}")


# =========================
# ENTRY POINT
# =========================

if __name__ == "__main__":
    extract_all_features()
