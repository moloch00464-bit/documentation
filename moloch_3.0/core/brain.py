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

            # Save
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

            return True

        except Exception as e:
            print(f"❌ Brain save error ({kategorie}/{dateiname}): {e}")
            return False

    def read(self, kategorie: str, dateiname: str) -> Optional[Dict]:
        """
        Read from Brain Tree

        Args:
            kategorie: Category path
            dateiname: Filename

        Returns:
            Content dict or None

        Example:
            data = brain.read("wer/freunde", "rebecca.json")
        """
        try:
            file_path = self.brain_dir / kategorie / dateiname

            if not file_path.exists():
                return None

            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)

        except Exception as e:
            print(f"⚠️ Brain read error ({kategorie}/{dateiname}): {e}")
            return None

    def find(self, query: str, kategorie: Optional[str] = None) -> List[Dict]:
        """
        Search in Brain Tree

        Args:
            query: Search query (case-insensitive)
            kategorie: Optional category to search in (searches all if None)

        Returns:
            List of matching entries

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
                    with open(json_file, "r", encoding="utf-8") as f:
                        data = json.load(f)

                    # Search in content
                    content_str = json.dumps(data.get("content", {}), ensure_ascii=False).lower()
                    if query.lower() in content_str:
                        results.append({
                            "file": str(json_file.relative_to(self.brain_dir)),
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

            stats["total"] = sum(stats.values())

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
