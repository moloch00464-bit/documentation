#!/bin/bash
#
# M.O.L.O.C.H. 3.0 - Termux Vollständiger Test
# Testet ALLE Komponenten: Voice (TTS + STT), Vision (Camera), Audio (ffmpeg)
#
# Usage auf Termux:
#   cd ~/documentation
#   bash test_moloch_termux.sh
#

echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║  M.O.L.O.C.H. 3.0 - TERMUX VOLLSTÄNDIGER TEST                 ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo ""
echo "⚠️  WICHTIG: Dieser Test benötigt Hardware-Zugriff!"
echo "   - Mikrofon-Berechtigung"
echo "   - Kamera-Berechtigung"
echo "   - Termux:API App (F-Droid)"
echo ""
read -p "Drücke ENTER um zu starten..."
echo ""

# Farben für Output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

TESTS_PASSED=0
TESTS_FAILED=0

# Test Helper Function
test_command() {
    local cmd="$1"
    local desc="$2"
    local test_type="$3"  # "critical", "medium", "optional"

    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "🧪 TEST: $desc"
    echo "   Command: $cmd"
    echo ""

    if which "$cmd" > /dev/null 2>&1; then
        echo -e "${GREEN}✅ PASSED${NC} - $cmd gefunden"
        TESTS_PASSED=$((TESTS_PASSED + 1))

        # Location anzeigen
        local location=$(which "$cmd")
        echo "   📍 Location: $location"

        return 0
    else
        if [ "$test_type" = "optional" ]; then
            echo -e "${YELLOW}⚠️  OPTIONAL${NC} - $cmd nicht gefunden (optional)"
            TESTS_PASSED=$((TESTS_PASSED + 1))
        else
            echo -e "${RED}❌ FAILED${NC} - $cmd nicht gefunden"
            TESTS_FAILED=$((TESTS_FAILED + 1))

            # Fix suggestion
            if [[ "$cmd" == termux-* ]]; then
                echo "   🔧 Fix: pkg install termux-api"
                echo "         + Termux:API App (F-Droid)"
            elif [ "$cmd" = "ffmpeg" ]; then
                echo "   🔧 Fix: pkg install ffmpeg"
            fi
        fi
        return 1
    fi
}

# Test Python Package
test_python_package() {
    local pkg="$1"
    local desc="$2"

    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "🧪 TEST: $desc"
    echo "   Package: $pkg"
    echo ""

    if python -c "import $pkg" 2>/dev/null; then
        echo -e "${GREEN}✅ PASSED${NC} - $pkg importiert"
        TESTS_PASSED=$((TESTS_PASSED + 1))
        return 0
    else
        echo -e "${RED}❌ FAILED${NC} - $pkg nicht gefunden"
        TESTS_FAILED=$((TESTS_FAILED + 1))
        echo "   🔧 Fix: pip install $pkg"
        return 1
    fi
}

# Test Environment Variable
test_env_var() {
    local var="$1"
    local desc="$2"

    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "🧪 TEST: $desc"
    echo "   Variable: $var"
    echo ""

    local value="${!var}"
    if [ -n "$value" ] && [ ${#value} -gt 10 ]; then
        echo -e "${GREEN}✅ PASSED${NC} - $var gesetzt"
        echo "   🔑 Value: ${value:0:20}..."
        TESTS_PASSED=$((TESTS_PASSED + 1))
        return 0
    else
        echo -e "${RED}❌ FAILED${NC} - $var nicht gesetzt"
        TESTS_FAILED=$((TESTS_FAILED + 1))
        echo "   🔧 Fix: echo \"export $var=your-key\" >> ~/.bashrc"
        echo "         source ~/.bashrc"
        return 1
    fi
}

echo "═══════════════════════════════════════════════════════════════"
echo "PHASE 1: TERMUX-API COMMANDS (kritisch)"
echo "═══════════════════════════════════════════════════════════════"
echo ""

test_command "termux-tts-speak" "Text-to-Speech (Voice OUT)" "critical"
test_command "termux-speech-to-text" "Speech-to-Text (Voice IN)" "critical"
test_command "termux-camera-photo" "Camera (Vision)" "critical"
test_command "termux-microphone-record" "Microphone (Audio Recording)" "optional"
test_command "termux-screenshot" "Screenshot" "optional"

echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "PHASE 2: SYSTEM TOOLS"
echo "═══════════════════════════════════════════════════════════════"
echo ""

test_command "ffmpeg" "Audio Konvertierung" "medium"
test_command "which" "Command Lookup (für diagnose.py)" "critical"

echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "PHASE 3: PYTHON PACKAGES"
echo "═══════════════════════════════════════════════════════════════"
echo ""

test_python_package "requests" "HTTP Requests (für Claude API)"
test_python_package "json" "JSON (Standard Library)"
test_python_package "subprocess" "Subprocess (Standard Library)"

echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "PHASE 4: API KEYS"
echo "═══════════════════════════════════════════════════════════════"
echo ""

test_env_var "ANTHROPIC_API_KEY" "Claude API Key"

echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "PHASE 5: LIVE HARDWARE TESTS (mit Benutzer-Interaktion)"
echo "═══════════════════════════════════════════════════════════════"
echo ""

# Test 5.1: TTS (Text-to-Speech)
if which termux-tts-speak > /dev/null 2>&1; then
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "🎙️  LIVE TEST: Text-to-Speech (Stimme)"
    echo ""
    read -p "Test TTS mit 'Hallo, ich bin MOLOCH'? (j/n) " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Jj]$ ]]; then
        termux-tts-speak "Hallo, ich bin MOLOCH. Drei Punkt Null."
        echo ""
        read -p "Hast du die Stimme gehört? (j/n) " -n 1 -r
        echo ""
        if [[ $REPLY =~ ^[Jj]$ ]]; then
            echo -e "${GREEN}✅ TTS FUNKTIONIERT${NC}"
            TESTS_PASSED=$((TESTS_PASSED + 1))
        else
            echo -e "${RED}❌ TTS FUNKTIONIERT NICHT${NC}"
            TESTS_FAILED=$((TESTS_FAILED + 1))
            echo "   🔧 Check: Lautstärke? Berechtigungen?"
        fi
    else
        echo "⏭️  TTS Test übersprungen"
    fi
    echo ""
