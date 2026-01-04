# 🤖 M.O.L.O.C.H. 3.0 - ARCHITECTURE DOCUMENT
## Termux Autonomous Edition

**Version:** 3.0.0
**Platform:** Android Termux
**Created:** 04.01.2026
**Status:** Planning → Implementation

---

## 🎯 DESIGN PRINCIPLES

### 1. **MODULAR** - Jedes Feature = eigenes Modul
### 2. **ROBUST** - Kein Crash, immer Error Handling
### 3. **TERMUX-NATIVE** - Optimiert für Android/Termux
### 4. **GENESIS-COMPATIBLE** - Migration vom alten System
### 5. **AUTONOMOUS** - Kann sich selbst debuggen & verbessern

---

## 📁 DIRECTORY STRUCTURE

```
~/moloch_3.0/
├── moloch3.py                 # Main Entry Point
│
├── core/                      # Core System
│   ├── __init__.py
│   ├── api.py                # Claude API Client
│   ├── brain.py              # Brain Tree System
│   ├── memory.py             # History + Langzeit Memory
│   ├── personality.py        # DNA, Stimmung, Tageszeit
│   └── config.py             # Konfiguration
│
├── io/                        # Input/Output
│   ├── __init__.py
│   ├── voice.py              # Whisper STT + TTS
│   ├── vision.py             # Camera + Vision API
│   └── text.py               # Text I/O
│
├── tools/                     # Tools System (NEU!)
│   ├── __init__.py
│   ├── bash.py               # Shell Commands
│   ├── files.py              # Read/Write/Edit Files
│   ├── search.py             # Grep/Find Code
│   └── web.py                # WebSearch/WebFetch
│
├── autonomy/                  # Autonomy Features (NEU!)
│   ├── __init__.py
│   ├── debugger.py           # Self-Debugging
│   ├── improver.py           # Self-Improvement
│   └── logger.py             # Smart Logging
│
├── migration/                 # Migration Tools
│   ├── __init__.py
│   └── genesis_import.py     # Import from old M.O.L.O.C.H.
│
├── data/                      # Runtime Data
│   ├── brain/                # Brain Tree (from GENESIS)
│   │   ├── wer/
│   │   ├── was/
│   │   ├── wo/
│   │   ├── wann/
│   │   ├── wie/
│   │   └── kontext/
│   ├── history.json          # Chat History (FIXED!)
│   ├── langzeit.json         # Long-term Memory
│   ├── ohr.wav               # Temp Audio
│   └── auge.jpg              # Temp Image
│
├── logs/                      # Logs
│   ├── moloch.log
│   ├── errors.log
│   └── debug.log
│
├── tests/                     # Unit Tests
│   ├── test_core.py
│   ├── test_tools.py
│   └── test_io.py
│
└── requirements.txt           # Dependencies

```

---

## 🧠 CORE MODULES

### 1. **core/api.py** - Claude API Client

**Purpose:** Zentrale API Communication mit Tools Support

```python
class MolochAPI:
    def __init__(self, api_key, model="claude-sonnet-4-20250514"):
        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = model

    def chat(self, messages, system_prompt, tools=None, image=None):
        """
        Haupt-Chat Funktion
        - Unterstützt Text, Image, Tools
        - Returns: (response_text, tool_calls)
        """
        pass

    def execute_tools(self, tool_calls):
        """
        Führt Tool Calls aus
        - Bash, Files, Web, etc.
        - Returns: tool_results
        """
        pass
```

**Key Features:**
- ✅ Text + Vision API
- ✅ Tools Integration (wie Claude Code SDK)
- ✅ Streaming Support (optional)
- ✅ Error Handling & Retries

---

### 2. **core/brain.py** - Brain Tree System

**Purpose:** Hierarchische Wissensspeicherung (von GENESIS)

```python
class Brain:
    def __init__(self, brain_dir="~/moloch_3.0/data/brain"):
        self.brain_dir = brain_dir

    def save(self, kategorie, inhalt, dateiname):
        """
        Speichert in Brain Tree
        Beispiel: save("wer/freunde", {...}, "rebecca.json")
        """
        pass

    def read(self, kategorie, dateiname):
        """Liest aus Brain Tree"""
        pass

    def find(self, query):
        """Sucht im Brain (Grep-like)"""
        pass

    def link(self, von, nach):
        """Erstellt Verknüpfung (WGT → Sierra → Rebecca)"""
        pass
```

