# Termux Speech-to-Text Sprach-Problem

## Das Problem

**termux-speech-to-text erkennt nur Englisch, obwohl System auf Deutsch**

User: Xiaomi Android Handy, System auf Deutsch
M.O.L.O.C.H. Voice Input erkennt nur Englisch ("hello" statt "hallo")

---

## Root Cause (Recherche 2025-01-07)

### termux-speech-to-text HAT KEINE SPRACH-PARAMETER!

Laut [Termux API Usage](https://github.com/gangadharKorrapati/termux-api-usage):
- **Usage**: `termux-speech-to-text` (KEINE Parameter!)
- **KEINE** `-l` Option für Sprache
- **KEINE** Command-line Parameter für Language Selection

**Im Vergleich:**
- `termux-tts-speak` **HAT** `-l language` Parameter ✅
- `termux-speech-to-text` **HAT NICHT** `-l` Parameter ❌

### Wie termux-speech-to-text funktioniert

Laut [DEV Community](https://dev.to/terminaltools/how-to-build-voice-activated-tools-using-termux-voice-apis-gp0):
- Nutzt **Android's built-in Speech Recognition API**
- Benötigt **Google App** installiert und enabled
- Sprache kommt von **Android System Settings**, nicht vom Command!

### Das bestätigt auch [Issue #437](https://github.com/termux/termux-api/issues/437):
> "termux-speech-to-text, but it doesn't understand spanish"

Gleiche Problem - keine Möglichkeit Sprache per Command zu setzen!

---

## Lösung 1: Android Settings ändern (EINZIGE echte Lösung)

**Laut [Android 12 TTS Guide](https://mcmw.abilitynet.org.uk/how-to-change-the-language-and-voice-used-in-text-to-speech-tts-in-android-12):**

```
Android Einstellungen → Accessibility → Text-to-speech output → Language
```

**ODER:**

```
Einstellungen → Apps → Google → Sprache → Deutsch
```

**ODER System-Sprache:**

```
Einstellungen → System → Sprachen → Deutsch als erste Sprache
```

---

## Lösung 2: Alternative Speech Recognition (Offline)

### Vosk (Offline, Deutsch Support)

Laut [Vosk API](https://alphacephei.com/vosk/):
- **Offline Speech Recognition**
- **20+ Sprachen** inkl. Deutsch (de-DE)
- Läuft auf Android, Raspberry Pi, Linux
- Python, Java, C# Support

**Installation:**
```bash
pip install vosk
# Download German model
wget https://alphacephei.com/vosk/models/vosk-model-de-0.21.zip
```

**Vorteile:**
- ✅ Komplett offline
- ✅ Kostenlos
- ✅ Sprache per Code wählbar

**Nachteile:**
- ❌ ~70-80% Genauigkeit (schlechter als Google)
- ❌ Größer (~50MB Model)
- ❌ Langsamer

### Termux-DeepSpeech

Laut [GitHub](https://github.com/T-vK/Termux-DeepSpeech):
- Open source offline speech recognition
- Mozilla DeepSpeech in Termux
- Deutsch Support möglich (mit passendem Model)

---

## Was wir versucht haben (funktioniert NICHT)

❌ `termux-speech-to-text -l de-DE` → "illegal option -l"
❌ Locale Environment Variables (LANG=de_DE.UTF-8) → Kein Effekt
❌ File Output statt capture_output → Funktioniert, aber immer noch Englisch
❌ Code-Updates → Kann Sprache nicht per Code ändern

**Warum?** → termux-speech-to-text nutzt Android API, die nutzt Google App Settings!

---

## Termux API Version Info

**User's Version:**
- Nach `pkg upgrade termux-api` (2025-01-07)
- Immer noch: `termux-speech-to-text: illegal option -l`
- → Auch neuere Versionen haben KEINE -l Option!

**Laut [Issue #404](https://github.com/termux/termux-api/issues/404):**
> "termux-speech-to-text not working on Android 11"
> "Google changed the speech-to-text API in Android 11"

→ Termux API hat Probleme mit neuen Android Versionen!

---

## Empfehlung für M.O.L.O.C.H.

**Für Termux/Android:**
1. **User muss** Google App Sprache auf Deutsch stellen (Android Settings)
2. **Keine Code-Lösung** möglich mit termux-speech-to-text

**Für Raspberry Pi:**
1. **Vosk** nutzen (Offline, Deutsch, per Code steuerbar)
2. **Oder:** Whisper (bessere Qualität, langsamer)
3. **Oder:** Google Speech API (beste Qualität, kostet Geld)

---

## Quellen

- [Termux API Usage](https://github.com/gangadharKorrapati/termux-api-usage)
- [DEV: Voice-Activated Tools](https://dev.to/terminaltools/how-to-build-voice-activated-tools-using-termux-voice-apis-gp0)
- [Issue #437: Spanish Speech](https://github.com/termux/termux-api/issues/437)
- [Vosk API](https://alphacephei.com/vosk/)
- [Termux-DeepSpeech](https://github.com/T-vK/Termux-DeepSpeech)
- [Android 12 TTS Guide](https://mcmw.abilitynet.org.uk/how-to-change-the-language-and-voice-used-in-text-to-speech-tts-in-android-12)

---

## Fazit

**termux-speech-to-text ist NICHT für mehrsprachige Apps geeignet!**

Die Sprache ist **hardcoded** durch Android Settings, nicht steuerbar per Code.

**Für Production:** Vosk oder andere Offline-Recognition nutzen!
