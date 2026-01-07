# Lösungs-Optionen für M.O.L.O.C.H. Voice

## Option 1: Google App Sprache ändern (EMPFOHLEN für Termux)

**Schwierigkeit:** Einfach (User muss es machen)
**Erfolgsrate:** 95%
**Kosten:** Kostenlos

**Schritte:**
1. Öffne **Google App** (buntes G Icon)
2. Tippe rechts oben auf **Profilbild**
3. Gehe zu **Einstellungen**
4. Suche **"Sprache"** oder **"Language"**
5. Stelle auf **Deutsch**

**ODER Alternative:**
```
Android Einstellungen → Apps → Google → Sprache → Deutsch
```

**ODER System-Sprache:**
```
Android Einstellungen → System → Sprachen → Deutsch als erste Sprache
```

**Nach Änderung:**
- Termux neu starten
- M.O.L.O.C.H. testen: `cd ~/documentation/moloch_3.0 && python moloch3_unified.py`
- Sollte jetzt Deutsch erkennen!

---

## Option 2: Vosk Offline Recognition (BESTE für RPi)

**Schwierigkeit:** Mittel
**Erfolgsrate:** 80%
**Kosten:** Kostenlos

### Installation (Termux/RPi)

```bash
# Python Vosk installieren
pip install vosk

# Deutsches Model herunterladen
cd ~/
wget https://alphacephei.com/vosk/models/vosk-model-small-de-0.15.zip
unzip vosk-model-small-de-0.15.zip
mv vosk-model-small-de-0.15 vosk-model-de
```

### Python Code

```python
import json
import pyaudio
from vosk import Model, KaldiRecognizer

# Model laden
model = Model("/home/user/vosk-model-de")
rec = KaldiRecognizer(model, 16000)

# Mikrofon öffnen
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16,
                channels=1,
                rate=16000,
                input=True,
                frames_per_buffer=8000)
stream.start_stream()

print("🎤 Sprich jetzt...")

while True:
    data = stream.read(4000, exception_on_overflow=False)
    if rec.AcceptWaveform(data):
        result = json.loads(rec.Result())
        text = result.get('text', '')
        if text:
            print(f"✅ Verstanden: {text}")
            break

stream.stop_stream()
stream.close()
p.terminate()
```

### Vorteile
- ✅ Komplett offline (keine Internet-Verbindung)
- ✅ Kostenlos
- ✅ Sprache per Code wählbar (kein Android Settings)
- ✅ Privacy (kein Google)

### Nachteile
- ❌ ~70-80% Genauigkeit (schlechter als Google)
- ❌ Model ~50MB Download
- ❌ Braucht pyaudio (kann auf Termux schwierig sein)

---

## Option 3: Whisper (OpenAI) - BESTE Qualität

**Schwierigkeit:** Mittel-Schwer
**Erfolgsrate:** 70% (langsam auf RPi)
**Kosten:** Kostenlos (lokal) oder $0.006/Minute (API)

### Installation

```bash
pip install openai-whisper
```

### Python Code (Lokal)

```python
import whisper

# Model laden (einmalig, dauert!)
model = whisper.load_model("base")  # tiny, base, small, medium, large

# Audio aufnehmen (termux oder pyaudio)
# ... record audio to file ...

# Transkribieren
result = model.transcribe("audio.mp3", language="de")
text = result["text"]
print(f"✅ Verstanden: {text}")
```

### Vorteile
- ✅ BESTE Genauigkeit (~95%)
- ✅ Offline möglich
- ✅ Mehrsprachig ohne Config

### Nachteile
- ❌ SEHR langsam auf Handy/RPi 3 (30 Sekunden für 5 Sekunden Audio)
- ❌ Hoher RAM-Verbrauch (2-4 GB)
- ❌ RPi 4 mit 4GB+ empfohlen

---

## Option 4: Google Cloud Speech API (Kostenpflichtig)

**Schwierigkeit:** Einfach
**Erfolgsrate:** 95%
**Kosten:** $0.006/15 Sekunden (~$0.024/Minute)

### Installation

```bash
pip install google-cloud-speech
```

### Python Code

```python
from google.cloud import speech
import io

client = speech.SpeechClient()

# Audio aufnehmen
# ... record audio to file ...

with io.open("audio.wav", "rb") as audio_file:
    content = audio_file.read()

audio = speech.RecognitionAudio(content=content)
config = speech.RecognitionConfig(
    encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
    sample_rate_hertz=16000,
    language_code="de-DE",
)

response = client.recognize(config=config, audio=audio)

for result in response.results:
    text = result.alternatives[0].transcript
    print(f"✅ Verstanden: {text}")
```

### Vorteile
- ✅ BESTE Genauigkeit (~99%)
- ✅ Schnell
- ✅ Language per Code
- ✅ Funktioniert überall (Internet nötig)

### Nachteile
- ❌ Kostet Geld
- ❌ Braucht Internet
- ❌ Privacy (Google)
- ❌ API Key Management

---

## Option 5: Hybrid Ansatz (SMART!)

**Kombination aus mehreren:**

```python
def listen_smart():
    # Versuch 1: Termux (schnell, kostenlos)
    if is_termux():
        text = termux_speech_to_text()
        if text:
            return text

    # Versuch 2: Vosk (offline fallback)
    if vosk_available():
        text = vosk_recognize()
        if text:
            return text

    # Versuch 3: Google API (beste Qualität, kostet)
    if google_api_key:
        text = google_speech_api()
        return text

    return None
```

**Vorteile:**
- Nutzt beste verfügbare Option
- Fallback bei Fehlern
- Kosten-Optimierung

---

## Empfehlung nach Platform

### Termux/Android:
1. **Erste Wahl:** Google App auf Deutsch → termux-speech-to-text nutzen
2. **Wenn nicht möglich:** Vosk (schwierig auf Termux)
3. **Letzter Ausweg:** Google Cloud API (kostet)

### Raspberry Pi:
1. **Erste Wahl:** Vosk (offline, kostenlos, gut genug)
2. **Beste Qualität:** Whisper (wenn RPi 4 mit 4GB+)
3. **Production:** Google Cloud API (wenn Budget da)

### Desktop/Server:
1. **Erste Wahl:** Whisper (beste Offline-Option)
2. **Production:** Google Cloud API
3. **Kostenlos:** Vosk

---

## Next Steps

**Für aktuellen Xiaomi/Termux:**
1. User muss Google App Sprache auf Deutsch stellen
2. Testen ob termux-speech-to-text dann Deutsch erkennt
3. Falls ja → M.O.L.O.C.H. 3.1 funktioniert!
4. Falls nein → Raspberry Pi Plan

**Für Raspberry Pi (falls User wechselt):**
1. SSH Zugriff einrichten
2. Vosk + Deutsches Model installieren
3. Python Voice Code umschreiben
4. Testen & Iterieren (mit direktem Zugriff!)

---

## Quellen

- [Vosk API](https://alphacephei.com/vosk/)
- [Vosk Models](https://alphacephei.com/vosk/models)
- [Whisper GitHub](https://github.com/openai/whisper)
- [Google Cloud Speech](https://cloud.google.com/speech-to-text)
- [pyaudio](https://people.csail.mit.edu/hubert/pyaudio/)