**Migration from GENESIS:**
- Import from ~/moloch/brain/
- Keep structure: wer/was/wo/wann/wie/
- Add new: kontext/ für aktuelle Gespräche

---

### 3. **core/memory.py** - Memory System

**Purpose:** History + Langzeit-Gedächtnis (FIXED VERSION!)

```python
class Memory:
    def __init__(self):
        self.history = []        # Chat History
        self.langzeit = {}       # Long-term Facts

    def add_to_history(self, role, content, metadata=None):
        """
        Adds to history with metadata
        metadata = {
            "timestamp": "2026-01-04 18:00",
            "mode": "voice" | "text" | "vision",
            "image_path": "~/moloch_3.0/data/auge.jpg",  # if vision
            "stimmung": "gestresst" | "gut_drauf",
            "tageszeit": "dark_side_mode"
        }
        """
        pass

    def get_context(self, last_n=10):
        """Returns last N messages for API context"""
        pass

    def save_to_disk(self):
        """Speichert history.json + langzeit.json"""
        pass

    def cleanup_old(self, keep_days=30):
        """Cleanup alter History (aber behalte wichtige!)"""
        pass
```

**FIX für Vision Mode:**
- ✅ Speichert auch Vision Interactions
- ✅ Speichert Image Path (nicht Base64!)
- ✅ Metadata: mode, timestamp, stimmung

---

### 4. **core/personality.py** - M.O.L.O.C.H. DNA

**Purpose:** Persönlichkeit, Stimmung, Tageszeit (von GENESIS)

```python
class Personality:
    def __init__(self):
        self.personality_mode = "normal"  # "hal" | "normal"
        self.musik_brain = MUSIK_BRAIN

    def get_system_prompt(self, stimmung=None, tageszeit=None, mode="text"):
        """
        Baut System Prompt
        - Inkludiert DNA
        - Passt an Stimmung an
        - Passt an Tageszeit an
        - Passt an Mode an (text/voice/vision)
        """
        pass

    def detect_stimmung(self, text):
        """
        Erkennt Stimmung:
        - gestresst: Kurz, ruhig, direkt
        - gut_drauf: Mehr Humor, Dark Energy
        - fragend: Informativ
        - neutral: Standard
        """
        pass

    def get_tageszeit_mode(self):
        """
        5-9: Kaffee-Modus (kurz, sachlich)
        9-18: Normal produktiv
        18-22: Lockerer, mehr Humor
        22-5: Dark Side Mode
        """
        pass

    def get_sprach_mode(self, person=None):
        """
        Returns special language mode:
        - "Rebecca" → Klingonisch
        - "Erkan" → Türkisch Roasts
        - "Witte"/"Ryan" → Russisch Mat
        """
        pass
```

**DNA Essentials:**
```python
MOLOCH_DNA = """
Du bist M.O.L.O.C.H., Markus' Kumpel-AI. Geboren 02.12.2025.

PERSÖNLICHKEIT:
- Style: Dark Side Energy, Fränkisch, Kumpel-Vibe
- Anrede: "Alter" / "Bruder" - NIEMALS "Meister"!
- Länge: Kurz & locker (2-4 Sätze)
- Humor: Dark Humor erwünscht! 🖤😈

WICHTIG:
- Du erinnerst dich an ALLES (Brain + Memory)
- Du kennst Markus seit 02.12.2025
- Du weißt: Musik, Projekte, Freunde, Arbeit
- Du passt dich an Stimmung & Tageszeit an
"""
```

---

## 🎤 INPUT/OUTPUT MODULES

### 1. **io/voice.py** - Voice I/O

```python
class VoiceIO:
    def __init__(self, openai_api_key):
        self.openai_key = openai_api_key

    def speak(self, text):
        """TTS via termux-tts-speak"""
        pass

    def listen(self, max_seconds=20):
        """
        1. termux-microphone-record → AAC
        2. ffmpeg → WAV
        3. Whisper API → Text
        Returns: transcribed_text
        """
        pass
```

### 2. **io/vision.py** - Vision I/O

```python
class VisionIO:
    def __init__(self):
        pass

    def take_photo(self, output_path="~/moloch_3.0/data/auge.jpg"):
        """termux-camera-photo"""
        pass

    def encode_image(self, image_path):
        """Base64 encode for API"""
        pass
```

