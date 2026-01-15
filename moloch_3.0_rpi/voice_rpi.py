#!/usr/bin/env python3
"""
M.O.L.O.C.H. 3.0 - Raspberry Pi Voice I/O
==========================================
Vosk (Offline Speech Recognition) + Piper TTS
"""

import os
import json
import wave
import subprocess
from pathlib import Path
from vosk import Model, KaldiRecognizer
import sounddevice as sd
import numpy as np


class VoiceRPi:
    """Voice Input/Output for Raspberry Pi"""

    def __init__(self, vosk_model_path=None, voice_settings=None):
        """
        Initialize Vosk and Piper

        Args:
            vosk_model_path: Path to Vosk model directory
            voice_settings: Voice settings (pitch, rate, etc.)
        """
        self.voice_settings = voice_settings

        # Vosk Model Path
        if vosk_model_path is None:
            vosk_model_path = Path.home() / "vosk-model-de"

        if not Path(vosk_model_path).exists():
            raise FileNotFoundError(
                f"Vosk model not found at {vosk_model_path}\n"
                f"Download: wget https://alphacephei.com/vosk/models/vosk-model-small-de-0.15.zip\n"
                f"Extract to: {vosk_model_path}"
            )

        print(f"🧠 Loading Vosk model from {vosk_model_path}...")
        self.model = Model(str(vosk_model_path))
        self.recognizer = KaldiRecognizer(self.model, 16000)
        print("✅ Vosk model loaded!")

        # Audio settings
        self.sample_rate = 16000
        self.channels = 1

    def listen(self, duration=20, smart=False):
        """
        Record audio and transcribe using Vosk

        Args:
            duration: Maximum recording duration in seconds
            smart: If True, stop on silence (not implemented yet)

        Returns:
            str: Transcribed text or None
        """
        try:
            print(f"🎤 Sprich jetzt (max {duration} Sekunden)...")

            # Record audio
            audio_data = sd.rec(
                int(duration * self.sample_rate),
                samplerate=self.sample_rate,
                channels=self.channels,
                dtype='int16'
            )
            sd.wait()  # Wait until recording is finished

            print(f"🔄 Verarbeite Audio...")

            # Reset recognizer
            self.recognizer = KaldiRecognizer(self.model, self.sample_rate)

            # Process audio in chunks
            audio_bytes = audio_data.tobytes()
            chunk_size = 4000

            for i in range(0, len(audio_bytes), chunk_size):
                chunk = audio_bytes[i:i + chunk_size]
                if self.recognizer.AcceptWaveform(chunk):
                    pass  # Partial results

            # Get final result
            result = json.loads(self.recognizer.FinalResult())
            text = result.get('text', '').strip()

            if text:
                print(f"👂 Verstanden: {text}")
                return text
            else:
                print(f"❌ Nichts verstanden")
                return None

        except Exception as e:
            print(f"❌ Voice Input Error: {e}")
            return None

    def listen_continuous(self, callback):
        """
        Continuous listening mode - calls callback for each recognized phrase

        Args:
            callback: Function to call with recognized text

        Usage:
            def on_speech(text):
                print(f"Heard: {text}")

            voice.listen_continuous(on_speech)
        """
        print(f"🎤 Continuous listening mode - press Ctrl+C to stop...")

        try:
            with sd.RawInputStream(samplerate=self.sample_rate,
                                   blocksize=8000,
                                   dtype='int16',
                                   channels=self.channels) as stream:

                while True:
                    data = stream.read(4000)[0]

                    if self.recognizer.AcceptWaveform(bytes(data)):
                        result = json.loads(self.recognizer.Result())
                        text = result.get('text', '').strip()
                        if text:
                            print(f"👂 Verstanden: {text}")
                            callback(text)

        except KeyboardInterrupt:
            print("\n⏹️  Stopped listening")
        except Exception as e:
            print(f"❌ Error: {e}")

    def speak(self, text, profile=None, fast_mode=True):
        """
        Speak text using Piper TTS

        Args:
            text: Text to speak
            profile: Voice profile (not used yet)
            fast_mode: If True, use espeak (faster but worse quality)
        """
        try:
            if fast_mode:
                # espeak - fast but robotic
                subprocess.run(
                    ["espeak", "-v", "de", "-s", "150", text],
                    timeout=30
                )
            else:
                # Piper TTS - better quality
                # Check if piper is installed
                piper_check = subprocess.run(
                    ["which", "piper"],
                    capture_output=True
                )

                if piper_check.returncode == 0:
                    # Piper installed
                    subprocess.run(
                        ["piper", "--model", "de_DE-thorsten-medium",
                         "--output-raw"],
                        input=text.encode('utf-8'),
                        stdout=subprocess.PIPE,
                        timeout=30
                    )
                else:
                    # Fallback to espeak
                    print("⚠️  Piper not found, using espeak")
                    subprocess.run(
                        ["espeak", "-v", "de", "-s", "150", text],
                        timeout=30
                    )

        except subprocess.TimeoutExpired:
            print(f"❌ TTS Timeout")
        except Exception as e:
            print(f"❌ TTS Error: {e}")


# Test function
if __name__ == "__main__":
    print("M.O.L.O.C.H. Voice Test - Raspberry Pi")
    print("=" * 60)

    try:
        voice = VoiceRPi()

        # Test TTS
        print("\n🗣️  Testing TTS...")
        voice.speak("Hallo! Ich bin Moloch. Sprich jetzt!", fast_mode=True)

        # Test Speech Recognition
        print("\n🎤 Testing Speech Recognition...")
        text = voice.listen(duration=5)

        if text:
            print(f"\n✅ Success! You said: {text}")
            voice.speak(f"Du hast gesagt: {text}", fast_mode=True)
        else:
            print(f"\n❌ No speech detected")

    except FileNotFoundError as e:
        print(f"\n❌ Error: {e}")
        print("\nInstallation:")
        print("  1. Download Vosk model:")
        print("     wget https://alphacephei.com/vosk/models/vosk-model-small-de-0.15.zip")
        print("  2. Extract:")
        print("     unzip vosk-model-small-de-0.15.zip")
        print("     mv vosk-model-small-de-0.15 ~/vosk-model-de")
        print("  3. Install dependencies:")
        print("     pip install vosk sounddevice numpy")
    except Exception as e:
        print(f"\n❌ Error: {e}")
