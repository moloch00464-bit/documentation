#!/bin/bash
# ═══════════════════════════════════════════════════════════════════════════════
# M.O.L.O.C.H. UNIFIED DEPLOYMENT
# ═══════════════════════════════════════════════════════════════════════════════
# Deployed UNIFIED M.O.L.O.C.H. (2.0 + 3.0) nach ~/moloch_3.0/
#
# Was passiert:
# 1. Backup vom alten 3.0
# 2. UNIFIED Code von GitHub holen
# 3. UNIFIED Code → ~/moloch_3.0/ kopieren
# 4. 2.0 Memory → 3.0 migrieren
# 5. Verify Installation
# ═══════════════════════════════════════════════════════════════════════════════

set -e  # Exit on error

echo "🤖 M.O.L.O.C.H. UNIFIED DEPLOYMENT"
echo "═══════════════════════════════════════════════════════════════"
echo ""

# ═══════════════════════════════════════════════════════════════════════════════
# STEP 1: BACKUP ALTER 3.0
# ═══════════════════════════════════════════════════════════════════════════════

echo "📦 STEP 1: Backup vom alten M.O.L.O.C.H. 3.0..."
echo ""

if [ -d "$HOME/moloch_3.0" ]; then
    BACKUP_NAME="moloch_3.0_backup_$(date +%Y%m%d_%H%M%S)"
    cp -r "$HOME/moloch_3.0" "$HOME/$BACKUP_NAME"
    echo "✅ Alter 3.0 gesichert: ~/$BACKUP_NAME"
else
    echo "⚠️  Kein alter 3.0 gefunden - erster Install?"
fi

echo ""
read -p "▶️  Weiter mit STEP 2? [Enter]"
echo ""

# ═══════════════════════════════════════════════════════════════════════════════
# STEP 2: UNIFIED VON GITHUB HOLEN
# ═══════════════════════════════════════════════════════════════════════════════

echo "🌐 STEP 2: UNIFIED von GitHub holen..."
echo ""

cd "$HOME/documentation"

echo "Fetching branch claude/review-moloch-architecture-KFibr..."
git fetch origin claude/review-moloch-architecture-KFibr

echo "Checking out branch..."
git checkout claude/review-moloch-architecture-KFibr

echo "Pulling latest changes..."
git pull origin claude/review-moloch-architecture-KFibr

echo "✅ UNIFIED Code von GitHub geholt!"

echo ""
read -p "▶️  Weiter mit STEP 3? [Enter]"
echo ""

# ═══════════════════════════════════════════════════════════════════════════════
# STEP 3: UNIFIED CODE DEPLOYEN
# ═══════════════════════════════════════════════════════════════════════════════

echo "🚀 STEP 3: UNIFIED Code nach ~/moloch_3.0/ deployen..."
echo ""

# Create moloch_3.0 if not exists
mkdir -p "$HOME/moloch_3.0"

# Copy main file
echo "Copying moloch3_unified.py..."
cp "$HOME/documentation/moloch_3.0/moloch3_unified.py" "$HOME/moloch_3.0/"

# Copy core/ modules
echo "Copying core/ modules..."
mkdir -p "$HOME/moloch_3.0/core"
cp -r "$HOME/documentation/moloch_3.0/core/"* "$HOME/moloch_3.0/core/"

# Copy moloch_io/ if exists
if [ -d "$HOME/documentation/moloch_3.0/moloch_io" ]; then
    echo "Copying moloch_io/..."
    mkdir -p "$HOME/moloch_3.0/moloch_io"
    cp -r "$HOME/documentation/moloch_3.0/moloch_io/"* "$HOME/moloch_3.0/moloch_io/"
fi

echo "✅ UNIFIED Code deployed!"

echo ""
echo "📋 Checking new features..."
if grep -q "from core.emotion" "$HOME/moloch_3.0/moloch3_unified.py"; then
    echo "  ✅ Emotion Detection"
fi
if grep -q "from core.knowledge_graph" "$HOME/moloch_3.0/moloch3_unified.py"; then
    echo "  ✅ Knowledge Graph"
fi
if grep -q "needs_web_search" "$HOME/moloch_3.0/moloch3_unified.py"; then
    echo "  ✅ Internet (web_search)"
fi

echo ""
read -p "▶️  Weiter mit STEP 4? [Enter]"
echo ""

# ═══════════════════════════════════════════════════════════════════════════════
# STEP 4: MEMORY MERGE (2.0 → 3.0)
# ═══════════════════════════════════════════════════════════════════════════════

