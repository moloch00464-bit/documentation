#!/usr/bin/env python3
"""
M.O.L.O.C.H. 3.0 - Simple Voice Test
=====================================
Test simple 20s recording - NO SMART PAUSE DETECTION!
"""

import sys
import os
from pathlib import Path

# Add to path
sys.path.insert(0, str(Path(__file__).parent))

from moloch_io.voice import VoiceIO
from core.config import OPENAI_API_KEY, RECORDING_DURATION

def main():
    """Test simple voice recording"""

    print("""
    ███╗   ███╗ ██████╗ ██╗      ██████╗  ██████╗██╗  ██╗
    ████╗ ████║██╔═══██╗██║     ██╔═══██╗██╔════╝██║  ██║
    ██╔████╔██║██║   ██║██║     ██║   ██║██║     ███████║
    ██║╚██╔╝██║██║   ██║██║     ██║   ██║██║     ██╔══██║
    ██║ ╚═╝ ██║╚██████╔╝███████╗╚██████╔╝╚██████╗██║  ██║
    ╚═╝     ╚═╝ ╚═════╝ ╚══════╝ ╚═════╝  ╚═════╝╚═╝  ╚═╝

    M.O.L.O.C.H. 3.0 - SIMPLE VOICE TEST
    """)

    # Check API key
    if not OPENAI_API_KEY or len(OPENAI_API_KEY) < 20:
        print("❌ OPENAI_API_KEY nicht gesetzt!")
        return 1

    print(f"\n{'='*60}")
    print(f"🎤 SIMPLE RECORDING TEST")
    print(f"{'='*60}")
    print(f"\n💡 Strategie: {RECORDING_DURATION} Sekunden FIXE Aufnahme")
    print(f"   ✅ KEINE Pause-Detection")
    print(f"   ✅ KEINE Lautstärke-Messung")
    print(f"   ✅ Einfach {RECORDING_DURATION}s aufnehmen und fertig!")
    print(f"\n{'='*60}")

    # Create voice
    voice = VoiceIO()

    # Greet
    voice.speak(f"Test läuft! Sprich {RECORDING_DURATION} Sekunden lang!")

    # Listen with SIMPLE mode (no smart detection!)
    print(f"\n🎤 Recording startet...")
    user_text = voice.listen(duration=RECORDING_DURATION, smart=False)

    # Check result
    if not user_text:
        print("\n❌ Keine Transkription erhalten!")
        print("   Mögliche Gründe:")
        print("   - Mikrofon funktioniert nicht")
        print("   - Whisper API Error")
        print("   - Aufnahme zu leise")
        return 1

    # Success!
    print(f"\n{'='*60}")
    print(f"✅ TRANSKRIPTION ERFOLGREICH!")
    print(f"{'='*60}")
    print(f"\n📝 Du hast gesagt:")
    print(f"   '{user_text}'")
    print(f"\n{'='*60}")

    voice.speak("Test erfolgreich! Simple Mode funktioniert!")

    return 0


if __name__ == "__main__":
    sys.exit(main())
