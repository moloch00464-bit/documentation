# M.O.L.O.C.H. 2.0 → 3.0 Cleanup Guide 🔥

## Warum Cleanup?

**M.O.L.O.C.H. 3.0 ist 2.0 - aber besser!** 🚀

Die alte 2.0 Version ist jetzt obsolet. Alle Features sind in 3.0 integriert und verbessert:
- ✅ Persistent Learning (Cross-Session Intelligence)
- ✅ Emotion Synthesis (Voice mit Persönlichkeit)
- ✅ Vision Mode
- ✅ Alle alten Features + mehr!

## Problem: Zombie Widgets 👻

Alte 2.0 Widgets erscheinen immer noch in Termux:Widget, obwohl sie gelöscht wurden. Grund: **Widget Cache**!

## Lösung: Kompletter Cleanup

### Schritt 1: Cleanup Script ausführen

```bash
cd ~/documentation/moloch_3.0
python3 cleanup_moloch_2.py
```

Das Script:
- 🔍 Findet ALLE alten 2.0 Files (Widgets, Directories, etc.)
- 📋 Zeigt dir was gelöscht wird
- ⚠️  Fragt nach Bestätigung
- 🔥 Löscht alles (außer 3.0!)

### Schritt 2: Termux:Widget Cache leeren

Nach dem Script:

1. **Android Settings** öffnen
2. **Apps** → **Termux:Widget**
3. **Storage** → **Clear Data**
4. **Termux:Widget** neu öffnen

### Schritt 3: Neue 3.0 Widgets hinzufügen

Die neuen Widgets sind in `~/.shortcuts/`:
- `moloch-start` - Quick-Start M.O.L.O.C.H. 3.0
- `moloch-voice-test` - Test current voice
- `moloch-voice-select` - Voice Selection System
- `moloch-vision` - Quick Vision Mode
- `moloch-learnings` - Show Persistent Learnings

In Termux:Widget sollten **nur** diese 5 neuen Widgets erscheinen! ✅

## Was wird gelöscht?

Das Script löscht:
- ❌ Alte Widget Scripts (die nicht auf `moloch_3.0` zeigen)
- ❌ Alte `~/moloch/` Directories (falls vorhanden)
- ❌ Alle anderen alten 2.0 Files

**WICHTIG:** `~/documentation/moloch_3.0/` bleibt natürlich! 😎

## Sicherheit

- Das Script zeigt **vor dem Löschen** was entfernt wird
- Du musst **"yes"** eingeben zur Bestätigung
- Du kannst mit **"no"** abbrechen

## Nach dem Cleanup

✅ Nur M.O.L.O.C.H. 3.0 läuft
✅ Keine Zombie Widgets mehr
✅ Sauberes System
✅ Alle Features funktionieren! 🚀

## Fragen?

Wenn du unsicher bist, laufe das Script erstmal **ohne Bestätigung**:
```bash
python3 cleanup_moloch_2.py
# Schau dir die Liste an
# Gib "no" ein wenn du abbrechen willst
```

Das Script zeigt dir **genau** was gelöscht würde!

---

**3.0 ist 2.0 - aber besser! Let's grill 2.0! 🔥🖤**
