#!/bin/bash
###############################################################################
# M.O.L.O.C.H. 3.0 - WIDGET FIX
# ==============================
# Installiert Widgets korrekt (OHNE hardcoded Pfade!)
###############################################################################

set -e

echo "════════════════════════════════════════════════════════════════"
echo "  M.O.L.O.C.H. 3.0 - WIDGET FIX"
echo "  Installiert Widgets richtig für Termux:Widget"
echo "════════════════════════════════════════════════════════════════"
echo ""

# Auto-detect M.O.L.O.C.H. 3.0 directory
if [ -d "$HOME/documentation/moloch_3.0" ]; then
    MOLOCH_DIR="$HOME/documentation/moloch_3.0"
elif [ -d "$HOME/moloch_3.0" ]; then
    MOLOCH_DIR="$HOME/moloch_3.0"
else
    echo "❌ FEHLER: M.O.L.O.C.H. 3.0 Verzeichnis nicht gefunden!"
    echo "   Gesucht in:"
    echo "   - $HOME/documentation/moloch_3.0"
    echo "   - $HOME/moloch_3.0"
    exit 1
fi

echo "✅ M.O.L.O.C.H. 3.0 gefunden: $MOLOCH_DIR"
echo ""

# Shortcuts directory
SHORTCUTS_DIR="$HOME/.shortcuts"
mkdir -p "$SHORTCUTS_DIR"

echo "📁 Shortcuts-Verzeichnis: $SHORTCUTS_DIR"
echo ""

###############################################################################
# BACKUP ALTE WIDGETS
###############################################################################

