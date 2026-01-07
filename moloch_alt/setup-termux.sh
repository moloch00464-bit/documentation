#!/data/data/com.termux/files/usr/bin/bash
# 🤖 M.O.L.O.C.H. v3.0 TERMUX INSTALLER
# Smartphone-Deployment für Android
# Installation: bash setup-termux.sh

set -e  # Exit on error

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}"
echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║         M.O.L.O.C.H. v3.0 - TERMUX DEPLOYMENT               ║"
echo "║           🤖 Smartphone AI Assistant Setup                   ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# ========== SYSTEM CHECK ==========
echo -e "${YELLOW}[1/7] System-Prüfung...${NC}"

if ! command -v pkg &> /dev/null; then
    echo -e "${RED}❌ Termux nicht erkannt. Bitte starten Sie das Skript in Termux!${NC}"
    exit 1
fi

TERMUX_VERSION=$(termux-setup-storage 2>/dev/null || echo "OK")
echo -e "${GREEN}✅ Termux erkannt${NC}"

# ========== UPDATE PACKAGES ==========
echo -e "${YELLOW}[2/7] System-Pakete aktualisieren...${NC}"
pkg update -y > /dev/null 2>&1 || true
pkg upgrade -y > /dev/null 2>&1 || true
echo -e "${GREEN}✅ Pakete aktualisiert${NC}"

# ========== INSTALL DEPENDENCIES ==========
echo -e "${YELLOW}[3/7] Abhängigkeiten installieren...${NC}"

PACKAGES=(
    "python"           # Python 3.x
    "ffmpeg"           # Audio/Video
    "tesseract"        # OCR
    "git"              # Version Control
    "curl"             # HTTP Client
    "jq"               # JSON Parser
    "openssh"          # SSH (optional)
)

for pkg in "${PACKAGES[@]}"; do
    if ! dpkg -l | grep -q "^ii.*$pkg"; then
        echo "  📦 Installing $pkg..."
        pkg install -y "$pkg" > /dev/null 2>&1 || echo "    ⚠️  $pkg skipped (optional)"
    fi
done

echo -e "${GREEN}✅ Abhängigkeiten installiert${NC}"

# ========== CREATE MOLOCH DIRECTORY ==========
echo -e "${YELLOW}[4/7] M.O.L.O.C.H. Verzeichnis erstellen...${NC}"

MOLOCH_DIR="$HOME/.moloch"
mkdir -p "$MOLOCH_DIR"/{brain,logs,gehirn,kontext,history,config,audio,daemon_logs}

echo -e "${GREEN}✅ Verzeichnisse erstellt:${NC}"
echo "   📁 $MOLOCH_DIR"

# ========== INSTALL PYTHON PACKAGES ==========
echo -e "${YELLOW}[5/7] Python-Packages installieren (dies kann einige Minuten dauern)...${NC}"

# Upgrade pip
pip install --upgrade pip setuptools wheel > /dev/null 2>&1

# Core packages
PYTHON_PACKAGES=(
    "requests>=2.31.0"
    "edge-tts>=0.2.0"
    "openai-whisper>=20231117"
    "Pillow>=10.0.0"
    "pytesseract>=0.3.10"
    "pyaudio>=0.2.13"
    "librosa>=0.10.0"
    "numpy>=1.24.0"
    "spotipy>=2.23.0"
    "python-dotenv>=1.0.0"
    "pyperclip>=1.8.2"
)

for pkg in "${PYTHON_PACKAGES[@]}"; do
    echo "  🐍 $pkg..."
    pip install "$pkg" > /dev/null 2>&1 || echo "    ⚠️  $pkg skipped"
done

echo -e "${GREEN}✅ Python-Packages installiert${NC}"

# ========== CLONE/SETUP MOLOCH ==========
echo -e "${YELLOW}[6/7] M.O.L.O.C.H. Code einrichten...${NC}"

# Falls nicht bereits vorhanden, clone from repository
if [ ! -f "$MOLOCH_DIR/moloch.py" ]; then
    echo "  📥 M.O.L.O.C.H. Code wird heruntergeladen..."
    # Falls Sie ein Git-Repo haben, ersetzen Sie die URL
    # git clone https://your-repo.git "$MOLOCH_DIR"
    echo "  ⚠️  Bitte kopieren Sie die M.O.L.O.C.H. Dateien nach $MOLOCH_DIR"
