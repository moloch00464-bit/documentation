#!/usr/bin/env python3
"""M.O.L.O.C.H. 3.1 - Voice Settings"""

import json
from pathlib import Path


class VoiceSettings:
    """Voice synthesis settings and profiles"""

    def __init__(self, data_dir):
        self.data_dir = data_dir
        self.settings_file = data_dir / "voice_settings.json"
        self.settings = self._load_settings()

    def _load_settings(self):
        """Load voice settings"""
        if self.settings_file.exists():
            try:
                with open(self.settings_file, 'r') as f:
                    return json.load(f)
            except:
                pass

        # Default settings
        return {
            "pitch": 1.0,
            "rate": 1.0,
            "custom_profiles": {
                "choice_1": {
                    "pitch": 1.0,
                    "rate": 1.0,
                    "description": "Standard"
                },
                "choice_2": {
                    "pitch": 0.9,
                    "rate": 1.1,
                    "description": "Schneller, tiefer"
                },
                "choice_3": {
                    "pitch": 1.1,
                    "rate": 0.9,
                    "description": "Langsamer, höher"
                }
            }
        }

    def save_settings(self):
        """Save voice settings"""
        try:
            with open(self.settings_file, 'w') as f:
                json.dump(self.settings, f, indent=2)
            return True
        except Exception as e:
            print(f"⚠️  Failed to save voice settings: {e}")
            return False

    def update_pitch(self, pitch: float):
        """Update pitch"""
        self.settings["pitch"] = pitch
        self.save_settings()

    def update_rate(self, rate: float):
        """Update rate"""
        self.settings["rate"] = rate
        self.save_settings()
