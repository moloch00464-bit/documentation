#!/usr/bin/env python3
"""
Brain Backup & Sync System für M.O.L.O.C.H.
Auto-Backup des Gehirns zu Google Drive mit Versionierung

Usage:
  python brain_backup.py                     # Full backup now
  python brain_backup.py --auto              # Start auto-backup daemon
  python brain_backup.py --restore <date>    # Restore von backup
  python brain_backup.py --list              # Liste alle backups
"""

import os
import sys
import json
import shutil
import time
from datetime import datetime
from pathlib import Path
import subprocess

# Config
BRAIN_DIR = os.path.expanduser("~/moloch/brain")
BACKUP_DIR = os.path.expanduser("~/moloch/backups")
BACKUP_INDEX = os.path.expanduser("~/moloch/backup_index.json")
GDRIVE_FOLDER = "M.O.L.O.C.H. Brain Backups"  # Google Drive Ordner

def ensure_backup_dir():
    """Erstelle Backup-Verzeichnis."""
    os.makedirs(BACKUP_DIR, exist_ok=True)

def load_backup_index():
    """Lade Backup-Index."""
    if os.path.exists(BACKUP_INDEX):
        try:
            with open(BACKUP_INDEX, 'r') as f:
                return json.load(f)
        except:
            pass
    return {"backups": [], "last_backup": None}

def save_backup_index(index):
    """Speichere Backup-Index."""
    with open(BACKUP_INDEX, 'w') as f:
        json.dump(index, f, indent=2)

def create_backup():
    """Erstelle Backup des Brain-Verzeichnisses."""
    ensure_backup_dir()
    
    if not os.path.exists(BRAIN_DIR):
        print("❌ Brain-Verzeichnis nicht gefunden")
        return None
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = f"brain_backup_{timestamp}"
    backup_path = os.path.join(BACKUP_DIR, backup_name)
    
    try:
        print(f"💾 Erstelle Backup: {backup_name}")
        shutil.copytree(BRAIN_DIR, backup_path)
        
        # Komprimiere
        print("🗜️ Komprimiere...")
        archive_path = f"{backup_path}.tar.gz"
        subprocess.run(
            f"tar -czf {archive_path} -C {BACKUP_DIR} {backup_name}",
            shell=True,
            check=False
        )
        
        # Alte Kopie löschen
        if os.path.exists(backup_path):
            shutil.rmtree(backup_path)
        
        # Index aktualisieren
        index = load_backup_index()
        index["backups"].append({
            "timestamp": timestamp,
            "size": os.path.getsize(archive_path),
            "path": archive_path
        })
        index["last_backup"] = timestamp
        save_backup_index(index)
        
        size_mb = os.path.getsize(archive_path) / (1024 * 1024)
        print(f"✅ Backup fertig: {size_mb:.1f} MB")
        return archive_path
    
    except Exception as e:
        print(f"❌ Backup Fehler: {e}")
        return None

def upload_to_gdrive(backup_path):
    """Lade Backup zu Google Drive hoch (via rclone)."""
    try:
        # Check if rclone configured
        result = subprocess.run(
            "rclone listremotes",
            shell=True,
            capture_output=True,
            text=True
        )
        
        if "gdrive:" not in result.stdout:
            print("⚠️ Google Drive nicht konfiguriert (rclone)")
            print("   Setup: rclone config")
            return False
        
        print(f"📤 Lade zu Google Drive hoch...")
        backup_filename = os.path.basename(backup_path)
        
        subprocess.run(
            f"rclone copy {backup_path} gdrive:{GDRIVE_FOLDER}/",
            shell=True,
            check=False
        )
        
        print(f"✅ Hochgeladen: gdrive:{GDRIVE_FOLDER}/{backup_filename}")
        return True
    
    except Exception as e:
        print(f"⚠️ Google Drive Upload Fehler: {e}")
        return False

def list_backups():
    """Liste alle Backups."""
    index = load_backup_index()
    
    if not index["backups"]:
        print("📭 Keine Backups gefunden")
        return
    
    print("\n🗂️ Verfügbare Backups:")
    for i, backup in enumerate(index["backups"]):
        size = backup.get("size", 0) / (1024 * 1024)
        ts = backup["timestamp"]
        print(f"  {i+1}. {ts} ({size:.1f} MB)")
    print()

def restore_backup(timestamp):
    """Stelle Backup wieder her."""
    index = load_backup_index()
    
    backup_entry = None
    for b in index["backups"]:
        if b["timestamp"] == timestamp:
            backup_entry = b
            break
    
    if not backup_entry:
        print(f"❌ Backup {timestamp} nicht gefunden")
        return False
    
    try:
        backup_path = backup_entry["path"]
        
        if not os.path.exists(backup_path):
            print(f"❌ Backup-Datei nicht gefunden: {backup_path}")
            return False
        
        print(f"⚠️ Stelle Brain wieder her von {timestamp}...")
        
        # Backup des aktuellen Brain machen (Safety)
        safety_backup = f"{BRAIN_DIR}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        if os.path.exists(BRAIN_DIR):
            shutil.move(BRAIN_DIR, safety_backup)
            print(f"💾 Safety-Backup erstellt: {safety_backup}")
        
        # Wiederherstellen
        subprocess.run(
            f"tar -xzf {backup_path} -C {os.path.dirname(BRAIN_DIR)}",
            shell=True,
            check=False
        )
        
        print(f"✅ Brain wiederhergestellt!")
        return True
    
    except Exception as e:
        print(f"❌ Restore Fehler: {e}")
        return False

def auto_backup_daemon(interval: int = 3600):
    """Auto-Backup Daemon (Standard: 1 Stunde)."""
    print(f"🔄 Auto-Backup gestartet (Interval: {interval}s)")
    
    try:
        while True:
            backup_path = create_backup()
            if backup_path:
                upload_to_gdrive(backup_path)
            
            print(f"⏰ Nächstes Backup in {interval}s...")
            time.sleep(interval)
    
    except KeyboardInterrupt:
        print("\n⛔ Auto-Backup gestoppt")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        # Default: Backup jetzt
        backup_path = create_backup()
        if backup_path:
            upload_to_gdrive(backup_path)
    
    elif sys.argv[1] == "--auto":
        interval = int(sys.argv[2]) if len(sys.argv) > 2 else 3600
        auto_backup_daemon(interval)
    
    elif sys.argv[1] == "--list":
        list_backups()
    
    elif sys.argv[1] == "--restore" and len(sys.argv) > 2:
        restore_backup(sys.argv[2])
    
    else:
        print(__doc__)
