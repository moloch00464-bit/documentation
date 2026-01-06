#!/usr/bin/env python3
"""
M.O.L.O.C.H. 3.0 - Voice Settings & Emotion Synthesis
======================================================
Voice customization, emotion-based modulation, voice selection

M.O.L.O.C.H. Request: F:emotion_synthesis|P:7|S:contextual_mood_generation|R:authentic_personality
"""

import json
from pathlib import Path
from typing import Dict, Optional
from datetime import datetime


class VoiceSettings:
    """
    Voice Settings & Emotion Synthesis for M.O.L.O.C.H.

    Features:
    - Voice parameter storage (pitch, rate, volume)
    - Emotion-based voice modulation
    - Voice profile selection
    - Per-emotion voice settings
    """

    def __init__(self, data_dir: Path):
        """Initialize Voice Settings"""
        self.data_dir = data_dir
        self.settings_file = data_dir / "voice_settings.json"

        # Load or create settings
        self.settings = self._load_settings()

    def _load_settings(self) -> Dict:
        """Load voice settings from file"""
        if self.settings_file.exists():
            try:
                with open(self.settings_file, 'r') as f:
                    return json.load(f)
            except:
                pass

        # Default settings
        return {
            "base_voice": {
                "pitch": 1.0,      # 0.5 - 2.0 (1.0 = normal)
                "rate": 1.0,       # 0.5 - 2.0 (1.0 = normal)
                "volume": 1.0,     # 0.0 - 1.0
                "language": "de-DE"
            },
            "emotion_modulation": {
                "enabled": True,
                "intensity": 1.0   # 0.0 - 1.0 (how much emotions affect voice)
            },
            "emotion_profiles": {
                "gestresst": {
                    "pitch": 0.9,   # Tiefer bei Stress
                    "rate": 1.2,    # Schneller bei Stress
                    "volume": 0.9
                },
                "gut_drauf": {
                    "pitch": 1.1,   # Höher wenn gut drauf
                    "rate": 1.1,    # Etwas schneller
                    "volume": 1.0
                },
                "fragend": {
                    "pitch": 1.05,  # Leicht höher bei Fragen
                    "rate": 0.95,   # Etwas langsamer
                    "volume": 1.0
                },
                "neutral": {
                    "pitch": 1.0,
                    "rate": 1.0,
                    "volume": 1.0
                },
                "dark_side": {
                    "pitch": 0.85,  # Extra tief im Dark Side Mode! 🖤😈
                    "rate": 0.95,   # Etwas langsamer, bedrohlicher
                    "volume": 1.0
                }
            },
            "tageszeit_profiles": {
                "kaffee": {
                    "pitch": 0.95,  # Morgens noch etwas tiefer
                    "rate": 0.9     # Langsamer (noch nicht wach)
                },
                "normal": {
                    "pitch": 1.0,
                    "rate": 1.0
                },
                "feierabend": {
                    "pitch": 1.0,
                    "rate": 1.05    # Etwas lebhafter
                },
                "dark_side": {
                    "pitch": 0.85,  # Nachts extra tief! 🖤
                    "rate": 0.95
                }
            },
            "selected_profile": "base",  # User's chosen voice profile
            "last_modified": datetime.now().isoformat()
        }

    def save_settings(self):
        """Save current settings to file"""
        self.settings["last_modified"] = datetime.now().isoformat()
        with open(self.settings_file, 'w') as f:
            json.dump(self.settings, indent=2, ensure_ascii=False, fp=f)

    # ═══════════════════════════════════════════════════════════════════════════
    # VOICE PARAMETER CALCULATION
    # ═══════════════════════════════════════════════════════════════════════════

    def get_voice_params(
        self,
        stimmung: Optional[str] = None,
        tageszeit: Optional[str] = None,
        profile: Optional[str] = None
    ) -> Dict[str, float]:
        """
        Calculate voice parameters based on emotion, time of day, and voice profile

        Args:
            stimmung: Current mood (gestresst, gut_drauf, fragend, neutral, dark_side)
            tageszeit: Time of day mode (kaffee, normal, feierabend, dark_side)
            profile: Custom voice profile to use (e.g., "choice_1", "choice_2", "choice_3")

        Returns:
            Dict with pitch, rate, volume parameters
        """
        # Start with base voice OR custom profile
        if profile and "custom_profiles" in self.settings and profile in self.settings["custom_profiles"]:
            # Use custom profile as base!
            custom = self.settings["custom_profiles"][profile]
            params = {
                "pitch": custom.get("pitch", 1.0),
                "rate": custom.get("rate", 1.0),
                "volume": custom.get("volume", 1.0),
                "language": self.settings["base_voice"].get("language", "de-DE")
            }
        else:
            # Use default base voice
            params = self.settings["base_voice"].copy()

        # Apply emotion modulation if enabled
        if self.settings["emotion_modulation"]["enabled"]:
            intensity = self.settings["emotion_modulation"]["intensity"]

            # Apply emotion profile (SKIP "neutral" - it should change nothing!)
            if stimmung and stimmung != "neutral" and stimmung in self.settings["emotion_profiles"]:
                emotion_profile = self.settings["emotion_profiles"][stimmung]

                # Blend base + emotion based on intensity
                for key in ["pitch", "rate", "volume"]:
                    if key in emotion_profile:
                        base_val = params.get(key, 1.0)
                        emotion_val = emotion_profile[key]
                        # Linear interpolation
                        params[key] = base_val + (emotion_val - base_val) * intensity

            # Apply tageszeit profile (lower intensity) - SKIP "normal"!
            if tageszeit and tageszeit != "normal" and tageszeit in self.settings["tageszeit_profiles"]:
                tageszeit_profile = self.settings["tageszeit_profiles"][tageszeit]

                for key in ["pitch", "rate"]:
                    if key in tageszeit_profile:
                        current_val = params.get(key, 1.0)
                        tageszeit_val = tageszeit_profile[key]
                        # Blend with lower intensity (0.5)
                        params[key] = current_val + (tageszeit_val - current_val) * 0.5

        # Clamp values to valid ranges
        params["pitch"] = max(0.5, min(2.0, params["pitch"]))
        params["rate"] = max(0.5, min(2.0, params["rate"]))
        params["volume"] = max(0.0, min(1.0, params["volume"]))

        return params

    # ═══════════════════════════════════════════════════════════════════════════
    # VOICE PROFILE MANAGEMENT
    # ═══════════════════════════════════════════════════════════════════════════

    def set_base_voice(self, pitch: float, rate: float, volume: float):
        """
        Set base voice parameters

        Args:
            pitch: Voice pitch (0.5 - 2.0, 1.0 = normal)
            rate: Speech rate (0.5 - 2.0, 1.0 = normal)
            volume: Volume (0.0 - 1.0)
        """
        self.settings["base_voice"]["pitch"] = max(0.5, min(2.0, pitch))
        self.settings["base_voice"]["rate"] = max(0.5, min(2.0, rate))
        self.settings["base_voice"]["volume"] = max(0.0, min(1.0, volume))
        self.save_settings()

    def set_emotion_intensity(self, intensity: float):
        """
        Set emotion modulation intensity

        Args:
            intensity: 0.0 (no modulation) to 1.0 (full modulation)
        """
        self.settings["emotion_modulation"]["intensity"] = max(0.0, min(1.0, intensity))
        self.save_settings()

    def enable_emotion_modulation(self, enabled: bool = True):
        """Enable or disable emotion-based voice modulation"""
        self.settings["emotion_modulation"]["enabled"] = enabled
        self.save_settings()

    # ═══════════════════════════════════════════════════════════════════════════
    # VOICE PROFILE SELECTION
    # ═══════════════════════════════════════════════════════════════════════════

    def get_available_profiles(self) -> list:
        """Get list of all available voice profiles"""
        profiles = ["base"]  # Base is always available

        # Add custom profiles if any exist
        if "custom_profiles" in self.settings:
            profiles.extend(self.settings["custom_profiles"].keys())

        return profiles

    def select_profile(self, profile_name: str):
        """
        Select a voice profile

        Args:
            profile_name: Name of the profile to select
        """
        profiles = self.get_available_profiles()

        if profile_name not in profiles:
            print(f"⚠️ Voice profile '{profile_name}' not found")
            return False

        self.settings["selected_profile"] = profile_name
        self.save_settings()
        print(f"✅ Voice profile set to: {profile_name}")
        return True

    def create_custom_profile(self, name: str, pitch: float, rate: float, volume: float):
        """
        Create a new custom voice profile

        Args:
            name: Profile name
            pitch: Voice pitch (0.5 - 2.0)
            rate: Speech rate (0.5 - 2.0)
            volume: Volume (0.0 - 1.0)
        """
        if "custom_profiles" not in self.settings:
            self.settings["custom_profiles"] = {}

        self.settings["custom_profiles"][name] = {
            "pitch": max(0.5, min(2.0, pitch)),
            "rate": max(0.5, min(2.0, rate)),
            "volume": max(0.0, min(1.0, volume)),
            "created_at": datetime.now().isoformat()
        }

        self.save_settings()
        print(f"✅ Custom voice profile '{name}' created!")

    def add_voice_profile(self, name: str, pitch: float, rate: float, description: str = None, volume: float = 1.0):
        """
        Add a voice profile (alias for create_custom_profile with description support)

        Args:
            name: Profile name
            pitch: Voice pitch (0.5 - 2.0)
            rate: Speech rate (0.5 - 2.0)
            description: Optional description of the profile
            volume: Volume (0.0 - 1.0)
        """
        if "custom_profiles" not in self.settings:
            self.settings["custom_profiles"] = {}

        self.settings["custom_profiles"][name] = {
            "pitch": max(0.5, min(2.0, pitch)),
            "rate": max(0.5, min(2.0, rate)),
            "volume": max(0.0, min(1.0, volume)),
            "description": description or f"Voice profile {name}",
            "created_at": datetime.now().isoformat()
        }

        self.save_settings()

    # ═══════════════════════════════════════════════════════════════════════════
    # INFO & DEBUGGING
    # ═══════════════════════════════════════════════════════════════════════════

    def get_current_config(self) -> str:
        """Get human-readable current config"""
        base = self.settings["base_voice"]
        intensity = self.settings["emotion_modulation"]["intensity"]
        enabled = self.settings["emotion_modulation"]["enabled"]

        config = f"""
🎤 VOICE SETTINGS:
   Base Pitch: {base['pitch']:.2f}
   Base Rate: {base['rate']:.2f}
   Base Volume: {base['volume']:.2f}

   Emotion Modulation: {'✅ Enabled' if enabled else '❌ Disabled'}
   Emotion Intensity: {intensity:.0%}

   Selected Profile: {self.settings['selected_profile']}
"""
        return config


