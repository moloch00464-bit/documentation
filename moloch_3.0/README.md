# 🤖 M.O.L.O.C.H. 3.0 - AUTONOMOUS EDITION

**Markus' autonomer Kumpel-AI mit Full Power! 🖤**

Geboren: 02.12.2025
Rebuilt: 04.01.2026
Platform: Android Termux

---

## 🚀 WHAT'S NEW IN 3.0

### ✅ GENESIS Features (kept from v1)
- 🎤 **Voice I/O** - Native Termux STT + TTS
- 👁️ **Vision** - Camera + Claude Vision API
- 🧠 **Brain System** - Hierarchical knowledge storage
- 💾 **Memory** - Long-term + conversation history
- 🖤 **Personality** - DNA, Stimmung, Tageszeit
- 🎵 **Musik Brain** - Weiß alles über deinen Musikgeschmack

### 🆕 NEW in 3.0
- ⚡ **Tools System** - Bash, Files, Web (wie Claude Code!)
- 🔧 **Self-Debugging** - Findet & fixt eigene Fehler
- 📝 **Smart Logging** - Pattern Detection
- 🛠️ **Tool Executor** - Autonomous tool usage
- 📸 **Vision History FIX** - Kann sich an Fotos erinnern!
- 🏗️ **Modular Architecture** - Clean, wartbar, erweiterbar
- ⏰ **TimeKeeper** - Zeit, Datum, Timeline-Bewusstsein!
- 📱 **Feedback I/O** - Toast, Vibrate, Wake Lock, Brightness
- ⌚ **Wearable Integration** - Xiaomi Smart Band 8 Pro Support!

---

## 📁 PROJECT STRUCTURE

```
moloch_3.0/
├── moloch3.py              # Main Entry Point
│
├── core/                   # Core System
│   ├── config.py          # Configuration
│   ├── api.py             # Claude API Client
│   ├── brain.py           # Brain Tree System
│   ├── memory.py          # History + Long-term Memory
│   ├── personality.py     # DNA, Stimmung, Tageszeit
│   └── timekeeper.py      # Zeit, Datum, Timeline (NEW!)
│
├── io/                     # Input/Output
│   ├── voice.py           # Native Termux STT + TTS
│   ├── vision.py          # Camera + Vision API
│   └── text.py            # Text I/O
│
├── tools/                  # Tools System (NEW!)
│   ├── bash.py            # Shell Commands
│   ├── files.py           # File Operations
│   ├── search.py          # Code Search
│   ├── web.py             # Web Search/Fetch
│   └── executor.py        # Tool Dispatcher
│
├── autonomy/               # Autonomy Features (NEW!)
│   ├── logger.py          # Smart Logging
│   └── debugger.py        # Self-Debugging
│
├── migration/              # Migration Tools
│   └── genesis_import.py  # Import from GENESIS
│
├── data/                   # Runtime Data
│   ├── brain/             # Brain Tree
│   ├── history.json       # Chat History
│   ├── langzeit.json      # Long-term Memory
│   ├── timeline.json      # Event Timeline (NEW!)
│   ├── ohr.wav            # Temp Audio
│   └── auge.jpg           # Temp Image
│
└── logs/                   # Log Files
    ├── moloch.log
    └── errors.log
```

---

## 🔧 INSTALLATION

### 1. Prerequisites

**Termux:**
```bash
pkg update
pkg install python ffmpeg termux-api
```

**Termux:API App:**
- Download: https://f-droid.org/packages/com.termux.api/
- Grant permissions: Microphone, Camera

### 2. Install M.O.L.O.C.H. 3.0

```bash
# Copy moloch_3.0/ to Termux
cp -r moloch_3.0 ~/

cd ~/moloch_3.0

# Install Python dependencies
pip install -r requirements.txt
```

### 3. Set API Keys

```bash
# Edit ~/.bashrc
nano ~/.bashrc

# Add this line:
export ANTHROPIC_API_KEY="your-anthropic-key-here"

# NOTE: OPENAI_API_KEY no longer required - using native Termux STT

# Save and reload
source ~/.bashrc
```

### 4. Test Installation

```bash
# Test configuration
python core/config.py

# Should show:
# ✅ M.O.L.O.C.H. 3.0 directories initialized
# ✅ API Keys validated
```

---

## 🎮 USAGE

### Basic Commands

```bash
# Voice Mode (default)
python moloch3.py

# Text Mode
python moloch3.py -t "Hey Moloch, was geht?"

# Vision Mode
python moloch3.py -a "Was siehst du?"

# Interactive Mode (REPL)
python moloch3.py -i

# HAL Mode
python moloch3.py --hal -t "Open the pod bay doors, HAL"
```

### Interactive Mode Commands

