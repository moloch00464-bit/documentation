#!/bin/bash
###############################################################################
# M.O.L.O.C.H. 2.0 → 3.0 MIGRATION SCRIPT
# ========================================
# Migriert ALLE Daten von M.O.L.O.C.H. 2.0 nach 3.0
#
# WICHTIG: Führe dieses Script auf deinem Termux-Gerät aus!
###############################################################################

set -e  # Stop bei Fehler

echo "════════════════════════════════════════════════════════════════"
echo "  M.O.L.O.C.H. 2.0 → 3.0 MIGRATION"
echo "  Alle Daten werden übertragen - KEIN Datenverlust!"
echo "════════════════════════════════════════════════════════════════"
echo ""

# Pfade definieren
MOLOCH_2_DIR="$HOME/moloch"
MOLOCH_3_DIR="$HOME/documentation/moloch_3.0"
MOLOCH_3_DATA="$MOLOCH_3_DIR/data"

# Backup-Verzeichnis erstellen
BACKUP_DIR="$HOME/moloch_migration_backup_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"

echo "📁 M.O.L.O.C.H. 2.0 Quelle: $MOLOCH_2_DIR"
echo "📁 M.O.L.O.C.H. 3.0 Ziel:   $MOLOCH_3_DIR"
echo "💾 Backup wird erstellt:    $BACKUP_DIR"
echo ""

# Prüfen ob 2.0 existiert
if [ ! -d "$MOLOCH_2_DIR" ]; then
    echo "❌ FEHLER: $MOLOCH_2_DIR nicht gefunden!"
    echo "   Bist du auf deinem Termux-Gerät?"
    exit 1
fi

# Prüfen ob 3.0 existiert
if [ ! -d "$MOLOCH_3_DIR" ]; then
    echo "❌ FEHLER: $MOLOCH_3_DIR nicht gefunden!"
    echo "   Hast du das Git-Repository geclont?"
    exit 1
fi

echo "✅ Beide Verzeichnisse gefunden!"
echo ""

# Backup von 3.0 erstellen (falls es schiefgeht)
echo "💾 Erstelle Backup von M.O.L.O.C.H. 3.0 Daten..."
if [ -d "$MOLOCH_3_DATA" ]; then
    cp -r "$MOLOCH_3_DATA" "$BACKUP_DIR/moloch_3.0_data_backup"
    echo "   ✅ Backup erstellt: $BACKUP_DIR/moloch_3.0_data_backup"
fi
echo ""

###############################################################################
# MIGRATION 1: BRAIN-VERZEICHNIS
###############################################################################

echo "🧠 [1/3] MIGRIERE BRAIN-VERZEICHNIS..."
echo "────────────────────────────────────────────────────────────────"

if [ -d "$MOLOCH_2_DIR/brain" ]; then
    # Brain-Verzeichnis komplett kopieren
    echo "   📂 Kopiere Brain-Struktur..."
    mkdir -p "$MOLOCH_3_DATA"
    cp -r "$MOLOCH_2_DIR/brain" "$MOLOCH_3_DATA/"

    # Statistiken
    BRAIN_DIRS=$(find "$MOLOCH_3_DATA/brain" -type d | wc -l)
    BRAIN_FILES=$(find "$MOLOCH_3_DATA/brain" -type f | wc -l)

    echo "   ✅ Brain migriert!"
    echo "      📁 $BRAIN_DIRS Verzeichnisse"
    echo "      📄 $BRAIN_FILES Dateien"
else
    echo "   ⚠️  Kein Brain-Verzeichnis in 2.0 gefunden"
fi
echo ""

###############################################################################
# MIGRATION 2: LANGZEIT-GEDÄCHTNIS (JSON MERGE!)
###############################################################################

echo "💾 [2/3] MIGRIERE LANGZEIT-GEDÄCHTNIS..."
echo "────────────────────────────────────────────────────────────────"

if [ -f "$MOLOCH_2_DIR/langzeit.json" ]; then
    LANGZEIT_2_SIZE=$(du -h "$MOLOCH_2_DIR/langzeit.json" | cut -f1)
    echo "   📄 2.0 langzeit.json: $LANGZEIT_2_SIZE"

    # Prüfen ob 3.0 schon ein langzeit.json hat
    if [ -f "$MOLOCH_3_DATA/langzeit.json" ]; then
        echo "   ⚠️  3.0 hat bereits langzeit.json - wird gesichert"
        cp "$MOLOCH_3_DATA/langzeit.json" "$BACKUP_DIR/langzeit_3.0_old.json"
    fi

    # Python-Script für intelligentes Mergen
    echo "   🔄 Merge 2.0 + 3.0 Langzeit-Daten..."

    python3 << 'PYTHON_SCRIPT'
import json
import sys
from pathlib import Path

# Pfade
moloch_2 = Path.home() / "moloch" / "langzeit.json"
moloch_3 = Path.home() / "documentation" / "moloch_3.0" / "data" / "langzeit.json"

