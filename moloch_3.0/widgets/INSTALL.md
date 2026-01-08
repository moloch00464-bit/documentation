# M.O.L.O.C.H. 3.0 - Termux:Widget Installation

## 📱 Widgets für Homescreen

### Voraussetzung:
```bash
pkg install termux-widget
```

### Installation:

**1. Shortcuts-Verzeichnis erstellen:**
```bash
mkdir -p ~/.shortcuts
```

**2. Widgets kopieren:**
```bash
cd ~/documentation/moloch_3.0/widgets
cp *.sh ~/.shortcuts/
chmod +x ~/.shortcuts/*.sh
```

**3. Widget zum Homescreen hinzufügen:**
- Long-press auf Homescreen
- "Widgets" auswählen
- "Termux:Widget" wählen
- Widget platzieren
- Buttons erscheinen automatisch!

### Verfügbare Widgets:

- **MOLOCH_Voice.sh** - 🎤 Voice Mode (Sprechen + Hören)
- **MOLOCH_Vision.sh** - 📷 Vision Mode (Foto + Bildanalyse)

### Später (nach Memory-Integration):

- **MOLOCH_Memory.sh** - 🧠 Memory Status
- **MOLOCH_Clear.sh** - 🗑️ Clear History

## 🔧 Troubleshooting:

**Widget erscheint nicht:**
- Prüfe ob `~/.shortcuts/` existiert
- Prüfe ob Scripts ausführbar sind: `ls -l ~/.shortcuts/`
- Termux:Widget neu laden (Widget entfernen + neu hinzufügen)

**Script startet nicht:**
- Prüfe Pfade in den Scripts
- Teste manuell: `bash ~/.shortcuts/MOLOCH_Voice.sh`
