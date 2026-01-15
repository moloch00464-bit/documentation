# M.O.L.O.C.H. 3.0 RPi - Quick Start

## 5-Minute Setup (wenn RPi schon läuft)

```bash
# 1. Update System
sudo apt update && sudo apt upgrade -y

# 2. Clone Repository
cd ~
git clone https://github.com/moloch00464-bit/documentation.git

# 3. Run Installation
cd documentation/moloch_3.0_rpi
chmod +x install_rpi.sh
./install_rpi.sh

# 4. Set API Key
export ANTHROPIC_API_KEY='sk-ant-YOUR-KEY-HERE'
echo 'export ANTHROPIC_API_KEY="sk-ant-YOUR-KEY-HERE"' >> ~/.bashrc

# 5. Test
~/moloch_test_voice.sh

# 6. Start!
~/moloch_voice.sh
```

**Fertig!** M.O.L.O.C.H. läuft jetzt auf Deutsch mit Vosk!

---

## Was du brauchst

**Minimum:**
- Raspberry Pi 5 (4GB) - ~80€
- USB Mikrofon - ~20€
- USB Lautsprecher - ~20€
- SD Card 32GB - ~10€
- **Total: ~130€**

**Empfohlen:**
- Raspberry Pi 5 (8GB) - ~100€
- Gutes USB Mikrofon - ~40€
- Bluetooth Speaker - ~50€
- SD Card 64GB - ~15€
- Pi Camera Module 3 - ~30€
- **Total: ~235€**

---

## Schnelltest - Funktioniert alles?

**1. Lautsprecher:**
```bash
espeak -v de "Test"
```
Hörst du was? ✅ Ja → Weiter | ❌ Nein → `alsamixer` öffnen, Lautstärke hoch

**2. Mikrofon:**
```bash
arecord -d 3 test.wav && aplay test.wav && rm test.wav
```
Hörst du deine Stimme? ✅ Ja → Weiter | ❌ Nein → `arecord -l` checken

**3. Vosk:**
```bash
~/moloch_test_voice.sh
```
Sag "Hallo Test" wenn gefragt. Erkennt es Deutsch? ✅ Ja → FERTIG! 🎉

---

## Vergleich: Termux vs Raspberry Pi

| Feature | Xiaomi/Termux | Raspberry Pi 5 |
|---------|---------------|----------------|
| **Setup** | ⚠️ Schwierig (termux-api) | ✅ Standard pip |
| **Sprache** | ❌ Google App Settings | ✅ Per Code (de-DE) |
| **Erfolgsrate** | ❌ 20% (wegen Google) | ✅ 80% |
| **Debugging** | ❌ Kein SSH | ✅ SSH + Logs |
| **Offline** | ❌ Braucht Google | ✅ Vosk offline |
| **Qualität** | ⚠️ 95% (wenn Google auf Deutsch) | ⚠️ 75% (Vosk) |
| **Kosten** | ✅ 0€ Hardware | ⚠️ ~150€ Hardware |
| **Mobilität** | ✅ Handy in der Tasche | ❌ Stationär |

**Fazit:** RPi für zuhause/Büro, Termux für unterwegs (wenn Google App auf Deutsch!)

---

## Wartung

**Updates holen:**
```bash
cd ~/documentation && git pull
```

**M.O.L.O.C.H. aktualisieren:**
```bash
cd ~/documentation/moloch_3.0_rpi
cp moloch3_rpi.py ~/moloch_rpi/
cp voice_rpi.py ~/moloch_rpi/
cp -r core ~/moloch_rpi/
```

**Logs anschauen:**
```bash
# Falls als Service läuft
journalctl -u moloch.service -f

# Falls manuell gestartet
# Logs sind im Terminal
```

---

## Häufige Probleme

**"Vosk erkennt nichts"**
→ Sprich lauter, näher ans Mikro, deutlicher

**"API Error 401"**
→ API Key vergessen: `export ANTHROPIC_API_KEY='sk-ant-...'`

**"No sound"**
→ `alsamixer` öffnen, F6 drücken, Device wählen, Lautstärke hoch

**"Permission denied"**
→ Scripts executable machen: `chmod +x ~/moloch_*.sh`

---

## Next Steps

**Wenn alles läuft:**
1. Teste Vision Mode: `~/moloch_vision.sh`
2. Lese INSTALL.md für Autostart
3. Optimiere Vosk Model (größer = besser, langsamer)
4. SSH vom Handy: `ssh pi@raspberrypi.local`

**Bei Problemen:**
→ Siehe INSTALL.md "Troubleshooting" (Seite 10-12)

---

## Performance

**Vosk Small Model (Default):**
- ✅ Schnell (~1s Latenz)
- ⚠️ 70-75% Genauigkeit
- ✅ 50MB

**Vosk Large Model (Upgrade):**
- ⚠️ Langsam (~3s Latenz)
- ✅ 85-90% Genauigkeit
- ⚠️ 400MB

**Upgrade Befehl:**
```bash
cd ~
wget https://alphacephei.com/vosk/models/vosk-model-de-0.21.zip
unzip vosk-model-de-0.21.zip
mv vosk-model-de-0.21 vosk-model-de
```

---

## Support

**GitHub Issues:** https://github.com/moloch00464-bit/documentation/issues

**Bei Session mit Claude Code:**
- Stelle sicher SSH läuft
- Claude kann direkt debuggen!

---

**🎉 VIEL ERFOLG!**