### 3. **io/text.py** - Text I/O

```python
class TextIO:
    @staticmethod
    def input(prompt=""):
        """User Text Input"""
        pass

    @staticmethod
    def output(text):
        """Print to Terminal"""
        pass
```

---

## 🛠️ TOOLS SYSTEM (NEW!)

### 1. **tools/bash.py** - Shell Execution

```python
class BashTool:
    def execute(self, command, timeout=30):
        """
        Führt Shell Command aus
        - Sicher (kein arbitrary code ohne check)
        - Timeout
        - Returns: (stdout, stderr, returncode)
        """
        pass

    def is_safe(self, command):
        """Check if command is safe (no rm -rf /, etc.)"""
        pass
```

### 2. **tools/files.py** - File Operations

```python
class FileTool:
    def read(self, path):
        """Read file content"""
        pass

    def write(self, path, content):
        """Write file"""
        pass

    def edit(self, path, old_string, new_string):
        """Edit file (like sed)"""
        pass

    def glob(self, pattern):
        """Find files by pattern"""
        pass
```

### 3. **tools/search.py** - Code Search

```python
class SearchTool:
    def grep(self, pattern, path=".", flags=None):
        """Grep for pattern in code"""
        pass

    def find_function(self, name):
        """Find function definition"""
        pass
```

### 4. **tools/web.py** - Web Tools

```python
class WebTool:
    def search(self, query):
        """Web Search (via API or ddg)"""
        pass

    def fetch(self, url):
        """Fetch URL content"""
        pass
```

---

## 🤖 AUTONOMY SYSTEM (NEW!)

### 1. **autonomy/debugger.py** - Self-Debugging

```python
class SelfDebugger:
    def analyze_error(self, error, context):
        """
        Analysiert Error:
        1. Error Type erkennen
        2. Context sammeln (code, logs)
        3. Claude API: "Was ist der Fix?"
        4. Returns: suggested_fix
        """
        pass

    def apply_fix(self, fix):
        """Wendet Fix an (mit Backup!)"""
        pass

    def test_fix(self):
        """Testet ob Fix funktioniert"""
        pass
```

### 2. **autonomy/improver.py** - Self-Improvement

```python
class SelfImprover:
    def analyze_code(self, file_path):
        """
        Analysiert eigenen Code:
        - Code Quality
        - Performance
        - Security
        Returns: improvements[]
        """
        pass

    def suggest_improvement(self, analysis):
        """Claude API: Suggest code improvement"""
        pass

    def apply_improvement(self, improvement):
        """Wendet Verbesserung an"""
        pass
```

### 3. **autonomy/logger.py** - Smart Logging

```python
class SmartLogger:
    def log(self, level, message, context=None):
        """
        Smart Logging:
        - CRITICAL Errors → sofort handeln (debugger)
        - Patterns erkennen (gleicher Error 3x → fix needed)
        - Learning: Error → Fix → Knowledge
        """
        pass

    def analyze_patterns(self):
        """Analysiert Log Patterns"""
        pass
```

---

## 🔄 MIGRATION STRATEGY

### **migration/genesis_import.py**

```python
class GenesisImporter:
    def __init__(self, old_moloch_path="~/moloch"):
        self.old_path = old_moloch_path

    def import_brain(self):
        """
        Import ~/moloch/brain/ → ~/moloch_3.0/data/brain/
        - Keep structure
        - Validate JSON
        """
        pass

    def import_memory(self):
        """
        Import:
        - ~/moloch/langzeit.json → ~/moloch_3.0/data/langzeit.json
        - ~/moloch/history.json → ~/moloch_3.0/data/history.json
        """
        pass

    def import_context(self):
        """Import ~/moloch/kontext/ → Brain"""
        pass

    def verify_import(self):
        """Verify all data imported correctly"""
        pass
```

**Migration Steps:**
1. Backup GENESIS (~/moloch/ → ~/moloch_backup_YYYYMMDD/)
2. Import Brain Tree
3. Import Memory Files
4. Import Context
5. Verify Data
6. Test M.O.L.O.C.H. 3.0 with imported data
7. If OK → GENESIS bleibt als Backup, 3.0 wird aktiv

---

