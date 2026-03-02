"""Command-line interface for Subtitler."""

import argparse
import os
import sys

from subtitler.transcriber import transcribe
from subtitler.subtitle import write_srt, read_srt, save_srt
from subtitler.translator import translate_srt, list_available_packages


def cmd_transcribe(args):
    """Transcribe a video/audio file to SRT subtitles."""
    segments, detected_lang = transcribe(
        args.input,
        model_size=args.model,
        language=args.language,
        device=args.device,
    )

    if not segments:
        print("No speech detected.")
        return

    output = args.output
    if output is None:
        base = os.path.splitext(args.input)[0]
        output = f"{base}.srt"

    write_srt(segments, output)
    print(f"\nSubtitles saved to: {output}")
    print(f"Detected language: {detected_lang}")


def cmd_translate(args):
    """Translate an existing SRT file."""
    subs = read_srt(args.input)

    print(f"Translating {len(subs)} subtitles: {args.source} -> {args.target}")
    translate_srt(subs, args.source, args.target)

    output = args.output
    if output is None:
        base, ext = os.path.splitext(args.input)
        output = f"{base}.{args.target}{ext}"

    save_srt(subs, output)
    print(f"\nTranslated subtitles saved to: {output}")


def cmd_auto(args):
    """Transcribe and then translate in one step."""
    segments, detected_lang = transcribe(
        args.input,
        model_size=args.model,
        language=args.language,
        device=args.device,
    )

    if not segments:
        print("No speech detected.")
        return

    base = os.path.splitext(args.input)[0]

    # Save original-language subtitles
    original_srt = args.output_original
    if original_srt is None:
        original_srt = f"{base}.{detected_lang}.srt"
    write_srt(segments, original_srt)
    print(f"\nOriginal subtitles saved to: {original_srt}")

    # Translate
    source_lang = args.source or detected_lang
    print(f"\nTranslating: {source_lang} -> {args.target}")
    subs = read_srt(original_srt)
    translate_srt(subs, source_lang, args.target)

    translated_srt = args.output_translated
    if translated_srt is None:
        translated_srt = f"{base}.{args.target}.srt"
    save_srt(subs, translated_srt)
    print(f"Translated subtitles saved to: {translated_srt}")


def cmd_languages(args):
    """List available translation language pairs."""
    print("Fetching available language pairs...")
    packages = list_available_packages()
    if not packages:
        print("No packages found. Check your internet connection.")
        return
    print(f"\n{'From':<20} {'Code':<8} {'To':<20} {'Code':<8}")
    print("-" * 58)
    for from_name, from_code, to_name, to_code in sorted(packages):
        print(f"{from_name:<20} {from_code:<8} {to_name:<20} {to_code:<8}")


def main():
    parser = argparse.ArgumentParser(
        prog="subtitler",
        description="Local AI-powered subtitle generator and translator",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # --- transcribe ---
    p_transcribe = subparsers.add_parser(
        "transcribe", help="Generate subtitles from a video/audio file"
    )
    p_transcribe.add_argument("input", help="Path to video or audio file")
    p_transcribe.add_argument("-o", "--output", help="Output SRT path (default: <input>.srt)")
    p_transcribe.add_argument("-m", "--model", default="medium",
                              choices=["tiny", "base", "small", "medium", "large-v3"],
                              help="Whisper model size (default: medium)")
    p_transcribe.add_argument("-l", "--language", default=None,
                              help="Source language code (default: auto-detect)")
    p_transcribe.add_argument("-d", "--device", default="auto",
                              choices=["auto", "cpu", "cuda"],
                              help="Compute device (default: auto)")
    p_transcribe.set_defaults(func=cmd_transcribe)

    # --- translate ---
    p_translate = subparsers.add_parser(
        "translate", help="Translate an existing SRT subtitle file"
    )
    p_translate.add_argument("input", help="Path to input SRT file")
    p_translate.add_argument("-s", "--source", required=True,
                             help="Source language code (e.g. en)")
    p_translate.add_argument("-t", "--target", required=True,
                             help="Target language code (e.g. es)")
    p_translate.add_argument("-o", "--output", help="Output SRT path (default: <input>.<target>.srt)")
    p_translate.set_defaults(func=cmd_translate)

    # --- auto (transcribe + translate) ---
    p_auto = subparsers.add_parser(
        "auto", help="Transcribe and translate in one step"
    )
    p_auto.add_argument("input", help="Path to video or audio file")
    p_auto.add_argument("-t", "--target", required=True,
                        help="Target language code (e.g. es)")
    p_auto.add_argument("-s", "--source", default=None,
                        help="Source language code (default: auto-detect)")
    p_auto.add_argument("-m", "--model", default="medium",
                        choices=["tiny", "base", "small", "medium", "large-v3"],
                        help="Whisper model size (default: medium)")
    p_auto.add_argument("-l", "--language", default=None,
                        help="Whisper language hint for transcription")
    p_auto.add_argument("-d", "--device", default="auto",
                        choices=["auto", "cpu", "cuda"],
                        help="Compute device (default: auto)")
    p_auto.add_argument("--output-original", default=None,
                        help="Path for original-language SRT")
    p_auto.add_argument("--output-translated", default=None,
                        help="Path for translated SRT")
    p_auto.set_defaults(func=cmd_auto)

    # --- languages ---
    p_lang = subparsers.add_parser(
        "languages", help="List available translation language pairs"
    )
    p_lang.set_defaults(func=cmd_languages)

    args = parser.parse_args()
    try:
        args.func(args)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
