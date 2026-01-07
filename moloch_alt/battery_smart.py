#!/usr/bin/env python3
"""
Batterie-Intelligenz für M.O.L.O.C.H.
Akku-Status & Sparmodus automatisch

Usage:
  python battery_smart.py                    # Check battery & activate savemode if needed
  python battery_smart.py --status          # Zeige Akku-Status
  python battery_smart.py --savemode on|off # Sparmodus an/aus
  python battery_smart.py --daemon          # Background daemon
"""

import os
import sys
import json
import subprocess
import time

# Config
BATTERY_CONFIG = os.path.expanduser("~/moloch/battery_config.json")
BATTERY_THRESHOLD = 20  # % - Sparmodus aktiviert unter dieser Prozent

def get_battery_status():
    """Hole Akku-Status via termux-battery-status."""
    try:
        result = subprocess.run(
            ["termux-battery-status"],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        if result.returncode == 0:
            return json.loads(result.stdout)
    except Exception as e:
        print(f"⚠️ Battery Status Fehler: {e}")
    
    return None

def load_battery_config():
    """Lade Batterie-Config."""
    if os.path.exists(BATTERY_CONFIG):
        try:
            with open(BATTERY_CONFIG, 'r') as f:
                return json.load(f)
        except:
            pass
    
    return {
        "savemode_enabled": False,
        "last_check": None,
        "threshold": BATTERY_THRESHOLD
    }

def save_battery_config(config):
    """Speichere Batterie-Config."""
    os.makedirs(os.path.dirname(BATTERY_CONFIG), exist_ok=True)
    with open(BATTERY_CONFIG, 'w') as f:
        json.dump(config, f, indent=2)

def activate_savemode():
    """Aktiviere Sparmodus."""
    config = load_battery_config()
    
    if config["savemode_enabled"]:
        print("⚠️ Sparmodus schon aktiv")
        return
    
    print("🔋 Aktiviere Sparmodus...")
    
    # Reduce CPU speed (wenn möglich)
    try:
        # Android/Termux specific
        subprocess.run(
            "termux-vibrate 500",
            shell=True,
            check=False,
            timeout=2
        )
    except:
        pass
    
    config["savemode_enabled"] = True
    save_battery_config(config)
    
    print("✅ Sparmodus AKTIV")
    print("   - Reduzierte Rechenleistung")
    print("   - Kürzere Timeouts")
    print("   - Offline-Modus für einige Features")

def deactivate_savemode():
    """Deaktiviere Sparmodus."""
    config = load_battery_config()
    
    if not config["savemode_enabled"]:
        print("⚠️ Sparmodus nicht aktiv")
        return
    
    print("🔌 Deaktiviere Sparmodus...")
    config["savemode_enabled"] = False
    save_battery_config(config)
    
    print("✅ Normalmodus AKTIV")

def check_and_adjust():
    """Prüfe Akku und passe Modus automatisch an."""
    status = get_battery_status()
    
    if not status:
        print("❌ Kann Akku-Status nicht auslesen")
        return
    
    percentage = status.get("percentage", 0)
    health = status.get("health", "unknown")
    plugged = status.get("plugged", "none")
    
    print(f"🔋 Akku: {percentage}% | {health} | Stecker: {plugged}")
    
    config = load_battery_config()
    threshold = config.get("threshold", BATTERY_THRESHOLD)
    
    # Auto-Entscheidung
    if percentage <= threshold:
        if not config["savemode_enabled"]:
            print(f"⚠️ Akku unter {threshold}% - Aktiviere Sparmodus!")
            activate_savemode()
    else:
        if config["savemode_enabled"] and plugged != "none":
            print(f"✅ Akku über {threshold}% und lädt - Deaktiviere Sparmodus")
            deactivate_savemode()

def battery_daemon(check_interval: int = 300):
    """Background Daemon für kontinuierliche Überwachung."""
    print(f"🔋 Battery Daemon gestartet (Check alle {check_interval}s)")
    
    try:
        while True:
            check_and_adjust()
            time.sleep(check_interval)
    
    except KeyboardInterrupt:
        print("\n⛔ Battery Daemon gestoppt")

def get_savemode_status():
    """Gibt aktuellen Sparmodus-Status zurück."""
    config = load_battery_config()
    status = get_battery_status()
    
    if status:
        print(f"Akku: {status.get('percentage', '?')}%")
        print(f"Zustand: {status.get('health', '?')}")
        print(f"Stecker: {status.get('plugged', '?')}")
    
    if config["savemode_enabled"]:
        print("Status: 🔴 SPARMODUS AKTIV")
    else:
        print("Status: 🟢 NORMALMODUS")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        check_and_adjust()
    
    elif sys.argv[1] == "--status":
        get_savemode_status()
    
    elif sys.argv[1] == "--savemode":
        if len(sys.argv) > 2:
            if sys.argv[2].lower() == "on":
                activate_savemode()
            elif sys.argv[2].lower() == "off":
                deactivate_savemode()
    
    elif sys.argv[1] == "--daemon":
        interval = int(sys.argv[2]) if len(sys.argv) > 2 else 300
        battery_daemon(interval)
    
    else:
        print(__doc__)
