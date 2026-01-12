#!/bin/bash
# ═══════════════════════════════════════════════════════════════════════════════
# M.O.L.O.C.H. 3.0 - Raspberry Pi 5 Installation
# ═══════════════════════════════════════════════════════════════════════════════

echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║  M.O.L.O.C.H. 3.0 - Raspberry Pi 5 Installation              ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo ""

# ═══════════════════════════════════════════════════════════════════════════════
# 1. System Update
# ═══════════════════════════════════════════════════════════════════════════════

echo "📦 System Update..."
sudo apt update
sudo apt upgrade -y

# ═══════════════════════════════════════════════════════════════════════════════
# 2. Install System Dependencies
# ═══════════════════════════════════════════════════════════════════════════════

echo ""
echo "📦 Installing system dependencies..."

# Audio
sudo apt install -y portaudio19-dev python3-pyaudio alsa-utils

# espeak (TTS fallback)
sudo apt install -y espeak espeak-ng

# Camera (Pi Camera)
sudo apt install -y python3-picamera2

# Camera (USB Webcam)
sudo apt install -y libopencv-dev python3-opencv

# Build tools
sudo apt install -y python3-dev build-essential git wget unzip

# ═══════════════════════════════════════════════════════════════════════════════
# 3. Python Virtual Environment
# ═══════════════════════════════════════════════════════════════════════════════

echo ""
echo "🐍 Setting up Python environment..."

# Create virtual environment
python3 -m venv ~/moloch_env

# Activate
source ~/moloch_env/bin/activate

# Upgrade pip
pip install --upgrade pip setuptools wheel

# ═══════════════════════════════════════════════════════════════════════════════
# 4. Install Python Dependencies
# ═══════════════════════════════════════════════════════════════════════════════

echo ""
echo "📦 Installing Python packages..."

# Install from requirements.txt
pip install -r requirements.txt

# ═══════════════════════════════════════════════════════════════════════════════
# 5. Download Vosk Model (German)
# ═══════════════════════════════════════════════════════════════════════════════

echo ""
echo "🧠 Downloading Vosk German model..."

VOSK_MODEL="vosk-model-small-de-0.15"
VOSK_URL="https://alphacephei.com/vosk/models/${VOSK_MODEL}.zip"

if [ ! -d "$HOME/vosk-model-de" ]; then
    cd ~
    wget -q --show-progress $VOSK_URL
    unzip -q ${VOSK_MODEL}.zip
    mv ${VOSK_MODEL} vosk-model-de
    rm ${VOSK_MODEL}.zip
    echo "✅ Vosk model installed: ~/vosk-model-de"
else
    echo "✅ Vosk model already installed"
fi

# ═══════════════════════════════════════════════════════════════════════════════
# 6. Download Piper TTS (Optional - High Quality German Voice)
# ═══════════════════════════════════════════════════════════════════════════════

echo ""
echo "🗣️  Installing Piper TTS..."

# Check if piper is already installed
if ! command -v piper &> /dev/null; then
    echo "📥 Downloading Piper..."

    # Download Piper binary for ARM64
    PIPER_URL="https://github.com/rhasspy/piper/releases/download/v1.2.0/piper_arm64.tar.gz"

    cd ~
    wget -q --show-progress $PIPER_URL
    tar -xzf piper_arm64.tar.gz
    sudo mv piper/piper /usr/local/bin/
    rm -rf piper piper_arm64.tar.gz

    echo "✅ Piper installed"
else
    echo "✅ Piper already installed"
fi

# Download German voice model
PIPER_VOICE_DIR="$HOME/.local/share/piper/voices"
mkdir -p $PIPER_VOICE_DIR

if [ ! -f "$PIPER_VOICE_DIR/de_DE-thorsten-medium.onnx" ]; then
    echo "📥 Downloading German voice..."
    cd $PIPER_VOICE_DIR
    wget -q --show-progress "https://huggingface.co/rhasspy/piper-voices/resolve/main/de/de_DE/thorsten/medium/de_DE-thorsten-medium.onnx"
    wget -q --show-progress "https://huggingface.co/rhasspy/piper-voices/resolve/main/de/de_DE/thorsten/medium/de_DE-thorsten-medium.onnx.json"
    echo "✅ German voice installed"
else
    echo "✅ German voice already installed"
fi

