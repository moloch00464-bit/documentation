#!/usr/bin/env python3
"""M.O.L.O.C.H. 3.1 - Vision I/O"""

import subprocess
from pathlib import Path
from core.config import IMAGE_FILE, DATA_DIR


class VisionIO:
    """Vision Input Handler"""

    def __init__(self):
        self.image_file = IMAGE_FILE
        # Ensure data directory exists
        DATA_DIR.mkdir(parents=True, exist_ok=True)

    def take_photo(self):
        """Take photo using termux-camera-photo"""
        try:
            print(f"📸 Taking photo...")

            result = subprocess.run(
                ["termux-camera-photo", str(self.image_file)],
                capture_output=True,
                text=True,
                timeout=10
            )

            if result.returncode == 0 and self.image_file.exists():
                print(f"✅ Photo saved: {self.image_file}")
                return True

            print(f"❌ Photo failed: {result.stderr}")
            return False

        except Exception as e:
            print(f"❌ Camera Error: {e}")
            return False
