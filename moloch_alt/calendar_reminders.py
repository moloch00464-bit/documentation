#!/usr/bin/env python3
"""
Calendar & Reminders für M.O.L.O.C.H.
Termine, Erinnerungen, To-Do Lists

Integration mit Google Calendar (optional)
Lokale JSON-Speicherung

Usage:
  python calendar_reminders.py --add "Zahnarzt" "14:00 Freitag"
  python calendar_reminders.py --list
  python calendar_reminders.py --remind          # Check Reminders
  python calendar_reminders.py --daemon          # Background daemon
  python calendar_reminders.py --today           # Heutige Termine
"""

import os
import sys
import json
from datetime import datetime, timedelta
import time

CALENDAR_FILE = os.path.expanduser("~/moloch/calendar.json")
REMINDERS_FILE = os.path.expanduser("~/moloch/reminders.json")

class CalendarReminders:
    def __init__(self):
        self.calendar = self.load_calendar()
        self.reminders = self.load_reminders()
    
    def load_calendar(self):
        """Lade Kalender."""
        if os.path.exists(CALENDAR_FILE):
            try:
                with open(CALENDAR_FILE, 'r') as f:
                    return json.load(f)
            except:
                pass
        
        return {"events": []}
    
    def save_calendar(self):
        """Speichere Kalender."""
        os.makedirs(os.path.dirname(CALENDAR_FILE), exist_ok=True)
        with open(CALENDAR_FILE, 'w') as f:
            json.dump(self.calendar, f, indent=2)
    
    def load_reminders(self):
        """Lade Reminders."""
        if os.path.exists(REMINDERS_FILE):
            try:
                with open(REMINDERS_FILE, 'r') as f:
                    return json.load(f)
            except:
                pass
        
        return {
            "daily": [],
            "one_time": [],
            "completed": []
        }
    
    def save_reminders(self):
        """Speichere Reminders."""
        os.makedirs(os.path.dirname(REMINDERS_FILE), exist_ok=True)
        with open(REMINDERS_FILE, 'w') as f:
            json.dump(self.reminders, f, indent=2)
    
    def parse_datetime(self, time_str):
        """Parse Zeitangabe in verschiedenen Formaten."""
        # Versuche verschiedene Formate
        formats = [
            "%H:%M %A",           # "14:00 Freitag"
            "%H:%M %d.%m",        # "14:00 25.12"
            "%H:%M",              # "14:00"
            "%d.%m %H:%M",        # "25.12 14:00"
        ]
        
        # Deutsch zu Englisch Wochentage
        german_days = {
            "montag": "Monday", "dienstag": "Tuesday",
            "mittwoch": "Wednesday", "donnerstag": "Thursday",
            "freitag": "Friday", "samstag": "Saturday",
            "sonntag": "Sunday"
        }
        
        time_str_lower = time_str.lower()
        for de, en in german_days.items():
            time_str_lower = time_str_lower.replace(de, en)
        
        for fmt in formats:
            try:
                dt = datetime.strptime(time_str_lower, fmt)
                
                # Wenn nur Wochentag: berechne nächstes Datum
                if "%" in fmt and "%d" not in fmt and "%m" not in fmt:
                    today = datetime.now()
                    target_weekday = dt.weekday()
                    current_weekday = today.weekday()
                    
                    days_ahead = (target_weekday - current_weekday) % 7
                    if days_ahead == 0:
                        days_ahead = 7  # Nächste Woche
                    
                    dt = today + timedelta(days=days_ahead)
                    dt = dt.replace(hour=dt.hour, minute=dt.minute)
                
                return dt
            
            except ValueError:
                continue
        
        return None
    
    def add_event(self, title, time_str, description=""):
        """Füge Event hinzu."""
        dt = self.parse_datetime(time_str)
        
        if not dt:
            print(f"❌ Zeitformat nicht erkannt: {time_str}")
            print("   Versuche: '14:00 Freitag' oder '14:00 25.12'")
            return False
        
        event = {
            "title": title,
            "datetime": dt.isoformat(),
            "description": description,
            "created": datetime.now().isoformat(),
            "reminder_sent": False
        }
        
        self.calendar["events"].append(event)
        self.save_calendar()
        
        print(f"✅ Event hinzugefügt: {title}")
        print(f"   Zeitpunkt: {dt.strftime('%A, %d.%m.%Y %H:%M')}")
        
        return True
    
    def add_reminder(self, text, reminder_type="one_time", repeat_days=None):
        """Füge Reminder hinzu."""
        reminder = {
            "text": text,
            "created": datetime.now().isoformat(),
            "type": reminder_type,
            "repeat_days": repeat_days,  # Für daily reminders
            "last_triggered": None
        }
        
        self.reminders[reminder_type].append(reminder)
        self.save_reminders()
        
        print(f"✅ Reminder hinzugefügt: {text}")
        
        return True
    
    def list_events(self):
        """Liste Events."""
        events = sorted(self.calendar.get("events", []), 
                       key=lambda e: e["datetime"])
        
        if not events:
            print("📭 Keine Events")
            return
        
        print("\n📅 Deine Events:\n")
        
        for event in events:
            dt = datetime.fromisoformat(event["datetime"])
            title = event["title"]
            desc = event.get("description", "")
            
            # Formatiere Datum
            now = datetime.now()
            if dt.date() == now.date():
                date_str = "Heute"
            elif dt.date() == (now + timedelta(days=1)).date():
                date_str = "Morgen"
            else:
                date_str = dt.strftime("%A, %d.%m.%Y")
            
            print(f"📍 {title}")
            print(f"   ⏰ {date_str} um {dt.strftime('%H:%M')}")
            if desc:
                print(f"   📝 {desc}")
            print()
    
    def list_reminders(self):
        """Liste Reminders."""
        print("\n🔔 Deine Reminders:\n")
        
        # Daily
        daily = self.reminders.get("daily", [])
        if daily:
            print("🔄 Täglich:")
            for r in daily:
                print(f"   ✓ {r['text']}")
        
        # One-time
        one_time = self.reminders.get("one_time", [])
        if one_time:
            print("\n📌 Einmalig:")
            for r in one_time:
                print(f"   ✓ {r['text']}")
        
        if not daily and not one_time:
            print("Keine Reminders gesetzt")
        
        print()
    
    def list_today(self):
        """Liste Termine für heute."""
        today = datetime.now().date()
        
        events = [e for e in self.calendar.get("events", [])
                 if datetime.fromisoformat(e["datetime"]).date() == today]
        
        if not events:
            print("📭 Keine Termine für heute")
            return
        
        print(f"\n📅 Termine für {today.strftime('%A, %d.%m.%Y')}:\n")
        
        for event in sorted(events, key=lambda e: e["datetime"]):
            dt = datetime.fromisoformat(event["datetime"])
            print(f"⏰ {dt.strftime('%H:%M')} - {event['title']}")
            if event.get("description"):
                print(f"   {event['description']}")
        
        print()
    
    def check_reminders(self):
        """Prüfe Reminders & Events."""
        triggered = []
        
        # Check Daily Reminders
        for reminder in self.reminders.get("daily", []):
            print(f"📌 {reminder['text']}")
            triggered.append(reminder)
        
        # Check Events (heute & kommend)
        now = datetime.now()
        upcoming = []
        
        for event in self.calendar.get("events", []):
            dt = datetime.fromisoformat(event["datetime"])
            
            # Nur zukünftige Events
            if dt > now:
                # Weniger als 1 Stunde entfernt?
                if (dt - now).total_seconds() < 3600 and not event.get("reminder_sent"):
                    minutes = int((dt - now).total_seconds() / 60)
                    print(f"🔔 Erinnerung: {event['title']} in {minutes} Minuten!")
                    event["reminder_sent"] = True
                    triggered.append(event)
                    upcoming.append(event)
        
        if triggered:
            self.save_calendar()
            self.save_reminders()
            
            # Spreche Reminder
            try:
                sys.path.insert(0, os.path.expanduser("~/moloch"))
                from moloch import speak
                
                if triggered:
                    text = f"Du hast {len(triggered)} Reminders"
                    speak(text)
            except:
                pass
        
        return triggered
    
    def reminder_daemon(self, check_interval=300):
        """Hintergrund-Daemon für Reminders."""
        print(f"🤖 Calendar Daemon gestartet (Check alle {check_interval}s)")
        
        try:
            while True:
                self.check_reminders()
                time.sleep(check_interval)
        
        except KeyboardInterrupt:
            print("\n⛔ Calendar Daemon gestoppt")
    
    def delete_event(self, title):
        """Lösche Event."""
        self.calendar["events"] = [
            e for e in self.calendar["events"]
            if e["title"].lower() != title.lower()
        ]
        self.save_calendar()
        print(f"✅ Event gelöscht: {title}")

