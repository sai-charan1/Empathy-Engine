"""CLI entry point for emotion-aware TTS."""

import argparse
import logging
from pathlib import Path

from empathy_engine.config import get_settings
from empathy_engine.engine import synthesize_to_file

logging.basicConfig(level=get_settings().log_level)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Empathy Engine — emotion-aware text-to-speech (CLI)"
    )
    parser.add_argument("text", type=str, help="Text to synthesize")
    parser.add_argument(
        "--dir",
        type=str,
        default=None,
        help="Output directory (default: from settings / static/audio)",
    )
    args = parser.parse_args()
    settings = get_settings()
    output_dir = Path(args.dir) if args.dir else settings.audio_dir_resolved

    result = synthesize_to_file(args.text, output_dir, settings)

    print("=== Empathy Engine (CLI) ===")
    print(f"Text     : {result.text}")
    print(f"Emotion  : {result.emotion}")
    print(f"Compound : {result.compound:.3f}")
    print(f"Rate     : {result.rate} WPM")
    print(f"Volume   : {result.volume:.2f}")
    print(f"File     : {output_dir / result.filename}")


if __name__ == "__main__":
    main()
