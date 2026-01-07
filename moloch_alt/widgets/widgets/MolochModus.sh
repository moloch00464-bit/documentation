#!/data/data/com.termux/files/usr/bin/bash
# MolochModus - Modi Switcher (HOMESCREEN-FREUNDLICH!)
# Komplette Interaktion via Pop-ups!

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
mkdir -p "$MOLOCH_DIR/config"

# Vibration Feedback
termux-vibrate -d 50 2>/dev/null

# Aktuellen Modus laden
CURRENT="NORMAL"
[ -f "$MOLOCH_DIR/config/current_mode.txt" ] && CURRENT=$(cat "$MOLOCH_DIR/config/current_mode.txt" | tr '[:lower:]' '[:upper:]')

# Modus-Auswahl via Pop-up Dialog
RESULT=$(termux-dialog radio \
    -t "MOLOCH Modus (Aktuell: $CURRENT)" \
    -v "NORMAL,HAL 9000,MAX HEADROOM,KOBOLD" 2>/dev/null)

# Text extrahieren ohne jq
CHOICE=$(echo "$RESULT" | grep -o '"text" *: *"[^"]*"' | sed 's/.*: *"\([^"]*\)"/\1/')

# Modus setzen + Toast Feedback
case "$CHOICE" in
    "HAL 9000")
        echo "hal" > "$MOLOCH_DIR/config/current_mode.txt"
        termux-toast -g middle "HAL 9000 aktiviert - Alle Systeme nominal, Markus." 2>/dev/null
        termux-vibrate -d 200 2>/dev/null
        ;;
    "MAX HEADROOM")
        echo "max" > "$MOLOCH_DIR/config/current_mode.txt"
        termux-toast -g middle "M-M-MAX HEADROOM aktiviert! Zik-Zik-Zik!" 2>/dev/null
        termux-vibrate -d 200 2>/dev/null
        ;;
    "KOBOLD")
        echo "kobold" > "$MOLOCH_DIR/config/current_mode.txt"
        termux-toast -g middle "KOBOLD aktiviert - Ich nerve dich jetzt!" 2>/dev/null
        termux-vibrate -d 200 2>/dev/null
        # Kobold im Hintergrund starten
        nohup python moloch.py -k > /dev/null 2>&1 &
        ;;
    "NORMAL"|*)
        echo "moloch" > "$MOLOCH_DIR/config/current_mode.txt"
        termux-toast -g middle "NORMAL Modus aktiviert" 2>/dev/null
        termux-vibrate -d 200 2>/dev/null
        ;;
esac
