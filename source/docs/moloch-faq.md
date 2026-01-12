---
title: Frequently Asked Questions
description: "Common questions about M.O.L.O.C.H. 3.0 on Raspberry Pi"
---

# Frequently Asked Questions

Common questions and answers about M.O.L.O.C.H. 3.0 - Autonomous Edition for Raspberry Pi.

## General Questions

### What is M.O.L.O.C.H. 3.0?

M.O.L.O.C.H. 3.0 (Multi-Operational Learning & Optimization Cognitive Holographic System) is an autonomous AI assistant system powered by Claude AI. It features voice interaction, vision capabilities, persistent memory, and autonomous personality traits.

### Is this related to HACS or Home Assistant?

No. This documentation repository was originally forked from HACS (Home Assistant Community Store) but M.O.L.O.C.H. 3.0 is a completely separate, independent project. It has nothing to do with Home Assistant or HACS.

### Which Raspberry Pi models are supported?

- **Minimum**: Raspberry Pi 3B+ (2GB RAM) - text mode only
- **Recommended**: Raspberry Pi 4 (4GB+ RAM) or Raspberry Pi 5
- **Best**: Raspberry Pi 4/5 with 8GB RAM

### What's the difference from the Termux version?

| Feature | Termux (Android) | Raspberry Pi |
|---------|------------------|--------------|
| Platform | Android phone | Dedicated hardware |
| Portability | High | Stationary |
| 24/7 Operation | Battery-limited | Yes, ideal |
| GPIO Access | No | Yes |
| Performance | Shared resources | Dedicated |
| Setup | Easier | Moderate |

### Is internet connection required?

Yes, M.O.L.O.C.H. 3.0 requires internet for:
- Claude API (brain/reasoning)
- Optional: OpenAI Whisper API (voice recognition)
- Optional: Web search features

Local-only mode is not currently supported but is planned for future releases.

---

## Installation & Setup

### Do I need both Anthropic and OpenAI API keys?

- **Anthropic API key**: **Required** (for Claude AI)
- **OpenAI API key**: **Optional** (for Whisper STT)

You can use local Whisper model instead of OpenAI API for voice recognition.

### How much do API costs run?

Typical costs (estimated):

| Usage Level | Daily Interactions | Monthly Cost |
|-------------|-------------------|--------------|
| Light | 10-20 exchanges | $5-15 (Sonnet) |
| Medium | 50-100 exchanges | $20-40 (Sonnet) |
| Heavy | 200+ exchanges | $50-100 (Sonnet) |

Vision features cost more. Opus model costs ~3x more than Sonnet.

### Can I run M.O.L.O.C.H. without a display?

Yes! M.O.L.O.C.H. works great headless via SSH. You can:
- Use text mode via SSH
- Use voice mode with audio forwarded
- Set up as systemd service for auto-start

### How long does installation take?

- **Basic setup**: 15-30 minutes
- **With audio/camera**: 30-60 minutes
- **Full configuration**: 1-2 hours

Actual time depends on internet speed and Pi model.

---

## Hardware Questions

### What audio hardware do I need?

**Minimum:**
- Any USB microphone
- 3.5mm speakers or headphones

**Recommended:**
- USB microphone with noise cancellation
- Audio HAT (like HiFiBerry)
- Quality speakers

### What camera should I use?

**Raspberry Pi Camera Module:**
- V2 (8MP) - good
- V3 (12MP) - better, has autofocus
- HQ Camera - best quality

**USB Webcam:**
- Any 720p+ webcam works
- Logitech C270, C920 recommended
- Make sure it's Linux-compatible

### How much storage do I need?

**Minimum**: 16GB SD card
**Recommended**: 64GB+ Class 10 SD card

Storage grows over time:
- Memory database: ~1-5MB per day
- Vision cache: ~10-20MB per day (if enabled)
- Logs: ~200MB total

### Do I need cooling?

**Recommended** for:
- Raspberry Pi 4/5 under any use
- Pi 3B+ for extended operation
- Any Pi running 24/7

Without cooling, Pi may throttle (slow down) when hot.

---

## Performance Questions

### Why is M.O.L.O.C.H. slow on my Pi 3B+?

Pi 3B+ has limited RAM (2GB max). Try:
- Use Haiku model instead of Opus
- Reduce `max_context` to 50000
- Disable vision features
- Use text mode only
- Close other applications

### Can I improve response speed?

Yes:
- Use Sonnet or Haiku instead of Opus
- Reduce context window size
- Use faster TTS engine (espeak)
- Ensure good network connection
- Add cooling to prevent throttling

### How much RAM does M.O.L.O.C.H. use?

Typical RAM usage:
- **Text mode**: 500MB-1GB
- **Voice mode**: 800MB-1.5GB
- **Vision mode**: 1GB-2GB
- **Unified mode**: 1.5GB-3GB

Varies based on context size and model.

---

## Features & Usage

### Can M.O.L.O.C.H. control GPIO pins?

Yes! Through bash command execution:
```
"Set GPIO pin 17 high"
"Read the value of GPIO pin 22"
```

Requires proper permissions and GPIO tools installed.

### Does it work offline?

Partially:
- ✅ Basic operation: No (needs Claude API)
- ✅ Local Whisper: Yes (for voice)
- ✅ Local TTS: Yes (pyttsx3, espeak)
- ✅ File operations: Yes
- ✅ Bash commands: Yes
- ❌ AI reasoning: No (requires Claude)
- ❌ Vision analysis: No (requires Claude Vision)
- ❌ Web search: No

Full offline mode planned for future release.

### How is memory managed?

M.O.L.O.C.H. uses two memory systems:

**Short-term (RAM):**
- Current conversation
- Last ~100k tokens
- Lost on restart

