#!/bin/bash
# ═══════════════════════════════════════════════════════════════════════════════
# M.O.L.O.C.H. UNIFIED - FIXED DEPLOYMENT
# ═══════════════════════════════════════════════════════════════════════════════
# This script upgrades your WORKING moloch_3.0 with emotion + knowledge features
# Instead of creating fresh (which fails), we ADD to what already works!
# ═══════════════════════════════════════════════════════════════════════════════

set -e

echo "🤖 M.O.L.O.C.H. UNIFIED - SMART DEPLOYMENT"
echo "═══════════════════════════════════════════════════════════════════════════════"
echo ""
echo "STRATEGIE: Upgrade your WORKING 3.0 instead of fresh install!"
echo ""

# ═══════════════════════════════════════════════════════════════════════════════
# STEP 0: Find your working M.O.L.O.C.H. 3.0
# ═══════════════════════════════════════════════════════════════════════════════

echo "📍 STEP 0: Suche funktionierenden M.O.L.O.C.H. 3.0..."

# Check for existing 3.0 installations
if [ -d "$HOME/moloch_3.0" ]; then
    MOLOCH_DIR="$HOME/moloch_3.0"
    echo "✅ Gefunden: ~/moloch_3.0"
elif [ -d "$HOME/moloch_3.0_backup_20260107_144336" ]; then
    MOLOCH_DIR="$HOME/moloch_3.0_backup_20260107_144336"
    echo "✅ Gefunden: ~/moloch_3.0_backup_20260107_144336"
else
    echo "❌ Kein M.O.L.O.C.H. 3.0 gefunden!"
    echo "   Bitte erst M.O.L.O.C.H. 3.0 installieren oder Pfad angeben"
    exit 1
fi

echo ""
read -p "▶️  Upgrade $MOLOCH_DIR? [Enter zum fortfahren, Ctrl+C zum Abbrechen]"
echo ""

# ═══════════════════════════════════════════════════════════════════════════════
# STEP 1: Backup current 3.0
# ═══════════════════════════════════════════════════════════════════════════════

echo "📦 STEP 1: Backup current installation..."

BACKUP_DIR="${MOLOCH_DIR}_pre_unified_$(date +%Y%m%d_%H%M%S)"
cp -r "$MOLOCH_DIR" "$BACKUP_DIR"

echo "✅ Backup: $BACKUP_DIR"
echo ""

# ═══════════════════════════════════════════════════════════════════════════════
# STEP 2: Add emotion.py (inline - no download issues!)
# ═══════════════════════════════════════════════════════════════════════════════

echo "🎭 STEP 2: Adding emotion.py..."

cat > "$MOLOCH_DIR/core/emotion.py" << 'EMOTION_EOF'
#!/usr/bin/env python3
"""M.O.L.O.C.H. 3.1 - Emotion Detection"""

from typing import Tuple
from datetime import datetime

def erkenne_stimmung(text: str) -> str:
    """Erkennt Stimmung aus Text"""
    lower = text.lower()

    # Negativ/Gestresst
    if any(w in lower for w in ["scheiße", "fuck", "stress", "müde", "genervt", "sauer"]):
        return "gestresst"

    # Positiv/Gut drauf
    if any(w in lower for w in ["geil", "super", "nice", "cool", "perfekt", "hammer"]):
        return "gut_drauf"

    # Fragend/Unsicher
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

echo "✅ emotion.py created ($(wc -l < "$MOLOCH_DIR/core/emotion.py") lines)"
echo ""

# ═══════════════════════════════════════════════════════════════════════════════
# STEP 3: Add knowledge_graph.py (inline - no download issues!)
# ═══════════════════════════════════════════════════════════════════════════════

echo "🧠 STEP 3: Adding knowledge_graph.py..."

cat > "$MOLOCH_DIR/core/knowledge_graph.py" << 'KNOWLEDGE_EOF'
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
    """Lädt verknüpftes Wissen (Placeholder)"""
    return []

def ist_neue_info(text: str) -> bool:
    """Prüft ob neue Info (Placeholder)"""
    return False

def kategorisiere_info(text: str) -> str:
    """Kategorisiert Info"""
    return "fakten"

def get_knowledge_context(user_input: str, memory_data: dict = None) -> str:
    """Knowledge Context für Prompt"""
    verknuepfungen = finde_verknuepfungen(user_input)
    if verknuepfungen:
        return f"🧠 Relevante Themen: {', '.join(verknuepfungen[:5])}"
    return ""
KNOWLEDGE_EOF

