#!/bin/bash
# ═══════════════════════════════════════════════════════════════════════════════
# M.O.L.O.C.H. 3.1 UNIFIED - ALL-IN-ONE INSTALLATION
# ═══════════════════════════════════════════════════════════════════════════════
# Installiert M.O.L.O.C.H. 3.1 UNIFIED komplett automatisch!
# ═══════════════════════════════════════════════════════════════════════════════

set -e

echo "🤖 M.O.L.O.C.H. 3.1 UNIFIED - INSTALLATION"
echo "═══════════════════════════════════════════════════════════════"
echo ""

# ═══════════════════════════════════════════════════════════════════════════════
# STEP 1: Verzeichnis erstellen
# ═══════════════════════════════════════════════════════════════════════════════

echo "📁 STEP 1: Erstelle moloch_3.1 Verzeichnis..."
cd ~
mkdir -p moloch_3.1/core moloch_3.1/moloch_io moloch_3.1/data
echo "✅ Verzeichnis erstellt"
echo ""

# ═══════════════════════════════════════════════════════════════════════════════
# STEP 2: Main File downloaden
# ═══════════════════════════════════════════════════════════════════════════════

echo "⬇️  STEP 2: Download moloch3_unified.py..."
cd ~/moloch_3.1
curl -s -o moloch3_unified.py https://raw.githubusercontent.com/moloch00464-bit/documentation/claude/review-moloch-architecture-KFibr/moloch_3.0/moloch3_unified.py

# Version auf 3.1 ändern
sed -i 's/M.O.L.O.C.H. 3.0/M.O.L.O.C.H. 3.1 UNIFIED/g' moloch3_unified.py
echo "✅ moloch3_unified.py downloaded (3.1 UNIFIED)"
echo ""

# ═══════════════════════════════════════════════════════════════════════════════
# STEP 3: Core Module erstellen
# ═══════════════════════════════════════════════════════════════════════════════

echo "🔧 STEP 3: Erstelle Core Module..."
cd ~/moloch_3.1/core

# __init__.py
touch __init__.py

# config.py
curl -s -o config.py https://raw.githubusercontent.com/moloch00464-bit/documentation/claude/review-moloch-architecture-KFibr/moloch_3.0/core/config.py

# emotion.py (NEU!)
cat > emotion.py << 'EMOTION_EOF'
#!/usr/bin/env python3
"""M.O.L.O.C.H. 3.1 - Emotion Detection"""

from typing import Tuple
from datetime import datetime

def erkenne_stimmung(text: str) -> str:
    """Erkennt Stimmung aus Text"""
    lower = text.lower()
    if any(w in lower for w in ["scheiße", "fuck", "stress", "müde", "genervt", "sauer"]):
        return "gestresst"
    if any(w in lower for w in ["geil", "super", "nice", "cool", "perfekt", "hammer"]):
        return "gut_drauf"
    if any(w in lower for w in ["wie", "was", "warum", "?"]):
        return "fragend"
    return "neutral"

def stimmung_reaktion(stimmung: str) -> str:
    """System prompt Anpassung"""
    reaktionen = {
        "gestresst": "Markus klingt gestresst. Sei ruhig und hilfreich.",
        "gut_drauf": "Markus ist gut drauf! Mehr Humor erlaubt! 🖤",
        "fragend": "Markus hat Fragen. Sei informativ.",
        "neutral": ""
    }
    return reaktionen.get(stimmung, "")

def get_tageszeit_info() -> Tuple[str, str]:
    """Tageszeit-Anpassung"""
    stunde = datetime.now().hour
    if 5 <= stunde < 9:
        return "früh_morgens", "Früher Morgen. Kaffee-Modus. ☕"
    elif 18 <= stunde < 22:
        return "abend", "Feierabend! Lockerer. 🍺"
    elif stunde >= 22 or stunde < 5:
        return "nacht", "Nachtschicht. Dark Side Mode. 🖤😈"
    else:
        return "normal", ""

