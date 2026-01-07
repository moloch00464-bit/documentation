#!/usr/bin/env python3
"""
Volume Setter für M.O.L.O.C.H.
Schnelle Lautstärkenanpassung ohne App zu öffnen.

Usage:
  python set_volume.py 10       # Set to level 10
  python set_volume.py up       # Increase by 1 (or 2 if Tasker)
  python set_volume.py down     # Decrease by 1
  python set_volume.py mute     # Set to 0
  python set_volume.py max      # Set to 15
"""

import os
import sys
import subprocess
from pathlib import Path

# Konfigurationsdatei
CONFIG_FILE = os.path.expanduser("~/moloch/volume.conf")

def load_volume():
    """Lade aktuelle Lautstärke aus Config."""
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r') as f:
                return int(f.read().strip())
        except:
            pass
    return 10  # Default

def save_volume(vol):
    """Speichere Lautstärke in Config."""
    os.makedirs(os.path.dirname(CONFIG_FILE), exist_ok=True)
    with open(CONFIG_FILE, 'w') as f:
        f.write(str(max(0, min(15, vol))))

def set_volume(vol):
    """Setzt Lautstärke via termux-volume."""
    vol = max(0, min(15, vol))
    try:
        subprocess.run(["termux-volume", "music", str(vol)], timeout=5, check=False)
        save_volume(vol)
        print(f"🔊 Volume: {vol}/15")
        return True
    except Exception as e:
        print(f"❌ Fehler: {e}")
        return False

if __name__ == '__main__':
    current = load_volume()
    
    if len(sys.argv) < 2:
        print(f"Aktuelle Lautstärke: {current}/15")
        print("Usage: python set_volume.py <level|up|down|mute|max>")
        sys.exit(0)
    
    arg = sys.argv[1].lower()
    
    if arg == "up":
        new_vol = min(15, current + 2)  # +2 für Tasker Schnelligkeit
        set_volume(new_vol)
    elif arg == "down":
        new_vol = max(0, current - 2)
        set_volume(new_vol)
    elif arg == "mute":
        set_volume(0)
    elif arg == "max":
        set_volume(15)
    else:
        try:
            set_volume(int(arg))
        except ValueError:
            print(f"❌ Ungültiges Argument: {arg}")
