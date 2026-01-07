# M.O.L.O.C.H. Architecture

Detaillierte Übersicht der Code-Struktur, Module und Datenflüsse

---

## 🏗️ System Architektur

```
┌─────────────────────────────────────────────────────┐
│         USER INTERFACE LAYER                         │
│  ┌─────────────┐  ┌──────────────┐  ┌──────────────┐│
│  │ Hotword     │  │ Share Intent │  │ Notifications││
│  │ Listener    │  │ Handler      │  │ Reader       ││
│  └─────────────┘  └──────────────┘  └──────────────┘│
│  ┌─────────────┐  ┌──────────────┐  ┌──────────────┐│
│  │ Voice Input │  │ Spotify      │  │ OCR Camera   ││
│  │ STT         │  │ Control      │  │ Analyzer     ││
│  └─────────────┘  └──────────────┘  └──────────────┘│
│  ┌─────────────┐  ┌──────────────┐  ┌──────────────┐│
│  │ Watch UI    │  │ Max Headroom │  │ HAL Eye      ││
│  │ (Smartwatch)│  │ (Cyberpunk)  │  │ (Monitor)    ││
│  └─────────────┘  └──────────────┘  └──────────────┘│
└─────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────┐
│      CORE ENGINE LAYER (moloch.py)                  │
│  ┌──────────────────────────────────────────────┐  │
│  │ ask_claude()  → AI Inference (with context) │  │
│  │ speak()       → TTS (edge-tts) + Playback   │  │
│  │ record_audio()→ STT (termux-microphone)     │  │
│  │ brain_save()  → Persistent Memory (JSON)    │  │
│  └──────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────┐  │
│  │ Personality System (HAL/Pumuckl)            │  │
│  │ Volume Control (termux-volume)              │  │
│  │ Auto-Save & Context Management              │  │
│  └──────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────┐
│      API & SERVICE LAYER                            │
│  ┌────────────┐  ┌──────────────┐  ┌────────────┐ │
│  │ Claude API │  │ Spotify API  │  │ Google API │ │
│  │ (Anthropic)│  │ (Music)      │  │ (Drive)    │ │
│  └────────────┘  └──────────────┘  └────────────┘ │
│  ┌────────────┐  ┌──────────────┐  ┌────────────┐ │
│  │ Porcupine  │  │ Whisper      │  │ Tesseract  │ │
│  │ (Hotword)  │  │ (STT)        │  │ (OCR)      │ │
│  └────────────┘  └──────────────┘  └────────────┘ │
└─────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────┐
│      SYSTEM LAYER (Android/Termux)                  │
│  ┌──────────┐ ┌──────────────┐ ┌─────────────────┐ │
│  │ Termux   │ │ Tasker       │ │ Audio System    │ │
│  │ (Linux)  │ │ (Automation) │ │ (mpv/ffplay)    │ │
│  └──────────┘ └──────────────┘ └─────────────────┘ │
│  ┌──────────┐ ┌──────────────┐ ┌─────────────────┐ │
│  │ Microphone│ │ Camera       │ │ Notification    │ │
│  │ Input    │ │ Input        │ │ System          │ │
│  └──────────┘ └──────────────┘ └─────────────────┘ │
└─────────────────────────────────────────────────────┘
```

---

## 📁 Modulstruktur

### Core Module

#### **moloch.py** (1197 Zeilen)
Zentrale KI-Engine mit allen Kernfunktionen

```python
# Hauptfunktionen:
ask_claude(prompt, personality="hal") → str
  ├─ get_system_prompt(personality) → system prompt
  ├─ auto_brain_save_genesis() → save context
  └─ Anthropic API Call

speak(text) → None
  ├─ edge-tts synthesis → audio file
  ├─ set_volume(volume) → adjust loudness
  └─ play_audio(path) → playback (multi-fallback)

record_audio() → str (filepath)
  ├─ termux-microphone-record
  ├─ pause-detection (1.5s silence)
  └─ error handling

voice_input_flow() → str (response)
  ├─ record_audio()
  ├─ whisper transcription
  ├─ ask_claude()
  ├─ speak()
  └─ auto_brain_save_genesis()

# Brain Management:
auto_brain_save_genesis(data) → None
  ├─ save to brain tree
  └─ update langzeit.json

load_brain_context() → dict
  ├─ read langzeit.json
  └─ build context
```

