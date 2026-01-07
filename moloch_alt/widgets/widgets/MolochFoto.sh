#!/data/data/com.termux/files/usr/bin/bash
# MolochFoto - Foto MIT Voice-Kommentar (HOMESCREEN-FREUNDLICH!)
# Schiesst Foto, nimmt dann Voice-Kommentar auf, analysiert beides!

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
termux-toast -g top "MOLOCH fotografiert..." 2>/dev/null

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
termux-toast -g top "Foto OK! Jetzt sprechen..." 2>/dev/null

# 2. Voice-Kommentar aufnehmen (kurz, max 5s)
AUDIO_RAW="$MOLOCH_DIR/ohr_raw.mp4"
AUDIO_FILE="$MOLOCH_DIR/ohr.mp3"
rm -f "$AUDIO_RAW" "$AUDIO_FILE" 2>/dev/null

# Aufnahme starten
termux-microphone-record -f "$AUDIO_RAW" -l 0 2>/dev/null &
REC_PID=$!
sleep 5  # Max 5 Sekunden fuer Kommentar

# Aufnahme stoppen
termux-microphone-record -q 2>/dev/null
kill $REC_PID 2>/dev/null
sleep 0.3

# Konvertieren
if [ -f "$AUDIO_RAW" ] && [ $(stat -c%s "$AUDIO_RAW" 2>/dev/null || echo 0) -gt 1000 ]; then
    ffmpeg -y -i "$AUDIO_RAW" -acodec libmp3lame -ar 16000 -ac 1 -b:a 64k "$AUDIO_FILE" 2>/dev/null
fi

termux-toast -g top "MOLOCH analysiert..." 2>/dev/null

# 3. Analyse - Foto (Voice wurde bereits aufgenommen)
ANTWORT_FILE="/tmp/moloch_foto_$$.txt"
python moloch.py -f > "$ANTWORT_FILE" 2>&1

# 4. Antwort als Toast
if [ -f "$ANTWORT_FILE" ]; then
    ANTWORT=$(grep -v "^DEBUG\|^🔧\|^📸\|^✅\|^🎤\|^📝\|^🔄" "$ANTWORT_FILE" | tail -10)
    [ -n "$ANTWORT" ] && termux-toast -g middle -b white -c black "$ANTWORT" 2>/dev/null
    rm -f "$ANTWORT_FILE"
fi

termux-vibrate -d 50 2>/dev/null
