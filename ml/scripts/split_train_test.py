import shutil
import random
from pathlib import Path

RANDOM_SEED = 42
TEST_SAMPLES_PER_CLASS = 50

random.seed(RANDOM_SEED)

LANGUAGES = ["english", "hindi", "tamil", "malayalam", "telugu"]
CLASSES = ["human", "ai"]

BASE_FEATURES = Path("data/features")
TRAIN_DIR = BASE_FEATURES / "train"
TEST_DIR = BASE_FEATURES / "test"

def split_language(lang, cls):
    src = TRAIN_DIR / lang / cls
    dst = TEST_DIR / lang / cls

    dst.mkdir(parents=True, exist_ok=True)

    files = list(src.glob("*.pt"))
    assert len(files) >= TEST_SAMPLES_PER_CLASS, f"Not enough files for {lang}/{cls}"

    test_files = random.sample(files, TEST_SAMPLES_PER_CLASS)

    for f in test_files:
        shutil.move(str(f), dst / f.name)

    print(f"[OK] {lang}/{cls}: moved {len(test_files)} files to test")

def main():
    for lang in LANGUAGES:
        for cls in CLASSES:
            split_language(lang, cls)

    print("\n✅ Train/Test split completed safely")

if __name__ == "__main__":
    main()
