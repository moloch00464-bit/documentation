#!/data/data/com.termux/files/usr/bin/bash
# MolochStatus - Status Check (HOMESCREEN-FREUNDLICH!)
# Zeigt alles als Toast Pop-up!

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

# Batterie-Status (ohne jq)
BATTERY_JSON=$(termux-battery-status 2>/dev/null)
BATTERY=$(echo "$BATTERY_JSON" | grep '"percentage"' | sed 's/[^0-9]//g')
[ -z "$BATTERY" ] && BATTERY="?"

# API Check (schneller ping)
API_STATUS="?"
if curl -s --max-time 2 https://api.anthropic.com > /dev/null 2>&1; then
    API_STATUS="OK"
else
    API_STATUS="FAIL"
fi

# Memory Stats
MEMORY_COUNT=$(grep -c '"' "$MOLOCH_DIR/langzeit.json" 2>/dev/null || echo "0")
HISTORY_COUNT=$(grep -c '"zeit"' "$MOLOCH_DIR/history.json" 2>/dev/null || echo "0")

# Aktiver Modus
CURRENT_MODE="NORMAL"
[ -f "$MOLOCH_DIR/config/current_mode.txt" ] && CURRENT_MODE=$(cat "$MOLOCH_DIR/config/current_mode.txt" | tr '[:lower:]' '[:upper:]')

# Volume
CURRENT_VOL="?"
[ -f "$MOLOCH_DIR/config/volume.txt" ] && CURRENT_VOL=$(cat "$MOLOCH_DIR/config/volume.txt")

# Status als Toast anzeigen (bleibt auf Homescreen!)
STATUS_MSG="M.O.L.O.C.H. STATUS
Batterie: ${BATTERY}%
API: ${API_STATUS}
Memory: ${MEMORY_COUNT} Eintraege
History: ${HISTORY_COUNT} Gespraeche
Modus: ${CURRENT_MODE}
Volume: ${CURRENT_VOL}%"

termux-toast -g middle -b black -c white "$STATUS_MSG" 2>/dev/null

# Kurze Vibration als Bestaetigung
termux-vibrate -d 50 2>/dev/null
