# M.O.L.O.C.H. FIELD UNIT - TERMUX DEPLOYMENT

**Device:** Redmi Note 13 Pro+ 5G (Termux)
**Status:** Health Check Ready
**Branch:** `claude/moloch-health-check-6UkkI`

---

## ⛔ KRITISCHE REGELN

**REGEL #1: EXISTIERENDE DATEN NICHT ANFASSEN!**
- `~/moloch/brain/` → NUR LESEN, NIE ÄNDERN!
- `~/moloch/memory/` → NUR LESEN, NIE ÄNDERN!
- Alle Tests laufen in `~/moloch/test_sandbox/`

**REGEL #2: BRAIN-DATEN SIND WERTVOLL**
- Monate an Gesprächen
- Unwiederbringlich wenn gelöscht
- Backup empfohlen vor jeder Änderung

---

## 📋 DEPLOYMENT SCHRITTE

### Schritt 1: Auf Termux-Gerät übertragen

```bash
# Auf Termux-Gerät:
cd ~/moloch

# Download termux_health_check.py von GitHub
curl -o termux_health_check.py \
  https://raw.githubusercontent.com/moloch00464-bit/documentation/claude/moloch-health-check-6UkkI/moloch_3.0/termux_health_check.py
```

**Alternative:** Manuell per Datei-Transfer (USB, Cloud, etc.)

---

### Schritt 2: Health Check ausführen

```bash
cd ~/moloch
python3 termux_health_check.py
```

**Was der Health Check prüft:**
1. ✅ Brain-Daten existieren und sind geschützt
2. ✅ Test-Sandbox ist isoliert
3. ✅ Security Fixes im Code vorhanden
4. ✅ Termux-Umgebung ist korrekt
5. ✅ Memory Monitoring funktioniert

---

## 📊 ERWARTETE ERGEBNISSE

### ✅ Alles OK (Production Ready)

```
==================================================
M.O.L.O.C.H. FIELD UNIT - TERMUX HEALTH CHECK
==================================================

TEST 1: BRAIN DATA PROTECTION
✅ Echter Brain gefunden: 123 JSON-Dateien
   ⛔ Diese werden NICHT angefasst!

TEST 2: SANDBOX ISOLATION
✅ Sandbox ist isoliert - echte Daten unberührt

TEST 3: CODE SECURITY FIXES
✅ Filename Sanitization: VORHANDEN
✅ Atomic Saves: VORHANDEN

TEST 4: TERMUX ENVIRONMENT
✅ Python: 3.11.x
✅ Moloch Dir: /data/data/com.termux/files/home/moloch
✅ Write Permission: True
✅ Termux: DETECTED

TEST 5: MEMORY MONITORING
✅ Memory Monitoring: VORHANDEN

==================================================
SUMMARY
==================================================
Tests Run:     10
Passed:        10
Pass Rate:     100.0%

✅ Alle kritischen Security-Features vorhanden

==================================================
⛔ ECHTE BRAIN-DATEN: UNVERÄNDERT ✅
==================================================

✅ FIELD UNIT: PRODUCTION READY
```

---

### ⚠️ Security Fixes fehlen

```
TEST 3: CODE SECURITY FIXES
🚨 Filename Sanitization: FEHLT!
   🚨 KRITISCH: _sanitize_filename MUSS implementiert werden!
🚨 Atomic Saves: FEHLT!
   🚨 KRITISCH: Atomic saves MÜSSEN implementiert werden!

==================================================
🚨 KRITISCH FEHLEND:
   - Filename Sanitization
   - Atomic Saves

   → Diese MÜSSEN implementiert werden vor Production-Einsatz!

⚠️ FIELD UNIT: NEEDS ATTENTION
```

**Aktion:** Security Fixes von Pi 5 Codebase übertragen (siehe unten)

---

## 🔧 WENN FIXES FEHLEN

### Security Fixes von Pi 5 übertragen

