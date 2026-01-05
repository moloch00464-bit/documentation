#!/usr/bin/env python3
"""
M.O.L.O.C.H. 3.0 - Vision I/O
==============================
Camera + Image Encoding
"""

import subprocess
import base64
import os
from pathlib import Path
from typing import Optional

from core.config import IMAGE_FILE


class VisionIO:
    """
    Vision Input for M.O.L.O.C.H. 3.0

    Features:
    - Photo capture via termux-camera-photo
    - Base64 encoding for Claude Vision API
    - Robust error handling
    """

    def __init__(self):
        """Initialize Vision I/O"""
        pass

    # ═══════════════════════════════════════════════════════════════════════════
    # CAMERA
    # ═══════════════════════════════════════════════════════════════════════════

    def take_photo(self, output_path: str = None) -> bool:
        """
        Take photo via camera

        Args:
            output_path: Path to save photo (defaults to config)

        Returns:
            Success status
        """
        output_path = output_path or str(IMAGE_FILE)

        # Remove old photo
        if os.path.exists(output_path):
            try:
                os.remove(output_path)
            except:
                pass

        print("📸 Taking photo...")

        try:
            result = subprocess.run(
                ["termux-camera-photo", output_path],
                capture_output=True,
                timeout=10,
                text=True
            )

            # Check if file was created
            if not os.path.exists(output_path):
                print("⚠️ No photo file created")
                return False

            # Check file size
            file_size = os.path.getsize(output_path)
            if file_size < 1000:  # Less than 1KB is probably broken
                print("⚠️ Photo file too small (might be corrupted)")
                return False

            print(f"✅ Photo taken ({file_size / 1024:.1f} KB)")
            return True

        except FileNotFoundError:
            print("❌ termux-camera-photo not found!")
            print("   Install: pkg install termux-api")
            return False

        except subprocess.TimeoutExpired:
            print("⚠️ Camera timeout")
            return False

        except Exception as e:
            print(f"❌ Camera error: {e}")
            return False

    # ═══════════════════════════════════════════════════════════════════════════
    # IMAGE ENCODING
    # ═══════════════════════════════════════════════════════════════════════════

    def encode_image(self, image_path: str = None) -> Optional[str]:
        """
        Encode image to base64 for Claude API

        Args:
            image_path: Path to image file (defaults to config)

        Returns:
            Base64 encoded string or None
        """
        image_path = image_path or str(IMAGE_FILE)

        if not os.path.exists(image_path):
            print(f"❌ Image file not found: {image_path}")
            return None

        try:
            with open(image_path, "rb") as f:
                image_bytes = f.read()
                image_b64 = base64.standard_b64encode(image_bytes).decode("utf-8")

            return image_b64

        except Exception as e:
            print(f"❌ Image encoding error: {e}")
            return None

    # ═══════════════════════════════════════════════════════════════════════════
    # COMBINED: TAKE & ENCODE
    # ═══════════════════════════════════════════════════════════════════════════

    def capture_and_encode(self) -> Optional[str]:
        """
        Take photo and encode to base64 in one step

        Returns:
            Base64 encoded image or None
        """
        if self.take_photo():
            return self.encode_image()
        return None


# ═══════════════════════════════════════════════════════════════════════════════
# TESTING
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("\n📸 M.O.L.O.C.H. 3.0 Vision I/O Test\n")

    vision = VisionIO()

    # Note: Camera test requires actual camera access
    # Can't be tested without hardware
    print("💡 Camera test requires actual hardware - skipped in automated test")
    print("   To test manually:")
    print("   >>> from moloch_io.vision import VisionIO")
    print("   >>> vision = VisionIO()")
    print("   >>> vision.take_photo()")

    # Test encoding (if photo exists)
    if os.path.exists(IMAGE_FILE):
        print("\n📝 Testing image encoding...")
        b64 = vision.encode_image()
        if b64:
            print(f"   ✅ Encoded {len(b64)} characters")
        else:
            print("   ❌ Encoding failed")

    print()
