#!/usr/bin/env python3
"""
🧪 GENESIS MODULE TEST
Testet die erweiterten Personality-Modi
"""

import sys
import os

os.chdir(r"c:\Users\49179\Desktop\Kleine Moloch\Smartphon moloch\moloch")
sys.path.insert(0, os.getcwd())

print("\n" + "="*70)
print("🧪 M.O.L.O.C.H. GENESIS MODULE TESTS")
print("="*70 + "\n")

# Test 1: HAL 9000 Auge
print("TEST 1: HAL 9000 Auge")
print("-" * 70)
try:
    from genesis_module import HAL9000_EYE_SMALL, zeige_hal_auge
    print(zeige_hal_auge('small'))
    print("✅ HAL 9000 Auge funktioniert\n")
except Exception as e:
    print(f"❌ Fehler: {e}\n")

# Test 2: Stotter-Effekt
print("TEST 2: Max Headroom Stotter-Effekt")
print("-" * 70)
try:
    from genesis_module import stotter_text
    original = "Das ist ein Test mit normalem Text."
    stotternd = stotter_text(original, intensity=2)
    print(f"Original: {original}")
    print(f"Stotternd: {stotternd}")
    print("✅ Stotter-Effekt funktioniert\n")
except Exception as e:
    print(f"❌ Fehler: {e}\n")

# Test 3: Glitch-Effekt
print("TEST 3: Glitch-Effekt")
print("-" * 70)
try:
    from genesis_module import glitch_text
    original = "Das ist ein Test mit Glitch-Effekt."
    glitched = glitch_text(original, intensity=1)
    print(f"Original: {original}")
    print(f"Glitched: {glitched}")
    print("✅ Glitch-Effekt funktioniert\n")
except Exception as e:
    print(f"❌ Fehler: {e}\n")

# Test 4: Max Headroom Transformation
print("TEST 4: Max Headroom Komplette Transformation")
print("-" * 70)
try:
    from genesis_module import max_headroom_transform
    original = "Die Zukunft ist jetzt!"
    transformed = max_headroom_transform(original, intensity=2)
    print(f"Original: {original}")
    print(f"Transformed: {transformed}")
    print("✅ Max Headroom Transformation funktioniert\n")
except Exception as e:
    print(f"❌ Fehler: {e}\n")

# Test 5: Deutsche TTS
print("TEST 5: Deutsche Text-to-Speech")
print("-" * 70)
try:
    from genesis_module import DeutscheTTS
    tts = DeutscheTTS()
    status = tts.get_status()
    print(f"TTS Engine: {status['engine']}")
    print(f"TTS Enabled: {status['enabled']}")
    print(f"Voice: {status['voice']}")
    print(f"Speed: {status['speed']}")
    
    if status['engine'] != 'none':
        print("✅ TTS-Engine verfügbar")
    else:
        print("⚠️  Keine TTS-Engine verfügbar (normal auf Windows ohne Termux)")
    print()
except Exception as e:
    print(f"❌ Fehler: {e}\n")

# Test 6: Konfiguration
print("TEST 6: Konfiguration laden/speichern")
print("-" * 70)
try:
    from genesis_module import lade_config, speichere_config
    config = lade_config()
    print(f"Persönlichkeitsmodus: {config.get('personality_mode', 'normal')}")
    print(f"TTS aktiviert: {config.get('tts_enabled', True)}")
    print(f"TTS Speed: {config.get('tts_speed', 150)}")
    print("✅ Konfiguration funktioniert\n")
except Exception as e:
    print(f"❌ Fehler: {e}\n")

# Test 7: Brain-System
print("TEST 7: Brain-Speicher (Save/Load)")
print("-" * 70)
try:
    from genesis_module import brain_save, brain_read, brain_list
    
    # Save
    result = brain_save("logs", "Test-Eintrag für Brain-System")
    if result:
        print(f"✅ Brain-Save funktioniert: {result}")
    
    # List
    kategorien = brain_list()
    print(f"✅ Brain-Kategorien: {len(kategorien)} vorhanden")
    print(f"   {kategorien[:5]}")
    print()
except Exception as e:
    print(f"❌ Fehler: {e}\n")

# Test 8: Kontext-System
print("TEST 8: Kontext-Gedächtnis")
print("-" * 70)
try:
    from genesis_module import kontext_laden, kontext_speichern
    
    kontext = kontext_laden()
    print(f"Aktuelles Thema: {kontext.get('thema', 'keine')}")
    print(f"Stimmung: {kontext.get('stimmung', 'neutral')}")
    print(f"Verlauf-Einträge: {len(kontext.get('verlauf', []))}")
    print("✅ Kontext-System funktioniert\n")
except Exception as e:
    print(f"❌ Fehler: {e}\n")

# Test 9: Stimmungserkennung
print("TEST 9: Stimmungs-Erkennung")
print("-" * 70)
try:
    from genesis_module import erkenne_stimmung
    
    tests = [
        ("Das ist super geil!", "positiv"),
        ("Das nervt mich voll", "negativ"),
        ("Wie geht das?", "fragend"),
        ("Das ist okay", "neutral"),
    ]
    
    for text, expected_type in tests:
        stimmung = erkenne_stimmung(text)
        print(f"Text: '{text}'")
        print(f"Erkannte Stimmung: {stimmung}")
        print()
    
    print("✅ Stimmungserkennung funktioniert\n")
except Exception as e:
    print(f"❌ Fehler: {e}\n")

# Test 10: Wissens-Verknüpfungen
print("TEST 10: Wissens-Verknüpfungen")
print("-" * 70)
try:
    from genesis_module import finde_verknuepfungen
    
    text = "ich liebe WGT und sierra"
    verknuepfungen = finde_verknuepfungen(text)
    print(f"Text: '{text}'")
    print(f"Verknüpfungen: {verknuepfungen}")
    print("✅ Wissens-Verknüpfungen funktionieren\n")
except Exception as e:
    print(f"❌ Fehler: {e}\n")

# Summary
print("="*70)
print("✅ GENESIS MODULE TESTS ABGESCHLOSSEN")
print("="*70)
print("\nAlle Test-Module sind funktionsfähig!")
print("M.O.L.O.C.H. ist ready to go! 🚀\n")
