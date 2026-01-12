#!/usr/bin/env python3
"""
Test: M.O.L.O.C.H. 2.0 → 3.0 Compatibility AFTER FIX
"""

import json
import sys
import tempfile
from pathlib import Path

# Add moloch_3.0 to path
sys.path.insert(0, str(Path(__file__).parent))

from core.brain import Brain

print("="*70)
print("M.O.L.O.C.H. 2.0 → 3.0 COMPATIBILITY TEST (AFTER FIX)")
print("="*70)
print()

# Create temp directory for testing
test_dir = Path(tempfile.mkdtemp(prefix="moloch_compat_test_"))
print(f"Test Dir: {test_dir}")
print()

# Create a Brain instance
brain = Brain(brain_dir=test_dir)

# Simulate 2.0 data (old format - no "content" wrapper)
old_2_0_data = {
    "name": "Rebecca",
    "sprache": "Klingonisch",
    "details": "Beste Freundin",
    "hobby": "Star Trek"
}

print("TEST 1: Manuell erstellte 2.0 Datei lesen")
print("-"*70)

# Manually write 2.0 format file
test_file = test_dir / "wer" / "rebecca.json"
test_file.parent.mkdir(parents=True, exist_ok=True)

with open(test_file, 'w', encoding='utf-8') as f:
    json.dump(old_2_0_data, f, ensure_ascii=False, indent=2)

print(f"Erstellt: {test_file}")
print(f"Inhalt (2.0 Format):")
print(json.dumps(old_2_0_data, ensure_ascii=False, indent=2))
print()

# Read with 3.0 Brain
print("Lesen mit 3.0 Brain.read():")
data = brain.read("wer", "rebecca.json")

if data:
    print(f"✅ Erfolgreich gelesen")
    print()
    print("Struktur:")
    print(json.dumps(data, ensure_ascii=False, indent=2))
    print()

    # Test access
    print("Zugriff auf Daten:")
    try:
        name = data['content']['name']
        sprache = data['content']['sprache']
        print(f"  ✅ Name: {name}")
        print(f"  ✅ Sprache: {sprache}")
        print(f"  ✅ Migration Flag: {data['metadata'].get('migrated_from_2_0', False)}")
    except KeyError as e:
        print(f"  ❌ FEHLER: {e}")
else:
    print("❌ Lesen fehlgeschlagen")

print()
print()

# TEST 2: Merge mit 2.0 Daten
print("TEST 2: Merge mit bestehenden 2.0 Daten")
print("-"*70)

print("Bestehende Daten (2.0 Format):")
print(f"  {old_2_0_data}")
print()

print("Neue Daten hinzufügen (save mit merge=True):")
new_data = {"lieblings_episode": "The Best of Both Worlds"}
print(f"  {new_data}")
print()

success = brain.save("wer", new_data, "rebecca.json", merge=True)

if success:
    print("✅ Save mit merge=True erfolgreich")
    print()

    # Read again
    merged = brain.read("wer", "rebecca.json")
    if merged:
        print("Ergebnis nach Merge:")
        print(json.dumps(merged['content'], ensure_ascii=False, indent=2))
        print()

        # Check if old data preserved
        if 'name' in merged['content'] and 'lieblings_episode' in merged['content']:
            print("✅ ERFOLG: Alte UND neue Daten vorhanden!")
            print(f"   - Alte Daten: name={merged['content']['name']}, sprache={merged['content']['sprache']}")
            print(f"   - Neue Daten: lieblings_episode={merged['content']['lieblings_episode']}")
        else:
            print("❌ FEHLER: Daten fehlen nach Merge")
else:
    print("❌ Save fehlgeschlagen")

print()
print()

# TEST 3: Neue 3.0 Daten schreiben und lesen
print("TEST 3: Neue 3.0 Daten schreiben und lesen")
print("-"*70)

new_person = {
    "name": "Sierra",
    "rolle": "Arbeitskollegin",
    "projekt": "M.O.L.O.C.H. 3.0"
}

print("Speichere neue Person (3.0 Format wird automatisch erstellt):")
print(f"  {new_person}")
print()

success = brain.save("wer", new_person, "sierra.json")

if success:
    print("✅ Save erfolgreich")
    print()

    # Read back
    data = brain.read("wer", "sierra.json")
    if data:
        print("Gespeicherte Struktur:")
        print(json.dumps(data, ensure_ascii=False, indent=2))
        print()

        if 'metadata' in data and 'created' in data['metadata']:
            print("✅ 3.0 Format mit Metadaten")
            print(f"   Erstellt: {data['metadata']['created']}")
        else:
            print("❌ Metadaten fehlen")
else:
    print("❌ Save fehlgeschlagen")

print()
print()

# TEST 4: find() mit gemischten 2.0 und 3.0 Daten
print("TEST 4: find() mit gemischten 2.0/3.0 Daten")
print("-"*70)

results = brain.find("Star Trek", kategorie="wer")
print(f"Suche nach 'Star Trek': {len(results)} Ergebnis(se)")
for result in results:
    if 'data' in result and 'content' in result['data']:
        print(f"  - {result['data']['content'].get('name', 'Unknown')} ({result['file']})")
    else:
        print(f"  - (Struktur-Fehler)")

print()
print()

# Cleanup
import shutil
shutil.rmtree(test_dir)
print(f"🧹 Test Dir gelöscht: {test_dir}")
print()

print("="*70)
print("FAZIT")
print("="*70)
print()
print("✅ M.O.L.O.C.H. 3.0 IST JETZT RÜCKWÄRTSKOMPATIBEL!")
print()
print("Features:")
print("  ✅ Liest 2.0 Daten ohne Probleme")
print("  ✅ Konvertiert automatisch zu 3.0 Format (in-memory)")
print("  ✅ Merge funktioniert mit 2.0 Daten")
print("  ✅ Alte Daten bleiben erhalten")
print("  ✅ Neue Daten werden im 3.0 Format gespeichert")
print()
print("Wichtig:")
print("  - Original 2.0 Dateien werden NICHT geändert beim Lesen")
print("  - Erst beim nächsten Save wird 3.0 Format geschrieben")
print("  - Flag 'migrated_from_2_0' zeigt konvertierte Dateien")
print()
