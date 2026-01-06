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

    def __init__(self, voice_settings=None):
        """Initialize Voice I/O"""
        # Ensure data directory exists
        DATA_DIR.mkdir(parents=True, exist_ok=True)

        # Voice settings for emotion-based modulation
        self.voice_settings = voice_settings

    # ═══════════════════════════════════════════════════════════════════════════
    # TEXT-TO-SPEECH (Output) - WITH EMOTION SYNTHESIS! 🎭🎤
    # ═══════════════════════════════════════════════════════════════════════════

    def speak(self, text: str, stimmung: str = None, tageszeit: str = None, profile: str = None, fast_mode: bool = True) -> bool:
        """
        Speak text via Termux TTS with OPTIONAL emotion-based voice modulation!

        Args:
            text: Text to speak
            stimmung: Current mood (ignored in fast_mode)
            tageszeit: Time of day (ignored in fast_mode)
            profile: Voice profile (ignored in fast_mode)
            fast_mode: Use PERFORMANCE MODE (default=True) ⚡

        Returns:
            Success status

        PERFORMANCE MODE (fast_mode=True, DEFAULT) ⚡:
        - Fixed settings: Pitch 0.75, Rate 0.95 (M.O.L.O.C.H.'s Choice #1)
        - NO emotion synthesis processing
        - NO debug output
        - INSTANT responses!

        FEATURE MODE (fast_mode=False) 🎭:
        - Emotion Synthesis with processing overhead
        - Profile switching
        - Slower but more expressive
        """
        # Always print (fallback if TTS fails)
        print(f"\n🗣️ {text}\n")

        try:
            # Use full path to avoid PATH issues
            termux_tts = "/data/data/com.termux/files/usr/bin/termux-tts-speak"
            cmd = [termux_tts]

            if fast_mode:
                # ⚡ FAST MODE: Fixed settings, zero overhead!
                # M.O.L.O.C.H.'s favorite voice: Choice #1
                cmd.extend(["-p", "0.75", "-r", "0.95"])
            elif self.voice_settings:
                # 🎭 FEATURE MODE: Emotion synthesis (slower)
                params = self.voice_settings.get_voice_params(
                    stimmung=stimmung,
                    tageszeit=tageszeit,
                    profile=profile
                )
                cmd.extend(["-p", str(params["pitch"]), "-r", str(params["rate"])])

            # Add text to speak
            cmd.append(text)

            # Run TTS
            result = subprocess.run(
                cmd,
                capture_output=True,
                timeout=60,
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
        Listen to user via Recording + Google Speech API

        KOSTENLOS! Nutzt Google Web Speech API (FREE!)
        - termux-microphone-record (20s fixe Aufnahme)
        - Google Web Speech API (DEUTSCH!)
        - KEIN API Key nötig!
        - KEINE Kosten!

        Args:
            duration: Max recording duration in seconds (default: 20)
            smart: Ignored (kept for backwards compatibility)

        Returns:
            Transcribed text or None
        """
        print("🎤 SPRICH JETZT!")
        print(f"   (Aufnahme läuft {duration} Sekunden)")
        print()

        try:
            # Step 1: Record audio
            audio_file = DATA_DIR / "voice_input.m4a"
            wav_file = DATA_DIR / "voice_input.wav"

            if not self._record_audio(audio_file, duration):
                print("⚠️ Aufnahme fehlgeschlagen")
                return self._fallback_text_input()

            # Step 2: Convert to WAV
            if not self._convert_to_wav(audio_file, wav_file):
                print("⚠️ Konvertierung fehlgeschlagen")
                return self._fallback_text_input()

            # Step 3: Transcribe with Google Speech API (DEUTSCH!)
            text = self._transcribe_audio(wav_file)

            if not text:
                print("⚠️ Nichts verstanden")
                return self._fallback_text_input()

            print(f"📝 Du: {text}")
            return text

        except KeyboardInterrupt:
            print("\n⚠️ Abgebrochen")
            return None

        except Exception as e:
            print(f"❌ STT Fehler: {e}")
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

            # Start termux-microphone-record (runs in background, default encoder)
            # Use full path to avoid PATH issues in subprocess
            termux_record = "/data/data/com.termux/files/usr/bin/termux-microphone-record"
            proc = subprocess.Popen(
                [termux_record, "-f", str(output_file)],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            # Wait for specified duration
            time.sleep(duration)

            # Stop recording properly (use -q flag to quit)
            subprocess.run([termux_record, "-q"], timeout=5)

            # Wait for process to finish
            proc.wait(timeout=5)

            # IMPORTANT: Give file time to be fully written to disk
            time.sleep(1)  # Reduced from 2s to 1s for faster processing

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
            input_file: Input audio file (.mp3 or default format)
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
