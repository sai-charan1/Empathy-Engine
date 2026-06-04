"""FastAPI application for the Empathy Engine TTS service."""

import logging

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, HTMLResponse

from empathy_engine import __version__
from empathy_engine.config import get_settings
from empathy_engine.engine import synthesize_to_file
from empathy_engine.models import TTSRequest, TTSResponse

logging.basicConfig(level=get_settings().log_level)
logger = logging.getLogger(__name__)

settings = get_settings()
AUDIO_DIR = settings.audio_dir_resolved

app = FastAPI(title="Empathy Engine", version=__version__)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "version": __version__}


@app.post("/api/tts", response_model=TTSResponse)
def create_tts(request: TTSRequest) -> TTSResponse:
    text = request.text.strip()
    if not text:
        raise HTTPException(status_code=400, detail="Text cannot be empty.")

    result = synthesize_to_file(text, AUDIO_DIR, settings)
    audio_url = f"/audio/{result.filename}"

    return TTSResponse(
        text=result.text,
        emotion=result.emotion,
        compound=result.compound,
        rate=result.rate,
        volume=result.volume,
        audio_filename=result.filename,
        audio_url=audio_url,
    )


@app.get("/audio/{filename}")
def get_audio(filename: str) -> FileResponse:
    file_path = AUDIO_DIR / filename
    if not file_path.exists() or ".." in filename:
        raise HTTPException(status_code=404, detail="Audio file not found")
    return FileResponse(path=str(file_path), media_type="audio/wav")


@app.get("/", response_class=HTMLResponse)
def index() -> HTMLResponse:
    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8" />
        <title>Empathy Engine</title>
        <style>
            body { font-family: system-ui, sans-serif; max-width: 720px; margin: 40px auto; }
            textarea { width: 100%; box-sizing: border-box; }
            button { margin-top: 8px; padding: 8px 16px; }
            .meta { margin-top: 16px; font-family: monospace; white-space: pre-wrap; }
        </style>
    </head>
    <body>
        <h1>Empathy Engine</h1>
        <p>Paste a sales or customer message and hear emotion-aware speech.</p>
        <textarea id="text" rows="5"
            placeholder="Great news! Your order was approved and ships today."></textarea><br />
        <button id="btn">Generate Audio</button>
        <div class="meta" id="meta"></div>
        <audio id="player" controls style="width: 100%; margin-top: 16px;"></audio>
        <script>
            const btn = document.getElementById('btn');
            const textArea = document.getElementById('text');
            const meta = document.getElementById('meta');
            const player = document.getElementById('player');
            btn.onclick = async () => {
                const text = textArea.value.trim();
                if (!text) { alert('Please enter some text'); return; }
                meta.textContent = 'Generating...';
                try {
                    const resp = await fetch('/api/tts', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ text })
                    });
                    if (!resp.ok) {
                        const err = await resp.json();
                        meta.textContent = 'Error: ' + (err.detail || resp.statusText);
                        return;
                    }
                    const data = await resp.json();
                    meta.textContent =
                        'Emotion : ' + data.emotion + '\\n' +
                        'Compound: ' + data.compound.toFixed(3) + '\\n' +
                        'Rate    : ' + data.rate + ' WPM\\n' +
                        'Volume  : ' + data.volume.toFixed(2);
                    player.src = data.audio_url + '?t=' + Date.now();
                    player.load();
                    player.play().catch(() => {});
                } catch (e) {
                    meta.textContent = 'Error calling API';
                }
            };
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html)
