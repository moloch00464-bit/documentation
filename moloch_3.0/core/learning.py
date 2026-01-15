#!/usr/bin/env python3
"""M.O.L.O.C.H. 3.1 - Persistent Learning"""

import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional


class PersistentLearning:
    """Cross-session learning and fact retention"""

    def __init__(self, data_dir):
        self.data_dir = data_dir
        self.learning_file = data_dir / "learnings.json"
        self.learnings = self._load_learnings()

    def _load_learnings(self) -> Dict:
        """Load learnings from disk"""
        if self.learning_file.exists():
            try:
                with open(self.learning_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                pass

        return {
            "facts": [],
            "sessions": []
        }

    def _save_learnings(self):
        """Save learnings to disk"""
        try:
            with open(self.learning_file, 'w', encoding='utf-8') as f:
                json.dump(self.learnings, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"⚠️  Failed to save learnings: {e}")

    def add_fact(self, fact: str, category: str, importance: int = 5):
        """Add a new learned fact"""
        entry = {
            "fact": fact,
            "category": category,
            "importance": importance,
            "learned_at": datetime.now().isoformat()
        }

        self.learnings["facts"].append(entry)
        self._save_learnings()

    def get_learned_facts(self, min_importance: int = 5) -> List[Dict]:
        """Get learned facts above importance threshold"""
        return [
            f for f in self.learnings["facts"]
            if f.get("importance", 0) >= min_importance
        ]

    def get_learning_summary(self, max_facts: int = 10) -> str:
        """Get learning summary for prompt"""
        facts = sorted(
            self.learnings["facts"],
            key=lambda x: x.get("importance", 0),
            reverse=True
        )[:max_facts]

        if not facts:
            return ""

        lines = ["💾 PERSISTENT LEARNINGS:"]
        for f in facts:
            lines.append(f"- [{f['category']}] {f['fact']}")

        return "\n".join(lines)

    def end_session(self, auto_summary: bool = True):
        """End current session"""
        session = {
            "ended_at": datetime.now().isoformat(),
            "facts_count": len(self.learnings["facts"])
        }

        self.learnings["sessions"].append(session)
        self._save_learnings()
