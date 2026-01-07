#!/bin/bash
# MINIMAL TEST - Kein Python, nur Bash!

echo "🗣️  M.O.L.O.C.H.: Ja, Alter? Was brauchst du?"
termux-tts-speak -l de-DE "Ja, Alter? Was brauchst du?"

echo ""
echo "👉 DRÜCK ENTER WENN BEREIT..."
read

# TTS stoppen
termux-tts-speak -e
sleep 2

echo "🎤 Sprich jetzt..."
TEXT=$(termux-speech-to-text -l de-DE)

echo "DEBUG: Return code: $?"
echo "DEBUG: Text: '$TEXT'"

if [ -n "$TEXT" ]; then
    echo "✅ Verstanden: $TEXT"
else
    echo "❌ Nichts verstanden"
fi
