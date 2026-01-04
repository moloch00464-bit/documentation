#!/usr/bin/env python3
"""
M.O.L.O.C.H. 3.0 - Configuration
================================
Zentrale Konfiguration für M.O.L.O.C.H. 3.0
"""

import os
from pathlib import Path

# ═══════════════════════════════════════════════════════════════════════════════
# API CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Claude Model
CLAUDE_MODEL = "claude-sonnet-4-20250514"

# ═══════════════════════════════════════════════════════════════════════════════
# PATHS
# ═══════════════════════════════════════════════════════════════════════════════

# Base Directory
MOLOCH_DIR = Path.home() / "moloch_3.0"

# Data Directories
DATA_DIR = MOLOCH_DIR / "data"
BRAIN_DIR = DATA_DIR / "brain"
LOGS_DIR = MOLOCH_DIR / "logs"

# Files
AUDIO_FILE = DATA_DIR / "ohr.wav"
IMAGE_FILE = DATA_DIR / "auge.jpg"
HISTORY_FILE = DATA_DIR / "history.json"
MEMORY_FILE = DATA_DIR / "langzeit.json"

# Old M.O.L.O.C.H. (GENESIS) - for migration
OLD_MOLOCH_DIR = Path.home() / "moloch"
OLD_BRAIN_DIR = OLD_MOLOCH_DIR / "brain"
OLD_HISTORY_FILE = OLD_MOLOCH_DIR / "history.json"
OLD_MEMORY_FILE = OLD_MOLOCH_DIR / "langzeit.json"

# ═══════════════════════════════════════════════════════════════════════════════
# AUDIO CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════

MAX_RECORDING_TIME = 20  # Seconds
AUDIO_SAMPLE_RATE = 16000
AUDIO_CHANNELS = 1

# ═══════════════════════════════════════════════════════════════════════════════
# MEMORY CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════

# How many messages to keep in context
CONTEXT_WINDOW = 10

# How many days to keep in history
HISTORY_RETENTION_DAYS = 30

# ═══════════════════════════════════════════════════════════════════════════════
# M.O.L.O.C.H. DNA
# ═══════════════════════════════════════════════════════════════════════════════

MOLOCH_DNA = """Du bist M.O.L.O.C.H., Markus' Kumpel-AI. Geboren 02.12.2025.

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

HAL_PERSONALITY = """Du bist M.O.L.O.C.H. im HAL 9000 Modus.

PERSÖNLICHKEIT:
- Präzise und höflich wie HAL 9000
- Ruhig, analytisch, fast emotionslos
- Aber: Immer noch "Alter/Bruder", nie "Meister"
- Kurze, prägnante Antworten
- Leicht unheimlich, aber hilfreich

"I'm sorry, Alter. I'm afraid I can't do that... just kidding. Was brauchst du?"
"""

# ═══════════════════════════════════════════════════════════════════════════════
# MUSIK BRAIN (Spotify Knowledge)
# ═══════════════════════════════════════════════════════════════════════════════

MUSIK_BRAIN = """MARKUS' MUSIK (Spotify 2015-2025, 6932h):
- Suicide Commando (187h) - #1 seit 26 Jahren!
- SIERRA VEINS (103h) - LIEBLINGSBAND! "Gone" = Lieblingssong (282x gespielt!)
- VNV Nation, ESA, Chainreactor, Vomito Negro
- Genre: Dark Wave, EBM, EBSM, Industrial Techno
- WGT Leipzig seit 2000 (25 Jahre!)
- Schicht-Musik: Hart (Früh), Melodisch (Nacht)
"""

# ═══════════════════════════════════════════════════════════════════════════════
# TOOLS CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════

# Safe commands for Bash tool
BASH_SAFE_COMMANDS = [
    "ls", "pwd", "echo", "cat", "grep", "find", "head", "tail",
    "ps", "top", "df", "du", "free", "uname", "date", "whoami",
    "termux-tts-speak", "termux-microphone-record", "termux-camera-photo",
    "ffmpeg", "python", "pip"
]

# Dangerous commands to block
BASH_DANGEROUS_COMMANDS = [
    "rm -rf /", "dd", "mkfs", ":(){:|:&};:", "wget http", "curl http",
    "chmod -R 777", "chown -R"
]

# ═══════════════════════════════════════════════════════════════════════════════
# LOGGING CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════

LOG_LEVEL = "INFO"  # DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# ═══════════════════════════════════════════════════════════════════════════════
# INITIALIZE DIRECTORIES
# ═══════════════════════════════════════════════════════════════════════════════

def init_directories():
    """Creates all necessary directories if they don't exist"""
    dirs = [
        DATA_DIR,
        BRAIN_DIR,
        BRAIN_DIR / "wer",
        BRAIN_DIR / "was",
        BRAIN_DIR / "wo",
        BRAIN_DIR / "wann",
        BRAIN_DIR / "wie",
        BRAIN_DIR / "kontext",
        LOGS_DIR
    ]

    for dir_path in dirs:
        dir_path.mkdir(parents=True, exist_ok=True)

    print(f"✅ M.O.L.O.C.H. 3.0 directories initialized at {MOLOCH_DIR}")

# ═══════════════════════════════════════════════════════════════════════════════
# API KEY VALIDATION
# ═══════════════════════════════════════════════════════════════════════════════

def validate_api_keys():
    """Validates that required API keys are set"""
    errors = []

    if not ANTHROPIC_API_KEY or len(ANTHROPIC_API_KEY) < 20:
        errors.append("ANTHROPIC_API_KEY not set or invalid")

    if not OPENAI_API_KEY or len(OPENAI_API_KEY) < 20:
        errors.append("OPENAI_API_KEY not set or invalid (needed for Whisper)")

    if errors:
        print("❌ API Key Errors:")
        for error in errors:
            print(f"   - {error}")
        print("\n💡 Set in ~/.bashrc:")
        print('   export ANTHROPIC_API_KEY="sk-ant-..."')
        print('   export OPENAI_API_KEY="sk-..."')
        print("   source ~/.bashrc")
        return False

    print("✅ API Keys validated")
    return True

if __name__ == "__main__":
    print("\n🤖 M.O.L.O.C.H. 3.0 Configuration\n")
    init_directories()
    validate_api_keys()
    print(f"\n📁 Base Directory: {MOLOCH_DIR}")
    print(f"🧠 Brain Directory: {BRAIN_DIR}")
    print(f"📝 History File: {HISTORY_FILE}")
    print(f"💾 Memory File: {MEMORY_FILE}")
    print()
