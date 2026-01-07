#!/data/data/com.termux/files/usr/bin/bash
# FIX WIDGETS - Erstellt alle Widgets NEU ohne jq
# Kopiere dieses Script aufs Handy und fuehre es aus!

SHORTCUTS_DIR="$HOME/.shortcuts"
mkdir -p "$SHORTCUTS_DIR"

echo "=== ERSTELLE WIDGETS NEU (OHNE JQ) ==="

# 1. MolochHoert.sh
cat > "$SHORTCUTS_DIR/MolochHoert.sh" << 'ENDSCRIPT'
#!/data/data/com.termux/files/usr/bin/bash
cd "$HOME/moloch" || exit 1
termux-vibrate -d 100 2>/dev/null
termux-toast -g top "MOLOCH hoert..." 2>/dev/null
python moloch.py -v
termux-vibrate -d 50 2>/dev/null
ENDSCRIPT
chmod +x "$SHORTCUTS_DIR/MolochHoert.sh"
echo "1. MolochHoert.sh erstellt"

# 2. MolochGuckMal.sh
cat > "$SHORTCUTS_DIR/MolochGuckMal.sh" << 'ENDSCRIPT'
#!/data/data/com.termux/files/usr/bin/bash
cd "$HOME/moloch" || exit 1
termux-vibrate -d 100 2>/dev/null
termux-toast -g top "MOLOCH analysiert Screenshot..." 2>/dev/null
python moloch.py -s
termux-vibrate -d 50 2>/dev/null
ENDSCRIPT
chmod +x "$SHORTCUTS_DIR/MolochGuckMal.sh"
echo "2. MolochGuckMal.sh erstellt"

# 3. MolochFoto.sh
cat > "$SHORTCUTS_DIR/MolochFoto.sh" << 'ENDSCRIPT'
#!/data/data/com.termux/files/usr/bin/bash
cd "$HOME/moloch" || exit 1
termux-vibrate -d 100 2>/dev/null
termux-toast -g top "MOLOCH fotografiert..." 2>/dev/null
python moloch.py -f
termux-vibrate -d 50 2>/dev/null
ENDSCRIPT
chmod +x "$SHORTCUTS_DIR/MolochFoto.sh"
echo "3. MolochFoto.sh erstellt"

# 4. MolochText.sh - OHNE JQ!
cat > "$SHORTCUTS_DIR/MolochText.sh" << 'ENDSCRIPT'
#!/data/data/com.termux/files/usr/bin/bash
cd "$HOME/moloch" || exit 1
termux-vibrate -d 50 2>/dev/null
RESULT=$(termux-dialog text -t "Nachricht an MOLOCH" -i "Was moechtest du sagen?" 2>/dev/null)
TEXT=$(echo "$RESULT" | grep -o '"text" *: *"[^"]*"' | sed 's/"text" *: *"\([^"]*\)"/\1/')
if [ -n "$TEXT" ]; then
    python moloch.py "$TEXT"
fi
ENDSCRIPT
chmod +x "$SHORTCUTS_DIR/MolochText.sh"
echo "4. MolochText.sh erstellt (OHNE JQ)"

# 5. MolochStatus.sh - OHNE JQ!
cat > "$SHORTCUTS_DIR/MolochStatus.sh" << 'ENDSCRIPT'
#!/data/data/com.termux/files/usr/bin/bash
cd "$HOME/moloch" || exit 1
termux-vibrate -d 50 2>/dev/null

# Batterie - OHNE JQ
BATT_RAW=$(termux-battery-status 2>/dev/null)
BATTERY=$(echo "$BATT_RAW" | grep -o '"percentage" *: *[0-9]*' | grep -o '[0-9]*')
[ -z "$BATTERY" ] && BATTERY="?"

# API Check
API="?"
curl -s --max-time 2 https://api.anthropic.com >/dev/null 2>&1 && API="OK" || API="FAIL"

# Modus
MODE="NORMAL"
[ -f "$HOME/moloch/config/current_mode.txt" ] && MODE=$(cat "$HOME/moloch/config/current_mode.txt")

# Anzeigen
MSG="MOLOCH STATUS
Batterie: ${BATTERY}%
API: ${API}
Modus: ${MODE}"

termux-toast -g middle "$MSG" 2>/dev/null
echo "$MSG"
ENDSCRIPT
chmod +x "$SHORTCUTS_DIR/MolochStatus.sh"
echo "5. MolochStatus.sh erstellt (OHNE JQ)"

# 6. MolochModus.sh - OHNE JQ! Speichert in config/current_mode.txt
cat > "$SHORTCUTS_DIR/MolochModus.sh" << 'ENDSCRIPT'
#!/data/data/com.termux/files/usr/bin/bash
cd "$HOME/moloch" || exit 1
mkdir -p "$HOME/moloch/config"
termux-vibrate -d 50 2>/dev/null

RESULT=$(termux-dialog radio -t "MOLOCH Modus" -v "NORMAL,HAL 9000,MAX HEADROOM,KOBOLD" 2>/dev/null)
CHOICE=$(echo "$RESULT" | grep -o '"text" *: *"[^"]*"' | sed 's/.*: *"\([^"]*\)"/\1/')

case "$CHOICE" in
    "HAL 9000")
        echo "hal" > "$HOME/moloch/config/current_mode.txt"
        termux-toast "HAL 9000 aktiviert" 2>/dev/null
        ;;
    "MAX HEADROOM")
        echo "max" > "$HOME/moloch/config/current_mode.txt"
        termux-toast "MAX HEADROOM aktiviert" 2>/dev/null
        ;;
    "KOBOLD")
        echo "kobold" > "$HOME/moloch/config/current_mode.txt"
        termux-toast "KOBOLD aktiviert" 2>/dev/null
        python moloch.py -k &
        ;;
    *)
        echo "moloch" > "$HOME/moloch/config/current_mode.txt"
        termux-toast "NORMAL aktiviert" 2>/dev/null
        ;;
esac
termux-vibrate -d 100 2>/dev/null
ENDSCRIPT
chmod +x "$SHORTCUTS_DIR/MolochModus.sh"
echo "6. MolochModus.sh erstellt (OHNE JQ)"

echo ""
echo "=== FERTIG ==="
echo "Alle 6 Widgets in: $SHORTCUTS_DIR"
echo ""
echo "TEST: Kein jq mehr vorhanden:"
grep -l "jq" "$SHORTCUTS_DIR"/Moloch*.sh 2>/dev/null && echo "FEHLER: jq gefunden!" || echo "OK: Kein jq gefunden"