if __name__ == "__main__":
    cal = CalendarReminders()
    
    if len(sys.argv) < 2:
        print(__doc__)
    
    elif sys.argv[1] == "--add":
        if len(sys.argv) > 3:
            title = sys.argv[2]
            time_str = sys.argv[3]
            desc = " ".join(sys.argv[4:]) if len(sys.argv) > 4 else ""
            cal.add_event(title, time_str, desc)
    
    elif sys.argv[1] == "--add-reminder":
        if len(sys.argv) > 2:
            text = " ".join(sys.argv[2:])
            reminder_type = "one_time"
            if "--daily" in sys.argv:
                reminder_type = "daily"
            cal.add_reminder(text, reminder_type)
    
    elif sys.argv[1] == "--list":
        cal.list_events()
    
    elif sys.argv[1] == "--reminders":
        cal.list_reminders()
    
    elif sys.argv[1] == "--today":
        cal.list_today()
    
    elif sys.argv[1] == "--remind":
        cal.check_reminders()
    
    elif sys.argv[1] == "--daemon":
        interval = int(sys.argv[2]) if len(sys.argv) > 2 else 300
        cal.reminder_daemon(interval)
    
    elif sys.argv[1] == "--delete":
        if len(sys.argv) > 2:
            title = " ".join(sys.argv[2:])
            cal.delete_event(title)
    
    else:
        print(__doc__)
