"""SRT subtitle file handling."""

import os
import pysrt


def write_srt(segments, output_path):
    """Write transcription segments to an SRT file.

    Args:
        segments: List of dicts with 'start', 'end' (seconds) and 'text' keys.
        output_path: Path to write the SRT file.
    """
    subs = pysrt.SubRipFile()

    for i, seg in enumerate(segments, start=1):
        start = pysrt.SubRipTime.from_ordinal(int(seg["start"] * 1000))
        end = pysrt.SubRipTime.from_ordinal(int(seg["end"] * 1000))
        item = pysrt.SubRipItem(index=i, start=start, end=end, text=seg["text"].strip())
        subs.append(item)

    subs.save(output_path, encoding="utf-8")
    return output_path


def read_srt(path):
    """Read an SRT file and return a pysrt SubRipFile object."""
    if not os.path.isfile(path):
        raise FileNotFoundError(f"Subtitle file not found: {path}")
    return pysrt.open(path, encoding="utf-8")


def save_srt(subs, output_path):
    """Save a pysrt SubRipFile to disk."""
    subs.save(output_path, encoding="utf-8")
    return output_path
