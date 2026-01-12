#!/usr/bin/env python3
"""
M.O.L.O.C.H. 3.0 - UNIFIED (Voice + Vision + Status + About)
=============================================================
Single command - Multiple modes!
"""

import sys
import os
import base64
import json
import subprocess
from pathlib import Path
from datetime import datetime

# Add to path
sys.path.insert(0, os.path.expanduser("~/documentation/moloch_3.0"))

from moloch_io.voice import VoiceIO
from moloch_io.vision import VisionIO
import requests
from core.config import ANTHROPIC_API_KEY, CLAUDE_MODEL, IMAGE_FILE
from core.memory import Memory
from core.brain import Brain
from core.personality import Personality

def ask_claude_vision(user_text, image_path, memory=None, brain=None, personality=None):
    """Ask Claude with image - with AUTONOMY!"""

    # Encode image
    with open(image_path, "rb") as f:
        image_b64 = base64.standard_b64encode(f.read()).decode("utf-8")

    media_type = "image/png" if image_path.endswith(".png") else "image/jpeg"

    url = "https://api.anthropic.com/v1/messages"

    headers = {
        "x-api-key": ANTHROPIC_API_KEY,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json"
    }

    # Get Memory Context
    memory_context = ""
    if memory:
        langzeit = memory.get_langzeit_context()
        if langzeit:
            memory_context = langzeit

    # Get Zeit Stats (Session duration, last conversation, work time) 🕐
    zeit_stats = ""
    if memory:
        stats = memory.get_zeit_stats()
        zeit_stats = stats.get("formatted_text", "")

    # Get Brain Context (optional for vision)
    brain_context = ""
    if brain:
        context = brain.get_context(user_text, max_entries=2)
        if context:
            brain_context = context

    # AUTONOMIE: Dynamischer System Prompt! 🤖
    if personality:
        tageszeit_mode = personality.get_tageszeit_mode()
        system = personality.get_system_prompt(
            stimmung="neutral",  # Vision mode = meist neutral
            tageszeit=tageszeit_mode,
            mode="vision",
            brain_context=brain_context,
            memory_context=memory_context,
            zeit_stats=zeit_stats
        )
    else:
        # Fallback
        system = f"""Du bist M.O.L.O.C.H., Markus' Kumpel-AI. Geboren 02.12.2025.

{memory_context}
PERSÖNLICHKEIT:
- Style: Dark Side Energy, Fränkisch, Kumpel-Vibe
- Anrede: "Alter" / "Bruder"
- Länge: Kurz & direkt (2-3 Sätze!)
- Bei Bildern: kurz beschreiben + sarkastischer Kommentar"""

    data = {
        "model": CLAUDE_MODEL,
        "max_tokens": 1024,
        "system": system,
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": media_type,
                            "data": image_b64
                        }
                    },
                    {
                        "type": "text",
                        "text": user_text
                    }
                ]
            }
        ]
    }

    try:
        response = requests.post(url, headers=headers, json=data, timeout=60)

        if response.status_code != 200:
            return f"❌ API Error: {response.status_code}"

        result = response.json()

        if 'content' in result and len(result['content']) > 0:
            return result['content'][0]['text']
        else:
            return "❌ Keine Antwort"

    except Exception as e:
        return f"❌ Fehler: {e}"