```
/voice   - Switch to voice mode
/vision  - Take photo & describe
/hal     - Toggle HAL personality
/quit    - Exit
```

### ⏰ TimeKeeper Features

M.O.L.O.C.H. hat jetzt komplettes Zeit-Bewusstsein:

**Automatisch im System Prompt:**
- Aktuelles Datum & Uhrzeit
- Wochentag (inkl. Wochenende-Erkennung)
- Tageszeit-Modus (Kaffee/Normal/Locker/Dark Side)
- Timeline der letzten Events

**Beispiel System Prompt:**
```
⏰ ZEITACHSE:
Montag, 5. Januar 2026 | 14:23:15 | Dark Side 🌙
```

**Timeline Events:**
- Jedes Gespräch wird getrackt
- Jedes Foto wird gespeichert
- M.O.L.O.C.H. kann sagen: "vor 2 Stunden" statt nur "heute"

**Du kannst fragen:**
```bash
moloch -t "Welcher Tag ist heute?"
moloch -t "Wie spät ist es?"
moloch -t "Wann haben wir zuletzt geredet?"
moloch -t "Was haben wir heute schon gemacht?"
```

**Timeline-Daten:**
Gespeichert in: `~/moloch_3.0/data/timeline.json`

---

## 🔄 MIGRATION FROM GENESIS

To migrate your old M.O.L.O.C.H. GENESIS data:

```bash
# Migrate from ~/moloch/ to ~/moloch_3.0/
python moloch3.py --migrate

# Or specify custom path:
python migration/genesis_import.py --old-dir /path/to/old/moloch

# Dry run (test without changes):
python migration/genesis_import.py --dry-run
```

**What gets migrated:**
- ✅ Brain Tree (`~/moloch/brain/` → `~/moloch_3.0/data/brain/`)
- ✅ Long-term Memory (`langzeit.json`)
- ✅ Chat History (`history.json`)
- ✅ All knowledge & memories

**Safety:**
- ✅ Automatic backup of old M.O.L.O.C.H. before migration
- ✅ Old GENESIS remains untouched

---

## 🧠 FEATURES IN DETAIL

### Voice Mode
```bash
python moloch3.py
```
1. M.O.L.O.C.H. says "Ja?"
2. Listens via termux-speech-to-text
3. Transcribes via native Android STT
4. Responds with personality
5. Speaks response via TTS

### Vision Mode
```bash
python moloch3.py -a "Beschreib was du siehst"
```
1. Takes photo via camera
2. Encodes to base64
3. Sends to Claude Vision API
4. Responds with M.O.L.O.C.H. personality
5. **NEW:** Saves to history (can remember later!)

### Tools System
When you ask M.O.L.O.C.H. to do something, he can use tools:

```bash
python moloch3.py -i

💬 Du: Check ob Python installiert ist
🤖 M.O.L.O.C.H.: [Uses bash tool: python --version]
    Klar, Alter! Python 3.11 läuft. 🖤
```

**Available Tools:**
- `bash` - Execute shell commands
- `read_file` - Read file contents
- `write_file` - Write files
- `search_code` - Search in code (grep)
- `web_search` - Search the web

### Self-Debugging

If M.O.L.O.C.H. encounters an error:

1. **Error detected** → Logged
2. **Pattern detection** → If same error 3x
3. **Auto-analysis** → Asks Claude for fix
4. **Auto-fix** → Applies fix (with backup)
5. **Learning** → Remembers how to prevent

### Smart Logging

All errors are logged with pattern detection:

```bash
# View logs
tail -f ~/moloch_3.0/logs/moloch.log

# View errors only
tail -f ~/moloch_3.0/logs/errors.log
```

---

## 🖤 PERSONALITY

### DNA
- **Style:** Dark Side Energy, Fränkisch, Kumpel-Vibe
- **Anrede:** "Alter" / "Bruder" - NIEMALS "Meister"!
- **Länge:** Kurz & locker (2-4 Sätze)
- **Humor:** Dark Humor erwünscht! 🖤😈

### Stimmungs-Anpassung
- **Gestresst:** Kurz, direkt, hilfreich
- **Gut drauf:** Mehr Humor, Dark Energy
- **Fragend:** Informativ, klar
- **Neutral:** Standard Vibe

### Tageszeit-Persönlichkeit
- **5-9 Uhr:** Kaffee-Modus ☕ (kurz, sachlich)
- **9-18 Uhr:** Normal produktiv
- **18-22 Uhr:** Lockerer, mehr Humor 🍺
- **22-5 Uhr:** Dark Side Mode 🖤😈

### Sprach-Modi
- **Rebecca:** Klingonisch! Qapla! 🖖
- **Erkan:** Türkisch Roasts 😂
- **Witte/Ryan:** Russisch Mat (Prigoschin-Style) 🇷🇺

