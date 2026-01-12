#!/usr/bin/env python3
"""
M.O.L.O.C.H. 3.0 - Voice I/O
=============================
Native Termux Speech-to-Text + Text-to-Speech

NEW IMPLEMENTATION (3.0):
- Uses termux-speech-to-text (native Android STT)
- Uses termux-tts-speak (native Android TTS)
- NO OpenAI Whisper API (no costs!)
- NO audio file recording/conversion
- German language support (-l de-DE)
- Instant recognition
"""

import subprocess
from typing import Optional


class VoiceIO:
    """
    Voice Input/Output for M.O.L.O.C.H. 3.0

    NEW 3.0 IMPLEMENTATION:
    - Native Termux Speech-to-Text (termux-speech-to-text)
    - Native Termux Text-to-Speech (termux-tts-speak)
    - German language support by default
    - No external API dependencies
    - No audio file handling needed
    """

    def __init__(self):
        """Initialize Voice I/O (no external dependencies!)"""
        pass

    # ═══════════════════════════════════════════════════════════════════════════
    # TEXT-TO-SPEECH (Output)
    # ═══════════════════════════════════════════════════════════════════════════

    def speak(self, text: str, language: str = "de-DE") -> bool:
        """
        Speak text via TTS

        Args:
            text: Text to speak
            language: TTS language code (default: de-DE for German)

        Returns:
            Success status
        """
        # Always print (fallback if TTS fails)
        print(f"\n🗣️ {text}\n")

        try:
            result = subprocess.run(
                ["termux-tts-speak", "-l", language, text],
                capture_output=True,
                timeout=30,
                text=True
            )
            return result.returncode == 0

        except FileNotFoundError:
            print("❌ termux-tts-speak not found!")
            return False

        except subprocess.TimeoutExpired:
            print("⚠️ TTS timeout")
            return False

        except Exception as e:
            print(f"⚠️ TTS error: {e}")
            return False

    # ═══════════════════════════════════════════════════════════════════════════
    # SPEECH-TO-TEXT (Input) - NATIVE TERMUX STT (NO WHISPER!)
    # ═══════════════════════════════════════════════════════════════════════════

    def listen(self, language: str = "de-DE") -> Optional[str]:
        """
        Listen and transcribe via native Termux Speech-to-Text

        Uses Android's native speech recognition (no API costs!)
        - Supports offline recognition (device-dependent)
        - Uses Google Speech Services by default
        - No audio file creation needed
        - Instant transcription

        Args:
            language: Speech recognition language (default: de-DE for German)

        Returns:
            Transcribed text or None
        """
        print(f"🎤 SPRICH JETZT! (Sprache: {language})")
        print("   (Beende mit Stille oder Android Stop-Button)")

        try:
            result = subprocess.run(
                ["termux-speech-to-text", "-l", language],
                capture_output=True,
                timeout=60,
                text=True
            )

            if result.returncode != 0:
                print(f"❌ STT Error (code {result.returncode})")
                if result.stderr:
                    print(f"   {result.stderr.strip()}")
                return None

            # Parse output (usually just the text)
            text = result.stdout.strip()

            if not text:
                print("⚠️ Keine Sprache erkannt")
                return None

            print(f"📝 Du: {text}")
            return text

        except FileNotFoundError:
            print("❌ termux-speech-to-text nicht gefunden!")
            print("   Fix: pkg install termux-api")
            return None

        except subprocess.TimeoutExpired:
            print("⚠️ STT Timeout (60s)")
            return None

        except Exception as e:
            print(f"❌ STT Fehler: {e}")
            return None



# ═══════════════════════════════════════════════════════════════════════════════
# TESTING
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("\n🎤 M.O.L.O.C.H. 3.0 Voice I/O Test (Native Termux STT/TTS!)\n")

    voice = VoiceIO()

    # Test TTS (German)
    print("📝 Testing TTS (Deutsch)...")
    voice.speak("M.O.L.O.C.H. drei punkt null ist bereit!")

    # Test STT (German)
    print("\n📝 Testing STT (Deutsch)...")
    print("   (Sprich wenn du die Aufforderung siehst)")
    text = voice.listen()

    if text:
        print(f"\n✅ SUCCESS! Transkription: '{text}'")
        voice.speak(f"Du hast gesagt: {text}")
    else:
        print("\n⚠️ Keine Transkription")

    print()