# ═══════════════════════════════════════════════════════════════════════════════
# 7. Copy M.O.L.O.C.H. Files
# ═══════════════════════════════════════════════════════════════════════════════

echo ""
echo "📂 Setting up M.O.L.O.C.H. files..."

# Install directory
INSTALL_DIR="$HOME/moloch_rpi"

# Create if not exists
mkdir -p $INSTALL_DIR

# Copy all files from current directory
cp -r . $INSTALL_DIR/

echo "✅ Files copied to $INSTALL_DIR"

# ═══════════════════════════════════════════════════════════════════════════════
# 8. API Key Setup
# ═══════════════════════════════════════════════════════════════════════════════

echo ""
echo "🔑 API Key Setup..."

# Check if API key is set
if [ -z "$ANTHROPIC_API_KEY" ]; then
    echo ""
    echo "⚠️  ANTHROPIC_API_KEY not set!"
    echo ""
    echo "To set your API key:"
    echo "  1. Get key from: https://console.anthropic.com/"
    echo "  2. Add to ~/.bashrc:"
    echo "     echo 'export ANTHROPIC_API_KEY=\"sk-ant-...\"' >> ~/.bashrc"
    echo "  3. Reload: source ~/.bashrc"
    echo ""
else
    echo "✅ ANTHROPIC_API_KEY is set"
fi

# ═══════════════════════════════════════════════════════════════════════════════
# 9. Test Audio
# ═══════════════════════════════════════════════════════════════════════════════

echo ""
echo "🔊 Testing audio..."

# Test speaker
echo "🗣️  Testing speaker (you should hear a voice)..."
espeak -v de "Test. Hörst du mich?"
sleep 1

# Test microphone
echo ""
echo "🎤 Testing microphone..."
echo "   (Recording 3 seconds...)"
arecord -d 3 -f cd /tmp/test.wav 2>/dev/null
if [ -f "/tmp/test.wav" ]; then
    echo "✅ Microphone working"
    rm /tmp/test.wav
else
    echo "❌ Microphone not working"
fi

# ═══════════════════════════════════════════════════════════════════════════════
# 10. Create Launch Scripts
# ═══════════════════════════════════════════════════════════════════════════════

echo ""
echo "🚀 Creating launch scripts..."

# Voice Mode
cat > ~/moloch_voice.sh << 'EOF'
#!/bin/bash
source ~/moloch_env/bin/activate
cd ~/moloch_rpi
python moloch3_rpi.py
EOF
chmod +x ~/moloch_voice.sh

# Vision Mode
cat > ~/moloch_vision.sh << 'EOF'
#!/bin/bash
source ~/moloch_env/bin/activate
cd ~/moloch_rpi
python moloch3_rpi.py -v
EOF
chmod +x ~/moloch_vision.sh

# Test Voice
cat > ~/moloch_test_voice.sh << 'EOF'
#!/bin/bash
source ~/moloch_env/bin/activate
cd ~/moloch_rpi
python voice_rpi.py
EOF
chmod +x ~/moloch_test_voice.sh

echo "✅ Launch scripts created:"
echo "   ~/moloch_voice.sh - Voice Mode"
echo "   ~/moloch_vision.sh - Vision Mode"
echo "   ~/moloch_test_voice.sh - Test Voice Only"

# ═══════════════════════════════════════════════════════════════════════════════
# DONE!
# ═══════════════════════════════════════════════════════════════════════════════

echo ""
echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║  ✅ Installation Complete!                                    ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo ""
echo "Next Steps:"
echo ""
echo "1. Set API Key (if not done):"
echo "   export ANTHROPIC_API_KEY='sk-ant-...'"
echo "   echo 'export ANTHROPIC_API_KEY=\"sk-ant-...\"' >> ~/.bashrc"
echo ""
echo "2. Test Voice System:"
echo "   ~/moloch_test_voice.sh"
echo ""
echo "3. Start M.O.L.O.C.H.:"
echo "   ~/moloch_voice.sh    # Voice Mode"
echo "   ~/moloch_vision.sh   # Vision Mode"
echo ""
echo "Troubleshooting:"
echo "  - No sound: Check alsamixer (run: alsamixer)"
echo "  - No mic: Check arecord -l (list devices)"
echo "  - Camera: Check /dev/video0 exists"
echo ""
