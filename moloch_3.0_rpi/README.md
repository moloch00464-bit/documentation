# M.O.L.O.C.H. 3.0 - Raspberry Pi 5 Edition

## Hardware Requirements

**Raspberry Pi 5 Specs:**
- RAM: 4GB+ (8GB empfohlen für beste Performance)
- Storage: 32GB+ SD Card
- Mikrofon: USB Mikrofon oder Audio HAT
- Lautsprecher: USB Speaker, 3.5mm Audio, oder HDMI
- Kamera: Pi Camera Module 3 oder USB Webcam
- Monitor: HDMI Display (optional für GUI)

## Features

### Voice Input - Vosk (Offline!)
- ✅ **Offline** - keine Internet-Verbindung nötig
- ✅ **Deutsch** - Nativ unterstützt
- ✅ **~70-80% Genauigkeit** - gut für normale Konversation
- ✅ **Kostenlos** - kein API Key nötig
- ✅ **Privacy** - alles lokal

### Voice Output - Piper TTS
- ✅ **Natürliche Stimme** - viel besser als espeak
- ✅ **Offline** - keine Cloud
- ✅ **Deutsch** - mehrere deutsche Stimmen verfügbar
- ✅ **Schnell** - RPi 5 ist stark genug

### Vision - picamera
- ✅ **Pi Camera Module 3** Support
- ✅ **USB Webcam** Support
- ✅ **Claude Vision API** - wie auf Termux

### Brain, Memory, Learning
- ✅ **Alle Features** aus M.O.L.O.C.H. 3.0
- ✅ **Persistent Storage** auf SD Card
- ✅ **Knowledge Graph**
- ✅ **Cross-Session Learning**

## Vorteile vs. Termux

| Feature | Termux (Android) | Raspberry Pi 5 |
|---------|------------------|----------------|
| Speech Recognition | termux-speech-to-text (Google abhängig) | Vosk (Offline, Deutsch) |
| Sprache per Code | ❌ Nein (Android Settings) | ✅ Ja (per Code) |
| TTS Qualität | Android TTS (variabel) | Piper (exzellent) |
| Debugging | Schwierig (kein SSH) | ✅ Einfach (SSH) |
| Installation | termux-api Probleme | ✅ Standard pip |
| Performance | Begrenzt | ✅ RPi 5 ist stark |
| Erfolgsrate | ~20% (Google App Problem) | ~80% (direkte Kontrolle) |

## Installation

Siehe `INSTALL.md` für vollständige Anleitung.

Kurz:
```bash
git clone https://github.com/moloch00464-bit/documentation.git
cd documentation/moloch_3.0_rpi
bash install_rpi.sh
```

## Kosten

- **Hardware:** ~150€ (RPi 5 8GB + Zubehör)
- **Software:** Kostenlos (alles Open Source!)
- **Laufend:** Nur Claude API (~0.50€ pro Tag bei normaler Nutzung)

## Next Steps

1. Raspberry Pi 5 Setup (OS installieren)
2. SSH aktivieren
3. Installation Script ausführen
4. Vosk Model herunterladen (~50MB)
5. Piper Voice herunterladen (~50MB)
6. Testen!

## Support

Bei Problemen: GitHub Issues oder direkt mit Claude Code debuggen!