echo "✅ knowledge_graph.py created ($(wc -l < "$MOLOCH_DIR/core/knowledge_graph.py") lines)"
echo ""

# ═══════════════════════════════════════════════════════════════════════════════
# STEP 4: Ensure __init__.py exists
# ═══════════════════════════════════════════════════════════════════════════════

echo "📝 STEP 4: Ensure core/__init__.py exists..."

if [ ! -f "$MOLOCH_DIR/core/__init__.py" ]; then
    touch "$MOLOCH_DIR/core/__init__.py"
    echo "✅ Created core/__init__.py"
else
    echo "✅ core/__init__.py already exists"
fi

echo ""

# ═══════════════════════════════════════════════════════════════════════════════
# STEP 5: Update moloch3_unified.py with emotion + knowledge
# ═══════════════════════════════════════════════════════════════════════════════

echo "🔧 STEP 5: Checking if moloch3_unified.py needs emotion imports..."

if grep -q "from core.emotion" "$MOLOCH_DIR/moloch3_unified.py" 2>/dev/null; then
    echo "✅ moloch3_unified.py already has emotion imports"
else
    echo "⚠️  moloch3_unified.py needs manual update!"
    echo ""
    echo "📝 ADD THESE IMPORTS to moloch3_unified.py after other core imports:"
    echo ""
    echo "    from core.emotion import erkenne_stimmung, enhance_system_prompt_with_emotion"
    echo "    from core.knowledge_graph import get_knowledge_context"
    echo ""
    echo "Then use in ask_claude_text() function:"
    echo "    stimmung = erkenne_stimmung(user_text)"
    echo "    knowledge_context = get_knowledge_context(user_text)"
    echo ""
fi

echo ""

# ═══════════════════════════════════════════════════════════════════════════════
# STEP 6: Verify installation
# ═══════════════════════════════════════════════════════════════════════════════

echo "✅ STEP 6: Verify installation..."
echo ""

cd "$MOLOCH_DIR"

echo "📊 M.O.L.O.C.H. UNIFIED Status:"
echo "═══════════════════════════════════════════════════════════════════════════════"
echo ""
echo "📁 Location: $MOLOCH_DIR"
echo ""
echo "🔧 Core Modules:"
ls -lh core/*.py | awk '{print "   " $9 " (" $5 ")"}'
echo ""

# Test imports
echo "🧪 Testing Python imports..."
python3 << 'PYTEST'
import sys
sys.path.insert(0, '.')

try:
    from core.emotion import erkenne_stimmung, enhance_system_prompt_with_emotion
    print("   ✅ core.emotion imports successfully")

    # Test function
    test_stimmung = erkenne_stimmung("Alter das ist geil!")
    print(f"   ✅ erkenne_stimmung() works: '{test_stimmung}'")
except Exception as e:
    print(f"   ❌ core.emotion FAILED: {e}")
    sys.exit(1)

try:
    from core.knowledge_graph import get_knowledge_context
    print("   ✅ core.knowledge_graph imports successfully")

    # Test function
    test_context = get_knowledge_context("Erzähl mir von Sierra")
    print(f"   ✅ get_knowledge_context() works")
except Exception as e:
    print(f"   ❌ core.knowledge_graph FAILED: {e}")
    sys.exit(1)

print()
print("🎉 ALL IMPORTS WORKING!")
PYTEST

if [ $? -eq 0 ]; then
    echo ""
    echo "═══════════════════════════════════════════════════════════════════════════════"
    echo "🎉 M.O.L.O.C.H. UNIFIED UPGRADE SUCCESSFUL!"
    echo "═══════════════════════════════════════════════════════════════════════════════"
    echo ""
    echo "✅ emotion.py: Stimmungserkennung aktiv"
    echo "✅ knowledge_graph.py: WISSENS_NETZ aktiv"
    echo ""
    echo "📝 NÄCHSTER SCHRITT:"
    echo "   1. Update moloch3_unified.py mit emotion imports (siehe oben)"
    echo "   2. Teste mit: cd $MOLOCH_DIR && python moloch3_unified.py"
    echo ""
    echo "📦 ROLLBACK (falls nötig):"
    echo "   rm -rf $MOLOCH_DIR"
    echo "   mv $BACKUP_DIR $MOLOCH_DIR"
    echo ""
else
    echo ""
    echo "❌ IMPORT TEST FAILED!"
    echo ""
    echo "📦 ROLLBACK:"
    echo "   rm -rf $MOLOCH_DIR"
    echo "   mv $BACKUP_DIR $MOLOCH_DIR"
    echo ""
    exit 1
fi
