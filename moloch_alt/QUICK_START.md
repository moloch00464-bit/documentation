# 🚀 M.O.L.O.C.H. v3.0 - QUICK START GUIDE

## ⚡ 5-Minuten Setup (Desktop)

### 1️⃣ Installation
```bash
# Clone or download
cd moloch

# Install dependencies
pip install -r requirements.txt
```

### 2️⃣ Initial Setup
```bash
# Run setup wizard (interactive configuration)
python setup_wizard.py
```

Der Wizard fragt:
- ✅ Dein Name
- ✅ Persönlichkeitsmodus (Normal/Max Headroom/HAL 9000)
- ✅ Standort (für Wetter)
- ✅ Features aktivieren

### 3️⃣ Start
```bash
# Run M.O.L.O.C.H.
python moloch.py

# Or test individual modules
python weather_aware.py --current
python location_aware.py --current
```

---

## 📱 Smartphone Setup (Termux)

### 1️⃣ Install Termux
- Open Google Play Store
- Search "Termux" (official)
- Install

### 2️⃣ Run Setup
```bash
# In Termux:
bash setup-termux.sh
```

### 3️⃣ Start
```bash
python ~/.moloch/moloch.py
```

---

## 🧪 Test Your Setup

```bash
# Test all Phase 4 modules
python test_phase4.py

# Test Genesis modules
python test_genesis.py

# Check syntax
python check_modules.py

# Live tests with module imports
python run_live_tests.py
```

---

## 🎯 First Interaction

### Desktop:
```
$ python moloch.py
🤖 M.O.L.O.C.H. v3.0 ready
> hello
👂 Processing...
🗣️ Responding...
```

### Smartphone:
```
$ python ~/.moloch/moloch.py
[Termux] M.O.L.O.C.H. v3.0 starting...
🎤 Voice input ready
Say something...
```

---

## 🎮 Interactive Commands

Once running, try:

```
# Voice Control
"hey moloch"           # Wake word
"what's the weather"   # Weather
"where am i"           # Location
"play some music"      # Spotify

# Special Modes
"/mode max_headroom"   # 80s glitch style!
"/mode hal9000"        # HAL 9000 personality
"/mode normal"         # Back to normal

# Brain Commands
"/brain save music WGT is awesome"
"/brain show"          # Show memory
"/brain clear"         # Clear (careful!)

# Information
"/help"                # Commands
"/status"              # System status
"/config"              # Show config
```

---

## 📂 Important Files

```
~/.moloch/
├── moloch.py                    # Main program
├── config/
│   ├── moloch.json             # Your config
│   ├── personality.json        # Personality
│   └── mood.json              # Moods
├── brain/
│   ├── logs/                  # Memories
│   ├── wer/                   # People
│   ├── wo/                    # Locations
│   └── was/                   # Knowledge
└── logs/
    └── moloch.log             # Activity log
```

---

## 🔧 Troubleshooting

### "Module not found" Error
```bash
pip install -r requirements.txt --upgrade
```

### Microphone not working
```bash
# Linux/Termux
apt-get install alsa-utils

# Windows
# Check Sound Settings
```

### No voice output
```bash
# Check TTS engine
python -c "from genesis_module import tts; print(tts.get_status())"

# Termux
pkg install termux-media-player
termux-media-player play audio.mp3
```

---

## 🎓 Learn More

- **README.md** - Full documentation
- **INSTALLATION.md** - Detailed setup
- **TERMUX_README.md** - Mobile guide
- **PHASE4_INTEGRATION.md** - Advanced features
- **RELEASE_NOTES.md** - What's new

---

## 🚀 Ready?

```bash
python setup_wizard.py
```

Let's go! 🎉

---

**Support:**
- Check logs: `~/.moloch/logs/moloch.log`
- Test modules: `python test_phase4.py`
- Read docs: See files above

**Questions?** Check the documentation or test scripts!
