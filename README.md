# Empathy Engine - Emotion-Aware TTS for Sales & CX

The Empathy Engine analyzes input text sentiment using VADER, classifies
it into 3 emotions (Positive, Negative, Neutral), and modulates TTS rate
and volume to produce human-like speech for sales/customer service
scenarios.

------------------------------------------------------------------------

## 🎯 Assignment Requirements

  -----------------------------------------------------------------------
  Requirement              Implementation
  ------------------------ ----------------------------------------------
  Text Input               CLI (`python cli.py`) + FastAPI
                           (`POST /api/tts`)

  3 Emotions               VADER: Positive / Negative / Neutral

  2 Vocal Parameters       Rate (WPM) + Volume (0-1) via `pyttsx3`

  Emotion → Voice Mapping  Defined below

  Audio Output             WAV files (`static/audio/*.wav`)
  -----------------------------------------------------------------------

------------------------------------------------------------------------

## 🧠 Emotion → Voice Mapping Logic

VADER compound score (`c` ∈ \[-1, 1\]) determines emotion + modulation:

  -------------------------------------------------------------------------------------
  Emotion    VADER Threshold      Rate Formula       Volume Formula       Effect
  ---------- -------------------- ------------------ -------------------- -------------
  Positive   `c > 0.05`           `160 + 40 × |c|`   `0.8 + 0.15 × |c|`   Fast +
                                                                          Energetic

  Negative   `c < -0.05`          `160 - 40 × |c|`   `0.8 - 0.20 × |c|`   Slow + Calm

  Neutral    `-0 ≤ c ≤ 0.05`   `160`              `0.8`                Standard
  -------------------------------------------------------------------------------------

Real Examples:

"This is fantastic news!" → Positive (c=0.836) → 193 WPM, 0.93 vol →
UPBEAT\
"I'm sorry for the delay." → Negative (c=-0.571) → 137 WPM, 0.69 vol →
CALM\
"Meeting at 3 PM tomorrow." → Neutral (c=0.000) → 160 WPM, 0.80 vol →
NORMAL

------------------------------------------------------------------------

## 🚀 Quick Start

### Setup (Windows CMD)

``` bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
mkdir static\audio
```

### CLI Demo

``` bash
python cli.py "This is the best news ever!"
python cli.py "I apologize for the inconvenience."
python cli.py "Your order #12345 is confirmed."
```

### Web UI

``` bash
uvicorn app:app --reload
```

Open in browser: http://127.0.0.1:8000

------------------------------------------------------------------------

## 🏗️ Architecture

Text → VADER → Rate/Volume Mapping → pyttsx3 → WAV Output

Files: - engine.py - app.py - cli.py - models.py - requirements.txt -
static/audio/

------------------------------------------------------------------------

## 🧪 Verified Results

  Input             Emotion    Compound   Rate   Volume
  ----------------- ---------- ---------- ------ --------
  Amazing deal!     positive   0.7506     190    0.91
  Very sorry...     negative   -0.5849    137    0.68
  Order confirmed   neutral    0.0779     160    0.80

------------------------------------------------------------------------
