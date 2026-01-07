#!/usr/bin/env python3
"""M.O.L.O.C.H. 3.1 - Brain System"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Optional, List
from core.config import BRAIN_DIR


class Brain:
    """Persistent knowledge storage"""

    def __init__(self):
        self.brain_dir = BRAIN_DIR
        self.brain_dir.mkdir(parents=True, exist_ok=True)

    def save(self, category: str, content: Dict, filename: Optional[str] = None):
        """Save entry to brain"""
        # Create category directory
        cat_dir = self.brain_dir / category
        cat_dir.mkdir(parents=True, exist_ok=True)

        # Generate filename if not provided
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"entry_{timestamp}.json"

        file_path = cat_dir / filename

        # Add metadata
        content["_brain_metadata"] = {
            "saved_at": datetime.now().isoformat(),
            "category": category
        }

        # Save
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(content, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"❌ Brain save failed: {e}")
            return False

    def load(self, category: str, search_term: Optional[str] = None) -> List[Dict]:
        """Load entries from brain"""
        cat_dir = self.brain_dir / category

        if not cat_dir.exists():
            return []

        results = []
        for file_path in cat_dir.glob("*.json"):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)

                # Search filter
                if search_term:
                    content_str = json.dumps(data, ensure_ascii=False).lower()
                    if search_term.lower() not in content_str:
                        continue

                results.append(data)
            except Exception as e:
                print(f"⚠️  Failed to load {file_path}: {e}")

        return results

    def get_context(self, query: str, max_entries: int = 3) -> str:
        """Get relevant context from brain"""
        # Search across all categories
        all_entries = []
        for cat_dir in self.brain_dir.iterdir():
            if cat_dir.is_dir():
                entries = self.load(cat_dir.name, query)
                all_entries.extend(entries)

        if not all_entries:
            return ""

        # Format for prompt
        lines = ["🧠 BRAIN CONTEXT:"]
        for entry in all_entries[:max_entries]:
            # Extract key information
            if "user_input" in entry:
                lines.append(f"- Q: {entry['user_input'][:100]}")
            if "response" in entry:
                lines.append(f"  A: {entry['response'][:100]}")

        return "\n".join(lines)