**Konfiguration:**
```python
ANTHROPIC_API_KEY = "sk-..."      # Claude API
TTS_VOICE = "en-US-JennyNeural"   # TTS Stimme
MOLOCH_VOLUME = 10                # 0-15
```

### Voice Processing

#### **voice_input.py** (90 Zeilen)
Complete STT → Claude → TTS Pipeline

```python
voice_input_flow()
  1. record_audio() → wav file
  2. whisper_transcribe() → text
  3. ask_claude() → response
  4. speak() → audio
  5. auto_brain_save_genesis()
```

#### **set_volume.py** (140 Zeilen)
Lautstärkeverwaltung mit Persistenz

```python
set_volume(volume: 0-15) → None
load_volume() → int
save_volume(volume) → None
  └─ persists to battery_config.json
```

### Audio & Playback

#### **play_audio()** (Multi-Fallback)
```
order:
1. termux-media-player
2. ffplay
3. mpv
4. termux-open
5. Windows: os.startfile()
```

### Personality System

#### **personalities.py** (120 Zeilen)
Dual-Mode Personality System

```python
# HAL Mode (Dark, Adult, Humor)
HAL_PERSONALITY = {
  "system_prompt": "...",
  "style": "dark_humor",
  "emotion": "analytical"
}

# Pumuckl Mode (Frech, Kurz, Verspielt)
PUMUCKL_PERSONALITY = {
  "system_prompt": "...",
  "style": "cheeky_kobold",
  "emotion": "playful"
}

get_personality_prompt(personality="hal") → str
format_response_for_watch(response, personality) → str
```

### UI & Interfaces

#### **watch_ui.py** (150 Zeilen)
Smartwatch Interface (Compact)

```python
watch_response(prompt, personality="hal") → str
  ├─ Shorten response to 200 chars
  ├─ Format for 1.8" display
  └─ Support Pumuckl personality

watch_voice_input(personality="hal") → str
  ├─ Record audio
  ├─ Process with personality
  └─ Display on watch
```

#### **max_headroom.py** (200 Zeilen)
80s Cyberpunk Interface

```python
# Modes:
print_glitchy(text) → None     # Glitchy output
streaming_output(text) → None  # Typewriter effect
interactive_chat() → None      # Live chat with glitches

# Features:
- Color cycling (cyan/magenta/yellow)
- Glitch text generation
- Retro formatting
```

#### **hal_eye.py** (150 Zeilen)
HAL 9000 Pulsing Monitor

```python
draw_hal_eye(status="scanning") → None
draw_boot_sequence() → None
draw_alert(message) → None
  └─ Red pulsing with flashing
```

### Vision & Recognition

#### **face_manager.py** (250 Zeilen)
Face Database Management

```python
register_face(person_name) → bool
  ├─ Capture from camera
  ├─ Face detection (OpenCV)
  ├─ Face encoding (face_recognition)
  └─ Save to pickle DB

list_faces() → List[str]
delete_face(person_name) → bool
recognize_faces() → List[(name, confidence)]
test_with_image(path) → List[(name, confidence)]
```

**Storage:**
```
~/.moloch/faces_database.pkl    # pickle serialized face encodings
~/.moloch/faces/                # backup PNG images
```

#### **face_monitor.py** (200 Zeilen)
Real-time Face Recognition

```python
recognize_from_camera(interval=2) → None
  ├─ Continuous camera capture
  ├─ Face detection + recognition
  ├─ Logging with timestamps
  └─ Pause detection (if registered)

test_with_image(image_path) → List[(name, confidence)]
```

**Output:**
```
~/.moloch/pause_monitor.log
  ├─ Timestamps
  ├─ Recognized persons
  ├─ Confidence scores
  └─ Activity tracking
```

#### **ptz_control.py** (180 Zeilen)
Pan-Tilt-Zoom Camera Control

