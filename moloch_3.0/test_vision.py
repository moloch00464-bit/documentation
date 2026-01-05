#!/usr/bin/env python3
"""
M.O.L.O.C.H. 3.0 - Vision Test
===============================
Test Camera + Claude Vision
"""

import sys
import os
from pathlib import Path

# Add to path
sys.path.insert(0, os.path.expanduser("~/documentation/moloch_3.0"))

from moloch_io.vision import VisionIO
import requests
from core.config import ANTHROPIC_API_KEY, CLAUDE_MODEL

def test_vision():
    """Test camera and Claude Vision API"""

    print("\n" + "="*60)
    print("📸 M.O.L.O.C.H. 3.0 VISION TEST")
    print("="*60)

    # Check API key
    if not ANTHROPIC_API_KEY or len(ANTHROPIC_API_KEY) < 20:
        print("\n❌ ANTHROPIC_API_KEY nicht gesetzt!")
        return False

    # Create vision
    vision = VisionIO()

    # Take photo
    print("\n📷 Nehme Foto auf...")
    if not vision.take_photo():
        print("❌ Foto fehlgeschlagen!")
        return False

    # Encode image
    print("🔄 Kodiere Bild...")
    image_b64 = vision.encode_image()

    if not image_b64:
        print("❌ Kodierung fehlgeschlagen!")
        return False

    print(f"✅ Bild kodiert ({len(image_b64)} chars)")

    # Send to Claude Vision
    print("\n🧠 Frage Claude was er sieht...")

    url = "https://api.anthropic.com/v1/messages"

    headers = {
        "x-api-key": ANTHROPIC_API_KEY,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json"
    }

    data = {
        "model": CLAUDE_MODEL,
        "max_tokens": 1024,
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": "image/jpeg",
                            "data": image_b64
                        }
                    },
                    {
                        "type": "text",
                        "text": "Was siehst du auf diesem Bild? Beschreibe es kurz und direkt, Alter!"
                    }
                ]
            }
        ]
    }

    try:
        response = requests.post(url, headers=headers, json=data, timeout=60)

        if response.status_code != 200:
            print(f"❌ Claude Vision API Error: {response.status_code}")
            print(response.text)
            return False

        result = response.json()

        if 'content' in result and len(result['content']) > 0:
            answer = result['content'][0]['text']

            print("\n" + "="*60)
            print("👁️ M.O.L.O.C.H. SIEHT:")
            print("="*60)
            print(f"\n{answer}\n")
            print("="*60)

            return True
        else:
            print("❌ Keine Antwort von Claude Vision")
            return False

    except requests.Timeout:
        print("❌ Claude Vision API Timeout")
        return False
    except Exception as e:
        print(f"❌ Fehler: {e}")
        return False


if __name__ == "__main__":
    print("""
    ███╗   ███╗ ██████╗ ██╗      ██████╗  ██████╗██╗  ██╗
    ████╗ ████║██╔═══██╗██║     ██╔═══██╗██╔════╝██║  ██║
    ██╔████╔██║██║   ██║██║     ██║   ██║██║     ███████║
    ██║╚██╔╝██║██║   ██║██║     ██║   ██║██║     ██╔══██║
    ██║ ╚═╝ ██║╚██████╔╝███████╗╚██████╔╝╚██████╗██║  ██║
    ╚═╝     ╚═╝ ╚═════╝ ╚══════╝ ╚═════╝  ╚═════╝╚═╝  ╚═╝

    M.O.L.O.C.H. 3.0 - Vision Test
    """)

    success = test_vision()

    if success:
        print("\n✅✅✅ VISION FUNKTIONIERT! ✅✅✅\n")
    else:
        print("\n❌ Vision Test fehlgeschlagen\n")

    sys.exit(0 if success else 1)
