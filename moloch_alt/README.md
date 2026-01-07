# M.O.L.O.C.H. - Mobile AI Assistant für Termux
**Intelligente Android-KI mit Sprachsteuerung, Sehen, Hören & Lernen**

> *"Hallo Moloch. Können wir reden?"* 🤖

## Features Übersicht

### ✅ Phase 1: Kern Funktionalität
- **TTS**: edge-tts mit en-US-JennyNeural (weiblich, natürlich)
- **STT**: Whisper mit Auto-Stop (1.5s Stille)
- **Volume Control**: 0-15 Skala mit Widgets
- **Brain Backup**: Google Drive Sync mit Kompressi​on

### ✅ Phase 2: Interaktion & Kontext
- **Hotword Detection**: "Hey Moloch" mit Porcupine/Snowboy
- **Share Intent**: Android Apps teilen Text/Links/Dateien
- **Battery Smart**: Automatischer Sparmodus <20%
- **Pumuckl Interface**: Frech-frecher Kobold Modus

### ✅ Phase 3: Vision & Content
- **OCR**: Screenshot-Analyse, Real-time Kamera
- **Spotify Control**: Musik spielen, nächster Track
- **Notification Reader**: Benachrichtigungen vorlesen

### 🧠 Self-Awareness System
- **Auto-Detection**: Erkennt 23+ Module beim Start
- **Awakening Sequence**: Dramatische Initialisierung mit TTS
- **Consciousness State**: Speichert Bewusstsein in Brain

### ⚡ Phase 4: Adaptive Intelligenz
- **Location Awareness**: GPS-Geofencing mit Personality-Wechsel
  - Zuhause = Pumuckl (frech)
  - Arbeit = HAL (professionell)
  - Gym = HAL (fokussiert)
- **Calendar & Reminders**: Termine, Events, Erinnerungen
  - Natural Language Datum-Parsing
  - Google Calendar Integration (optional)
  - Auto-Reminders 1h vorher
- **Weather Awareness**: Wetter-abhängige Anpassungen
  - Open-Meteo API (kostenlos!)
  - Personality nach Wetter (Sonnenschein = frech, Regen = melancholisch)
  - 7-Tage Vorhersage
- **Clipboard Monitor**: Intelligente Zwischenablage
  - URL, Email, Phone Erkennung
  - Code/Markdown Detection
  - History & Analytics
- **Music Recognition**: Musik-Erkennung
  - AcoustID Fingerprinting
  - MusicBrainz Integration
  - Spotify Integration (optional)

### 🎬 Bonus Features
- **Face Recognition**: Gesichtserkennung für Arbeitsplatz-Tracking
- **Max Headroom Mode**: 80s Cyberpunk Interface
- **HAL 9000 Eye**: Red Pulsing Monitor

## Quick Start

### 1. Installation

```bash
cd ~/moloch
pip install --upgrade pip
pip install -r requirements.txt

# Optional: Tesseract für OCR
pkg install tesseract
```

### 2. Setup & Konfiguration

```bash
# TTS Stimme (default: en-US-JennyNeural)
export TTS_VOICE=en-US-JennyNeural

# Volumen (0-15)
export MOLOCH_VOLUME=10

# Claude API Key (falls nicht in moloch.py)
export ANTHROPIC_API_KEY="your-key-here"
```

### 3. Basis-Tests

```bash
# Voice Input → Claude → TTS
python voice_input.py

# Nur Sprachausgabe testen
python moloch.py "Hallo Welt"

# Smartwatch UI (Kompakt-Modus)
python watch_ui.py
```

## Feature Details

### 🎤 Voice Input (STT)

Automatische Spracherkennung mit intelligentim Stop:

```bash
python voice_input.py
# Sprich... [Erkennt automatisch bei 1.5s Stille]
```

**Features:**
- Auto-Stop bei Stille (1.5s timeout)
- Whisper Transkription
- Claude Antwort
- TTS Wiedergabe
- Brain-Speicherung

### 🔊 TTS & Lautstärke

```bash
# Volume direkt setzen
python set_volume.py 12

# Schnelle Änderung
python set_volume.py up      # +2
python set_volume.py down    # -2
python set_volume.py max     # 15
```

### 🎵 Spotify Control

```bash
# Setup (OAuth)
python spotify_control.py --setup

# Musik spielen
python spotify_control.py play "Sierra Leone"
python spotify_control.py play:playlist "Lo-Fi Beats"
python spotify_control.py play:album "OK Computer"

# Kontrolle
python spotify_control.py next
python spotify_control.py previous
python spotify_control.py pause
python spotify_control.py volume 80
python spotify_control.py now     # Aktueller Song
```

### 🎤 Hotword Detection

Always-listening "Hey Moloch" Aktivierung:

