"""Application configuration via environment variables."""

from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    audio_dir: Path = Field(default=Path("static/audio"))
    base_rate_wpm: int = Field(default=160, ge=80, le=300)
    base_volume: float = Field(default=0.8, ge=0.0, le=1.0)
    positive_threshold: float = Field(default=0.05)
    negative_threshold: float = Field(default=-0.05)
    log_level: str = Field(default="INFO")

    @property
    def audio_dir_resolved(self) -> Path:
        path = Path(self.audio_dir)
        path.mkdir(parents=True, exist_ok=True)
        return path


def get_settings() -> Settings:
    return Settings()
