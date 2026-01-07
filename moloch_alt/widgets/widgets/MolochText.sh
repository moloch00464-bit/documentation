#!/data/data/com.termux/files/usr/bin/bash
# MolochText - Text Eingabe (HOMESCREEN-FREUNDLICH!)
# Input via Pop-up Dialog, Output via Toast!

# MOLOCH_DIR finden
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
termux-vibrate -d 50 2>/dev/null

# Input via Pop-up Dialog
RESULT=$(termux-dialog text -t "Nachricht an M.O.L.O.C.H." -i "Was moechtest du sagen?" 2>/dev/null)

# Text extrahieren (ohne jq!)
TEXT=$(echo "$RESULT" | grep '"text"' | sed 's/.*"text" *: *"\([^"]*\)".*/\1/')

if [ -n "$TEXT" ] && [ "$TEXT" != "null" ]; then
    termux-toast -g top "MOLOCH denkt nach..." 2>/dev/null

    # M.O.L.O.C.H. aufrufen, Antwort speichern
    ANTWORT_FILE="/tmp/moloch_text_$$.txt"
    python moloch.py "$TEXT" > "$ANTWORT_FILE" 2>&1

    # Zeige Antwort als Toast
    if [ -f "$ANTWORT_FILE" ]; then
        ANTWORT=$(grep -v "^DEBUG\|^🔧" "$ANTWORT_FILE" | tail -10)
        if [ -n "$ANTWORT" ]; then
            termux-toast -g middle -b white -c black "$ANTWORT" 2>/dev/null
        fi
        rm -f "$ANTWORT_FILE"
    fi
else
    termux-toast -g middle "Abgebrochen" 2>/dev/null
fi

termux-vibrate -d 50 2>/dev/null
