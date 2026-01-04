#!/usr/bin/env python3
"""
M.O.L.O.C.H. 3.0 - Memory System
=================================
Chat History + Long-term Memory
FIXED: Vision Mode history saving!
"""

import json
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta

from core.config import HISTORY_FILE, MEMORY_FILE, CONTEXT_WINDOW, HISTORY_RETENTION_DAYS


class Memory:
    """
    M.O.L.O.C.H. Memory System

    Features:
    - Chat History (ALL modes: text, voice, vision)
    - Long-term Facts Storage
    - Context Window Management
    - Auto-cleanup of old history
    - Metadata tracking (mode, timestamp, stimmung, etc.)
    """

    def __init__(
        self,
        history_file: Path = HISTORY_FILE,
        memory_file: Path = MEMORY_FILE
    ):
        """
        Initialize Memory System

        Args:
            history_file: Path to history.json
            memory_file: Path to langzeit.json
        """
        self.history_file = Path(history_file)
        self.memory_file = Path(memory_file)

        self.history = self._load_history()
        self.langzeit = self._load_langzeit()

    # ═══════════════════════════════════════════════════════════════════════════
    # HISTORY (Chat History)
    # ═══════════════════════════════════════════════════════════════════════════

    def _load_history(self) -> List[Dict]:
        """Load chat history from file"""
        try:
            if self.history_file.exists():
                with open(self.history_file, "r", encoding="utf-8") as f:
                    return json.load(f)
        except Exception as e:
            print(f"⚠️ History load error: {e}")

        return []

    def _save_history(self):
        """Save chat history to file"""
        try:
            # Ensure parent directory exists
            self.history_file.parent.mkdir(parents=True, exist_ok=True)

            with open(self.history_file, "w", encoding="utf-8") as f:
                json.dump(self.history, f, ensure_ascii=False, indent=2)

        except Exception as e:
            print(f"❌ History save error: {e}")

    def add_to_history(
        self,
        role: str,
        content: str,
        metadata: Optional[Dict[str, Any]] = None
    ):
        """
        Add message to history

        Args:
            role: "user" or "assistant"
            content: Message content
            metadata: Optional metadata dict
                - mode: "text" | "voice" | "vision"
                - image_path: Path to image (if vision mode)
                - stimmung: Detected mood
                - tageszeit: Time of day mode
                - timestamp: ISO timestamp (auto-added if not present)

        Example:
            memory.add_to_history(
                role="user",
                content="Was siehst du?",
                metadata={
                    "mode": "vision",
                    "image_path": "~/moloch_3.0/data/auge.jpg",
                    "stimmung": "neutral",
                    "tageszeit": "dark_side_mode"
                }
            )
        """
        # Build entry
        entry = {
            "role": role,
            "content": content,
            "metadata": metadata or {}
        }

        # Add timestamp if not present
        if "timestamp" not in entry["metadata"]:
            entry["metadata"]["timestamp"] = datetime.now().isoformat()

        # Add to history
        self.history.append(entry)

    def get_context(self, last_n: int = CONTEXT_WINDOW) -> List[Dict]:
        """
        Get last N messages for API context

        Args:
            last_n: Number of recent messages to return

        Returns:
            List of message dicts for Claude API

        Note:
            Returns messages in Claude API format:
            [{"role": "user", "content": "..."}, ...]
            WITHOUT metadata (metadata is for internal tracking only)
        """
        # Get last N entries
        recent = self.history[-last_n:] if len(self.history) > last_n else self.history

        # Convert to API format (no metadata)
        context = []
        for entry in recent:
            context.append({
                "role": entry["role"],
                "content": entry["content"]
            })

        return context

    def get_full_history(self) -> List[Dict]:
        """Get full history (with metadata)"""
        return self.history

    def clear_history(self):
        """Clear all history"""
        self.history = []
        self._save_history()

    def cleanup_old_history(self, keep_days: int = HISTORY_RETENTION_DAYS):
        """
        Remove history older than keep_days

        Args:
            keep_days: Number of days to keep

        Note:
            Keeps entries marked as "important" in metadata
        """
        if not self.history:
            return

        cutoff_date = datetime.now() - timedelta(days=keep_days)

        # Filter: Keep recent OR important
        self.history = [
            entry for entry in self.history
            if self._should_keep_entry(entry, cutoff_date)
        ]

        self._save_history()

    def _should_keep_entry(self, entry: Dict, cutoff_date: datetime) -> bool:
        """Check if history entry should be kept"""
        metadata = entry.get("metadata", {})

        # Keep if marked important
        if metadata.get("important", False):
            return True

        # Keep if recent
        timestamp_str = metadata.get("timestamp", "")
        if timestamp_str:
            try:
                timestamp = datetime.fromisoformat(timestamp_str)
                return timestamp > cutoff_date
            except:
                pass

        # Keep by default if no timestamp
        return True

    # ═══════════════════════════════════════════════════════════════════════════
    # LANGZEIT (Long-term Memory)
    # ═══════════════════════════════════════════════════════════════════════════

    def _load_langzeit(self) -> Dict:
        """Load long-term memory from file"""
        try:
            if self.memory_file.exists():
                with open(self.memory_file, "r", encoding="utf-8") as f:
                    return json.load(f)
        except Exception as e:
            print(f"⚠️ Langzeit load error: {e}")

        return {
            "wichtig": [],
            "fakten": [],
            "personen": [],
            "orte": [],
            "vorlieben": [],
            "projekte": []
        }

    def _save_langzeit(self):
        """Save long-term memory to file"""
        try:
            # Ensure parent directory exists
            self.memory_file.parent.mkdir(parents=True, exist_ok=True)

            with open(self.memory_file, "w", encoding="utf-8") as f:
                json.dump(self.langzeit, f, ensure_ascii=False, indent=2)

        except Exception as e:
            print(f"❌ Langzeit save error: {e}")

    def add_to_langzeit(self, kategorie: str, inhalt: str):
        """
        Add to long-term memory

        Args:
            kategorie: Category (wichtig, fakten, personen, orte, vorlieben, projekte)
            inhalt: Content to remember

        Example:
            memory.add_to_langzeit("fakten", "M.O.L.O.C.H. geboren am 02.12.2025")
        """
        if kategorie not in self.langzeit:
            self.langzeit[kategorie] = []

        # Add with timestamp
        entry = {
            "content": inhalt,
            "added": datetime.now().isoformat()
        }

        # Avoid duplicates
        if entry not in self.langzeit[kategorie]:
            self.langzeit[kategorie].append(entry)

    def get_langzeit(self, kategorie: Optional[str] = None) -> Any:
        """
        Get long-term memory

        Args:
            kategorie: Optional category (returns all if None)

        Returns:
            Category content or all memory
        """
        if kategorie:
            return self.langzeit.get(kategorie, [])
        return self.langzeit

    def get_langzeit_context(self) -> str:
        """
        Get formatted long-term memory for system prompt

        Returns:
            Formatted context string
        """
        if not any(self.langzeit.values()):
            return ""

        lines = ["LANGZEIT-GEDÄCHTNIS:"]

        for kategorie, entries in self.langzeit.items():
            if entries:
                lines.append(f"\n{kategorie.upper()}:")
                for entry in entries:
                    content = entry.get("content") if isinstance(entry, dict) else entry
                    lines.append(f"- {content}")

        return "\n".join(lines)

    # ═══════════════════════════════════════════════════════════════════════════
    # SAVE ALL
    # ═══════════════════════════════════════════════════════════════════════════

    def save_to_disk(self):
        """Save both history and langzeit to disk"""
        self._save_history()
        self._save_langzeit()

    # ═══════════════════════════════════════════════════════════════════════════
    # STATS
    # ═══════════════════════════════════════════════════════════════════════════

    def stats(self) -> Dict[str, Any]:
        """
        Get memory statistics

        Returns:
            Stats dict
        """
        # Count by mode
        mode_counts = {"text": 0, "voice": 0, "vision": 0, "unknown": 0}
        for entry in self.history:
            mode = entry.get("metadata", {}).get("mode", "unknown")
            mode_counts[mode] = mode_counts.get(mode, 0) + 1

        # Count langzeit
        langzeit_counts = {
            kategorie: len(entries)
            for kategorie, entries in self.langzeit.items()
        }

        return {
            "total_messages": len(self.history),
            "by_mode": mode_counts,
            "langzeit": langzeit_counts
        }


