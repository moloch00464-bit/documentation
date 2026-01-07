# 📱 M.O.L.O.C.H. v3.0 - TERMUX SMARTPHONE DEPLOYMENT GUIDE

## 🤖 Übersicht

M.O.L.O.C.H. v3.0 läuft jetzt auf Ihrem Android-Smartphone! Dieser Guide zeigt die Installation und Nutzung auf **Termux** (Terminal-Emulator für Android).

### Was ist Termux?
- **Kostenlos** auf Google Play Store
- Terminal-Emulator für Android
- Python, Git, Build-Tools, alles nativ
- Root nicht erforderlich
- Vollständige Linux-Umgebung

---

## ⚡ Schnell-Start (5 Minuten)

### 1️⃣ Termux installieren
1. Google Play Store → "Termux" suchen
2. **Von der offiziellen Termux-Organisation** installieren (nicht Termux:Styling etc.)
3. App öffnen

### 2️⃣ Setup-Skript ausführen

```bash
# Klone das Repo oder lade setup-termux.sh herunter
curl -L https://[YOUR-REPO]/setup-termux.sh -o setup-termux.sh
bash setup-termux.sh
```

Das Skript installiert automatisch:
- ✅ Python 3.x
- ✅ ffmpeg, tesseract, git
- ✅ Alle Python-Abhängigkeiten
- ✅ M.O.L.O.C.H. Verzeichnis (~/.moloch)
- ✅ Daemon-Wrapper-Skripte

### 3️⃣ M.O.L.O.C.H. starten

```bash
# Hauptprogramm
python ~/.moloch/moloch.py

# Oder einzelne Module testen:
python ~/.moloch/clipboard_monitor.py --current
python ~/.moloch/location_aware.py --current
python ~/.moloch/weather_aware.py --current
```

---

## 📋 Detaillierte Installation

### Manuelle Installation

Falls das automatische Skript fehlschlägt:

```bash
# 1. System aktualisieren
pkg update
pkg upgrade -y

# 2. Abhängigkeiten installieren
pkg install -y python ffmpeg tesseract git curl jq

# 3. Verzeichnis erstellen
mkdir -p ~/.moloch/{brain,logs,gehirn,kontext,history,config,audio}

# 4. Python-Pakete installieren
pip install --upgrade pip
pip install -r requirements.txt
```

### Termux Storage-Zugriff erlauben

Für Zugriff auf Fotos, Downloads etc.:

```bash
# Wird normalerweise beim ersten Start abgefragt
termux-setup-storage

# Dann können Sie auf External Storage zugreifen:
cd ~/storage/pictures   # Fotos
cd ~/storage/downloads  # Downloads
```

---

## 🎯 Praktische Nutzung

### Phase 4 Module einzeln testen

#### 📋 Clipboard Monitor
```bash
python ~/.moloch/clipboard_monitor.py --current
# Zeigt aktuellen Clipboard-Inhalt

python ~/.moloch/clipboard_monitor.py --daemon
# Überwacht Clipboard-Änderungen im Hintergrund
```

#### 🗺️ Location Aware
```bash
python ~/.moloch/location_aware.py --current
# Zeigt aktuellen Standort (GPS oder IP-Fallback)

python ~/.moloch/location_aware.py --add home "Wohnzimmer"
# Speichert Wohnort für Geofencing

python ~/.moloch/location_aware.py --daemon
# Aktiviert Geofencing (Persönlichkeit ändert sich mit Ort)
```

#### 🌦️ Weather Aware
```bash
python ~/.moloch/weather_aware.py --current
# Aktuelles Wetter

python ~/.moloch/weather_aware.py --forecast
# 7-Tage-Vorhersage

python ~/.moloch/weather_aware.py --daemon
# Hintergrund-Monitor (Wetter ändert Stimmung)
```

#### 📅 Calendar & Reminders
```bash
python ~/.moloch/calendar_reminders.py --today
# Heutige Termine

python ~/.moloch/calendar_reminders.py --add "Zahnarzt" "14:00 Freitag"
# Termin hinzufügen

python ~/.moloch/calendar_reminders.py --daemon
# Automatische Erinnerungen
```

#### 🎵 Music Recognition
```bash
python ~/.moloch/music_recognition.py --recognize
# Stellt Musik ein und erkennt sie (via AcoustID)

python ~/.moloch/music_recognition.py --daemon
# Hintergrund-Musikerkennung
```

---

## 🚀 Daemon-Betrieb (Keep-Alive)

Starten Sie Module als Hintergrund-Daemons:

```bash
# Einzeln starten
bash ~/.moloch/daemon_wrappers/start-clipboard.sh
bash ~/.moloch/daemon_wrappers/start-location.sh
bash ~/.moloch/daemon_wrappers/start-weather.sh

# Status prüfen
ps aux | grep moloch

# Logs anschauen
tail -f ~/.moloch/daemon_logs/clipboard.log
tail -f ~/.moloch/daemon_logs/location.log
```

### Keep-Alive Script (Alle Daemons starten)

Erstelle `~/.moloch/start_all_daemons.sh`:

```bash
#!/data/data/com.termux/files/usr/bin/bash
# Starte alle M.O.L.O.C.H. Daemons

echo "🤖 Starte M.O.L.O.C.H. Daemons..."

for script in ~/.moloch/daemon_wrappers/start-*.sh; do
    echo "  ▶️ $(basename $script)"
    bash "$script" &
    sleep 2
done

echo "✅ Alle Daemons gestartet!"
ps aux | grep moloch | grep -v grep
```