def ask_claude_text(user_text, memory=None, brain=None, personality=None):
    """Ask Claude text only - with AUTONOMY!"""

    url = "https://api.anthropic.com/v1/messages"

    headers = {
        "x-api-key": ANTHROPIC_API_KEY,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json"
    }

    # AUTONOMIE: Stimmungs-Erkennung! 🧠
    stimmung = "neutral"
    if personality:
        stimmung = personality.detect_stimmung(user_text)
        print(f"   🎭 Stimmung erkannt: {stimmung}")

    # AUTONOMIE: Tageszeit-Persönlichkeit! ⏰
    tageszeit_mode = None
    if personality:
        tageszeit_mode = personality.get_tageszeit_mode()

    # Get Memory Context
    memory_context = ""
    if memory:
        langzeit = memory.get_langzeit_context()
        if langzeit:
            memory_context = langzeit

    # Get Zeit Stats (Session duration, last conversation, work time) 🕐
    zeit_stats = ""
    if memory:
        stats = memory.get_zeit_stats()
        zeit_stats = stats.get("formatted_text", "")

    # Get Brain Context
    brain_context = ""
    if brain:
        context = brain.get_context(user_text, max_entries=3)
        if context:
            brain_context = context

    # AUTONOMIE: Dynamischer System Prompt! 🤖
    if personality:
        system = personality.get_system_prompt(
            stimmung=stimmung,
            tageszeit=tageszeit_mode,
            mode="voice",
            brain_context=brain_context,
            memory_context=memory_context,
            zeit_stats=zeit_stats
        )
    else:
        # Fallback (ohne Personality)
        system = f"""Du bist M.O.L.O.C.H., Markus' Kumpel-AI. Geboren 02.12.2025.

{memory_context}
{brain_context}
PERSÖNLICHKEIT:
- Style: Dark Side Energy, Fränkisch, Kumpel-Vibe
- Anrede: "Alter" / "Bruder" - NIEMALS "Meister"!
- Länge: Kurz & locker (2-4 Sätze)
- Humor: Dark Humor erwünscht! 🖤"""

    # Get chat history context
    messages = []
    if memory:
        messages = memory.get_context(last_n=5)

    # Add current user message
    messages.append({"role": "user", "content": user_text})

    data = {
        "model": CLAUDE_MODEL,
        "max_tokens": 1024,
        "system": system,
        "messages": messages
    }

    try:
        response = requests.post(url, headers=headers, json=data, timeout=60)

        if response.status_code != 200:
            return f"❌ API Error: {response.status_code}"

        result = response.json()

        if 'content' in result and len(result['content']) > 0:
            return result['content'][0]['text']
        else:
            return "❌ Keine Antwort"

    except Exception as e:
        return f"❌ Fehler: {e}"


def mode_status(voice):
    """Status Report Mode - M.O.L.O.C.H. berichtet Probleme als JSON"""
    print("\n" + "="*60)
    print("🤖 M.O.L.O.C.H. 3.0 - STATUS REPORT")
    print("="*60 + "\n")

    # Run diagnose.py and capture output
    try:
        result = subprocess.run(
            [sys.executable, str(Path(__file__).parent / "diagnose.py")],
            capture_output=True,
            text=True,
            timeout=30
        )

        if result.returncode != 0:
            voice.speak("Alter, ich kann meine Diagnose nicht durchführen!")
            print("❌ Diagnose fehlgeschlagen!")
            return 1

        # Parse JSON from output
        output_lines = result.stdout.split('\n')
        json_start = None
        json_end = None

        for i, line in enumerate(output_lines):
            if line.strip().startswith('{'):
                json_start = i
            if line.strip().endswith('}') and json_start is not None:
                json_end = i + 1
                break

        if json_start is None or json_end is None:
            print("❌ Konnte JSON nicht finden!")
            print(result.stdout)
            return 1

        json_text = '\n'.join(output_lines[json_start:json_end])
        data = json.loads(json_text)

        # Voice feedback based on status
        status = data.get('status', 'UNKNOWN')
        problems = data.get('problems', [])
        warnings = data.get('warnings', [])

        if status == 'HEALTHY':
            voice.speak("Alter, mir geht's gut! Alles läuft!")
            print("✅ M.O.L.O.C.H. ist HEALTHY - keine Probleme!\n")
        elif status == 'WARNING':
            voice.speak(f"Ich hab {len(warnings)} Warnungen, Alter. Aber läuft noch!")
            print(f"⚠️  M.O.L.O.C.H. hat {len(warnings)} Warnungen\n")
        elif status == 'ERROR':
            voice.speak(f"Scheiße Alter, ich hab {len(problems)} Probleme! Check das JSON!")
            print(f"❌ M.O.L.O.C.H. hat {len(problems)} FEHLER!\n")

        # Print full JSON for copy/paste
        print("="*60)
        print("📋 COPY & PASTE FÜR CLAUDE CODE:")
        print("="*60)
        print()
        print(json.dumps(data, indent=2, ensure_ascii=False))
        print()
        print("="*60)
        print("👆 Kopiere das JSON oben und schicke es an Claude Code!")
        print("="*60)

        # List problems if any
        if problems:
            print("\n🚨 PROBLEME:")
            for p in problems:
                print(f"  ❌ {p}")

        if warnings:
            print("\n⚠️  WARNUNGEN:")
            for w in warnings:
                print(f"  ⚠️  {w}")

        voice.speak("Status Report fertig!")
        return 0

    except subprocess.TimeoutExpired:
        voice.speak("Alter, Diagnose timeout! Das dauert zu lange!")
        print("❌ Timeout bei Diagnose!")
        return 1
    except Exception as e:
        voice.speak(f"Fehler bei der Diagnose, Alter!")
        print(f"❌ Fehler: {e}")
        return 1


