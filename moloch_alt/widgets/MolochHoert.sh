#!/data/data/com.termux/files/usr/bin/bash
# MolochHoert - Voice Input Widget für Termux:Widget
# Legt in ~/.shortcuts/ als MolochHoert.sh

cd "$HOME/moloch" || cd "$HOME/.moloch" || exit 1

# Vibration Feedback
termux-vibrate -d 100 2>/dev/null

# Status anzeigen
termux-toast -g top "🎤 MOLOCH hört..." 2>/dev/null

# Voice Input starten
python moloch.py -v

# Fertig-Feedback
termux-vibrate -d 50 2>/dev/null
