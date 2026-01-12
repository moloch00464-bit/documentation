# M.O.L.O.C.H. 3.0 - Deutsche Spracheingabe einrichten

## 🎯 Problem

`termux-speech-to-text` versteht nur Englisch, obwohl dein Handy auf Deutsch eingestellt ist.

**Grund:** `termux-speech-to-text` nutzt Android's "Google Voice Typing" System, das eine **separate Sprach-Einstellung** hat (unabhängig von der System-Sprache)!

---

## ✅ Lösung: Android Voice Input auf Deutsch stellen

### **Schritt-für-Schritt Anleitung**

#### **Variante 1: Google Voice Typing Einstellungen (Standard)**

```
1. Öffne: Einstellungen (Settings)

2. Gehe zu: System

3. Wähle: Sprache & Eingabe (Language & Input)

4. Unter "Tastaturen":
   → Bildschirmtastatur (On-screen keyboard)

5. Wähle: Google Spracheingabe (Google Voice Typing)

6. Tippe auf: Sprachen (Languages)

7. ✅ Aktiviere: Deutsch (Deutschland) / German (Germany)

8. ⚠️ WICHTIG: Stelle sicher, dass Deutsch als PRIMÄRE Sprache markiert ist!
```

#### **Variante 2: Gboard Einstellungen (falls du Gboard nutzt)**

```
1. Öffne: Einstellungen (Settings)

2. Gehe zu: System → Sprache & Eingabe

3. Unter "Tastaturen":
   → Bildschirmtastatur
   → Gboard

4. Tippe auf: Sprachen (Languages)

5. Füge hinzu: Deutsch (Deutschland)

6. Stelle sicher: Deutsch ist als primäre Sprache gesetzt

7. Gehe zurück zu Gboard-Einstellungen

8. Tippe auf: Spracheingabe (Voice typing)

9. Aktiviere: "Spracheingabe über Tastatur verwenden"

10. Wähle: Sprachen → Deutsch
```

#### **Variante 3: Google App Einstellungen**

```
1. Öffne: Google App

2. Tippe auf: Profil-Icon (oben rechts)

3. Wähle: Einstellungen (Settings)

4. Gehe zu: Sprache & Region (Language & Region)

5. Tippe auf: Sprache (Language)

6. Wähle: Deutsch (Deutschland)

7. ✅ Bestätige die Änderung
```

---

## 🧪 Nach der Einstellung testen

### **Test 1: Termux Voice Test**

```bash
cd ~/documentation
termux-speech-to-text
```

**Sprich:** "Hallo M.O.L.O.C.H."

**Erwartetes Ergebnis:** Output sollte "Hallo M.O.L.O.C.H." oder "Hallo Moloch" sein (auf Deutsch!)

### **Test 2: M.O.L.O.C.H. Voice I/O**

```bash
cd ~/documentation/moloch_3.0
python moloch_io/voice.py
```

---

## 📱 Geräte-spezifische Hinweise

### **Xiaomi (MIUI/HyperOS)**

Xiaomi hat manchmal eigene Sprach-Einstellungen:

```
Einstellungen → Zusätzliche Einstellungen → Sprache & Eingabe
```

Oder:

```
Einstellungen → Sprache, Zeit & Tastatur → Google Spracheingabe
```

### **Samsung (One UI)**

```
Einstellungen → Allgemeine Verwaltung → Sprache und Eingabe → Bildschirmtastatur → Google Spracheingabe
```

### **Stock Android / Pixel**

```
Einstellungen → System → Sprachen & Eingabe → Virtuelle Tastatur → Google Spracheingabe → Sprachen
```

---

## ⚠️ Häufige Probleme

### **Problem 1: "Google Voice Typing" nicht gefunden**

**Lösung:** Installiere "Google App" aus dem Play Store:
```
Play Store → Suche "Google" → Installieren
```

### **Problem 2: Deutsch nicht in der Liste**

**Lösung:** Lade Deutsch-Sprachpaket herunter:
```
Google Voice Typing → Sprachen → Alle Sprachen
→ Suche "Deutsch" → Download-Icon tippen
```

### **Problem 3: Erkennt immer noch Englisch**

**Lösungen:**
1. Prüfe ob Deutsch als **Primärsprache** gesetzt ist (nicht nur hinzugefügt)
2. Entferne Englisch aus der Sprach-Liste (falls möglich)
3. Starte dein Handy neu
4. Teste ob Google Assistant auf Deutsch antwortet: "Hey Google, wie ist das Wetter?"

### **Problem 4: Offline-Erkennung funktioniert nicht**

**Lösung:** Lade Offline-Sprachpaket:
```
Google Voice Typing → Offline-Spracherkennung
→ Deutsch (Deutschland) herunterladen
```

---

## 🎤 Technische Details

### **Warum kein `-l de-DE` Parameter?**

`termux-speech-to-text` ist nur ein **Wrapper** für Android's natives Speech Recognition API. Es hat **keine eigenen Parameter** für Sprache!

**Vergleich:**
```bash
# TTS (Text-to-Speech) - HATt -l Parameter ✅
termux-tts-speak -l de-DE "Hallo"

# STT (Speech-to-Text) - HAT KEINEN -l Parameter ❌
termux-speech-to-text                    # Nutzt System-Einstellung
```

### **Welche Sprache wird verwendet?**

Android wählt die Sprache in dieser Reihenfolge:
1. **Google Voice Typing primäre Sprache** (höchste Priorität)
2. System-Sprache (Settings → Languages)
3. Google App Sprache
4. Fallback: Englisch (US)

---

## 📚 Quellen

- [Android system settings for speech recognition](https://speaking.email/FAQ/87/android-system-settings-for-speech-and-voice-recognition)
- [Change Google Assistant language](https://support.google.com/assistant/answer/7394513?hl=en&co=GENIE.Platform%3DAndroid)
- [Google Voice Typing Languages](https://support.google.com/googlenest/answer/7550584?hl=en&co=GENIE.Platform%3DAndroid)

---

## ✅ Erfolgskriterium

Nach der Einrichtung sollte M.O.L.O.C.H.:
- ✅ Deutsche Sprache verstehen
- ✅ Deutsch transkribieren
- ✅ Auf Deutsch sprechen (TTS)
- ✅ Keine API-Kosten verursachen

**Viel Erfolg!** 🚀