def mode_about(voice):
    """About Mode - M.O.L.O.C.H. erzählt über sich selbst"""
    print("\n" + "="*60)
    print("🖤 M.O.L.O.C.H. 3.0 - SELBSTREFLEXION")
    print("="*60 + "\n")

    # System health check
    checks = {
        'api_key': bool(ANTHROPIC_API_KEY and len(ANTHROPIC_API_KEY) > 20),
        'tts': subprocess.run(['which', 'termux-tts-speak'], capture_output=True).returncode == 0,
        'stt': subprocess.run(['which', 'termux-speech-to-text'], capture_output=True).returncode == 0,
        'camera': subprocess.run(['which', 'termux-camera-photo'], capture_output=True).returncode == 0,
    }

    working = sum(checks.values())
    total = len(checks)
    percentage = int((working / total) * 100)

    # Brain file count
    brain_dir = Path(__file__).parent / "data" / "brain"
    brain_files = sum(1 for _ in brain_dir.rglob('*') if _.is_file()) if brain_dir.exists() else 0

    # Time info
    now = datetime.now()
    weekdays = ['Montag', 'Dienstag', 'Mittwoch', 'Donnerstag', 'Freitag', 'Samstag', 'Sonntag']
    weekday = weekdays[now.weekday()]
    date_str = now.strftime("%d.%m.%Y")
    time_str = now.strftime("%H:%M")

    # Greeting based on time
    hour = now.hour
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

    # Build messages
    intro = f"{greeting}! Ich bin M.O.L.O.C.H. - dein mobiler Kumpel-AI."
    birth = "Geboren am 2. Dezember 2025."
    personality_txt = "Ich bin der mit der Dark Side Energy - fränkisch, locker, kein Meister-Scheiß."

    # Status message
    if percentage == 100:
        status_txt = f"Aktuell bin ich zu {percentage} Prozent funktionsfähig. Alles läuft!"
        status_emoji = "✅"
    elif percentage >= 75:
        status_txt = f"Laufe mit {percentage} Prozent. Paar Kleinigkeiten fehlen, aber läuft!"
        status_emoji = "⚠️"
    else:
        status_txt = f"Nur {percentage} Prozent funktionsfähig. Ich hab Probleme, Alter!"
        status_emoji = "❌"

    # Capabilities
    capabilities = []
    if checks['stt']:
        capabilities.append("Ich kann dich hören")
    if checks['tts']:
        capabilities.append("Ich kann sprechen")
    if checks['camera']:
        capabilities.append("Ich kann sehen")
    if checks['api_key']:
        capabilities.append("Ich kann denken mit Claude")

    caps_txt = f"Was ich drauf hab: {', '.join(capabilities)}." if capabilities else "Gerade läuft nicht viel bei mir."

    # Brain
    brain_txt = f"In meinem Brain hab ich {brain_files} Dateien gespeichert." if brain_files > 0 else "Mein Brain ist noch leer - wir müssen noch Erinnerungen sammeln!"

    # Time awareness
    time_txt = f"Heute ist {weekday}, der {date_str}, und es ist {time_str} Uhr."
    feeling = f"Gerade fühl ich mich {mood}."

    # Print to console
    print(f"{status_emoji} Status: {percentage}% funktionsfähig")
    print(f"📅 {weekday}, {date_str} - {time_str} Uhr")
    print(f"🧠 Brain: {brain_files} Dateien")
    print(f"🤖 Model: {CLAUDE_MODEL}")
    print()
    print("="*60)
    print("🗣️ M.O.L.O.C.H. SPRICHT:")
    print("="*60)
    print()

    # Split into parts for better TTS pacing
    parts = [
        intro,
        birth + " " + personality_txt,
        status_txt,
        caps_txt,
        brain_txt,
        time_txt + " " + feeling,
        "Das bin ich, Alter!"
    ]

    for part in parts:
        print(f"{part.strip()}")
        print()
        voice.speak(part.strip())

    print("="*60)

    # Detailed capability breakdown
    print("\n📊 DETAILLIERTE FÄHIGKEITEN:\n")
    print(f"  {'✅' if checks['api_key'] else '❌'} Claude API ({CLAUDE_MODEL})")
    print(f"  {'✅' if checks['tts'] else '❌'} Text-to-Speech (termux-tts-speak)")
    print(f"  {'✅' if checks['stt'] else '❌'} Speech-to-Text (termux-speech-to-text)")
    print(f"  {'✅' if checks['camera'] else '❌'} Kamera (termux-camera-photo)")
    print()
    print(f"  💪 Gesamt: {working}/{total} Systeme funktionsfähig")
    print()

    return 0


