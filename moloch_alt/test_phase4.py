#!/usr/bin/env python3
"""
🧪 TEST: Phase 4 Modules
Testet alle Phase 4 Features: Clipboard, Location, Calendar, Wetter, Musik
"""

import subprocess
import sys
from pathlib import Path

def test_module(module_name, description):
    """Test a module's --help output"""
    print(f"\n{'='*60}")
    print(f"🧪 TEST: {description} ({module_name})")
    print('='*60)
    
    try:
        result = subprocess.run(
            [sys.executable, module_name, '--help'],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        if result.returncode == 0:
            print(f"✅ SUCCESS: {module_name} loaded successfully")
            print("\n📋 HELP OUTPUT:")
            print(result.stdout[:500])  # First 500 chars
            if len(result.stdout) > 500:
                print(f"... ({len(result.stdout)} Zeichen total)")
            return True
        else:
            print(f"❌ ERROR ({result.returncode}): {module_name}")
            print(f"stderr: {result.stderr[:300]}")
            return False
            
    except subprocess.TimeoutExpired:
        print(f"⏱️ TIMEOUT: {module_name} took too long")
        return False
    except Exception as e:
        print(f"🔥 EXCEPTION: {e}")
        return False

def main():
    """Run all Phase 4 tests"""
    cwd = Path.cwd()
    print(f"🧬 PHASE 4 MODULE TEST")
    print(f"📁 Working Directory: {cwd}")
    print(f"🐍 Python: {sys.version.split()[0]}")
    
    modules = [
        ("clipboard_monitor.py", "📋 Clipboard Monitor"),
        ("location_aware.py", "🗺️ Location Aware"),
        ("calendar_reminders.py", "📅 Calendar & Reminders"),
        ("weather_aware.py", "🌦️ Weather Aware"),
        ("music_recognition.py", "🎵 Music Recognition"),
    ]
    
    results = {}
    for module, desc in modules:
        results[module] = test_module(module, desc)
    
    # Summary
    print(f"\n\n{'='*60}")
    print("📊 TEST SUMMARY")
    print('='*60)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for module, success in results.items():
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status}: {module}")
    
    print(f"\n🎯 Result: {passed}/{total} modules working")
    
    if passed == total:
        print("🚀 ALL PHASE 4 MODULES OPERATIONAL!")
    else:
        print(f"⚠️ {total - passed} module(s) need attention")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