# Lade 2.0 Daten
with open(moloch_2, 'r', encoding='utf-8') as f:
    data_2 = json.load(f)

# Lade 3.0 Daten (falls vorhanden)
if moloch_3.exists():
    with open(moloch_3, 'r', encoding='utf-8') as f:
        data_3 = json.load(f)
else:
    data_3 = {"fakten": [], "personen": [], "orte": [], "vorlieben": [], "events": []}

# Merge: 2.0 Daten haben Priorität, 3.0 Daten werden hinzugefügt wenn neu
merged = {}
for key in set(list(data_2.keys()) + list(data_3.keys())):
    if key not in merged:
        merged[key] = []

    # 2.0 Daten zuerst
    if key in data_2:
        if isinstance(data_2[key], list):
            merged[key].extend(data_2[key])
        else:
            merged[key] = data_2[key]

    # 3.0 Daten hinzufügen (nur wenn nicht schon vorhanden)
    if key in data_3 and isinstance(data_3[key], list):
        for item in data_3[key]:
            if item not in merged[key]:
                merged[key].append(item)

# Speichern
moloch_3.parent.mkdir(parents=True, exist_ok=True)
with open(moloch_3, 'w', encoding='utf-8') as f:
    json.dump(merged, f, indent=2, ensure_ascii=False)

# Statistiken
total_entries = sum(len(v) if isinstance(v, list) else 1 for v in merged.values())
print(f"   ✅ Langzeit-Gedächtnis gemerged!")
print(f"      📊 Gesamt: {total_entries} Einträge")
for key, val in merged.items():
    if isinstance(val, list):
        print(f"      - {key}: {len(val)}")
PYTHON_SCRIPT

else
    echo "   ⚠️  Keine langzeit.json in 2.0 gefunden"
fi
echo ""

###############################################################################
# MIGRATION 3: HISTORY
###############################################################################

echo "📜 [3/3] MIGRIERE CONVERSATION HISTORY..."
echo "────────────────────────────────────────────────────────────────"

if [ -f "$MOLOCH_2_DIR/history.json" ]; then
    HISTORY_SIZE=$(du -h "$MOLOCH_2_DIR/history.json" | cut -f1)
    echo "   📄 2.0 history.json: $HISTORY_SIZE"

    # Backup von 3.0 History (falls vorhanden)
    if [ -f "$MOLOCH_3_DATA/history.json" ]; then
        cp "$MOLOCH_3_DATA/history.json" "$BACKUP_DIR/history_3.0_old.json"
    fi

    # History kopieren (2.0 überschreibt 3.0, da 3.0 eh leer ist)
    cp "$MOLOCH_2_DIR/history.json" "$MOLOCH_3_DATA/history.json"

    # Anzahl Gespräche zählen
    CONVERSATIONS=$(python3 -c "import json; print(len(json.load(open('$MOLOCH_3_DATA/history.json'))))")
    echo "   ✅ History migriert!"
    echo "      💬 $CONVERSATIONS Gespräche"
else
    echo "   ⚠️  Keine history.json in 2.0 gefunden"
fi
echo ""

###############################################################################
# BONUS: Weitere wichtige Dateien
###############################################################################

echo "📦 [BONUS] WEITERE DATEIEN..."
echo "────────────────────────────────────────────────────────────────"

# gehirn_index.json
if [ -f "$MOLOCH_2_DIR/gehirn_index.json" ]; then
    cp "$MOLOCH_2_DIR/gehirn_index.json" "$MOLOCH_3_DATA/"
    echo "   ✅ gehirn_index.json kopiert"
fi

# self_awareness.json
if [ -f "$MOLOCH_2_DIR/self_awareness.json" ]; then
    cp "$MOLOCH_2_DIR/self_awareness.json" "$MOLOCH_3_DATA/"
    echo "   ✅ self_awareness.json kopiert"
fi

echo ""

###############################################################################
# ABSCHLUSS
###############################################################################

echo "════════════════════════════════════════════════════════════════"
echo "  ✅ MIGRATION ERFOLGREICH ABGESCHLOSSEN!"
echo "════════════════════════════════════════════════════════════════"
echo ""
echo "📊 ZUSAMMENFASSUNG:"
echo "   🧠 Brain-Verzeichnis:      migriert"
echo "   💾 Langzeit-Gedächtnis:    gemerged"
echo "   📜 Conversation History:   migriert"
echo "   💾 Backup erstellt in:     $BACKUP_DIR"
echo ""
echo "🎉 M.O.L.O.C.H. 3.0 hat jetzt das komplette Gedächtnis von 2.0!"
echo ""
echo "NÄCHSTE SCHRITTE:"
echo "1. Prüfe die Daten in: $MOLOCH_3_DATA"
echo "2. Teste M.O.L.O.C.H. 3.0"
echo "3. Wenn alles läuft, kannst du das Backup löschen"
echo ""
echo "Bei Problemen: Das Backup liegt in $BACKUP_DIR"
echo "════════════════════════════════════════════════════════════════"