```bash
# Setup Porcupine (kostenlos, 30s/min)
python hotword_listener.py --setup

# Daemon gestartet
python hotword_listener.py --daemon

# Test
python hotword_listener.py --test
```

**Fähigkeiten:**
- Kontinuierlich im Hintergrund
- Auto-Response nach Erkennung
- Fallback zu Whisper-Analyse

### 📱 Share Intent

Android Apps können direkt an Moloch senden:

```bash
# Text analysieren
python share_handler.py --from-intent "Text zum Analysieren"

# Link verarbeiten
python share_handler.py --link "https://example.com"

# Datei analysieren
python share_handler.py --file "/sdcard/document.txt"

# History anzeigen
python share_handler.py --list
```

**Tasker Integration:**
```
Trigger: Intent android.intent.action.SEND
Action: Call: termux-open 'moloch://share?text=%CLIP'
```

### 📷 OCR & Screenshot Analyse

Text von Bildern & Screenshots lesen:

```bash
# Screenshot machen & OCR
python camera_ocr.py --screenshot

# Datei analysieren
python camera_ocr.py --file /sdcard/DCIM/image.png

# Real-time Kamera
python camera_ocr.py --camera

# Daemon (Screenshots alle 60s)
python camera_ocr.py --daemon 60
```

**Features:**
- Deutsch + Englisch Erkennung
- Auto-Analyse mit Claude
- Sprachausgabe Ergebnisse
- Brain-Speicherung

### 🔋 Battery Smart Mode

Automatischer Sparmodus unter 20% Akku:

```bash
# Prüfe & aktiviere ggf.
python battery_smart.py

# Status
python battery_smart.py --status

# Daemon (check alle 300s)
python battery_smart.py --daemon 300
```

**Sparmodus aktiviert:**
- Reduzierte API Requests
- Längere Timeouts
- Offline Mode für Features

### 📢 Notification Reader

Android Benachrichtigungen vorlesen:

```bash
# Monitor starten
python notification_reader.py

# Liste anzeigen
python notification_reader.py --list

# Clear
python notification_reader.py --clear

# Daemon (check alle 5s)
python notification_reader.py --daemon 5

# Filter konfigurieren
python notification_reader.py --filter
```

**Filter Setup:**
```json
{
  "ignore_apps": ["com.android.systemui"],
  "priority_apps": ["com.whatsapp", "com.telegram.messenger"]
}
```

### 👁️ Gesichtserkennung

Face Recognition für Arbeitsplatz-Tracking:

```bash
# Gesicht registrieren
python face_manager.py register

# Alle Gesichter anzeigen
python face_manager.py list

# Monitoring starten
python face_monitor.py

# PTZ Kamera steuern
python ptz_control.py pan 10
python ptz_control.py zoom 2
```

### 🧠 Brain Backup

Automatische Sicherung ins Google Drive:

```bash
# Backup erstellen
python brain_backup.py

# Google Drive Sync
python brain_backup.py --upload

# Restore
python brain_backup.py --restore 20251214_142934

# Daemon (backup jede Stunde)
python brain_backup.py --daemon 3600

# Liste
python brain_backup.py --list
```

**Google Drive Setup:**
```bash
# Installation
pkg install rclone

# Konfiguration
rclone config

# Remote als 'gdrive' setzen
```

### 🎭 Personalities & Watch Mode

```bash
# Smartwatch UI (kurz & prägnant)
python watch_ui.py

# Pumuckl Kobold Modus (frech)
python moloch.py "Was machst du?" --personality pumuckl

# Max Headroom Cyberpunk
python max_headroom.py --chat

# HAL 9000 Eye Monitor
python hal_eye.py --boot
```

## Tasker Integration

### Widget: Volume Schnell-Zugriff
```
Task: Volume Up/Down
→ Run Shell: python ~/moloch/set_volume.py up
```

### Widget: Voice Input
```
Task: Voice Input
→ Run Shell: python ~/moloch/voice_input.py
→ Vibrate 100ms
```

### Share Intent Handler
```
Trigger: Intent android.intent.action.SEND
→ Run Shell: python ~/moloch/share_handler.py --from-intent "%CLIP"
```

### Hotword Daemon (AutoStart)
```
Profile: Device Boot
→ Task: Start Hotword Listener
  Run Shell: nohup python ~/moloch/hotword_listener.py --daemon &
```

## Requirements

```
edge-tts>=0.2.0          # TTS Synthese
requests>=2.31.0         # HTTP Client
opencv-python>=4.8.0     # Vision/Gesichter
face-recognition>=1.3.5  # Face Encoding
numpy>=1.24.0            # Math/Arrays
Pillow>=10.0.0          # Image Processing
pytesseract>=0.3.10     # OCR
pvporcupine>=2.3.0      # Hotword Detection (optional)
```

