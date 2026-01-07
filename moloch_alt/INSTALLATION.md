# M.O.L.O.C.H. Installation Guide

Kompletter Setup für Android Termux oder Desktop Development

## 🚀 Quick Start (5 Minuten)

### 1. Termux Basis-Setup

```bash
# Update Package Manager
pkg update && pkg upgrade -y

# Installiere Python 3 + Git
pkg install python git termux-api termux-tools

# Clone M.O.L.O.C.H.
cd ~
git clone <repo-url> moloch
cd moloch

# Installiere Python Dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

### 2. Claude API Key

```bash
# Option A: Direkt in moloch.py (Zeile ~20)
nano moloch.py
# Suche: ANTHROPIC_API_KEY = "sk-..."
# Setze deinen Key

# Option B: Environment Variable
export ANTHROPIC_API_KEY="sk-..."

# Option C: .env Datei (wenn python-dotenv installiert)
echo 'ANTHROPIC_API_KEY="sk-..."' > ~/.moloch/.env
```

**Key bekommen:**
1. Gehe zu: https://console.anthropic.com/account/keys
2. Erstelle neuen Key
3. Setze 100,000 token/min Limit (kostenlos 5M token/Monat)

### 3. Test

```bash
# Einfacher Test
python moloch.py "Hallo Moloch"

# Voice Input Test
python voice_input.py
# → Sprich etwas, 1.5s Pause → AI antwortet → TTS spricht

# Fertig! ✅
```

---

## 📦 Vollständiger Setup (Alle Features)

### Phase 1: TTS & Voice (Kern)

```bash
# Installation
pip install edge-tts

# Test
python tts_test.py

# Lautstärke setzen
python set_volume.py 12

# Voice Input testen
python voice_input.py
```

### Phase 2: Android Integration

#### Hotword Detection

```bash
# Option 1: Porcupine (kostenlos, 30s/min)
pip install pvporcupine

# Setup
python hotword_listener.py --setup
# → Gehe zu: https://picovoice.ai/console
# → Copy Access Key
# → Paste im Terminal

# Daemon starten
python hotword_listener.py --daemon

# Option 2: Snowboy (besser, mehr Aufwand)
# TBD - Siehe ALTERNATIVE.md
```

#### Share Intent Integration

```bash
# Installation
# (Keine zusätzliche Installation nötig)

# Tasker Setup notwendig:
# 1. Öffne Tasker
# 2. Create Profile → Event → Intent
# 3. Action: am broadcast intent=android.intent.action.SEND
# 4. Task: Run Shell → termux-open 'moloch://share?text=%CLIP'
```

#### Battery Smart Mode

```bash
# Installation
# (Nutzt termux-battery-status)

# Test
python battery_smart.py --status

# Daemon
python battery_smart.py --daemon
```

### Phase 3: Vision & Content

#### OCR Setup

```bash
# Tesseract Binary installieren
pkg install tesseract tesseract-data-deu tesseract-data-eng

# Python OCR Library
pip install pytesseract pillow

# Test
python camera_ocr.py --screenshot
```

#### Spotify Integration

```bash
# Installation
pip install spotipy

# Setup
python spotify_control.py --setup
# → https://developer.spotify.com/dashboard
# → Create App
# → Client ID + Secret kopieren
# → Redirect URI: http://localhost:8888/callback

# Browser öffnet automatisch → Authorize
# → Code kopieren → Paste im Terminal

# Musik spielen
python spotify_control.py play "Dua Lipa"
```

#### Notification Reader

```bash
# Installation
# (Nutzt Android Notifications)

# Test
python notification_reader.py --daemon

# Filter konfigurieren
python notification_reader.py --filter
```

---

## 🧠 Brain Backup

### Google Drive Sync

```bash
# rclone installieren
pkg install rclone

# Konfigurieren
rclone config

# Schritte:
# 1. n (new remote)
# 2. Name: gdrive
# 3. Storage type: google drive
# 4. Client ID: (leave empty)
# 5. Follow OAuth flow
# 6. Authenticate im Browser

# Test
python brain_backup.py --daemon 3600
# → Backup jede Stunde zum Google Drive
```

---

## 🎭 Personality & Watch Mode

### Smartwatch UI (Fitbit, WearOS)

```bash
# Basis
python watch_ui.py

# Pumuckl Modus
python watch_ui.py --personality pumuckl

# Max Headroom
python max_headroom.py --live

# HAL 9000 Eye
python hal_eye.py --boot
```

---

## 🎮 Tasker Widgets

### Widget 1: Volume Control

```
Task: MOLOCH_Volume_Up
  → Run Shell: python ~/moloch/set_volume.py up

Task: MOLOCH_Volume_Down
  → Run Shell: python ~/moloch/set_volume.py down

Task: MOLOCH_Voice_Input
  → Run Shell: python ~/moloch/voice_input.py && termux-vibrate 100
