from ml.preprocessing.audio_preprocessor import mp3_bytes_to_wav_tensor
from ml.models.wav2vec2_extractor import Wav2Vec2Extractor

from pathlib import Path
import random
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader, ConcatDataset
import matplotlib.pyplot as plt
import numpy as np

# =========================
# CONFIG
# =========================
LANGUAGES = ["english", "hindi", "tamil", "malayalam", "telugu"]

FEATURE_ROOT = Path("data/features")
MODEL_PATH = Path("models/voice_classifier.pt")
OUTPUT_DIR = Path("outputs")

FEATURE_DIM = 768
BATCH_SIZE = 64
EPOCHS = 25
LR = 5e-4
SEED = 42

TRAIN_PER_LANG = 950
TEST_PER_LANG  = 50
# =========================

random.seed(SEED)
torch.manual_seed(SEED)
OUTPUT_DIR.mkdir(exist_ok=True)


# -------------------------
# DATASET
# -------------------------
class FeatureDataset(Dataset):
    def __init__(self, files, label):
        self.files = files
        self.label = label

    def __len__(self):
        return len(self.files)

    def __getitem__(self, idx):
        x = torch.load(self.files[idx], weights_only=True)
        y = torch.tensor(self.label, dtype=torch.float32)
        return x, y


# -------------------------
# MODEL
# -------------------------
class VoiceClassifier(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(FEATURE_DIM, 512),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(512, 256),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(256, 1)
        )

    def forward(self, x):
        return self.net(x).squeeze(1)


# -------------------------
# DATA LOADER
# -------------------------
def collect_multilingual_files():
    train_human, train_ai = [], []
    test_human, test_ai = [], []

    required = TRAIN_PER_LANG + TEST_PER_LANG

    for lang in LANGUAGES:
        human = list((FEATURE_ROOT / lang / "human").glob("*.pt"))
        ai = list((FEATURE_ROOT / lang / "ai").glob("*.pt"))

        if len(human) < required or len(ai) < required:
            raise RuntimeError(f"{lang}: insufficient data")

        random.shuffle(human)
        random.shuffle(ai)

        train_human += human[:TRAIN_PER_LANG]
        test_human  += human[TRAIN_PER_LANG:required]

        train_ai += ai[:TRAIN_PER_LANG]
        test_ai  += ai[TRAIN_PER_LANG:required]

    return train_human, train_ai, test_human, test_ai


# -------------------------
# EVALUATION
# -------------------------
def evaluate(model, loader, device):
    model.eval()
    tp = tn = fp = fn = 0

    with torch.no_grad():
        for x, y in loader:
            x, y = x.to(device), y.to(device)
            preds = (torch.sigmoid(model(x)) >= 0.5).float()

            tp += ((preds == 1) & (y == 1)).sum().item()
            tn += ((preds == 0) & (y == 0)).sum().item()
            fp += ((preds == 1) & (y == 0)).sum().item()
            fn += ((preds == 0) & (y == 1)).sum().item()

    acc = (tp + tn) / (tp + tn + fp + fn)
    prec = tp / (tp + fp + 1e-8)
    rec = tp / (tp + fn + 1e-8)
    f1 = 2 * prec * rec / (prec + rec + 1e-8)

    return acc, prec, rec, f1, tp, tn, fp, fn


# -------------------------
# PLOTTING
# -------------------------
def save_confusion_matrix(tp, tn, fp, fn):
    cm = np.array([[tn, fp],
                   [fn, tp]])

    plt.figure()
    plt.imshow(cm)
    plt.colorbar()
    plt.xticks([0, 1], ["Human", "AI"])
    plt.yticks([0, 1], ["Human", "AI"])
    plt.xlabel("Predicted")
    plt.ylabel("Actual")

    for i in range(2):
        for j in range(2):
            plt.text(j, i, cm[i, j], ha="center", va="center")

    plt.title("Confusion Matrix (AI vs Human)")
    plt.savefig(OUTPUT_DIR / "confusion_matrix.png")
    plt.close()


def save_metric_bar(acc, prec, rec, f1):
    labels = ["Accuracy", "Precision", "Recall", "F1"]
    values = [acc, prec, rec, f1]

    plt.figure()
    plt.bar(labels, values)
    plt.ylim(0, 1)
    plt.title("Model Performance Metrics")
    plt.savefig(OUTPUT_DIR / "metrics.png")
    plt.close()


# -------------------------
# MAIN
# -------------------------
def main():
    if MODEL_PATH.exists():
        print("Model already trained. Delete model to retrain.")
        return

    train_h, train_a, test_h, test_a = collect_multilingual_files()

    train_ds = ConcatDataset([
        FeatureDataset(train_h, 0),
        FeatureDataset(train_a, 1)
    ])
    test_ds = ConcatDataset([
        FeatureDataset(test_h, 0),
        FeatureDataset(test_a, 1)
    ])

    train_loader = DataLoader(train_ds, batch_size=BATCH_SIZE, shuffle=True)
    test_loader = DataLoader(test_ds, batch_size=BATCH_SIZE)

    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = VoiceClassifier().to(device)
    opt = torch.optim.Adam(model.parameters(), lr=LR)
    loss_fn = nn.BCEWithLogitsLoss()

    for e in range(EPOCHS):
        model.train()
        loss_sum = 0
        for x, y in train_loader:
            x, y = x.to(device), y.to(device)
            loss = loss_fn(model(x), y)
            opt.zero_grad()
            loss.backward()
            opt.step()
            loss_sum += loss.item()
        print(f"Epoch {e+1}/{EPOCHS} | Loss: {loss_sum:.4f}")

    acc, prec, rec, f1, tp, tn, fp, fn = evaluate(model, test_loader, device)

    print("\nMetrics:")
    print(f"Accuracy : {acc:.4f}")
    print(f"Precision: {prec:.4f}")
    print(f"Recall   : {rec:.4f}")
    print(f"F1 Score : {f1:.4f}")

    save_confusion_matrix(tp, tn, fp, fn)
    save_metric_bar(acc, prec, rec, f1)

    MODEL_PATH.parent.mkdir(exist_ok=True)
    torch.save(model.state_dict(), MODEL_PATH)
    print("Model & plots saved.")


if __name__ == "__main__":
    main()