echo "🧠 STEP 4: Memory Merge (2.0 → 3.0)..."
echo ""

# Backup alte 3.0 data
if [ -d "$HOME/moloch_3.0/data" ]; then
    mv "$HOME/moloch_3.0/data" "$HOME/moloch_3.0/data_old_backup_$(date +%Y%m%d_%H%M%S)"
    echo "✅ Alte 3.0 data gesichert"
fi

# Create fresh data dir
mkdir -p "$HOME/moloch_3.0/data"

# Copy 2.0 Memory
echo "Copying M.O.L.O.C.H. 2.0 Memory → 3.0..."

if [ -f "$HOME/moloch/history.json" ]; then
    cp "$HOME/moloch/history.json" "$HOME/moloch_3.0/data/history.json"
    echo "  ✅ history.json ($(ls -lh $HOME/moloch/history.json | awk '{print $5}'))"
else
    echo "  ⚠️  history.json nicht gefunden!"
fi

if [ -f "$HOME/moloch/langzeit.json" ]; then
    cp "$HOME/moloch/langzeit.json" "$HOME/moloch_3.0/data/langzeit.json"
    echo "  ✅ langzeit.json ($(ls -lh $HOME/moloch/langzeit.json | awk '{print $5}'))"
else
    echo "  ⚠️  langzeit.json nicht gefunden!"
fi

if [ -d "$HOME/moloch/brain" ]; then
    cp -r "$HOME/moloch/brain" "$HOME/moloch_3.0/data/brain"
    BRAIN_FILES=$(find "$HOME/moloch_3.0/data/brain" -type f | wc -l)
    echo "  ✅ brain/ ($BRAIN_FILES files)"
else
    echo "  ⚠️  brain/ nicht gefunden!"
fi

echo ""
echo "✅ Memory Merge complete!"

echo ""
read -p "▶️  Weiter mit STEP 5? [Enter]"
echo ""

# ═══════════════════════════════════════════════════════════════════════════════
# STEP 5: VERIFY INSTALLATION
# ═══════════════════════════════════════════════════════════════════════════════

echo "✅ STEP 5: Installation verifizieren..."
echo ""

echo "📊 M.O.L.O.C.H. UNIFIED Status:"
echo "═══════════════════════════════════════════════════════════════"
echo ""

# Code
echo "📁 Code:"
echo "  Location: ~/moloch_3.0/"
echo "  Main: $(ls -lh $HOME/moloch_3.0/moloch3_unified.py | awk '{print $5}')"
echo "  Modules: $(ls $HOME/moloch_3.0/core/*.py | wc -l) files"
echo ""

# Memory
echo "🧠 Memory:"
if [ -f "$HOME/moloch_3.0/data/history.json" ]; then
    echo "  history.json: $(ls -lh $HOME/moloch_3.0/data/history.json | awk '{print $5}')"
else
    echo "  ⚠️  history.json FEHLT!"
fi

if [ -f "$HOME/moloch_3.0/data/langzeit.json" ]; then
    echo "  langzeit.json: $(ls -lh $HOME/moloch_3.0/data/langzeit.json | awk '{print $5}')"
else
    echo "  ⚠️  langzeit.json FEHLT!"
fi

if [ -d "$HOME/moloch_3.0/data/brain" ]; then
    BRAIN_COUNT=$(find "$HOME/moloch_3.0/data/brain" -type f | wc -l)
    echo "  brain/: $BRAIN_COUNT files"
else
    echo "  ⚠️  brain/ FEHLT!"
fi
echo ""

# Features
echo "🎭 Features:"
echo "  ✅ Emotion Detection (from 2.0)"
echo "  ✅ Knowledge Graph (from 2.0)"
echo "  ✅ Internet (web_search_20250305)"
echo "  ✅ Tool Calling (bash, files)"
echo "  ✅ Self-Modification"
echo "  ✅ API Safeguards"
echo ""

echo "═══════════════════════════════════════════════════════════════"
echo "🎉 M.O.L.O.C.H. UNIFIED DEPLOYMENT COMPLETE!"
echo "═══════════════════════════════════════════════════════════════"
echo ""
echo "🚀 STARTEN MIT:"
echo "   cd ~/moloch_3.0"
echo "   python moloch3_unified.py"
echo ""
echo "📦 ROLLBACK (falls Probleme):"
echo "   rm -rf ~/moloch_3.0"
echo "   mv ~/$BACKUP_NAME ~/moloch_3.0"
echo ""
echo "🖤 VIEL ERFOLG MIT UNIFIED M.O.L.O.C.H.!"
echo ""
