---
title: Raspberry Pi Installation
description: "Complete guide to installing M.O.L.O.C.H. 3.0 on Raspberry Pi"
---

# Installing M.O.L.O.C.H. 3.0 on Raspberry Pi

This guide will walk you through installing M.O.L.O.C.H. 3.0 - Autonomous Edition on your Raspberry Pi hardware.

## Prerequisites

Before you begin, ensure you have:

- **Raspberry Pi 3B+ or newer** (Raspberry Pi 4/5 recommended for optimal performance)
- **Raspberry Pi OS Bookworm** or newer (64-bit recommended)
- **Minimum 4GB RAM** (8GB recommended for Raspberry Pi 4/5)
- **32GB+ SD card** (64GB+ recommended for extensive memory storage)
- **Internet connection** (for API access and package installation)
- **USB microphone** (for voice input)
- **Speakers or audio output** (for voice synthesis)
- **Camera module or USB webcam** (optional, for vision features)

### Required Accounts & API Keys

- **Anthropic API Key** - For Claude AI access ([get yours here](https://console.anthropic.com/))
- **Optional**: OpenAI API Key - For Whisper STT (can use local Whisper alternative)

## Step 1: System Preparation

First, update your Raspberry Pi OS to ensure all packages are current:

```bash
sudo apt update && sudo apt upgrade -y
```

## Step 2: Install System Dependencies

Install required system packages:

```bash
# Core dependencies
sudo apt install -y python3 python3-pip python3-venv git

# Audio dependencies
sudo apt install -y portaudio19-dev python3-pyaudio espeak ffmpeg

# Camera dependencies (if using vision features)
sudo apt install -y python3-picamera2 libcamera-apps

# Optional: for better TTS quality
sudo apt install -y festival festvox-kallpc16k
```

## Step 3: Clone the Repository

Clone the M.O.L.O.C.H. 3.0 repository to your Raspberry Pi:

```bash
cd ~
git clone https://github.com/moloch00464-bit/documentation.git moloch_3.0
cd moloch_3.0
```

## Step 4: Create Python Virtual Environment

Set up an isolated Python environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

!!! tip
    You'll need to activate this virtual environment (`source venv/bin/activate`) every time you want to run M.O.L.O.C.H.

## Step 5: Install Python Dependencies

Install all required Python packages:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Key Dependencies Installed:

- **anthropic** - Claude API client
- **openai** - For Whisper STT
- **SpeechRecognition** - Voice input processing
- **pyttsx3** - Text-to-speech engine
- **Pillow** - Image processing for vision
- **requests** - Web search and API calls

## Step 6: Configure API Keys

Create your configuration file:

```bash
cp config.example.json config.json
nano config.json
```

Edit the configuration with your API keys:

```json
{
  "api_keys": {
    "anthropic": "YOUR_ANTHROPIC_API_KEY_HERE",
    "openai": "YOUR_OPENAI_API_KEY_HERE"
  },
  "model": "claude-3-opus-20240229",
  "voice": {
    "enabled": true,
    "engine": "pyttsx3",
    "rate": 150,
    "volume": 0.9
  },
  "vision": {
    "enabled": true,
    "camera_index": 0
  },
  "memory": {
    "max_context": 100000,
    "auto_save": true
  }
}
```

!!! warning
    Never commit your `config.json` file with real API keys to version control!

## Step 7: Test Audio Setup

Before running M.O.L.O.C.H., verify your audio configuration:

```bash
# Test microphone
arecord -d 3 test.wav
aplay test.wav

# Test speakers
speaker-test -t wav -c 2
```

## Step 8: Test Camera Setup (Optional)

If using vision features, test your camera:

```bash
# For Raspberry Pi Camera Module
libcamera-hello

# For USB webcam
v4l2-ctl --list-devices
```

## Step 9: Run M.O.L.O.C.H. 3.0

Now you're ready to launch M.O.L.O.C.H.!

### Text Mode

```bash
python3 moloch3.py
```

### Voice Mode

```bash
python3 moloch3_voice.py
```

### Vision Mode

```bash
python3 moloch3_vision.py
```

### Unified Mode (All Features)

```bash
python3 moloch3_unified.py
```

## Step 10: First-Time Setup

On first launch, M.O.L.O.C.H. will:

1. Initialize the memory database
2. Create personality profile
3. Set up temporal awareness
4. Calibrate voice settings (if using voice mode)

Follow the on-screen prompts to complete the initial setup.

## Autostart on Boot (Optional)

To have M.O.L.O.C.H. start automatically when your Raspberry Pi boots:

### Create Systemd Service

```bash
sudo nano /etc/systemd/system/moloch.service
```

Add the following content:

```ini
[Unit]
Description=M.O.L.O.C.H. 3.0 Autonomous AI System
After=network.target

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi/moloch_3.0
Environment="PATH=/home/pi/moloch_3.0/venv/bin"
ExecStart=/home/pi/moloch_3.0/venv/bin/python3 /home/pi/moloch_3.0/moloch3_unified.py
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start the service:

```bash
sudo systemctl daemon-reload
sudo systemctl enable moloch.service
sudo systemctl start moloch.service
```

Check status:

```bash
sudo systemctl status moloch.service
```

## Troubleshooting

### Audio Issues

**Problem**: No audio output

```bash
# Check audio devices
aplay -l

# Set default audio device
raspi-config
# Navigate to: System Options > Audio
```

**Problem**: Microphone not detected

```bash
# List recording devices
arecord -l

# Test with verbose output
python3 -c "import speech_recognition as sr; print(sr.Microphone.list_microphone_names())"
```

### Camera Issues

**Problem**: Camera not detected

```bash
# Enable camera interface
sudo raspi-config
# Navigate to: Interface Options > Camera

# Check camera status
vcgencmd get_camera
```

### API Connection Issues

**Problem**: Claude API errors

- Verify your API key is correct in `config.json`
- Check internet connectivity: `ping api.anthropic.com`
- Ensure sufficient API credits in your Anthropic account

### Performance Issues

**Problem**: Slow response times

- Consider using Claude Sonnet instead of Opus (faster, lower cost)
- Reduce `max_context` in configuration
- Use faster TTS engine (espeak instead of festival)

## Next Steps

- **[Configuration Guide](/docs/configuration/basic.md)** - Customize M.O.L.O.C.H. settings
- **[Usage Guide](/docs/usage/index.md)** - Learn how to interact effectively
- **[Features Overview](/docs/features/index.md)** - Explore all capabilities
- **[FAQ](/docs/moloch-faq.md)** - Common questions and answers

## Upgrading

To upgrade to a newer version:

```bash
cd ~/moloch_3.0
git pull origin main
source venv/bin/activate
pip install -r requirements.txt --upgrade
```

---

**Need help?** Check the [FAQ](/docs/moloch-faq.md) or [open an issue](https://github.com/moloch00464-bit/documentation/issues).
