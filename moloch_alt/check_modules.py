#!/usr/bin/env python3
"""
📊 Phase 4 Module Analysis
Zeigt Modulinformationen ohne Terminal-Output-Probleme
"""

import py_compile
import sys
from pathlib import Path

modules = [
    "clipboard_monitor.py",
    "location_aware.py", 
    "calendar_reminders.py",
    "weather_aware.py",
    "music_recognition.py",
]

print("=" * 70)
print("🧪 PHASE 4 MODULE SYNTAX CHECK")
print("=" * 70)

passed = 0
failed = []

for module in modules:
    filepath = Path(module)
    if filepath.exists():
        try:
            py_compile.compile(str(filepath), doraise=True)
            print(f"✅ {module:30} - OK ({filepath.stat().st_size:6d} bytes)")
            passed += 1
        except py_compile.PyCompileError as e:
            print(f"❌ {module:30} - SYNTAX ERROR")
            print(f"   Error: {str(e)[:100]}")
            failed.append(module)
    else:
        print(f"⚠️  {module:30} - FILE NOT FOUND")
        failed.append(module)

print("\n" + "=" * 70)
print(f"📊 RESULT: {passed}/{len(modules)} modules passed syntax check")
print("=" * 70)

if failed:
    print(f"\n🔥 Failed modules: {', '.join(failed)}")
    sys.exit(1)
else:
    print("\n✅ ALL PHASE 4 MODULES SYNTACTICALLY CORRECT!")
    sys.exit(0)
