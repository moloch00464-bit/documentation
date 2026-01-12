---
title: Basic Configuration
description: "Configure M.O.L.O.C.H. 3.0 for your Raspberry Pi"
---

# Basic Configuration

This guide covers the essential configuration settings for M.O.L.O.C.H. 3.0 on Raspberry Pi.

## Configuration File

M.O.L.O.C.H. 3.0 uses a JSON configuration file located at:

```
~/moloch_3.0/config.json
```

### Creating Your Configuration

If you haven't already, create your configuration from the example:

```bash
cd ~/moloch_3.0
cp config.example.json config.json
nano config.json
```

## Essential Settings

### API Keys

The most important configuration - your AI API access:

```json
{
  "api_keys": {
    "anthropic": "sk-ant-api03-YOUR_KEY_HERE",
    "openai": "sk-YOUR_OPENAI_KEY_HERE"
  }
}
```

**Anthropic API Key** (Required):
- Get from: [console.anthropic.com](https://console.anthropic.com/)
- Used for: Claude AI (main brain)
- Must have credits available

**OpenAI API Key** (Optional):
- Get from: [platform.openai.com](https://platform.openai.com/)
- Used for: Whisper STT (voice recognition)
- Alternative: Use local Whisper model

!!! danger "Security Warning"
    Never commit `config.json` to version control!
    Never share your API keys publicly!

---

### Model Selection

Choose which Claude model to use:

```json
{
  "model": "claude-3-opus-20240229"
}
```

**Available Models:**

| Model | Speed | Intelligence | Cost | Recommended For |
|-------|-------|--------------|------|-----------------|
| `claude-3-opus-20240229` | Slower | Highest | $$$$ | Pi 4/5, complex tasks |
| `claude-3-sonnet-20240229` | Medium | High | $$ | Pi 4, balanced use |
| `claude-3-haiku-20240307` | Fastest | Good | $ | Pi 3B+, simple tasks |

**Recommendations by Hardware:**
- **Pi 3B+ (2GB)**: Use Haiku, limit context
- **Pi 4 (4GB)**: Use Sonnet, good balance
- **Pi 4 (8GB)**: Use Opus, maximum capability
- **Pi 5**: Use Opus, best performance

---

### Voice Configuration

Settings for voice interaction:

```json
{
  "voice": {
    "enabled": true,
    "engine": "pyttsx3",
    "rate": 150,
    "volume": 0.9,
    "voice_id": 0,
    "silence_threshold": 500,
    "silence_duration": 2.0
  }
}
```

**Voice Settings Explained:**

**`enabled`** (true/false)
- Enable voice features
- Set to `false` for text-only mode

**`engine`** (string)
- TTS engine to use
- Options: `"pyttsx3"`, `"espeak"`, `"festival"`, `"gtts"`
- `pyttsx3`: Best for offline use
- `espeak`: Fast, lightweight
- `festival`: Higher quality, slower
- `gtts`: Google TTS, requires internet

**`rate`** (integer: 50-300)
- Speaking speed in words per minute
- 150 = normal speed
- Lower = slower, clearer
- Higher = faster

**`volume`** (float: 0.0-1.0)
- Speaking volume
- 0.0 = silent
- 1.0 = maximum

**`voice_id`** (integer: 0-N)
- Which voice to use (if multiple available)
- 0 = default voice
- Try different numbers for different voices

**`silence_threshold`** (integer)
- Audio level below which is considered silence
- Higher = more sensitive (ends recording sooner)
- Lower = less sensitive (waits longer)
- Typical range: 300-700

**`silence_duration`** (float)
- Seconds of silence before ending recording
- 1.0-3.0 recommended
- Longer = more patient, may feel slow
- Shorter = more responsive, may cut off

---

### Vision Configuration

Settings for camera and vision:

```json
{
  "vision": {
    "enabled": true,
    "camera_index": 0,
    "resolution": [1920, 1080],
    "store_images": true,
    "max_image_age_days": 30
  }
}
```

**Vision Settings Explained:**

**`enabled`** (true/false)
- Enable vision features
- Requires camera hardware

**`camera_index`** (integer: 0-N)
- Which camera to use if multiple connected
- 0 = first camera (default)
- Try 1, 2, etc. if camera not detected

**`resolution`** (array: [width, height])
- Image capture resolution
- `[1920, 1080]` = Full HD
- `[1280, 720]` = HD (faster, smaller files)
- `[640, 480]` = VGA (lowest quality, fastest)
- Higher resolution = more detail but slower

**`store_images`** (true/false)
- Save captured images to disk
- true = keep visual memory
- false = analyze but don't save

**`max_image_age_days`** (integer)
- Auto-delete images older than X days
- Helps manage storage
- 0 = never delete
- 30 = keep one month

---

### Memory Configuration

Settings for memory and context:

```json
{
  "memory": {
    "enabled": true,
    "max_context": 100000,
    "auto_save": true,
    "save_interval": 300,
    "database_path": "data/memory.db"
  }
}
```

**Memory Settings Explained:**

**`enabled`** (true/false)
- Enable persistent memory
- false = no conversation history saved

**`max_context`** (integer: tokens)
- Maximum context window size
- Claude Opus/Sonnet: up to 200k
- Higher = more memory but slower
- Recommendations:
  - Pi 3B+: 50000
  - Pi 4 4GB: 100000
  - Pi 4 8GB: 150000
  - Pi 5: 200000

**`auto_save`** (true/false)
- Automatically save conversations
- true = periodic saves (recommended)
- false = manual save only

**`save_interval`** (integer: seconds)
- How often to auto-save
- 300 = every 5 minutes
- Lower = more frequent saves
- Higher = less disk I/O

**`database_path`** (string)
- Location of SQLite memory database
- Relative to moloch_3.0 directory
- Default: `"data/memory.db"`

---

### Personality Configuration

Customize M.O.L.O.C.H.'s behavior:

```json
{
  "personality": {
    "name": "M.O.L.O.C.H.",
    "formality": 0.5,
    "verbosity": 0.6,
    "creativity": 0.7,
    "emotional_tone": 0.5
  }
}
```

**Personality Settings Explained:**

**`name`** (string)
- What M.O.L.O.C.H. calls itself
- Default: "M.O.L.O.C.H."
- Customize as you like

**`formality`** (float: 0.0-1.0)
- 0.0 = very casual
- 0.5 = balanced
- 1.0 = very formal

**`verbosity`** (float: 0.0-1.0)
- 0.0 = very concise
- 0.5 = balanced
- 1.0 = very detailed

**`creativity`** (float: 0.0-1.0)
- 0.0 = very structured
- 0.5 = balanced
- 1.0 = very creative

**`emotional_tone`** (float: 0.0-1.0)
- 0.0 = neutral, technical
- 0.5 = balanced
- 1.0 = expressive, warm

---

## Complete Example Configuration

Here's a complete `config.json` optimized for **Raspberry Pi 4 (4GB)**:

```json
{
  "api_keys": {
    "anthropic": "sk-ant-api03-YOUR_ANTHROPIC_KEY_HERE",
    "openai": "sk-YOUR_OPENAI_KEY_HERE"
  },
  "model": "claude-3-sonnet-20240229",
  "voice": {
    "enabled": true,
    "engine": "pyttsx3",
    "rate": 160,
    "volume": 0.85,
    "voice_id": 0,
    "silence_threshold": 500,
    "silence_duration": 2.0
  },
  "vision": {
    "enabled": true,
    "camera_index": 0,
    "resolution": [1280, 720],
    "store_images": true,
    "max_image_age_days": 30
  },
  "memory": {
    "enabled": true,
    "max_context": 100000,
    "auto_save": true,
    "save_interval": 300,
    "database_path": "data/memory.db"
  },
  "personality": {
    "name": "M.O.L.O.C.H.",
    "formality": 0.4,
    "verbosity": 0.6,
    "creativity": 0.7,
    "emotional_tone": 0.5
  },
  "tools": {
    "bash": {
      "enabled": true,
      "safe_mode": true
    },
    "web_search": {
      "enabled": true
    },
    "file_operations": {
      "enabled": true,
      "allowed_paths": [
        "/home/pi",
        "/tmp"
      ]
    }
  },
  "logging": {
    "level": "INFO",
    "file": "logs/moloch.log",
    "max_size_mb": 10,
    "backup_count": 5
  }
}
```

---

## Configuration for Different Pi Models

### Raspberry Pi 3B+ (2GB)

Optimized for limited resources:

```json
{
  "model": "claude-3-haiku-20240307",
  "voice": {
    "engine": "espeak",
    "enabled": true
  },
  "vision": {
    "enabled": false,
    "resolution": [640, 480]
  },
  "memory": {
    "max_context": 50000
  }
}
```

### Raspberry Pi 4 (8GB) / Pi 5

Maximum capabilities:

```json
{
  "model": "claude-3-opus-20240229",
  "voice": {
    "engine": "festival",
    "enabled": true
  },
  "vision": {
    "enabled": true,
    "resolution": [1920, 1080]
  },
  "memory": {
    "max_context": 200000
  }
}
```

---

## Testing Your Configuration

After making changes, test your configuration:

```bash
# Validate JSON syntax
python3 -m json.tool config.json

# Test with text mode first
python3 moloch3.py

# Then test specific features
python3 moloch3_voice.py  # Test voice
python3 moloch3_vision.py # Test vision
```

---

## Environment Variables

Alternative to config.json for sensitive data:

```bash
# Add to ~/.bashrc or ~/.profile
export ANTHROPIC_API_KEY="sk-ant-api03-YOUR_KEY_HERE"
export OPENAI_API_KEY="sk-YOUR_KEY_HERE"
```

M.O.L.O.C.H. will check environment variables if not found in config.json.

---

## Troubleshooting Configuration

### API Key Not Working

```bash
# Test Anthropic key
curl https://api.anthropic.com/v1/messages \
  -H "x-api-key: YOUR_KEY_HERE" \
  -H "anthropic-version: 2023-06-01" \
  -H "content-type: application/json" \
  -d '{"model":"claude-3-haiku-20240307","max_tokens":10,"messages":[{"role":"user","content":"Hi"}]}'
```

### Voice Not Working

```bash
# Test TTS
echo "Testing voice" | espeak

# Test pyttsx3
python3 -c "import pyttsx3; engine = pyttsx3.init(); engine.say('Test'); engine.runAndWait()"
```

### Vision Not Working

```bash
# Test camera
libcamera-hello

# Check camera in Python
python3 -c "import cv2; print(cv2.VideoCapture(0).isOpened())"
```

---

## Next Steps

- **[Usage Guide](/docs/usage/index.md)** - Start using M.O.L.O.C.H.
- **[Features Overview](/docs/features/index.md)** - Explore capabilities
- **[FAQ](/docs/moloch-faq.md)** - Configuration questions

---

**Questions?** Check the [FAQ](/docs/moloch-faq/) or [open an issue](https://github.com/moloch00464-bit/documentation/issues).