echo "💾 Backup alte Widgets..."
if [ -f "$SHORTCUTS_DIR/M.O.L.O.C.H. Vision" ] || [ -f "$SHORTCUTS_DIR/MOLOCH_Vision.sh" ]; then
    BACKUP_DIR="$HOME/.shortcuts_backup_$(date +%Y%m%d_%H%M%S)"
    mkdir -p "$BACKUP_DIR"
    cp -r "$SHORTCUTS_DIR"/* "$BACKUP_DIR/" 2>/dev/null || true
    echo "   ✅ Backup erstellt: $BACKUP_DIR"
else
    echo "   ⚠️  Keine alten Widgets gefunden (OK für Neuinstallation)"
fi
echo ""

###############################################################################
# LÖSCHE ALTE WIDGETS
###############################################################################

echo "🗑️  Lösche alte/kaputte Widgets..."
rm -f "$SHORTCUTS_DIR/M.O.L.O.C.H."* 2>/dev/null || true
rm -f "$SHORTCUTS_DIR/MOLOCH_"* 2>/dev/null || true
echo "   ✅ Alte Widgets entfernt"
echo ""

###############################################################################
# ERSTELLE NEUE WIDGETS (MIT AUTO-DETECTED PATH!)
###############################################################################

echo "🔧 Erstelle neue Widgets..."

# ═══════════════════════════════════════════════════════════════════════════
# WIDGET 1: Voice Mode
# ═══════════════════════════════════════════════════════════════════════════

cat > "$SHORTCUTS_DIR/MOLOCH_Voice.sh" << 'WIDGET_VOICE_EOF'
#!/data/data/com.termux/files/usr/bin/bash
#
# M.O.L.O.C.H. 3.0 - Voice Mode Widget
# =====================================
# Homescreen Button: Voice Interaction
#

# Load API Keys from ~/.bashrc
source ~/.bashrc

# Auto-detect M.O.L.O.C.H. 3.0 directory
if [ -d "$HOME/documentation/moloch_3.0" ]; then
    cd "$HOME/documentation/moloch_3.0"
elif [ -d "$HOME/moloch_3.0" ]; then
    cd "$HOME/moloch_3.0"
else
    echo "❌ FEHLER: M.O.L.O.C.H. 3.0 nicht gefunden!"
    echo "Drücke ENTER..."
    read
    exit 1
fi

# Run Voice Mode
python3 moloch3_unified.py 2>&1

# Keep terminal open to see result
echo ""
echo "=================================="
echo "Drücke ENTER zum Schließen..."
echo "=================================="
read
WIDGET_VOICE_EOF

chmod +x "$SHORTCUTS_DIR/MOLOCH_Voice.sh"
echo "   ✅ MOLOCH_Voice.sh erstellt"

# ═══════════════════════════════════════════════════════════════════════════
# WIDGET 2: Vision Mode
# ═══════════════════════════════════════════════════════════════════════════

cat > "$SHORTCUTS_DIR/MOLOCH_Vision.sh" << 'WIDGET_VISION_EOF'
#!/data/data/com.termux/files/usr/bin/bash
#
# M.O.L.O.C.H. 3.0 - Vision Mode Widget
# ======================================
# Homescreen Button: Photo + Vision
#

# Load API Keys from ~/.bashrc
source ~/.bashrc

# Auto-detect M.O.L.O.C.H. 3.0 directory
if [ -d "$HOME/documentation/moloch_3.0" ]; then
    cd "$HOME/documentation/moloch_3.0"
elif [ -d "$HOME/moloch_3.0" ]; then
    cd "$HOME/moloch_3.0"
else
    echo "❌ FEHLER: M.O.L.O.C.H. 3.0 nicht gefunden!"
    echo "Drücke ENTER..."
    read
    exit 1
fi

# Run Vision Mode
python3 moloch3_unified.py -v 2>&1

# Keep terminal open to see result
echo ""
echo "=================================="
echo "Drücke ENTER zum Schließen..."
echo "=================================="
read
WIDGET_VISION_EOF

chmod +x "$SHORTCUTS_DIR/MOLOCH_Vision.sh"
echo "   ✅ MOLOCH_Vision.sh erstellt"

# ═══════════════════════════════════════════════════════════════════════════
# WIDGET 3: Interactive Mode (Text Chat)
# ═══════════════════════════════════════════════════════════════════════════

cat > "$SHORTCUTS_DIR/MOLOCH_Interactive.sh" << 'WIDGET_INTERACTIVE_EOF'
#!/data/data/com.termux/files/usr/bin/bash
#
# M.O.L.O.C.H. 3.0 - Interactive Mode Widget
# ===========================================
# Homescreen Button: Text Chat
#

# Load API Keys from ~/.bashrc
source ~/.bashrc

# Auto-detect M.O.L.O.C.H. 3.0 directory
if [ -d "$HOME/documentation/moloch_3.0" ]; then
    cd "$HOME/documentation/moloch_3.0"
elif [ -d "$HOME/moloch_3.0" ]; then
    cd "$HOME/moloch_3.0"
else
    echo "❌ FEHLER: M.O.L.O.C.H. 3.0 nicht gefunden!"
    echo "Drücke ENTER..."
    read
    exit 1
fi

# Run Interactive Mode
python3 moloch3_unified.py -i 2>&1

# Keep terminal open to see result
echo ""
echo "=================================="
echo "Drücke ENTER zum Schließen..."
echo "=================================="
read
WIDGET_INTERACTIVE_EOF

chmod +x "$SHORTCUTS_DIR/MOLOCH_Interactive.sh"
echo "   ✅ MOLOCH_Interactive.sh erstellt"

echo ""

###############################################################################
# VERIFICATION
###############################################################################

echo "✅ INSTALLATION ABGESCHLOSSEN!"
echo ""
echo "📊 INSTALLIERTE WIDGETS:"
ls -lh "$SHORTCUTS_DIR"/MOLOCH*.sh
echo ""

###############################################################################
# INSTRUCTIONS
###############################################################################

echo "════════════════════════════════════════════════════════════════"
echo "  NÄCHSTE SCHRITTE:"
echo "════════════════════════════════════════════════════════════════"
echo ""
echo "1. Installiere Termux:Widget (falls noch nicht installiert):"
echo "   pkg install termux-widget"
echo ""
echo "2. Widget zum Homescreen hinzufügen:"
echo "   - Long-press auf Homescreen"
echo "   - 'Widgets' auswählen"
echo "   - 'Termux:Widget' wählen"
echo "   - Widget platzieren"
echo ""
echo "3. Verfügbare Buttons:"
echo "   🎤 MOLOCH_Voice.sh       - Voice Mode (Sprechen)"
echo "   📷 MOLOCH_Vision.sh      - Vision Mode (Foto)"
echo "   💬 MOLOCH_Interactive.sh - Text Chat"
echo ""
echo "4. Test (optional):"
echo "   bash ~/.shortcuts/MOLOCH_Voice.sh"
echo ""
echo "════════════════════════════════════════════════════════════════"
