"""Empathy Engine — emotion-aware text-to-speech for sales and customer experience."""

from empathy_engine.engine import EmotionConfig, analyze_text, synthesize_to_file
from empathy_engine.models import TTSRequest, TTSResponse

__all__ = [
    "EmotionConfig",
    "TTSRequest",
    "TTSResponse",
    "analyze_text",
    "synthesize_to_file",
]

__version__ = "1.0.0"
