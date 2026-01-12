#!/bin/bash
#
# M.O.L.O.C.H. 3.0 - Voice Debug Logger
# Logged ALLE Voice-Operationen in eine Datei
#

LOG_FILE="$HOME/moloch_voice_debug.log"

echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║  M.O.L.O.C.H. - VOICE DEBUG LOGGER                            ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo ""
echo "🔍 Alle Voice-Operationen werden geloggt nach:"
echo "   📄 $LOG_FILE"
echo ""

# Start logging
{
    echo "════════════════════════════════════════════════════════════"
    echo "M.O.L.O.C.H. Voice Debug Log"
    echo "Date: $(date)"
    echo "════════════════════════════════════════════════════════════"
    echo ""

    # System Info
    echo "━━━ SYSTEM INFO ━━━"
    echo "Termux Version: $(termux-info 2>&1 | grep -i version | head -1)"
    echo "Android Version: $(getprop ro.build.version.release 2>/dev/null || echo 'N/A')"
    echo "Device: $(getprop ro.product.model 2>/dev/null || echo 'N/A')"
    echo ""

    # Locale Info
    echo "━━━ LOCALE INFO ━━━"
    echo "System Locale:"
    locale 2>&1
    echo ""
    echo "Android Language:"
    getprop persist.sys.language 2>&1 || echo "N/A"
    echo "Android Locale:"
    getprop persist.sys.locale 2>&1 || echo "N/A"
    echo ""

    # Check termux-api
    echo "━━━ TERMUX-API COMMANDS ━━━"
    for cmd in termux-tts-speak termux-speech-to-text; do
        if command -v $cmd &> /dev/null; then
            echo "✅ $cmd: $(which $cmd)"
        else
            echo "❌ $cmd: NOT FOUND"
        fi
    done
    echo ""

    # Test 1: TTS (Text-to-Speech)
    echo "━━━ TEST 1: TTS (Text-to-Speech) ━━━"
    echo "Testing: termux-tts-speak -l de-DE 'Hallo Test'"
    echo "Command started: $(date '+%H:%M:%S')"

    TTS_OUTPUT=$(termux-tts-speak -l de-DE "Hallo Test" 2>&1)
    TTS_EXIT=$?

    echo "Command finished: $(date '+%H:%M:%S')"
    echo "Exit code: $TTS_EXIT"
    echo "Output: $TTS_OUTPUT"
    echo ""

    # Test 2: STT (Speech-to-Text)
    echo "━━━ TEST 2: STT (Speech-to-Text) ━━━"
    echo "Testing: termux-speech-to-text"
    echo ""
    echo "🎤 USER INTERACTION REQUIRED:"
    echo "   Sprich jetzt: 'Hallo MOLOCH'"
    echo ""

} | tee -a "$LOG_FILE"

# Interactive STT test with logging
echo "Command started: $(date '+%H:%M:%S')" | tee -a "$LOG_FILE"

# Run STT and capture ALL output
STT_OUTPUT=$(termux-speech-to-text 2>&1)
STT_EXIT=$?

{
    echo "Command finished: $(date '+%H:%M:%S')"
    echo "Exit code: $STT_EXIT"
    echo ""
    echo "📝 RAW OUTPUT:"
    echo "────────────────────────────────────────────────────────────"
    echo "$STT_OUTPUT"
    echo "────────────────────────────────────────────────────────────"
    echo ""

    # Analyze output
    echo "━━━ ANALYSIS ━━━"

    if [ $STT_EXIT -ne 0 ]; then
        echo "⚠️  NON-ZERO EXIT CODE: $STT_EXIT"
    fi

    if [ -z "$STT_OUTPUT" ]; then
        echo "⚠️  EMPTY OUTPUT"
    else
        echo "Output length: ${#STT_OUTPUT} characters"

        # Check for API errors
        if echo "$STT_OUTPUT" | grep -iq "error"; then
            echo "🚨 ERROR DETECTED in output!"
            echo "$STT_OUTPUT" | grep -i "error"
        fi

        # Check for API keywords
        if echo "$STT_OUTPUT" | grep -iq "api"; then
            echo "🔑 API keyword found in output"
        fi

        # Check language detection
        if echo "$STT_OUTPUT" | grep -iq "hello"; then
            echo "🇬🇧 ENGLISH DETECTED! (found 'hello')"
        fi

        if echo "$STT_OUTPUT" | grep -iq "hallo"; then
            echo "🇩🇪 GERMAN DETECTED! (found 'hallo')"
        fi
    fi
    echo ""

    # Test 3: Check for API errors in logcat
    echo "━━━ TEST 3: Android Logcat (last 20 lines) ━━━"
    echo "Checking for recent errors..."
    logcat -d -t 20 2>&1 | grep -i "speech\|voice\|recognition" || echo "No speech-related logs found"
    echo ""

    # Summary
    echo "════════════════════════════════════════════════════════════"
    echo "DEBUG LOG COMPLETE"
    echo "════════════════════════════════════════════════════════════"
    echo ""

} | tee -a "$LOG_FILE"

# Show log location
echo ""
echo "✅ Log gespeichert in: $LOG_FILE"
echo ""
echo "📋 Um den kompletten Log zu sehen:"
echo "   cat $LOG_FILE"
echo ""
echo "📋 Um den Log zu Claude zu schicken:"
echo "   cat $LOG_FILE"
echo ""
echo "   Dann: Copy & Paste alles hier!"
echo ""