```

**Home Screen Widget:**
1. Long Press Home → Widgets
2. Tasker Widget → Select Task
3. Choose: MOLOCH_Volume_Up / MOLOCH_Voice_Input

---

## ⚙️ Konfiguration

### moloch.py (Main Config)

```python
# Zeile ~20-30
ANTHROPIC_API_KEY = "sk-..."  # Claude API
TTS_VOICE = "en-US-JennyNeural"  # oder en-US-AriaNeural
MOLOCH_VOLUME = 10            # 0-15
```

### Config Dateien

```
~/moloch/
├── battery_config.json       # Battery Sparmodus
├── spotify_config.json       # Spotify OAuth Tokens
├── hotword_config.json       # Hotword Settings
├── ocr_config.json          # OCR Language + Settings
├── notification_filter.json # Notification Filter
└── brain/                   # Brain Storage
    ├── langzeit.json       # Long-term Memory
    └── history.json        # Chat History
```

---

## 🔧 Troubleshooting

### ❌ TTS funktioniert nicht

```bash
# Check Audioplayer
which ffplay          # oder: which mpv
which termux-media-player

# Fallback prüfen
python -c "import subprocess; subprocess.run(['termux-media-player', 'play', 'ohr.mp3'])"

# Manueller Test
echo "Test" | termux-tts-speak
```

### ❌ Voice Input Error

```bash
# Mikrofon prüfen
termux-microphone-record -f test.wav -d 5

# Whisper testen
whisper test.wav --language en

# Audio Level checken
pkg install sox
sox test.wav -n stat
```

### ❌ Claude API Fehler

```bash
# API Key validieren
python -c "
import anthropic
client = anthropic.Anthropic()
print(client.models.list())
"

# Error Logs
tail -f ~/moloch/brain/logs/*.txt
```

### ❌ Tesseract nicht gefunden

```bash
# Installation
pkg install tesseract tesseract-data-deu

# Path setzen
export TESSDATA_PREFIX=/data/data/com.termux/files/usr/share/tessdata

# Test
tesseract --version
```

---

## 📱 Android Permissions

Folgende Berechtigungen braucht M.O.L.O.C.H.:

1. **Microphone** (Sprachaufnahme)
   - Settings → Apps → Termux → Permissions → Microphone

2. **Camera** (OCR, Face Recognition)
   - Settings → Apps → Termux → Permissions → Camera

3. **Storage** (Brain Backup, Dateien)
   - Settings → Apps → Termux → Permissions → Storage

4. **Notification Access** (Notification Reader)
   - Settings → Accessibility → Notification Reader

### Tasker Setup

```bash
# Tasker Berechtigungen
adb shell pm grant net.dinglisch.android.taskerm android.permission.RECEIVE_BOOT_COMPLETED
adb shell pm grant net.dinglisch.android.taskerm android.permission.RECORD_AUDIO
```

---

## 🚀 Autostart bei Boot

### Option 1: Tasker Profile

```
Trigger: Device Boot
Task: Start MOLOCH Daemon
  → Run Shell:
    nohup python ~/moloch/hotword_listener.py --daemon &
    nohup python ~/moloch/battery_smart.py --daemon &
    nohup python ~/moloch/notification_reader.py --daemon &
```

### Option 2: cron Job

```bash
# Installiere cronie
pkg install cronie

# Edit crontab
crontab -e

# Füge hinzu:
@reboot nohup python ~/moloch/hotword_listener.py --daemon > /dev/null 2>&1 &
@reboot nohup python ~/moloch/battery_smart.py --daemon > /dev/null 2>&1 &
```

---

## 💾 Backup & Restore

### Manuelles Backup

```bash
# Erstelle Backup
python brain_backup.py

# Liste Backups
python brain_backup.py --list

# Restore
python brain_backup.py --restore 20251215_092900
```

### Automatisches Backup

```bash
# Google Drive Daemon
python brain_backup.py --daemon 3600

# Checke Status
ls -lah ~/moloch/backups/
rclone ls gdrive:M.O.L.O.C.H./Brain\ Backups
```

---

## 📊 Performance

### Sparmodus aktivieren (low battery)

```bash
python battery_smart.py --savemode on

# Deaktivieren
python battery_smart.py --savemode off
```

### Daemon Monitoring

```bash
# Check active processes
ps aux | grep moloch

# Logs
tail -f ~/moloch/brain/logs/*.txt

# Activity Monitor
top -p $(pgrep -f moloch | paste -sd, -)
```

---

## 🎓 Learning Path

1. **Tag 1:** Basis Setup + Voice Input Test
2. **Tag 2:** TTS Stimme konfigurieren + Volume Widget
3. **Tag 3:** Hotword Detection + Daemon
4. **Tag 4:** Spotify Control + Notifications
5. **Tag 5:** OCR + Brain Backup
6. **Week 2+:** Fine-Tuning & Custom Commands

---

## 📚 Weitere Ressourcen

- **README.md** — Feature Übersicht
- **ARCHITECTURE.md** — Code Structure
- **API_REFERENCE.md** — Function Docs
- **TROUBLESHOOTING.md** — Häufige Probleme
- **CUSTOMIZATION.md** — Custom Prompts & Personalities

---

## 💬 Support

Fehler? Fragen?

```bash
# Debug Mode
python moloch.py --debug

# Logs checken
cat ~/moloch/brain/logs/latest.txt

# Error Reporting
# GitHub Issues → include logs
```

---

**Installation Status:** ✅ Complete
**Last Updated:** 2025-12-15
**Version:** 3.0