# ═══════════════════════════════════════════════════════════════════════════════
# TESTING
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("\n💾 M.O.L.O.C.H. 3.0 Memory System Test\n")

    memory = Memory()

    # Test history
    print("📝 Testing history...")
    memory.add_to_history(
        role="user",
        content="Test message",
        metadata={"mode": "text", "stimmung": "neutral"}
    )
    print(f"   ✅ History: {len(memory.history)} entries")

    # Test vision history (THE FIX!)
    print("\n📸 Testing vision history (THE FIX!)...")
    memory.add_to_history(
        role="user",
        content="Was siehst du?",
        metadata={
            "mode": "vision",
            "image_path": "~/moloch_3.0/data/auge.jpg",
            "stimmung": "neutral"
        }
    )
    memory.add_to_history(
        role="assistant",
        content="Ich sehe...",
        metadata={"mode": "vision"}
    )
    print(f"   ✅ Vision history saved!")

    # Test context
    print("\n📖 Testing context...")
    context = memory.get_context(last_n=5)
    print(f"   ✅ Context: {len(context)} messages")

    # Test langzeit
    print("\n🧠 Testing langzeit...")
    memory.add_to_langzeit("fakten", "M.O.L.O.C.H. 3.0 geboren 04.01.2026")
    print(f"   ✅ Langzeit: {len(memory.langzeit['fakten'])} fakten")

    # Save
    print("\n💾 Saving to disk...")
    memory.save_to_disk()
    print(f"   ✅ Saved to {memory.history_file}")

    # Stats
    print("\n📊 Memory stats:")
    stats = memory.stats()
    print(f"   Total: {stats['total_messages']} messages")
    print(f"   By mode: {stats['by_mode']}")

    print()
