"""Unit tests for sentiment analysis and emotion mapping."""

import pytest

from empathy_engine.config import Settings
from empathy_engine.engine import analyze_text


@pytest.fixture
def settings() -> Settings:
    return Settings(
        base_rate_wpm=160,
        base_volume=0.8,
        positive_threshold=0.05,
        negative_threshold=-0.05,
    )


class TestAnalyzeText:
    def test_positive_sentiment(self, settings: Settings) -> None:
        emotion, compound, rate, volume = analyze_text(
            "This is fantastic news!", settings
        )
        assert emotion == "positive"
        assert compound > 0.05
        assert rate > 160
        assert volume > 0.8

    def test_negative_sentiment(self, settings: Settings) -> None:
        emotion, compound, rate, volume = analyze_text(
            "I am very sorry for the inconvenience.", settings
        )
        assert emotion == "negative"
        assert compound < -0.05
        assert rate < 160
        assert volume < 0.8

    def test_neutral_sentiment(self, settings: Settings) -> None:
        emotion, compound, rate, volume = analyze_text(
            "Meeting at 3 PM tomorrow.", settings
        )
        assert emotion == "neutral"
        assert rate == 160
        assert volume == 0.8

    def test_intensity_scales_positive_rate(self, settings: Settings) -> None:
        _, _, rate_strong, _ = analyze_text("Amazing! Best deal ever!", settings)
        _, _, rate_weak, _ = analyze_text("Good.", settings)
        assert rate_strong >= rate_weak

    def test_volume_bounds(self, settings: Settings) -> None:
        _, _, _, volume_neg = analyze_text(
            "Terrible horrible awful disaster.", settings
        )
        assert volume_neg >= 0.5
