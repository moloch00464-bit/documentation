# M.O.L.O.C.H. 3.0 - Raspberry Pi 5 Installation Guide

## Voraussetzungen

### Hardware
- **Raspberry Pi 5** (8GB empfohlen, 4GB funktioniert auch)
- **SD Card:** 32GB+ (64GB empfohlen)
- **USB Mikrofon** oder Audio HAT
- **Lautsprecher:** USB, 3.5mm, oder HDMI
- **Kamera:** Pi Camera Module 3 oder USB Webcam
- **Monitor:** HDMI (optional für GUI)
- **Netzteil:** Offizielles RPi 5 Netzteil (27W)

### Software
- **Raspberry Pi OS:** Bookworm (64-bit) empfohlen
- **Python:** 3.11+ (kommt mit OS)
- **SSH:** Aktiviert für Remote-Zugriff

## Installation

### 1. Raspberry Pi OS Setup

**SD Card vorbereiten:**
1. Download Raspberry Pi Imager: https://www.raspberrypi.com/software/
2. Wähle: **Raspberry Pi OS (64-bit)**
3. Erweiterte Optionen:
   - ✅ SSH aktivieren
   - ✅ WLAN konfigurieren
   - ✅ Hostname: `moloch` (optional)
4. Schreibe auf SD Card

**Booten:**
1. SD Card in RPi 5
2. Verbinde Mikrofon, Lautsprecher, Kamera
3. Power on
4. Warte ~2 Minuten für ersten Boot

### 2. SSH Verbindung (vom PC)

```bash
# Finde RPi IP Adresse
ping raspberrypi.local

# SSH verbinden
ssh pi@raspberrypi.local
# Default Passwort: raspberry (oder was du im Imager gesetzt hast)
```

### 3. System Update

```bash
sudo apt update
sudo apt upgrade -y
sudo reboot
```

### 4. M.O.L.O.C.H. Installation

**Download vom GitHub:**
```bash
cd ~
git clone https://github.com/moloch00464-bit/documentation.git
cd documentation/moloch_3.0_rpi
```

**Installation ausführen:**
```bash
chmod +x install_rpi.sh
./install_rpi.sh
```

**Das Script installiert:**
- ✅ System Dependencies (portaudio, opencv, etc.)
- ✅ Python Packages (vosk, sounddevice, anthropic, etc.)
- ✅ Vosk German Model (~50MB)
- ✅ Piper TTS + German Voice (~50MB)
- ✅ Launch Scripts

**Dauer:** ~15-20 Minuten (je nach Internet)

### 5. API Key konfigurieren

**Anthropic API Key holen:**
1. Gehe zu: https://console.anthropic.com/
2. Erstelle Account (falls noch nicht)
3. API Keys → Create Key
4. Kopiere Key (beginnt mit `sk-ant-...`)

**Key setzen:**
```bash
export ANTHROPIC_API_KEY='sk-ant-api03-YOUR-KEY-HERE'

# Permanent speichern:
echo 'export ANTHROPIC_API_KEY="sk-ant-api03-YOUR-KEY-HERE"' >> ~/.bashrc
source ~/.bashrc
```

### 6. Audio Test

**Lautsprecher testen:**
```bash
# Test Sound
speaker-test -t wav -c 2

# Test TTS
espeak -v de "Hallo, ich bin Moloch"
```

**Mikrofon testen:**
```bash
# Liste Audio Devices
arecord -l

# Test Recording
arecord -d 5 -f cd test.wav
aplay test.wav
rm test.wav
```

**Falls kein Sound:**
```bash
# Audio Mixer öffnen
alsamixer

# Pfeiltasten: Lautstärke anpassen
# F6: Device wählen
# M: Mute/Unmute
```

### 7. Kamera Test

**Pi Camera:**
```bash
# Test Photo
libcamera-still -o test.jpg

# Bild anschauen (wenn Monitor angeschlossen)
feh test.jpg
```

**USB Webcam:**
```bash
# Check Device
ls /dev/video*

# Test with fswebcam
sudo apt install fswebcam
fswebcam test.jpg
```

### 8. M.O.L.O.C.H. Test

**Voice System Test:**
```bash
~/moloch_test_voice.sh
```

**Was sollte passieren:**
- 🗣️ TTS sagt "Hallo! Ich bin Moloch. Sprich jetzt!"
- 🎤 5 Sekunden aufnehmen
- 👂 Zeigt erkannten Text
- ✅ Spricht zurück was du gesagt hast

**Voice Mode starten:**
```bash
~/moloch_voice.sh
```

**Vision Mode starten:**
```bash
~/moloch_vision.sh
```

## Troubleshooting

### Problem: "Vosk model not found"

```bash
cd ~
wget https://alphacephei.com/vosk/models/vosk-model-small-de-0.15.zip
unzip vosk-model-small-de-0.15.zip
mv vosk-model-small-de-0.15 vosk-model-de
```

### Problem: "No sound from speaker"

```bash
# Check ALSA
alsamixer
# Drücke F6, wähle richtiges Device
# Erhöhe Lautstärke mit Pfeiltasten
# Drücke M wenn "MM" angezeigt wird (unmute)

# Test
speaker-test -t wav -c 2
```

