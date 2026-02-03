import io
import numpy as np
import librosa

TARGET_SAMPLE_RATE = 16000


def mp3_bytes_to_wav_tensor(mp3_bytes: bytes) -> np.ndarray:
    """
    Convert MP3 bytes to normalized mono waveform (float32).

    Returns:
        np.ndarray of shape (n_samples,)
    """

    audio_buffer = io.BytesIO(mp3_bytes)

    waveform, sr = librosa.load(
        audio_buffer,
        sr=TARGET_SAMPLE_RATE,
        mono=True
    )

    waveform = waveform.astype(np.float32)

    peak = np.max(np.abs(waveform))
    if peak > 0:
        waveform = waveform / peak

    return waveform
