#!/usr/bin/env python3
"""M.O.L.O.C.H. 3.1 - Voice I/O"""

import subprocess
import tempfile
from pathlib import Path


class VoiceIO:
    """Voice Input/Output Handler"""

    def __init__(self, voice_settings=None):
        self.voice_settings = voice_settings
        self.audio_file = Path(tempfile.gettempdir()) / "moloch_audio.mp3"

    def listen(self, duration=20, smart=False):
        """Record audio and transcribe using Google Speech API"""
        try:
            print(f"🎤 Sprich jetzt...")
            print(f"DEBUG: Starte termux-speech-to-text...")

            # DIRECT Speech-to-Text (wie 2.0!)
            # Kein File-Recording, direkt Google Speech API
            # -l de-DE = DEUTSCH (nicht Englisch!)
            result = subprocess.run(
                ["termux-speech-to-text", "-l", "de-DE"],
                capture_output=True,
                text=True,
                timeout=30
            )

            print(f"DEBUG: Return code: {result.returncode}")
            print(f"DEBUG: STDOUT: '{result.stdout}'")
            print(f"DEBUG: STDERR: '{result.stderr}'")

            if result.returncode == 0 and result.stdout.strip():
                text = result.stdout.strip()
                print(f"👂 Verstanden: {text}")
                return text

            print(f"❌ Nichts verstanden (returncode: {result.returncode})")
            return None

        except subprocess.TimeoutExpired as e:
            print(f"❌ Timeout nach 30 Sekunden!")
            return None
        except Exception as e:
            print(f"❌ Voice Error: {e}")
            return None

    def speak(self, text, profile=None, fast_mode=True):
        """Speak text using termux-tts"""
        try:
            # Apply voice settings if available
            pitch = 1.0
            rate = 1.0

            if self.voice_settings and not fast_mode:
                if profile and "custom_profiles" in self.voice_settings.settings:
                    profiles = self.voice_settings.settings["custom_profiles"]
                    if profile in profiles:
                        pitch = profiles[profile].get("pitch", 1.0)
                        rate = profiles[profile].get("rate", 1.0)
                else:
                    # Use default settings
                    pitch = self.voice_settings.settings.get("pitch", 1.0)
                    rate = self.voice_settings.settings.get("rate", 1.0)

            # Speak with termux-tts (DEUTSCH!)
            subprocess.run(
                ["termux-tts-speak", "-l", "de-DE", "-p", str(pitch), "-r", str(rate), text],
                timeout=60
            )

        except Exception as e:
            print(f"❌ TTS Error: {e}")
