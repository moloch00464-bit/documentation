#!/data/data/com.termux/files/usr/bin/bash
#
# Direct Voice Test - Checkt ob termux-speech-to-text funktioniert
#

echo "🎤 VOICE TEST - Sprich jetzt etwas!"
echo ""

# Run termux-speech-to-text directly
output=$(termux-speech-to-text 2>&1)
exit_code=$?

echo ""
echo "═══════════════════════════════════════"
echo "Exit Code: $exit_code"
echo "Output: '$output'"
echo "Output Length: ${#output}"
echo "═══════════════════════════════════════"

if [ -z "$output" ]; then
    echo "⚠️ OUTPUT IST LEER!"
    echo "   Das ist das Problem - termux-speech-to-text gibt nichts zurück!"
else
    echo "✅ Output erhalten: $output"
fi
