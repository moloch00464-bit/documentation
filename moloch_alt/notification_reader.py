#!/usr/bin/env python3
"""
Notification Reader für M.O.L.O.C.H.
Android Benachrichtigungen lesen & vorlesen

Reads from /sdcard/Android/data/com.termux/files/home/.moloch/notifications.json
(Updated by Tasker automation or notification listener service)

Usage:
  python notification_reader.py              # Monitor & speak notifications
  python notification_reader.py --list       # Liste aktuelle Notifications
  python notification_reader.py --clear      # Lösche alle Notifications
  python notification_reader.py --filter     # Setze Filter
  python notification_reader.py --daemon     # Background daemon
"""

import os
import sys
import json
import time
import subprocess
from datetime import datetime

# Pfade
NOTIFICATION_DIR = os.path.expanduser("~/moloch")
NOTIFICATION_FILE = os.path.join(NOTIFICATION_DIR, "notifications.json")
NOTIFICATION_FILTER = os.path.join(NOTIFICATION_DIR, "notification_filter.json")

# Default Filter (ignoriere diese Apps)
DEFAULT_FILTER = {
    "ignore_apps": [
        "com.android.systemui",
        "com.google.android.apps.wellbeing",
        "com.android.settings",
    ],
    "priority_apps": [
        "com.whatsapp",
        "com.telegram.messenger",
        "com.google.android.gm",  # Gmail
    ],
    "enabled": True
}

