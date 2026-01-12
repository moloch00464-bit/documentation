# M.O.L.O.C.H. 3.0 Raspberry Pi Installation - CORRECTED VERSION

This is the FIXED version of the installation guide with all errors corrected.

---

# Installing M.O.L.O.C.H. 3.0 on Raspberry Pi

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

---

## Step 1: System Preparation

First, update your Raspberry Pi OS to ensure all packages are current:

```bash
sudo apt update && sudo apt upgrade -y
```

---

## Step 2: Install System Dependencies

Install required system packages:

```bash
# Core dependencies
sudo apt install -y python3 python3-pip python3-venv git

# Audio dependencies
sudo apt install -y portaudio19-dev python3-pyaudio espeak ffmpeg

# Camera dependencies (if using vision features)
# Try picamera2 first (for Bookworm), fallback to legacy
sudo apt install -y python3-picamera2 libcamera-apps || \
  sudo apt install -y python3-picamera

# Optional: for better TTS quality
sudo apt install -y festival festvox-kallpc16k
```

### Add User to Audio Group

This is required for microphone access:

```bash
# Add your user to the audio group
sudo usermod -a -G audio $USER

# Verify group membership
groups | grep audio && echo "✅ Audio group OK" || echo "⚠️ Need to logout/login"
```

**Important**: You must **logout and login** (or reboot) for the group change to take effect!

---

## Step 3: Clone the Repository **[CORRECTED]**

⚠️ **IMPORTANT**: The M.O.L.O.C.H. 3.0 code is currently on a specific branch. Use ONE of these options:

### Option A: If PR #1 has been merged to main

```bash
cd ~
git clone https://github.com/moloch00464-bit/documentation.git moloch_3.0
cd moloch_3.0
```

### Option B: Use specific branch (if PR not yet merged)

```bash
cd ~
git clone -b claude/moloch-3-upgrade-uaAzw https://github.com/moloch00464-bit/documentation.git moloch_3.0
cd moloch_3.0
```

### Verify You Have the Correct Code

```bash
# Check that M.O.L.O.C.H. code files exist
ls moloch3.py core/ moloch_io/ tools/ 2>/dev/null && \
  echo "✅ M.O.L.O.C.H. 3.0 code found" || \
  echo "❌ ERROR: This is documentation only! Use Option B above"
```

---

## Step 4: Create Python Virtual Environment

Set up an isolated Python environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

!!! tip
    You'll need to activate this virtual environment (`source venv/bin/activate`) every time you want to run M.O.L.O.C.H.

---

## Step 5: Install Python Dependencies

Install all required Python packages:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Expected Dependencies

The requirements.txt should include:

- **anthropic** - Claude API client
- **openai** - For Whisper STT (optional)
- **SpeechRecognition** - Voice input processing
- **pyttsx3** - Text-to-speech engine
- **Pillow** - Image processing for vision
- **opencv-python** OR **picamera2** - Camera interface
- **requests** - Web search and API calls
- **sqlite3** - (built-in) Memory database

### Verify Installation

```bash
# Test that key packages are available
python3 << 'VERIFY'
try:
    import anthropic
    import speech_recognition
    import pyttsx3
    from PIL import Image
    print("✅ All critical dependencies installed successfully")
except ImportError as e:
    print(f"❌ Missing dependency: {e}")
VERIFY
```

---

## Step 6: Configure API Keys **[CORRECTED]**

### Option A: If config.example.json exists

```bash
cp config.example.json config.json
nano config.json
```

### Option B: Create config.json manually

If `config.example.json` doesn't exist, create `config.json` from scratch:

```bash
cat > config.json << 'EOF'
{
  "api_keys": {
    "anthropic": "YOUR_ANTHROPIC_API_KEY_HERE",
    "openai": "YOUR_OPENAI_API_KEY_HERE"
  },
  "model": "claude-3-sonnet-20240229",
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
EOF
```

### Edit and Add Your API Key

```bash
nano config.json
```

Replace `YOUR_ANTHROPIC_API_KEY_HERE` with your actual API key from https://console.anthropic.com/

!!! warning
    Never commit your `config.json` file with real API keys to version control!

---

## Step 7: Test Audio Setup

Before running M.O.L.O.C.H., verify your audio configuration:

```bash
# Test microphone
arecord -d 3 test.wav
aplay test.wav

# Test speakers
speaker-test -t wav -c 2 -l 1
```

If audio doesn't work, check:

```bash
# List audio devices
arecord -l
aplay -l

# Check if you're in audio group (after logout/login)
groups | grep audio
```

