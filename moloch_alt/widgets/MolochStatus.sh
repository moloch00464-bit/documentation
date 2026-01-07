#!/data/data/com.termux/files/usr/bin/bash
# MolochStatus - Status Check Widget für Termux:Widget
# Legt in ~/.shortcuts/ als MolochStatus.sh

cd "$HOME/moloch" || cd "$HOME/.moloch" || exit 1

# Vibration Feedback
termux-vibrate -d 50 2>/dev/null

# Batterie-Status
BATTERY=$(termux-battery-status 2>/dev/null | jq -r '.percentage // "?"')

# API Check (schneller ping)
API_STATUS="?"
if curl -s --max-time 2 https://api.anthropic.com > /dev/null 2>&1; then
    API_STATUS="✅"
else
    API_STATUS="❌"
fi

# Memory Stats
MEMORY_COUNT=$(cat "$HOME/moloch/langzeit.json" 2>/dev/null | jq 'reduce .[] as $arr (0; . + ($arr | length))' 2>/dev/null || echo "0")
HISTORY_COUNT=$(cat "$HOME/moloch/history.json" 2>/dev/null | jq 'length' 2>/dev/null || echo "0")

# Aktiver Modus
CURRENT_MODE="NORMAL"
if [ -f "$HOME/moloch/.current_mode" ]; then
    CURRENT_MODE=$(cat "$HOME/moloch/.current_mode")
fi

# Status anzeigen
STATUS_MSG="🤖 M.O.L.O.C.H. STATUS
━━━━━━━━━━━━━━━━━━
🔋 Batterie: ${BATTERY}%
🌐 API: ${API_STATUS}
🧠 Memory: ${MEMORY_COUNT} Einträge
📜 History: ${HISTORY_COUNT} Gespräche
🎭 Modus: ${CURRENT_MODE}
━━━━━━━━━━━━━━━━━━"

# Als Dialog anzeigen
termux-dialog -t "M.O.L.O.C.H. Status" -i "$STATUS_MSG" 2>/dev/null || echo "$STATUS_MSG"
