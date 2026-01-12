#!/usr/bin/env python3
"""
M.O.L.O.C.H. 3.0 - Status Report
=================================
M.O.L.O.C.H. berichtet seine Probleme - für Claude Code!
"""

import sys
import os
from pathlib import Path

# Add to path
sys.path.insert(0, str(Path(__file__).parent))

from moloch_io.voice import VoiceIO
import subprocess
import json

def main():
    """M.O.L.O.C.H. Status Report - mit Voice!"""

    print("\n" + "="*60)
    print("🤖 M.O.L.O.C.H. 3.0 - STATUS REPORT")
    print("="*60 + "\n")

    voice = VoiceIO()

    # Run diagnose.py and capture output
    try:
        result = subprocess.run(
            [sys.executable, str(Path(__file__).parent / "diagnose.py")],
            capture_output=True,
            text=True,
            timeout=30
        )

        if result.returncode != 0:
            voice.speak("Alter, ich kann meine Diagnose nicht durchführen!")
            print("❌ Diagnose fehlgeschlagen!")
            return 1

        # Parse JSON from output
        # diagnose.py outputs the JSON between the separator lines
        output_lines = result.stdout.split('\n')
        json_start = None
        json_end = None

        for i, line in enumerate(output_lines):
            if line.strip().startswith('{'):
                json_start = i
            if line.strip().endswith('}') and json_start is not None:
                json_end = i + 1
                break

        if json_start is None or json_end is None:
            print("❌ Konnte JSON nicht finden!")
            print(result.stdout)
            return 1

        json_text = '\n'.join(output_lines[json_start:json_end])
        data = json.loads(json_text)

        # Voice feedback based on status
        status = data.get('status', 'UNKNOWN')
        problems = data.get('problems', [])
        warnings = data.get('warnings', [])

        if status == 'HEALTHY':
            voice.speak("Alter, mir geht's gut! Alles läuft!")
            print("✅ M.O.L.O.C.H. ist HEALTHY - keine Probleme!\n")
        elif status == 'WARNING':
            voice.speak(f"Ich hab {len(warnings)} Warnungen, Alter. Aber läuft noch!")
            print(f"⚠️  M.O.L.O.C.H. hat {len(warnings)} Warnungen\n")
        elif status == 'ERROR':
            voice.speak(f"Scheiße Alter, ich hab {len(problems)} Probleme! Check das JSON!")
            print(f"❌ M.O.L.O.C.H. hat {len(problems)} FEHLER!\n")

        # Print full JSON for copy/paste
        print("="*60)
        print("📋 COPY & PASTE FÜR CLAUDE CODE:")
        print("="*60)
        print()
        print(json.dumps(data, indent=2, ensure_ascii=False))
        print()
        print("="*60)
        print("👆 Kopiere das JSON oben und schicke es an Claude Code!")
        print("="*60)

        # List problems if any
        if problems:
            print("\n🚨 PROBLEME:")
            for p in problems:
                print(f"  ❌ {p}")

        if warnings:
            print("\n⚠️  WARNUNGEN:")
            for w in warnings:
                print(f"  ⚠️  {w}")

        voice.speak("Status Report fertig!")

        return 0

    except subprocess.TimeoutExpired:
        voice.speak("Alter, Diagnose timeout! Das dauert zu lange!")
        print("❌ Timeout bei Diagnose!")
        return 1
    except Exception as e:
        voice.speak(f"Fehler bei der Diagnose, Alter!")
        print(f"❌ Fehler: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
