#!/data/data/com.termux/files/usr/bin/bash
#
# M.O.L.O.C.H. 3.0 - Installation Script
# ========================================
# Installiert M.O.L.O.C.H. 3.0 auf Termux
#

echo ""
echo "🤖 M.O.L.O.C.H. 3.0 - Installation"
echo "=================================="
echo ""

# Check if running in Termux
if [ ! -d "/data/data/com.termux" ]; then
    echo "❌ Nicht in Termux! Bitte in Termux ausführen."
    exit 1
fi

echo "📦 Installing dependencies..."
pip install -q -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ Dependency installation failed!"
    exit 1
fi

echo "✅ Dependencies installed"
echo ""

# Check API Keys
echo "🔑 Checking API Keys..."

if [ -z "$ANTHROPIC_API_KEY" ]; then
    echo "⚠️ ANTHROPIC_API_KEY not set!"
    echo ""
    echo "   Set in ~/.bashrc:"
    echo '   export ANTHROPIC_API_KEY="your-anthropic-key"'
    echo ""
    MISSING_KEYS=1
fi

# NOTE: OPENAI_API_KEY no longer required - using native Termux STT

if [ -z "$MISSING_KEYS" ]; then
    echo "✅ API Key found"
fi

echo ""

# Make moloch executable
echo "🔧 Making moloch command executable..."
chmod +x moloch

# Create symlink in ~/bin/
echo "🔗 Creating 'moloch' command..."

mkdir -p ~/bin

if [ -L ~/bin/moloch ]; then
    rm ~/bin/moloch
fi

ln -s ~/moloch_3.0/moloch ~/bin/moloch

# Add ~/bin to PATH if not already there
if [[ ":$PATH:" != *":$HOME/bin:"* ]]; then
    echo ""
    echo "📝 Adding ~/bin to PATH..."
    echo 'export PATH="$HOME/bin:$PATH"' >> ~/.bashrc
    echo "   Please run: source ~/.bashrc"
fi

echo ""
echo "✅ Installation complete!"
echo ""
echo "🚀 Start M.O.L.O.C.H. with:"
echo "   moloch                    # Voice Mode"
echo "   moloch -t \"Hey!\"          # Text Mode"
echo "   moloch -a \"Was siehst du?\" # Vision Mode"
echo "   moloch -i                 # Interactive Mode"
echo ""

if [ ! -z "$MISSING_KEYS" ]; then
    echo "⚠️ Don't forget to set API Keys in ~/.bashrc!"
    echo ""
fi

echo "🖤 Dark Side Energy! Let's go! 🖤"
echo ""
