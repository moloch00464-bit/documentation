# Phase 4: Advanced Integration Guide
**M.O.L.O.C.H. v3.0 - Adaptive Intelligence Features**

> Implementierung der optionalen Phase 4 Features (Location, Calendar, Weather, Clipboard, Music)

---

## 📚 Übersicht Phase 4

| Feature | Beschreibung | Status | Dependencies |
|---------|-------------|--------|--------------|
| **location_aware.py** | GPS-Geofencing + Location-basierte Personality | ✅ Complete | Termux API, Haversine |
| **calendar_reminders.py** | Kalender, Erinnerungen, Events | ✅ Complete | requests (Google Cal optional) |
| **weather_aware.py** | Wetter-Integration + Mood Adaptation | ✅ Complete | requests, Open-Meteo API |
| **clipboard_monitor.py** | Clipboard-Überwachung + Pattern Detection | ✅ Complete | Termux API, regex |
| **music_recognition.py** | Musik-Erkennung via AcoustID | ✅ Complete | chromaprint, ffmpeg |

---

## 🌍 1. Location Awareness (`location_aware.py`)

### Installation
```bash
python location_aware.py --help
```

### Setup: Orte hinzufügen
```bash
# Interaktiv
python location_aware.py add-location

# Oder manuell in ~/.moloch/locations.json:
{
  "home": {
    "lat": 52.5200,
    "lon": 13.4050,
    "personality": "pumuckl",
    "mood_bonus": "relaxed",
    "radius_m": 100
  },
  "work": {
    "lat": 52.5165,
    "lon": 13.3865,
    "personality": "hal",
    "mood_bonus": "focused",
    "radius_m": 150
  }
}
```

### Daemon starten
```bash
# Hintergrund
python location_aware.py daemon &

# Vordergrund (Test)
python location_aware.py daemon --interval 5
```

### Integration in moloch.py
```python
from location_aware import LocationAwareness

loc = LocationAwareness()

# Prüfe aktuelle Location
current = loc.detect_current_location()
if current:
    print(f"📍 Jetzt in: {current}")
    # Personality auto-wechselt!

# Daemon im Background
loc.start_daemon()
```

### API
```python
# Orte verwalten
loc.add_location("home", lat, lon, personality="pumuckl")
loc.get_location(name)
loc.remove_location(name)

# Detection
location = loc.detect_current_location()  # Returns: name oder None

# Dashboard
loc.display_dashboard()
stats = loc.get_stats()
```

---

## 📅 2. Calendar & Reminders (`calendar_reminders.py`)

### Installation
```bash
python calendar_reminders.py --help
```

### Setup: Erinnerungen hinzufügen
```bash
# Interaktiv
python calendar_reminders.py add-reminder

# CLI
python calendar_reminders.py add "Zahnarzt" "14.01.2025 14:00"
```

### Unterstützte Formate
```python
# Deutsch
"Freitag 14:00"
"25.12 14:00"
"25.12.2025 14:00"
"14:00 heute"

# Englisch
"Friday 2pm"
"Jan 25 2:00 PM"
"Today at 14:00"

# Flexibel
"in 30 minutes"
"tomorrow 14:00"
```

### Reminder Types
```python
# One-Time Reminder
reminder.add_reminder("Zahnarzt", "25.12 14:00", type="once")

# Daily Reminder
reminder.add_reminder("Wasser trinken", "09:00", type="daily")

# Weekly
reminder.add_reminder("Freitag Gym", "Freitag 18:00", type="weekly")
```

### Daemon starten
```bash
# Hintergrund - prüft alle 5 Minuten
python calendar_reminders.py daemon &

# Vordergrund mit kurz. Intervall (zum Testen)
python calendar_reminders.py daemon --interval 10
```

### Integration in moloch.py
```python
from calendar_reminders import CalendarReminders

cal = CalendarReminders()

# Erinnerung hinzufügen
cal.add_reminder("Anrufen", "17:00 heute")

# Daemon starten
cal.start_daemon(interval=300)  # 5 Min

# Alle Reminders anzeigen
for reminder in cal.get_all_reminders():
    print(f"⏰ {reminder['text']} at {reminder['time']}")

# Dashboard
cal.display_dashboard()
```