**Long-term (SQLite):**
- All conversations saved
- Searchable history
- Persists across restarts
- Auto-pruning optional

### Can multiple people use it?

Currently M.O.L.O.C.H. doesn't have multi-user support. All conversations are in one shared memory. Multi-user mode is planned for future releases.

---

## Voice & Vision

### Why isn't my microphone detected?

Check:
```bash
# List recording devices
arecord -l

# Test recording
arecord -d 3 test.wav && aplay test.wav

# Check permissions
groups | grep audio
```

If not in 'audio' group:
```bash
sudo usermod -a -G audio $USER
# Then logout and login
```

### Voice recognition is inaccurate

Tips:
- Speak clearly at normal pace
- Reduce background noise
- Check microphone positioning (6-12" away)
- Adjust `silence_threshold` in config
- Ensure good internet connection (if using Whisper API)

### Camera not working

Check:
```bash
# Enable camera interface
sudo raspi-config
# Interface Options → Camera → Enable

# Test camera
libcamera-hello

# Check in Python
python3 -c "import cv2; print(cv2.VideoCapture(0).isOpened())"
```

### Why are images blurry?

Possible causes:
- Camera out of focus (use Pi Camera V3 with autofocus)
- Poor lighting
- Camera moved during capture
- Low resolution setting

Try increasing resolution in config or improving lighting.

---

## Troubleshooting

### "API key invalid" error

Check:
1. API key is correct in `config.json`
2. No extra spaces or quotes
3. Key has available credits
4. Test key with curl (see Configuration guide)

### M.O.L.O.C.H. crashes or freezes

Common causes:
- Out of memory (check with `free -h`)
- Overheating (check with `vcgencmd measure_temp`)
- Insufficient power supply
- SD card corruption

Solutions:
- Reduce `max_context`
- Add cooling
- Use proper power supply
- Check SD card with `sudo dmesg`

### "Module not found" errors

Ensure virtual environment is activated:
```bash
cd ~/moloch_3.0
source venv/bin/activate
pip install -r requirements.txt
```

### Slow response times

Possible causes and fixes:
- Poor network: Check internet speed
- Hot Pi: Add cooling
- Wrong model: Switch to Sonnet/Haiku
- Too much context: Reduce `max_context`
- Other processes: Check with `htop`

---

## Data & Privacy

### Where is my data stored?

**Configuration**: `~/moloch_3.0/config.json`
**Memory Database**: `~/moloch_3.0/data/memory.db`
**Images**: `~/moloch_3.0/data/vision/`
**Logs**: `~/moloch_3.0/logs/`

All data stays on your Pi by default.

### Is my data sent anywhere?

Data sent to APIs:
- **Anthropic**: Your conversations, images (for Claude Vision)
- **OpenAI**: Your voice recordings (if using Whisper API)

Nothing else is sent externally. No telemetry, no tracking.

### How do I delete my conversation history?

```bash
# Delete memory database
rm ~/moloch_3.0/data/memory.db

# Delete all images
rm -rf ~/moloch_3.0/data/vision/*

# Delete logs
rm ~/moloch_3.0/logs/*.log
```

M.O.L.O.C.H. will create new databases on next run.

### Can I backup my memory?

Yes:
```bash
# Backup memory database
cp ~/moloch_3.0/data/memory.db ~/moloch_backup_$(date +%Y%m%d).db

# Backup entire data folder
tar -czf moloch_data_backup.tar.gz ~/moloch_3.0/data/

# Restore
cp ~/moloch_backup_20260112.db ~/moloch_3.0/data/memory.db
```

---

## Advanced

### Can I customize the personality?

Yes! Edit `personality` section in `config.json`:
```json
{
  "personality": {
    "formality": 0.5,
    "verbosity": 0.6,
    "creativity": 0.7,
    "emotional_tone": 0.5
  }
}
```

Values range from 0.0 to 1.0. See Configuration guide for details.

### Can I add custom tools?

Custom tool integration is possible but requires Python programming. Check the [Development guide](/docs/contribute/devcontainer.md) for details.

### Does it support other languages?

Yes! Claude supports multiple languages. M.O.L.O.C.H. will respond in whatever language you use. Voice recognition (Whisper) also supports many languages.

### Can I run multiple instances?

Yes, but each needs:
- Separate directory
- Own config.json
- Different ports (if using web interface)
- Sufficient RAM (4GB+ recommended per instance)

### How do I update M.O.L.O.C.H.?

```bash
cd ~/moloch_3.0
git pull origin main
source venv/bin/activate
pip install -r requirements.txt --upgrade
```

---

## Getting Help

### Where can I get support?

- **Documentation**: You're reading it! Check other sections
- **GitHub Issues**: [Report bugs/ask questions](https://github.com/moloch00464-bit/documentation/issues)
- **Troubleshooting Guide**: [/docs/use/troubleshooting/diagnostics.md](/docs/use/troubleshooting/diagnostics.md)

### How do I report a bug?

1. Go to [GitHub Issues](https://github.com/moloch00464-bit/documentation/issues)
2. Click "New Issue"
3. Include:
   - Pi model and OS version
   - M.O.L.O.C.H. version
   - Steps to reproduce
   - Error messages
   - Relevant logs

### Can I contribute?

Yes! Contributions welcome:
- Documentation improvements
- Bug fixes
- New features
- Testing on different hardware

See [Contributing guide](/docs/contribute/index.md).

---

## Future Features

### What's planned for future releases?

- Scheduler (time-based autonomous actions)
- Web interface (browser-based control)
- Multi-user support
- Offline mode (local models)
- Mobile app (remote control)
- Home automation integration
- Multi-Pi cluster support
- Goal tracking system

---

**Didn't find your answer?** [Ask on GitHub Issues](https://github.com/moloch00464-bit/documentation/issues)
