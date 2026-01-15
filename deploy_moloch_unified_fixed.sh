#!/bin/bash
# ═══════════════════════════════════════════════════════════════════════════════
# M.O.L.O.C.H. 3.1 UNIFIED - ONE-COMMAND DEPLOYMENT
# ═══════════════════════════════════════════════════════════════════════════════
# Deployed M.O.L.O.C.H. 3.1 UNIFIED mit allen Features!
# ═══════════════════════════════════════════════════════════════════════════════

set -e

echo ""
echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║  🤖 M.O.L.O.C.H. 3.1 UNIFIED - ONE-COMMAND DEPLOYMENT 🤖     ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo ""

TARGET_DIR="$HOME/moloch_unified"

# ═══════════════════════════════════════════════════════════════════════════════
# STEP 1: Backup existierendes System
# ═══════════════════════════════════════════════════════════════════════════════

if [ -d "$TARGET_DIR" ]; then
    echo "📦 Backup altes System..."
    BACKUP_NAME="moloch_unified_backup_$(date +%Y%m%d_%H%M%S)"
    mv "$TARGET_DIR" "$HOME/$BACKUP_NAME"
    echo "✅ Backup: ~/$BACKUP_NAME"
fi

# ═══════════════════════════════════════════════════════════════════════════════
# STEP 2: GitHub Code holen
# ═══════════════════════════════════════════════════════════════════════════════

echo ""
echo "🌐 Download Code von GitHub..."

cd ~

# Clone oder update repo
if [ ! -d "$HOME/documentation" ]; then
    git clone https://github.com/moloch00464-bit/documentation.git
fi

cd ~/documentation
git fetch origin claude/review-moloch-architecture-KFibr
git checkout claude/review-moloch-architecture-KFibr
git pull origin claude/review-moloch-architecture-KFibr

echo "✅ Code von GitHub geholt"

# ═══════════════════════════════════════════════════════════════════════════════
# STEP 3: Deploy nach ~/moloch_unified/
# ═══════════════════════════════════════════════════════════════════════════════

echo ""
echo "🚀 Deploy nach $TARGET_DIR..."

# Copy entire moloch_3.0 directory
cp -r ~/documentation/moloch_3.0 "$TARGET_DIR"

echo "✅ Code deployed"

# ═══════════════════════════════════════════════════════════════════════════════
# STEP 4: Memory Migration (2.0 → 3.1)
# ═══════════════════════════════════════════════════════════════════════════════

echo ""
echo "🧠 Memory Migration (M.O.L.O.C.H. 2.0 → 3.1)..."

mkdir -p "$TARGET_DIR/data"

# Copy 2.0 memories if they exist
if [ -f "$HOME/moloch/history.json" ]; then
    cp "$HOME/moloch/history.json" "$TARGET_DIR/data/"
    SIZE=$(ls -lh "$TARGET_DIR/data/history.json" | awk '{print $5}')
    echo "  ✅ history.json ($SIZE)"
else
    echo "  ⚠️  history.json nicht gefunden (OK für fresh install)"
fi

if [ -f "$HOME/moloch/langzeit.json" ]; then
    cp "$HOME/moloch/langzeit.json" "$TARGET_DIR/data/"
    echo "  ✅ langzeit.json"
else
    echo "  ⚠️  langzeit.json nicht gefunden (OK für fresh install)"
fi

if [ -d "$HOME/moloch/brain" ]; then
    cp -r "$HOME/moloch/brain" "$TARGET_DIR/data/"
    FILES=$(find "$TARGET_DIR/data/brain" -type f 2>/dev/null | wc -l)
    echo "  ✅ brain/ ($FILES files)"
else
    echo "  ⚠️  brain/ nicht gefunden (OK für fresh install)"
fi

# ═══════════════════════════════════════════════════════════════════════════════
# STEP 5: API Key Setup
# ═══════════════════════════════════════════════════════════════════════════════

echo ""
echo "🔑 API Key Setup..."

