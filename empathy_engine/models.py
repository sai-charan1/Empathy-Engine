"""Pydantic request/response schemas for the TTS API."""

from pydantic import BaseModel, Field


class TTSRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=5000)


class TTSResponse(BaseModel):
    text: str
    emotion: str
    compound: float
    rate: int
    volume: float
    audio_filename: str
    audio_url: str


class SentimentAnalysis(BaseModel):
    """Structured output from sentiment analysis (no TTS)."""

    text: str
    emotion: str
    compound: float
    rate: int
    volume: float