### Google Calendar Integration
```python
# Setup (optional)
cal.setup_google_calendar(
    credentials_file="google_credentials.json"
)

# Sync mit Google
cal.sync_to_google()
```

---

## ☀️ 3. Weather Awareness (`weather_aware.py`)

### Installation
```bash
# Kein API Key nötig! (Open-Meteo ist kostenlos)
python weather_aware.py --help
```

### Setup: Location (optional)
```json
{
  "location": {
    "name": "Berlin",
    "lat": 52.52,
    "lon": 13.40
  },
  "cache": {
    "enabled": true,
    "ttl": 1800
  }
}
```

### Daemon starten
```bash
# Updates alle 30 Min
python weather_aware.py daemon &

# Test Mode (kurze Intervalle)
python weather_aware.py daemon --interval 60
```

### Commands
```bash
# Aktuelle Wetter
python weather_aware.py current

# 7-Tage Vorhersage
python weather_aware.py forecast

# Dashboard
python weather_aware.py dashboard

# Stats
python weather_aware.py stats
```

### Personality Mapping
```python
weather = WeatherAwareness()

# Automatisch bestimmt:
# Sonnig + Warm (>20°C) → Pumuckl (frech)
# Regen + Kalt (<15°C) → HAL (professionell)
# Gewitter (Code 95+) → MAX HEADROOM (cyberpunk!)
# Kalt (<5°C) → Cozy Mood

personality = weather.get_personality_by_weather()
mood_bonus = weather.get_mood_bonus()
```

### Integration in moloch.py
```python
from weather_aware import WeatherAwareness

weather = WeatherAwareness()

# Hole aktuelle Bedingungen
current = weather.fetch_weather()
print(f"🌡️  {current['temp']}°C, {current['description']}")

# Personality anpassen
personality = weather.get_personality_by_weather()
print(f"🎭 Personality: {personality}")

# Daemon
weather.start_daemon()

# Dashboard
weather.display_dashboard()
```

---

## 📋 4. Clipboard Monitor (`clipboard_monitor.py`)

### Installation
```bash
python clipboard_monitor.py --help
```

### Daemon starten
```bash
# Prüft Clipboard alle 3 Sekunden
python clipboard_monitor.py daemon

# Mit kunst. Intervall
python clipboard_monitor.py daemon --interval 5
```

### Commands
```bash
# History (letzte 10)
python clipboard_monitor.py history -n 20

# Statistiken
python clipboard_monitor.py stats

# Dashboard
python clipboard_monitor.py dashboard

# Test (test verschiedene Typen)
python clipboard_monitor.py test
```

### Erkannte Pattern
```
✅ URLs
   https://example.com/page

✅ Emails
   support@example.com

✅ Telefonnummern
   +49 123 456789

✅ Code
   def hello():
       print('world')

✅ Markdown
   # Header
   - List
```

### Konfiguration
```json
{
  "enabled": true,
  "check_interval": 3,
  "auto_actions": {
    "url": true,
    "email": true,
    "phone": true
  },
  "filters": {
    "min_length": 3,
    "ignore_duplicates": true
  }
}
```

### Integration in moloch.py
```python
from clipboard_monitor import ClipboardMonitor

clip = ClipboardMonitor()

# Daemon
clip.daemon_loop(interval=3)

# Oder via Thread
thread = clip.start_daemon(interval=3)

# History anschauen
for entry in clip.get_history(limit=5):
    print(f"{entry['type']}: {entry['preview']}")

# Stats
stats = clip.get_stats()
print(f"Total items: {stats['total_items']}")
```

---

## 🎵 5. Music Recognition (`music_recognition.py`)

### Installation
```bash
# Benötigte Tools:
apt install chromaprint ffmpeg

# Python Module:
pip install -r requirements.txt

# Testen:
python music_recognition.py recognize --duration 10
```

