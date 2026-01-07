# API KEYS SETUP - M.O.L.O.C.H. UNIFIED
## Wie du deine API Keys wieder einsetzt

**WICHTIG:** Ohne API Keys läuft M.O.L.O.C.H. nicht! ❌

---

## **WO SIND DEINE ALTEN KEYS?** 🔍

Deine API Keys sind wahrscheinlich noch hier auf dem Handy:

```bash
# In der alten moloch.py (2.0):
grep "sk-ant" ~/moloch/moloch.py
grep "sk-proj" ~/moloch/moloch.py
```

**KOPIERE DIE KEYS AUS DER AUSGABE!** (Die langen Strings nach `=`)

---

## **OPTION 1: Keys in config.py setzen** (Permanent) 📝

### **Schritt 1: Keys aus altem moloch.py holen**

```bash
# Zeige Anthropic Key
grep "ANTHROPIC_KEY\|anthropic" ~/moloch/moloch.py | grep "sk-ant"

# Zeige OpenAI Key (falls du einen hast)
grep "OPENAI_KEY\|openai" ~/moloch/moloch.py | grep "sk-proj"
```

### **Schritt 2: config.py editieren**

```bash
cd ~/moloch_3.0
nano core/config.py
```

**Ändere diese Zeile:**
```python
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "DEIN_ANTHROPIC_KEY_HIER")
```

**Nach:**
```python
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "sk-ant-api03-DEIN_ECHTER_KEY_HIER")
```

**Speichern:** `Ctrl+O`, `Enter`, `Ctrl+X`

---

## **OPTION 2: Environment Variable** (Temporär) 🌍

```bash
# Setze Key für Session
export ANTHROPIC_API_KEY="sk-ant-api03-DEIN_KEY_HIER"

# Starte M.O.L.O.C.H.
cd ~/moloch_3.0
python moloch3_unified.py
```

**Dauerhaft machen:**
```bash
# In ~/.bashrc eintragen
echo 'export ANTHROPIC_API_KEY="sk-ant-api03-DEIN_KEY_HIER"' >> ~/.bashrc
source ~/.bashrc
```

---

## **OPTION 3: .env File** (Sicher & Clean) 🔒

```bash
# Erstelle .env File
cd ~/moloch_3.0
cat > .env << 'EOF'
ANTHROPIC_API_KEY=sk-ant-api03-DEIN_KEY_HIER
OPENAI_API_KEY=sk-proj-DEIN_KEY_HIER
EOF

# Protect the file
chmod 600 .env

# M.O.L.O.C.H. lädt automatisch .env
python moloch3_unified.py
```

---

## **AUTOMATISCHES SETUP SCRIPT** 🚀

```bash
#!/bin/bash
# setup_keys.sh - Holt Keys aus 2.0 und setzt sie in 3.0

echo "🔑 M.O.L.O.C.H. API KEYS SETUP"
echo "=============================="
echo ""

# Keys aus 2.0 holen
echo "📋 Suche Keys in M.O.L.O.C.H. 2.0..."
ANTHROPIC=$(grep -oP 'sk-ant-api03-[A-Za-z0-9_-]+' ~/moloch/moloch.py | head -1)

if [ -n "$ANTHROPIC" ]; then
    echo "✅ Anthropic Key gefunden: ${ANTHROPIC:0:20}..."

    # In config.py setzen
    sed -i "s/DEIN_ANTHROPIC_KEY_HIER/$ANTHROPIC/g" ~/moloch_3.0/core/config.py

    echo "✅ Key in config.py gesetzt!"
else
    echo "❌ Kein Anthropic Key gefunden!"
    echo "Setze ihn manuell in ~/moloch_3.0/core/config.py"
fi

echo ""
echo "🎯 READY! Starte M.O.L.O.C.H. mit:"
echo "   cd ~/moloch_3.0 && python moloch3_unified.py"
```

**Ausführen:**
```bash
chmod +x setup_keys.sh
./setup_keys.sh
```

---

## **VERIFY: Sind Keys gesetzt?** ✅

```bash
cd ~/moloch_3.0
python -c "from core.config import ANTHROPIC_API_KEY; print('✅ Key:', ANTHROPIC_API_KEY[:20] + '...' if len(ANTHROPIC_API_KEY) > 20 else '❌ NICHT GESETZT')"
```

**Erwartete Ausgabe:**
```
✅ Key: sk-ant-api03-xxxxxxx...
```

---

## **FEHLERSUCHE** 🔍

### **"ANTHROPIC_API_KEY nicht gesetzt!"**
- Check: `grep ANTHROPIC_API_KEY ~/moloch_3.0/core/config.py`
- Sollte NICHT "DEIN_ANTHROPIC_KEY_HIER" sein!

### **"API Error 401: Invalid API Key"**
- Key ist falsch oder abgelaufen
- Check auf: https://console.anthropic.com/
- Neuen Key erstellen und einsetzen

### **Keys aus GitHub Backup holen?**
```bash
# NEIN! Die wurden entfernt wegen Secret Scanning!
# Hol sie aus deiner lokalen ~/moloch/moloch.py
```

---

## **SICHERHEIT** 🔒

**NIEMALS:**
- ❌ Keys in Git committen
- ❌ Keys in Screenshots teilen
- ❌ Keys in Chat posten

**IMMER:**
- ✅ Keys in config.py oder .env
- ✅ .env in .gitignore
- ✅ chmod 600 für Key-Files

---

## **QUICK START** ⚡

```bash
# 1. Keys aus 2.0 holen
grep "sk-ant" ~/moloch/moloch.py

# 2. In 3.0 config.py setzen
nano ~/moloch_3.0/core/config.py
# Ersetze "DEIN_ANTHROPIC_KEY_HIER" mit deinem echten Key

# 3. Testen
cd ~/moloch_3.0
python moloch3_unified.py

# 4. Wenn M.O.L.O.C.H. startet = ✅ ERFOLG!
```

---

**NACH DEM SETUP:** M.O.L.O.C.H. UNIFIED läuft! 🤖🖤
