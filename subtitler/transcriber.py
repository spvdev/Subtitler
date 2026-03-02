"""Speech-to-text transcription using faster-whisper (runs locally)."""

import os
from faster_whisper import WhisperModel


# Whisper model sizes: tiny, base, small, medium, large-v3
# Larger = more accurate but slower and more VRAM/RAM
DEFAULT_MODEL_SIZE = "medium"


def transcribe(video_path, model_size=DEFAULT_MODEL_SIZE, language=None, device="auto"):
    """Transcribe audio from a video/audio file using Whisper.

    Args:
        video_path: Path to the video or audio file.
        model_size: Whisper model size (tiny/base/small/medium/large-v3).
        language: Source language code (e.g. 'en'). None = auto-detect.
        device: 'auto', 'cpu', or 'cuda'.

    Returns:
        Tuple of (segments_list, detected_language) where segments_list is
        a list of dicts with 'start', 'end', 'text' keys.
    """
    if not os.path.isfile(video_path):
        raise FileNotFoundError(f"Input file not found: {video_path}")

    compute_type = "float16" if device == "cuda" else "int8"
    if device == "auto":
        compute_type = "int8"

    print(f"Loading Whisper model '{model_size}' (device={device})...")
    model = WhisperModel(model_size, device=device, compute_type=compute_type)

    print(f"Transcribing: {video_path}")
    segments_iter, info = model.transcribe(
        video_path,
        language=language,
        beam_size=5,
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