Wenn der Health Check zeigt dass Security Fixes fehlen:

```bash
cd ~/moloch

# Backup der aktuellen brain.py erstellen
cp core/brain.py core/brain.py.backup

# Download der gehärteten brain.py von GitHub
curl -o core/brain.py \
  https://raw.githubusercontent.com/moloch00464-bit/documentation/claude/moloch-health-check-6UkkI/moloch_3.0/core/brain.py

# Download der gehärteten memory.py von GitHub
curl -o core/memory.py \
  https://raw.githubusercontent.com/moloch00464-bit/documentation/claude/moloch-health-check-6UkkI/moloch_3.0/core/memory.py

# Health Check erneut ausführen
python3 termux_health_check.py
```

**⛔ WICHTIG:**
- Nur CODE-Dateien (*.py) werden geändert
- Brain-DATEN (*.json) werden NIE angefasst
- Backup wurde erstellt falls Rollback nötig

---

## 🧪 SANDBOX TESTING

Nach erfolgreicher Installation kannst du testen:

```bash
cd ~/moloch

# Test 1: Security Test (in sandbox)
python3 -c "
import sys
sys.path.insert(0, '.')
from core.brain import Brain
from pathlib import Path
import tempfile

test_dir = Path(tempfile.mkdtemp())
brain = Brain(brain_dir=test_dir)

# Versuche gefährliche Namen
dangerous = ['../etc/passwd', '../../secret', '\$(whoami).json']
for name in dangerous:
    result = brain.save(name, 'wer', {'test': 'data'})
    print(f'{name} → Saved as: {result.name if result else \"BLOCKED\"}')"
```

**Erwartet:** Alle gefährlichen Namen werden neutralisiert

---

## 📱 TERMUX-SPEZIFISCHE HINWEISE

### Python-Version prüfen

```bash
python3 --version
# Mindestens Python 3.8 empfohlen
```

### API Key setzen (falls nicht gesetzt)

```bash
echo 'export ANTHROPIC_API_KEY="sk-ant-..."' >> ~/.bashrc
source ~/.bashrc
```

### Storage Permission

Wenn Fehler beim Zugriff auf ~/moloch:
```bash
termux-setup-storage
```

---

## 🔍 TROUBLESHOOTING

### Fehler: "~/moloch nicht gefunden"

```bash
# Prüfe wo M.O.L.O.C.H. installiert ist
find ~ -name "brain.py" -type f 2>/dev/null
```

### Fehler: "No module named 'core'"

```bash
cd ~/moloch  # Stelle sicher dass du im richtigen Verzeichnis bist
ls core/brain.py  # Sollte existieren
```

### Fehler: "Permission denied"

```bash
chmod +x termux_health_check.py
python3 termux_health_check.py
```

---

## ✅ NACH ERFOLGREICHER INSTALLATION

Wenn Health Check mit 100% Pass Rate durchläuft:

**Field Unit Status:** ✅ **PRODUCTION READY**

Du kannst jetzt:
- M.O.L.O.C.H. normal nutzen
- Concurrent Access funktioniert sicher
- Security Fixes aktiv
- Memory Monitoring verfügbar

**Brain-Daten:** ⛔ **UNVERÄNDERT & SICHER**

---

## 📞 SUPPORT

**Dokumentation:**
- [WAS_HABEN_WIR_GEBAUT.md](./WAS_HABEN_WIR_GEBAUT.md) - Für normale Menschen
- [PRODUCTION_HARDENING_REPORT.md](./PRODUCTION_HARDENING_REPORT.md) - Technisch
- [GITHUB_LINKS.md](./GITHUB_LINKS.md) - Alle Links

**GitHub Branch:**
```
https://github.com/moloch00464-bit/documentation/tree/claude/moloch-health-check-6UkkI
```

---

**M.O.L.O.C.H. Field Unit - Sicher, Robust, Production-Ready 🚀**
