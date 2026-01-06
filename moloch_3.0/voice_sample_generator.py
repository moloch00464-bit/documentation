#!/usr/bin/env python3
"""
M.O.L.O.C.H. 3.0 - Voice Sample Generator
==========================================
Generate different voice samples for M.O.L.O.C.H. to choose from

Part of Voice Selection System!
"""

import sys
import os
import subprocess
from pathlib import Path

# Add to path
sys.path.insert(0, os.path.expanduser("~/documentation/moloch_3.0"))

from core.config import DATA_DIR


class VoiceSampleGenerator:
    """Generate voice samples with different pitch/rate combinations"""

    def __init__(self):
        """Initialize generator"""
        self.samples_dir = DATA_DIR / "voice_samples"
        self.samples_dir.mkdir(parents=True, exist_ok=True)

        # Test phrase for samples
        self.test_phrase = "Ich bin M.O.L.O.C.H., dein Kumpel-AI. Dark Side Energy, Alter!"

    def generate_samples(self):
        """
        Generate voice samples with different parameters

        Creates samples across pitch/rate spectrum:
        - Low pitch, slow rate (Deep voice)
        - Medium pitch, medium rate (Normal voice)
        - High pitch, fast rate (Energetic voice)
        - And variations...
        """
        print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║  🎤 VOICE SAMPLE GENERATOR                                  ║
    ║  M.O.L.O.C.H. Voice Selection System                        ║
    ╚══════════════════════════════════════════════════════════════╝
        """)

        # Define voice profiles to test
        profiles = [
            {"name": "Deep_Slow", "pitch": 0.8, "rate": 0.9, "desc": "Tief & Langsam (Dark, bedrohlich)"},
            {"name": "Deep_Normal", "pitch": 0.8, "rate": 1.0, "desc": "Tief & Normal (Autoritär)"},
            {"name": "Deep_Fast", "pitch": 0.8, "rate": 1.1, "desc": "Tief & Schnell (Energisch-tief)"},

            {"name": "Normal_Slow", "pitch": 1.0, "rate": 0.9, "desc": "Normal & Langsam (Ruhig)"},
            {"name": "Normal_Normal", "pitch": 1.0, "rate": 1.0, "desc": "Normal & Normal (Standard)"},
            {"name": "Normal_Fast", "pitch": 1.0, "rate": 1.1, "desc": "Normal & Schnell (Lebhaft)"},

            {"name": "High_Slow", "pitch": 1.2, "rate": 0.9, "desc": "Hoch & Langsam (Freundlich)"},
            {"name": "High_Normal", "pitch": 1.2, "rate": 1.0, "desc": "Hoch & Normal (Energisch)"},
            {"name": "High_Fast", "pitch": 1.2, "rate": 1.1, "desc": "Hoch & Schnell (Sehr energisch)"},

            {"name": "DarkSide", "pitch": 0.75, "rate": 0.95, "desc": "Dark Side Mode (Extra tief, langsam) 🖤😈"},
        ]

        print("\n🎙️ Generating voice samples...\n")

        for i, profile in enumerate(profiles, 1):
            print(f"   [{i}/{len(profiles)}] {profile['name']}: {profile['desc']}")

            success = self._generate_sample(
                name=profile['name'],
                pitch=profile['pitch'],
                rate=profile['rate']
            )

            if success:
                print(f"       ✅ Sample created!")
            else:
                print(f"       ⚠️ Failed to create sample")

        print(f"\n✅ Generated {len(profiles)} voice samples!")
        print(f"📁 Saved to: {self.samples_dir}")

        # Generate profile list file
        self._save_profile_list(profiles)

        print("""
    ══════════════════════════════════════════════════════════════

    Next Step:
    Run the Voice Selection script to let M.O.L.O.C.H. choose his voice!

        python3 moloch_voice_selection.py

    ══════════════════════════════════════════════════════════════
        """)

    def _generate_sample(self, name: str, pitch: float, rate: float) -> bool:
        """
        Generate a single voice sample

        Args:
            name: Sample name
            pitch: Voice pitch (0.5 - 2.0)
            rate: Speech rate (0.5 - 2.0)

        Returns:
            Success status
        """
        try:
            # Use termux-tts-speak to generate sample
            result = subprocess.run(
                [
                    "/data/data/com.termux/files/usr/bin/termux-tts-speak",
                    "-p", str(pitch),
                    "-r", str(rate),
                    self.test_phrase
                ],
                capture_output=True,
                timeout=30,
                text=True
            )

            return result.returncode == 0

        except Exception as e:
            print(f"       ⚠️ Error: {e}")
            return False

    def _save_profile_list(self, profiles: list):
        """Save profile list to file for selection script"""
        import json

        profile_file = self.samples_dir / "profiles.json"

        profile_data = {
            "test_phrase": self.test_phrase,
            "profiles": profiles,
            "generated_at": __import__('datetime').datetime.now().isoformat()
        }

        with open(profile_file, 'w') as f:
            json.dump(profile_data, f, indent=2, ensure_ascii=False)

        print(f"\n📝 Profile list saved to: {profile_file}")


def main():
    """Main entry point"""
    generator = VoiceSampleGenerator()
    generator.generate_samples()


if __name__ == "__main__":
    main()