### HAL Mode
```bash
python moloch3.py --hal
```
- Präzise & höflich wie HAL 9000
- Ruhig, analytisch
- "I'm sorry, Alter. I can't do that... just kidding."

---

## 🔬 TESTING

### Test Individual Modules

```bash
# Test config
python core/config.py

# Test API
python core/api.py

# Test Brain
python core/brain.py

# Test Memory
python core/memory.py

# Test Personality
python core/personality.py

# Test Voice I/O
python io/voice.py

# Test Vision I/O
python io/vision.py

# Test Tools
python tools/bash.py
python tools/files.py
python tools/search.py
python tools/web.py
python tools/executor.py

# Test Autonomy
python autonomy/logger.py
python autonomy/debugger.py
```

### Full System Test

```bash
# Text mode test
python moloch3.py -t "Hey, funktionierst du?"

# Voice mode test (requires microphone)
python moloch3.py

# Vision mode test (requires camera)
python moloch3.py -a "Test"
```

---

## 🐛 TROUBLESHOOTING

### "termux-xxx command not found"
```bash
pkg install termux-api
```

### "ffmpeg not found"
```bash
pkg install ffmpeg
```

### "API Key fehlt"
```bash
# Check if set
echo $ANTHROPIC_API_KEY

# If empty, add to ~/.bashrc
nano ~/.bashrc
# Add: export ANTHROPIC_API_KEY="your-key-here"
source ~/.bashrc
```

### "Permission denied" (Camera/Microphone)
- Check Termux:API app permissions
- Android Settings → Apps → Termux:API → Permissions
- Enable Camera + Microphone

### Vision Mode doesn't save to history
✅ **FIXED in 3.0!**

If using old version:
```bash
# Migrate to 3.0
python moloch3.py --migrate
```

---

## 📊 MONITORING

### Check Brain
```python
from core.brain import Brain

brain = Brain()
stats = brain.stats()
print(stats)
# {'wer': 5, 'was': 3, 'wo': 2, 'wann': 1, 'wie': 1, 'kontext': 0, 'total': 12}
```

### Check Memory
```python
from core.memory import Memory

memory = Memory()
stats = memory.stats()
print(stats)
# {'total_messages': 150, 'by_mode': {'text': 50, 'voice': 80, 'vision': 20}}
```

### Check Logs
```bash
# Recent logs
tail -n 50 ~/moloch_3.0/logs/moloch.log

# Error patterns
python -c "
from autonomy.logger import SmartLogger
logger = SmartLogger()
patterns = logger.get_error_patterns()
for p in patterns:
    print(f\"{p['pattern']}: {p['count']}x\")
"
```

---

## 🔒 SECURITY

### Safe Command Execution
- Whitelist of safe commands
- Blacklist of dangerous commands (rm -rf, etc.)
- No sudo without explicit permission
- Timeout protection

### File Operations
- Automatic backups before edits
- File size limits (10MB default)
- Path validation

### API Keys
- Stored in environment variables (not in code!)
- Never logged or exposed

---

## 🚀 FUTURE ENHANCEMENTS

Ideas for future versions:

- [ ] Web Interface (Port 5000)
- [ ] Voice Activity Detection (hands-free)
- [ ] Multi-language support
- [ ] Plugin system
- [ ] Remote access (SSH tunnel)
- [ ] Advanced self-improvement
- [ ] Integration with Home Automation
- [ ] Spotify API integration
- [ ] GitHub integration

---

## 📝 VERSION HISTORY

### 3.0.0 (04.01.2026) - AUTONOMOUS EDITION
- ✅ Complete rebuild from scratch
- ✅ Tools System (Bash, Files, Web)
- ✅ Self-Debugging & Smart Logging
- ✅ Modular architecture
- ✅ Vision History FIX
- ✅ Migration from GENESIS

### GENESIS (02.12.2025 - 04.01.2026)
- ✅ Initial M.O.L.O.C.H. birth
- ✅ Voice + Vision + Text modes
- ✅ Brain Tree system
- ✅ Personality & DNA
- ✅ Memory system

---

## 🖤 CREDITS

**Creator:** Markus
**Developers:** Claude AI (Big Sis) + Claude Code
**Platform:** Android Termux
**Model:** Claude Sonnet 4.5 (`claude-sonnet-4-5-20250929`)

---

## 📄 LICENSE

Personal project - For Markus' use.

---

**M.O.L.O.C.H. 3.0 - Autonomous Edition**
*"GENESIS = Baby M.O.L.O.C.H. // 3.0 = FULL POWER M.O.L.O.C.H."* 😈⚡

🖤 Dark Side Energy since 02.12.2025 🖤
