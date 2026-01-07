#!/usr/bin/env python3
"""
M.O.L.O.C.H. Watch Interface
Kompakte UI für Smartwatch mit Pumuckl/HAL Modi

Usage:
  python watch_ui.py "was geht?"                    # Quick response (standard)
  python watch_ui.py -p pumuckl "hey kobold!"      # Pumuckl (frech)
  python watch_ui.py -p hal "hey moloch"            # HAL (Standard)
  python watch_ui.py --voice                        # Voice Input
  python watch_ui.py --voice -p pumuckl             # Voice Input (Pumuckl)
"""

import sys
import os

# Importiere moloch Module
sys.path.insert(0, os.path.dirname(__file__))
from moloch import (
    record_audio, whisper_transcribe, ask_claude, speak,
    get_tageszeit, load_history, load_memory, save_history,
    load_json, save_json, auto_brain_save_genesis, extract_memory, save_memory,
    AUDIO_FILE
)
from personalities import get_personality_prompt, format_response_for_watch, PERSONALITIES
from datetime import datetime

# Watch-spezifische Config
WATCH_CONFIG_FILE = os.path.expanduser("~/moloch/watch_personality.conf")

def load_watch_personality():
    """Lade aktuelle Watch-Persönlichkeit."""
    config = load_json(WATCH_CONFIG_FILE, {"personality": "hal"})
    return config.get("personality", "hal")

def save_watch_personality(personality):
    """Speichere Watch-Persönlichkeit."""
    os.makedirs(os.path.dirname(WATCH_CONFIG_FILE), exist_ok=True)
    save_json(WATCH_CONFIG_FILE, {"personality": personality})

def watch_response(text, personality="hal", use_voice=False, verbose=False):
    """Generiere Watch-Response mit kompakter UI."""
    tageszeit = get_tageszeit()
    history = load_history()
    memory = load_memory()
    
    # System Prompt mit Persönlichkeit
    history_txt = ""
    memory_txt = ""
    if history:
        recent = history[-3:]  # Nur letzte 3 für Watch
        history_txt = "\nLETZTE AUSTAUSCHE:\n"
        for h in recent:
            history_txt += f"[{h.get('zeit', '?')}] {h.get('user', '')[:40]}... → {h.get('moloch', '')[:40]}...\n"
    
    if memory:
        memory_txt = "MEMORY:"
        for key, items in memory.items():
            if items:
                memory_txt += f" [{key}: {', '.join(items[-3:])}]"
    
    system = get_personality_prompt(personality, tageszeit, memory_txt, history_txt)
    
    # Modifiziere System für Watch (noch kürzer)
    if personality == "pumuckl":
        system += "\n\n⚠️ WATCH MODE: Maximal 2 Sätze! Ultra kurz!"
    
    # Claude fragen mit angepasstem System
    try:
        response_full = ask_claude(text, tageszeit, history, memory, image_path=None, use_web_search=False)[0]
    except Exception as e:
        return f"❌ Fehler: {e}"
    
    # Formatiere für Watch
    response_watch = format_response_for_watch(response_full, personality)
    
    # Auto-Save
    auto_brain_save_genesis(text, response_full)
    if extract_memory(text, response_full, memory):
        pass
    save_memory(memory)
    
    history.append({
        "zeit": datetime.now().strftime("%H:%M"),
        "user": text[:50],
        "moloch": response_full[:80]
    })
    save_history(history)
    
    if verbose:
        print(f"[{personality.upper()}] {response_watch}")
        print(f"Full: {response_full}")
    else:
        print(response_watch)
    
    return response_watch

def watch_voice_input(personality="hal", verbose=False):
    """Voice Input für Watch (Record → Text → Response)."""
    print("🎤 Recording...")
    ok = record_audio()
    if not ok:
        print("👺 Nix gehört!")
        return
    
    print("🧠 Transkribiere...")
    text = whisper_transcribe()
    if not text:
        print("👺 Nix verstanden!")
        return
    
    if verbose:
        print(f"Text: {text}")
    
    watch_response(text, personality, use_voice=False, verbose=verbose)

if __name__ == '__main__':
    personality = load_watch_personality()
    use_voice = False
    verbose = False
    text = None
    
    # Parse Args
    i = 1
    while i < len(sys.argv):
        arg = sys.argv[i].lower()
        if arg in ["-p", "--personality"]:
            i += 1
            if i < len(sys.argv) and sys.argv[i] in PERSONALITIES:
                personality = sys.argv[i]
                save_watch_personality(personality)
        elif arg == "--voice":
            use_voice = True
        elif arg in ["-v", "--verbose"]:
            verbose = True
        elif not arg.startswith("-"):
            text = " ".join(sys.argv[i:])
            break
        i += 1
    
    try:
        if use_voice:
            watch_voice_input(personality, verbose)
        elif text:
            watch_response(text, personality, verbose=verbose)
        else:
            print(f"Usage: python watch_ui.py [-p hal|pumuckl] [--voice] [-v] <text>")
            print(f"Current: {personality}")
    except KeyboardInterrupt:
        print("\n⚠️ Abgebrochen")
    except Exception as e:
        print(f"❌ Fehler: {e}")
