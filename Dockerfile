FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    espeak \
    libespeak1 \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml README.md ./
COPY empathy_engine ./empathy_engine
COPY app.py cli.py ./

RUN pip install --no-cache-dir -e .

RUN mkdir -p static/audio

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
