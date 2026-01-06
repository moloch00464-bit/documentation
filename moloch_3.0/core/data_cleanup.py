#!/usr/bin/env python3
"""
M.O.L.O.C.H. 3.0 - Data Cleanup System
=======================================
⚠️ DEFAULT: CLEANUP DEAKTIVIERT!

M.O.L.O.C.H. soll sich ALLES merken (Langzeitgedächtnis)!

Dieses Tool ist NUR für:
- Manuelle Bereinigung bei Speicherproblemen
- File Size Monitoring (Warnung bei >1GB)
- Dry-Run Tests

NIEMALS automatisch ausführen!
"""

import json
import os
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List

from core.config import DATA_DIR, HISTORY_FILE, MEMORY_FILE, TIMELINE_FILE


class DataCleaner:
    """
    Data Cleanup System

    Features:
    - Auto-cleanup old history (keep last N days)
    - Auto-cleanup timeline (keep last N days)
    - Brain Tree pruning (remove empty nodes)
    - Max size limits
    """

    def __init__(self, config: Dict = None):
        """
        Initialize Data Cleaner

        ⚠️ DEFAULT: CLEANUP DISABLED!
        M.O.L.O.C.H. soll sich ALLES merken (Langzeitgedächtnis)!

        Cleanup nur auf explizite Anforderung (dry_run zum Testen)

        Args:
            config: Optional cleanup configuration
        """
        self.config = config or {
            # History cleanup - DEFAULT: DISABLED (infinite memory!)
            "history_keep_days": 999999,  # Praktisch unendlich
            "history_max_entries": 999999,  # Praktisch unendlich

            # Timeline cleanup - DEFAULT: DISABLED
            "timeline_keep_days": 999999,  # Praktisch unendlich
            "timeline_max_entries": 999999,  # Praktisch unendlich

            # Brain cleanup - DEFAULT: DISABLED
            "brain_prune_empty": False,  # KEINE Auto-Löschung!
            "brain_max_files_per_category": 999999,  # Praktisch unendlich

            # File size limits - NUR WARNUNG, KEINE AUTO-LÖSCHUNG
            "max_history_size_mb": 1000,  # 1GB Warnung
            "max_memory_size_mb": 1000,  # 1GB Warnung
            "max_timeline_size_mb": 1000,  # 1GB Warnung
        }

    # ═══════════════════════════════════════════════════════════════════════════
    # CLEANUP OPERATIONS
    # ═══════════════════════════════════════════════════════════════════════════

    def cleanup_all(self, dry_run: bool = False) -> Dict[str, int]:
        """
        Run all cleanup operations

        Args:
            dry_run: If True, don't actually delete (just report)

        Returns:
            Stats: {"history_deleted": N, "timeline_deleted": M, ...}
        """
        stats = {
            "history_deleted": 0,
            "timeline_deleted": 0,
            "brain_pruned": 0
        }

        print("\n🧹 M.O.L.O.C.H. Data Cleanup")
        if dry_run:
            print("   (DRY RUN - keine echten Änderungen)")
        print()

        # Cleanup history
        stats["history_deleted"] = self.cleanup_history(dry_run=dry_run)

        # Cleanup timeline
        stats["timeline_deleted"] = self.cleanup_timeline(dry_run=dry_run)

        # Cleanup brain
        stats["brain_pruned"] = self.cleanup_brain(dry_run=dry_run)

        # Print summary
        print("\n" + "="*60)
        print("📊 CLEANUP SUMMARY")
        print("="*60)
        print(f"History entries deleted:  {stats['history_deleted']}")
        print(f"Timeline events deleted:  {stats['timeline_deleted']}")
        print(f"Brain nodes pruned:       {stats['brain_pruned']}")
        print("="*60 + "\n")

        return stats

    # ═══════════════════════════════════════════════════════════════════════════
    # HISTORY CLEANUP
    # ═══════════════════════════════════════════════════════════════════════════

    def cleanup_history(self, dry_run: bool = False) -> int:
        """
        Cleanup old history entries

        Args:
            dry_run: If True, don't actually delete

        Returns:
            Number of deleted entries
        """
        print("📜 Cleaning up history...")

        if not HISTORY_FILE.exists():
            print("   ⚠️ No history file found")
            return 0

        try:
            # Load history
            with open(HISTORY_FILE, "r") as f:
                history = json.load(f)

            if not isinstance(history, list):
                print("   ⚠️ Invalid history format")
                return 0

            original_count = len(history)

            # Filter by date
            cutoff_date = datetime.now() - timedelta(days=self.config["history_keep_days"])
            cutoff_timestamp = cutoff_date.timestamp()

            filtered_history = []
            for entry in history:
                # Keep if timestamp is recent
                timestamp = entry.get("metadata", {}).get("timestamp", 0)
                if isinstance(timestamp, str):
                    # Parse ISO format timestamp
                    try:
                        timestamp = datetime.fromisoformat(timestamp).timestamp()
                    except:
                        timestamp = 0

                if timestamp >= cutoff_timestamp:
                    filtered_history.append(entry)

            # Also enforce max entries limit
            if len(filtered_history) > self.config["history_max_entries"]:
                # Keep only most recent entries
                filtered_history = filtered_history[-self.config["history_max_entries"]:]

            deleted_count = original_count - len(filtered_history)

            if deleted_count > 0:
                print(f"   🗑️  Deleting {deleted_count} old entries (keeping {len(filtered_history)})")

                if not dry_run:
                    # Backup first
                    self._backup_file(HISTORY_FILE)

                    # Save cleaned history
                    with open(HISTORY_FILE, "w") as f:
                        json.dump(filtered_history, f, indent=2)

                    print(f"   ✅ History cleaned")
            else:
                print(f"   ✅ No cleanup needed ({len(history)} entries)")

            return deleted_count

        except Exception as e:
            print(f"   ❌ Cleanup failed: {e}")
            return 0

    # ═══════════════════════════════════════════════════════════════════════════
    # TIMELINE CLEANUP
    # ═══════════════════════════════════════════════════════════════════════════

    def cleanup_timeline(self, dry_run: bool = False) -> int:
        """
        Cleanup old timeline events

        Args:
            dry_run: If True, don't actually delete

        Returns:
            Number of deleted events
        """
        print("\n⏰ Cleaning up timeline...")

        if not TIMELINE_FILE.exists():
            print("   ⚠️ No timeline file found")
            return 0

        try:
            # Load timeline
            with open(TIMELINE_FILE, "r") as f:
                timeline = json.load(f)

            if not isinstance(timeline, list):
                print("   ⚠️ Invalid timeline format")
                return 0

            original_count = len(timeline)

            # Filter by date
            cutoff_date = datetime.now() - timedelta(days=self.config["timeline_keep_days"])
            cutoff_timestamp = cutoff_date.timestamp()

            filtered_timeline = []
            for event in timeline:
                timestamp = event.get("timestamp", 0)
                if isinstance(timestamp, str):
                    try:
                        timestamp = datetime.fromisoformat(timestamp).timestamp()
                    except:
                        timestamp = 0

                if timestamp >= cutoff_timestamp:
                    filtered_timeline.append(event)

            # Enforce max entries
            if len(filtered_timeline) > self.config["timeline_max_entries"]:
                filtered_timeline = filtered_timeline[-self.config["timeline_max_entries"]:]

            deleted_count = original_count - len(filtered_timeline)

            if deleted_count > 0:
                print(f"   🗑️  Deleting {deleted_count} old events (keeping {len(filtered_timeline)})")

                if not dry_run:
                    self._backup_file(TIMELINE_FILE)

                    with open(TIMELINE_FILE, "w") as f:
                        json.dump(filtered_timeline, f, indent=2)

                    print(f"   ✅ Timeline cleaned")
            else:
                print(f"   ✅ No cleanup needed ({len(timeline)} events)")

            return deleted_count

        except Exception as e:
            print(f"   ❌ Cleanup failed: {e}")
            return 0

    # ═══════════════════════════════════════════════════════════════════════════
    # BRAIN CLEANUP
    # ═══════════════════════════════════════════════════════════════════════════

    def cleanup_brain(self, dry_run: bool = False) -> int:
        """
        Cleanup brain tree (remove empty nodes)

        Args:
            dry_run: If True, don't actually delete

        Returns:
            Number of pruned nodes
        """
        print("\n🧠 Cleaning up brain...")

        from core.brain import Brain
        brain = Brain()

        pruned = 0

        # TODO: Implement brain pruning
        # For now, just report
        print(f"   ✅ Brain OK (pruning not yet implemented)")

        return pruned

    # ═══════════════════════════════════════════════════════════════════════════
    # FILE SIZE CHECKS
    # ═══════════════════════════════════════════════════════════════════════════

    def check_file_sizes(self) -> Dict[str, float]:
        """
        Check file sizes and warn if too large

        Returns:
            Dict of file sizes in MB
        """
        print("\n📊 Checking file sizes...")

        sizes = {}
        warnings = []

        files_to_check = [
            (HISTORY_FILE, "history", self.config["max_history_size_mb"]),
            (MEMORY_FILE, "memory", self.config["max_memory_size_mb"]),
            (TIMELINE_FILE, "timeline", self.config["max_timeline_size_mb"]),
        ]

        for file_path, name, max_size in files_to_check:
            if file_path.exists():
                size_mb = file_path.stat().st_size / (1024 * 1024)
                sizes[name] = size_mb

                if size_mb > max_size:
                    warnings.append(f"⚠️  {name}.json: {size_mb:.2f}MB (Max: {max_size}MB)")
                else:
                    print(f"   ✅ {name}.json: {size_mb:.2f}MB")

        if warnings:
            print("\n⚠️  SIZE WARNINGS:")
            for warning in warnings:
                print(f"   {warning}")
            print("   Run cleanup to reduce file sizes!")

        return sizes

    # ═══════════════════════════════════════════════════════════════════════════
    # HELPERS
    # ═══════════════════════════════════════════════════════════════════════════

    def _backup_file(self, file_path: Path):
        """Backup file before modification"""
        import shutil

        backup_path = file_path.parent / f"{file_path.name}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        try:
            shutil.copy2(file_path, backup_path)
            print(f"   💾 Backup: {backup_path.name}")
        except Exception as e:
            print(f"   ⚠️ Backup failed: {e}")


# ═══════════════════════════════════════════════════════════════════════════════
# AUTO-CLEANUP SCHEDULER
# ═══════════════════════════════════════════════════════════════════════════════

def should_run_cleanup() -> bool:
    """
    ⚠️ DEAKTIVIERT!

    Auto-Cleanup ist DISABLED - M.O.L.O.C.H. soll sich ALLES merken!

    Returns:
        False (always - no automatic cleanup!)
    """
    # NIEMALS automatisch cleanen!
    return False


def mark_cleanup_done():
    """Mark cleanup as done (update timestamp)"""
    cleanup_marker = DATA_DIR / ".last_cleanup"

    try:
        with open(cleanup_marker, "w") as f:
            f.write(str(datetime.now().timestamp()))
    except:
        pass


# ═══════════════════════════════════════════════════════════════════════════════
# TESTING
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("\n🧹 M.O.L.O.C.H. 3.0 Data Cleanup Test\n")

    cleaner = DataCleaner()

    # Check file sizes
    cleaner.check_file_sizes()

    # Dry run cleanup
    print("\n" + "="*60)
    cleaner.cleanup_all(dry_run=True)

    print("✅ Data Cleanup test complete\n")
