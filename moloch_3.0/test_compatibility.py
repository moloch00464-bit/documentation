#!/usr/bin/env python3
"""
Test: M.O.L.O.C.H. 2.0 → 3.0 Compatibility
"""

import json
import tempfile
from pathlib import Path

# Simuliere 2.0 Daten
old_2_0_data = {
    "name": "Rebecca",
    "sprache": "Klingonisch",
    "details": "Beste Freundin"
}

# Simuliere 3.0 Daten
new_3_0_data = {
    "content": {
        "name": "Rebecca",
        "sprache": "Klingonisch",
        "details": "Beste Freundin"
    },
    "metadata": {
        "created": "2025-01-01T00:00:00",
        "updated": "2025-01-01T00:00:00",
        "category": "wer/freunde",
        "filename": "rebecca.json"
    }
}

print("="*70)
print("M.O.L.O.C.H. 2.0 → 3.0 COMPATIBILITY TEST")
print("="*70)
print()

# Test 1: Lesen von 2.0 Daten
print("TEST 1: 3.0 Code liest 2.0 Daten")
print("-"*70)

with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
    json.dump(old_2_0_data, f)
    temp_file = f.name

# 3.0 Brain.read() macht nur: json.load(f)
with open(temp_file, 'r') as f:
    loaded = json.load(f)

print(f"2.0 Datei enthält: {old_2_0_data}")
print(f"3.0 read() gibt zurück: {loaded}")
print()

# Versuche darauf zuzugreifen wie 3.0 Code es erwartet
print("Zugriff wie 3.0 erwartet (data['content']['name']):")
try:
    name = loaded['content']['name']
    print(f"  ✅ Name: {name}")
except KeyError as e:
    print(f"  ❌ FEHLER: KeyError - {e}")
    print(f"     → 2.0 Daten haben KEIN 'content' key!")

print()

# Zugriff wie 2.0 Code es machte
print("Zugriff wie 2.0 es machte (data['name']):")
try:
    name = loaded['name']
    print(f"  ✅ Name: {name}")
except KeyError as e:
    print(f"  ❌ FEHLER: KeyError - {e}")

print()
print()

# Test 2: Was passiert beim Merge?
print("TEST 2: Merge von 2.0 Daten mit neuem Inhalt")
print("-"*70)

print("Alter Inhalt (2.0 Struktur):")
print(f"  {old_2_0_data}")
print()

print("3.0 save() mit merge=True versucht:")
print("  data['content'] = {**existing.get('content', {}), **inhalt}")
print()

# Simuliere was passiert
existing = old_2_0_data  # Das gibt read() zurück
new_inhalt = {"hobby": "Star Trek"}

merged_content = {**existing.get('content', {}), **new_inhalt}
print(f"Ergebnis: {merged_content}")
print()

if not merged_content.get("name"):
    print("❌ FEHLER: Alte Daten (name, sprache, details) sind WEG!")
    print("   → existing.get('content', {}) gibt {} zurück weil 2.0 kein 'content' hat")
    print("   → Nur 'hobby' bleibt übrig!")
    print("   → DATENVERLUST!")
else:
    print("✅ Alte Daten erhalten")

print()
print()

# Test 3: Rückwärtskompatible Lösung
print("TEST 3: Rückwärtskompatible Lösung")
print("-"*70)

def is_3_0_format(data):
    """Prüfe ob Daten im 3.0 Format sind"""
    return "content" in data and "metadata" in data

def normalize_to_3_0(data):
    """Konvertiere 2.0 → 3.0 Format"""
    if is_3_0_format(data):
        return data
    else:
        # 2.0 Format → Wrap in 3.0 Struktur
        return {
            "content": data,
            "metadata": {
                "created": "unknown",
                "updated": "unknown",
                "category": "unknown",
                "filename": "unknown",
                "migrated_from_2_0": True
            }
        }

# Test mit 2.0 Daten
normalized = normalize_to_3_0(old_2_0_data)
print("2.0 Daten normalisiert:")
print(json.dumps(normalized, indent=2, ensure_ascii=False))
print()

# Test Zugriff
print("Zugriff nach Normalisierung:")
name = normalized['content']['name']
print(f"  ✅ Name: {name}")

print()
print("="*70)
print("FAZIT")
print("="*70)
print()
print("❌ AKTUELLER 3.0 CODE IST NICHT KOMPATIBEL MIT 2.0 DATEN!")
print()
print("Probleme:")
print("  1. read() gibt rohe JSON zurück → 2.0 hat keine 'content' key")
print("  2. save() mit merge=True verliert 2.0 Daten")
print("  3. Kein Migrations-Code vorhanden")
print()
print("Lösung:")
print("  → read() muss 2.0 Daten automatisch zu 3.0 konvertieren")
print("  → Oder: Migrations-Script erstellen")
print()

# Cleanup
Path(temp_file).unlink()
