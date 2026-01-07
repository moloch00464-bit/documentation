#!/data/data/com.termux/files/usr/bin/bash
# MolochHoert - Voice Input Widget (HOMESCREEN-FREUNDLICH!)
# Bleibt auf Homescreen, nutzt Pop-ups!

# MOLOCH_DIR finden - probiere alle möglichen Pfade
if [ -d "$HOME/moloch" ]; then
    MOLOCH_DIR="$HOME/moloch"
elif [ -d "/storage/emulated/0/moloch" ]; then
    MOLOCH_DIR="/storage/emulated/0/moloch"
elif [ -d "$HOME/.moloch" ]; then
    MOLOCH_DIR="$HOME/.moloch"
else
    termux-toast -g middle "FEHLER: moloch nicht gefunden!" 2>/dev/null
    exit 1
fi

cd "$MOLOCH_DIR" || exit 1

# Vibration Feedback
termux-vibrate -d 100 2>/dev/null

# Status via Toast
termux-toast -g top "MOLOCH hoert..." 2>/dev/null

# Voice Input + Antwort speichern
ANTWORT_FILE="/tmp/moloch_antwort_$$.txt"
python moloch.py -v > "$ANTWORT_FILE" 2>&1

# Zeige Antwort als Toast
if [ -f "$ANTWORT_FILE" ]; then
    # Extrahiere nur die Antwort (letzte Zeilen ohne Debug)
    ANTWORT=$(grep -v "^DEBUG\|^🔧\|^🎤\|^📝\|^🔄\|^⏱️\|^🔇" "$ANTWORT_FILE" | tail -10)
    if [ -n "$ANTWORT" ]; then
        termux-toast -g middle -b white -c black "$ANTWORT" 2>/dev/null
    fi
    rm -f "$ANTWORT_FILE"
fi

# Fertig-Feedback
termux-vibrate -d 50 2>/dev/null
