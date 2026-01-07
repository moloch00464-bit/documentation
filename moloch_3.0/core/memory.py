#!/usr/bin/env python3
"""M.O.L.O.C.H. 3.1 - Memory System"""

import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional
from core.config import DATA_DIR


class Memory:
    """Short-term and long-term memory management"""

    def __init__(self):
        self.data_dir = DATA_DIR
        self.data_dir.mkdir(parents=True, exist_ok=True)

        self.history_file = self.data_dir / "history.json"
        self.langzeit_file = self.data_dir / "langzeit.json"

        # Load history
        self.history = self._load_json(self.history_file, [])
        self.langzeit = self._load_json(self.langzeit_file, {})

        # Session start time
        self.session_start = datetime.now()

    def _load_json(self, file_path: Path, default):
        """Load JSON file"""
        if file_path.exists():
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"⚠️  Failed to load {file_path.name}: {e}")
                return default
        return default

    def _save_json(self, file_path: Path, data):
        """Save JSON file"""
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"⚠️  Failed to save {file_path.name}: {e}")

    def add_to_history(self, role: str, content: str, metadata: Optional[Dict] = None):
        """Add message to history"""
        entry = {
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        }
        if metadata:
            entry["metadata"] = metadata

        self.history.append(entry)

    def get_context(self, last_n: int = 5) -> List[Dict]:
        """Get recent conversation context"""
        recent = self.history[-last_n * 2:] if len(self.history) > last_n * 2 else self.history

        # Convert to Claude API format
        messages = []
        for entry in recent:
            messages.append({
                "role": entry["role"],
                "content": entry["content"]
            })

        return messages

    def get_langzeit_context(self) -> str:
        """Get long-term memory context"""
        if not self.langzeit:
            return ""

        lines = ["🧠 LANGZEITGEDÄCHTNIS:"]
        for key, value in list(self.langzeit.items())[:10]:
            lines.append(f"- {key}: {value}")

        return "\n".join(lines)

    def get_zeit_stats(self) -> Dict:
        """Get time statistics"""
        now = datetime.now()
        session_duration = (now - self.session_start).total_seconds() / 60  # minutes

        stats_text = f"⏱️ Session: {session_duration:.0f} min"

        return {
            "session_duration_minutes": session_duration,
            "formatted_text": stats_text
        }

    def save_to_disk(self):
        """Save memory to disk"""
        self._save_json(self.history_file, self.history)
        self._save_json(self.langzeit_file, self.langzeit)