```python
pan(degrees) → bool
tilt(degrees) → bool
zoom(factor) → bool
goto_preset(name) → bool
set_preset(name) → bool

# HTTP API Integration:
Config: ~/moloch/ptz_config.json
  ├─ camera_url
  ├─ username
  ├─ password
  └─ presets[]
```

### Content Processing

#### **camera_ocr.py** (400 Zeilen)
Screenshot & OCR Analysis

```python
take_screenshot() → str (filepath)
  ├─ termux screencap
  └─ adb fallback

extract_text(image_path) → str
  ├─ Tesseract OCR
  ├─ German + English support
  └─ Image preprocessing

analyze_text(text) → str
  ├─ Claude analysis
  ├─ auto_brain_save_genesis()
  └─ speak() results

process_screenshot() → dict
process_file(filepath) → dict
camera_realtime() → None (interactive)
daemon_mode(interval) → None
```

#### **notification_reader.py** (350 Zeilen)
Android Notification Processing

```python
process_notifications() → int
  ├─ Load from ~/moloch/notifications.json
  ├─ Apply filters
  ├─ Priority apps → auto speak
  └─ Count new items

configure_filter() → None
  ├─ Interactive setup
  ├─ Ignore list
  ├─ Priority apps
  └─ Save to notification_filter.json

monitor_daemon(interval) → None
```

**Filter Config:**
```json
{
  "ignore_apps": ["com.android.systemui"],
  "priority_apps": ["com.whatsapp"],
  "enabled": true
}
```

#### **spotify_control.py** (450 Zeilen)
Spotify Web API Integration

```python
class SpotifyMoloch:
  setup_oauth() → bool          # Authenticate user
  refresh_access_token() → bool # Token refresh
  search_and_play(query, type) → bool
  next_track() → bool
  previous_track() → bool
  pause() → bool
  resume() → bool
  set_volume(percent) → bool
  now_playing() → None

# Storage:
~/.moloch/spotify_config.json
  ├─ client_id
  ├─ client_secret
  ├─ refresh_token
  └─ device_id
```

### Automation & Detection

#### **hotword_listener.py** (350 Zeilen)
"Hey Moloch" Voice Activation

```python
listen_porcupine() → None
  ├─ Porcupine hotword detection
  ├─ 30s/min free tier
  └─ Google, Alexa, Jarvis presets

listen_snowboy() → None        # TBD (optional)
listen_simple_rms() → None     # Fallback (RMS + Whisper)

detect_and_respond() → None
  └─ triggers voice_input_flow()

daemon_mode(auto_restart) → None
  ├─ Continuous listening
  ├─ Error handling
  └─ Auto-reconnect

# Config:
~/.moloch/hotword_config.json
  ├─ method (porcupine/snowboy)
  ├─ sensitivity
  ├─ access_key
  └─ custom_model
```

#### **share_handler.py** (400 Zeilen)
Android Share Intent Processing

```python
handle_from_intent(text) → result
  ├─ Auto-detect type (URL/file/text)
  └─ Route to handler

process_text(text) → str
  ├─ <500 chars: direct Claude
  ├─ >500 chars: save file + summarize
  ├─ ask_claude()
  └─ speak() + auto_brain_save_genesis()

process_link(url) → str
  ├─ Fetch page
  ├─ Extract text
  ├─ Analyze with Claude
  └─ Summarize + speak

process_file(filepath) → result
  ├─ .txt/.md → process_text()
  ├─ .jpg/.png → vision analysis
  └─ other → error

# Storage:
~/.moloch/share_history.json (last 100 items)
~/.moloch/shared/              (shared files)
```

#### **battery_smart.py** (180 Zeilen)
Automatic Battery Management

```python
get_battery_status() → dict
  ├─ termux-battery-status
  └─ Returns: percentage, health, plugged

check_and_adjust() → None
  ├─ Get battery %
  ├─ Compare to threshold (default 20%)
  ├─ Auto-activate sparmodus if needed
  └─ Auto-deactivate if >20% + charging

activate_savemode() → None
  ├─ Reduce API requests
  ├─ Increase timeouts
  ├─ Disable optional features
  └─ Save to battery_config.json

battery_daemon(interval) → None
  └─ Check every interval seconds

# Config:
~/.moloch/battery_config.json
  ├─ savemode_enabled
  ├─ threshold (%)
  └─ last_check (timestamp)
```

