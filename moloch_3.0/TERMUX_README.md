# 🤖 M.O.L.O.C.H. FIXED - Installation & Test

## 📥 1. DATEIEN AUF DEIN SMARTPHONE KOPIEREN

Kopiere diese 2 Dateien in dein Termux:
- `diagnose.py` → `~/diagnose.py`
- `moloch_fixed.py` → `~/moloch_fixed.py`

**Via Termux:**
```bash
# In Downloads kopiert? Dann:
cp ~/storage/downloads/diagnose.py ~/
cp ~/storage/downloads/moloch_fixed.py ~/
chmod +x ~/diagnose.py
chmod +x ~/moloch_fixed.py
```

---

## 🔍 2. DIAGNOSE LAUFEN LASSEN

**Check was fehlt:**
```bash
python ~/diagnose.py
```

Das Script zeigt dir **genau** was fehlt und wie du es installierst!

---

## ⚙️ 3. FEHLENDE SACHEN INSTALLIEREN

### Termux-API App
- Download von F-Droid: https://f-droid.org/packages/com.termux.api/
- Installiere die App
- Erlaube Permissions (Mikro, Kamera)

### Termux Packages
```bash
pkg update
pkg install termux-api
pkg install ffmpeg
pkg install python
pip install requests
```

### API Keys setzen
```bash
# In ~/.bashrc eintragen:
nano ~/.bashrc

# Diese Zeilen hinzufügen:
export ANTHROPIC_API_KEY="sk-ant-..."
export OPENAI_API_KEY="dein-openai-key-hier"

# Speichern: CTRL+X, dann Y, dann Enter

# Keys laden:
source ~/.bashrc
```

---

## 🧪 4. TESTEN!

### Test 1: Text Mode (einfachster Test!)
```bash
python ~/moloch_fixed.py -t "Hey Moloch, funktionierst du?"
```

**Erwartung:**
- ✅ Du siehst die Antwort als Text
- ✅ TTS spricht (wenn termux-tts-speak funktioniert)

### Test 2: Voice Mode (Ohren testen)
```bash
python ~/moloch_fixed.py
```

**Erwartung:**
- ✅ M.O.L.O.C.H. sagt "Ja?"
- ✅ Mikro nimmt 20 Sek auf
- ✅ Whisper transkribiert
- ✅ Claude antwortet

### Test 3: Vision (Augen testen)
```bash
python ~/moloch_fixed.py -a "Was siehst du?"
```

**Erwartung:**
- ✅ Kamera macht Foto
- ✅ Claude beschreibt das Bild
- ✅ Antwort als Text + TTS

---

## ❌ WENN WAS NICHT GEHT

### "termux-xxx command not found"
```bash
pkg install termux-api
```

### "ffmpeg not found"
```bash
pkg install ffmpeg
```

### "API Key fehlt"
```bash
# Check ob gesetzt:
echo $ANTHROPIC_API_KEY

# Wenn leer:
export ANTHROPIC_API_KEY="dein-key"
# ODER in ~/.bashrc eintragen (siehe oben)
```

### "Permission denied" (Mikro/Kamera)
- Termux:API App Permissions checken
- Android Settings → Apps → Termux:API → Permissions
- Mikro + Kamera erlauben

### "Keine Internet-Verbindung"
- WiFi/Mobile Daten an?
- `ping google.com` testen

---

## ✅ WENN ALLES LÄUFT

### Backup vom alten M.O.L.O.C.H.
```bash
cp ~/moloch.py ~/moloch_backup_$(date +%Y%m%d).py
```

### Neuen M.O.L.O.C.H. aktivieren
```bash
cp ~/moloch_fixed.py ~/moloch.py
```

### Oder: Beide parallel nutzen
```bash
# Alter M.O.L.O.C.H.:
python ~/moloch.py

# Neuer M.O.L.O.C.H.:
python ~/moloch_fixed.py
```

---

## 🚀 USAGE

```bash
# Voice Mode (Standard)
python ~/moloch.py

# Text Mode
python ~/moloch.py -t "Deine Frage"

# Vision (Foto + Frage)
python ~/moloch.py -a "Was siehst du?"

# Hilfe
python ~/moloch.py -h
```

---

## 🆘 SUPPORT

Wenn's immer noch nicht geht:
1. Run `python ~/diagnose.py` und schick Output
2. Check Fehler-Meldungen genau an
3. Test einzeln: TTS, Mikro, Kamera

---

## 🖤 FEATURES

- ✅ **Crash-Safe** - Stürzt nicht ab!
- ✅ **Error Messages** - Sagt was fehlt!
- ✅ **Voice Input** - Whisper STT
- ✅ **Voice Output** - TTS
- ✅ **Vision** - Foto beschreiben
- ✅ **Memory** - Langzeitgedächtnis
- ✅ **Spotify Brain** - Kennt deinen Musikgeschmack!

---

**Let's fix M.O.L.O.C.H.! 🔧🤖**
