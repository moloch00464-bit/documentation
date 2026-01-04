#!/usr/bin/env python3
"""
M.O.L.O.C.H. 3.0 - Voice I/O
=============================
Speech-to-Text (Whisper) + Text-to-Speech (TTS)
"""

import subprocess
import os
import time
from pathlib import Path
from typing import Optional
import requests

from core.config import (
    AUDIO_FILE,
    MAX_RECORDING_TIME,
    AUDIO_SAMPLE_RATE,
    AUDIO_CHANNELS,
    OPENAI_API_KEY,
    MOLOCH_DIR
)


class VoiceIO:
    """
    Voice Input/Output for M.O.L.O.C.H. 3.0

    Features:
    - TTS via termux-tts-speak
    - STT via termux-microphone-record + Whisper API
    - Robust error handling
    """

    def __init__(self, openai_api_key: str = None):
        """
        Initialize Voice I/O

        Args:
            openai_api_key: OpenAI API Key for Whisper
        """
        self.openai_key = openai_api_key or OPENAI_API_KEY

    # ═══════════════════════════════════════════════════════════════════════════
    # TEXT-TO-SPEECH (Output)
    # ═══════════════════════════════════════════════════════════════════════════

    def speak(self, text: str) -> bool:
        """
        Speak text via TTS

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

            if result.returncode == 0:
                return True
            else:
                print("💡 TTS not available - but text is shown above! ☝️")
                return False

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
    # SPEECH-TO-TEXT (Input)
    # ═══════════════════════════════════════════════════════════════════════════

    def listen(self, max_seconds: int = MAX_RECORDING_TIME) -> Optional[str]:
        """
        Record audio and transcribe via Whisper

        Args:
            max_seconds: Max recording time

        Returns:
            Transcribed text or None

        Process:
        1. termux-microphone-record → AAC file
        2. ffmpeg → WAV conversion
        3. Whisper API → Transcription
        """
        print(f"🎙️ Listening (max {max_seconds} seconds)...")

        # Step 1: Record audio
        temp_file = self._record_audio(max_seconds)
        if not temp_file:
            return None

        # Step 2: Convert to WAV
        if not self._convert_to_wav(temp_file):
            return None

        # Step 3: Transcribe with Whisper
        transcription = self._transcribe_whisper()

        # Cleanup temp file
        try:
            os.remove(temp_file)
        except:
            pass

        return transcription

    def _record_audio(self, max_seconds: int) -> Optional[str]:
        """
        Record audio via termux-microphone-record

        Args:
            max_seconds: Max recording time

        Returns:
            Path to temp audio file or None
        """
        # Temp file path
        temp_file = str(MOLOCH_DIR / "data" / "temp_recording.m4a")

        # Remove old file
        if os.path.exists(temp_file):
            try:
                os.remove(temp_file)
            except:
                pass

        # Remove old WAV too
        if os.path.exists(AUDIO_FILE):
            try:
                os.remove(AUDIO_FILE)
            except:
                pass

        try:
            # Record
            result = subprocess.run(
                [
                    "termux-microphone-record",
                    "-f", temp_file,
                    "-l", str(max_seconds),
                    "-e", "aac"
                ],
                capture_output=True,
                timeout=max_seconds + 5,
                text=True
            )

            # Wait for file
            time.sleep(1)

            # Check if file exists
            if not os.path.exists(temp_file):
                print("⚠️ No audio file created")
                return None

            return temp_file

        except FileNotFoundError:
            print("❌ termux-microphone-record not found!")
            print("   Install: pkg install termux-api")
            return None

        except subprocess.TimeoutExpired:
            print("⚠️ Recording timeout")
            return None

        except Exception as e:
            print(f"❌ Recording error: {e}")
            return None

    def _convert_to_wav(self, input_file: str) -> bool:
        """
        Convert audio to WAV via ffmpeg

        Args:
            input_file: Path to input audio file

        Returns:
            Success status
        """
        print("🔄 Converting to WAV...")

        try:
            result = subprocess.run(
                [
                    "ffmpeg", "-y", "-i", input_file,
                    "-ar", str(AUDIO_SAMPLE_RATE),
                    "-ac", str(AUDIO_CHANNELS),
                    "-acodec", "pcm_s16le",
                    str(AUDIO_FILE)
                ],
                capture_output=True,
                timeout=30,
                text=True
            )

            if not os.path.exists(AUDIO_FILE):
                print("❌ WAV conversion failed")
                return False

            return True

        except FileNotFoundError:
            print("❌ ffmpeg not found!")
            print("   Install: pkg install ffmpeg")
            return False

        except subprocess.TimeoutExpired:
            print("⚠️ Conversion timeout")
            return False

        except Exception as e:
            print(f"❌ Conversion error: {e}")
            return False

    def _transcribe_whisper(self) -> Optional[str]:
        """
        Transcribe audio via Whisper API

        Returns:
            Transcribed text or None
        """
        if not self.openai_key:
            print("❌ OPENAI_API_KEY not set!")
            return None

        if not os.path.exists(AUDIO_FILE):
            print("❌ No audio file to transcribe")
            return None

        print("🧠 Transcribing with Whisper...")

        try:
            # Open audio file
            with open(AUDIO_FILE, "rb") as audio_file:
                # Whisper API call
                response = requests.post(
                    "https://api.openai.com/v1/audio/transcriptions",
                    headers={
                        "Authorization": f"Bearer {self.openai_key}"
                    },
                    files={
                        "file": ("audio.wav", audio_file, "audio/wav")
                    },
                    data={
                        "model": "whisper-1",
                        "language": "de"  # German
                    },
                    timeout=60
                )

            if response.status_code != 200:
                print(f"❌ Whisper API error: {response.status_code}")
                print(f"   {response.text}")
                return None

            # Extract transcription
            result = response.json()
            text = result.get("text", "").strip()

            if text:
                print(f"✅ Transcribed: '{text}'")
                return text
            else:
                print("⚠️ Empty transcription")
                return None

        except requests.exceptions.Timeout:
            print("⚠️ Whisper API timeout")
            return None

        except Exception as e:
            print(f"❌ Whisper error: {e}")
            return None


# ═══════════════════════════════════════════════════════════════════════════════
# TESTING
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("\n🎤 M.O.L.O.C.H. 3.0 Voice I/O Test\n")

    voice = VoiceIO()

    # Test TTS
    print("📝 Testing TTS...")
    success = voice.speak("Test Test, eins zwei drei")
    print(f"   {'✅' if success else '⚠️'} TTS: {success}")

    # Note: STT test requires actual microphone recording
    # Can't be tested without user interaction
    print("\n💡 STT test requires actual voice input - skipped in automated test")

    print()