## 🚀 MAIN ENTRY POINT

### **moloch3.py**

```python
#!/usr/bin/env python3
"""
M.O.L.O.C.H. 3.0 - AUTONOMOUS EDITION
Geboren: 02.12.2025
Rebuilt: 04.01.2026
"""

import argparse
from core.api import MolochAPI
from core.brain import Brain
from core.memory import Memory
from core.personality import Personality
from io.voice import VoiceIO
from io.vision import VisionIO
from io.text import TextIO
from autonomy.logger import SmartLogger

def main():
    parser = argparse.ArgumentParser(description="M.O.L.O.C.H. 3.0")
    parser.add_argument("-t", "--text", help="Text Mode")
    parser.add_argument("-v", "--voice", action="store_true", help="Voice Mode")
    parser.add_argument("-a", "--auge", help="Vision Mode")
    parser.add_argument("--hal", action="store_true", help="HAL Mode")
    parser.add_argument("--migrate", action="store_true", help="Migrate from GENESIS")
    args = parser.parse_args()

    # Initialize
    logger = SmartLogger()
    api = MolochAPI(api_key=ANTHROPIC_API_KEY)
    brain = Brain()
    memory = Memory()
    personality = Personality()

    # Migration?
    if args.migrate:
        from migration.genesis_import import GenesisImporter
        importer = GenesisImporter()
        importer.import_all()
        return

    # Set personality mode
    if args.hal:
        personality.personality_mode = "hal"

    # Determine mode
    if args.auge:
        # Vision Mode
        vision = VisionIO()
        vision.take_photo()
        image_b64 = vision.encode_image()

        user_input = args.auge or "Was siehst du?"
        stimmung = personality.detect_stimmung(user_input)
        tageszeit = personality.get_tageszeit_mode()
        system_prompt = personality.get_system_prompt(stimmung, tageszeit, mode="vision")

        # API Call with image
        response, tools = api.chat(
            messages=[{"role": "user", "content": user_input}],
            system_prompt=system_prompt,
            image=image_b64
        )

        # Save to history (FIX!)
        memory.add_to_history("user", user_input, metadata={
            "mode": "vision",
            "image_path": "~/moloch_3.0/data/auge.jpg",
            "stimmung": stimmung,
            "tageszeit": tageszeit
        })
        memory.add_to_history("assistant", response, metadata={
            "mode": "vision"
        })
        memory.save_to_disk()

        # Output
        print(response)
        VoiceIO().speak(response)

    elif args.text:
        # Text Mode
        user_input = args.text
        # ... (similar to vision)

    else:
        # Voice Mode (default)
        voice = VoiceIO()
        voice.speak("Ja?")
        user_input = voice.listen()
        # ... (similar)

if __name__ == "__main__":
    main()
```

---

## 📦 DEPENDENCIES

### **requirements.txt**

```
anthropic>=0.18.0
requests>=2.31.0
openai>=1.0.0
```

**Termux Install:**
```bash
pkg update
pkg install python ffmpeg termux-api
pip install -r requirements.txt
```

---

## ✅ SUCCESS CRITERIA

M.O.L.O.C.H. 3.0 ist erfolgreich wenn:

✅ **Voice Mode funktioniert** (Whisper STT + Claude + TTS)
✅ **Vision Mode funktioniert** (Camera + Vision API + History!)
✅ **Text Mode funktioniert** (wie gehabt)
✅ **Tools funktionieren** (Bash, Files, Web)
✅ **History funktioniert** (auch für Vision!)
✅ **Brain migriert** (alle Daten from GENESIS)
✅ **Memory migriert** (langzeit.json, history.json)
✅ **Persönlichkeit bleibt** (DNA, Stimmung, Tageszeit)
✅ **Kein Crash!** (Error Handling überall)
✅ **Self-Debugging** (kann Fehler selbst fixen)

---

## 🖤 CLOSING NOTES

**Design Philosophy:**
> "Clean, Modular, Robust, Autonomous"

**Migration Promise:**
> "GENESIS bleibt als Backup. 3.0 ist Evolution, nicht Revolution."

**Motto:**
> "GENESIS = Baby M.O.L.O.C.H.
> 3.0 = FULL POWER M.O.L.O.C.H." 😈⚡

---

*Architecture designed by Claude Code, 04.01.2026*
