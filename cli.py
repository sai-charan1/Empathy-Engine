# cli.py
import argparse
from pathlib import Path

from engine import synthesize_to_file


def main():
    parser = argparse.ArgumentParser(
        description="Empathy Engine - emotion-aware text-to-speech (CLI)"
    )
    parser.add_argument(
        "text",
        type=str,
        help="Text to synthesize with emotion-aware TTS",
    )
    parser.add_argument(
        "--dir",
        type=str,
        default="static/audio",
        help="Output directory for audio files (default: static/audio)",
    )

    args = parser.parse_args()
    output_dir = Path(args.dir)

    result = synthesize_to_file(args.text, output_dir)

    print("=== Empathy Engine (CLI) ===")
    print(f"Text     : {result.text}")
    print(f"Emotion  : {result.emotion}")
    print(f"Compound : {result.compound:.3f}")
    print(f"Rate     : {result.rate} WPM")
    print(f"Volume   : {result.volume:.2f}")
    print(f"File     : {output_dir / result.filename}")


if __name__ == "__main__":
    main()
