#!/usr/bin/env python3
"""
Hotword Detection für M.O.L.O.C.H.
"Hey Moloch" Voice Trigger - Always Listening

Requires: pvporcupine (free tier: 30s/min limit)
  pip install pvporcupine

Alternative (better): Snowboy
  pip install snowboy

Usage:
  python hotword_listener.py                 # Start listening
  python hotword_listener.py --train         # Trainiere Custom Hotword
  python hotword_listener.py --test          # Test mit Mikrofon
  python hotword_listener.py --daemon        # Background daemon
"""

import os
import sys
import json
import subprocess
import time
import threading
import queue

HOTWORD_CONFIG = os.path.expanduser("~/moloch/hotword_config.json")

# Try different approaches
try:
    import pvporcupine
    PORCUPINE_AVAILABLE = True
except ImportError:
    PORCUPINE_AVAILABLE = False

class HotwordListener:
    def __init__(self):
        self.config = self.load_config()
        self.is_listening = False
        self.detection_queue = queue.Queue()
    
    def load_config(self):
        """Lade Hotword Config."""
        if os.path.exists(HOTWORD_CONFIG):
            try:
                with open(HOTWORD_CONFIG, 'r') as f:
                    return json.load(f)
            except:
                pass
        
        return {
            "method": "porcupine",  # oder "snowboy", "custom"
            "sensitivity": 0.5,
            "language": "en",
            "access_key": "",  # Porcupine API Key from pvporcupine.picovoice.ai
            "custom_model": None
        }
    
    def save_config(self):
        """Speichere Hotword Config."""
        os.makedirs(os.path.dirname(HOTWORD_CONFIG), exist_ok=True)
        with open(HOTWORD_CONFIG, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def listen_porcupine(self):
        """Listen mit Porcupine (kostenlos, 30s/min)."""
        if not PORCUPINE_AVAILABLE:
            print("❌ pvporcupine nicht installiert")
            print("   pip install pvporcupine")
            return False
        
        if not self.config.get("access_key"):
            print("⚠️ Keine Porcupine Access Key")
            print("   1. Gehe zu https://picovoice.ai/console/auth/signup")
            print("   2. Copy Access Key")
            print("   3. Setze in hotword_config.json")
            return False
        
        print("🎤 Porcupine Hotword Listener gestartet...")
        print("   Sag: 'Hey Google' oder andere vordefinierte Keywords")
        
        try:
            porcupine = pvporcupine.create(
                access_key=self.config["access_key"],
                keywords=["google"]  # Vordefinierte Keywords
            )
            
            pa = None
            try:
                import pyaudio
                pa = pyaudio.PyAudio()
                stream = pa.open(
                    rate=porcupine.sample_rate,
                    channels=1,
                    format=pyaudio.paInt16,
                    input=True,
                    frames_per_buffer=porcupine.frame_length
                )
                
                self.is_listening = True
                
                print("🟢 Höre...")
                
                while self.is_listening:
                    pcm = stream.read(porcupine.frame_length)
                    pcm = np.frombuffer(pcm, dtype=np.int16)
                    
                    keyword_index = porcupine.process(pcm)
                    
                    if keyword_index >= 0:
                        print(f"🎯 Hotword erkannt! (Keyword {keyword_index})")
                        self.detection_queue.put("hotword_detected")
                
                stream.close()
            
            finally:
                if pa:
                    pa.terminate()
                porcupine.delete()
        
        except Exception as e:
            print(f"❌ Porcupine Error: {e}")
            return False
        
        return True
    
    def listen_snowboy(self):
        """Listen mit Snowboy (besser, aber komplizierter)."""
        print("❌ Snowboy nicht implementiert")
        print("   Installiere: pip install snowboy")
        print("   Dann trainiere Custom Model auf snowboy.kitt.ai")
        return False
    
    def listen_simple_rms(self):
        """Simpel Listen basierend auf Audio-Level (nur für Testing)."""
        print("🎤 Simple RMS-basierter Listener (Fallback)...")
        print("   Sprich laut 'HEY MOLOCH'")
        
        try:
            subprocess.run(
                ["termux-microphone-record", "-f", "hotword_temp.wav"],
                timeout=10,
                check=False
            )
            
            # Einfache FFT-Analyse oder Whisper für Erkennung
            print("⚠️ Verwende Whisper für Spracherkennung...")
            
            import subprocess
            result = subprocess.run(
                ["whisper", "hotword_temp.wav", "--language", "en", "--output_format", "txt"],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                text = result.stdout.lower()
                if "hey moloch" in text or "hey" in text and "moloch" in text:
                    print("🎯 Hotword erkannt!")
                    self.detection_queue.put("hotword_detected")
                    return True
            
            print("❌ Hotword nicht erkannt")
            return False
        
        except Exception as e:
            print(f"❌ Error: {e}")
            return False
    
    def listen_with_fallback(self):
        """Listen mit Fallback-Methoden."""
        method = self.config.get("method", "porcupine")
        
        if method == "porcupine":
            if not self.listen_porcupine():
                print("⚠️ Fallback zu Whisper-Methode...")
                return self.listen_simple_rms()
            return True
        
        elif method == "snowboy":
            if not self.listen_snowboy():
                print("⚠️ Fallback zu Porcupine...")
                self.config["method"] = "porcupine"
                return self.listen_with_fallback()
            return True
        
        else:
            return self.listen_simple_rms()
    
    def detect_and_respond(self):
        """Erkenne Hotword und starte Spracherkennung."""
        print("🎯 Hotword erkannt! Starte Sprachverarbeitung...")
        
        try:
            # Importiere moloch main module
            sys.path.insert(0, os.path.expanduser("~/moloch"))
            from moloch import voice_input_flow, speak
            
            # Starte Voice Input
            voice_input_flow()
        
        except Exception as e:
            print(f"❌ Voice Processing Error: {e}")
            print("⚠️ Versuche Fallback...")
            
            try:
                subprocess.run(
                    ["python", "voice_input.py"],
                    timeout=60,
                    check=False
                )
            except:
                print("❌ Voice Input fehlgeschlagen")
    
    def daemon_mode(self, auto_restart: bool = True):
        """Laufe als Background Daemon."""
        print("🎤 Hotword Daemon gestartet")
        print("   Auto-Restart bei Fehler:", "✅" if auto_restart else "❌")
        
        consecutive_errors = 0
        max_errors = 5
        
        try:
            while True:
                try:
                    # Starte Listening
                    self.listen_with_fallback()
                    consecutive_errors = 0
                    
                    # Check für detektierte Hotwords
                    while not self.detection_queue.empty():
                        event = self.detection_queue.get()
                        if event == "hotword_detected":
                            self.detect_and_respond()
                
                except KeyboardInterrupt:
                    print("\n⛔ Daemon beendet vom Benutzer")
                    break
                
                except Exception as e:
                    consecutive_errors += 1
                    print(f"⚠️ Error {consecutive_errors}/{max_errors}: {e}")
                    
                    if consecutive_errors >= max_errors:
                        print("❌ Zu viele Fehler - beende Daemon")
                        break
                    
                    time.sleep(5)  # Warte vor Restart
        
        except KeyboardInterrupt:
            print("\n⛔ Hotword Daemon gestoppt")
    
    def test_hotword(self):
        """Test Hotword Detection."""
        print("🧪 Teste Hotword Detection")
        print("   Sprich: 'Hey Moloch' in 5 Sekunden...\n")
        
        time.sleep(2)
        
        if self.listen_with_fallback():
            print("✅ Hotword erfolgreich erkannt!")
            self.detect_and_respond()
        else:
            print("❌ Hotword nicht erkannt")
    
    def setup_porcupine(self):
        """Setup Porcupine API Key."""
        print("🔑 Porcupine API Key Setup")
        print("   1. Gehe zu: https://picovoice.ai/console/auth/signup")
        print("   2. Melde dich an/registriere")
        print("   3. Copy deinen Access Key\n")
        
        key = input("Paste deinen Access Key: ").strip()
        
        if key:
            self.config["access_key"] = key
            self.save_config()
            print("✅ Access Key gespeichert")
        else:
            print("❌ Kein Key eingegeben")

if __name__ == "__main__":
    listener = HotwordListener()
    
    if len(sys.argv) < 2:
        listener.daemon_mode()
    
    elif sys.argv[1] == "--test":
        listener.test_hotword()
    
    elif sys.argv[1] == "--daemon":
        auto_restart = "--no-restart" not in sys.argv
        listener.daemon_mode(auto_restart)
    
    elif sys.argv[1] == "--setup":
        listener.setup_porcupine()
    
    else:
        print(__doc__)
