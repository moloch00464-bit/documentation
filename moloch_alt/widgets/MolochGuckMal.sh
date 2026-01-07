#!/data/data/com.termux/files/usr/bin/bash
# MolochGuckMal - Screenshot Analyse Widget für Termux:Widget
# Legt in ~/.shortcuts/ als MolochGuckMal.sh

cd "$HOME/moloch" || cd "$HOME/.moloch" || exit 1

# Vibration Feedback
termux-vibrate -d 100 2>/dev/null

# Status anzeigen
termux-toast -g top "📸 MOLOCH analysiert Screenshot..." 2>/dev/null

# Screenshot machen und analysieren
python moloch.py -s

# Fertig-Feedback
termux-vibrate -d 50 2>/dev/null