#### **brain_backup.py** (400 Zeilen)
Brain Backup & Google Drive Sync

```python
create_backup() → str (filepath)
  ├─ tar.gz compress ~/moloch/brain
  ├─ Save to ~/moloch/backups/
  └─ Update backup_index.json

upload_to_gdrive(backup_path) → bool
  ├─ rclone copy to gdrive:M.O.L.O.C.H./...
  └─ Verify success

restore_backup(timestamp) → bool
  ├─ Safety backup current brain
  ├─ Extract selected backup
  └─ Restore to ~/moloch/brain

auto_backup_daemon(interval) → None
  ├─ Continuous backups
  ├─ Default 3600s (1 hour)
  └─ Error handling

# Storage:
~/.moloch/backups/
  ├─ brain_backup_YYYYMMDD_HHMMSS.tar.gz
  └─ backup_index.json (metadata)

Google Drive:
  gdrive:M.O.L.O.C.H./Brain\ Backups/
```

---

## 🧠 Data Structure

### Brain Tree

```
~/.moloch/brain/
├── langzeit.json              # Long-term memory (1MB+)
│   ├─ important_facts[]
│   ├─ person_names[]
│   ├─ work_context{}
│   └─ preferences{}
│
├── history.json              # Chat history (20K lines)
│   └─ {timestamp, role, content}[]
│
├── kontext/
│   └─ aktuell.json          # Current context
│
├── wer/                      # People info
│   ├─ freunde/              # Friends
│   ├─ arbeit/               # Work colleagues
│   └─ crew/                 # Main crew
│
├── was/                      # Things/Topics
│   ├─ musik.json            # Music preferences
│   ├─ musik/                # Music folders
│   ├─ projekte/             # Projects
│   ├─ hardware/             # Hardware info
│   └─ musik_compact.json
│
├── wie/                      # Methods/Procedures
│   ├─ regeln/               # Rules
│   └─ sprache/              # Language/Speech settings
│
├── wo/                       # Locations
│   ├─ arbeit/               # Work places
│   ├─ events/               # Event locations
│   └─ home/                 # Home info
│
├── wann/                     # Time-based
│   └─ meilensteine/         # Milestones
│
└── logs/                     # Activity logs
    └─ YYYYMMDD_HHMMSS.txt   # Daily logs
```

### Config Files

```
~/.moloch/
├── config.json
├── gehirn_index.json
├── langzeit.json
├── history.json
├── moloch.py
├── requirements.txt
├── README.md
├── INSTALLATION.md
├── ARCHITECTURE.md
│
├── battery_config.json
├── spotify_config.json
├── hotword_config.json
├── ocr_config.json
├── notification_filter.json
├── ptz_config.json
├── watch_personality.conf
│
├── faces_database.pkl        # Face encodings
├── faces/                    # Face images backup
│
├── backups/                  # Brain backups
│   ├─ brain_backup_*.tar.gz
│   └─ backup_index.json
│
├── shared/                   # Shared content
├── ocr_cache/                # OCR screenshots
├── pause_monitor.log
└── share_history.json
```

---

## 🔄 Data Flow Examples

### Example 1: Voice Input Flow

```
User: Speaks into Microphone
  ↓
record_audio() [moloch.py]
  ├─ termux-microphone-record
  └─ Returns: /tmp/voice.wav (1-45s)
  ↓
whisper_transcribe() [moloch.py]
  ├─ Whisper OpenAI model
  └─ Returns: "Hey Moloch, what's the weather?"
  ↓
ask_claude(text, personality="hal")
  ├─ Loads context from langzeit.json
  ├─ Formats system prompt
  ├─ Calls Anthropic Claude API
  └─ Returns: "It's currently 22°C and cloudy..."
  ↓
auto_brain_save_genesis()
  ├─ Extracts facts
  ├─ Saves to brain/was/
  └─ Updates langzeit.json
  ↓
speak(response)
  ├─ edge-tts synthesis
  ├─ Saves to ~/moloch/ohr.mp3
  └─ Plays via ffplay/mpv
  ↓
User: Hears AI Response via Speaker
```

