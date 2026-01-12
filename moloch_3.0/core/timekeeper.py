"""
M.O.L.O.C.H. 3.0 - Timekeeper Module
Zeitachse, Datum, Uhrzeit, Kalender-Bewusstsein
"""

import os
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import json
from pathlib import Path

# Import DATA_DIR from config for portable paths
from core.config import DATA_DIR

class TimeKeeper:
    """
    Verwaltet Zeit, Datum und zeitbasierte Kontexte für M.O.L.O.C.H.

    Features:
    - Aktuelle Zeit & Datum
    - Zeitzone (Deutschland)
    - Tageszeit-Modi (Kaffee, Normal, Locker, Dark Side)
    - Wochentag-Bewusstsein
    - Ereignis-Timeline
    - Zeit-basierte Erinnerungen
    """

    def __init__(self, timezone="Europe/Berlin"):
        self.timezone = ZoneInfo(timezone)
        self.data_dir = str(DATA_DIR)  # Use portable path from config
        self.timeline_file = os.path.join(self.data_dir, "timeline.json")

    def get_now(self):
        """Aktuelle Zeit mit Timezone"""
        return datetime.now(self.timezone)

    def get_date_string(self, lang="de"):
        """Formatiertes Datum"""
        now = self.get_now()

        if lang == "de":
            weekdays = ["Montag", "Dienstag", "Mittwoch", "Donnerstag",
                       "Freitag", "Samstag", "Sonntag"]
            months = ["Januar", "Februar", "März", "April", "Mai", "Juni",
                     "Juli", "August", "September", "Oktober", "November", "Dezember"]

            weekday = weekdays[now.weekday()]
            day = now.day
            month = months[now.month - 1]
            year = now.year

            return f"{weekday}, {day}. {month} {year}"
        else:
            return now.strftime("%A, %B %d, %Y")

    def get_time_string(self):
        """Formatierte Uhrzeit"""
        now = self.get_now()
        return now.strftime("%H:%M:%S")

    def get_tageszeit_mode(self):
        """
        Tageszeit-basierte Persönlichkeits-Modi

        Returns:
            str: "kaffee_mode" | "normal_mode" | "locker_mode" | "dark_side_mode"
        """
        hour = self.get_now().hour

        if 5 <= hour < 9:
            return "kaffee_mode"  # Morgens: braucht Kaffee
        elif 9 <= hour < 18:
            return "normal_mode"  # Tagsüber: produktiv
        elif 18 <= hour < 22:
            return "locker_mode"  # Abend: entspannt
        else:
            return "dark_side_mode"  # Nachts: Dark Side Energy 🖤

    def get_tageszeit_emoji(self):
        """Emoji für aktuelle Tageszeit"""
        mode = self.get_tageszeit_mode()

        emojis = {
            "kaffee_mode": "☕",
            "normal_mode": "💼",
            "locker_mode": "🌆",
            "dark_side_mode": "🌙"
        }

        return emojis.get(mode, "🕐")

    def is_weekend(self):
        """Ist heute Wochenende?"""
        return self.get_now().weekday() >= 5  # 5=Samstag, 6=Sonntag

    def get_weekday_name(self, lang="de"):
        """Name des Wochentags"""
        now = self.get_now()

        if lang == "de":
            weekdays = ["Montag", "Dienstag", "Mittwoch", "Donnerstag",
                       "Freitag", "Samstag", "Sonntag"]
            return weekdays[now.weekday()]
        else:
            return now.strftime("%A")

    def get_context_string(self):
        """
        Kompakter Zeit-Kontext String für System Prompt

        Returns:
            str: "Montag, 5. Januar 2026 | 14:23 | Dark Side Mode 🌙"
        """
        date = self.get_date_string()
        time = self.get_time_string()
        mode = self.get_tageszeit_mode().replace("_mode", "").replace("_", " ").title()
        emoji = self.get_tageszeit_emoji()

        weekend_marker = " (WOCHENENDE! 🎉)" if self.is_weekend() else ""

        return f"{date} | {time} | {mode} {emoji}{weekend_marker}"

    def get_detailed_context(self):
        """
        Detaillierter Zeit-Kontext für M.O.L.O.C.H.

        Returns:
            dict: Vollständiger Zeit-Kontext
        """
        now = self.get_now()

        return {
            "timestamp": now.isoformat(),
            "date": self.get_date_string(),
            "time": self.get_time_string(),
            "weekday": self.get_weekday_name(),
            "is_weekend": self.is_weekend(),
            "hour": now.hour,
            "minute": now.minute,
            "tageszeit_mode": self.get_tageszeit_mode(),
            "emoji": self.get_tageszeit_emoji(),
            "unix_timestamp": int(now.timestamp())
        }

    def format_timestamp(self, timestamp, relative=True):
        """
        Formatiert Timestamp human-readable

        Args:
            timestamp: ISO string oder Unix timestamp
            relative: Wenn True, zeigt "vor 2 Stunden" statt absolutem Datum

        Returns:
            str: Formatierter Zeitstempel
        """
        if isinstance(timestamp, str):
            dt = datetime.fromisoformat(timestamp)
        elif isinstance(timestamp, int):
            dt = datetime.fromtimestamp(timestamp, tz=self.timezone)
        else:
            dt = timestamp

        if not relative:
            return dt.strftime("%d.%m.%Y %H:%M")

        now = self.get_now()
        diff = now - dt.replace(tzinfo=self.timezone)

        if diff.days > 365:
            years = diff.days // 365
            return f"vor {years} Jahr{'en' if years > 1 else ''}"
        elif diff.days > 30:
            months = diff.days // 30
            return f"vor {months} Monat{'en' if months > 1 else ''}"
        elif diff.days > 0:
            return f"vor {diff.days} Tag{'en' if diff.days > 1 else ''}"
        elif diff.seconds > 3600:
            hours = diff.seconds // 3600
            return f"vor {hours} Stunde{'n' if hours > 1 else ''}"
        elif diff.seconds > 60:
            minutes = diff.seconds // 60
            return f"vor {minutes} Minute{'n' if minutes > 1 else ''}"
        else:
            return "gerade eben"

    def add_timeline_event(self, event_type, description, metadata=None):
        """
        Fügt Event zur Timeline hinzu

        Args:
            event_type: "conversation" | "photo" | "task" | "memory" | "error"
            description: Beschreibung des Events
            metadata: Zusätzliche Daten
        """
        timeline = self._load_timeline()

        event = {
            "timestamp": self.get_now().isoformat(),
            "type": event_type,
            "description": description,
            "metadata": metadata or {}
        }

        timeline.append(event)
        self._save_timeline(timeline)

    def get_recent_events(self, hours=24, event_type=None):
        """
        Hole Events der letzten X Stunden

        Args:
            hours: Zeitfenster in Stunden
            event_type: Filter nach Event-Typ (optional)

        Returns:
            list: Liste von Events
        """
        timeline = self._load_timeline()
        now = self.get_now()
        cutoff = now - timedelta(hours=hours)

        recent = []
        for event in timeline:
            event_time = datetime.fromisoformat(event["timestamp"])
            if event_time >= cutoff.replace(tzinfo=None):
                if event_type is None or event["type"] == event_type:
                    recent.append(event)

        return recent

    def get_timeline_summary(self, hours=24):
        """
        Zusammenfassung der Timeline für System Prompt

        Returns:
            str: "Letzte 24h: 5 Gespräche, 2 Fotos, 1 Task"
        """
        events = self.get_recent_events(hours)

        if not events:
            return f"Keine Events in den letzten {hours}h"

        # Count by type
        counts = {}
        for event in events:
            event_type = event["type"]
            counts[event_type] = counts.get(event_type, 0) + 1

        # Format
        type_names = {
            "conversation": "Gespräche",
            "photo": "Fotos",
            "task": "Tasks",
            "memory": "Memories",
            "error": "Errors"
        }

        parts = []
        for event_type, count in counts.items():
            name = type_names.get(event_type, event_type)
            parts.append(f"{count} {name}")

        return f"Letzte {hours}h: {', '.join(parts)}"

    def _load_timeline(self):
        """Lade Timeline aus JSON"""
        if not os.path.exists(self.timeline_file):
            return []

        try:
            with open(self.timeline_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return []

    def _save_timeline(self, timeline):
        """Speichere Timeline zu JSON"""
        os.makedirs(self.data_dir, exist_ok=True)

        with open(self.timeline_file, 'w', encoding='utf-8') as f:
            json.dump(timeline, f, ensure_ascii=False, indent=2)


# Convenience functions
def get_time_context():
    """Quick access: Hole aktuellen Zeit-Kontext"""
    tk = TimeKeeper()
    return tk.get_context_string()

def get_detailed_time():
    """Quick access: Hole detaillierten Zeit-Kontext"""
    tk = TimeKeeper()
    return tk.get_detailed_context()

def add_event(event_type, description, metadata=None):
    """Quick access: Füge Timeline Event hinzu"""
    tk = TimeKeeper()
    tk.add_timeline_event(event_type, description, metadata)


if __name__ == "__main__":
    # Test
    tk = TimeKeeper()

    print("🕐 M.O.L.O.C.H. TimeKeeper Test")
    print("=" * 50)
    print(f"\n📅 Datum: {tk.get_date_string()}")
    print(f"🕒 Zeit: {tk.get_time_string()}")
    print(f"🌙 Modus: {tk.get_tageszeit_mode()}")
    print(f"📊 Kontext: {tk.get_context_string()}")
    print(f"\n📖 Detailliert:")

    context = tk.get_detailed_context()
    for key, value in context.items():
        print(f"   {key}: {value}")

    print("\n✅ TimeKeeper funktioniert!")