### Problem: "Mic not working"

```bash
# Liste Devices
arecord -l

# Test specific device (z.B. card 1, device 0)
arecord -D plughw:1,0 -d 3 test.wav
aplay test.wav
```

### Problem: "Camera not detected"

```bash
# Pi Camera
vcgencmd get_camera

# Enable Camera in raspi-config
sudo raspi-config
# Interface Options → Camera → Enable

# Reboot
sudo reboot
```

### Problem: "API Error 401"

```bash
# Check API Key
echo $ANTHROPIC_API_KEY

# Sollte anzeigen: sk-ant-api03-...
# Falls leer: API Key nicht gesetzt!

# Setze Key
export ANTHROPIC_API_KEY='sk-ant-YOUR-KEY'
echo 'export ANTHROPIC_API_KEY="sk-ant-YOUR-KEY"' >> ~/.bashrc
```

### Problem: "Python ImportError"

```bash
# Aktiviere Virtual Environment
source ~/moloch_env/bin/activate

# Re-installiere Dependencies
cd ~/documentation/moloch_3.0_rpi
pip install -r requirements.txt
```

### Problem: "Vosk erkennt nichts"

**Mögliche Ursachen:**
1. Zu leise gesprochen → Näher ans Mikro
2. Mikrofon zu leise → `alsamixer` → Capture erhöhen
3. Falsches Mikrofon → `arecord -l` → Device checken
4. Background Noise → Ruhigere Umgebung

**Debug:**
```bash
# Test Voice System mit Debug
python ~/moloch_rpi/voice_rpi.py
```

### Problem: "Performance langsam"

**Vosk ist langsam? Upgrade zu größerem Model:**
```bash
cd ~
# Download large model (~400MB, bessere Genauigkeit)
wget https://alphacephei.com/vosk/models/vosk-model-de-0.21.zip
unzip vosk-model-de-0.21.zip
mv vosk-model-de-0.21 vosk-model-de
```

**Oder nutze kleines Model für Geschwindigkeit:**
```bash
# Tiny model (~50MB, schlechtere Genauigkeit)
wget https://alphacephei.com/vosk/models/vosk-model-small-de-0.15.zip
```

## Autostart (Optional)

**M.O.L.O.C.H. beim Boot starten:**

```bash
# Systemd Service erstellen
sudo nano /etc/systemd/system/moloch.service
```

**Inhalt:**
```ini
[Unit]
Description=M.O.L.O.C.H. Voice Assistant
After=network.target sound.target

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi/moloch_rpi
ExecStart=/home/pi/moloch_env/bin/python /home/pi/moloch_rpi/moloch3_rpi.py
Restart=on-failure
RestartSec=10
Environment="ANTHROPIC_API_KEY=sk-ant-YOUR-KEY-HERE"

[Install]
WantedBy=multi-user.target
```

**Aktivieren:**
```bash
sudo systemctl enable moloch.service
sudo systemctl start moloch.service

# Status checken
sudo systemctl status moloch.service

# Logs anschauen
journalctl -u moloch.service -f
```

## Remote Access (SSH von Handy)

**Vom Xiaomi/Termux:**
```bash
# Termux auf Handy
pkg install openssh

# SSH zum RPi
ssh pi@raspberrypi.local

# M.O.L.O.C.H. starten
~/moloch_voice.sh
```

## Updates

**M.O.L.O.C.H. updaten:**
```bash
cd ~/documentation
git pull
cd moloch_3.0_rpi
cp -r core ~/moloch_rpi/
cp -r moloch_io ~/moloch_rpi/
cp moloch3_rpi.py ~/moloch_rpi/
cp voice_rpi.py ~/moloch_rpi/
```

**System updaten:**
```bash
sudo apt update
sudo apt upgrade -y
```

**Python Packages updaten:**
```bash
source ~/moloch_env/bin/activate
pip install --upgrade anthropic vosk sounddevice
```

## Performance Tuning

**RPi 5 übertakten (für bessere Vosk Performance):**
```bash
sudo nano /boot/config.txt

# Add:
over_voltage=6
arm_freq=2800

# Reboot
sudo reboot
```

**Hinweis:** Braucht gute Kühlung!

## Support

**Bei Problemen:**
1. Check Logs: `journalctl -u moloch.service -f`
2. Test einzelne Komponenten (Voice, Camera, TTS)
3. GitHub Issue erstellen mit Logs

**Performance:**
- RPi 5 8GB: ✅ Exzellent
- RPi 5 4GB: ✅ Gut (Vosk small model)
- RPi 4 8GB: ⚠️ Okay (Vosk tiny model)
- RPi 4 4GB: ⚠️ Langsam (nur espeak TTS)

## Kosten

**Hardware:** ~150-200€
- RPi 5 8GB: ~80€
- SD Card 64GB: ~15€
- USB Mikrofon: ~20€
- USB Speaker: ~20€
- Pi Camera: ~30€
- Gehäuse + Kühlung: ~20€

**Laufend:**
- Claude API: ~0.50€/Tag (normal usage)
- Strom: ~5€/Jahr (RPi 5 ~15W)

**Total:** ~200€ Hardware + ~15€/Monat Claude API
