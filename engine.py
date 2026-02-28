# engine.py
from dataclasses import dataclass
from pathlib import Path
from typing import Tuple

import pyttsx3
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer  # [web:60][web:51]


# Instantiate VADER once at module load.
_analyzer = SentimentIntensityAnalyzer()


@dataclass
class EmotionConfig:
    text: str
    emotion: str         # "positive", "neutral", "negative"
    compound: float      # VADER compound score (-1..1)
    rate: int            # words per minute
    volume: float        # 0.0 .. 1.0
    filename: str        # relative filename under static/audio/


def analyze_text(text: str) -> Tuple[str, float, int, float]:
    """
    Analyze sentiment with VADER and map to an emotion and voice parameters.

    VADER compound score:
      - >  0.05: Positive
      - < -0.05: Negative
      - else   : Neutral.[web:60][web:51]
    """
    scores = _analyzer.polarity_scores(text)
    compound = float(scores["compound"])

    # Decide discrete emotion using standard VADER thresholds.[web:60][web:51]
    if compound > 0.05:
        emotion = "positive"
    elif compound < -0.05:
        emotion = "negative"
    else:
        emotion = "neutral"

    # Base parameters.
    base_rate = 160
    base_volume = 0.8

    # Intensity scaling factor based on absolute compound.
    intensity = min(1.0, abs(compound))

    if emotion == "positive":
        # More positive → faster and slightly louder.
        rate = int(base_rate + 40 * intensity)       # up to ~200 wpm
        volume = min(1.0, base_volume + 0.15 * intensity)
    elif emotion == "negative":
        # More negative → slower and softer.
        rate = int(base_rate - 40 * intensity)       # down to ~120 wpm
        volume = max(0.5, base_volume - 0.2 * intensity)
    else:
        # Neutral stays at baseline.
        rate = base_rate
        volume = base_volume

    return emotion, compound, rate, volume


def synthesize_to_file(text: str, output_dir: Path) -> EmotionConfig:
    """
    Full pipeline: analyze text, configure pyttsx3, and synthesize audio to a WAV file.

    Uses documented pyttsx3 properties:
      - 'rate': integer words per minute.[web:22][web:31][web:61]
      - 'volume': float between 0.0 and 1.0.[web:22][web:31][web:61]
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    emotion, compound, rate, volume = analyze_text(text)

    # Simple filename based on hash; in real app you might use UUID.
    filename = f"tts_{abs(hash(text)) & 0xFFFFFFFF}.wav"
    file_path = output_dir / filename

    engine = pyttsx3.init()  # standard engine creation[web:22][web:26]

    # Configure engine with our mapped parameters.
    engine.setProperty("rate", rate)
    engine.setProperty("volume", volume)

    # Optional: select first voice (default is usually fine).
    voices = engine.getProperty("voices")
    if voices:
        engine.setProperty("voice", voices[0].id)

    engine.save_to_file(text, str(file_path))
    engine.runAndWait()  # blocks until audio is written[web:22][web:31][web:26]

    return EmotionConfig(
        text=text,
        emotion=emotion,
        compound=compound,
        rate=rate,
        volume=volume,
        filename=filename,
    )
