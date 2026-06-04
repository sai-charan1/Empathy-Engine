"""API smoke tests (no TTS synthesis)."""

from fastapi.testclient import TestClient

from app import app

client = TestClient(app)


def test_health() -> None:
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"


def test_tts_empty_text_rejected() -> None:
    resp = client.post("/api/tts", json={"text": "   "})
    assert resp.status_code == 422 or resp.status_code == 400
