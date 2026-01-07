#!/usr/bin/env python3
"""
Voice Input für M.O.L.O.C.H.
Sprachsteuerung mit Auto-Stop: Record → Whisper → Claude → TTS

Usage:
  python voice_input.py          # Starte Voice-Recording
  python voice_input.py -v       # Verbose (zeige alle Zwischenschritte)

Flow:
  1. Drücke Button / Starte Script
  2. Spreche (max 45s)
  3. Nach Pause (1-2s) stoppt Recording automatisch
  4. Whisper transkribiert
  5. Claude antwortet
  6. TTS spricht Antwort
"""

import sys
import os

# Importiere moloch Module
sys.path.insert(0, os.path.dirname(__file__))
from moloch import (
    record_audio, whisper_transcribe, ask_claude, speak,
    get_tageszeit, load_history, load_memory, save_history,
    auto_brain_save_genesis, extract_memory, save_memory
)
from datetime import datetime

def voice_input_flow(verbose=False):
    """Komplette Voice-Input Flow."""
    tageszeit = get_tageszeit()
    history = load_history()
    memory = load_memory()
    
    # 1. Recording
    if verbose:
        print("📢 Starte Voice-Recording...")
    ok = record_audio()
    if not ok:
        speak("Hab nix verstanden, Alter.")
        return False
    
    # 2. Whisper Transkription
    if verbose:
        print("🧠 Transkribiere mit Whisper...")
    user_input = whisper_transcribe()
    if not user_input:
        speak("Hab nix verstanden, Alter.")
        return False
    
    if verbose:
        print(f"✅ Text: {user_input}")
    
    # 3. Claude fragen
    if verbose:
        print("💭 Claude denkt...")
    response, _ = ask_claude(user_input, tageszeit, history, memory, image_path=None, use_web_search=False)
    
    if verbose:
        print(f"✅ Antwort: {response}")
    
    # 4. TTS
    if verbose:
        print("🔊 Spreche...")
    speak(response)
    
    # 5. Brain-Save & Memory
    auto_brain_save_genesis(user_input, response)
    if extract_memory(user_input, response, memory):
        if verbose:
            print("💾 Memory aktualisiert")
    save_memory(memory)
    
    # 6. History speichern
    history.append({
        "zeit": datetime.now().strftime("%d.%m %H:%M"),
        "user": user_input,
        "moloch": response
    })
    save_history(history)
    
    if verbose:
        print("✅ Fertig!")
    return True

if __name__ == '__main__':
    verbose = "-v" in sys.argv or "--verbose" in sys.argv
    
    try:
        voice_input_flow(verbose=verbose)
    except KeyboardInterrupt:
        print("\n⚠️ Abgebrochen")
    except Exception as e:
        print(f"❌ Fehler: {e}")
        speak("Mist, was ist da schiefgelaufen?")
