#!/bin/bash
#
# M.O.L.O.C.H. 3.0 - Sprach-Check für termux-speech-to-text
# Findet heraus warum nur Englisch erkannt wird
#

echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║  M.O.L.O.C.H. - SPRACH-DIAGNOSE                               ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo ""
echo "🔍 Checking warum termux-speech-to-text nur Englisch versteht..."
echo ""

# Test 1: System Locale
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "1️⃣  SYSTEM LOCALE (Termux)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Current locale:"
locale | grep LANG
echo ""

# Test 2: Android System Properties
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "2️⃣  ANDROID SYSTEM PROPERTIES"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
if command -v getprop &> /dev/null; then
    echo "System Language:"
    getprop persist.sys.language 2>/dev/null || echo "   (nicht verfügbar)"
    echo ""
    echo "System Locale:"
    getprop persist.sys.locale 2>/dev/null || echo "   (nicht verfügbar)"
    echo ""
    echo "Country:"
    getprop persist.sys.country 2>/dev/null || echo "   (nicht verfügbar)"
else
    echo "⚠️  getprop nicht verfügbar"
fi
echo ""

# Test 3: Actual Voice Recognition Test
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "3️⃣  LIVE SPRACH-TEST"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Jetzt machen wir einen Live-Test:"
echo ""
read -p "Test mit deutschem Wort 'Hallo'? (j/n) " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Jj]$ ]]; then
    echo ""
    echo "🎤 SPRICH JETZT: 'Hallo'"
    echo "   (genau so aussprechen!)"
    echo ""

    RESULT=$(termux-speech-to-text 2>&1)

    echo ""
    echo "📝 Erkannter Text: '$RESULT'"
    echo ""

    # Analyze result
    if [[ "$RESULT" == *"hallo"* ]] || [[ "$RESULT" == *"Hallo"* ]]; then
        echo "✅ DEUTSCH ERKANNT! Problem gelöst!"
    elif [[ "$RESULT" == *"hello"* ]] || [[ "$RESULT" == *"Hello"* ]]; then
        echo "❌ ENGLISCH ERKANNT! Problem besteht!"
        echo ""
        echo "Das bedeutet: Google Voice Typing ist auf ENGLISCH eingestellt!"
    else
        echo "⚠️  UNBEKANNTES ERGEBNIS: '$RESULT'"
    fi
fi

echo ""
echo ""

# Solution
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "💡 LÖSUNG"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Du musst GOOGLE VOICE TYPING auf Deutsch stellen!"
echo ""
echo "📱 ÖFFNE IN ANDROID EINSTELLUNGEN:"
echo ""
echo "Variante 1 (die meisten Geräte):"
echo "  Settings → System → Languages & input"
echo "    → On-screen keyboard → Google voice typing"
echo "      → Languages"
echo "        → ✅ Deutsch (Deutschland) als PRIMÄR setzen"
echo ""
echo "Variante 2 (Xiaomi/MIUI/HyperOS):"
echo "  Einstellungen → Zusätzliche Einstellungen"
echo "    → Sprache & Eingabe → Google Spracheingabe"
echo "      → Sprachen → Deutsch auswählen"
echo ""
echo "Variante 3 (Samsung):"
echo "  Einstellungen → Allgemeine Verwaltung"
echo "    → Sprache und Eingabe → Bildschirmtastatur"
echo "      → Google Spracheingabe → Sprachen"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "⚠️  WICHTIG:"
echo "   - Nicht nur 'hinzufügen' sondern als PRIMÄR setzen!"
echo "   - Eventuell Englisch ENTFERNEN aus der Liste"
echo "   - Nach Änderung: Handy neu starten!"
echo ""
echo "🔧 ALTERNATIVE:"
echo "   Öffne Google App → Settings → Voice → Languages"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Nach der Einstellung: Führe dieses Script nochmal aus!"
echo "  bash ~/documentation/check_voice_language.sh"
echo ""
