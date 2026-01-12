#!/bin/bash
#
# M.O.L.O.C.H. 3.0 - VOSK German STT Installation
# Installiert Vosk Offline Speech Recognition mit German Model
#
# VOSK ist BESSER als DeepSpeech:
# ✅ Bessere Erkennungsqualität
# ✅ Schneller
# ✅ Kleinere Models
# ✅ Aktiv maintained (2024+)
# ✅ Offline + Kostenlos

set -e  # Exit on error

echo "═══════════════════════════════════════════════════════════════"
echo "🎤 M.O.L.O.C.H. 3.0 - VOSK German STT Installation"
echo "═══════════════════════════════════════════════════════════════"
echo ""

# Paths
MOLOCH_DIR="$HOME/documentation/moloch_3.0"
VOSK_MODEL_DIR="$MOLOCH_DIR/vosk_models"
GERMAN_MODEL_NAME="vosk-model-small-de-0.15"
GERMAN_MODEL_URL="https://alphacephei.com/vosk/models/${GERMAN_MODEL_NAME}.zip"

# Step 1: Update packages
echo "📦 Step 1/5: Updating Termux packages..."
pkg update -y >/dev/null 2>&1 || echo "⚠️  Package update had warnings (continuing)"

# Step 2: Install dependencies
echo "🔧 Step 2/5: Installing dependencies..."
pkg install -y python python-pip wget unzip >/dev/null 2>&1 || {
    echo "❌ Failed to install dependencies!"
    exit 1
}
echo "   ✅ Python, pip, wget, unzip installed"

# Step 3: Install Vosk Python package
echo "🐍 Step 3/5: Installing Vosk Python package..."
pip install --upgrade pip >/dev/null 2>&1
pip install vosk sounddevice >/dev/null 2>&1 || {
    echo "❌ Failed to install Vosk!"
    exit 1
}
echo "   ✅ Vosk Python package installed"

# Step 4: Download German model
echo "🇩🇪 Step 4/5: Downloading German language model..."
echo "   Model: ${GERMAN_MODEL_NAME} (~45 MB)"

# Create model directory
mkdir -p "$VOSK_MODEL_DIR"
cd "$VOSK_MODEL_DIR"

# Check if already downloaded
if [ -d "$GERMAN_MODEL_NAME" ]; then
    echo "   ℹ️  Model already exists - skipping download"
else
    # Download with progress bar
    wget --show-progress -q "$GERMAN_MODEL_URL" -O "${GERMAN_MODEL_NAME}.zip" || {
        echo "❌ Failed to download German model!"
        echo "   URL: $GERMAN_MODEL_URL"
        exit 1
    }

    # Extract
    echo "   📂 Extracting model..."
    unzip -q "${GERMAN_MODEL_NAME}.zip" || {
        echo "❌ Failed to extract model!"
        exit 1
    }

    # Cleanup
    rm "${GERMAN_MODEL_NAME}.zip"
    echo "   ✅ German model downloaded and extracted"
fi

# Step 5: Test Vosk installation
echo "🧪 Step 5/5: Testing Vosk installation..."
python3 << 'EOF'
import sys
try:
    from vosk import Model
    import os

    model_path = os.path.expanduser("~/documentation/moloch_3.0/vosk_models/vosk-model-small-de-0.15")

    if not os.path.exists(model_path):
        print(f"❌ Model path not found: {model_path}")
        sys.exit(1)

    # Try to load model
    model = Model(model_path)
    print("   ✅ Vosk German model loaded successfully!")

except Exception as e:
    print(f"❌ Vosk test failed: {e}")
    sys.exit(1)
EOF

if [ $? -eq 0 ]; then
    echo ""
    echo "═══════════════════════════════════════════════════════════════"
    echo "✅ VOSK GERMAN STT ERFOLGREICH INSTALLIERT!"
    echo "═══════════════════════════════════════════════════════════════"
    echo ""
    echo "📍 Model Location:"
    echo "   $VOSK_MODEL_DIR/$GERMAN_MODEL_NAME"
    echo ""
    echo "🎯 Nächster Schritt:"
    echo "   M.O.L.O.C.H. 3.0 wird jetzt automatisch Vosk nutzen!"
    echo "   Test mit: python moloch3_unified.py --voice"
    echo ""
else
    echo ""
    echo "❌ Installation hatte Probleme!"
    echo "   Bitte Log überprüfen und nochmal versuchen."
    exit 1
fi
