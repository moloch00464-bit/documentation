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
        """Record audio and transcribe using Google Speech API"""
        import tempfile

        try:
            # CRITICAL: Android Audio-System muss komplett frei sein!
            # TTS muss GESTOPPT sein, sonst blockiert Android das Mikrofon!
            print(f"\n🎤 Mikrofon startet JETZT...")
            print(f"   (Sprich wenn du das Google Voice Dialog siehst!)")

            # NEUER ANSATZ: Schreibe Output in Datei statt capture_output
            # capture_output scheint bei termux-speech-to-text Probleme zu machen!
            temp_file = Path(tempfile.gettempdir()) / "moloch_voice_input.txt"

            # Run termux-speech-to-text und schreibe Output in File
            # VERSUCH: Setze Locale auf Deutsch - vielleicht respektiert Google das!
            env = os.environ.copy()
            env['LANG'] = 'de_DE.UTF-8'
            env['LC_ALL'] = 'de_DE.UTF-8'
            env['LANGUAGE'] = 'de_DE:de'

            with open(temp_file, 'w') as f:
                result = subprocess.run(
                    ["termux-speech-to-text"],
                    stdout=f,
                    stderr=subprocess.PIPE,
                    text=True,
                    timeout=30,
                    env=env
                )

            # Lese die Datei
            text = ""
            if temp_file.exists():
                text = temp_file.read_text().strip()
                temp_file.unlink()  # Cleanup

            # DIAGNOSTICS
            print(f"\n📊 SPEECH-TO-TEXT DIAGNOSTICS:")
            print(f"   Return code: {result.returncode}")
            print(f"   Output: '{text}'")
            if result.stderr:
                print(f"   STDERR: '{result.stderr.strip()}'")

            # Check Ergebnis
            if result.returncode == 0 and text:
                print(f"\n✅ Verstanden: {text}")
                return text

            # FEHLER-DIAGNOSE
            if result.returncode != 0:
                print(f"\n❌ FEHLER - Return Code {result.returncode}")
                if result.stderr:
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
                        print(f"   → Fehler: {result.stderr}")
                return None

            if not text:
                print(f"\n❌ Nichts verstanden (Google Dialog hat nichts zurückgegeben)")
                print(f"   Mögliche Ursachen:")
                print(f"   1. Dialog abgebrochen (zurück gedrückt)")
                print(f"   2. Zu leise gesprochen")
                print(f"   3. Mikrofon blockiert")
                print(f"   4. Google App nicht konfiguriert")
                return None

        except subprocess.TimeoutExpired:
            print(f"\n❌ Timeout nach 30 Sekunden!")
            print(f"   → Google Voice Dialog wurde nicht geschlossen?")
            if temp_file.exists():
                temp_file.unlink()
            return None
        except FileNotFoundError:
            print(f"\n❌ termux-speech-to-text nicht gefunden!")
            print(f"   → Installiere: pkg install termux-api")
            print(f"   → Dann: Termux:API App aus Play Store installieren")
            return None
        except Exception as e:
            print(f"\n❌ Unerwarteter Fehler: {e}")
            print(f"   → Bitte Screenshot machen und Fehler melden!")
            if temp_file.exists():
                temp_file.unlink()
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