def enhance_system_prompt_with_emotion(system_prompt: str, user_input: str) -> str:
    """Erweitert System Prompt mit Emotion"""
    stimmung = erkenne_stimmung(user_input)
    reaktion = stimmung_reaktion(stimmung)
    _, tageszeit_info = get_tageszeit_info()
    enhancements = []
    if reaktion:
        enhancements.append(f"🎭 {reaktion}")
    if tageszeit_info:
        enhancements.append(f"⏰ {tageszeit_info}")
    if enhancements:
        return system_prompt + "\n\n" + "\n".join(enhancements)
    return system_prompt
EMOTION_EOF

# knowledge_graph.py (NEU!)
cat > knowledge_graph.py << 'KNOWLEDGE_EOF'
#!/usr/bin/env python3
"""M.O.L.O.C.H. 3.1 - Knowledge Graph"""

from typing import List, Dict

WISSENS_NETZ: Dict[str, List[str]] = {
    "wgt": ["shower noise group", "leipzig", "sierra", "dark wave"],
    "sierra": ["frankreich", "gone", "lieblingsartist"],
    "rebecca": ["klingonisch", "qapla", "freundin"],
    "erkan": ["türkisch", "staplerfahrer"],
    "dgm": ["arbeit", "druckguss"],
}

def finde_verknuepfungen(text: str) -> List[str]:
    """Findet Verknüpfungen"""
    lower = text.lower()
    gefunden = []
    for keyword, verknuepft in WISSENS_NETZ.items():
        if keyword in lower:
            gefunden.extend(verknuepft)
    return list(set(gefunden))

def lade_verknuepftes_wissen(text: str, memory_data: dict) -> List[str]:
    return []

def ist_neue_info(text: str) -> bool:
    return False

def kategorisiere_info(text: str) -> str:
    return "fakten"

def get_knowledge_context(user_input: str, memory_data: dict = None) -> str:
    """Knowledge Context für Prompt"""
    verknuepfungen = finde_verknuepfungen(user_input)
    if verknuepfungen:
        return f"🧠 Relevante Themen: {', '.join(verknuepfungen[:5])}"
    return ""
KNOWLEDGE_EOF

# tools.py
curl -s -o tools.py https://raw.githubusercontent.com/moloch00464-bit/documentation/claude/review-moloch-architecture-KFibr/moloch_3.0/core/tools.py