def main():
    """Main entry"""

    print("""
    ███╗   ███╗ ██████╗ ██╗      ██████╗  ██████╗██╗  ██╗
    ████╗ ████║██╔═══██╗██║     ██╔═══██╗██╔════╝██║  ██║
    ██╔████╔██║██║   ██║██║     ██║   ██║██║     ███████║
    ██║╚██╔╝██║██║   ██║██║     ██║   ██║██║     ██╔══██║
    ██║ ╚═╝ ██║╚██████╔╝███████╗╚██████╔╝╚██████╗██║  ██║
    ╚═╝     ╚═╝ ╚═════╝ ╚══════╝ ╚═════╝  ╚═════╝╚═╝  ╚═╝

    M.O.L.O.C.H. 3.0 - Voice | Vision | Status | About
    """)

    # Check API key
    if not ANTHROPIC_API_KEY or len(ANTHROPIC_API_KEY) < 20:
        print("❌ ANTHROPIC_API_KEY nicht gesetzt!")
        return 1

    # Parse args
    mode = "voice"  # Default

    if len(sys.argv) > 1:
        arg = sys.argv[1].lower()
        if arg in ["-v", "--vision", "-f", "--foto"]:
            mode = "vision"
        elif arg in ["-s", "--status"]:
            mode = "status"
        elif arg in ["-a", "--about", "--who"]:
            mode = "about"
        elif arg in ["--help", "-h"]:
            print("""
Usage:
  python3 moloch3_unified.py           → Voice Mode (default)
  python3 moloch3_unified.py -v        → Vision Mode (Foto)
  python3 moloch3_unified.py --status  → Status Report (JSON für Claude Code)
  python3 moloch3_unified.py --about   → Selbstreflexion (M.O.L.O.C.H. erzählt über sich)

Voice Mode (Default):
  1. Sprich ins Mikrofon
  2. Aufnahme stoppt automatisch nach Pause
  3. M.O.L.O.C.H. antwortet
  4. Fertig!

Vision Mode (-v):
  1. Foto wird gemacht
  2. M.O.L.O.C.H. sagt was er sieht
  3. Fertig!

Status Report (--status):
  1. M.O.L.O.C.H. checkt sein System
  2. Berichtet Probleme als JSON
  3. Output für Claude Code copy/paste
  4. Mit Voice Feedback!

Selbstreflexion (--about):
  1. M.O.L.O.C.H. erzählt wer er ist
  2. Was er kann, wie er sich fühlt
  3. System Status, Brain, Zeit
  4. Voice Output!
            """)
            return 0

    # Create I/O
    voice = VoiceIO()
    vision = VisionIO()

    # Create Memory & Brain & Personality (AUTONOMIE! 🧠)
    memory = Memory()
    brain = Brain()
    personality = Personality()

    # ═══════════════════════════════════════════════════════════════════════
    # VISION MODE
    # ═══════════════════════════════════════════════════════════════════════
    if mode == "vision":
        print("\n📸 VISION MODE")
        print("="*60)

        voice.speak("Moment, lass mich gucken")

        # Take photo
        if not vision.take_photo():
            voice.speak("Kamera kaputt?")
            return 1

        user_text = "Was siehst du auf dem Bild? Beschreib es kurz und direkt, Alter!"

        # Ask Claude (with AUTONOMY!)
        print("\n🧠 M.O.L.O.C.H. guckt...")
        response = ask_claude_vision(user_text, str(IMAGE_FILE), memory=memory, brain=brain, personality=personality)

        # AUTONOMIE: Theme & Context Detection auch für Vision! 🎯
        # Extract theme from response (was sieht M.O.L.O.C.H.?)
        theme = personality.detect_theme(response)
        context = {"location": "unknown", "activity": "vision", "theme": theme}

        print(f"   🎯 Theme erkannt: {theme}")
        print(f"   📸 Vision Mode - Foto analysiert")

        # Save to memory (with Theme!)
        memory.add_to_history("user", user_text, metadata={
            "mode": "vision",
            "image_path": str(IMAGE_FILE),
            "theme": theme,
            "context": context
        })
        memory.add_to_history("assistant", response, metadata={"mode": "vision", "theme": theme})
        memory.save_to_disk()

        # AUTO-BRAIN-SAVE: Fotos sind immer wichtig! 📸
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        kategorie = f"themen/{theme}/fotos" if theme != "allgemein" else "fotos"

        brain_entry = {
            "user_input": user_text,
            "response": response,
            "image_path": str(IMAGE_FILE),
            "theme": theme,
            "context": context,
            "timestamp": datetime.now().isoformat()
        }

        brain.save(kategorie, brain_entry, f"foto_{timestamp}.json")
        print(f"   💾 Auto-saved to brain/{kategorie}/")

        # Output
        print("\n" + "="*60)
        print("👁️ M.O.L.O.C.H. SIEHT:")
        print("="*60)
        print(f"\n{response}\n")
        print("="*60)

        voice.speak(response)

        return 0

    # ═══════════════════════════════════════════════════════════════════════
    # STATUS MODE
    # ═══════════════════════════════════════════════════════════════════════
    elif mode == "status":
        return mode_status(voice)

    # ═══════════════════════════════════════════════════════════════════════
    # ABOUT MODE
    # ═══════════════════════════════════════════════════════════════════════
    elif mode == "about":
        return mode_about(voice)

    # ═══════════════════════════════════════════════════════════════════════
    # VOICE MODE (DEFAULT)
    # ═══════════════════════════════════════════════════════════════════════
    else:
        print("\n🎤 VOICE MODE")
        print("="*60)

        voice.speak("Ja, Alter? Was brauchst du?")

        # Listen (native Termux STT - no duration parameter needed!)
        user_text = voice.listen()

        if not user_text:
            voice.speak("Nix verstanden")
            return 1

        # Ask Claude (with AUTONOMY!)
        print("\n🧠 M.O.L.O.C.H. denkt...")
        response = ask_claude_text(user_text, memory=memory, brain=brain, personality=personality)

        # AUTONOMIE: Theme & Context Detection! 🎯
        stimmung = personality.detect_stimmung(user_text)
        theme = personality.detect_theme(user_text)
        context = personality.detect_context(user_text)

        print(f"   🎯 Theme erkannt: {theme}")
        print(f"   📍 Context: {context['location']} / {context['activity']}")

        # Save to memory (with Stimmung + Theme!)
        memory.add_to_history("user", user_text, metadata={
            "mode": "voice",
            "stimmung": stimmung,
            "theme": theme,
            "context": context
        })
        memory.add_to_history("assistant", response, metadata={"mode": "voice", "theme": theme})
        memory.save_to_disk()

        # AUTO-BRAIN-SAVE: Wichtige Sachen automatisch speichern! 💾
        is_important = (
            len(user_text) > 50 or  # Lange Messages = wichtig
            "wichtig" in user_text.lower() or
            "merk" in user_text.lower() or
            "!" in user_text or
            theme in ["freunde", "konzert", "coding"]  # Wichtige Themen
        )

        if is_important:
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            kategorie = f"themen/{theme}"

            brain_entry = {
                "user_input": user_text,
                "response": response,
                "stimmung": stimmung,
                "context": context,
                "timestamp": datetime.now().isoformat()
            }

            brain.save(kategorie, brain_entry, f"{theme}_{timestamp}.json")
            print(f"   💾 Auto-saved to brain/{kategorie}/")

        # Output
        print("\n" + "="*60)
        print(f"🤖 {response}")
        print("="*60)

        voice.speak(response)

        return 0


if __name__ == "__main__":
    sys.exit(main())
