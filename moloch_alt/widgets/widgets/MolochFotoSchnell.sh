#!/data/data/com.termux/files/usr/bin/bash
# MolochFotoSchnell - Foto OHNE Voice-Kommentar (SCHNELL!)
# Schiesst Foto und analysiert direkt, kein Voice Input!

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
termux-vibrate -d 100 2>/dev/null
termux-toast -g top "MOLOCH fotografiert schnell..." 2>/dev/null

# 1. Foto schiessen
FOTO_FILE="$MOLOCH_DIR/auge.jpg"
rm -f "$FOTO_FILE" 2>/dev/null
termux-camera-photo -c 0 "$FOTO_FILE" 2>/dev/null
sleep 0.5

if [ ! -f "$FOTO_FILE" ]; then
    termux-toast -g middle "Kamera Fehler!" 2>/dev/null
    exit 1
fi

termux-vibrate -d 50 2>/dev/null
termux-toast -g top "Analysiere..." 2>/dev/null

# 2. Direkt analysieren (kein Voice)
ANTWORT_FILE="/tmp/moloch_foto_schnell_$$.txt"
python moloch.py -f > "$ANTWORT_FILE" 2>&1

# 3. Antwort als Toast
if [ -f "$ANTWORT_FILE" ]; then
    ANTWORT=$(grep -v "^DEBUG\|^🔧\|^📸\|^✅" "$ANTWORT_FILE" | tail -10)
    [ -n "$ANTWORT" ] && termux-toast -g middle -b white -c black "$ANTWORT" 2>/dev/null
    rm -f "$ANTWORT_FILE"
fi

termux-vibrate -d 50 2>/dev/null
