#!/data/data/com.termux/files/usr/bin/bash
# M.O.L.O.C.H. Termux Widget Installer
# HOMESCREEN-FREUNDLICH - Alle Widgets nutzen Pop-ups!

SHORTCUTS_DIR="$HOME/.shortcuts"
WIDGET_DIR="$(dirname "$0")"

echo "M.O.L.O.C.H. Widget Installer"
echo "================================"
echo "HOMESCREEN-FREUNDLICH Edition!"
echo ""

# Shortcuts-Ordner erstellen
mkdir -p "$SHORTCUTS_DIR"

# Widgets kopieren und ausfuehrbar machen
for widget in MolochHoert.sh MolochGuckMal.sh MolochStatus.sh MolochModus.sh MolochVolume.sh MolochFotoSchnell.sh MolochFoto.sh MolochText.sh; do
    if [ -f "$WIDGET_DIR/$widget" ]; then
        cp "$WIDGET_DIR/$widget" "$SHORTCUTS_DIR/"
        chmod +x "$SHORTCUTS_DIR/$widget"
        echo "[OK] $widget installiert"
    else
        echo "[!] $widget nicht gefunden"
    fi
done

echo ""
echo "================================"
echo "[OK] Installation abgeschlossen!"
echo ""
echo "Naechste Schritte:"
echo "1. Installiere 'Termux:Widget' aus F-Droid"
echo "2. Fuege ein Termux-Widget zu deinem Homescreen hinzu"
echo "3. Waehle das gewuenschte M.O.L.O.C.H. Script"
echo ""
echo "ALLE 8 WIDGETS SIND JETZT HOMESCREEN-FREUNDLICH!"
echo "- Input via termux-dialog (Pop-up)"
echo "- Output via termux-toast (Pop-up)"
echo "- Du bleibst auf dem Homescreen!"
echo ""
echo "Verfuegbare Widgets:"
echo "- MolochHoert     = Sprachbefehl"
echo "- MolochGuckMal   = Screenshot analysieren"
echo "- MolochFoto      = Foto mit Voice-Kommentar"
echo "- MolochFotoSchnell = Foto ohne Voice (schnell!)"
echo "- MolochText      = Text-Eingabe"
echo "- MolochStatus    = System-Status"
echo "- MolochModus     = Persoenlichkeit wechseln"
echo "- MolochVolume    = Lautstaerke regeln"
echo ""
echo "Widgets in: $SHORTCUTS_DIR"
ls -la "$SHORTCUTS_DIR"/Moloch*.sh 2>/dev/null