### Daemon starten
```bash
# Nimmt alle 30s Audio auf, versucht zu erkennen
python music_recognition.py daemon

# Mit Custom Intervall
python music_recognition.py daemon --duration 5
```

### Commands
```bash
# Einen Song erkennen
python music_recognition.py recognize --duration 10

# Audio-Datei analysieren
python music_recognition.py recognize --file /path/to/song.mp3

# History
python music_recognition.py history

# Dashboard
python music_recognition.py dashboard

# Stats
python music_recognition.py stats
```

### Konfiguration
```json
{
  "backend": "acoustid",
  "min_confidence": 0.8,
  "spotify_integration": false,
  "cache_results": true
}
```

### Integration in moloch.py
```python
from music_recognition import MusicRecognition

music = MusicRecognition()

# Song erkennen
song = music.recognize_music(duration=10)
if song:
    print(f"🎵 {song['title']} by {song['artists']}")

# Daemon
music.daemon_loop()

# History
recent = music.get_history(limit=10)

# Stats
stats = music.get_stats()
print(f"Songs recognized: {stats['total_songs']}")
```

---

## 🔗 Integration mit moloch.py

### Alle Daemons parallel starten
```python
# In moloch.py add:

from location_aware import LocationAwareness
from calendar_reminders import CalendarReminders
from weather_aware import WeatherAwareness
from clipboard_monitor import ClipboardMonitor
from music_recognition import MusicRecognition

def start_phase4_daemons():
    """Starte alle Phase 4 Features"""
    
    print("🚀 Starte Phase 4 Daemons...")
    
    # Location
    loc = LocationAwareness()
    loc_thread = loc.start_daemon()
    
    # Calendar
    cal = CalendarReminders()
    cal_thread = cal.start_daemon()
    
    # Weather
    weather = WeatherAwareness()
    weather_thread = weather.start_daemon()
    
    # Clipboard
    clip = ClipboardMonitor()
    clip_thread = clip.start_daemon()
    
    # Music
    music = MusicRecognition()
    music_thread = Thread(target=music.daemon_loop, daemon=True)
    music_thread.start()
    
    print("✅ Alle Phase 4 Daemons aktiv!")
    
    return {
        'location': loc_thread,
        'calendar': cal_thread,
        'weather': weather_thread,
        'clipboard': clip_thread,
        'music': music_thread
    }

# Während Startup aufrufen:
if __name__ == "__main__":
    daemons = start_phase4_daemons()
    # ... rest of code
```

### Mit Personality Integration
```python
def adapt_personality_phase4():
    """Adaptive Personality basierend auf Phase 4 Input"""
    
    # Hole aktuelle Bedingungen
    weather = WeatherAwareness()
    loc = LocationAwareness()
    
    # Bestimme beste Personality
    personality = "pumuckl"  # default
    
    # Wetter-Priorität (höher)
    weather_personality = weather.get_personality_by_weather()
    if weather_personality:
        personality = weather_personality
    
    # Location-Priorität (höher)
    location = loc.detect_current_location()
    if location:
        personality = loc.config[location]['personality']
    
    # Setze Personality
    set_personality(personality)
```

---

## 📊 Monitoring & Logs

### Log Files
```
~/.moloch/location_aware.log
~/.moloch/calendar_reminders.log
~/.moloch/weather_aware.log
~/.moloch/clipboard_monitor.log
~/.moloch/music_recognition.log
```

### Dashboards anschauen
```bash
python location_aware.py dashboard
python calendar_reminders.py dashboard
python weather_aware.py dashboard
python clipboard_monitor.py dashboard
python music_recognition.py dashboard
```

---

## 📱 Termux (Smartphone) Deployment

Diese Anleitung beschreibt, wie du die Phase‑4 Daemons direkt auf deinem Android‑Smartphone unter Termux laufen lässt.

