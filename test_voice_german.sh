#!/bin/bash
#
# M.O.L.O.C.H. 3.0 - Deutscher Voice Test
# Testet TTS und STT mit deutscher Sprache
#

echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║  M.O.L.O.C.H. 3.0 - DEUTSCHER VOICE TEST                      ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo ""

# Test 1: TTS Deutsch
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🎙️  TEST 1: Text-to-Speech (Deutsch)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Spreche: 'Hallo, ich bin MOLOCH Drei Punkt Null'"
echo ""

termux-tts-speak -l de-DE "Hallo, ich bin MOLOCH Drei Punkt Null"

echo ""
read -p "Hast du die deutsche Stimme gehört? (j/n) " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Jj]$ ]]; then
    echo "✅ TTS Deutsch funktioniert!"
else
    echo "❌ TTS Problem"
    echo ""
    echo "🔧 Mögliche Fixes:"
    echo "   1. Lautstärke checken"
    echo "   2. Settings → Accessibility → Text-to-speech"
    echo "   3. Deutsche TTS Engine installieren (Google TTS)"
fi

echo ""
echo ""

# Test 2: STT Deutsch (OHNE -l Parameter)
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🎤 TEST 2: Speech-to-Text OHNE Language-Parameter (Default)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
read -p "Teste STT ohne -l Parameter? (j/n) " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Jj]$ ]]; then
    echo "🎤 Sprich jetzt: 'Hallo MOLOCH'"
    echo ""

    STT_OUTPUT=$(termux-speech-to-text 2>&1)

    echo ""
    echo "📝 Transkript (DEFAULT):"
    echo "$STT_OUTPUT"
    echo ""
fi

echo ""

# Test 3: STT Deutsch (MIT -l de-DE Parameter)
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🎤 TEST 3: Speech-to-Text MIT -l de-DE (Deutsch forciert)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
read -p "Teste STT mit -l de-DE Parameter? (j/n) " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Jj]$ ]]; then
    echo "🎤 Sprich jetzt: 'Hallo MOLOCH'"
    echo "   (MIT -l de-DE Parameter)"
    echo ""

    STT_OUTPUT_DE=$(termux-speech-to-text -l de-DE 2>&1)

    echo ""
    echo "📝 Transkript (DEUTSCH):"
    echo "$STT_OUTPUT_DE"
    echo ""

    if [ -n "$STT_OUTPUT_DE" ]; then
        echo "✅ STT mit -l de-DE funktioniert!"
        echo ""
        echo "💡 WICHTIG: M.O.L.O.C.H. muss -l de-DE verwenden!"
    else
        echo "❌ STT kein Output"
    fi
fi

echo ""
echo ""

# Test 4: Verfügbare Sprachen anzeigen
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📋 INFO: Verfügbare Sprachen testen"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Teste verschiedene deutsche Varianten:"
echo ""

for lang in de-DE de-AT de-CH de; do
    echo -n "Testing: $lang ... "
    # Quick test (timeout after 1 second)
    timeout 1s termux-speech-to-text -l "$lang" 2>&1 > /dev/null && echo "✅ Verfügbar" || echo "❌ Nicht verfügbar"
done

echo ""
echo ""
echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║  🎯 ZUSAMMENFASSUNG                                           ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo ""
echo "Um deutsche Sprache zu verwenden:"
echo ""
echo "TTS (Text-to-Speech):"
echo "  termux-tts-speak -l de-DE \"Dein Text\""
echo ""
echo "STT (Speech-to-Text):"
echo "  termux-speech-to-text -l de-DE"
echo ""
echo "💡 M.O.L.O.C.H. muss den -l de-DE Parameter verwenden!"
echo ""
