"""Speech-to-text transcription using faster-whisper (runs locally)."""

import os
import platform
from faster_whisper import WhisperModel


# Whisper model sizes: tiny, base, small, medium, large-v3
# Larger = more accurate but slower and more VRAM/RAM
DEFAULT_MODEL_SIZE = "medium"


def _default_compute_type(device):
    """Pick the best compute type for the current platform."""
    if device == "cuda":
        return "float16"
    # CTranslate2 CPU backend only supports int8 and float32
    return "int8"


def _default_cpu_threads():
    """Use all performance cores on Apple Silicon, otherwise let CTranslate2 decide."""
    if platform.system() == "Darwin" and platform.machine() == "arm64":
        # Use all available cores; os.cpu_count() includes efficiency cores
        # but CTranslate2 benefits from using them all
        return os.cpu_count() or 0
    return 0  # 0 = CTranslate2 default


def transcribe(video_path, model_size=DEFAULT_MODEL_SIZE, language=None, device="auto", beam_size=1, compute_type=None):
    """Transcribe audio from a video/audio file using Whisper.

    Args:
        video_path: Path to the video or audio file.
        model_size: Whisper model size (tiny/base/small/medium/large-v3).
        language: Source language code (e.g. 'en'). None = auto-detect.
        device: 'auto', 'cpu', or 'cuda'.
        beam_size: Beam size for decoding (1=greedy, lower=less RAM).
        compute_type: Data type for inference (auto/int8/float16/float32).

    Returns:
        Tuple of (segments_list, detected_language) where segments_list is
        a list of dicts with 'start', 'end', 'text' keys.
    """
    if not os.path.isfile(video_path):
        raise FileNotFoundError(f"Input file not found: {video_path}")

    if compute_type is None or compute_type == "auto":
        compute_type = _default_compute_type(device)

    cpu_threads = _default_cpu_threads()

    print(f"Loading Whisper model '{model_size}' (device={device}, compute={compute_type})...")
    model = WhisperModel(model_size, device=device, compute_type=compute_type, cpu_threads=cpu_threads)

    print(f"Transcribing: {video_path}")
    segments_iter, info = model.transcribe(
        video_path,
        language=language,
        beam_size=beam_size,
        vad_filter=True,
    )

    detected_lang = info.language
    print(f"Detected language: {detected_lang} (probability {info.language_probability:.2f})")

    segments = []
    for seg in segments_iter:
        segments.append({
            "start": seg.start,
            "end": seg.end,
            "text": seg.text,
        })
        print(f"  [{seg.start:.1f}s -> {seg.end:.1f}s] {seg.text.strip()}")

    print(f"Transcription complete: {len(segments)} segments")
    return segments, detected_lang
