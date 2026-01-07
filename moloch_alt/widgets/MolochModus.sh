#!/data/data/com.termux/files/usr/bin/bash
# MolochModus - Modi Switcher Widget für Termux:Widget
# Legt in ~/.shortcuts/ als MolochModus.sh

cd "$HOME/moloch" || cd "$HOME/.moloch" || exit 1

# Vibration Feedback
termux-vibrate -d 50 2>/dev/null

# Modus-Auswahl Dialog
CHOICE=$(termux-dialog radio \
    -t "🎭 M.O.L.O.C.H. Modus wählen" \
    -v "NORMAL,HAL 9000,MAX HEADROOM,KOBOLD" 2>/dev/null | jq -r '.text // "NORMAL"')

case "$CHOICE" in
    "HAL 9000")
        echo "hal" > "$HOME/moloch/.current_mode"
        termux-toast "🔴 HAL 9000 Modus aktiviert" 2>/dev/null
        # Optional: HAL Eye Animation starten
        python hal_eye.py --boot &
        ;;
    "MAX HEADROOM")
        echo "max" > "$HOME/moloch/.current_mode"
        termux-toast "📺 MAX HEADROOM Modus aktiviert" 2>/dev/null
        ;;
    "KOBOLD")
        echo "kobold" > "$HOME/moloch/.current_mode"
        termux-toast "👺 KOBOLD Modus aktiviert" 2>/dev/null
        # Kobold-Modus starten
        python moloch.py -k &
        ;;
    *)
        echo "normal" > "$HOME/moloch/.current_mode"
        termux-toast "🤖 NORMAL Modus aktiviert" 2>/dev/null
        ;;
esac

termux-vibrate -d 100 2>/dev/null
