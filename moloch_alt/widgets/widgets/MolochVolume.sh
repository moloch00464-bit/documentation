#!/data/data/com.termux/files/usr/bin/bash
# MolochVolume - Lautstaerke-Kontrolle (HOMESCREEN-FREUNDLICH!)
# Slider fuer Volume, speichert in config/volume.txt

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

# Aktuellen Wert laden (default 70%)
CURRENT_VOL="70"
[ -f "$MOLOCH_DIR/config/volume.txt" ] && CURRENT_VOL=$(cat "$MOLOCH_DIR/config/volume.txt")

# Volume-Auswahl via Slider Dialog
RESULT=$(termux-dialog seekbar \
    -t "MOLOCH Lautstaerke" \
    -m "Aktuell: ${CURRENT_VOL}%" \
    --range "0,100" 2>/dev/null)

# Wert extrahieren (ohne jq)
NEW_VOL=$(echo "$RESULT" | grep -o '"value" *: *[0-9]*' | grep -o '[0-9]*')

# Wenn abgebrochen, nichts tun
if [ -z "$NEW_VOL" ]; then
    termux-toast -g middle "Abgebrochen" 2>/dev/null
    exit 0
fi

# Volume speichern
echo "$NEW_VOL" > "$MOLOCH_DIR/config/volume.txt"

# System-Lautstaerke setzen (alle Streams)
termux-volume music "$NEW_VOL" 2>/dev/null
termux-volume notification "$NEW_VOL" 2>/dev/null
termux-volume alarm "$NEW_VOL" 2>/dev/null
termux-volume ring "$NEW_VOL" 2>/dev/null

# Feedback
if [ "$NEW_VOL" -eq 0 ]; then
    termux-toast -g middle "STUMM" 2>/dev/null
elif [ "$NEW_VOL" -lt 30 ]; then
    termux-toast -g middle "Leise: ${NEW_VOL}%" 2>/dev/null
elif [ "$NEW_VOL" -lt 70 ]; then
    termux-toast -g middle "Mittel: ${NEW_VOL}%" 2>/dev/null
else
    termux-toast -g middle "Laut: ${NEW_VOL}%" 2>/dev/null
fi

termux-vibrate -d 100 2>/dev/null
