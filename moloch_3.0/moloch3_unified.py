#!/usr/bin/env python3
"""
M.O.L.O.C.H. 3.0 - UNIFIED (Voice + Vision)
===========================================
Single command - Voice OR Vision mode!
"""

import sys
import os
import base64
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
            memory_context=memory_context
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
            memory_context=memory_context
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


def main():
    """Main entry"""

    print("""
    ███╗   ███╗ ██████╗ ██╗      ██████╗  ██████╗██╗  ██╗
    ████╗ ████║██╔═══██╗██║     ██╔═══██╗██╔════╝██║  ██║
    ██╔████╔██║██║   ██║██║     ██║   ██║██║     ███████║
    ██║╚██╔╝██║██║   ██║██║     ██║   ██║██║     ██╔══██║
    ██║ ╚═╝ ██║╚██████╔╝███████╗╚██████╔╝╚██████╗██║  ██║
    ╚═╝     ╚═╝ ╚═════╝ ╚══════╝ ╚═════╝  ╚═════╝╚═╝  ╚═╝

    M.O.L.O.C.H. 3.0 UNIFIED - Voice + Vision
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
        elif arg in ["--help", "-h"]:
            print("""
Usage:
  python3 moloch3_unified.py           → Voice Mode (default)
  python3 moloch3_unified.py -v        → Vision Mode (Foto)

Voice Mode:
  1. Sprich ins Mikrofon
  2. Aufnahme stoppt automatisch nach Pause
  3. M.O.L.O.C.H. antwortet
  4. Fertig!

Vision Mode:
  1. Foto wird gemacht
  2. M.O.L.O.C.H. sagt was er sieht
  3. Fertig!
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

        # Save to memory
        memory.add_to_history("user", user_text, metadata={"mode": "vision", "image_path": str(IMAGE_FILE)})
        memory.add_to_history("assistant", response, metadata={"mode": "vision"})
        memory.save_to_disk()

        # Output
        print("\n" + "="*60)
        print("👁️ M.O.L.O.C.H. SIEHT:")
        print("="*60)
        print(f"\n{response}\n")
        print("="*60)

        voice.speak(response)

        return 0

    # ═══════════════════════════════════════════════════════════════════════
    # VOICE MODE (DEFAULT)
    # ═══════════════════════════════════════════════════════════════════════
    else:
        print("\n🎤 VOICE MODE")
        print("="*60)

        voice.speak("Ja, Alter? Was brauchst du?")

        # Listen (20 seconds fixed - NO PAUSE DETECTION!)
        user_text = voice.listen(duration=20, smart=False)

        if not user_text:
            voice.speak("Nix verstanden")
            return 1

        # Ask Claude (with AUTONOMY!)
        print("\n🧠 M.O.L.O.C.H. denkt...")
        response = ask_claude_text(user_text, memory=memory, brain=brain, personality=personality)

        # Save to memory (with Stimmung!)
        stimmung = personality.detect_stimmung(user_text)
        memory.add_to_history("user", user_text, metadata={"mode": "voice", "stimmung": stimmung})
        memory.add_to_history("assistant", response, metadata={"mode": "voice"})
        memory.save_to_disk()

        # Output
        print("\n" + "="*60)
        print(f"🤖 {response}")
        print("="*60)

        voice.speak(response)

        return 0


if __name__ == "__main__":
    sys.exit(main())
