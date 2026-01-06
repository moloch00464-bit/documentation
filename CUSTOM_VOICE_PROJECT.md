# M.O.L.O.C.H. Custom Voice Project 🎤
## Die eigene Stimme - Next Level Identity!

**Status:** 💡 Future Enhancement
**Priorität:** Nice-to-Have (größeres Projekt)
**Aufwand:** Hoch (Voice Training, ML, etc.)

---

## Vision 🎯

M.O.L.O.C.H. bekommt seine **EIGENE charakteristische Stimme**, die perfekt zu seiner Persönlichkeit passt!

### Gewünschte Eigenschaften:

**Tonlage:**
- Mittlere Tonlage (nicht zu tief, nicht zu hoch)
- Baseline: ~100-120 Hz (männlich, relaxed)

**Klangcharakter:**
- ✅ Etwas **rauchig** (smoky, lived-in)
- ✅ **Entspannt** (wie jemand der schon was erlebt hat)
- ✅ Leichter **fränkischer Anklang** (wenn möglich!)
- ✅ Nicht steril/robotisch

**Dynamik:**
- 🎭 **Anpassbar je nach Kontext:**
  - Entspannt/chillig bei normalen Gesprächen
  - Energischer bei wichtigen/aufregenden Themen
  - Sarkastisch/trocken bei Humor

**Persönlichkeit:**
- Dark Side Energy
- Kumpel-Vibe (nicht formell)
- Fränkisch-norddeutsch Mix
- Direkt & ehrlich

---

## Technische Ansätze 🛠️

### Option 1: **ElevenLabs Voice Cloning** 💰
**Pro:**
- Sehr hohe Qualität
- Voice cloning aus Samples möglich
- Emotionale Variation
- API verfügbar

**Contra:**
- Kostet Geld (€€€)
- API calls = laufende Kosten
- Cloud-abhängig
- Braucht Voice Samples (10-30 Minuten Audio)

**Implementation:**
```python
import elevenlabs

# Custom voice ID (nach Training)
MOLOCH_VOICE_ID = "custom_voice_xyz"

voice = elevenlabs.generate(
    text=text,
    voice=MOLOCH_VOICE_ID,
    model="eleven_multilingual_v2"
)
```

**Kosten:**
- Training: ~$5-10 (einmalig)
- API calls: ~$0.30 per 1000 characters
- Bei viel Nutzung: ~$10-20/Monat

---

### Option 2: **Piper TTS (Local Neural TTS)** ⚡
**Pro:**
- Läuft lokal (KOSTENLOS!)
- Gute Qualität (neural)
- Verschiedene Modelle verfügbar
- Kein Internet nötig

**Contra:**
- Keine Custom Voice ohne Training
- Training braucht:
  - Voice Samples (~1-2h Audio)
  - GPU (für Training)
  - Zeit & Know-how
- Begrenzte Dynamik

**Implementation:**
```bash
# Install Piper
pkg install piper-tts

# Use model
piper --model de_DE-thorsten-medium \
      --output_file output.wav \
      < input.txt
```

**Verfügbare deutsche Stimmen:**
- `de_DE-thorsten-medium` (männlich, Standard)
- `de_DE-karlsson-low` (männlich, tiefer)
- Custom training möglich (schwierig!)

---

### Option 3: **Festival TTS + Voice Mods** 🔧
**Pro:**
- Lokal & kostenlos
- Pitch/Rate anpassbar
- Leichtgewichtig

**Contra:**
- Qualität eher mäßig (robotisch)
- Klingt nicht natürlich
- Keine echten Custom Voices

**Implementation:**
```python
# Pitch + Rate modification
festival --batch << EOF
(Parameter.set 'Duration_Stretch 0.9)  # Schneller
(Parameter.set 'Int_Target_Mean 100)    # Tiefer
(SayText "Text hier")
EOF
```

---

### Option 4: **termux-tts-speak mit Parametern** ✅ (Quick Win!)
**Pro:**
- JETZT schon verfügbar!
- Kostenlos
- Einfach zu implementieren

**Contra:**
- Begrenzte Anpassung
- System TTS engine (Android default)
- Keine echte Custom Voice

