#!/usr/bin/env python3
"""
M.O.L.O.C.H. 3.0 - Configuration
================================
API Keys und Einstellungen
"""

import os
from pathlib import Path

# ═══════════════════════════════════════════════════════════════════════════════
# API KEYS - SETZE DEINE KEYS HIER! 🔑
# ═══════════════════════════════════════════════════════════════════════════════

# ANTHROPIC API KEY (Claude) - NUR ANTHROPIC, KEIN OPENAI!
# Hol dir deinen Key von: https://console.anthropic.com/
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "DEIN_ANTHROPIC_KEY_HIER")

# ═══════════════════════════════════════════════════════════════════════════════
# MODEL SETTINGS
# ═══════════════════════════════════════════════════════════════════════════════

# Claude Model
CLAUDE_MODEL = "claude-sonnet-4-20250514"

# Max Tokens
MAX_TOKENS = 1024

# ═══════════════════════════════════════════════════════════════════════════════
# PATHS
# ═══════════════════════════════════════════════════════════════════════════════

# Base Directory - auto-detect from script location
_config_file = Path(__file__)
BASE_DIR = _config_file.parent.parent  # Go up two levels from core/config.py to base

# Data Directory
DATA_DIR = BASE_DIR / "data"

# Brain Directory
BRAIN_DIR = DATA_DIR / "brain"

# Image File (for Vision)
IMAGE_FILE = DATA_DIR / "auge.jpg"

# ═══════════════════════════════════════════════════════════════════════════════
# VOICE SETTINGS
# ═══════════════════════════════════════════════════════════════════════════════

# Voice Recording Duration (seconds)
VOICE_DURATION = 20

# Voice Engine (termux-tts, edge-tts, piper)
VOICE_ENGINE = "termux-tts"

# Default Voice
DEFAULT_VOICE = "de-DE"

# ═══════════════════════════════════════════════════════════════════════════════
# FEATURE FLAGS
# ═══════════════════════════════════════════════════════════════════════════════

# Enable Web Search
ENABLE_WEB_SEARCH = True

# Enable Self-Modification
ENABLE_SELF_MODIFY = True

# Enable Location Tracking
ENABLE_LOCATION = True

# ═══════════════════════════════════════════════════════════════════════════════
# API SAFEGUARDS
# ═══════════════════════════════════════════════════════════════════════════════

# Max Claude Calls per Hour
MAX_CLAUDE_CALLS_PER_HOUR = 60

# Max Vision Calls per Hour
MAX_VISION_CALLS_PER_HOUR = 20

# Daily Budget (USD)
DAILY_BUDGET = 10.0

# ═══════════════════════════════════════════════════════════════════════════════
# VALIDATE CONFIG
# ═══════════════════════════════════════════════════════════════════════════════

def validate_config():
    """Validate configuration on import"""
    errors = []

    if ANTHROPIC_API_KEY == "DEIN_ANTHROPIC_KEY_HIER":
        errors.append("⚠️  ANTHROPIC_API_KEY nicht gesetzt!")

    if not ANTHROPIC_API_KEY or len(ANTHROPIC_API_KEY) < 20:
        errors.append("❌ ANTHROPIC_API_KEY ungültig!")

    if errors:
        print("\n🔑 CONFIG FEHLER:\n")
        for error in errors:
            print(f"   {error}")
        print("\n📝 SETZE DEINE API KEYS IN: ~/moloch_3.0/core/config.py")
        print("   Oder als Environment Variable: export ANTHROPIC_API_KEY='sk-ant-...'")
        print()

    return len(errors) == 0

# Validate on import (optional - kann auskommentiert werden)
# validate_config()
