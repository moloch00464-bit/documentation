#!/usr/bin/env python3
"""
M.O.L.O.C.H. 3.0 - Voice Test (WORKING 2.0 CODE!)
===================================================
Final test with exact 2.0 implementation
"""

import sys
import os

# Add moloch_3.0 to path
sys.path.insert(0, os.path.expanduser("~/documentation/moloch_3.0"))

from moloch_io.voice import VoiceIO

def main():
    print("\n" + "="*60)
    print("🎤 M.O.L.O.C.H. 3.0 VOICE TEST - WORKING 2.0 CODE!")
    print("="*60)

    voice = VoiceIO()

    # Test TTS first
    print("\n📢 Testing TTS...")
    success = voice.speak("Alter, M.O.L.O.C.H. drei punkt null ist ready!")

    if success:
        print("✅ TTS funktioniert!")
    else:
        print("⚠️ TTS hat Probleme, aber das ist OK")

    # Test STT
    print("\n🎤 Testing STT...")
    print("   (Sprich wenn du das Mikrofon-Symbol siehst)")
    print()

    text = voice.listen()

    if text:
        print(f"\n{'='*60}")
        print(f"✅✅✅ SUCCESS! ✅✅✅")
        print(f"{'='*60}")
        print(f"Du hast gesagt: '{text}'")
        print(f"{'='*60}\n")

        voice.speak(f"Perfekt, Alter! Du hast gesagt: {text}")

        return True
    else:
        print("\n❌ Keine Transkription erhalten")
        print("   Mögliche Probleme:")
        print("   - Kein Audio aufgenommen?")
        print("   - Whisper API Fehler?")
        print("   - Check OPENAI_API_KEY in ~/.bashrc")

        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
