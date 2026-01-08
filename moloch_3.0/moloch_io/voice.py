#!/usr/bin/env python3
"""
M.O.L.O.C.H. 3.0 - Voice I/O
=============================
Speech-to-Text (Whisper) + Text-to-Speech (TTS)

FIXED: Using EXACT working 2.0 implementation!
- .mp4 raw → .mp3 final (NOT .m4a or .wav!)
- Smart recording with byte monitoring
- Direct Whisper API (NO ffmpeg conversion!)
- audio/mpeg MIME type
"""

import subprocess
import os
import time
from pathlib import Path
from typing import Optional
import requests

from core.config import (
    AUDIO_RAW,
    AUDIO_FILE,
    MIN_RECORDING_TIME,
    MAX_RECORDING_TIME,
    SILENCE_DURATION,
    SPEECH_THRESHOLD,
    OPENAI_API_KEY,
    DATA_DIR
)


class VoiceIO:
    """
    Voice Input/Output for M.O.L.O.C.H. 3.0

    Uses WORKING 2.0 implementation:
    - Smart recording (bytes/time monitoring)
    - .mp4 → .mp3 format
    - Direct Whisper API
    """

    def __init__(self, openai_api_key: str = None):
        """Initialize Voice I/O"""
        self.openai_key = openai_api_key or OPENAI_API_KEY

        # Ensure data directory exists
        DATA_DIR.mkdir(parents=True, exist_ok=True)

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
    # SPEECH-TO-TEXT (Input) - WORKING 2.0 CODE!
    # ═══════════════════════════════════════════════════════════════════════════

    def listen(self, duration: int = 20, smart: bool = False) -> Optional[str]:
        """
        Record audio and transcribe via Whisper

        Args:
            duration: Recording duration in seconds (default: 20)
            smart: Use smart pause detection (default: False - SIMPLE MODE!)

        Returns:
            Transcribed text or None
        """
        # Step 1: Record audio
        if smart:
            # Smart recording with pause detection (UNRELIABLE!)
            if not self._record_audio_smart():
                return None
        else:
            # Simple fixed-duration recording (RELIABLE!)
            if not self._record_audio_simple(duration):
                return None

        # Step 2: Convert .mp4 → .mp3
        if not self._convert_mp4_to_mp3():
            return None

        # Step 3: Transcribe with Whisper
        return self._transcribe_whisper()

    def _record_audio_simple(self, duration: int) -> bool:
        """
        Simple Fixed-Duration Recording - NO SMART PAUSE DETECTION!

        MOST RELIABLE APPROACH:
        - Records for fixed duration (default 20s)
        - No threshold detection
        - No pause detection
        - Just records and stops

        Args:
            duration: Recording duration in seconds

        Returns:
            Success status
        """
        # Delete old files
        for f in [AUDIO_RAW, AUDIO_FILE]:
            if os.path.exists(f):
                try:
                    os.remove(f)
                except:
                    pass

        print(f"🎤 SPRICH JETZT! ({duration} Sekunden)")
        print(f"⏱️  ", end="", flush=True)

        # Start recording with fixed limit
        try:
            proc = subprocess.Popen(
                ["termux-microphone-record", "-f", str(AUDIO_RAW), "-l", str(duration)],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
        except FileNotFoundError:
            print("\n❌ termux-microphone-record nicht gefunden")
            return False

        # Wait for recording to complete
        start_time = time.time()
        while time.time() - start_time < duration:
            elapsed = int(time.time() - start_time)
            remaining = duration - elapsed
            print(f"\r⏱️  {remaining}s... ", end="", flush=True)
            time.sleep(1)

        print(f"\r⏱️  Fertig! ({duration}s)         ")

        # Stop recording (just in case)
        try:
            subprocess.run(
                ["termux-microphone-record", "-q"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                timeout=2
            )
        except:
            pass

        # Wait a bit for file to be finalized
        time.sleep(0.5)

        # Verify file exists and has content
        if not os.path.exists(AUDIO_RAW):
            print("❌ Keine Aufnahme erstellt!")
            return False

        file_size = os.path.getsize(AUDIO_RAW)
        if file_size < 1000:
            print(f"⚠️ Aufnahme zu klein ({file_size} bytes)")
            return False

        print(f"✅ Aufnahme fertig ({file_size / 1024:.1f} KB)")
        return True

    def _record_audio_smart(self) -> bool:
        """
        Smart Recording: Records until pause detected

        EXACT 2.0 ALGORITHM:
        - Measures bytes per time unit (not just file growth)
        - "Loud" = many bytes = speech
        - "Quiet" = few bytes = silence/noise
        - Stops after SILENCE_DURATION seconds of "quiet" audio

        Returns:
            Success status
        """
        # Delete old files
        for f in [AUDIO_RAW, AUDIO_FILE]:
            if os.path.exists(f):
                try:
                    os.remove(f)
                except:
                    pass

        print(f"🎤 SPRICH JETZT! (min {MIN_RECORDING_TIME}s, max {MAX_RECORDING_TIME}s)")

        # Start recording with NO LIMIT (-l 0)
        try:
            proc = subprocess.Popen(
                ["termux-microphone-record", "-f", str(AUDIO_RAW), "-l", "0"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
        except FileNotFoundError:
            print("❌ termux-microphone-record nicht gefunden")
            return False

        start_time = time.time()
        last_size = 0
        last_loud_time = time.time()  # When did we last hear LOUD audio?
        got_speech = False  # Did we detect any speech at all?

        try:
            # Wait for file to be created
            time.sleep(0.5)

            while True:
                elapsed = time.time() - start_time

                # Max time reached
                if elapsed >= MAX_RECORDING_TIME:
                    print(f"\n⏱️ Max Zeit ({MAX_RECORDING_TIME}s)")
                    break

                # Check file size
                if os.path.exists(AUDIO_RAW):
                    try:
                        current_size = os.path.getsize(AUDIO_RAW)
                    except OSError:
                        time.sleep(0.2)
                        continue

                    # Growth = bytes since last check (per 200ms)
                    growth = current_size - last_size
                    last_size = current_size

                    # SIMPLE LOGIC:
                    # > SPEECH_THRESHOLD (150) = Speech (█) = Reset Timer
                    # <= SPEECH_THRESHOLD = Silence (.) = counts to pause
                    if growth > SPEECH_THRESHOLD:
                        last_loud_time = time.time()  # Reset timer ONLY on speech!
                        got_speech = True
                        print("█", end="", flush=True)
                    else:
                        print(".", end="", flush=True)

                    # ALWAYS check after MIN_RECORDING_TIME!
                    if elapsed >= MIN_RECORDING_TIME:
                        quiet_duration = time.time() - last_loud_time

                        # STOP if SILENCE_DURATION without █
                        if quiet_duration >= SILENCE_DURATION:
                            if got_speech:
                                print(f"\n🔇 {quiet_duration:.1f}s Pause - Stopp!")
                            else:
                                print(f"\n🔇 Keine Sprache erkannt - Stopp!")
                            break

                time.sleep(0.2)  # Check every 200ms

        except KeyboardInterrupt:
            print("\n⚠️ Abgebrochen")

        # Stop recording - multiple attempts
        for _ in range(3):
            result = subprocess.run(
                ["termux-microphone-record", "-q"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            time.sleep(0.1)
            if result.returncode == 0:
                break

        # Wait for file to be written
        time.sleep(0.3)

        # Check if we got audio
        if not os.path.exists(AUDIO_RAW):
            print("❌ Keine Audio-Datei erstellt")
            return False

        # Check file size
        try:
            size = os.path.getsize(AUDIO_RAW)
            print(f"✅ Aufnahme: {size} bytes")

            if size < 1000:
                print("⚠️ Audio zu kurz")
                return False

            return True

        except:
            return False

    def _convert_mp4_to_mp3(self) -> bool:
        """
        Convert .mp4 → .mp3

        NOTE: In 2.0 this is done by just renaming/copying.
        Whisper accepts .mp4 with audio/mpeg MIME!

        Returns:
            Success status
        """
        if not os.path.exists(AUDIO_RAW):
            return False

        try:
            # Simple copy (Whisper accepts the .mp4 as "audio.mp3"!)
            import shutil
            shutil.copy(str(AUDIO_RAW), str(AUDIO_FILE))
            return True

        except Exception as e:
            print(f"❌ Konvertierung fehlgeschlagen: {e}")
            return False

    def _transcribe_whisper(self) -> Optional[str]:
        """
        Transcribe audio via Whisper API

        EXACT 2.0 IMPLEMENTATION:
        - Sends .mp3 file (actually .mp4 content)
        - Uses "audio/mpeg" MIME type
        - German language

        Returns:
            Transcribed text or None
        """
        if not os.path.exists(AUDIO_FILE):
            return ""

        # Check file size
        try:
            size = os.path.getsize(AUDIO_FILE)
            if size < 1000:
                print("⚠️ Audio zu kurz")
                return ""
        except:
            return ""

        print("🧠 Whisper denkt...")

        try:
            with open(AUDIO_FILE, "rb") as f:
                response = requests.post(
                    "https://api.openai.com/v1/audio/transcriptions",
                    headers={"Authorization": f"Bearer {self.openai_key}"},
                    files={"file": ("audio.mp3", f, "audio/mpeg")},  # CRITICAL!
                    data={"model": "whisper-1", "language": "de"},
                    timeout=30
                )

            result = response.json()

            if "error" in result:
                print(f"❌ Whisper Error: {result['error']}")
                return ""

            text = result.get("text", "").strip()

            if text:
                print(f"📝 Du: {text}")

            return text

        except requests.Timeout:
            print("❌ Whisper Timeout")
        except Exception as e:
            print(f"❌ Whisper Fehler: {e}")

        return ""


# ═══════════════════════════════════════════════════════════════════════════════
# TESTING
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("\n🎤 M.O.L.O.C.H. 3.0 Voice I/O Test (WORKING 2.0 CODE!)\n")

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
