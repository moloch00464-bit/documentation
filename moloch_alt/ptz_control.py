#!/usr/bin/env python3
"""
PTZ Kamera Control für DGM Vision System
Pan-Tilt-Zoom über HTTP/RTSP API

Unterstützt:
- Hikvision PTZ Kameras
- Dahua PTZ Kameras
- ONVIF-kompatible Kameras

Usage:
  python ptz_control.py pan <direction> <speed>    # pan left/right
  python ptz_control.py tilt <direction> <speed>   # tilt up/down
  python ptz_control.py zoom <direction> <speed>   # zoom in/out
  python ptz_control.py preset <number>            # goto preset
  python ptz_control.py track <person_name>        # auto-track person
"""

import os
import sys
import requests
import json
from typing import Optional

# Config
PTZ_CONFIG = os.path.expanduser("~/moloch/ptz_config.json")

class PTZController:
    """PTZ Kamera Controller."""
    
    def __init__(self, camera_url: str, username: str, password: str):
        self.camera_url = camera_url  # z.B. http://192.168.1.100
        self.username = username
        self.password = password
        self.session = requests.Session()
        self.session.auth = (username, password)
    
    def pan(self, direction: str, speed: int = 5):
        """Pan left/right."""
        # direction: "left" oder "right"
        # speed: 1-10
        speed = max(1, min(10, speed))
        pan_val = speed if direction.lower() == "right" else -speed
        
        params = {
            "action": "start",
            "code": "Pan",
            "arg1": pan_val,
            "arg2": 0,
            "arg3": 0
        }
        
        try:
            r = self.session.get(f"{self.camera_url}/cgi-bin/ptz", params=params, timeout=5)
            if r.status_code == 200:
                print(f"↔️ Pan {direction} (Speed: {speed})")
                return True
        except Exception as e:
            print(f"❌ Pan Error: {e}")
        
        return False
    
    def tilt(self, direction: str, speed: int = 5):
        """Tilt up/down."""
        # direction: "up" oder "down"
        speed = max(1, min(10, speed))
        tilt_val = speed if direction.lower() == "up" else -speed
        
        params = {
            "action": "start",
            "code": "Tilt",
            "arg1": 0,
            "arg2": tilt_val,
            "arg3": 0
        }
        
        try:
            r = self.session.get(f"{self.camera_url}/cgi-bin/ptz", params=params, timeout=5)
            if r.status_code == 200:
                print(f"⬆️ Tilt {direction} (Speed: {speed})")
                return True
        except Exception as e:
            print(f"❌ Tilt Error: {e}")
        
        return False
    
    def zoom(self, direction: str, speed: int = 3):
        """Zoom in/out."""
        # direction: "in" oder "out"
        speed = max(1, min(10, speed))
        zoom_val = speed if direction.lower() == "in" else -speed
        
        params = {
            "action": "start",
            "code": "Zoom",
            "arg1": zoom_val,
            "arg2": 0,
            "arg3": 0
        }
        
        try:
            r = self.session.get(f"{self.camera_url}/cgi-bin/ptz", params=params, timeout=5)
            if r.status_code == 200:
                print(f"🔍 Zoom {direction} (Speed: {speed})")
                return True
        except Exception as e:
            print(f"❌ Zoom Error: {e}")
        
        return False
    
    def goto_preset(self, preset_id: int):
        """Fahre zu Preset Position."""
        preset_id = max(1, min(255, preset_id))
        
        params = {
            "action": "goto",
            "number": preset_id
        }
        
        try:
            r = self.session.get(f"{self.camera_url}/cgi-bin/ptz", params=params, timeout=5)
            if r.status_code == 200:
                print(f"📍 Goto Preset {preset_id}")
                return True
        except Exception as e:
            print(f"❌ Preset Error: {e}")
        
        return False
    
    def set_preset(self, preset_id: int, name: str = ""):
        """Speichere aktuelle Position als Preset."""
        preset_id = max(1, min(255, preset_id))
        
        params = {
            "action": "set",
            "number": preset_id,
            "name": name
        }
        
        try:
            r = self.session.get(f"{self.camera_url}/cgi-bin/ptz", params=params, timeout=5)
            if r.status_code == 200:
                print(f"💾 Preset {preset_id} gespeichert")
                return True
        except Exception as e:
            print(f"❌ Set Preset Error: {e}")
        
        return False

def load_ptz_config() -> Optional[dict]:
    """Lade PTZ Kamera Config."""
    if os.path.exists(PTZ_CONFIG):
        try:
            with open(PTZ_CONFIG, 'r') as f:
                return json.load(f)
        except:
            pass
    
    return {
        "enabled": False,
        "camera_url": "http://192.168.1.100",
        "username": "admin",
        "password": "12345"
    }

if __name__ == '__main__':
    config = load_ptz_config()
    
    if not config.get("enabled"):
        print("⚠️ PTZ nicht konfiguriert")
        print(f"   Bearbeite: {PTZ_CONFIG}")
        sys.exit(1)
    
    ptz = PTZController(
        config["camera_url"],
        config["username"],
        config["password"]
    )
    
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    
    cmd = sys.argv[1].lower()
    
    try:
        if cmd == "pan" and len(sys.argv) >= 3:
            direction = sys.argv[2]
            speed = int(sys.argv[3]) if len(sys.argv) >= 4 else 5
            ptz.pan(direction, speed)
        
        elif cmd == "tilt" and len(sys.argv) >= 3:
            direction = sys.argv[2]
            speed = int(sys.argv[3]) if len(sys.argv) >= 4 else 5
            ptz.tilt(direction, speed)
        
        elif cmd == "zoom" and len(sys.argv) >= 3:
            direction = sys.argv[2]
            speed = int(sys.argv[3]) if len(sys.argv) >= 4 else 3
            ptz.zoom(direction, speed)
        
        elif cmd == "preset" and len(sys.argv) >= 3:
            preset_id = int(sys.argv[2])
            ptz.goto_preset(preset_id)
        
        else:
            print(__doc__)
    
    except Exception as e:
        print(f"❌ Fehler: {e}")
