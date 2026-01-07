#!/bin/bash
# ═══════════════════════════════════════════════════════════════════════════════
# M.O.L.O.C.H. 3.1 - TERMUX DIAGNOSTICS
# ═══════════════════════════════════════════════════════════════════════════════
# Testet ob termux-speech-to-text korrekt funktioniert
# ═══════════════════════════════════════════════════════════════════════════════

echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║  M.O.L.O.C.H. 3.1 - TERMUX DIAGNOSTICS                        ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo ""

# ═══════════════════════════════════════════════════════════════════════════════
# TEST 1: Ist termux-speech-to-text installiert?
# ═══════════════════════════════════════════════════════════════════════════════

echo "🔍 TEST 1: termux-speech-to-text Installation"
echo "─────────────────────────────────────────────────────────────────"

if command -v termux-speech-to-text &> /dev/null; then
    echo "✅ termux-speech-to-text gefunden!"
    echo "   Location: $(which termux-speech-to-text)"
else
    echo "❌ termux-speech-to-text NICHT gefunden!"
    echo ""
    echo "LÖSUNG:"
    echo "  1. pkg install termux-api"
    echo "  2. Installiere 'Termux:API' App aus Play Store"
    echo "  3. Starte Termux neu"
    exit 1
fi

echo ""

# ═══════════════════════════════════════════════════════════════════════════════
# TEST 2: Ist termux-api Package installiert?
# ═══════════════════════════════════════════════════════════════════════════════

echo "🔍 TEST 2: termux-api Package"
echo "─────────────────────────────────────────────────────────────────"

if pkg list-installed | grep -q "termux-api"; then
    echo "✅ termux-api Package installiert!"
    VERSION=$(pkg list-installed termux-api 2>/dev/null | grep -o "[0-9]\+\.[0-9]\+" | head -1)
    if [ -n "$VERSION" ]; then
        echo "   Version: $VERSION"
    fi
else
    echo "❌ termux-api Package NICHT installiert!"
    echo ""
    echo "LÖSUNG:"
    echo "  pkg install termux-api"
    exit 1
fi

echo ""

# ═══════════════════════════════════════════════════════════════════════════════
# TEST 3: Internet-Verbindung (Google Speech API braucht Internet!)
# ═══════════════════════════════════════════════════════════════════════════════

echo "🔍 TEST 3: Internet-Verbindung"
echo "─────────────────────────────────────────────────────────────────"

if ping -c 1 google.com &> /dev/null; then
    echo "✅ Internet-Verbindung OK!"
else
    echo "⚠️  Keine Internet-Verbindung!"
    echo "   Google Speech API braucht Internet!"
    echo ""
fi

echo ""

# ═══════════════════════════════════════════════════════════════════════════════
# TEST 4: TTS Test (termux-tts-speak)
# ═══════════════════════════════════════════════════════════════════════════════

echo "🔍 TEST 4: Text-to-Speech (TTS)"
echo "─────────────────────────────────────────────────────────────────"

if command -v termux-tts-speak &> /dev/null; then
    echo "✅ termux-tts-speak gefunden!"
    echo ""
    echo "🗣️  TTS TEST - Hörst du mich?"
    termux-tts-speak -l de-DE "Test. Hörst du mich?"
    sleep 2
    termux-tts-speak -e  # Stop TTS
    echo "✅ TTS Test abgeschlossen"
else
    echo "⚠️  termux-tts-speak nicht gefunden"
fi

echo ""

# ═══════════════════════════════════════════════════════════════════════════════
# TEST 5: Speech-to-Text LIVE TEST
# ═══════════════════════════════════════════════════════════════════════════════

echo "🔍 TEST 5: Speech-to-Text LIVE TEST"
echo "─────────────────────────────────────────────────────────────────"
echo ""
echo "WICHTIG:"
echo "  - Dieser Test öffnet das Google Voice Dialog"
echo "  - Sprich DEUTSCH ins Mikrofon"
echo "  - Sag etwas einfaches wie 'Hallo Test'"
echo ""
echo "👉 DRÜCK ENTER WENN BEREIT..."
read

echo ""
echo "🎤 Sprich JETZT..."

# Run termux-speech-to-text with German language
TEXT=$(termux-speech-to-text -l de-DE 2>&1)
RETURN_CODE=$?

echo ""
echo "📊 ERGEBNIS:"
echo "─────────────────────────────────────────────────────────────────"
echo "Return Code: $RETURN_CODE"
echo "Output: '$TEXT'"
echo ""

if [ $RETURN_CODE -eq 0 ] && [ -n "$TEXT" ]; then
    echo "✅ ERFOLG! Speech-to-Text funktioniert!"
    echo "   Verstanden: $TEXT"
    echo ""
    echo "╔═══════════════════════════════════════════════════════════════╗"
    echo "║  ✅ ALLE TESTS BESTANDEN!                                     ║"
    echo "╚═══════════════════════════════════════════════════════════════╝"
    echo ""
    echo "M.O.L.O.C.H. 3.1 sollte jetzt funktionieren!"
    echo ""
else
    echo "❌ FEHLER - Speech-to-Text funktioniert NICHT!"
    echo ""
    echo "FEHLER-DIAGNOSE:"

    if [ $RETURN_CODE -ne 0 ]; then
        echo "  → Return Code $RETURN_CODE (Fehler!)"
    fi

    if echo "$TEXT" | grep -q "not found"; then
        echo "  → Command nicht gefunden"
        echo "    LÖSUNG: pkg install termux-api"
    fi

    if echo "$TEXT" | grep -qi "permission"; then
        echo "  → Android Permissions fehlen!"
        echo "    LÖSUNG:"
        echo "      1. Gehe zu: Einstellungen → Apps → Termux"
        echo "      2. Permissions → Mikrofon → Erlauben"
        echo "      3. Starte Termux neu"
    fi

    if echo "$TEXT" | grep -qi "network\|connection"; then
        echo "  → Keine Internet-Verbindung!"
        echo "    Google Speech API braucht Internet!"
    fi

    if [ -z "$TEXT" ]; then
        echo "  → Kein Output (nichts verstanden)"
        echo "    Mögliche Ursachen:"
        echo "      1. Zu leise gesprochen"
        echo "      2. Mikrofon blockiert"
        echo "      3. Google App nicht konfiguriert"
        echo "      4. Voice Dialog abgebrochen"
    fi

    echo ""
    echo "NÄCHSTE SCHRITTE:"
    echo "  1. Überprüfe Android Permissions für Termux"
    echo "  2. Stelle sicher dass 'Termux:API' App installiert ist"
    echo "  3. Teste mit: termux-speech-to-text -l de-DE"
    echo "  4. Wenn Problem bleibt: Termux + Termux:API neu installieren"
fi

echo ""
