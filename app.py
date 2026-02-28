# app.py
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from models import TTSRequest, TTSResponse
from engine import synthesize_to_file

AUDIO_DIR = Path("static/audio")
AUDIO_DIR.mkdir(parents=True, exist_ok=True)

app = FastAPI(title="Empathy Engine", version="1.0.0")


@app.post("/api/tts", response_model=TTSResponse)
def create_tts(request: TTSRequest) -> TTSResponse:
    text = request.text.strip()
    if not text:
        raise HTTPException(status_code=400, detail="Text cannot be empty.")

    result = synthesize_to_file(text, AUDIO_DIR)
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
def get_audio(filename: str):
    """
    Serve a previously generated WAV file via FileResponse.[web:23][web:56]
    """
    file_path = AUDIO_DIR / filename
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Audio file not found")
    return FileResponse(path=str(file_path), media_type="audio/wav")


@app.get("/", response_class=HTMLResponse)
def index() -> HTMLResponse:
    """
    Simple demo UI: textarea -> POST /api/tts -> play audio.
    """
    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8" />
        <title>Empathy Engine</title>
        <style>
            body { font-family: Arial, sans-serif; max-width: 720px; margin: 40px auto; }
            textarea { width: 100%; box-sizing: border-box; }
            button { margin-top: 8px; padding: 8px 16px; }
            .meta { margin-top: 16px; font-family: monospace; white-space: pre-wrap; }
        </style>
    </head>
    <body>
        <h1>Empathy Engine</h1>
        <p>Paste a sales/customer message and hear emotion-aware speech.</p>

        <textarea id="text" rows="5"
            placeholder="Type something like: 'Great news! Your order was approved and ships today.'"></textarea><br />
        <button id="btn">Generate Audio</button>

        <div class="meta" id="meta"></div>

        <audio id="player" controls style="width: 100%; margin-top: 16px;">
            Your browser does not support the audio element.
        </audio>

        <script>
            const btn = document.getElementById('btn');
            const textArea = document.getElementById('text');
            const meta = document.getElementById('meta');
            const player = document.getElementById('player');

            btn.onclick = async () => {
                const text = textArea.value.trim();
                if (!text) {
                    alert('Please enter some text');
                    return;
                }

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
                    console.error(e);
                    meta.textContent = 'Error calling API';
                }
            };
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html)
