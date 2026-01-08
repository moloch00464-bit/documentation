#!/usr/bin/env python3
"""
M.O.L.O.C.H. 3.0 - GENESIS Migration Tool
===========================================
Import data from old M.O.L.O.C.H. GENESIS
"""

import json
import shutil
from pathlib import Path
from typing import Dict, List
from datetime import datetime

from core.config import (
    OLD_MOLOCH_DIR,
    OLD_BRAIN_DIR,
    OLD_HISTORY_FILE,
    OLD_MEMORY_FILE,
    BRAIN_DIR,
    HISTORY_FILE,
    MEMORY_FILE
)
from core.brain import Brain
from core.memory import Memory


class GenesisImporter:
    """
    Import M.O.L.O.C.H. GENESIS data into M.O.L.O.C.H. 3.0

    Migration:
    - Brain Tree (~/moloch/brain/ → ~/moloch_3.0/data/brain/)
    - History (~/moloch/history.json → ~/moloch_3.0/data/history.json)
    - Memory (~/moloch/langzeit.json → ~/moloch_3.0/data/langzeit.json)
    """

    def __init__(
        self,
        old_moloch_dir: Path = OLD_MOLOCH_DIR,
        dry_run: bool = False
    ):
        """
        Initialize Genesis Importer

        Args:
            old_moloch_dir: Path to old M.O.L.O.C.H. directory
            dry_run: If True, don't actually copy files (just report)
        """
        self.old_dir = Path(old_moloch_dir)
        self.dry_run = dry_run

        self.brain = Brain()
        self.memory = Memory()

        self.stats = {
            "brain_files": 0,
            "history_entries": 0,
            "memory_entries": 0,
            "errors": []
        }

    # ═══════════════════════════════════════════════════════════════════════════
    # MAIN IMPORT
    # ═══════════════════════════════════════════════════════════════════════════

    def import_all(self) -> bool:
        """
        Import all GENESIS data

        Returns:
            Success status
        """
        print("\n🚀 M.O.L.O.C.H. GENESIS → 3.0 Migration\n")

        if self.dry_run:
            print("🔍 DRY RUN MODE (no actual changes)\n")

        # Check if old M.O.L.O.C.H. exists
        if not self.old_dir.exists():
            print(f"❌ Old M.O.L.O.C.H. not found: {self.old_dir}")
            print(f"   Expected path: {self.old_dir}")
            return False

        print(f"✅ Found GENESIS at: {self.old_dir}\n")

        # Backup old M.O.L.O.C.H. first!
        if not self.dry_run:
            self._backup_genesis()

        # Import brain
        print("🧠 Importing Brain Tree...")
        self.import_brain()

        # Import memory
        print("\n💾 Importing Long-term Memory...")
        self.import_memory()

        # Import history
        print("\n📜 Importing History...")
        self.import_history()

        # Print stats
        self._print_stats()

        # Verify
        print("\n🔍 Verifying import...")
        if self.verify_import():
            print("✅ Migration successful!\n")
            return True
        else:
            print("⚠️ Migration completed with warnings\n")
            return False

    def _backup_genesis(self):
        """Backup old M.O.L.O.C.H. before migration"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_dir = self.old_dir.parent / f"moloch_backup_{timestamp}"

        print(f"💾 Creating backup: {backup_dir}")

        try:
            shutil.copytree(self.old_dir, backup_dir)
            print(f"   ✅ Backup created\n")
        except Exception as e:
            print(f"   ⚠️ Backup failed: {e}\n")
            self.stats["errors"].append(f"Backup failed: {e}")

    # ═══════════════════════════════════════════════════════════════════════════
    # BRAIN IMPORT
    # ═══════════════════════════════════════════════════════════════════════════

    def import_brain(self):
        """Import Brain Tree"""
        old_brain_dir = OLD_BRAIN_DIR

        if not old_brain_dir.exists():
            print(f"   ⚠️ No brain directory found: {old_brain_dir}")
            return

        # Import each category
        categories = ["wer", "was", "wo", "wann", "wie", "kontext"]

        for category in categories:
            old_category_dir = old_brain_dir / category

            if not old_category_dir.exists():
                continue

            # Copy all JSON files in category
            for json_file in old_category_dir.rglob("*.json"):
                try:
                    # Read old file
                    with open(json_file, "r", encoding="utf-8") as f:
                        data = json.load(f)

                    # Get relative path from brain root
                    rel_path = json_file.relative_to(old_brain_dir)
                    kategorie = str(rel_path.parent)
                    filename = rel_path.name

                    # Save to new brain
                    if not self.dry_run:
                        # Check if data has old structure (just dict) or new structure (with metadata)
                        if "content" in data and "metadata" in data:
                            content = data["content"]
                        else:
                            content = data

                        self.brain.save(kategorie, content, filename)

                    self.stats["brain_files"] += 1
                    print(f"   ✅ {kategorie}/{filename}")

                except Exception as e:
                    error_msg = f"Failed to import {json_file}: {e}"
                    self.stats["errors"].append(error_msg)
                    print(f"   ❌ {error_msg}")

        print(f"\n   📊 Imported {self.stats['brain_files']} brain files")

    # ═══════════════════════════════════════════════════════════════════════════
    # MEMORY IMPORT
    # ═══════════════════════════════════════════════════════════════════════════

    def import_memory(self):
        """Import long-term memory"""
        if not OLD_MEMORY_FILE.exists():
            print(f"   ⚠️ No memory file found: {OLD_MEMORY_FILE}")
            return

        try:
            # Read old memory
            with open(OLD_MEMORY_FILE, "r", encoding="utf-8") as f:
                old_memory = json.load(f)

            # Count entries
            total_entries = sum(len(v) for v in old_memory.values() if isinstance(v, list))
            self.stats["memory_entries"] = total_entries

            # Merge with new memory
            if not self.dry_run:
                # Load existing memory
                current_memory = self.memory.langzeit

                # Merge categories
                for kategorie, entries in old_memory.items():
                    if kategorie not in current_memory:
                        current_memory[kategorie] = []

                    # Add entries (avoid duplicates)
                    for entry in entries:
                        if entry not in current_memory[kategorie]:
                            current_memory[kategorie].append(entry)

                # Save merged memory
                self.memory.langzeit = current_memory
                self.memory._save_langzeit()

            print(f"   ✅ Imported {total_entries} memory entries")

        except Exception as e:
            error_msg = f"Memory import failed: {e}"
            self.stats["errors"].append(error_msg)
            print(f"   ❌ {error_msg}")

    # ═══════════════════════════════════════════════════════════════════════════
    # HISTORY IMPORT
    # ═══════════════════════════════════════════════════════════════════════════

    def import_history(self):
        """Import chat history"""
        if not OLD_HISTORY_FILE.exists():
            print(f"   ⚠️ No history file found: {OLD_HISTORY_FILE}")
            return

        try:
            # Read old history
            with open(OLD_HISTORY_FILE, "r", encoding="utf-8") as f:
                old_history = json.load(f)

            if not isinstance(old_history, list):
                print(f"   ⚠️ Invalid history format")
                return

            self.stats["history_entries"] = len(old_history)

            # Import into new memory
            if not self.dry_run:
                for entry in old_history:
                    # Check if entry has new format
                    if "role" in entry and "content" in entry:
                        role = entry["role"]
                        content = entry["content"]
                        metadata = entry.get("metadata", {})

                        self.memory.add_to_history(role, content, metadata)

                    # Old format fallback
                    elif isinstance(entry, dict):
                        # Try to infer structure
                        role = "user" if entry.get("type") == "user" else "assistant"
                        content = entry.get("text", str(entry))

                        self.memory.add_to_history(role, content)

                # Save history
                self.memory.save_to_disk()

            print(f"   ✅ Imported {self.stats['history_entries']} history entries")

        except Exception as e:
            error_msg = f"History import failed: {e}"
            self.stats["errors"].append(error_msg)
            print(f"   ❌ {error_msg}")

    # ═══════════════════════════════════════════════════════════════════════════
    # VERIFICATION
    # ═══════════════════════════════════════════════════════════════════════════

    def verify_import(self) -> bool:
        """
        Verify that import was successful

        Returns:
            True if verification passed
        """
        issues = []

        # Check brain
        brain_stats = self.brain.stats()
        if brain_stats["total"] == 0:
            issues.append("No brain files imported")

        # Check memory
        if not MEMORY_FILE.exists():
            issues.append("Memory file not created")

        # Check history
        if not HISTORY_FILE.exists():
            issues.append("History file not created")

        # Report
        if issues:
            print("   ⚠️ Issues found:")
            for issue in issues:
                print(f"      - {issue}")
            return False
        else:
            print("   ✅ All checks passed")
            return True

    # ═══════════════════════════════════════════════════════════════════════════
    # STATS
    # ═══════════════════════════════════════════════════════════════════════════

    def _print_stats(self):
        """Print migration statistics"""
        print("\n" + "=" * 60)
        print("📊 MIGRATION STATISTICS")
        print("=" * 60)
        print(f"Brain files:     {self.stats['brain_files']}")
        print(f"Memory entries:  {self.stats['memory_entries']}")
        print(f"History entries: {self.stats['history_entries']}")
        print(f"Errors:          {len(self.stats['errors'])}")

        if self.stats['errors']:
            print("\n⚠️ Errors:")
            for error in self.stats['errors']:
                print(f"   - {error}")

        print("=" * 60)


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Import GENESIS data into M.O.L.O.C.H. 3.0")
    parser.add_argument("--dry-run", action="store_true", help="Dry run (no actual changes)")
    parser.add_argument("--old-dir", type=str, help="Old M.O.L.O.C.H. directory")
    args = parser.parse_args()

    # Run migration
    importer = GenesisImporter(
        old_moloch_dir=Path(args.old_dir) if args.old_dir else OLD_MOLOCH_DIR,
        dry_run=args.dry_run
    )

    success = importer.import_all()

    exit(0 if success else 1)
