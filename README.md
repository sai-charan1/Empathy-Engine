# Empathy Engine – Emotion-Aware TTS for Sales & CX

This project implements **The Empathy Engine**: a service that takes text,
detects its emotion using VADER sentiment analysis, and modulates text-to-speech
parameters (rate and volume) to produce more human-like, context-aware audio
for sales and customer interactions.[web:60][web:51]

## Features

- **Text input** via CLI and REST API.
- **Emotion detection** with VADER (`positive`, `neutral`, `negative`) using the
  `compound` score in [-1, 1].[web:60][web:51]
- **Vocal modulation** of **rate** (words per minute) and **volume** (0–1)
  using documented pyttsx3 properties.[web:22][web:31][web:61]
- **Intensity scaling**: stronger sentiment → stronger modulation.
- **Web UI** (FastAPI + HTML) with textarea and audio player.

## Tech Stack

- Python 3.10+
- VADER Sentiment (`vaderSentiment`) for sentiment analysis.[web:60][web:51]
- pyttsx3 for offline TTS.[web:22][web:26][web:31]
- FastAPI + Uvicorn for API and HTML UI.[web:23]

## Setup

```bash
git clone <your-repo-url>
cd empathy-engine
python -m venv venv
source venv/bin/activate  # Windows: venv\\Scripts\\activate
pip install -r requirements.txt


Emotion → Voice Mapping
Emotion	VADER Score	Rate	Volume	Effect
Positive	> 0.05	160+40×|c|	0.8+0.15×|c|	Fast/Energetic
Negative	< -0.05	160-40×|c|	0.8-0.20×|c|	Slow/Calm
Neutral	[-0.05,0.05]	160	0.8	Normal
Tech
VADER sentiment analysis

pyttsx3 TTS (rate + volume)

FastAPI web UI

text

***

## **7. `.gitignore`**
venv/
pycache/
.pyc
static/audio/.wav
.env

text

***

## **🚀 RUN NOW:**

```bash
# Windows CMD (recommended)
venv\Scripts\activate
pip install -r requirements.txt
python cli.py "Test"

# Web
uvicorn app:app --reload