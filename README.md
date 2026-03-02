# Subtitler

Local AI-powered subtitle generator and translator. Everything runs on your machine — no cloud APIs needed.

- **Transcription**: Uses [faster-whisper](https://github.com/SYSTRAN/faster-whisper) (OpenAI Whisper) to generate subtitles from video/audio
- **Translation**: Uses [Argos Translate](https://github.com/argosopentech/argos-translate) for fully offline translation between 30+ languages

## Installation

```bash
# 1. Clone and install
git clone <repo-url> && cd Subtitler
pip install -e .

# 2. (Optional) For GPU acceleration, install CUDA-compatible PyTorch first:
# pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
```

## Usage

### Generate subtitles from video

```bash
subtitler transcribe video.mp4
# -> creates video.srt

# Choose model size (tiny/base/small/medium/large-v3)
subtitler transcribe video.mp4 -m large-v3

# Force a specific language instead of auto-detect
subtitler transcribe video.mp4 -l en

# Use GPU
subtitler transcribe video.mp4 -d cuda
```

### Translate an existing SRT file

```bash
subtitler translate video.srt -s en -t es
# -> creates video.es.srt

subtitler translate video.srt -s en -t fr -o french_subs.srt
```

### Transcribe + translate in one step

```bash
subtitler auto video.mp4 -t es
# -> creates video.en.srt (original) and video.es.srt (translated)

subtitler auto video.mp4 -t de -m large-v3 -d cuda
```

### List available translation languages

```bash
subtitler languages
```

## Whisper Model Sizes

| Model    | Parameters | Speed    | Accuracy  | VRAM   |
|----------|-----------|----------|-----------|--------|
| tiny     | 39M       | Fastest  | Lower     | ~1 GB  |
| base     | 74M       | Fast     | Fair      | ~1 GB  |
| small    | 244M      | Moderate | Good      | ~2 GB  |
| medium   | 769M      | Slow     | Very Good | ~5 GB  |
| large-v3 | 1550M     | Slowest  | Best      | ~10 GB |

Models are downloaded automatically on first use.

## Supported Translation Languages

Common pairs include: English, Spanish, French, German, Italian, Portuguese, Russian, Chinese, Japanese, Korean, Arabic, Hindi, and many more. Run `subtitler languages` for the full list.