### Example 2: Share Intent Flow

```
User: Shares link from browser
  ↓
Tasker Intent Handler
  └─ Triggers: share_handler.py --from-intent
  ↓
handle_from_intent(url)
  ├─ Detects: URL
  └─ Routes to: process_link()
  ↓
process_link(url)
  ├─ requests.get(url)
  ├─ Extract text content
  └─ Returns: webpage_text
  ↓
ask_claude("Analyse diese webpage...")
  ├─ Call Claude API
  └─ Returns: analysis
  ↓
auto_brain_save_genesis()
  └─ Save to brain/was/shared_links/
  ↓
speak(analysis)
  └─ TTS output
  ↓
User: Hears summary
```

### Example 3: Hotword Detection Flow

```
System: Always Listening
  ↓
hotword_listener.py --daemon
  ├─ Porcupine listening
  └─ ~30s until budget refresh
  ↓
User: Says "Hey Moloch"
  ↓
detect_and_respond()
  ├─ Hotword matched!
  ├─ Battery check
  ├─ Intent: START_VOICE_INPUT
  └─ Call: voice_input_flow()
  ↓
voice_input_flow()
  ├─ Continue from Step 1 (Voice Input Flow)
  ...
```

### Example 4: Brain Backup Flow

```
Scheduled: Every 3600 seconds
  ↓
brain_backup.py --daemon
  ↓
create_backup()
  ├─ tar czf ~/moloch/brain/
  ├─ Save to ~/moloch/backups/brain_backup_TIMESTAMP.tar.gz
  └─ Update backup_index.json
  ↓
upload_to_gdrive()
  ├─ rclone copy to gdrive:M.O.L.O.C.H./Brain Backups/
  └─ Verify checksum
  ↓
Backup Complete ✅
  ├─ Logged to backup_index.json
  └─ Available for restore
```

---

## 🔌 API Integrations

### Anthropic Claude
- **Endpoint:** https://api.anthropic.com/v1/messages
- **Auth:** ANTHROPIC_API_KEY header
- **Usage:** ask_claude() → Inference
- **Model:** claude-3-5-sonnet-20241022
- **Context Window:** 200K tokens

### Spotify Web API
- **Auth:** OAuth 2.0 (refresh token)
- **Endpoints:**
  - `/v1/search` → Search
  - `/v1/me/player/play` → Play track/artist
  - `/v1/me/player/next` → Next
  - `/v1/me/player/pause` → Pause
- **Rate:** 429 rate limits

### Google Drive (via rclone)
- **Auth:** OAuth 2.0 via rclone config
- **Remote:** `gdrive:` named remote
- **Operations:** cp, ls, rm

### Porcupine (Hotword)
- **Endpoint:** Local processing
- **Library:** pvporcupine Python SDK
- **Free Tier:** 30s/min listening
- **Keywords:** Pre-trained ("Google", "Alexa", etc)

---

## ⚡ Performance Notes

### Memory Footprint
- **moloch.py:** ~50MB (with dependencies)
- **Face DB:** ~10MB per 100 faces
- **Brain (langzeit.json):** ~1-2MB
- **Logs:** ~100KB/day

### Processing Times
- **Voice Input:** 3-5s (record + whisper + claude)
- **TTS:** 1-2s (synthesis + playback)
- **Face Recognition:** 500ms per frame
- **OCR:** 2-5s per screenshot
- **Brain Save:** <100ms

### API Costs (Approximate)
- **Claude:** $3-5/month (5M tokens)
- **Spotify:** Free (with premium account)
- **Porcupine:** Free (30s/min)
- **Google Drive:** Free (100GB)

---

## 🔐 Security Considerations

### API Keys
- Store in environment variables, not in code
- Never commit to git
- Use `.env` file (add to .gitignore)

### Storage
- Brain stored locally (encrypted SD card recommended)
- Google Drive: standard encryption
- Face encodings: pickle format (not reversible)

### Permissions
- Microphone: Required for STT
- Camera: Required for face recognition
- Storage: Required for brain/backups
- Notifications: Required for reader

---

**Architecture Version:** 3.0
**Last Updated:** 2025-12-15
