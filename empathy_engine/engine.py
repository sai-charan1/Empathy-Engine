"""VADER sentiment analysis and emotion-aware TTS parameter mapping."""

from __future__ import annotations

import hashlib
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Literal, Tuple

import pyttsx3
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

from empathy_engine.config import Settings, get_settings

logger = logging.getLogger(__name__)

Emotion = Literal["positive", "neutral", "negative"]

_analyzer = SentimentIntensityAnalyzer()


@dataclass
class EmotionConfig:
    text: str
    emotion: str
    compound: float
    rate: int
    volume: float
    filename: str


def analyze_text(
    text: str,
    settings: Settings | None = None,
) -> Tuple[Emotion, float, int, float]:
    """
    Analyze sentiment with VADER and map to emotion + voice parameters.

    VADER compound score:
      - >  positive_threshold: positive
      - <  negative_threshold: negative
      - else: neutral
    """
    cfg = settings or get_settings()
    scores = _analyzer.polarity_scores(text)
    compound = float(scores["compound"])

    if compound > cfg.positive_threshold:
        emotion: Emotion = "positive"
    elif compound < cfg.negative_threshold:
        emotion = "negative"
    else:
        emotion = "neutral"

    base_rate = cfg.base_rate_wpm
    base_volume = cfg.base_volume
    intensity = min(1.0, abs(compound))

    if emotion == "positive":
        rate = int(base_rate + 40 * intensity)
        volume = min(1.0, base_volume + 0.15 * intensity)
    elif emotion == "negative":
        rate = int(base_rate - 40 * intensity)
        volume = max(0.5, base_volume - 0.2 * intensity)
    else:
        rate = base_rate
        volume = base_volume

    logger.debug(
        "analyzed text emotion=%s compound=%.3f rate=%d volume=%.2f",
        emotion,
        compound,
        rate,
        volume,
    )
    return emotion, compound, rate, volume


def _filename_for_text(text: str) -> str:
    digest = hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]
    return f"tts_{digest}.wav"


def synthesize_to_file(
    text: str,
    output_dir: Path | None = None,
    settings: Settings | None = None,
) -> EmotionConfig:
    """Analyze text, configure pyttsx3, and write a WAV file."""
    cfg = settings or get_settings()
    out = Path(output_dir) if output_dir else cfg.audio_dir_resolved
    out.mkdir(parents=True, exist_ok=True)

    emotion, compound, rate, volume = analyze_text(text, cfg)
    filename = _filename_for_text(text)
    file_path = out / filename

    engine = pyttsx3.init()
    engine.setProperty("rate", rate)
    engine.setProperty("volume", volume)

    voices = engine.getProperty("voices")
    if voices:
        engine.setProperty("voice", voices[0].id)

    engine.save_to_file(text, str(file_path))
    engine.runAndWait()

    logger.info("synthesized audio file=%s emotion=%s", filename, emotion)

    return EmotionConfig(
        text=text,
        emotion=emotion,
        compound=compound,
        rate=rate,
        volume=volume,
        filename=filename,
    )
