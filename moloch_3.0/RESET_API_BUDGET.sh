#!/bin/bash
###############################################################################
# M.O.L.O.C.H. 3.0 - API BUDGET MANUAL RESET
# ===========================================
# Setzt API Counters zurück (für Notfälle!)
###############################################################################

echo "════════════════════════════════════════════════════════════════"
echo "  M.O.L.O.C.H. 3.0 - API BUDGET RESET"
echo "════════════════════════════════════════════════════════════════"
echo ""
echo "⚠️  ACHTUNG: Dieser Reset ist normalerweise NICHT nötig!"
echo "   Das Budget wird automatisch jeden Tag um Mitternacht resettet."
echo ""
echo "   Benutze dieses Script nur wenn:"
echo "   - Du das Budget überschritten hast UND"
echo "   - Du dringend Voice/Vision brauchst UND"
echo "   - Du nicht bis Mitternacht warten kannst"
echo ""
read -p "Wirklich resetten? (y/N): " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[YyJj]$ ]]; then
    echo "❌ Abgebrochen."
    exit 0
fi

echo ""
echo "🔄 Resette API Budget..."
echo ""

# Auto-detect M.O.L.O.C.H. 3.0 directory
if [ -d "$HOME/documentation/moloch_3.0" ]; then
    cd "$HOME/documentation/moloch_3.0"
elif [ -d "$HOME/moloch_3.0" ]; then
    cd "$HOME/moloch_3.0"
else
    echo "❌ FEHLER: M.O.L.O.C.H. 3.0 nicht gefunden!"
    exit 1
fi

# Run manual reset
python3 << 'PYTHON_RESET'
import sys
sys.path.insert(0, '.')

from core.api_safeguards import get_api_guard

# Get API Guard
guard = get_api_guard()

# Show current status
print("📊 AKTUELLER STATUS:")
status = guard.get_status()
print(f"   Whisper: {status['whisper']['day']} calls, {status['whisper']['cost_today']}")
print(f"   Claude:  {status['claude']['day']} calls, {status['claude']['cost_today']}")
print(f"   Vision:  {status['vision']['day']} calls, {status['vision']['cost_today']}")
print(f"   TOTAL:   {status['total']['cost_today']} / {status['total']['budget']}")
print()

# Manual reset
guard.manual_reset()

# Show new status
print("📊 NEUER STATUS:")
status = guard.get_status()
print(f"   Whisper: {status['whisper']['day']} calls, {status['whisper']['cost_today']}")
print(f"   Claude:  {status['claude']['day']} calls, {status['claude']['cost_today']}")
print(f"   Vision:  {status['vision']['day']} calls, {status['vision']['cost_today']}")
print(f"   TOTAL:   {status['total']['cost_today']} / {status['total']['budget']}")
PYTHON_RESET

echo ""
echo "════════════════════════════════════════════════════════════════"
echo "  ✅ RESET ABGESCHLOSSEN!"
echo "════════════════════════════════════════════════════════════════"
echo ""
echo "Du kannst jetzt wieder Voice/Vision benutzen!"
echo "Neues Budget: \$10.00"
echo ""