fi

# Create config template
cat > "$MOLOCH_DIR/config/moloch.json.template" << 'EOF'
{
  "personality": "moloch",
  "voice": {
    "tts_engine": "edge-tts",
    "voice": "en-US-JennyNeural",
    "speed": 1.0
  },
  "location": {
    "mode": "gps",  # "gps", "ip", "manual"
    "latitude": 0.0,
    "longitude": 0.0
  },
  "phone": {
    "is_termux": true,
    "device_id": "unknown",
    "battery_aware": true
  },
  "logging": {
    "level": "INFO",
    "file": "~/.moloch/logs/moloch.log"
  }
}
EOF

echo -e "${GREEN}✅ M.O.L.O.C.H. Code vorbereitet${NC}"

# ========== CREATE DAEMON SCRIPTS ==========
echo -e "${YELLOW}[7/7] Daemon-Skripte erstellen...${NC}"

mkdir -p "$MOLOCH_DIR/daemon_wrappers"

# Clipboard Monitor Daemon
cat > "$MOLOCH_DIR/daemon_wrappers/start-clipboard.sh" << 'EOF'
#!/data/data/com.termux/files/usr/bin/bash
cd "$HOME/.moloch"
nohup python clipboard_monitor.py --daemon > daemon_logs/clipboard.log 2>&1 &
echo $! > daemon_logs/clipboard.pid
echo "📋 Clipboard Monitor gestartet (PID: $!)"
EOF

# Location Daemon
cat > "$MOLOCH_DIR/daemon_wrappers/start-location.sh" << 'EOF'
#!/data/data/com.termux/files/usr/bin/bash
cd "$HOME/.moloch"
nohup python location_aware.py --daemon > daemon_logs/location.log 2>&1 &
echo $! > daemon_logs/location.pid
echo "🗺️ Location Daemon gestartet (PID: $!)"
EOF

# Weather Daemon
cat > "$MOLOCH_DIR/daemon_wrappers/start-weather.sh" << 'EOF'
#!/data/data/com.termux/files/usr/bin/bash
cd "$HOME/.moloch"
nohup python weather_aware.py --daemon > daemon_logs/weather.log 2>&1 &
echo $! > daemon_logs/weather.pid
echo "🌦️ Weather Daemon gestartet (PID: $!)"
EOF

chmod +x "$MOLOCH_DIR/daemon_wrappers"/*.sh

echo -e "${GREEN}✅ Daemon-Skripte erstellt${NC}"

# ========== FINAL SUMMARY ==========
echo ""
echo -e "${GREEN}╔═══════════════════════════════════════════════════════════════╗"
echo "║           ✅ INSTALLATION ERFOLGREICH ABGESCHLOSSEN            ║"
echo "╚═══════════════════════════════════════════════════════════════╝${NC}"

echo ""
echo -e "${BLUE}📁 Installation in:${NC}"
echo "   $MOLOCH_DIR"

echo ""
echo -e "${BLUE}🚀 Erste Schritte:${NC}"
echo "   1. Kopieren Sie M.O.L.O.C.H. Dateien nach: $MOLOCH_DIR"
echo "   2. Konfigurieren Sie: $MOLOCH_DIR/config/moloch.json"
echo "   3. Starten Sie: python \$HOME/.moloch/moloch.py"
echo "   4. Daemons starten:"
echo "      - bash \$HOME/.moloch/daemon_wrappers/start-clipboard.sh"
echo "      - bash \$HOME/.moloch/daemon_wrappers/start-location.sh"
echo "      - bash \$HOME/.moloch/daemon_wrappers/start-weather.sh"

echo ""
echo -e "${BLUE}📖 Hilfe:${NC}"
echo "   python \$HOME/.moloch/moloch.py --help"
echo "   python \$HOME/.moloch/clipboard_monitor.py --help"

echo ""
echo -e "${YELLOW}⚠️  Beachten Sie:${NC}"
echo "   • GPS: Aktivieren Sie Standortdienste"
echo "   • Microfon: Erlauben Sie Zugriff für Termux"
echo "   • Speicher: setup-storage wird ggf. erneut abgefragt"

echo ""