fi

# Test 5.2: Speech-to-Text
if which termux-speech-to-text > /dev/null 2>&1; then
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "🎤 LIVE TEST: Speech-to-Text (Ohren)"
    echo ""
    read -p "Test STT mit Aufnahme? (j/n) " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Jj]$ ]]; then
        echo "🎤 Sprich jetzt: 'Hallo MOLOCH'"
        echo "   (Beende mit Stille oder Android Stop-Button)"
        echo ""

        # Run STT and capture output
        STT_OUTPUT=$(termux-speech-to-text 2>&1)

        echo ""
        echo "📝 Transkript:"
        echo "$STT_OUTPUT"
        echo ""

        if [ -n "$STT_OUTPUT" ]; then
            echo -e "${GREEN}✅ STT FUNKTIONIERT${NC}"
            TESTS_PASSED=$((TESTS_PASSED + 1))
        else
            echo -e "${RED}❌ STT KEIN OUTPUT${NC}"
            TESTS_FAILED=$((TESTS_FAILED + 1))
            echo "   🔧 Check: Mikrofon-Berechtigung? Internet?"
        fi
    else
        echo "⏭️  STT Test übersprungen"
    fi
    echo ""
fi

# Test 5.3: Camera
if which termux-camera-photo > /dev/null 2>&1; then
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "📷 LIVE TEST: Camera (Augen)"
    echo ""
    read -p "Test Kamera mit Foto? (j/n) " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Jj]$ ]]; then
        PHOTO_PATH="/data/data/com.termux/files/home/test_photo.jpg"
        echo "📸 Mache Foto..."

        # Try to take photo
        termux-camera-photo -c 0 "$PHOTO_PATH" 2>&1

        if [ -f "$PHOTO_PATH" ]; then
            FILE_SIZE=$(stat -c%s "$PHOTO_PATH" 2>/dev/null || stat -f%z "$PHOTO_PATH" 2>/dev/null)
            echo ""
            echo "✅ Foto erstellt: $PHOTO_PATH"
            echo "   📊 Größe: $FILE_SIZE bytes"

            if [ "$FILE_SIZE" -gt 1000 ]; then
                echo -e "${GREEN}✅ CAMERA FUNKTIONIERT${NC}"
                TESTS_PASSED=$((TESTS_PASSED + 1))
            else
                echo -e "${YELLOW}⚠️  Foto sehr klein, eventuell Problem${NC}"
                TESTS_FAILED=$((TESTS_FAILED + 1))
            fi

            # Cleanup
            rm -f "$PHOTO_PATH"
        else
            echo -e "${RED}❌ CAMERA KEIN OUTPUT${NC}"
            TESTS_FAILED=$((TESTS_FAILED + 1))
            echo "   🔧 Check: Kamera-Berechtigung?"
        fi
    else
        echo "⏭️  Camera Test übersprungen"
    fi
    echo ""
fi

echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "ZUSAMMENFASSUNG"
echo "═══════════════════════════════════════════════════════════════"
echo ""

TOTAL_TESTS=$((TESTS_PASSED + TESTS_FAILED))
echo "📊 Tests durchgeführt: $TOTAL_TESTS"
echo -e "   ${GREEN}✅ Passed: $TESTS_PASSED${NC}"
echo -e "   ${RED}❌ Failed: $TESTS_FAILED${NC}"
echo ""

if [ $TESTS_FAILED -eq 0 ]; then
    echo "╔═══════════════════════════════════════════════════════════════╗"
    echo "║                  ✅ ALLE TESTS BESTANDEN!                     ║"
    echo "║           M.O.L.O.C.H. 3.0 ist EINSATZBEREIT! 🤖🔥           ║"
    echo "╚═══════════════════════════════════════════════════════════════╝"
    exit 0
else
    echo "╔═══════════════════════════════════════════════════════════════╗"
    echo "║           ⚠️  EINIGE TESTS FEHLGESCHLAGEN                    ║"
    echo "║     Siehe Fehler oben für Installations-Anweisungen          ║"
    echo "╚═══════════════════════════════════════════════════════════════╝"
    echo ""
    echo "💡 Quick Fix Commands:"
    echo "   pkg install termux-api"
    echo "   pkg install ffmpeg"
    echo "   pip install requests"
    echo ""
    echo "   + Termux:API App von F-Droid installieren!"
    exit 1
fi