## Dateistruktur

```
~/moloch/
├── moloch.py                 # Main AI Engine
├── brain/                    # Brain Storage (JSON)
│   ├── kontext/
│   ├── was/
│   ├── wer/
│   ├── wann/
│   ├── wie/
│   └── wo/
├── config/
│   └── personality.txt
├── history/                  # Chat History
└── backups/                  # Brain Backups
```

## Environment Variables

```bash
# Core
ANTHROPIC_API_KEY=sk-...     # Claude API
TTS_VOICE=en-US-JennyNeural  # TTS Stimme
MOLOCH_VOLUME=10             # 0-15

# Optional
SPOTIFY_CLIENT_ID=...        # Spotify API
SPOTIFY_SECRET=...
PORCUPINE_ACCESS_KEY=...     # Hotword
```

## Troubleshooting

**❌ TTS funktioniert nicht:**
- Check: `which ffplay` oder `which mpv`
- Fallback: `termux-media-player play ohr.mp3`

**❌ Voice Input Fehler:**
- Check Mikrofon: `termux-microphone-record -f test.wav`
- Check Whisper: `whisper test.wav`

**❌ OCR schlechte Ergebnisse:**
- Install Tesseract: `pkg install tesseract`
- Beste: Deutsche + Englisch: `--lang deu+eng`

**❌ Share Intent nicht funktioniert:**
- Aktiviere Tasker: Settings → Tasker
- Gebe Berechtigungen: Notification Access

## API Keys Setup

### Claude (Erforderlich)
1. https://console.anthropic.com/account/keys
2. Copy Key → in `moloch.py` oder ENV

### Spotify (Optional)
1. https://developer.spotify.com/dashboard
2. Create App → Client ID + Secret
3. Redirect URI: `http://localhost:8888/callback`

### Porcupine (Optional)
1. https://picovoice.ai/console/auth/signup
2. Copy Access Key
3. Run: `python hotword_listener.py --setup`

## Support & Bugs

Fehler? Fragen?
```bash
# Check logs
tail -f ~/moloch/brain/logs/*.txt

# Debug Mode
python moloch.py --debug
```

---

**Version:** 3.0 (Phasen 1-3 Complete)
**Status:** Production Ready 🚀
**Last Updated:** 2025-12-15

Tasker-Widget Setup (Android)

1. **Tasker öffnen** → **+ Task erstellen** → z.B. „Moloch Vol Up"
2. **Action:** Code/Shell:
   ```bash
   python ~/moloch/set_volume.py up
   ```
