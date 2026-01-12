#!/bin/bash
# Debug Script für termux-speech-to-text Sprach-Problem
# Findet heraus WARUM STT nur Englisch versteht

echo "═══════════════════════════════════════════════════════════════"
echo "🔍 DEBUG: termux-speech-to-text Sprach-Erkennung"
echo "═══════════════════════════════════════════════════════════════"
echo ""

# Check 1: Ist termux-speech-to-text installiert?
echo "📦 Check 1: Ist termux-speech-to-text installiert?"
if command -v termux-speech-to-text &> /dev/null; then
    echo "   ✅ termux-speech-to-text gefunden: $(which termux-speech-to-text)"
else
    echo "   ❌ termux-speech-to-text NICHT gefunden!"
    echo "   Fix: pkg install termux-api"
    exit 1
fi
echo ""

# Check 2: Ist Termux:API App installiert?
echo "📱 Check 2: Ist Termux:API App installiert?"
if pm list packages | grep -q com.termux.api; then
    echo "   ✅ Termux:API App installiert"
else
    echo "   ❌ Termux:API App NICHT installiert!"
    echo "   Fix: Installiere Termux:API aus F-Droid"
    exit 1
fi
echo ""

# Check 3: Android System-Sprache
echo "🌍 Check 3: Android System-Sprache"
SYSTEM_LANG=$(getprop persist.sys.locale 2>/dev/null || getprop ro.product.locale 2>/dev/null || echo "unknown")
echo "   System Locale: $SYSTEM_LANG"
echo ""

# Check 4: Test mit deutschem Satz
echo "🎤 Check 4: LIVE TEST - Sprich DEUTSCH!"
echo ""
echo "   SAG JETZT AUF DEUTSCH:"
echo "   'Ich bin Markus und spreche Deutsch'"
echo ""
echo "   (Warte auf Mikrofon-Symbol...)"
echo ""

# Run termux-speech-to-text und zeige Ausgabe
RESULT=$(termux-speech-to-text 2>&1)
EXIT_CODE=$?

echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "📊 ERGEBNIS:"
echo "═══════════════════════════════════════════════════════════════"
echo ""
echo "Exit Code: $EXIT_CODE"
echo ""
echo "Text erkannt:"
echo "$RESULT"
echo ""

# Analyse
if [ $EXIT_CODE -ne 0 ]; then
    echo "❌ STT FEHLER - Exit Code: $EXIT_CODE"
    echo ""
    echo "Mögliche Ursachen:"
    echo "  - Mikrofon-Berechtigung fehlt"
    echo "  - Google Voice Typing nicht verfügbar"
    echo "  - Termux:API App defekt"
elif echo "$RESULT" | grep -qi "deutsch\|markus"; then
    echo "✅ DEUTSCH ERKANNT!"
    echo ""
    echo "STT funktioniert korrekt mit Deutsch!"
elif echo "$RESULT" | grep -qi "german\|marcus"; then
    echo "⚠️  ENGLISCH ERKANNT (aber deutscher Inhalt)"
    echo ""
    echo "Das bedeutet: Google Voice Typing ist auf ENGLISCH gestellt!"
    echo ""
    echo "FIX:"
    echo "1. Öffne: Einstellungen"
    echo "2. Suche nach: 'Google Voice Typing' oder 'Spracheingabe'"
    echo "3. Gehe zu: Sprachen"
    echo "4. Stelle sicher dass 'Deutsch (Deutschland)' AKTIV ist"
    echo "5. Entferne ggf. Englisch als primäre Sprache"
else
    echo "⚠️  UNBEKANNTE SPRACHE ERKANNT"
    echo ""
    echo "Erkannter Text war weder Deutsch noch Englisch."
    echo ""
    echo "Mögliche Probleme:"
    echo "  - Google Voice Typing nutzt falsche Sprache"
    echo "  - Mehrere Sprachen sind aktiv (Konflikt)"
    echo "  - Audio zu leise"
fi

echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "🔧 NÄCHSTE SCHRITTE:"
echo "═══════════════════════════════════════════════════════════════"
echo ""
echo "1. Prüfe Google Voice Typing Einstellungen:"
echo "   Einstellungen → System → Sprachen & Eingabe"
echo "   → Google Voice Typing → Sprachen"
echo ""
echo "2. Stelle sicher dass NUR Deutsch aktiviert ist"
echo ""
echo "3. Starte Handy neu"
echo ""
echo "4. Führe dieses Script nochmal aus"
echo ""