class NotificationReader:
    def __init__(self):
        self.notifications = []
        self.processed_ids = set()
        self.filter_config = self.load_filter()
    
    def load_filter(self):
        """Lade Benachrichtigungs-Filter."""
        if os.path.exists(NOTIFICATION_FILTER):
            try:
                with open(NOTIFICATION_FILTER, 'r') as f:
                    return json.load(f)
            except:
                pass
        
        # Save defaults
        self.save_filter(DEFAULT_FILTER)
        return DEFAULT_FILTER
    
    def save_filter(self, filter_config):
        """Speichere Filter."""
        os.makedirs(NOTIFICATION_DIR, exist_ok=True)
        with open(NOTIFICATION_FILTER, 'w') as f:
            json.dump(filter_config, f, indent=2)
    
    def load_notifications(self):
        """Lade Benachrichtigungen aus Datei."""
        if not os.path.exists(NOTIFICATION_FILE):
            return []
        
        try:
            with open(NOTIFICATION_FILE, 'r') as f:
                return json.load(f)
        except:
            return []
    
    def save_notifications(self, notifications):
        """Speichere Benachrichtigungen."""
        os.makedirs(NOTIFICATION_DIR, exist_ok=True)
        with open(NOTIFICATION_FILE, 'w') as f:
            json.dump(notifications, f, indent=2)
    
    def should_process(self, notification):
        """Prüfe ob Benachrichtigung verarbeitet werden sollte."""
        if not self.filter_config.get("enabled", True):
            return False
        
        app = notification.get("package", "")
        
        # Ignoriere bestimmte Apps
        if app in self.filter_config.get("ignore_apps", []):
            return False
        
        # Filtere Spam/Duplicates
        notification_id = notification.get("id", "")
        if notification_id in self.processed_ids:
            return False
        
        return True
    
    def format_notification(self, notification):
        """Formatiere Benachrichtigung für Anzeige."""
        app = notification.get("package", "Unknown").split('.')[-1]
        title = notification.get("title", "")
        text = notification.get("text", "")
        
        # Kürze lange Texte
        if len(text) > 200:
            text = text[:197] + "..."
        
        return f"📱 {app}: {title}\n{text}"
    
    def speak_notification(self, notification):
        """Spreche Benachrichtigung aus."""
        app = notification.get("package", "Unknown").split('.')[-1]
        title = notification.get("title", "")
        text = notification.get("text", "")
        
        # Kurze Version für TTS
        message = f"{app}. {title}. {text}"
        
        # Begrentz auf ~300 Zeichen für schnelle Ansage
        if len(message) > 300:
            message = message[:297] + "..."
        
        try:
            # Versuche via speak() aus moloch.py (wenn verfügbar)
            import sys
            sys.path.insert(0, NOTIFICATION_DIR)
            from moloch import speak
            
            speak(message)
        
        except:
            # Fallback zu termux-tts
            try:
                subprocess.run(
                    ["termux-tts-speak", message],
                    timeout=30,
                    check=False
                )
            except:
                print(f"❌ TTS Error für: {message}")
    
    def process_notifications(self):
        """Verarbeite neue Benachrichtigungen."""
        notifications = self.load_notifications()
        
        new_count = 0
        for notification in notifications:
            if self.should_process(notification):
                app = notification.get("package", "")
                notification_id = notification.get("id", "")
                
                # Markiere als verarbeitet
                self.processed_ids.add(notification_id)
                
                # Prioritäts-Apps bekommen sofort Sprachausgabe
                if app in self.filter_config.get("priority_apps", []):
                    print(self.format_notification(notification))
                    self.speak_notification(notification)
                    new_count += 1
                
                else:
                    # Normale Apps: nur anzeigen
                    print(self.format_notification(notification))
                    new_count += 1
        
        return new_count
    
    def list_notifications(self):
        """Liste alle Benachrichtigungen."""
        notifications = self.load_notifications()
        
        if not notifications:
            print("📭 Keine Benachrichtigungen")
            return
        
        print(f"📬 {len(notifications)} Benachrichtigungen:\n")
        
        for i, notif in enumerate(notifications[-10:], 1):  # Letzte 10
            timestamp = notif.get("timestamp", "")
            print(self.format_notification(notif))
            print(f"   ⏱️ {timestamp}\n")
    
    def clear_notifications(self):
        """Lösche alle Benachrichtigungen."""
        print("🗑️ Lösche alle Benachrichtigungen...")
        self.save_notifications([])
        self.processed_ids.clear()
        print("✅ Gelöscht")
    
    def monitor_daemon(self, interval: int = 5):
        """Hintergrund-Daemon überwacht Benachrichtigungen."""
        print(f"📱 Notification Daemon gestartet (Check alle {interval}s)")
        
        try:
            while True:
                count = self.process_notifications()
                if count > 0:
                    print(f"✅ {count} neue Benachrichtigungen verarbeitet")
                
                time.sleep(interval)
        
        except KeyboardInterrupt:
            print("\n⛔ Notification Daemon gestoppt")
    
    def configure_filter(self):
        """Interaktive Filter-Konfiguration."""
        print("🔧 Notification Filter Konfiguration\n")
        
        print(f"Aktuell ignorierte Apps: {self.filter_config.get('ignore_apps', [])}")
        print(f"Prioritäts-Apps: {self.filter_config.get('priority_apps', [])}\n")
        
        print("1. App zu Ignore-Liste hinzufügen")
        print("2. App aus Ignore-Liste entfernen")
        print("3. App zu Prioritäts-Liste hinzufügen")
        
        choice = input("Wahl (1-3) oder q zum Beenden: ").strip().lower()
        
        if choice == "1":
            app = input("Package name (z.B. com.facebook.katana): ").strip()
            if app and app not in self.filter_config.get("ignore_apps", []):
                self.filter_config["ignore_apps"].append(app)
                self.save_filter(self.filter_config)
                print(f"✅ {app} ignoriert")
        
        elif choice == "2":
            app = input("Package name: ").strip()
            if app in self.filter_config.get("ignore_apps", []):
                self.filter_config["ignore_apps"].remove(app)
                self.save_filter(self.filter_config)
                print(f"✅ {app} nicht mehr ignoriert")
        
        elif choice == "3":
            app = input("Package name: ").strip()
            if app and app not in self.filter_config.get("priority_apps", []):
                self.filter_config["priority_apps"].append(app)
                self.save_filter(self.filter_config)
                print(f"✅ {app} ist jetzt Priorität")

if __name__ == "__main__":
    reader = NotificationReader()
    
    if len(sys.argv) < 2:
        reader.process_notifications()
    
    elif sys.argv[1] == "--list":
        reader.list_notifications()
    
    elif sys.argv[1] == "--clear":
        reader.clear_notifications()
    
    elif sys.argv[1] == "--filter":
        reader.configure_filter()
    
    elif sys.argv[1] == "--daemon":
        interval = int(sys.argv[2]) if len(sys.argv) > 2 else 5
        reader.monitor_daemon(interval)
    
    else:
        print(__doc__)