3. **Shortcut-Widget erstellen:**
   - Homescreen → **Widget** → **Tasker** → **Shortcut**
   - Task auswählen (z.B. „Moloch Vol Up")
   - Icon & Label: z.B. 🔊 „Vol +"
4. **Mehrere Buttons:** Gleicher Prozess für `down`, `mute`, `max`

Voice Input (STT) mit Auto-Stop

Sprachsteuerung mit intelligenter Pause-Erkennung:

```bash
python voice_input.py          # Starte Voice-Recording (Auto-Stop bei Stille)
python voice_input.py -v       # Verbose (zeige Zwischenschritte)
```

**Flow:**
1. Script/Button drücken → Recording startet
2. Spreche (max 45s)
3. Nach ~1.5s Stille → Recording stoppt automatisch
4. Whisper transkribiert deinen Text
5. Claude antwortet
6. M.O.L.O.C.H. spricht die Antwort

**Tasker-Widget für Voice Input:**

1. **Tasker** → **+ Task** → „Moloch Voice"
2. **Action:** Shell/Code:
   ```bash
   cd ~/moloch && python voice_input.py
   ```
3. **Homescreen Widget** → Tasker Shortcut
   - Icon: 🎤 oder 🗣️
   - Label: „Moloch Voice"
4. **Einmal tippen** = vollständiger Voice-Austausch (Record → Antwort)

Pumuckl Interface (Smartwatch)

M.O.L.O.C.H. hat eine freche kleine Schwester: **Pumuckl** — ein verspielter Kobold für deine Smartwatch!

**Persönlichkeiten:**
- **HAL** (Standard): Erwachsener KI-Kumpel mit Dark Humor
- **Pumuckl** (Watch): Frecher Kobold, lustig, kurz & prägnant

**Schnelle Watch-Antwort:**

```bash
python watch_ui.py "hey moloch"              # HAL antwortet
python watch_ui.py -p pumuckl "hey kobold"   # Pumuckl antwortet
```

**Watch Voice Input:**

```bash
python watch_ui.py --voice                    # Voice Input (HAL)
python watch_ui.py --voice -p pumuckl         # Voice Input (Pumuckl)
```

**Output für Smartwatch (kompakt):**
```
🤖 Yo, was geht?
👺 Haha! Des schaut gut aus!
```

**Umschalten der Standard-Persönlichkeit:**

```bash
python watch_ui.py -p pumuckl "test"         # Speichert Pumuckl als Standard
python watch_ui.py -p hal "test"             # Zurück zu HAL
```

**Tasker-Widget für Watch (Pumuckl-Mode):**

1. **Tasker** → **+ Task** → „Pumuckl Voice"
2. **Action:** Shell:
   ```bash
   cd ~/moloch && python watch_ui.py --voice -p pumuckl
   ```
3. **Homescreen Widget** → 👺 Icon → Fertig!
4. **Tippen** = Aufnahme → Kobold-Antwort (ultrakurz & frech)

DGM Vision System (Face Recognition)

Automatische Gesichtserkennung für Pausen-Monitoring am DGM Arbeitsplatz.

**Gesichter registrieren:**

```bash
# Neue Person registrieren
python face_manager.py register markus ~/path/to/markus.jpg
python face_manager.py register erkan ~/path/to/erkan.jpg

# Alle Gesichter anzeigen
python face_manager.py list

# Gesicht löschen
python face_manager.py delete erkan

# Test mit Foto
python face_manager.py test ~/test_image.jpg
```

**Pause-Monitoring starten:**

```bash
# Live Kamera-Monitoring (real-time)
python face_monitor.py

# Mit Custom Interval (Sekunden)
python face_monitor.py --interval 3

# Test mit Foto
python face_monitor.py --test ~/photo.jpg
```

**Output:**
```
✅ Markus erkannt (Sicherheit: 98%)
❓ Unbekannte Person
🔴 ALERT: Unknown person detected!
```

**Log-Datei:** `~/moloch/pause_monitor.log`

**PTZ Kamera Control (Pan-Tilt-Zoom):**

Für PTZ-Kameras am DGM Arbeitsplatz:

```bash
# Konfiguriere PTZ (ptz_config.json)
# {
#   "enabled": true,
#   "camera_url": "http://192.168.1.100",
#   "username": "admin",
#   "password": "password"
# }

# Pan (links/rechts)
python ptz_control.py pan left 5
python ptz_control.py pan right 7

# Tilt (oben/unten)
python ptz_control.py tilt up 5
python ptz_control.py tilt down 3

# Zoom
python ptz_control.py zoom in 5
python ptz_control.py zoom out 3

# Preset fahren
python ptz_control.py preset 1     # Fahre zu Preset 1
```

**Auto-Tracking (geplant):**
Automatisches Folgen von erkannten Personen mit PTZ-Kamera.

Special Interfaces (80s Cyberpunk & HAL 9000)

**Max Headroom Mode — 80s Cyberpunk Interface:**

```bash
python max_headroom.py "NEURAL NETWORK ACTIVATED"    # Standard output
python max_headroom.py --live "MESSAGE"               # Streaming typewriter effect
python max_headroom.py --chat                         # Interactive mode
```

Features:
- Glitchy 80s aesthetic
- Cyan/Magenta/Yellow colors
- Random text corruption
- Cyberpunk vibe 🖤

**HAL 9000 Eye — Pulsing Red Eye Monitor:**

```bash
python hal_eye.py 30                                  # Scanning mode (30 seconds)
python hal_eye.py --boot                              # Boot sequence
python hal_eye.py --status "SYSTEM READY"             # Status display
python hal_eye.py --alert "UNKNOWN INTRUDER"          # Alert display
```

Features:
- Iconic red pulsing eye (from 2001: A Space Odyssey)
- Real-time monitoring animation
- Status updates
- Alert mode with flashing

**Tasker Integration — Always watching:**

```bash
# Run HAL Eye in background while working
nohup python ~/moloch/hal_eye.py 600 &

# Max Headroom for intense moments
python ~/moloch/max_headroom.py --chat
```

Hinweise
- Wenn `edge-tts` nicht installiert ist oder kein Internet besteht, fällt M.O.L.O.C.H. auf lokale Termux-TTS zurück.
- Standard-Stimme: `en-US-JennyNeural` (weiblich, natürlich). Du kannst die Stimme mit der Umgebungsvariable `TTS_VOICE` ändern.
- Falls das Abspielen der erzeugten Datei fehlschlägt, wird nacheinander `termux-media-player`, `ffplay`, `mpv` und `termux-open` versucht.

Fehlerbehebung
- `edge-tts` benötigt Internet. Bei Problemen: überprüfe Netzwerk und Python-Pakete.
- Unter Android/Termux: stelle sicher, dass `termux-api` installiert ist (`pkg install termux-api`).
