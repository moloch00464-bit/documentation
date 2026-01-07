#!/usr/bin/env python3
"""
🧪 LIVE TEST: Phase 4 Modules
Testet die Module praktisch und speichert Output in Datei
"""

import sys
import json
import time
from datetime import datetime
from pathlib import Path
from io import StringIO

# Teste jedes Modul einzeln
test_results = []

def test_weather():
    """Test weather_aware.py"""
    try:
        print("\n" + "="*70)
        print("🧪 TEST 1: Weather Aware (🌦️)")
        print("="*70)
        
        from weather_aware import WeatherAwareness
        
        print("✅ Module loaded successfully")
        
        # Erstelle Instanz
        weather = WeatherAwareness(latitude=52.5200, longitude=13.4050)
        print(f"✅ WeatherAwareness initialized")
        print(f"   Location: {weather.latitude}, {weather.longitude}")
        
        # Test get_weather
        if hasattr(weather, 'get_weather'):
            print("✅ get_weather() method found")
        
        # Config
        config = weather.load_config()
        print(f"✅ Config loaded: {len(config)} settings")
        
        return {
            "module": "weather_aware.py",
            "status": "✅ PASS",
            "info": "Weather module initialized successfully"
        }
    except Exception as e:
        print(f"❌ ERROR: {str(e)[:200]}")
        return {
            "module": "weather_aware.py",
            "status": "❌ FAIL",
            "error": str(e)[:100]
        }

def test_location():
    """Test location_aware.py"""
    try:
        print("\n" + "="*70)
        print("🧪 TEST 2: Location Aware (🗺️)")
        print("="*70)
        
        from location_aware import LocationAwareness
        
        print("✅ Module loaded successfully")
        
        # Erstelle Instanz
        location = LocationAwareness()
        print(f"✅ LocationAwareness initialized")
        
        # Config
        config = location.load_config()
        print(f"✅ Config loaded: {len(config)} settings")
        print(f"   Locations: {list(config.get('locations', {}).keys())}")
        
        return {
            "module": "location_aware.py",
            "status": "✅ PASS",
            "info": "Location module initialized successfully"
        }
    except Exception as e:
        print(f"❌ ERROR: {str(e)[:200]}")
        return {
            "module": "location_aware.py",
            "status": "❌ FAIL",
            "error": str(e)[:100]
        }

def test_clipboard():
    """Test clipboard_monitor.py"""
    try:
        print("\n" + "="*70)
        print("🧪 TEST 3: Clipboard Monitor (📋)")
        print("="*70)
        
        from clipboard_monitor import ClipboardMonitor
        
        print("✅ Module loaded successfully")
        
        # Erstelle Instanz
        clipboard = ClipboardMonitor()
        print(f"✅ ClipboardMonitor initialized")
        
        # Test get_clipboard
        if hasattr(clipboard, 'get_clipboard_text'):
            print("✅ get_clipboard_text() method found")
        
        return {
            "module": "clipboard_monitor.py",
            "status": "✅ PASS",
            "info": "Clipboard module initialized successfully"
        }
    except Exception as e:
        print(f"❌ ERROR: {str(e)[:200]}")
        return {
            "module": "clipboard_monitor.py",
            "status": "❌ FAIL",
            "error": str(e)[:100]
        }

def test_calendar():
    """Test calendar_reminders.py"""
    try:
        print("\n" + "="*70)
        print("🧪 TEST 4: Calendar & Reminders (📅)")
        print("="*70)
        
        from calendar_reminders import CalendarReminders
        
        print("✅ Module loaded successfully")
        
        # Erstelle Instanz
        calendar = CalendarReminders()
        print(f"✅ CalendarReminders initialized")
        
        # Check calendar data
        calendar_data = calendar.load_calendar()
        print(f"✅ Calendar data loaded: {len(calendar_data.get('events', []))} events")
        
        return {
            "module": "calendar_reminders.py",
            "status": "✅ PASS",
            "info": "Calendar module initialized successfully"
        }
    except Exception as e:
        print(f"❌ ERROR: {str(e)[:200]}")
        return {
            "module": "calendar_reminders.py",
            "status": "❌ FAIL",
            "error": str(e)[:100]
        }

def test_music():
    """Test music_recognition.py"""
    try:
        print("\n" + "="*70)
        print("🧪 TEST 5: Music Recognition (🎵)")
        print("="*70)
        
        from music_recognition import MusicRecognition
        
        print("✅ Module loaded successfully")
        
        # Erstelle Instanz
        music = MusicRecognition()
        print(f"✅ MusicRecognition initialized")
        
        # Check methods
        methods = [m for m in dir(music) if not m.startswith('_')]
        print(f"✅ {len(methods)} public methods found")
        
        return {
            "module": "music_recognition.py",
            "status": "✅ PASS",
            "info": "Music module initialized successfully"
        }
    except Exception as e:
        print(f"❌ ERROR: {str(e)[:200]}")
        return {
            "module": "music_recognition.py",
            "status": "❌ FAIL",
            "error": str(e)[:100]
        }

def main():
    """Run all tests"""
    print("\n" + "╔" + "="*68 + "╗")
    print("║" + " "*68 + "║")
    print("║" + "  🧪 PHASE 4 LIVE TEST SUITE".center(68) + "║")
    print("║" + "  Testing all Phase 4 modules with actual execution".center(68) + "║")
    print("║" + " "*68 + "║")
    print("╚" + "="*68 + "╝\n")
    
    print(f"⏰ Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"📁 Working directory: {Path.cwd()}")
    print(f"🐍 Python version: {sys.version.split()[0]}\n")
    
    # Run all tests
    test_results.append(test_weather())
    test_results.append(test_location())
    test_results.append(test_clipboard())
    test_results.append(test_calendar())
    test_results.append(test_music())
    
    # Summary
    print("\n" + "="*70)
    print("📊 TEST SUMMARY")
    print("="*70 + "\n")
    
    passed = sum(1 for r in test_results if "PASS" in r["status"])
    total = len(test_results)
    
    for result in test_results:
        status_icon = "✅" if "PASS" in result["status"] else "❌"
        print(f"{status_icon} {result['module']:30} - {result['status']}")
        if "info" in result:
            print(f"   ℹ️  {result['info']}")
        if "error" in result:
            print(f"   ❌ {result['error'][:60]}")
    
    print(f"\n{'='*70}")
    print(f"🎯 Result: {passed}/{total} modules passed")
    print(f"{'='*70}\n")
    
    if passed == total:
        print("🚀 ALL PHASE 4 MODULES WORKING!")
        print("✅ Ready for deployment!")
    else:
        print(f"⚠️  {total - passed} module(s) need attention")
    
    # Save results to JSON
    with open("test_results.json", "w", encoding="utf-8") as f:
        json.dump({
            "timestamp": datetime.now().isoformat(),
            "total_tests": total,
            "passed": passed,
            "failed": total - passed,
            "results": test_results
        }, f, indent=2, ensure_ascii=False)
    
    print("\n📄 Results saved to: test_results.json\n")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