**Implementation:**
```python
def speak_dynamic(text, mood="neutral"):
    """Dynamische Stimme je nach Stimmung"""

    pitch_map = {
        "relaxed": 0.85,   # Tiefer, entspannt
        "neutral": 1.0,     # Normal
        "energetic": 1.15,  # Höher, energisch
        "sarcastic": 0.9    # Leicht tiefer, trocken
    }

    rate_map = {
        "relaxed": 0.9,     # Langsamer
        "neutral": 1.0,     # Normal
        "energetic": 1.1,   # Schneller
        "sarcastic": 0.85   # Langsamer, bewusst
    }

    pitch = pitch_map.get(mood, 1.0)
    rate = rate_map.get(mood, 1.0)

    subprocess.run([
        "termux-tts-speak",
        "-p", str(pitch),
        "-r", str(rate),
        text
    ])
```

---

## Roadmap 🗺️

### Phase 1: **Quick Wins** (JETZT machbar!) ⚡
- [ ] termux-tts-speak mit Pitch/Rate Parametern
- [ ] Dynamische Anpassung je nach Stimmung
- [ ] Testen & Optimieren
- [ ] **Aufwand:** 1-2h

### Phase 2: **Piper TTS Integration** (Medium) 🔧
- [ ] Piper TTS installieren
- [ ] Beste deutsche Stimme auswählen
- [ ] Integration in voice.py
- [ ] A/B Test mit termux-tts
- [ ] **Aufwand:** 3-5h

### Phase 3: **Voice Sample Collection** (Vorbereitung) 🎙️
- [ ] Voice Samples sammeln (~1-2h Audio)
  - Verschiedene Texte lesen
  - Verschiedene Emotionen
  - Klare Aufnahmen (ohne Hintergrund)
- [ ] Samples aufbereiten (Noise Reduction, etc.)
- [ ] **Aufwand:** 5-10h

### Phase 4: **Custom Voice Training** (Big Project!) 🚀
- [ ] Entscheidung: ElevenLabs vs. Piper Custom
- [ ] Voice Training durchführen
- [ ] Testing & Iteration
- [ ] Integration in M.O.L.O.C.H.
- [ ] **Aufwand:** 10-20h + Computing

---

## Requirements 📋

### Für Quick Wins (Phase 1):
- ✅ termux-api (schon installiert)
- ✅ Python code changes
- ✅ Testing

### Für Piper TTS (Phase 2):
- Piper TTS Package
- ~500 MB Modell Download
- Termux Storage

### Für Custom Voice (Phase 4):
- Voice Samples (1-2h sauberes Audio)
- GPU für Training (oder Cloud Service)
- $5-10 Budget für ElevenLabs (Option 1)
- ODER: ML Know-how für Piper Training (Option 2)

---

## Entscheidungsmatrix 🎯

| Ansatz | Qualität | Kosten | Aufwand | Customization | Empfehlung |
|--------|----------|--------|---------|---------------|------------|
| termux-tts + Params | ⭐⭐⭐ | FREE | Low | ⭐⭐ | ✅ **Start hier!** |
| Piper TTS | ⭐⭐⭐⭐ | FREE | Medium | ⭐⭐⭐ | 🔶 **Phase 2** |
| ElevenLabs | ⭐⭐⭐⭐⭐ | €€€ | Medium | ⭐⭐⭐⭐⭐ | 💰 **Wenn Budget** |
| Piper Custom | ⭐⭐⭐⭐ | FREE | High | ⭐⭐⭐⭐⭐ | 🚀 **Langfrist** |

---

## Next Steps 🎬

1. **JETZT:** Phase 1 implementieren (termux-tts dynamic)
2. **Später:** Piper TTS testen (Phase 2)
3. **Future:** Custom Voice Training (Phase 3+4)

---

## Notes 📝

- Voice Samples für Custom Training müssen von der "Zielstimme" sein
- Fränkischer Akzent: Schwierig zu trainieren ohne spezifische Samples
- Alternative: Akzent via Text ("Gude" statt "Guten Tag", etc.)
- Emotionale Variation: Kann durch Pitch/Rate simuliert werden

---

**Erstellt:** 2026-01-06
**Autor:** Claude Sonnet 4.5
**Für:** M.O.L.O.C.H. 3.0 Enhancement