---

## Step 8: Test Camera Setup (Optional)

If using vision features, test your camera:

```bash
# For Raspberry Pi Camera Module
libcamera-hello --timeout 2000

# For USB webcam
v4l2-ctl --list-devices
```

---

## Step 9: Run M.O.L.O.C.H. 3.0

Now you're ready to launch M.O.L.O.C.H.!

### Test Mode (Verify Everything Works)

```bash
python3 moloch3.py
```

If this runs without errors, M.O.L.O.C.H. is installed correctly!

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

---

## Step 10: First-Time Setup

On first launch, M.O.L.O.C.H. will:

1. Initialize the memory database
2. Create personality profile
3. Set up temporal awareness
4. Calibrate voice settings (if using voice mode)

Follow the on-screen prompts to complete the initial setup.

---

## Autostart on Boot (Optional) **[CORRECTED]**

To have M.O.L.O.C.H. start automatically when your Raspberry Pi boots:

### Create Systemd Service

```bash
sudo nano /etc/systemd/system/moloch.service
```

Add the following content (replacing `YOUR_USERNAME` with your actual username):

```ini
[Unit]
Description=M.O.L.O.C.H. 3.0 Autonomous AI System
After=network.target

[Service]
Type=simple
User=YOUR_USERNAME
WorkingDirectory=/home/YOUR_USERNAME/moloch_3.0
Environment="PATH=/home/YOUR_USERNAME/moloch_3.0/venv/bin"
ExecStart=/home/YOUR_USERNAME/moloch_3.0/venv/bin/python3 /home/YOUR_USERNAME/moloch_3.0/moloch3_unified.py
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Or use environment variables automatically:

```bash
# Create service file with automatic path substitution
sudo bash -c "cat > /etc/systemd/system/moloch.service" << EOF
[Unit]
Description=M.O.L.O.C.H. 3.0 Autonomous AI System
After=network.target

[Service]
Type=simple
User=$(whoami)
WorkingDirectory=${HOME}/moloch_3.0
Environment="PATH=${HOME}/moloch_3.0/venv/bin"
ExecStart=${HOME}/moloch_3.0/venv/bin/python3 ${HOME}/moloch_3.0/moloch3_unified.py
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF
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

---

## Troubleshooting

### "Module not found" Errors

Make sure virtual environment is activated:

```bash
cd ~/moloch_3.0
source venv/bin/activate
pip install -r requirements.txt
```

### Audio Not Working

```bash
# Check audio devices
aplay -l

# Set default audio device
raspi-config
# Navigate to: System Options > Audio

# Verify you're in audio group (reboot if just added)
groups | grep audio
```

### Camera Not Working

```bash
# Enable camera interface
sudo raspi-config
# Navigate to: Interface Options > Camera

# Check camera status
vcgencmd get_camera

# Test camera
libcamera-hello --timeout 2000
```

### API Connection Errors

- Verify your API key is correct in `config.json`
- Check internet connectivity: `ping api.anthropic.com`
- Ensure sufficient API credits in your Anthropic account

---

## Upgrading **[CORRECTED]**

To upgrade to a newer version:

### If using main branch:

```bash
cd ~/moloch_3.0
git pull origin main
source venv/bin/activate
pip install -r requirements.txt --upgrade
```

### If using specific branch:

```bash
cd ~/moloch_3.0
git pull origin claude/moloch-3-upgrade-uaAzw
source venv/bin/activate
pip install -r requirements.txt --upgrade
```

---

## Next Steps

- **[Configuration Guide](/docs/configuration/basic.md)** - Customize M.O.L.O.C.H. settings
- **[Usage Guide](/docs/usage/index.md)** - Learn how to interact effectively
- **[Features Overview](/docs/features/index.md)** - Explore all capabilities
- **[FAQ](/docs/moloch-faq.md)** - Common questions and answers

---

**Need help?** Check the [FAQ](/docs/moloch-faq.md) or [open an issue](https://github.com/moloch00464-bit/documentation/issues).

---

## Summary of Corrections

This fixed version includes:

1. ✅ Correct repository cloning (with branch option)
2. ✅ Verification steps after each major step
3. ✅ Audio group membership instructions
4. ✅ Fallback for picamera2 installation
5. ✅ Manual config.json creation if example doesn't exist
6. ✅ Python dependency verification
7. ✅ Systemd service with variable substitution
8. ✅ Correct upgrade commands for both branches
9. ✅ Better error checking and troubleshooting
10. ✅ Clear warnings about logout/reboot requirements
