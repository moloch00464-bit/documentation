#!/usr/bin/env python3
"""
M.O.L.O.C.H. 3.0 - Voice Debug Test
Captured ALLE Errors und loggt sie
"""

import sys
import subprocess
from pathlib import Path
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from moloch_io.voice import VoiceIO

LOG_FILE = Path.home() / "moloch_voice_python_debug.log"

def log(msg):
    """Log to both console and file"""
    print(msg)
    with open(LOG_FILE, "a") as f:
        f.write(msg + "\n")

def main():
    log("=" * 70)
    log("M.O.L.O.C.H. Voice Python Debug Test")
    log(f"Time: {datetime.now().isoformat()}")
    log("=" * 70)
    log("")

    # Test 1: Initialize VoiceIO
    log("━━━ TEST 1: Initialize VoiceIO ━━━")
    try:
        voice = VoiceIO()
        log("✅ VoiceIO initialized successfully")
    except Exception as e:
        log(f"❌ VoiceIO initialization failed: {e}")
        log(f"   Exception type: {type(e).__name__}")
        import traceback
        log(f"   Traceback:\n{traceback.format_exc()}")
        return
    log("")

    # Test 2: TTS (Text-to-Speech)
    log("━━━ TEST 2: TTS (speak) ━━━")
    log("Calling: voice.speak('Hallo Test', language='de-DE')")
    try:
        result = voice.speak("Hallo Test", language="de-DE")
        log(f"✅ TTS returned: {result}")
    except Exception as e:
        log(f"❌ TTS failed: {e}")
        log(f"   Exception type: {type(e).__name__}")
        import traceback
        log(f"   Traceback:\n{traceback.format_exc()}")
    log("")

    # Test 3: STT (Speech-to-Text)
    log("━━━ TEST 3: STT (listen) ━━━")
    log("Calling: voice.listen()")
    log("")
    log("🎤 USER: Sprich jetzt 'Hallo MOLOCH'")
    log("")

    try:
        text = voice.listen()

        log("")
        log(f"📝 Result: '{text}'")
        log(f"   Type: {type(text)}")
        log(f"   Length: {len(text) if text else 0}")

        if text:
            log("✅ STT returned text")

            # Analyze language
            if "hello" in text.lower():
                log("🇬🇧 WARNING: English detected!")
            elif "hallo" in text.lower():
                log("🇩🇪 SUCCESS: German detected!")
            else:
                log(f"❓ Unknown language pattern: {text}")
        else:
            log("⚠️  STT returned None/empty")

    except subprocess.TimeoutExpired as e:
        log(f"⏱️  TIMEOUT: {e}")
        log(f"   Command: {e.cmd}")
        log(f"   Timeout: {e.timeout}s")

    except FileNotFoundError as e:
        log(f"❌ FILE NOT FOUND: {e}")
        log("   Likely: termux-speech-to-text not installed")
        log("   Fix: pkg install termux-api")

    except subprocess.CalledProcessError as e:
        log(f"❌ COMMAND ERROR: {e}")
        log(f"   Return code: {e.returncode}")
        log(f"   Command: {e.cmd}")
        if e.stdout:
            log(f"   Stdout: {e.stdout}")
        if e.stderr:
            log(f"   Stderr: {e.stderr}")

    except Exception as e:
        log(f"❌ UNEXPECTED ERROR: {e}")
        log(f"   Exception type: {type(e).__name__}")
        import traceback
        log(f"   Traceback:\n{traceback.format_exc()}")

    log("")

    # Test 4: Direct termux-speech-to-text call
    log("━━━ TEST 4: Direct termux-speech-to-text test ━━━")
    log("Calling subprocess directly with full error capture")
    log("")

    try:
        log("🎤 USER: Sprich nochmal 'Hallo MOLOCH'")
        log("")

        result = subprocess.run(
            ["termux-speech-to-text"],
            capture_output=True,
            timeout=60,
            text=True
        )

        log(f"Return code: {result.returncode}")
        log(f"Stdout length: {len(result.stdout)} chars")
        log(f"Stderr length: {len(result.stderr)} chars")
        log("")

        if result.stdout:
            log("📝 STDOUT:")
            log(f"   {result.stdout}")
        else:
            log("   (empty)")

        if result.stderr:
            log("⚠️  STDERR:")
            log(f"   {result.stderr}")
        else:
            log("   (no errors)")

    except Exception as e:
        log(f"❌ Direct call failed: {e}")
        import traceback
        log(f"   Traceback:\n{traceback.format_exc()}")

    log("")
    log("=" * 70)
    log("DEBUG TEST COMPLETE")
    log("=" * 70)
    log("")
    log(f"Log saved to: {LOG_FILE}")
    log("")
    log("To view full log:")
    log(f"  cat {LOG_FILE}")
    log("")
    print("")
    print(f"📄 KOMPLETTER LOG: {LOG_FILE}")
    print("")
    print("Führe aus um Log zu sehen:")
    print(f"  cat {LOG_FILE}")
    print("")

if __name__ == "__main__":
    # Clear old log
    if LOG_FILE.exists():
        LOG_FILE.unlink()

    main()