Vorbereitung (einmalig)
```bash
# 1) Termux App installieren (Play Store / F‑Droid)
pkg update && pkg upgrade -y

# 2) Wichtige Pakete
pkg install python ffmpeg git termux-api -y

# 3) Optional (für Musik-Fingerprinting)
pkg install chromaprint -y   # liefert fpcalc

# 4) Repository auf das Telefon bringen (git clone oder rclone)
cd $HOME
git clone <your-repo-url> moloch
cd moloch

# 5) Python-Abhängigkeiten
pip install --upgrade pip
pip install -r requirements.txt
```

Wrapper starten (empfohlen)
```bash
cd ~/moloch
chmod +x daemon_wrappers/*.sh

# Starte alle Daemons im Hintergrund (nohup erlaubt log-Weiterleitung)
nohup bash daemon_wrappers/run_location.sh >/dev/null 2>&1 &
nohup bash daemon_wrappers/run_calendar.sh >/dev/null 2>&1 &
nohup bash daemon_wrappers/run_weather.sh >/dev/null 2>&1 &
nohup bash daemon_wrappers/run_clipboard.sh >/dev/null 2>&1 &
nohup bash daemon_wrappers/run_music.sh >/dev/null 2>&1 &

# Prüfe laufende Prozesse
ps aux | grep python
```

Logs & Keep-Alive
```bash
# Log-Dateien befinden sich in ~/.moloch
ls -la ~/.moloch
tail -f ~/.moloch/weather_daemon.log

# Verhindere, dass Android den Prozess tötet
termux-wake-lock

# Optional: Termux:Boot nutzen, damit die Wrapper beim Booten starten
# Installiere Termux:Boot aus F‑Droid, lege Shortcut in ~/.termux/boot/
mkdir -p ~/.termux/boot
cp daemon_wrappers/run_weather.sh ~/.termux/boot/
# (Passe ggf. an: Wrapper starten mit nohup)
```

Debugging Hinweise
- Wenn `termux-clipboard-get` fehlt, installiere `termux-api` und erlaube Berechtigungen.
- Wenn `fpcalc` nicht gefunden wird, installiere `chromaprint`.
- Prüfe Permissions: `termux-setup-storage` falls Dateizugriff nötig.

Sichere Deinstallation
```bash
# Stoppe Wrapper-Prozesse (finde PIDs via ps/pgrep)
pkill -f run_weather.sh || true
pkill -f run_clipboard.sh || true

# Entferne Logs / Configs
rm -rf ~/.moloch
```


## 🐛 Troubleshooting

### "GPS nicht verfügbar"
```bash
# Prüfe Termux API Installation
pkg install termux-api

# Prüfe Permission
echo "Termux API Test:" $(termux-location)
```

### "Musik nicht erkannt"
```bash
# Stelle sicher dass fpcalc installiert ist
fpcalc --version

# Bzw. chromaprint
apt install chromaprint
```

### "Clipboard funktioniert nicht"
```bash
# Termux Clipboard API testen
termux-clipboard-get
termux-clipboard-set "Test"
```

### "Wetter zeigt falsche Location"
```bash
# Konfigurationsdatei prüfen
cat ~/.moloch/weather.json

# Neue Location setzen
python weather_aware.py --lat 52.52 --lon 13.40
```

---

## 📈 Performance Tips

| Feature | Intervall | Impact |
|---------|-----------|--------|
| Location | 30-60s | Low (GPS ca. 5 Sec) |
| Calendar | 300s (5m) | Low (Nur Check) |
| Weather | 1800s (30m) | Low (HTTP Cache) |
| Clipboard | 3-5s | Low (In-Memory) |
| Music | 30s+ | High (Audio Processing) |

**Empfehlung**: Music Recognition separaten Thread, andere parallel.

---

## 🎯 Next Steps

- [ ] NFC Tag Actions
- [ ] Multi-Widget Dashboard
- [ ] Offline LLM Mode
- [ ] Voice Profiling & Recognition
- [ ] Advanced Analytics

---

**Status**: Phase 4 Complete ✅
**Version**: M.O.L.O.C.H. v3.0+
**Last Updated**: 2025-12-15
