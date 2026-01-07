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
            # CRITICAL: Android Audio-System muss komplett frei sein!
            # TTS muss GESTOPPT sein, sonst blockiert Android das Mikrofon!
            print(f"\n🎤 Mikrofon startet JETZT...")
            print(f"   (Sprich wenn du das Google Voice Dialog siehst!)")

            # DIRECT Speech-to-Text (wie 2.0!)
            # Kein File-Recording, direkt Google Speech API
            # -l de-DE = DEUTSCH (nicht Englisch!)
            result = subprocess.run(
                ["termux-speech-to-text", "-l", "de-DE"],
                capture_output=True,
                text=True,
                timeout=30
            )

            # DIAGNOSTICS - Was ist passiert?
            print(f"\n📊 SPEECH-TO-TEXT DIAGNOSTICS:")
            print(f"   Return code: {result.returncode}")
            print(f"   STDOUT: '{result.stdout.strip()}'")
            print(f"   STDERR: '{result.stderr.strip()}'")

            # Check verschiedene Fehler-Fälle
            if result.returncode == 0 and result.stdout.strip():
                text = result.stdout.strip()
                print(f"\n✅ Verstanden: {text}")
                return text

            # FEHLER-DIAGNOSE
            if result.returncode != 0:
                print(f"\n❌ FEHLER - Return Code {result.returncode}")

                if "not found" in result.stderr or "No such" in result.stderr:
                    print("   → termux-speech-to-text nicht installiert!")
                    print("   → Installiere: pkg install termux-api")
                elif "permission" in result.stderr.lower():
                    print("   → Android Permissions fehlen!")
                    print("   → Gehe zu: Einstellungen → Apps → Termux → Permissions")
                elif "network" in result.stderr.lower() or "connection" in result.stderr.lower():
                    print("   → Keine Internet-Verbindung!")
                    print("   → Google Speech API braucht Internet!")
                else:
                    print(f"   → Unbekannter Fehler: {result.stderr}")

                return None

            if not result.stdout.strip():
                print(f"\n❌ Nichts verstanden")
                print(f"   Mögliche Ursachen:")
                print(f"   1. Zu leise gesprochen")
                print(f"   2. Mikrofon blockiert (TTS noch aktiv?)")
                print(f"   3. Google App nicht konfiguriert")
                print(f"   4. Keine Internet-Verbindung")
                return None

        except subprocess.TimeoutExpired:
            print(f"\n❌ Timeout nach 30 Sekunden!")
            print(f"   → Google Voice Dialog wurde nicht geschlossen?")
            return None
        except FileNotFoundError:
            print(f"\n❌ termux-speech-to-text nicht gefunden!")
            print(f"   → Installiere: pkg install termux-api")
            print(f"   → Dann: Termux:API App aus Play Store installieren")
            return None
        except Exception as e:
            print(f"\n❌ Unerwarteter Fehler: {e}")
            print(f"   → Bitte Screenshot machen und Fehler melden!")
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
