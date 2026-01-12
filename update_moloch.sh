#!/bin/bash
#
# M.O.L.O.C.H. 3.0 - Update Script
# Holt die neueste Version und testet diagnose.py
#
# Usage:
#   cd ~/documentation
#   bash update_moloch.sh
#

echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║  M.O.L.O.C.H. 3.0 - UPDATE SCRIPT                             ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo ""

# Schritt 0: Prüfe ob wir im documentation Verzeichnis sind
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if [ ! -d "$SCRIPT_DIR/moloch_3.0" ]; then
    echo "❌ FEHLER: Script muss aus dem documentation/ Verzeichnis ausgeführt werden!"
    echo "   Führe aus: cd ~/documentation && bash update_moloch.sh"
    exit 1
fi
echo "✅ Im richtigen Verzeichnis: $SCRIPT_DIR"
echo ""

# Schritt 1: Fetch
echo "📡 Hole neueste Änderungen vom Server..."
git fetch origin
if [ $? -ne 0 ]; then
    echo "❌ FEHLER: git fetch fehlgeschlagen!"
    exit 1
fi
echo "✅ Fetch erfolgreich"
echo ""

# Schritt 2: Checkout Branch
echo "🔄 Wechsle zu Branch: claude/moloch-health-check-6UkkI"
git checkout claude/moloch-health-check-6UkkI
if [ $? -ne 0 ]; then
    echo "❌ FEHLER: Branch wechseln fehlgeschlagen!"
    exit 1
fi
echo "✅ Branch gewechselt"
echo ""

# Schritt 3: Pull
echo "⬇️  Pull neueste Änderungen..."
git pull origin claude/moloch-health-check-6UkkI
if [ $? -ne 0 ]; then
    echo "❌ FEHLER: git pull fehlgeschlagen!"
    exit 1
fi
echo "✅ Pull erfolgreich"
echo ""

# Schritt 3.5: Reload Environment Variables
echo "🔄 Lade Environment Variables neu..."
if [ -f "$HOME/.bashrc" ]; then
    source "$HOME/.bashrc"
    echo "✅ .bashrc neu geladen"

    # Check if API key is set
    if [ -n "$ANTHROPIC_API_KEY" ]; then
        echo "✅ ANTHROPIC_API_KEY gefunden: ${ANTHROPIC_API_KEY:0:20}..."
    else
        echo "⚠️  ANTHROPIC_API_KEY nicht gesetzt!"
        echo "   Setze mit: export ANTHROPIC_API_KEY='sk-ant-api03-...'"
    fi
else
    echo "⚠️  ~/.bashrc nicht gefunden"
fi
echo ""

# Schritt 4: Teste diagnose.py in moloch_3.0
echo "🔍 Teste diagnose.py..."
echo ""
cd moloch_3.0
if [ $? -ne 0 ]; then
    echo "❌ FEHLER: Verzeichnis moloch_3.0 nicht gefunden!"
    exit 1
fi

python diagnose.py --json
DIAGNOSE_EXIT=$?

# Gehe zurück ins documentation Verzeichnis
cd ..

echo ""
echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║  ✅ UPDATE ABGESCHLOSSEN!                                     ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo ""
echo "📂 Du bist jetzt in: $(pwd)"

exit $DIAGNOSE_EXIT