Dann ausführbar machen und starten:
```bash
chmod +x ~/.moloch/start_all_daemons.sh
bash ~/.moloch/start_all_daemons.sh
```

---

## 🔧 Konfiguration

### Hauptkonfiguration: ~/.moloch/config/moloch.json

```json
{
  "personality": "moloch",
  "voice": {
    "tts_engine": "edge-tts",
    "voice": "en-US-JennyNeural",
    "speed": 1.0,
    "language": "en-US"
  },
  "location": {
    "mode": "gps",
    "latitude": 52.5200,
    "longitude": 13.4050,
    "geofence_radius": 500
  },
  "phone": {
    "is_termux": true,
    "battery_mode": "aggressive",
    "low_power_threshold": 20
  },
  "logging": {
    "level": "INFO",
    "file": "~/.moloch/logs/moloch.log"
  }
}
```

### Locations: ~/.moloch/locations.json

```json
{
  "locations": {
    "home": {
      "name": "Wohnzimmer",
      "lat": 52.5200,
      "lon": 13.4050,
      "personality": "pumuckl",
      "emoji": "🏠"
    },
    "work": {
      "name": "Büro",
      "lat": 52.5201,
      "lon": 13.4051,
      "personality": "hal",
      "emoji": "💼"
    }
  }
}
```

---

## 🔐 Berechtigungen

M.O.L.O.C.H. benötigt folgende Android-Berechtigungen:

| Feature | Berechtigung | Status |
|---------|-------------|--------|
| 📋 Clipboard | - | ✅ Keine spezial |
| 🗺️ Standort | Location (GPS) | ⚠️ Manuell aktivieren |
| 🎤 Spracheingabe | Microphone | ⚠️ Beim Start abfragen |
| 📷 Webcam | Camera | ⚠️ Nur für Face-Rec |
| 🔊 Audio-Ausgabe | - | ✅ Standard |
| 📱 Speicher | Storage | ⚠️ termux-setup-storage |

**Wie aktivieren:**
1. Android Settings → Apps → Termux
2. Permissions → Location, Microphone, Camera
3. Alle auf "Allow while using app" setzen

---

## 🐛 Troubleshooting

### Problem: Python Module nicht gefunden

```bash
pip list  # Zeige installierte Pakete
pip install -r requirements.txt  # Neu installieren
```

### Problem: Tesseract OCR nicht gefunden

```bash
pkg install tesseract  # CLI-Tool installieren
python ~/.moloch/camera_ocr.py --test  # Test
```

### Problem: Kein Audio-Ein-/Ausgabe

```bash
# Audio-Geräte prüfen
termux-mic-record --help
termux-media-player --help

# ffmpeg testen
ffmpeg -f lavfi -i anullsrc=r=44100:cl=mono -t 1 test.wav
```

### Problem: GPS funktioniert nicht

```bash
# Standortdienste prüfen
termux-location

# Fallback auf IP-Geolocation
python ~/.moloch/location_aware.py --mode ip
```

### Problem: Daemons starten nicht

```bash
# Prüfe Logs
tail -100 ~/.moloch/daemon_logs/*.log

# Prüfe Prozesse
ps aux | grep python

# Manuell starten zum Debuggen
python ~/.moloch/clipboard_monitor.py --daemon
```

---

## 📊 Performance-Tipps

### Speicher sparen (Low-End Phones)

```bash
# Nur leichte Module starten
python ~/.moloch/weather_aware.py --daemon
python ~/.moloch/location_aware.py --daemon

# Nicht starten (speicherhungrig):
# - face_recognition
# - music_recognition (ohne ffmpeg)
```

### Batterie sparen

```json
// In config/moloch.json
{
  "phone": {
    "battery_aware": true,
    "low_power_threshold": 25,
    "aggressive_cache": true
  },
  "update_interval": 300  // 5 Minuten statt 1 Minute
}
```

### Netzwerk optimieren

```bash
# WiFi bevorzugen
echo "wifi_only=true" >> ~/.moloch/config/network.json

# Daten-Volumen reduzieren
python ~/.moloch/weather_aware.py --cache 3600  # 1h Cache
```

---

## 🔄 Updates

### M.O.L.O.C.H. aktualisieren

```bash
cd ~/.moloch
git pull origin main

# Neue Dependencies?
pip install -r requirements.txt --upgrade
```

### Termux System aktualisieren

```bash
pkg update
pkg upgrade -y
```

---

## 📚 Weitere Ressourcen

- **Termux Wiki:** https://wiki.termux.com
- **Termux API:** https://wiki.termux.com/wiki/Termux:API
- **M.O.L.O.C.H. Repo:** https://[YOUR-REPO]
- **Python auf Android:** https://chaquo.com/chaquopy/

---

## 📞 Support

Bei Problemen:

1. Checke die Logs:
   ```bash
   tail -50 ~/.moloch/logs/moloch.log
   ```

2. Teste einzelnes Modul:
   ```bash
   python ~/.moloch/weather_aware.py --help
   ```

3. Überprüfe Dependencies:
   ```bash
   pip list | grep -E "edge-tts|requests|opencv"
   ```

4. Melde einen Issue mit:
   - Termux-Version
   - Android-Version
   - Fehlerausgabe (kompletter Log)

---

**🚀 Viel Spaß mit M.O.L.O.C.H. auf Ihrem Smartphone!**
