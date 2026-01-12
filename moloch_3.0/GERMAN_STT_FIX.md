# 🇩🇪 GERMAN STT FIX - WARUM NUR ENGLISCH?

## Problem

termux-speech-to-text versteht nur Englisch, obwohl Handy auf Deutsch eingestellt ist!

## Root Cause

**Google Voice Typing** hat SEPARATE Spracheinstellungen, die UNABHÄNGIG von der System-Sprache sind!

## 🔍 DIAGNOSE

Führe das Debug-Script aus:

```bash
cd ~/documentation/moloch_3.0
bash debug_stt_language.sh
```

Sprich wenn aufgefordert: **"Ich bin Markus und spreche Deutsch"**

### Ergebnis interpretieren:

**Fall 1: "german" oder "marcus" erkannt**
- ✅ STT funktioniert, aber erkennt Englisch
- ❌ Google Voice Typing ist auf ENGLISCH gestellt

**Fall 2: "deutsch" oder "markus" erkannt**
- ✅ STT funktioniert korrekt mit Deutsch
- Problem liegt woanders

**Fall 3: Fehler oder kein Text**
- ❌ termux-speech-to-text funktioniert nicht
- Mikrofon-Berechtigung oder Installation fehlt

---

## 🔧 FIX: Google Voice Typing auf Deutsch stellen

### Für Xiaomi/MIUI (Redmi Note 13 Pro+):

```
1. Einstellungen öffnen
2. Suchen nach: "Spracheingabe" oder "Google Voice"
3. ODER: Zusätzliche Einstellungen → Sprache & Eingabe
4. Tippe auf: Google Voice Typing
5. Sprachen → Deutsch (Deutschland) hinzufügen
6. WICHTIG: Englisch als Primärsprache entfernen!
7. Handy neu starten
```

### Für Stock Android:

```
1. Settings → System
2. Languages & input
3. Virtual keyboard
4. Google Voice Typing
5. Languages
6. Wähle: Deutsch (Deutschland)
7. Entferne: English (falls primär)
8. Restart phone
```

### Für Samsung:

```
1. Settings → General management
2. Language and input
3. On-screen keyboard
4. Google Voice Typing
5. Languages
6. Add: Deutsch (Deutschland)
7. Remove: English (primary)
8. Restart
```

---

## ⚠️ WICHTIGE HINWEISE

### 1. System-Sprache ≠ Voice Typing Sprache!

Diese sind GETRENNT:
- **System-Sprache:** Settings → System → Languages
- **Voice Typing Sprache:** Settings → Google Voice Typing → Languages ← HIER!

### 2. Mehrere Sprachen können Probleme machen

Wenn du Englisch UND Deutsch aktiv hast, kann es sein dass:
- termux-speech-to-text die ERSTE Sprache nimmt (meist Englisch)
- Es zwischen Sprachen wechselt (unvorhersehbar)

**Lösung:** NUR Deutsch (Deutschland) aktiviert lassen!

### 3. Nach Änderung: Handy neu starten!

Google Voice Typing cached die Sprache. Ohne Neustart bleibt es bei Englisch!

---

## 🧪 TEST NACH FIX

1. **Debug-Script nochmal:**
   ```bash
   bash debug_stt_language.sh
   ```
   Sprich: "Ich bin Markus und spreche Deutsch"

2. **M.O.L.O.C.H. Voice Test:**
   ```bash
   python moloch3_unified.py
   ```
   Sprich: "Hey Moloch, kannst du mich verstehen?"

3. **Erwartetes Ergebnis:**
   ```
   📝 Du: hey moloch kannst du mich verstehen
   ```
   Oder ähnlich (in Deutsch!)

---

## 🔍 FALLS ES IMMER NOCH NICHT FUNKTIONIERT

### Check 1: Google App Sprache

Manchmal hat die **Google App** selbst eine falsche Sprache:

```
1. Öffne Google App
2. Profile icon → Settings
3. Language & region
4. Search language → Deutsch
5. Restart phone
```

### Check 2: Termux:API Neuinstallation

```bash
# Termux:API komplett neu installieren
pkg uninstall termux-api
pkg install termux-api

# Termux:API App neu installieren (F-Droid)
# Dann: Alle Berechtigungen erlauben
```

### Check 3: Alternative Test

Teste termux-speech-to-text direkt:

```bash
# Einfacher Test
termux-speech-to-text

# Sprich: "Das ist ein Test"
```

Wenn das funktioniert (Deutsch erkannt), ist M.O.L.O.C.H. Code korrekt!

---

## 💡 WARUM PASSIERT DAS?

Google Voice Typing ist ein **separater Service** der:
1. Eigene Spracheinstellungen hat
2. NICHT automatisch der System-Sprache folgt
3. Oft auf Englisch default installiert ist
4. Erst manuell auf Deutsch umgestellt werden muss

**termux-speech-to-text** kann diese Sprache **NICHT ändern** - es nutzt nur was Google Voice Typing vorgibt!

---

## 📊 BEKANNTE PROBLEME

### Problem 1: Englisch kehrt zurück

**Ursache:** Google App Update resettet Sprache
**Fix:** Nach jedem großen Google App Update Sprache neu prüfen

### Problem 2: Wechselt zwischen Sprachen

**Ursache:** Mehrere Sprachen aktiv, Google wählt automatisch
**Fix:** NUR Deutsch aktiviert lassen

### Problem 3: "Offline-Modus" nutzt falsche Sprache

**Ursache:** Offline-Sprachpakete nicht installiert
**Fix:** Google Voice Typing → Languages → Download "Deutsch (offline)"

---

## 🎯 ZUSAMMENFASSUNG

1. **System-Sprache ≠ Google Voice Typing Sprache**
2. **Google Voice Typing muss SEPARAT auf Deutsch gestellt werden**
3. **NUR Deutsch aktivieren, Englisch entfernen**
4. **Handy neu starten nach Änderung**
5. **Test mit `debug_stt_language.sh`**

**M.O.L.O.C.H. Code ist korrekt! Das Problem ist Android's separate Sprach-Konfiguration!**

---

**Last Updated:** 2026-01-12
**For:** M.O.L.O.C.H. 3.0 German STT Support
