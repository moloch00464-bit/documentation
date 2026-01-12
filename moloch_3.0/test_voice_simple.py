#!/usr/bin/env python3
"""
M.O.L.O.C.H. 3.0 - Simple Voice Test
=====================================
Test native Termux Speech-to-Text (NO Whisper!)
"""

import sys
import os
from pathlib import Path

# Add to path
sys.path.insert(0, str(Path(__file__).parent))

from moloch_io.voice import VoiceIO

def main():
    """Test simple voice recording"""

    print("""
    ███╗   ███╗ ██████╗ ██╗      ██████╗  ██████╗██╗  ██╗
    ████╗ ████║██╔═══██╗██║     ██╔═══██╗██╔════╝██║  ██║
    ██╔████╔██║██║   ██║██║     ██║   ██║██║     ███████║
    ██║╚██╔╝██║██║   ██║██║     ██║   ██║██║     ██╔══██║
    ██║ ╚═╝ ██║╚██████╔╝███████╗╚██████╔╝╚██████╗██║  ██║
    ╚═╝     ╚═╝ ╚═════╝ ╚══════╝ ╚═════╝  ╚═════╝╚═╝  ╚═╝

    M.O.L.O.C.H. 3.0 - NATIVE VOICE TEST
    """)

    print(f"\n{'='*60}")
    print(f"🎤 NATIVE TERMUX STT TEST")
    print(f"{'='*60}")
    print(f"\n💡 Strategie: Native termux-speech-to-text")
    print(f"   ✅ KEINE OpenAI Whisper API")
    print(f"   ✅ KEINE Kosten")
    print(f"   ✅ Stoppt automatisch bei Stille")
    print(f"\n{'='*60}")

    # Create voice
    voice = VoiceIO()

    # Greet
    voice.speak("Test läuft! Sprich jetzt!")

    # Listen with native Termux STT
    print(f"\n🎤 Mikrofon startet...")
    user_text = voice.listen()

    # Check result
    if not user_text:
        print("\n❌ Keine Transkription erhalten!")
        print("   Mögliche Gründe:")
        print("   - Mikrofon funktioniert nicht")
        print("   - termux-speech-to-text fehlt")
        print("   - Aufnahme zu leise")
        return 1

    # Success!
    print(f"\n{'='*60}")
    print(f"✅ TRANSKRIPTION ERFOLGREICH!")
    print(f"{'='*60}")
    print(f"\n📝 Du hast gesagt:")
    print(f"   '{user_text}'")
    print(f"\n{'='*60}")

    voice.speak("Test erfolgreich! Native STT funktioniert!")

    return 0


if __name__ == "__main__":
    sys.exit(main())
