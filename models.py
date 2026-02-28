# models.py
from pydantic import BaseModel


class TTSRequest(BaseModel):
    text: str


class TTSResponse(BaseModel):
    text: str
    emotion: str
    compound: float
    rate: int
    volume: float
    audio_filename: str
    audio_url: str