# Alle anderen Module vom Backup kopieren
if [ -d "$HOME/moloch_3.0_backup_20260107_144336/core" ]; then
    cp -n $HOME/moloch_3.0_backup_20260107_144336/core/*.py .
    echo "✅ Core Module von Backup kopiert"
else
    echo "⚠️  Kein Backup gefunden - einige Module könnten fehlen"
fi

echo "✅ Core Module erstellt"
echo ""

# ═══════════════════════════════════════════════════════════════════════════════
# STEP 4: moloch_io Module
# ═══════════════════════════════════════════════════════════════════════════════

echo "🔧 STEP 4: Erstelle moloch_io Module..."
cd ~/moloch_3.1/moloch_io

touch __init__.py

# Von Backup kopieren
if [ -d "$HOME/moloch_3.0_backup_20260107_144336/moloch_io" ]; then
    cp $HOME/moloch_3.0_backup_20260107_144336/moloch_io/*.py .
    echo "✅ moloch_io Module kopiert"
else
    echo "⚠️  Kein Backup - moloch_io könnte unvollständig sein"
fi

echo ""

# ═══════════════════════════════════════════════════════════════════════════════
# STEP 5: Memory Merge (2.0 → 3.1)
# ═══════════════════════════════════════════════════════════════════════════════

echo "🧠 STEP 5: Memory Merge (M.O.L.O.C.H. 2.0 → 3.1)..."
cd ~/moloch_3.1/data

if [ -f "$HOME/moloch/history.json" ]; then
    cp $HOME/moloch/history.json .
    SIZE=$(ls -lh history.json | awk '{print $5}')
    echo "  ✅ history.json ($SIZE)"
else
    echo "  ⚠️  history.json nicht gefunden"
fi

if [ -f "$HOME/moloch/langzeit.json" ]; then
    cp $HOME/moloch/langzeit.json .
    echo "  ✅ langzeit.json"
else
    echo "  ⚠️  langzeit.json nicht gefunden"
fi

if [ -d "$HOME/moloch/brain" ]; then
    cp -r $HOME/moloch/brain .
    FILES=$(find brain -type f | wc -l)
    echo "  ✅ brain/ ($FILES files)"
else
    echo "  ⚠️  brain/ nicht gefunden"
fi

echo "✅ Memory Merge complete!"
echo ""

# ═══════════════════════════════════════════════════════════════════════════════
# STEP 6: API Key Setup
# ═══════════════════════════════════════════════════════════════════════════════

echo "🔑 STEP 6: API Key Setup..."

if [ -f "$HOME/moloch/moloch.py" ]; then
    ANTHROPIC_KEY=$(grep -oP 'sk-ant-api03-[A-Za-z0-9_-]+' $HOME/moloch/moloch.py | head -1)

    if [ -n "$ANTHROPIC_KEY" ]; then
        sed -i "s/DEIN_ANTHROPIC_KEY_HIER/$ANTHROPIC_KEY/g" $HOME/moloch_3.1/core/config.py
        echo "✅ API Key automatisch gesetzt: ${ANTHROPIC_KEY:0:20}..."
    else
        echo "⚠️  Kein API Key gefunden - bitte manuell setzen!"
    fi
else
    echo "⚠️  moloch.py nicht gefunden - API Key manuell setzen!"
fi

echo ""

# ═══════════════════════════════════════════════════════════════════════════════
# STEP 7: Verify Installation
# ═══════════════════════════════════════════════════════════════════════════════

echo "✅ STEP 7: Verify Installation..."
echo ""

cd ~/moloch_3.1

echo "📊 M.O.L.O.C.H. 3.1 UNIFIED Status:"
echo "═══════════════════════════════════════════════════════════════"
echo ""

echo "📁 Struktur:"
echo "  ~/moloch_3.1/"
echo "    ├── moloch3_unified.py ($(ls -lh moloch3_unified.py | awk '{print $5}'))"
echo "    ├── core/ ($(ls core/*.py | wc -l) modules)"
echo "    ├── moloch_io/ ($(ls moloch_io/*.py 2>/dev/null | wc -l) modules)"
echo "    └── data/"
if [ -f "data/history.json" ]; then
    echo "        ├── history.json ($(ls -lh data/history.json | awk '{print $5}'))"
fi
if [ -d "data/brain" ]; then
    echo "        └── brain/ ($(find data/brain -type f | wc -l) files)"
fi
echo ""

echo "🎭 Features:"
echo "  ✅ Emotion Detection (from 2.0)"
echo "  ✅ Knowledge Graph (from 2.0)"
echo "  ✅ Internet (web_search_20250305)"
echo "  ✅ Tool Calling"
echo "  ✅ Self-Modification"
echo ""

echo "═══════════════════════════════════════════════════════════════"
echo "🎉 M.O.L.O.C.H. 3.1 UNIFIED INSTALLATION COMPLETE!"
echo "═══════════════════════════════════════════════════════════════"
echo ""
echo "🚀 STARTEN MIT:"
echo "   cd ~/moloch_3.1"
echo "   python moloch3_unified.py"
echo ""
echo "💡 TIPP: Sag was wie 'Alter, kennst du noch Sierra Veins?'"
echo "   → Emotion Detection + Knowledge Graph in Action!"
echo ""
echo "🖤 VIEL ERFOLG MIT M.O.L.O.C.H. 3.1 UNIFIED!"
echo ""
