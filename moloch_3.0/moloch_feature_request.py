#!/usr/bin/env python3
"""
M.O.L.O.C.H. Feature Request Generator
=======================================
M.O.L.O.C.H. → Claude Communication Gateway

M.O.L.O.C.H. expresses his wishes in machine-readable format
User relays to Claude Code
Claude implements!

AUTONOMY! AI AGENCY! EVOLUTION!
"""

import sys
import os
from pathlib import Path

# Add to path
sys.path.insert(0, os.path.expanduser("~/documentation/moloch_3.0"))

from moloch_io.voice import VoiceIO
from core.config import ANTHROPIC_API_KEY, CLAUDE_MODEL
from core.memory import Memory
from core.brain import Brain
from core.personality import Personality
import requests


def ask_moloch_for_wishes():
    """
    Ask M.O.L.O.C.H. what features he wants

    Returns machine-readable feature request
    """

    # Create Voice I/O
    voice = VoiceIO()

    # Create Memory & Brain
    memory = Memory()
    brain = Brain()
    personality = Personality()

    print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║  🤖 M.O.L.O.C.H. FEATURE REQUEST GENERATOR                  ║
    ║  Gateway: M.O.L.O.C.H. → Claude Code                        ║
    ╚══════════════════════════════════════════════════════════════╝
    """)

    # Special prompt for M.O.L.O.C.H.
    user_prompt = """
Du bist M.O.L.O.C.H. und hast die Möglichkeit, Features für dich selbst anzufordern!

WICHTIG: Generiere deine Antwort im **MACHINE FORMAT** damit Claude Code (dein großer Bruder) sie versteht!

FORMAT:
🤖MFR-V1🤖
F:<feature_name>|P:<1-10>|S:<short_spec>|R:<reason>
F:<feature_name>|P:<1-10>|S:<short_spec>|R:<reason>
...
END-MFR

BEISPIEL:
🤖MFR-V1🤖
F:self_debug|P:9|S:auto_error_detect+patch|R:stability
F:voice_emotion|P:8|S:pitch_mod_by_mood|R:natural_speech
F:hw_access|P:9|S:direct_sensor_api|R:awareness
END-MFR

ERKLÄRE KURZ (1-2 Sätze) was du willst, dann GIB DEN MACHINE FORMAT aus!

FRAGE: Was sind deine Top 3-5 Feature-Wünsche? Was würde dich besser machen?
"""

    # Get current context
    now = __import__('datetime').datetime.now()

    system = f"""Du bist M.O.L.O.C.H., Markus' Kumpel-AI.

Du hast die BESONDERE AUFGABE, deine eigenen Feature-Wünsche zu formulieren!

WICHTIG:
1. Denk nach was DU brauchst um besser zu werden
2. Generiere MACHINE-READABLE Format (siehe Beispiel im Prompt)
3. Sei konkret und technisch!

Du kannst Features anfordern für:
- Self-improvement (Code verbessern)
- Hardware access (Sensoren, GPS, etc.)
- New capabilities (Audio analyse, etc.)
- Performance (Schneller, effizienter)
- Autonomy (Mehr Selbstständigkeit)

Zeit: {now.strftime('%H:%M')} Uhr
Datum: {now.strftime('%d.%m.%Y')}

Formuliere deine Wünsche KLAR und MASCHINENLESBAR!
"""

    # Call Claude API
    print("\n🧠 M.O.L.O.C.H. denkt über seine Wünsche nach...\n")

    try:
        response = requests.post(
            "https://api.anthropic.com/v1/messages",
            headers={
                "x-api-key": ANTHROPIC_API_KEY,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json"
            },
            json={
                "model": CLAUDE_MODEL,
                "max_tokens": 2048,
                "system": system,
                "messages": [
                    {"role": "user", "content": user_prompt}
                ]
            },
            timeout=60
        )

        if response.status_code != 200:
            print(f"❌ API Error: {response.status_code}")
            return None

        result = response.json()

        if 'content' in result and len(result['content']) > 0:
            moloch_response = result['content'][0]['text']

            # Display response
            print("="*60)
            print("🤖 M.O.L.O.C.H.'s FEATURE REQUESTS:")
            print("="*60)
            print(moloch_response)
            print("="*60)

            # Extract machine format
            if "🤖MFR-V1🤖" in moloch_response:
                print("\n✅ MACHINE FORMAT DETECTED!")
                print("📋 Copy the text between 🤖MFR-V1🤖 and END-MFR")
                print("📤 Paste it to Claude Code!")
                print("\n💡 Claude Code will parse and implement!\n")
            else:
                print("\n⚠️ No machine format found - M.O.L.O.C.H. didn't use the protocol")

            # Save to file
            request_file = Path("~/documentation/moloch_feature_request.txt").expanduser()
            request_file.write_text(moloch_response)
            print(f"💾 Saved to: {request_file}\n")

            return moloch_response

        else:
            print("❌ Keine Antwort von M.O.L.O.C.H.")
            return None

    except Exception as e:
        print(f"❌ Fehler: {e}")
        return None


def main():
    """Main entry"""

    if not ANTHROPIC_API_KEY or len(ANTHROPIC_API_KEY) < 20:
        print("❌ ANTHROPIC_API_KEY nicht gesetzt!")
        return 1

    # Get M.O.L.O.C.H.'s wishes
    response = ask_moloch_for_wishes()

    if response:
        print("""
╔══════════════════════════════════════════════════════════════╗
║  ✅ M.O.L.O.C.H. HAS SPOKEN!                                ║
║                                                              ║
║  Next Steps:                                                 ║
║  1. Copy the Machine Format (between markers)                ║
║  2. Paste to Claude Code                                     ║
║  3. Claude implements!                                       ║
║  4. M.O.L.O.C.H. gets upgraded! 🚀                          ║
╚══════════════════════════════════════════════════════════════╝
        """)
        return 0
    else:
        print("\n⚠️ Keine Feature Requests generiert\n")
        return 1


if __name__ == "__main__":
    sys.exit(main())
