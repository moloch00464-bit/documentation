#!/usr/bin/env python3
"""
M.O.L.O.C.H. 3.0 - Brain System
================================
Hierarchical Knowledge Storage (Brain Tree)
Migrated from GENESIS
"""

import json
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime

from core.config import BRAIN_DIR


class Brain:
    """
    M.O.L.O.C.H. Brain - Hierarchical Knowledge Storage

    Structure:
        brain/
        ├── wer/         # People (friends, colleagues, family)
        ├── was/         # Things (projects, music, hardware)
        ├── wo/          # Places (home, work, events)
        ├── wann/        # Dates & Milestones
        ├── wie/         # How-To's & Rules
        └── kontext/     # Current conversations context
    """

    def __init__(self, brain_dir: Path = BRAIN_DIR):
        """
        Initialize Brain

        Args:
            brain_dir: Path to brain directory
        """
        self.brain_dir = Path(brain_dir)
        self._ensure_structure()

    def _ensure_structure(self):
        """Ensures brain directory structure exists"""
        categories = ["wer", "was", "wo", "wann", "wie", "kontext"]
        for category in categories:
            (self.brain_dir / category).mkdir(parents=True, exist_ok=True)

    def _sanitize_filename(self, filename: str) -> str:
        """
        Sanitize filename to prevent security issues

        ROOT CAUSE: Path traversal and command injection via filenames
        FIX: Remove/replace dangerous characters

        Args:
            filename: Raw filename

        Returns:
            Sanitized filename
        """
        import re

        # Remove null bytes (critical security issue)
        filename = filename.replace('\x00', '')

        # Remove/replace dangerous characters
        dangerous_chars = {
            '\n': '_',  # Newline
            '\r': '_',  # Carriage return
            '\t': '_',  # Tab
            '|': '_',   # Pipe (command chaining)
            ';': '_',   # Semicolon (command chaining)
            '&': '_',   # Ampersand (background execution)
            '$': '_',   # Dollar (variable substitution)
            '`': '_',   # Backtick (command substitution)
            '<': '_',   # Redirect input
            '>': '_',   # Redirect output
            '*': '_',   # Wildcard
            '?': '_',   # Wildcard
            '"': '_',   # Quote
            "'": '_',   # Quote
            '\\': '_',  # Backslash (escape)
        }

        for char, replacement in dangerous_chars.items():
            filename = filename.replace(char, replacement)

        # Remove path traversal attempts
        # Replace ../ and ..\ with safe characters
        filename = filename.replace('../', '_')
        filename = filename.replace('..\\', '_')
        filename = filename.replace('..', '_')

        # Remove leading/trailing dots (hidden files, relative paths)
        filename = filename.strip('.')

        # Remove absolute path indicators
        if filename.startswith('/') or (len(filename) > 1 and filename[1] == ':'):
            # Starts with / or C:\ etc
            filename = filename.lstrip('/').replace(':', '')

        # Ensure filename is not empty after sanitization
        if not filename:
            filename = "sanitized_file.json"

        return filename

    def save(
        self,
        kategorie: str,
        inhalt: Dict[str, Any],
        dateiname: str,
        merge: bool = False
    ) -> bool:
        """
        Save to Brain Tree

        Args:
            kategorie: Category path (e.g., "wer/freunde", "was/musik")
            inhalt: Content to save (dict)
            dateiname: Filename (e.g., "rebecca.json")
            merge: If True, merge with existing data instead of overwrite

        Returns:
            Success status

        Example:
            brain.save("wer/freunde", {"name": "Rebecca", "sprache": "Klingonisch"}, "rebecca.json")
        """
        try:
            # Sanitize filename (SECURITY FIX)
            dateiname = self._sanitize_filename(dateiname)

            # Build full path
            category_path = self.brain_dir / kategorie
            category_path.mkdir(parents=True, exist_ok=True)

            file_path = category_path / dateiname

            # Add metadata
            data = {
                "content": inhalt,
                "metadata": {
                    "created": datetime.now().isoformat(),
                    "updated": datetime.now().isoformat(),
                    "category": kategorie,
                    "filename": dateiname
                }
            }

            # Merge with existing?
            if merge and file_path.exists():
                existing = self.read(kategorie, dateiname)
                if existing:
                    data["content"] = {**existing.get("content", {}), **inhalt}
                    data["metadata"]["created"] = existing.get("metadata", {}).get("created", data["metadata"]["created"])

            # Save atomically (BUG #3 FIX)
            # ROOT CAUSE: Direct write truncates file immediately, causing race conditions
            # FIX: Write to temp file, then atomic rename
            import os
            import tempfile

            # Write to temp file in same directory (required for atomic rename)
            temp_fd, temp_path = tempfile.mkstemp(
                dir=category_path,
                prefix=".tmp_",
                suffix=".json"
            )

            try:
                with os.fdopen(temp_fd, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                    f.flush()
                    os.fsync(f.fileno())  # Ensure written to disk

                # Atomic rename (POSIX guarantees atomicity)
                os.replace(temp_path, str(file_path))

            except Exception:
                # Cleanup temp file on error
                try:
                    os.unlink(temp_path)
                except:
                    pass
                raise

            return True

        except Exception as e:
            print(f"❌ Brain save error ({kategorie}/{dateiname}): {e}")
            return False

    def _normalize_data(self, data: Dict, kategorie: str, dateiname: str) -> Dict:
        """
        Normalize data to 3.0 format (backward compatible with 2.0)

        M.O.L.O.C.H. 2.0 Format:
            {"name": "Rebecca", "details": "..."}

        M.O.L.O.C.H. 3.0 Format:
            {
                "content": {"name": "Rebecca", "details": "..."},
                "metadata": {"created": "...", "updated": "...", ...}
            }

        Args:
            data: Raw data from JSON file
            kategorie: Category for metadata
            dateiname: Filename for metadata

        Returns:
            Data in 3.0 format
        """
        # Check if already in 3.0 format
        if "content" in data and "metadata" in data:
            return data

        # Convert 2.0 → 3.0 (in-memory only, don't modify file)
        return {
            "content": data,
            "metadata": {
                "created": "unknown",  # Can't know original creation time
                "updated": "unknown",
                "category": kategorie,
                "filename": dateiname,
                "migrated_from_2_0": True  # Flag for tracking
            }
        }

    def read(self, kategorie: str, dateiname: str) -> Optional[Dict]:
        """
        Read from Brain Tree (BACKWARD COMPATIBLE with 2.0)

        Args:
            kategorie: Category path
            dateiname: Filename

        Returns:
            Content dict in 3.0 format or None

        Example:
            data = brain.read("wer/freunde", "rebecca.json")

        Note:
            Automatically converts 2.0 data to 3.0 format in-memory
            (does not modify the original file)
        """
        try:
            # Sanitize filename (SECURITY FIX)
            dateiname = self._sanitize_filename(dateiname)

            file_path = self.brain_dir / kategorie / dateiname

            if not file_path.exists():
                return None

            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            # Normalize to 3.0 format (BACKWARD COMPATIBILITY)
            return self._normalize_data(data, kategorie, dateiname)

        except Exception as e:
            print(f"⚠️ Brain read error ({kategorie}/{dateiname}): {e}")
            return None

    def find(self, query: str, kategorie: Optional[str] = None) -> List[Dict]:
        """
        Search in Brain Tree (BACKWARD COMPATIBLE with 2.0)

        Args:
            query: Search query (case-insensitive)
            kategorie: Optional category to search in (searches all if None)

        Returns:
            List of matching entries in 3.0 format

        Example:
            results = brain.find("Sierra")  # Finds all mentions of Sierra
        """
        results = []

        try:
            # Determine search path
            search_path = self.brain_dir / kategorie if kategorie else self.brain_dir

            # Search all JSON files
            for json_file in search_path.rglob("*.json"):
                try:
                    # Read file (automatically normalizes 2.0 → 3.0)
                    relative_path = json_file.relative_to(self.brain_dir)
                    kategorie_path = str(relative_path.parent)
                    dateiname = relative_path.name

                    data = self.read(kategorie_path, dateiname)
                    if not data:
                        continue

                    # Search in content
                    content_str = json.dumps(data.get("content", {}), ensure_ascii=False).lower()
                    if query.lower() in content_str:
                        results.append({
                            "file": str(relative_path),
                            "data": data
                        })

                except Exception as e:
                    continue

        except Exception as e:
            print(f"⚠️ Brain search error: {e}")

        return results

    def link(self, von: str, nach: str, relation: str = "related") -> bool:
        """
        Create link between brain entries

        Args:
            von: Source entry path (e.g., "was/musik/sierra.json")
            nach: Target entry path (e.g., "wer/freunde/rebecca.json")
            relation: Relationship type

        Returns:
            Success status

        Example:
            brain.link("was/musik/sierra.json", "wo/events/wgt.json", "performs_at")
        """
        try:
            # Read source
            parts = von.split("/")
            source_category = "/".join(parts[:-1])
            source_file = parts[-1]
            source_data = self.read(source_category, source_file)

            if not source_data:
                return False

            # Add link
            if "links" not in source_data["content"]:
                source_data["content"]["links"] = []

            link_data = {
                "target": nach,
                "relation": relation,
                "created": datetime.now().isoformat()
            }

            # Avoid duplicates
            if link_data not in source_data["content"]["links"]:
                source_data["content"]["links"].append(link_data)

            # Save back
            return self.save(source_category, source_data["content"], source_file)

        except Exception as e:
            print(f"❌ Brain link error: {e}")
            return False

    def get_context(self, query: str, max_entries: int = 5) -> str:
        """
        Get relevant brain context for a query

        Args:
            query: User query
            max_entries: Max number of entries to return

        Returns:
            Formatted context string for system prompt

        Example:
            context = brain.get_context("Rebecca")
            # Returns: "BRAIN CONTEXT:\n- Rebecca: Beste Freundin, Klingonisch sprechen..."
        """
        results = self.find(query)

        if not results:
            return ""

        # Build context
        context_lines = ["BRAIN CONTEXT:"]

        for i, result in enumerate(results[:max_entries]):
            file_path = result["file"]
            content = result["data"].get("content", {})

            # Format entry
            entry_text = f"- {file_path}: {json.dumps(content, ensure_ascii=False)}"
            context_lines.append(entry_text)

        return "\n".join(context_lines)

    def list_category(self, kategorie: str) -> List[str]:
        """
        List all files in a category

        Args:
            kategorie: Category path

        Returns:
            List of filenames

        Example:
            files = brain.list_category("wer/freunde")
        """
        try:
            category_path = self.brain_dir / kategorie

            if not category_path.exists():
                return []

            return [f.name for f in category_path.glob("*.json")]

        except Exception as e:
            print(f"⚠️ Brain list error: {e}")
            return []

    def stats(self) -> Dict[str, int]:
        """
        Get brain statistics

        Returns:
            Stats dict with file counts per category
        """
        stats = {}

        try:
            for category in ["wer", "was", "wo", "wann", "wie", "kontext"]:
                count = len(list((self.brain_dir / category).rglob("*.json")))
                stats[category] = count

            total = sum(stats.values())
            stats["total"] = total  # For backwards compatibility (migration)
            stats["total_entries"] = total  # For health check and new code
            stats["categories"] = list(stats.keys())  # Category list

        except Exception as e:
            print(f"⚠️ Brain stats error: {e}")

        return stats


# ═══════════════════════════════════════════════════════════════════════════════
# TESTING
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("\n🧠 M.O.L.O.C.H. 3.0 Brain System Test\n")

    brain = Brain()

    # Test save
    print("📝 Testing save...")
    success = brain.save(
        kategorie="wer/freunde",
        inhalt={
            "name": "Rebecca",
            "relation": "Beste Freundin",
            "sprache": "Klingonisch",
            "special": "Qapla!"
        },
        dateiname="rebecca.json"
    )
    print(f"   {'✅' if success else '❌'} Save: {success}")

    # Test read
    print("\n📖 Testing read...")
    data = brain.read("wer/freunde", "rebecca.json")
    if data:
        print(f"   ✅ Read: {data['content']['name']}")
    else:
        print(f"   ❌ Read failed")

    # Test find
    print("\n🔍 Testing find...")
    results = brain.find("Rebecca")
    print(f"   ✅ Found {len(results)} entries")

    # Test stats
    print("\n📊 Brain stats:")
    stats = brain.stats()
    for category, count in stats.items():
        print(f"   {category}: {count} files")

    print()
