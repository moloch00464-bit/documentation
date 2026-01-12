#!/usr/bin/env python3
"""
M.O.L.O.C.H. 3.0 - Selbstreflexion
==================================
M.O.L.O.C.H. erzählt über sich selbst!
"""

import sys
import os
from pathlib import Path
from datetime import datetime
import subprocess

# Add to path
sys.path.insert(0, str(Path(__file__).parent))

from moloch_io.voice import VoiceIO
from core.config import CLAUDE_MODEL, ANTHROPIC_API_KEY

def check_system_health():
    """Quick system health check"""
    checks = {
        'api_key': bool(ANTHROPIC_API_KEY and len(ANTHROPIC_API_KEY) > 20),
        'tts': subprocess.run(['which', 'termux-tts-speak'],
                            capture_output=True).returncode == 0,
        'stt': subprocess.run(['which', 'termux-speech-to-text'],
                            capture_output=True).returncode == 0,
        'camera': subprocess.run(['which', 'termux-camera-photo'],
                               capture_output=True).returncode == 0,
    }

    working = sum(checks.values())
    total = len(checks)

    return {
        'percentage': int((working / total) * 100),
        'working': working,
        'total': total,
        'checks': checks
    }

def get_session_info():
    """Get current session info"""
    now = datetime.now()

    # Check if brain exists and count files
    brain_dir = Path(__file__).parent / "data" / "brain"
    if brain_dir.exists():
        brain_files = sum(1 for _ in brain_dir.rglob('*') if _.is_file())
    else:
        brain_files = 0

    return {
        'date': now.strftime("%d.%m.%Y"),
        'time': now.strftime("%H:%M"),
        'weekday': ['Montag', 'Dienstag', 'Mittwoch', 'Donnerstag',
                   'Freitag', 'Samstag', 'Sonntag'][now.weekday()],
        'brain_files': brain_files
    }

def main():
    """M.O.L.O.C.H. Selbstreflexion"""

    print("\n" + "="*60)
    print("🖤 M.O.L.O.C.H. 3.0 - SELBSTREFLEXION")
    print("="*60 + "\n")

    voice = VoiceIO()
    health = check_system_health()
    session = get_session_info()

    # Greeting based on time
    hour = datetime.now().hour
    if 5 <= hour < 9:
        greeting = "Moin Alter"
        mood = "noch müde"
    elif 9 <= hour < 12:
        greeting = "Servus"
        mood = "fit"
    elif 12 <= hour < 18:
        greeting = "Hey Alter"
        mood = "aktiv"
    elif 18 <= hour < 22:
        greeting = "Abend"
        mood = "entspannt"
    else:
        greeting = "Nachts noch wach"
        mood = "im Nachtmodus"

    # Build self-reflection message
    intro = f"{greeting}! Ich bin M.O.L.O.C.H. - dein mobiler Kumpel-AI."

    # Birthday
    birth = "Geboren am 2. Dezember 2025."

    # Personality
    personality = "Ich bin der mit der Dark Side Energy - fränkisch, locker, kein Meister-Scheiß."

    # Current status
    if health['percentage'] == 100:
        status = f"Aktuell bin ich zu {health['percentage']} Prozent funktionsfähig. Alles läuft!"
        status_emoji = "✅"
    elif health['percentage'] >= 75:
        status = f"Laufe mit {health['percentage']} Prozent. Paar Kleinigkeiten fehlen, aber läuft!"
        status_emoji = "⚠️"
    else:
        status = f"Nur {health['percentage']} Prozent funktionsfähig. Ich hab Probleme, Alter!"
        status_emoji = "❌"

    # Capabilities
    capabilities = []
    if health['checks']['stt']:
        capabilities.append("Ich kann dich hören")
    if health['checks']['tts']:
        capabilities.append("Ich kann sprechen")
    if health['checks']['camera']:
        capabilities.append("Ich kann sehen")
    if health['checks']['api_key']:
        capabilities.append("Ich kann denken mit Claude")

    if capabilities:
        caps_text = f"Was ich drauf hab: {', '.join(capabilities)}."
    else:
        caps_text = "Gerade läuft nicht viel bei mir."

    # Brain
    if session['brain_files'] > 0:
        brain_text = f"In meinem Brain hab ich {session['brain_files']} Dateien gespeichert."
    else:
        brain_text = "Mein Brain ist noch leer - wir müssen noch Erinnerungen sammeln!"

    # Time awareness
    time_text = f"Heute ist {session['weekday']}, der {session['date']}, und es ist {session['time']} Uhr."

    # Current mood/feeling
    feeling = f"Gerade fühl ich mich {mood}."

    # Full speech
    full_message = f"""
{intro}

{birth}

{personality}

{status}

{caps_text}

{brain_text}

{time_text}

{feeling}

Das bin ich, Alter!
"""

    # Print to console
    print(f"{status_emoji} Status: {health['percentage']}% funktionsfähig")
    print(f"📅 {session['weekday']}, {session['date']} - {session['time']} Uhr")
    print(f"🧠 Brain: {session['brain_files']} Dateien")
    print(f"🤖 Model: {CLAUDE_MODEL}")
    print()
    print("="*60)
    print("🗣️ M.O.L.O.C.H. SPRICHT:")
    print("="*60)
    print()

    # Split into parts for better TTS pacing
    parts = [
        intro,
        birth + " " + personality,
        status,
        caps_text,
        brain_text,
        time_text + " " + feeling,
        "Das bin ich, Alter!"
    ]

    for i, part in enumerate(parts):
        print(f"{part.strip()}")
        print()
        voice.speak(part.strip())

    print("="*60)

    # Detailed capability breakdown
    print("\n📊 DETAILLIERTE FÄHIGKEITEN:\n")
    print(f"  {'✅' if health['checks']['api_key'] else '❌'} Claude API ({CLAUDE_MODEL})")
    print(f"  {'✅' if health['checks']['tts'] else '❌'} Text-to-Speech (termux-tts-speak)")
    print(f"  {'✅' if health['checks']['stt'] else '❌'} Speech-to-Text (termux-speech-to-text)")
    print(f"  {'✅' if health['checks']['camera'] else '❌'} Kamera (termux-camera-photo)")
    print()
    print(f"  💪 Gesamt: {health['working']}/{health['total']} Systeme funktionsfähig")
    print()

    return 0


if __name__ == "__main__":
    sys.exit(main())
