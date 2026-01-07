#!/bin/bash
# ═══════════════════════════════════════════════════════════════════════════════
# M.O.L.O.C.H. 3.1 UNIFIED - FINAL DEPLOYMENT SCRIPT
# ═══════════════════════════════════════════════════════════════════════════════
# Installiert M.O.L.O.C.H. 3.1 UNIFIED komplett neu
# NUR ANTHROPIC API KEY - KEIN OPENAI!
# VOICE: MP3 Format
# ═══════════════════════════════════════════════════════════════════════════════

set -e

echo ""
echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║     M.O.L.O.C.H. 3.1 UNIFIED - FINAL DEPLOYMENT               ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo ""

TARGET_DIR="$HOME/moloch_3.1_final"

# ═══════════════════════════════════════════════════════════════════════════════
# SCHRITT 1: Cleanup
# ═══════════════════════════════════════════════════════════════════════════════

echo "🗑️  CLEANUP alte Installationen..."
rm -rf "$TARGET_DIR" 2>/dev/null || true
echo "✅ Cleanup done"
echo ""

# ═══════════════════════════════════════════════════════════════════════════════
# SCHRITT 2: GitHub Code holen
# ═══════════════════════════════════════════════════════════════════════════════

echo "🌐 GitHub Code holen..."

# Repo clonen falls nicht vorhanden
if [ ! -d "$HOME/documentation" ]; then
    cd ~
    git clone https://github.com/moloch00464-bit/documentation.git
    cd documentation
else
    cd ~/documentation
    git fetch origin
fi

# Branch mit allen Fixes
git checkout claude/fix-moloch-imports-5zWsV
git pull origin claude/fix-moloch-imports-5zWsV

echo "✅ Code von GitHub geholt"
echo ""

# ═══════════════════════════════════════════════════════════════════════════════
# SCHRITT 3: Deploy
# ═══════════════════════════════════════════════════════════════════════════════

echo "🚀 Deploy nach $TARGET_DIR..."
cp -r ~/documentation/moloch_3.0 "$TARGET_DIR"
echo "✅ Code deployed"
echo ""

# ═══════════════════════════════════════════════════════════════════════════════
# SCHRITT 4: Verify Module
# ═══════════════════════════════════════════════════════════════════════════════

echo "🔍 Verify Module..."
CORE_COUNT=$(ls "$TARGET_DIR/core"/*.py 2>/dev/null | wc -l)
IO_COUNT=$(ls "$TARGET_DIR/moloch_io"/*.py 2>/dev/null | wc -l)

echo "   Core modules: $CORE_COUNT (sollte 14 sein)"
echo "   moloch_io modules: $IO_COUNT (sollte 3 sein)"

if [ "$CORE_COUNT" -lt 10 ] || [ "$IO_COUNT" -lt 2 ]; then
    echo "❌ FEHLER: Module fehlen!"
    exit 1
fi

echo "✅ Alle Module vorhanden"
echo ""

# ═══════════════════════════════════════════════════════════════════════════════
# SCHRITT 5: API Key Setup
# ═══════════════════════════════════════════════════════════════════════════════

echo "🔑 API Key Setup..."
echo ""
echo "WICHTIG: Du brauchst NUR deinen ANTHROPIC API Key!"
echo "         KEIN OpenAI Key nötig!"
echo ""
read -p "Anthropic API Key eingeben (oder Enter für später): " API_KEY

if [ -n "$API_KEY" ]; then
    sed -i "s/DEIN_ANTHROPIC_KEY_HIER/$API_KEY/g" "$TARGET_DIR/core/config.py"
    echo "✅ API Key gesetzt"
else
    echo "⚠️  Kein API Key - setze später mit:"
    echo "   nano $TARGET_DIR/core/config.py"
fi

echo ""

# ═══════════════════════════════════════════════════════════════════════════════
# SCHRITT 6: Permissions
# ═══════════════════════════════════════════════════════════════════════════════

echo "🔧 Permissions setzen..."
chmod +x "$TARGET_DIR/moloch3_unified.py"
echo "✅ Permissions OK"
echo ""

# ═══════════════════════════════════════════════════════════════════════════════
# FERTIG!
# ═══════════════════════════════════════════════════════════════════════════════

echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║  ✅ M.O.L.O.C.H. 3.1 UNIFIED INSTALLATION COMPLETE!           ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo ""
echo "📍 Location: $TARGET_DIR"
echo ""
echo "🚀 STARTEN:"
echo "   cd $TARGET_DIR"
echo "   python moloch3_unified.py          # Voice Mode"
echo "   python moloch3_unified.py -v       # Vision Mode"
echo ""
echo "🎤 VOICE:"
echo "   ✅ MP3 Format"
echo "   ✅ termux-microphone-record"
echo "   ✅ Google Speech API (kostenlos!)"
echo ""
echo "🔑 API:"
echo "   ✅ NUR Anthropic Claude API"
echo "   ❌ KEIN OpenAI nötig!"
echo ""
echo "🖤 VIEL ERFOLG!"
echo ""
