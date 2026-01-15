# User Hardware & Environment Info

## Android Device

**Marke:** Xiaomi
**OS:** Android (Version unbekannt - TODO: `termux-info` ausführen)
**Termux Version:** Latest (Stand 2025-01-07 nach `pkg upgrade`)

## Termux API Version

**termux-api Package:**
- Nach `pkg upgrade termux-api` (2025-01-07)
- **Unterstützt NICHT:** `-l` Parameter für termux-speech-to-text
- **Unterstützt NICHT:** `-e` Parameter für termux-tts-speak (stop)
- **Unterstützt:** `-p` (pitch) und `-r` (rate) für termux-tts-speak

**Getestete Commands:**
```bash
termux-speech-to-text -l de-DE  # ❌ "illegal option -l"
termux-tts-speak -e             # ❌ "illegal option -e"
termux-tts-speak -p 1.0 -r 1.0 "test"  # ✅ Funktioniert
```

## System Language Settings

**System-Sprache:** Deutsch (vermutlich)
**Google App Sprache:** ENGLISCH (Problem!)
- User hat System nie auf Englisch gestellt
- Google App scheint separates Language Setting zu haben
- Deswegen erkennt termux-speech-to-text nur Englisch

## Was funktioniert

✅ **termux-speech-to-text** - Erkennung funktioniert (aber nur Englisch)
✅ **termux-tts-speak** - TTS funktioniert
✅ **termux-camera-photo** - Kamera funktioniert (nicht getestet aber sollte)
✅ **Internet** - Verbindung OK
✅ **Termux:API App** - Installiert und funktioniert

## Was NICHT funktioniert

❌ **Deutsch erkennen** - Trotz deutscher System-Sprache
❌ **termux-location** - Timeout nach 10 Sekunden (GPS Problem)
❌ **Language Parameter** - termux-api Version zu alt

## Probleme

### Problem 1: Google App Language auf Englisch
- **Symptom:** "Hallo" wird als "hello" erkannt
- **Ursache:** Google App Sprache != System-Sprache
- **Lösung:** Android Settings → Apps → Google → Sprache → Deutsch

### Problem 2: Location Timeout
```
⚠️  Location failed: Command '['termux-location']' timed out after 10 seconds
📍 Location: Nicht verfügbar
```
- **Mögliche Ursachen:**
  - GPS Permission fehlt
  - GPS nicht aktiviert
  - Kein GPS Signal (Indoor)
- **Lösung:** TODO - GPS Permissions checken

### Problem 3: Alte termux-api Version
- Keine `-l` Option für Language
- User hat bereits `pkg upgrade` gemacht
- → Auch neueste Version hat diese Features nicht!

## M.O.L.O.C.H. 2.0 vs 3.1

**M.O.L.O.C.H. 2.0:**
- Voice hat funktioniert (vermutlich weil damals Google App auf Deutsch war?)
- User konnte Deutsch sprechen und wurde verstanden

**M.O.L.O.C.H. 3.1:**
- Voice erkennt technisch, aber nur Englisch
- Timing-Probleme wurden gefixt (TTS async)
- API funktioniert (aber 401 Error - API Key Problem)

## Debugging Commands für Future

```bash
# System Info
termux-info

# Audio Devices
termux-audio-info

# API Versions
pkg list-installed | grep termux-api

# Test Speech Recognition
termux-speech-to-text

# Test TTS
termux-tts-speak "Test Deutsch"

# Check Locale
echo $LANG
locale

# Check Android Version
getprop ro.build.version.release

# Check Device Model
getprop ro.product.model
```

## Raspberry Pi Plan (Future)

**Wenn User auf RPi wechselt:**
- Vosk für Deutsch Speech Recognition (offline)
- espeak/piper für TTS (offline)
- picamera für Vision
- Python 3.10+
- Standard Linux - VIEL einfacher zu debuggen!

**Wahrscheinlichkeit Erfolg:** 70-80% (vs. 10% auf Termux mit Language Problem)
