#!/usr/bin/env python3
"""
M.O.L.O.C.H. 3.0 - Voice I/O
=============================
Speech-to-Text (Termux STT) + Text-to-Speech (Termux TTS)

KOSTENLOS WIE 2.0!
- termux-speech-to-text (lokal, kostenlos!)
- termux-tts-speak (lokal, kostenlos!)
- KEIN OpenAI Key nötig!
"""

import subprocess
import os
import time
from pathlib import Path
from typing import Optional

from core.config import DATA_DIR


class VoiceIO:
    """
    Voice Input/Output for M.O.L.O.C.H. 3.0

    KOSTENLOS wie M.O.L.O.C.H. 2.0:
    - termux-speech-to-text (STT)
    - termux-tts-speak (TTS)
    """

    def __init__(self):
        """Initialize Voice I/O"""
        # Ensure data directory exists
        DATA_DIR.mkdir(parents=True, exist_ok=True)

    # ═══════════════════════════════════════════════════════════════════════════
    # TEXT-TO-SPEECH (Output)
    # ═══════════════════════════════════════════════════════════════════════════

    def speak(self, text: str) -> bool:
        """
        Speak text via Termux TTS

        Args:
            text: Text to speak

        Returns:
            Success status
        """
        # Always print (fallback if TTS fails)
        print(f"\n🗣️ {text}\n")

        try:
            result = subprocess.run(
                ["termux-tts-speak", text],
                capture_output=True,
                timeout=30,
                text=True
            )
            return result.returncode == 0

        except FileNotFoundError:
            print("❌ termux-tts-speak not found!")
            print("   Install: pkg install termux-api")
            return False

        except subprocess.TimeoutExpired:
            print("⚠️ TTS timeout")
            return False

        except Exception as e:
            print(f"⚠️ TTS error: {e}")
            return False

    # ═══════════════════════════════════════════════════════════════════════════
    # SPEECH-TO-TEXT (Input) - TERMUX STT (KOSTENLOS!)
    # ═══════════════════════════════════════════════════════════════════════════

    def listen(self, duration: int = 60, smart: bool = False) -> Optional[str]:
        """
        Listen to user via Termux Speech-to-Text

        KOSTENLOS! Nutzt Termux API (lokal, kein Cloud-Service!)
        - Google Speech Recognition (on-device oder Google Cloud je nach Android)
        - KEIN API Key nötig!
        - KEINE Kosten!

        Args:
            duration: Max recording duration in seconds (default: 60)
            smart: Ignored (kept for backwards compatibility)

        Returns:
            Transcribed text or None
        """
        print("🎤 SPRICH JETZT!")
        print("   (Drücke CTRL+C zum Abbrechen)")
        print()

        try:
            # Run termux-speech-to-text
            result = subprocess.run(
                ["termux-speech-to-text", "-l", "de-DE"],  # German language
                capture_output=True,
                text=True,
                timeout=duration  # Use provided duration
            )

            if result.returncode != 0:
                stderr = result.stderr.strip()
                if stderr:
                    print(f"❌ STT Fehler: {stderr}")
                else:
                    print("❌ STT fehlgeschlagen (Mikrofon-Berechtigung?)")

                # FALLBACK: Use text input
                print("   📝 FALLBACK: Text-Eingabe aktiviert")
                print()
                try:
                    text = input("💬 Tippe deine Nachricht: ").strip()
                    if text:
                        print(f"📝 Du: {text}")
                        return text
                except (KeyboardInterrupt, EOFError):
                    print("\n⚠️ Abgebrochen")
                return None

            # Get transcribed text
            text = result.stdout.strip()

            if not text:
                print("⚠️ Nichts verstanden")
                return None

            print(f"📝 Du: {text}")
            return text

        except subprocess.TimeoutExpired:
            print("⏱️ Timeout - zu lange gewartet")
            return None

        except FileNotFoundError:
            # FALLBACK: Use text input if termux-speech-to-text not available
            print("⚠️ termux-speech-to-text nicht verfügbar")
            print("   📝 FALLBACK: Text-Eingabe aktiviert")
            print("   (Install termux-api für Voice: pkg install termux-api)")
            print()

            try:
                text = input("💬 Tippe deine Nachricht: ").strip()
                if text:
                    print(f"📝 Du: {text}")
                    return text
                return None
            except (KeyboardInterrupt, EOFError):
                print("\n⚠️ Abgebrochen")
                return None

        except KeyboardInterrupt:
            print("\n⚠️ Abgebrochen")
            return None

        except Exception as e:
            print(f"❌ STT Fehler: {e}")
            return None


# ═══════════════════════════════════════════════════════════════════════════════
# TESTING
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("\n🎤 M.O.L.O.C.H. 3.0 Voice I/O Test (KOSTENLOS!)\n")

    voice = VoiceIO()

    # Test TTS
    print("📝 Testing TTS...")
    voice.speak("M.O.L.O.C.H. drei punkt null ist bereit, Alter!")

    # Test STT
    print("\n📝 Testing STT...")
    print("   (Speak when prompted)")
    text = voice.listen()

    if text:
        print(f"\n✅ SUCCESS! Transcription: '{text}'")
        voice.speak(f"Du hast gesagt: {text}")
    else:
        print("\n⚠️ No transcription")

    print()
