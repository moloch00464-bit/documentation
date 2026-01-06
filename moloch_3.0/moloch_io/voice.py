#!/usr/bin/env python3
"""
M.O.L.O.C.H. 3.0 - Voice I/O
=============================
Speech-to-Text (20s Fixed Recording) + Text-to-Speech (Termux TTS)

KOSTENLOS WIE 2.0!
- termux-microphone-record (20s fixe Aufnahme!)
- Google Web Speech API (KOSTENLOS!)
- termux-tts-speak (lokal, kostenlos!)
- KEIN OpenAI/Anthropic Key nötig!
"""

import subprocess
import os
import time
from pathlib import Path
from typing import Optional

from core.config import DATA_DIR

# Try to import speech_recognition (will install if needed)
try:
    import speech_recognition as sr
except ImportError:
    sr = None


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

    def listen(self, duration: int = 20, smart: bool = False) -> Optional[str]:
        """
        Record audio for fixed duration and transcribe via Google Speech API

        KOSTENLOS! KEINE API Keys nötig!
        - termux-microphone-record (fixe Dauer, kein Auto-Stopp!)
        - Google Web Speech API (kostenlos!)
        - KEINE Kosten!

        Args:
            duration: Recording duration in seconds (default: 20)
            smart: Ignored (kept for backwards compatibility)

        Returns:
            Transcribed text or None
        """
        # Audio file paths - use M4A for termux-microphone-record with AAC encoder
        audio_raw = DATA_DIR / "voice_recording.m4a"
        audio_wav = DATA_DIR / "voice_recording.wav"

        print(f"🎤 AUFNAHME STARTET - {duration} SEKUNDEN!")
        print("   Sprich jetzt - Aufnahme stoppt NICHT bei Pausen!")
        print()

        try:
            # Step 1: Record audio for fixed duration
            if not self._record_audio(audio_raw, duration):
                return self._fallback_text_input()

            # Step 2: Convert to WAV (needed for SpeechRecognition)
            if not self._convert_to_wav(audio_raw, audio_wav):
                return self._fallback_text_input()

            # Step 3: Transcribe with Google Speech API (FREE!)
            text = self._transcribe_audio(audio_wav)

            if text:
                print(f"📝 Du: {text}")
                return text
            else:
                print("⚠️ Nichts verstanden")
                return self._fallback_text_input()

        except KeyboardInterrupt:
            print("\n⚠️ Abgebrochen")
            return None

        except Exception as e:
            print(f"❌ Voice Fehler: {e}")
            return self._fallback_text_input()

    def _record_audio(self, output_file: Path, duration: int) -> bool:
        """
        Record audio for fixed duration using termux-microphone-record

        Args:
            output_file: Path to save audio file
            duration: Recording duration in seconds

        Returns:
            Success status
        """
        # Remove old file
        if output_file.exists():
            output_file.unlink()

        try:
            # Start recording in background
            print(f"🎙️ Aufnahme läuft für {duration} Sekunden...")

            # Start termux-microphone-record (runs in background)
            proc = subprocess.Popen(
                ["termux-microphone-record", "-f", str(output_file), "-e", "aac"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            # Wait for specified duration
            time.sleep(duration)

            # Stop recording properly with termux-microphone-stop (not terminate!)
            subprocess.run(["termux-microphone-stop"], timeout=5)

            # Wait for process to finish
            proc.wait(timeout=5)

            print(f"⏹️ Aufnahme gestoppt")

            # Check if file was created
            if not output_file.exists():
                print("❌ Audio-Datei wurde nicht erstellt")
                return False

            # Check file size
            file_size = output_file.stat().st_size
            if file_size < 1000:  # Less than 1KB is probably broken
                print("❌ Audio-Datei zu klein (kaputt?)")
                return False

            print(f"✅ Aufnahme erfolgreich ({file_size / 1024:.1f} KB)")
            return True

        except FileNotFoundError:
            print("❌ termux-microphone-record nicht gefunden!")
            print("   Install: pkg install termux-api")
            return False

        except Exception as e:
            print(f"❌ Aufnahme Fehler: {e}")
            # Try to kill process if still running
            try:
                proc.kill()
            except:
                pass
            return False

    def _convert_to_wav(self, input_file: Path, output_file: Path) -> bool:
        """
        Convert audio file to WAV format using ffmpeg

        Args:
            input_file: Input audio file (.m4a)
            output_file: Output WAV file

        Returns:
            Success status
        """
        # Remove old WAV file
        if output_file.exists():
            output_file.unlink()

        try:
            # Convert with ffmpeg
            result = subprocess.run(
                ["ffmpeg", "-i", str(input_file), "-acodec", "pcm_s16le", "-ar", "16000", str(output_file), "-y"],
                capture_output=True,
                text=True,
                timeout=30
            )

            if result.returncode != 0:
                print(f"⚠️ Konvertierung fehlgeschlagen")
                if result.stderr:
                    print(f"   Error: {result.stderr}")
                return False

            if not output_file.exists():
                print("❌ WAV-Datei wurde nicht erstellt")
                return False

            print("✅ Audio konvertiert")
            return True

        except FileNotFoundError:
            print("❌ ffmpeg nicht gefunden!")
            print("   Install: pkg install ffmpeg")
            return False

        except Exception as e:
            print(f"❌ Konvertierungs-Fehler: {e}")
            return False

    def _transcribe_audio(self, audio_file: Path) -> Optional[str]:
        """
        Transcribe audio file using Google Web Speech API (FREE!)

        Args:
            audio_file: Path to audio file

        Returns:
            Transcribed text or None
        """
        if sr is None:
            print("⚠️ speech_recognition nicht installiert!")
            print("   Install: pip install SpeechRecognition")
            return None

        try:
            # Load audio file
            recognizer = sr.Recognizer()

            with sr.AudioFile(str(audio_file)) as source:
                audio_data = recognizer.record(source)

            # Transcribe with Google Web Speech API (FREE!)
            print("🔄 Transkribiere...")
            text = recognizer.recognize_google(audio_data, language="de-DE")

            return text.strip()

        except sr.UnknownValueError:
            print("⚠️ Google Speech konnte Audio nicht verstehen")
            return None

        except sr.RequestError as e:
            print(f"❌ Google Speech API Fehler: {e}")
            return None

        except Exception as e:
            print(f"❌ Transkriptions-Fehler: {e}")
            return None

    def _fallback_text_input(self) -> Optional[str]:
        """
        Fallback to text input if voice fails

        Returns:
            User text input or None
        """
        print("   📝 FALLBACK: Text-Eingabe aktiviert")
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
