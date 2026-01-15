#!/usr/bin/env python3
"""M.O.L.O.C.H. 3.1 - Voice I/O"""

import os
import subprocess
import tempfile
from pathlib import Path


class VoiceIO:
    """Voice Input/Output Handler"""

    def __init__(self, voice_settings=None):
        self.voice_settings = voice_settings
        self.audio_file = Path(tempfile.gettempdir()) / "moloch_audio.mp3"

    def listen(self, duration=20, smart=False):
        """Record audio and transcribe - M.O.L.O.C.H. 2.0 STYLE (FUNKTIONIERT!)"""
        try:
            print(f"🎤 Sprich jetzt...")

            # EINFACH WIE 2.0 - KEIN BULLSHIT!
            result = subprocess.run(
                ["termux-speech-to-text"],
                capture_output=True,
                text=True,
                timeout=30
            )

            if result.returncode == 0 and result.stdout.strip():
                text = result.stdout.strip()
                print(f"👂 Verstanden: {text}")
                return text

            print(f"❌ Nichts verstanden")
            return None

        except subprocess.TimeoutExpired:
            print(f"❌ Timeout!")
            return None
        except Exception as e:
            print(f"❌ Fehler: {e}")
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

            # Speak with termux-tts (nutzt System-Sprache)
            # HINWEIS: -l Option nicht in alter termux-api! Nutzt Android TTS Engine.
            subprocess.run(
                ["termux-tts-speak", "-p", str(pitch), "-r", str(rate), text],
                timeout=60
            )

        except Exception as e:
            print(f"❌ TTS Error: {e}")
