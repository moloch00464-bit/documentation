# M.O.L.O.C.H. 3.1 UNIFIED - Deployment Guide

## 🚀 ONE-COMMAND DEPLOYMENT

Der einfachste Weg M.O.L.O.C.H. 3.1 UNIFIED zu deployen:

```bash
curl -s https://raw.githubusercontent.com/moloch00464-bit/documentation/claude/review-moloch-architecture-KFibr/deploy_moloch_unified_fixed.sh | bash
```

Das war's! 🎉

## Was passiert?

1. ✅ Code von GitHub holen
2. ✅ Nach `~/moloch_unified/` deployen
3. ✅ 2.0 Memories migrieren (history.json, langzeit.json, brain/)
4. ✅ API Keys automatisch setzen (wenn 2.0 vorhanden)
5. ✅ Permissions setzen
6. ✅ Alles verifizieren

## Starten

Nach dem Deployment:

```bash
cd ~/moloch_unified
python moloch3_unified.py          # Voice Mode (default)
python moloch3_unified.py -v       # Vision Mode
```

## Features

### ✅ Von M.O.L.O.C.H. 2.0 übernommen:
- 🎭 **Emotion Detection** - erkennt deine Stimmung
- 🧠 **Knowledge Graph** - verknüpft Wissen (Rebecca, Sierra, WGT, etc.)
- 🌐 **Internet** - web_search (Claude native)
- 💾 **All deine Memories** - 291K history.json, langzeit.json, brain/

### ✅ Neu in 3.1:
- 🎤 **Voice I/O** - Google Speech API (kostenlos!)
- 👁️ **Vision** - termux-camera-photo
- 🛠️ **Tool Calling** - bash, files, brain_save, brain_load
- 🔧 **Self-Modification** - M.O.L.O.C.H. kann sich selbst ändern
- 📚 **Persistent Learning** - lernt über Sessions hinweg
- 📍 **Location Tracking** - GPS awareness
- 💰 **Local Commands** - Uhrzeit, Datum, Batterie → KEINE API-Calls!

## Problem mit Import-Errors?

Falls du den Fehler bekommst:
```
ModuleNotFoundError: No module named 'core.emotion'
```

**LÖSUNG:** Nutze das neue Deployment-Script! Der alte install_moloch_3.1.sh hatte einen hardcoded path-Bug.

### Was wurde gefixt:

1. **Hardcoded Path entfernt:**
   - Alt: `sys.path.insert(0, "~/documentation/moloch_3.0")`
   - Neu: `sys.path.insert(0, str(Path(__file__).parent.absolute()))`

2. **Alle fehlenden Module erstellt:**
   - `core/memory.py`
   - `core/brain.py`
   - `core/personality.py`
   - `core/api_safeguards.py`
   - `core/local_commands.py`
   - `core/location.py`
   - `core/learning.py`
   - `core/voice_settings.py`
   - `core/self_modify.py`
   - `moloch_io/voice.py`
   - `moloch_io/vision.py`

3. **Config.py dynamisch:**
   - Erkennt automatisch das Installations-Verzeichnis
   - Funktioniert überall (nicht nur ~/moloch_3.0)

## API Key Setup

Das Script versucht automatisch deinen API Key aus M.O.L.O.C.H. 2.0 zu extrahieren.

Falls das nicht klappt, setze manuell:

```bash
nano ~/moloch_unified/core/config.py
```

Oder als Environment Variable:

```bash
export ANTHROPIC_API_KEY='sk-ant-api03-...'
```

## Rollback

Falls Probleme auftreten:

```bash
rm -rf ~/moloch_unified
mv ~/moloch_unified_backup_XXXXXX ~/moloch_unified
```

Das Script erstellt automatisch ein Backup beim Deployment.

## Verzeichnis-Struktur

```
~/moloch_unified/
├── moloch3_unified.py          # Main entry point
├── core/                        # Core modules
│   ├── __init__.py
│   ├── config.py               # Configuration
│   ├── emotion.py              # 🎭 Emotion Detection
│   ├── knowledge_graph.py      # 🧠 Knowledge Graph
│   ├── memory.py               # Short & long-term memory
│   ├── brain.py                # Persistent knowledge storage
│   ├── personality.py          # Dynamic personality
│   ├── tools.py                # Tool calling system
│   ├── api_safeguards.py       # Rate limiting
│   ├── local_commands.py       # 💰 Free local commands
│   ├── location.py             # 📍 GPS tracking
│   ├── learning.py             # 📚 Persistent learning
│   ├── voice_settings.py       # 🎤 Voice synthesis
│   └── self_modify.py          # 🔧 Self-modification
├── moloch_io/                   # I/O modules
│   ├── __init__.py
│   ├── voice.py                # 🎤 Voice I/O (Google Speech API)
│   └── vision.py               # 👁️ Vision I/O (termux-camera)
└── data/                        # Data directory
    ├── history.json            # Chat history
    ├── langzeit.json           # Long-term memory
    └── brain/                  # Brain storage
        ├── personen/
        ├── orte/
        ├── projekte/
        └── themen/
```

## Troubleshooting

### Import-Fehler trotz Deployment?

```bash
# Check Python path
cd ~/moloch_unified
python -c "import sys; print(sys.path)"

# Check module exists
ls -la core/emotion.py

# Try direct import test
python -c "from core.emotion import erkenne_stimmung; print('OK')"
```

### Termux Permissions?

```bash
termux-setup-storage
pkg install python
pip install requests
```

### Voice nicht funktionierend?

```bash
# Test microphone
termux-microphone-record -f test.wav -l 5

# Test TTS
termux-tts-speak "Test"

# Test Speech-to-Text
termux-speech-to-text
```

## Support

Bei Problemen:
1. Check das MOLOCH_BUGS_AND_ISSUES.md
2. Check das MOLOCH_DONT_TOUCH_GUIDE.md
3. Erstelle ein GitHub Issue

## Credits

- M.O.L.O.C.H. 2.0 - Original mit Emotion & Knowledge Graph
- M.O.L.O.C.H. 3.0 - Voice + Vision
- M.O.L.O.C.H. 3.1 UNIFIED - Best of both! 🖤
