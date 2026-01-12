#!/bin/bash
#
# M.O.L.O.C.H. 3.0 - Update Script
# Holt die neueste Version und testet diagnose.py
#

echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║  M.O.L.O.C.H. 3.0 - UPDATE SCRIPT                             ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
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

# Schritt 4: Gehe zu moloch_3.0
echo "📂 Wechsle zu moloch_3.0..."
cd moloch_3.0
if [ $? -ne 0 ]; then
    echo "❌ FEHLER: Verzeichnis moloch_3.0 nicht gefunden!"
    exit 1
fi
echo "✅ In moloch_3.0"
echo ""

# Schritt 5: Teste diagnose.py
echo "🔍 Teste diagnose.py..."
echo ""
python diagnose.py --json

echo ""
echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║  ✅ UPDATE ABGESCHLOSSEN!                                     ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
