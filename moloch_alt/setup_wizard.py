#!/usr/bin/env python3
"""
🧠 M.O.L.O.C.H. v3.0 SETUP WIZARD
Interaktive Konfiguration für Erstinstallation
"""

import json
import os
from pathlib import Path
from datetime import datetime

class SetupWizard:
    def __init__(self):
        self.home = Path.home()
        self.moloch_dir = self.home / ".moloch"
        self.config_dir = self.moloch_dir / "config"
        self.brain_dir = self.moloch_dir / "brain"
        self.config_file = self.config_dir / "moloch.json"
        
    def print_header(self):
        """Zeige Welcome-Banner."""
        print("\n" + "="*70)
        print("🤖 M.O.L.O.C.H. v3.0 - INITIAL SETUP WIZARD".center(70))
        print("="*70)
        print("\nWelcome! Diese Wizard konfiguriert M.O.L.O.C.H. für dich.\n")
    
    def create_directories(self):
        """Erstelle notwendige Verzeichnisse."""
        print("📁 Erstelle Verzeichnisse...")
        
        dirs = [
            self.config_dir,
            self.brain_dir / "kontext",
            self.brain_dir / "logs",
            self.brain_dir / "wann",
            self.brain_dir / "was" / "musik",
            self.brain_dir / "was" / "projekte",
            self.brain_dir / "was" / "hardware",
            self.brain_dir / "wer" / "freunde",
            self.brain_dir / "wer" / "crew",
            self.brain_dir / "wer" / "arbeit",
            self.brain_dir / "wie" / "regeln",
            self.brain_dir / "wie" / "sprache",
            self.brain_dir / "wo" / "home",
            self.brain_dir / "wo" / "arbeit",
            self.brain_dir / "wo" / "events",
        ]
        
        for d in dirs:
            d.mkdir(parents=True, exist_ok=True)
        
        print("   ✅ Verzeichnisse erstellt\n")
    
    def ask_name(self) -> str:
        """Frage nach dem Namen."""
        print("👤 Wer bist du?")
        print("   (Das ist der Name von dem M.O.L.O.C.H. angesprochen wird)")
        name = input("   > ").strip()
        if not name:
            name = "Markus"
        print(f"   ✅ Okay, du bist {name}!\n")
        return name
    
    def ask_personality(self) -> str:
        """Frage nach Persönlichkeit."""
        print("🎭 Persönlichkeits-Modus:")
        print("   1. Normal (Standard)")
        print("   2. Max Headroom (80s chaotisch, stotternd)")
        print("   3. HAL 9000 (langsam, bedächtig, bedrohlich)")
        
        choice = input("   Deine Wahl (1-3)? ").strip()
        
        modes = {
            "1": "normal",
            "2": "max_headroom",
            "3": "hal9000"
        }
        
        mode = modes.get(choice, "normal")
        print(f"   ✅ Modus: {mode}\n")
        return mode
    
    def ask_location(self) -> tuple:
        """Frage nach Standort."""
        print("🗺️ Standort-Konfiguration:")
        print("   Ungefährer Standort für Wetter, etc.")
        
        print("\n   Beliebte Standorte:")
        print("   • Berlin: 52.5200, 13.4050")
        print("   • München: 48.1351, 11.5820")
        print("   • Köln: 50.9365, 6.9582")
        print("   • Hamburg: 53.5511, 9.9937")
        
        lat = input("   Latitude (52.5): ").strip() or "52.5"
        lon = input("   Longitude (13.4): ").strip() or "13.4"
        
        try:
            lat = float(lat)
            lon = float(lon)
            print(f"   ✅ Standort: {lat}, {lon}\n")
            return lat, lon
        except:
            print("   ⚠️ Ungültig, verwende Berlin\n")
            return 52.5200, 13.4050
    
    def ask_tts(self) -> dict:
        """Frage nach TTS-Einstellungen."""
        print("🔊 Text-to-Speech Einstellungen:")
        print("   Engine: edge-tts (Microsoft)")
        print("   Sprache: en-US-JennyNeural")
        
        speed = input("   Sprechgeschwindigkeit (1.0)? ").strip() or "1.0"
        
        try:
            speed = float(speed)
        except:
            speed = 1.0
        
        print(f"   ✅ TTS Speed: {speed}x\n")
        return {
            "engine": "edge-tts",
            "voice": "en-US-JennyNeural",
            "speed": speed,
            "language": "en-US"
        }
    
    def ask_features(self) -> dict:
        """Frage nach aktivierten Features."""
        print("⚙️ Features aktivieren:")
        
        features = {
            "voice_input": "ja",  # Immer an
            "face_recognition": input("   Face Recognition? (j/n, default: j): ").strip().lower() in ["j", "ja", "yes", ""],
            "ocr_enabled": input("   OCR (Kamera)? (j/n, default: j): ").strip().lower() in ["j", "ja", "yes", ""],
            "spotify_enabled": input("   Spotify Integration? (j/n, default: j): ").strip().lower() in ["j", "ja", "yes", ""],
            "clipboard_monitor": input("   Clipboard Monitor? (j/n, default: j): ").strip().lower() in ["j", "ja", "yes", ""],
            "location_aware": input("   Location Awareness? (j/n, default: j): ").strip().lower() in ["j", "ja", "yes", ""],
            "weather_aware": input("   Weather Module? (j/n, default: j): ").strip().lower() in ["j", "ja", "yes", ""],
            "music_recognition": input("   Music Recognition? (j/n, default: n): ").strip().lower() in ["j", "ja", "yes"],
        }
        
        print(f"   ✅ {sum(features.values())} Features aktiviert\n")
        return features
    
    def create_config(self, name: str, personality: str, location: tuple, 
                      tts: dict, features: dict) -> dict:
        """Erstelle Konfigurationsdatei."""
        config = {
            "personality": personality,
            "user_name": name,
            "voice": tts,
            "location": {
                "mode": "auto",
                "latitude": location[0],
                "longitude": location[1],
                "geofence_radius": 500
            },
            "phone": {
                "is_termux": os.path.exists("/data/data/com.termux"),
                "battery_aware": True,
                "low_power_threshold": 20
            },
            "features": features,
            "logging": {
                "level": "INFO",
                "file": str(self.moloch_dir / "logs" / "moloch.log")
            },
            "created": datetime.now().isoformat(),
            "version": "3.0"
        }
        
        # Speichere Config
        self.config_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Konfiguration gespeichert: {self.config_file}\n")
        return config
    
    def create_personality_file(self, name: str):
        """Erstelle Personality-Datei."""
        personality = {
            "name": "M.O.L.O.C.H.",
            "version": "3.0",
            "user": name,
            "traits": {
                "humor": "dark",
                "language": "german",
                "attitude": "helpful_but_sarcastic",
                "emotion_range": "wide"
            },
            "knowledge_areas": [
                "music",
                "technology",
                "projects",
                "work",
                "personal"
            ],
            "response_style": {
                "short": "Keep it brief and punchy",
                "medium": "Mix info and personality",
                "long": "Full explanation with context"
            }
        }
        
        personality_file = self.config_dir / "personality.json"
        with open(personality_file, 'w', encoding='utf-8') as f:
            json.dump(personality, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Personality-Datei erstellt\n")
    
    def create_mood_file(self):
        """Erstelle Mood-Datei."""
        moods = {
            "current": "neutral",
            "moods": {
                "happy": {"emoji": "😊", "response_style": "humorous"},
                "stressed": {"emoji": "😤", "response_style": "direct"},
                "curious": {"emoji": "🤔", "response_style": "detailed"},
                "tired": {"emoji": "😴", "response_style": "brief"},
                "confused": {"emoji": "🤨", "response_style": "ask_clarification"},
                "neutral": {"emoji": "😐", "response_style": "balanced"}
            }
        }
        
        mood_file = self.config_dir / "mood.json"
        with open(mood_file, 'w', encoding='utf-8') as f:
            json.dump(moods, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Mood-Datei erstellt\n")
    
    def create_memory_files(self, name: str):
        """Erstelle initiale Memory-Dateien."""
        
        # Personen
        personen = {
            "primary_user": {
                "name": name,
                "relationship": "owner",
                "known_since": datetime.now().isoformat()
            }
        }
        
        # Orte
        orte = {
            "home": {
                "name": "Home",
                "type": "personal",
                "personality_adjust": "relaxed"
            },
            "work": {
                "name": "Work",
                "type": "professional",
                "personality_adjust": "focused"
            }
        }
        
        # Speichere
        with open(self.brain_dir / "wer" / "freunde.json", 'w', encoding='utf-8') as f:
            json.dump(personen, f, indent=2, ensure_ascii=False)
        
        with open(self.brain_dir / "wo" / "home.json", 'w', encoding='utf-8') as f:
            json.dump(orte, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Memory-Dateien initialisiert\n")
    
    def show_summary(self, config: dict):
        """Zeige Setup-Summary."""
        print("="*70)
        print("✅ SETUP ABGESCHLOSSEN!".center(70))
        print("="*70)
        
        print("\n📋 Konfiguration:")
        print(f"   Benutzer: {config['user_name']}")
        print(f"   Persönlichkeit: {config['personality']}")
        print(f"   Standort: {config['location']['latitude']}, {config['location']['longitude']}")
        print(f"   TTS: {config['voice']['engine']}")
        
        print(f"\n📁 Verzeichnis: {self.moloch_dir}")
        print(f"\n🚀 Nächste Schritte:")
        print(f"   Desktop: python {Path.cwd() / 'moloch.py'}")
        print(f"   Smartphone: bash {Path.cwd() / 'setup-termux.sh'}")
        
        print("\n📖 Dokumentation:")
        print(f"   • README.md")
        print(f"   • INSTALLATION.md")
        print(f"   • TERMUX_README.md")
        
        print("\n" + "="*70 + "\n")
    
    def run(self):
        """Führe Setup-Wizard aus."""
        self.print_header()
        
        # 1. Verzeichnisse
        self.create_directories()
        
        # 2. Fragen
        name = self.ask_name()
        personality = self.ask_personality()
        location = self.ask_location()
        tts = self.ask_tts()
        features = self.ask_features()
        
        # 3. Erstelle Dateien
        config = self.create_config(name, personality, location, tts, features)
        self.create_personality_file(name)
        self.create_mood_file()
        self.create_memory_files(name)
        
        # 4. Summary
        self.show_summary(config)
        
        return True

if __name__ == "__main__":
    wizard = SetupWizard()
    try:
        wizard.run()
        print("✅ Setup erfolgreich abgeschlossen!")
    except KeyboardInterrupt:
        print("\n\n⚠️ Setup abgebrochen!")
    except Exception as e:
        print(f"\n❌ Fehler: {e}")