# Try to extract from 2.0
if [ -f "$HOME/moloch/moloch.py" ]; then
    ANTHROPIC_KEY=$(grep -oP 'sk-ant-api03-[A-Za-z0-9_-]+' "$HOME/moloch/moloch.py" 2>/dev/null | head -1)

    if [ -n "$ANTHROPIC_KEY" ]; then
        # Set in config.py
        sed -i "s/DEIN_ANTHROPIC_KEY_HIER/$ANTHROPIC_KEY/g" "$TARGET_DIR/core/config.py"
        echo "✅ API Key automatisch gesetzt: ${ANTHROPIC_KEY:0:20}..."
    else
        echo "⚠️  Kein API Key in 2.0 gefunden"
    fi
else
    echo "⚠️  moloch.py nicht gefunden"
fi

# Check if key is set
if grep -q "DEIN_ANTHROPIC_KEY_HIER" "$TARGET_DIR/core/config.py"; then
    echo ""
    echo "📝 WICHTIG: Setze deinen API Key!"
    echo "   nano $TARGET_DIR/core/config.py"
    echo "   Oder: export ANTHROPIC_API_KEY='sk-ant-api03-...'"
fi

# ═══════════════════════════════════════════════════════════════════════════════
# STEP 6: Permissions
# ═══════════════════════════════════════════════════════════════════════════════

echo ""
echo "🔧 Setze Permissions..."
chmod +x "$TARGET_DIR/moloch3_unified.py"
echo "✅ Permissions gesetzt"

# ═══════════════════════════════════════════════════════════════════════════════
# STEP 7: Verify Installation
# ═══════════════════════════════════════════════════════════════════════════════

echo ""
echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║  ✅ M.O.L.O.C.H. 3.1 UNIFIED DEPLOYMENT COMPLETE!             ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo ""

echo "📊 Installation Summary:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

echo "📁 Location: $TARGET_DIR"
echo ""

echo "📦 Modules:"
echo "  ├── moloch3_unified.py ($(ls -lh $TARGET_DIR/moloch3_unified.py | awk '{print $5}'))"
echo "  ├── core/ ($(ls $TARGET_DIR/core/*.py 2>/dev/null | wc -l) modules)"
echo "  └── moloch_io/ ($(ls $TARGET_DIR/moloch_io/*.py 2>/dev/null | wc -l) modules)"
echo ""

echo "🧠 Memory:"
if [ -f "$TARGET_DIR/data/history.json" ]; then
    echo "  ✅ history.json ($(ls -lh $TARGET_DIR/data/history.json | awk '{print $5}'))"
else
    echo "  ➖ history.json (fresh)"
fi

if [ -d "$TARGET_DIR/data/brain" ]; then
    echo "  ✅ brain/ ($(find $TARGET_DIR/data/brain -type f 2>/dev/null | wc -l) files)"
else
    echo "  ➖ brain/ (fresh)"
fi
echo ""

echo "🎭 Features:"
echo "  ✅ Emotion Detection (from 2.0)"
echo "  ✅ Knowledge Graph (from 2.0)"
echo "  ✅ Internet (web_search)"
echo "  ✅ Voice I/O (Google Speech API)"
echo "  ✅ Vision (termux-camera)"
echo "  ✅ Tool Calling (bash, files, brain)"
echo "  ✅ Self-Modification"
echo "  ✅ Persistent Learning"
echo "  ✅ Location Tracking"
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

echo "🚀 STARTEN:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "  cd $TARGET_DIR"
echo "  python moloch3_unified.py          # Voice Mode (default)"
echo "  python moloch3_unified.py -v       # Vision Mode"
echo ""

echo "💡 BEISPIELE:"
echo "  'Alter, wie spät ist es?'          → Local command (FREE!)"
echo "  'Kennst du noch Rebecca?'          → Memory + Emotion"
echo "  'Such mal nach Sierra Veins'       → Web Search"
echo ""

echo "🖤 VIEL ERFOLG MIT M.O.L.O.C.H. 3.1 UNIFIED!"
echo ""
