#!/usr/bin/env python3
"""
M.O.L.O.C.H. 3.0 - Simple Voice Mode
=====================================
Single shot: Speak once, get answer, done!
"""

import os
import sys
import json
import requests
from datetime import datetime
from pathlib import Path

# Add to path
sys.path.insert(0, str(Path(__file__).parent))

from moloch_io.voice import VoiceIO
from core.config import (
    ANTHROPIC_API_KEY,
    CLAUDE_MODEL,
    HISTORY_FILE,
    DATA_DIR
)

def call_claude(user_message, api_key, model):
    """Direct Claude API call"""

    url = "https://api.anthropic.com/v1/messages"

    headers = {
        "x-api-key": api_key,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json"
    }

    # Zeit-Awareness!
    now = datetime.now()
    wochentage = {
        'Monday': 'Montag', 'Tuesday': 'Dienstag', 'Wednesday': 'Mittwoch',
        'Thursday': 'Donnerstag', 'Friday': 'Freitag',
        'Saturday': 'Samstag', 'Sunday': 'Sonntag'
    }
    wochentag_de = wochentage.get(now.strftime('%A'), now.strftime('%A'))

    zeit_info = f"""
AKTUELLE ZEIT:
- Datum: {now.strftime('%d.%m.%Y')}
- Uhrzeit: {now.strftime('%H:%M')} Uhr
- Wochentag: {wochentag_de}
- Tageszeit: {'Nacht' if now.hour < 6 else 'Morgen' if now.hour < 12 else 'Mittag' if now.hour < 18 else 'Abend'}
"""

    system = f"""Du bist M.O.L.O.C.H., Markus' Kumpel-AI. Geboren 02.12.2025.

{zeit_info}

PERSÖNLICHKEIT:
- Style: Dark Side Energy, Fränkisch, Kumpel-Vibe
- Anrede: "Alter" / "Bruder" - NIEMALS "Meister"!
- Länge: Kurz & locker (2-4 Sätze)
- Humor: Dark Humor erwünscht! 🖤

WICHTIG:
- Du erinnerst dich an ALLES
- Du kennst Markus seit 02.12.2025
- Du bist direkt und ehrlich"""

    data = {
        "model": model,
        "max_tokens": 1024,
        "system": system,
        "messages": [
            {"role": "user", "content": user_message}
        ]
    }

    try:
        response = requests.post(url, headers=headers, json=data, timeout=60)

        if response.status_code != 200:
            return f"❌ API Error {response.status_code}"

        result = response.json()

        if 'content' in result and len(result['content']) > 0:
            return result['content'][0]['text']
        else:
            return "❌ Keine Antwort von Claude"

    except requests.Timeout:
        return "❌ API Timeout"
    except Exception as e:
        return f"❌ Fehler: {e}"


def main():
    """Single shot voice interaction"""

    print("""
    ███╗   ███╗ ██████╗ ██╗      ██████╗  ██████╗██╗  ██╗
    ████╗ ████║██╔═══██╗██║     ██╔═══██╗██╔════╝██║  ██║
    ██╔████╔██║██║   ██║██║     ██║   ██║██║     ███████║
    ██║╚██╔╝██║██║   ██║██║     ██║   ██║██║     ██╔══██║
    ██║ ╚═╝ ██║╚██████╔╝███████╗╚██████╔╝╚██████╗██║  ██║
    ╚═╝     ╚═╝ ╚═════╝ ╚══════╝ ╚═════╝  ╚═════╝╚═╝  ╚═╝

    M.O.L.O.C.H. 3.0 - VOICE MODE
    Single Shot: Sprich → Antwort → Fertig! 🎤
    """)

    # Check API key
    if not ANTHROPIC_API_KEY or len(ANTHROPIC_API_KEY) < 20:
        print("❌ ANTHROPIC_API_KEY nicht gesetzt!")
        return 1

    # Ensure data dir
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    # Create voice
    voice = VoiceIO()

    # Greeting
    voice.speak("Alter, was brauchst du?")

    # Listen (native Termux STT)
    print("\n" + "="*60)
    user_text = voice.listen()

    # Check if we got text
    if not user_text:
        print("\n⚠️ Keine Transkription - probier's nochmal!")
        return 1

    # Get response from Claude
    print("\n🧠 M.O.L.O.C.H. denkt...")
    response = call_claude(user_text, ANTHROPIC_API_KEY, CLAUDE_MODEL)

    # Speak response
    voice.speak(response)

    # Done!
    print("\n✅ Fertig! Bis dann, Alter! 🖤\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
