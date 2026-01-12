#!/usr/bin/env python3
"""
M.O.L.O.C.H. 3.0 - Voice I/O
=============================
Offline German Speech-to-Text + Text-to-Speech

LATEST IMPLEMENTATION (Jan 2026):
- PRIMARY: Vosk offline German STT (beste Qualität!)
- FALLBACK: termux-speech-to-text (Android native)
- TTS: termux-tts-speak (native Android TTS)
- NO OpenAI Whisper API (no costs!)
- Offline + German language support
- Instant recognition

VOSK ADVANTAGES:
✅ Better recognition quality than termux-speech-to-text
✅ Explicit German language model
✅ Offline (no internet needed)
✅ Free (no API costs)
✅ Works on Termux/Android
"""

import subprocess
import json
import os
import tempfile
import wave
from typing import Optional
from pathlib import Path

# Try to import Vosk (optional - fallback to termux-speech-to-text if not available)
try:
    from vosk import Model, KaldiRecognizer
    VOSK_AVAILABLE = True
except ImportError:
    VOSK_AVAILABLE = False


class VoiceIO:
    """
    Voice Input/Output for M.O.L.O.C.H. 3.0

    LATEST 3.0 IMPLEMENTATION (Jan 2026):
    - PRIMARY: Vosk offline German STT (best quality!)
    - FALLBACK: Native Termux Speech-to-Text (termux-speech-to-text)
    - TTS: Native Termux Text-to-Speech (termux-tts-speak)
    - German language support by default
    - Offline + No API costs
    """

    def __init__(self):
        """Initialize Voice I/O with Vosk model (if available)"""
        self.vosk_model = None
        self.vosk_model_path = None

        # Try to load Vosk German model
        if VOSK_AVAILABLE:
            # Default model path
            model_dir = Path.home() / "documentation" / "moloch_3.0" / "vosk_models" / "vosk-model-small-de-0.15"

            if model_dir.exists():
                try:
                    print(f"🎤 Loading Vosk German model... ", end='', flush=True)
                    self.vosk_model = Model(str(model_dir))
                    self.vosk_model_path = model_dir
                    print("✅")
                except Exception as e:
                    print(f"⚠️ Failed: {e}")
                    print("   → Falling back to termux-speech-to-text")
            else:
                print(f"ℹ️  Vosk model not found at {model_dir}")
                print(f"   → Install with: bash install_vosk_german.sh")
                print(f"   → Using termux-speech-to-text fallback")

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
    # SPEECH-TO-TEXT (Input) - VOSK OFFLINE GERMAN (PRIMARY) + TERMUX FALLBACK
    # ═══════════════════════════════════════════════════════════════════════════

    def listen(self) -> Optional[str]:
        """
        Listen and transcribe speech (Vosk German primary, Termux fallback)

        STRATEGY:
        1. Try Vosk offline German STT (best quality, explicit German)
        2. Fallback to termux-speech-to-text (if Vosk not available)

        Returns:
            Transcribed text or None
        """
        # Primary: Try Vosk offline German STT
        if self.vosk_model:
            text = self._listen_vosk()
            if text:
                return text
            # Vosk failed, try fallback
            print("   ⚠️  Vosk failed, trying termux-speech-to-text...")

        # Fallback: termux-speech-to-text
        return self._listen_termux()

    def _listen_vosk(self) -> Optional[str]:
        """
        Listen via Vosk offline German STT

        Uses termux-microphone-record to capture audio,
        then processes with Vosk German model.

        Returns:
            Transcribed German text or None
        """
        print(f"🎤 SPRICH JETZT! (Vosk Offline German STT)")
        print("   (Recording 5 seconds...)")

        # Temp file for audio recording
        temp_audio = tempfile.NamedTemporaryFile(suffix='.wav', delete=False)
        temp_path = temp_audio.name
        temp_audio.close()

        try:
            # 1. Record audio with termux-microphone-record
            # Format: WAV, 16kHz, mono (Vosk requirement)
            result = subprocess.run(
                [
                    "termux-microphone-record",
                    "-d", "5",  # Duration: 5 seconds
                    "-f", temp_path,
                    "-e", "wav",
                    "-r", "16000",  # Sample rate: 16kHz (Vosk optimal)
                    "-c", "1"  # Channels: 1 (mono)
                ],
                capture_output=True,
                timeout=10,
                text=True
            )

            if result.returncode != 0:
                print(f"❌ Recording failed (code {result.returncode})")
                return None

            # 2. Check if audio file was created
            if not os.path.exists(temp_path) or os.path.getsize(temp_path) == 0:
                print("❌ No audio recorded")
                return None

            # 3. Process with Vosk
            print("   🔄 Processing with Vosk...")

            wf = wave.open(temp_path, "rb")

            # Verify audio format
            if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getframerate() != 16000:
                print(f"⚠️  Audio format mismatch: {wf.getnchannels()}ch, {wf.getsampwidth()}byte, {wf.getframerate()}Hz")
                print("   → Expected: 1ch, 2byte, 16000Hz")
                wf.close()
                return None

            # Create recognizer
            rec = KaldiRecognizer(self.vosk_model, wf.getframerate())
            rec.SetWords(True)

            # Process audio
            transcription_parts = []
            while True:
                data = wf.readframes(4000)
                if len(data) == 0:
                    break
                if rec.AcceptWaveform(data):
                    result = json.loads(rec.Result())
                    if 'text' in result and result['text']:
                        transcription_parts.append(result['text'])

            # Get final result
            final_result = json.loads(rec.FinalResult())
            if 'text' in final_result and final_result['text']:
                transcription_parts.append(final_result['text'])

            wf.close()

            # Combine transcription
            text = ' '.join(transcription_parts).strip()

            if not text:
                print("⚠️ Keine Sprache erkannt (Vosk)")
                return None

            print(f"📝 Du: {text}")
            return text

        except FileNotFoundError:
            print("❌ termux-microphone-record not found!")
            print("   Fix: pkg install termux-api")
            return None

        except subprocess.TimeoutExpired:
            print("⚠️ Recording timeout")
            return None

        except Exception as e:
            print(f"❌ Vosk error: {e}")
            return None

        finally:
            # Cleanup temp file
            try:
                if os.path.exists(temp_path):
                    os.unlink(temp_path)
            except:
                pass

    def _listen_termux(self) -> Optional[str]:
        """
        Listen via native Termux Speech-to-Text (FALLBACK)

        Uses Android's native speech recognition (no API costs!)
        - Uses system-wide language settings (Settings → Google Voice Typing)
        - Supports offline recognition (device-dependent)
        - Uses Google Speech Services by default
        - No audio file creation needed
        - Instant transcription

        IMPORTANT: Language is set in Android settings, NOT via command-line!
        To use German: Settings → Language & Input → Google Voice Typing → Languages → Deutsch

        Returns:
            Transcribed text or None
        """
        print(f"🎤 SPRICH JETZT! (Termux Native STT)")
        print("   (Beende mit Stille oder Android Stop-Button)")
        print("   ⚙️  Sprache: Android System-Einstellung")

        try:
            result = subprocess.run(
                ["termux-speech-to-text"],
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
