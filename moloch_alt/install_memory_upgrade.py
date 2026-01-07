#!/usr/bin/env python3
"""
M.O.L.O.C.H. MEMORY UPGRADE INSTALLER
=====================================
Fügt search_memory() und erweiterte extract_memory() hinzu
"""

import os
import re
import shutil
from datetime import datetime

MOLOCH_FILE = os.path.expanduser("~/moloch/moloch.py")

# ═══════════════════════════════════════════════════════════════════════════════
# NEUE FUNKTIONEN
# ═══════════════════════════════════════════════════════════════════════════════

SEARCH_MEMORY_CODE = '''

def search_memory(query):
    """Durchsucht langzeit.json nach passenden Einträgen"""
    memory = load_memory()
    query_lower = query.lower()
    results = []
    
    for kategorie, items in memory.items():
        for item in items:
            if query_lower in item.lower():
                results.append(f"[{kategorie}] {item}")
    
    return results

'''

NEW_EXTRACT_MEMORY_CODE = '''def extract_memory(user_input, response, memory):
    """Extrahiert wichtige Infos aus dem Gespräch - ERWEITERT"""
    lower = user_input.lower()
    changed = False

    # ═══════════════════════════════════════════════════════════════
    # EXPLIZITE SPEICHER-BEFEHLE (erweitert!)
    # ═══════════════════════════════════════════════════════════════
    speicher_trigger = [
        "merk dir", "merke dir", "vergiss nicht",
        "speicher das", "speicher es", "speicher ab",
        "das ist wichtig", "nicht vergessen", "füge ein",
        "denk dran", "behalte", "erinnere dich"
    ]
    
    for trigger in speicher_trigger:
        if trigger in lower:
            # Text nach dem Trigger extrahieren
            info = user_input.split(trigger)[-1].strip()
            info = info.lstrip(":,. ")  # Satzzeichen am Anfang weg
            
            if info and len(info) > 3:
                # Auto-Kategorisierung versuchen
                kategorie = auto_kategorisiere(info)
                
                if info not in memory[kategorie]:
                    memory[kategorie].append(info)
                    changed = True
                    print(f"💾 [{kategorie}] {info}")
            break

    # ═══════════════════════════════════════════════════════════════
    # VORLIEBEN ERKENNEN
    # ═══════════════════════════════════════════════════════════════
    vorlieben_trigger = ["mag ich", "liebe ich", "gefällt mir", 
                         "gefaellt mir", "höre gern", "schau gern"]
    
    for trigger in vorlieben_trigger:
        if trigger in lower:
            if user_input not in memory["vorlieben"]:
                memory["vorlieben"].append(user_input)
                changed = True
                print(f"💾 [vorlieben] {user_input}")
            break

    return changed


def auto_kategorisiere(text):
    """Versucht Text automatisch zu kategorisieren"""
    lower = text.lower()
    
    # Personen-Indikatoren
    personen_keywords = ["heißt", "heisst", "name ist", "freund", "freundin", 
                         "kollege", "kollegin", "bruder", "schwester", "chef",
                         "kennt", "arbeitet bei", "ist von"]
    if any(kw in lower for kw in personen_keywords):
        return "personen"
    
    # Ort-Indikatoren
    ort_keywords = ["wohnt", "wohne", "stadt", "straße", "strasse", 
                    "liegt in", "kommt aus", "geboren in", "adresse",
                    "nürnberg", "schwabach", "leipzig"]
    if any(kw in lower for kw in ort_keywords):
        return "orte"
    
    # Projekt-Indikatoren
    projekt_keywords = ["projekt", "baue", "bastel", "programmier", 
                        "arbeite an", "entwickle", "esp32", "home assistant",
                        "led", "sensor", "arduino", "raspberry"]
    if any(kw in lower for kw in projekt_keywords):
        return "projekte"
    
    # Fakten-Indikatoren
    fakten_keywords = ["ist ein", "bedeutet", "heißt dass", "funktioniert",
                       "steht für", "nennt man", "definition"]
    if any(kw in lower for kw in fakten_keywords):
        return "fakten"
    
    # Default: wichtig
    return "wichtig"

'''

# ═══════════════════════════════════════════════════════════════════════════════
# INSTALLER
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    print("╔═══════════════════════════════════════════════════════════════╗")
    print("║  M.O.L.O.C.H. MEMORY UPGRADE INSTALLER                        ║")
    print("╚═══════════════════════════════════════════════════════════════╝")
    print()
    
    # Check ob Datei existiert
    if not os.path.exists(MOLOCH_FILE):
        print(f"❌ FEHLER: {MOLOCH_FILE} nicht gefunden!")
        return False
    
    # Backup erstellen
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = f"{MOLOCH_FILE}.backup_{timestamp}"
    
    print(f"📦 Erstelle Backup: {backup_file}")
    shutil.copy2(MOLOCH_FILE, backup_file)
    print("✅ Backup erstellt")
    print()
    
    # Datei lesen
    with open(MOLOCH_FILE, 'r', encoding='utf-8') as f:
        content = f.read()
    
    modified = False
    
    # ═══════════════════════════════════════════════════════════════
    # ADDITION 1: search_memory()
    # ═══════════════════════════════════════════════════════════════
    print("🔧 Prüfe search_memory()...")
    
    if "def search_memory" in content:
        print("⚠️  search_memory() existiert bereits - überspringe")
    else:
        # Nach save_memory() einfügen
        pattern = r'(def save_memory\(memory\):.*?save_json\(MEMORY_FILE, memory\))'
        match = re.search(pattern, content, re.DOTALL)
        
        if match:
            insert_pos = match.end()
            content = content[:insert_pos] + SEARCH_MEMORY_CODE + content[insert_pos:]
            print("✅ search_memory() hinzugefügt")
            modified = True
        else:
            print("⚠️  save_memory() nicht gefunden - manuell einfügen!")
    
    # ═══════════════════════════════════════════════════════════════
    # ÄNDERUNG 2: extract_memory() ersetzen
    # ═══════════════════════════════════════════════════════════════
    print("🔧 Ersetze extract_memory()...")
    
    # Pattern für alte extract_memory (bis zum nächsten Kommentarblock)
    pattern = r'def extract_memory\(user_input, response, memory\):.*?return changed\n'
    
    if re.search(pattern, content, re.DOTALL):
        content = re.sub(pattern, NEW_EXTRACT_MEMORY_CODE, content, flags=re.DOTALL)
        print("✅ extract_memory() ersetzt")
        print("✅ auto_kategorisiere() hinzugefügt")
        modified = True
    else:
        print("⚠️  extract_memory() Pattern nicht gefunden!")
    
    # Speichern
    if modified:
        with open(MOLOCH_FILE, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print()
        print("═══════════════════════════════════════════════════════════════")
        print("🎯 INSTALLATION ERFOLGREICH!")
        print("═══════════════════════════════════════════════════════════════")
        print()
        print("📋 TESTEN MIT:")
        print('   python ~/moloch/moloch.py "merk dir: Test Eintrag"')
        print('   python ~/moloch/moloch.py "speicher ab: Erkan ist Staplerfahrer"')
        print("   python ~/moloch/moloch.py -m")
        print()
        print("🔙 BEI PROBLEMEN:")
        print(f"   cp {backup_file} {MOLOCH_FILE}")
    else:
        print()
        print("⚠️  Keine Änderungen vorgenommen")
    
    return modified


if __name__ == "__main__":
    main()
