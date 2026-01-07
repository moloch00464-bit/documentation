#!/data/data/com.termux/files/usr/bin/bash
# M.O.L.O.C.H. Termux Widget Installer
# HOMESCREEN-FREUNDLICH - Widgets laufen im HINTERGRUND!

# WICHTIG: .shortcuts/tasks/ = Background (kein Termux-Fenster!)
#          .shortcuts/ = Foreground (öffnet Termux!)
TASKS_DIR="$HOME/.shortcuts/tasks"
WIDGET_DIR="$(dirname "$0")"

echo "M.O.L.O.C.H. Widget Installer"
echo "================================"
echo "BACKGROUND Edition - Kein Termux-Fenster!"
echo ""

# Tasks-Ordner erstellen (WICHTIG: tasks/ Unterordner!)
mkdir -p "$TASKS_DIR"

# Widgets kopieren und ausfuehrbar machen
for widget in MolochHoert.sh MolochGuckMal.sh MolochStatus.sh MolochModus.sh MolochVolume.sh MolochFotoSchnell.sh MolochFoto.sh MolochText.sh; do
    if [ -f "$WIDGET_DIR/$widget" ]; then
        cp "$WIDGET_DIR/$widget" "$TASKS_DIR/"
        chmod +x "$TASKS_DIR/$widget"
        echo "[OK] $widget installiert"
    else
        echo "[!] $widget nicht gefunden"
    fi
done

echo ""
echo "================================"
echo "[OK] Installation abgeschlossen!"
echo ""
echo "WICHTIG: Widgets sind in .shortcuts/tasks/"
echo "         Das bedeutet: BACKGROUND EXECUTION!"
echo "         Termux wird NICHT geoeffnet!"
echo ""
echo "Naechste Schritte:"
echo "1. Installiere 'Termux:Widget' aus F-Droid"
echo "2. Fuege ein Termux-Widget zu deinem Homescreen hinzu"
echo "3. Waehle das gewuenschte M.O.L.O.C.H. Script"
echo ""
echo "Verfuegbare Widgets:"
echo "- MolochHoert       = Sprachbefehl"
echo "- MolochGuckMal     = Screenshot analysieren"
echo "- MolochFoto        = Foto mit Voice-Kommentar"
echo "- MolochFotoSchnell = Foto ohne Voice (schnell!)"
echo "- MolochText        = Text-Eingabe"
echo "- MolochStatus      = System-Status"
echo "- MolochModus       = Persoenlichkeit wechseln"
echo "- MolochVolume      = Lautstaerke regeln"
echo ""
echo "Widgets in: $TASKS_DIR"
ls -la "$TASKS_DIR"/Moloch*.sh 2>/dev/null
