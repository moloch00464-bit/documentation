# 📱 M.O.L.O.C.H. 3.0 - Termux Widgets Setup

## 🎯 WAS SIND WIDGETS?

**Termux Widgets** = Shortcuts auf dem Android Homescreen!

Ein Tap → M.O.L.O.C.H. startet! 🚀

---

## 📦 INSTALLATION

### 1. Termux:Widget App installieren

**Download:**
- F-Droid: https://f-droid.org/packages/com.termux.widget/
- Oder Google Play Store

### 2. Widget Scripts installieren

```bash
cd ~/moloch_3.0

# Copy widget scripts to ~/.shortcuts/
mkdir -p ~/.shortcuts
cp .shortcuts/* ~/.shortcuts/

# Make executable
chmod +x ~/.shortcuts/*
```

---

## 🎨 WIDGETS HINZUFÜGEN

### **Auf dem Homescreen:**

1. **Long press** auf freien Platz
2. **Widgets** auswählen
3. **Termux:Widget** finden
4. **Widget hinzufügen** (drag & drop)

### **Verfügbare Widgets:**

📱 **M.O.L.O.C.H.** - Voice Mode (Standard)
  → Startet Voice Mode, sagt "Ja?", hört zu

📸 **M.O.L.O.C.H. Vision** - Vision Mode
  → Macht Foto und beschreibt es

💬 **M.O.L.O.C.H. Interactive** - Interactive Mode
  → Chat Mode (REPL)

---

## 🎯 EIGENE WIDGETS ERSTELLEN

### Beispiel: "M.O.L.O.C.H. HAL Mode"

```bash
# Create file: ~/.shortcuts/M.O.L.O.C.H. HAL
nano ~/.shortcuts/M.O.L.O.C.H.\ HAL

# Add:
#!/data/data/com.termux/files/usr/bin/bash
cd ~/moloch_3.0 && python moloch3.py --hal -i

# Make executable:
chmod +x ~/.shortcuts/M.O.L.O.C.H.\ HAL
```

### Beispiel: "Quick Question"

```bash
# ~/.shortcuts/Ask M.O.L.O.C.H.
#!/data/data/com.termux/files/usr/bin/bash
cd ~/moloch_3.0
python -c "
from io.text import TextIO
question = TextIO.input('Frage: ')
import subprocess
subprocess.run(['python', 'moloch3.py', '-t', question])
"
```

---

## 🔔 WIDGET MIT NOTIFICATION

```bash
# ~/.shortcuts/M.O.L.O.C.H. Background
#!/data/data/com.termux/files/usr/bin/bash
cd ~/moloch_3.0

# Notification anzeigen
termux-notification \
  --title "M.O.L.O.C.H. 3.0" \
  --content "Running in background..." \
  --id moloch \
  --ongoing

# M.O.L.O.C.H. starten
python moloch3.py -i
```

---

## 💡 PRO TIPPS

### **Widget mit Input Dialog:**

```bash
#!/data/data/com.termux/files/usr/bin/bash
cd ~/moloch_3.0

# Dialog zeigen
QUESTION=$(termux-dialog text -t "Frage an M.O.L.O.C.H." | jq -r .text)

if [ ! -z "$QUESTION" ]; then
    python moloch3.py -t "$QUESTION"
fi
```

### **Widget mit Toast Feedback:**

```bash
#!/data/data/com.termux/files/usr/bin/bash
cd ~/moloch_3.0

termux-toast "Starting M.O.L.O.C.H...."
termux-vibrate -d 100

python moloch3.py -i
```

### **Widget mit Wake Lock:**

```bash
#!/data/data/com.termux/files/usr/bin/bash
cd ~/moloch_3.0

# Wake lock aktivieren
termux-wake-lock

# M.O.L.O.C.H. starten
python moloch3.py

# Wake lock deaktivieren
termux-wake-unlock
```

---

## 🎨 WIDGET ICONS

**Termux:Widget** zeigt Icons basierend auf Dateinamen:
- Emojis im Namen werden als Icon gezeigt!

```bash
# Beispiele:
~/.shortcuts/🤖 M.O.L.O.C.H.
~/.shortcuts/📸 Vision
~/.shortcuts/💬 Chat
~/.shortcuts/🖤 HAL Mode
```

---

## 🛠️ TROUBLESHOOTING

### **Widget erscheint nicht:**

1. Check: `ls ~/.shortcuts/`
2. Check Permissions: `chmod +x ~/.shortcuts/*`
3. Termux:Widget App neu öffnen
4. Widget neu hinzufügen

### **Widget funktioniert nicht:**

1. Test manuell in Termux:
   ```bash
   bash ~/.shortcuts/M.O.L.O.C.H.
   ```
2. Check Errors
3. Fix Script

### **Widget zu langsam:**

```bash
# Add am Anfang:
#!/data/data/com.termux/files/usr/bin/bash
termux-toast -s "Starting..."
# Rest of script...
```

---

## 📱 HOMESCREEN SETUP VORSCHLAG

```
┌─────────────────────┐
│                     │
│    🤖 M.O.L.O.C.H.  │ ← Voice Mode
│                     │
│    📸 Vision        │ ← Photo + Describe
│                     │
│    💬 Interactive   │ ← Chat Mode
│                     │
│    🖤 HAL           │ ← HAL Mode
│                     │
└─────────────────────┘
```

---

## 🖤 READY TO GO!

**Mit Widgets:**
- Ein Tap → M.O.L.O.C.H. startet! 🚀
- Kein Terminal öffnen nötig
- Schneller Zugriff
- Custom Shortcuts möglich

**Let's go, Alter! 🖤😈**
