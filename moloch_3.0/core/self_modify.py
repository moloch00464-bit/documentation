#!/usr/bin/env python3
"""M.O.L.O.C.H. 3.1 - Self-Modification System"""

from pathlib import Path
from datetime import datetime
from typing import Optional
from core.voice_settings import VoiceSettings
from core.config import DATA_DIR, BRAIN_DIR


class SelfModificationSystem:
    """Allow M.O.L.O.C.H. to modify itself"""

    def __init__(self):
        self.data_dir = DATA_DIR
        self.brain_dir = BRAIN_DIR
        self.voice_settings = VoiceSettings(self.data_dir)

    def modify_voice_settings(self, pitch: Optional[float] = None, rate: Optional[float] = None, reason: str = ""):
        """Modify voice settings"""
        try:
            if pitch is not None:
                self.voice_settings.update_pitch(pitch)

            if rate is not None:
                self.voice_settings.update_rate(rate)

            print(f"✅ Voice modified: pitch={pitch}, rate={rate}")
            if reason:
                print(f"   Reason: {reason}")

            return True

        except Exception as e:
            print(f"❌ Voice modification failed: {e}")
            return False

    def create_brain_category(self, name: str, description: str = ""):
        """Create new brain category"""
        try:
            cat_dir = self.brain_dir / name
            cat_dir.mkdir(parents=True, exist_ok=True)

            # Create README in category
            readme = cat_dir / "README.txt"
            readme.write_text(f"Category: {name}\nDescription: {description}\nCreated: {datetime.now().isoformat()}")

            print(f"✅ Brain category created: {name}")
            return True

        except Exception as e:
            print(f"❌ Category creation failed: {e}")
            return False

    def modify_performance_mode(self, fast_mode: bool, reason: str = ""):
        """Modify performance mode"""
        # This would adjust internal performance settings
        print(f"✅ Performance mode: {'FAST' if fast_mode else 'QUALITY'}")
        if reason:
            print(f"   Reason: {reason}")

        return True