# ═══════════════════════════════════════════════════════════════════════════════
# TESTING
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    from core.config import DATA_DIR

    print("\n🎤 Testing Voice Settings System\n")

    voice_settings = VoiceSettings(DATA_DIR)

    # Test: Get voice params for different moods
    print("📊 Testing voice parameter calculation...")

    moods = ["gestresst", "gut_drauf", "fragend", "neutral", "dark_side"]

    for mood in moods:
        params = voice_settings.get_voice_params(stimmung=mood)
        print(f"\n   {mood}:")
        print(f"      Pitch: {params['pitch']:.2f}")
        print(f"      Rate: {params['rate']:.2f}")
        print(f"      Volume: {params['volume']:.2f}")

    # Test: Tageszeit modulation
    print("\n\n📅 Testing time-of-day modulation...")

    times = ["kaffee", "normal", "feierabend", "dark_side"]

    for time_mode in times:
        params = voice_settings.get_voice_params(tageszeit=time_mode)
        print(f"\n   {time_mode}:")
        print(f"      Pitch: {params['pitch']:.2f}")
        print(f"      Rate: {params['rate']:.2f}")

    # Test: Combined emotion + tageszeit
    print("\n\n🎭 Testing combined emotion + tageszeit...")
    params = voice_settings.get_voice_params(stimmung="dark_side", tageszeit="dark_side")
    print(f"   Dark Side Mode (emotion + night):")
    print(f"      Pitch: {params['pitch']:.2f} (EXTRA TIEF! 🖤)")
    print(f"      Rate: {params['rate']:.2f}")

    # Show current config
    print("\n" + voice_settings.get_current_config())

    print("✅ Voice Settings System works!\n")
