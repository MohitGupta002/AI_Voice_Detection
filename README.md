AI Generated Voice Detection

Input: Base64 encoded MP3
Preprocessing: MP3 → WAV (16kHz, mono)
Feature extraction: wav2vec2 embeddings
Model: Binary classifier (AI vs Human)
Output: classification, confidenceScore, explanation
