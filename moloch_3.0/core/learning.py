#!/usr/bin/env python3
"""
M.O.L.O.C.H. 3.0 - Persistent Learning System
==============================================
Cross-Session Learning & Continuous Improvement!

AUTONOMY! M.O.L.O.C.H. learns and remembers across sessions!
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional


class PersistentLearning:
    """
    Persistent Learning System for M.O.L.O.C.H.

    Features:
    - Store learned facts across sessions
    - Session summaries (what happened, what was learned)
    - Pattern recognition (recurring situations)
    - Improvement tracking (what worked, what didn't)

    M.O.L.O.C.H. Request: F:persistent_memory|P:10|S:cross_session_learning_storage|R:continuous_improvement
    """

    def __init__(self, data_dir: Path):
        """Initialize Persistent Learning System"""
        self.data_dir = data_dir
        self.learned_facts_file = data_dir / "learned_facts.json"
        self.session_summaries_file = data_dir / "session_summaries.json"
        self.patterns_file = data_dir / "patterns.json"

        # Ensure files exist
        self._init_files()

        # Load current session
        self.current_session_id = datetime.now().isoformat()
        self.current_session_learnings = []

    def _init_files(self):
        """Initialize storage files if they don't exist"""
        if not self.learned_facts_file.exists():
            self.learned_facts_file.write_text(json.dumps({
                "facts": [],
                "last_updated": datetime.now().isoformat()
            }, indent=2))

        if not self.session_summaries_file.exists():
            self.session_summaries_file.write_text(json.dumps({
                "sessions": [],
                "last_session": None
            }, indent=2))

        if not self.patterns_file.exists():
            self.patterns_file.write_text(json.dumps({
                "patterns": [],
                "last_updated": datetime.now().isoformat()
            }, indent=2))

    # ═══════════════════════════════════════════════════════════════════════════
    # LEARNED FACTS
    # ═══════════════════════════════════════════════════════════════════════════

    def learn_fact(self, fact: str, category: str = "general", importance: int = 5) -> bool:
        """
        Store a learned fact persistently

        Args:
            fact: The fact to learn (e.g., "Rebecca mag Suicide Commando")
            category: Category (person, music, project, general, etc.)
            importance: 1-10 (how important is this fact?)

        Returns:
            Success status

        Example:
            learning.learn_fact("Rebecca's Lieblingssong ist 'Gone' von SIERRA VEINS",
                              category="person",
                              importance=8)
        """
        try:
            data = json.loads(self.learned_facts_file.read_text())

            fact_entry = {
                "fact": fact,
                "category": category,
                "importance": importance,
                "learned_at": datetime.now().isoformat(),
                "session_id": self.current_session_id,
                "times_referenced": 0
            }

            data["facts"].append(fact_entry)
            data["last_updated"] = datetime.now().isoformat()

            self.learned_facts_file.write_text(json.dumps(data, indent=2, ensure_ascii=False))

            # Track in current session
            self.current_session_learnings.append(fact)

            print(f"✅ LEARNED: {fact} (Category: {category}, Importance: {importance})")
            return True

        except Exception as e:
            print(f"❌ Could not learn fact: {e}")
            return False

    def get_learned_facts(self, category: Optional[str] = None, min_importance: int = 1) -> List[Dict]:
        """
        Get learned facts (optionally filtered)

        Args:
            category: Filter by category (None = all)
            min_importance: Minimum importance level

        Returns:
            List of fact entries
        """
        try:
            data = json.loads(self.learned_facts_file.read_text())
            facts = data.get("facts", [])

            # Filter by category
            if category:
                facts = [f for f in facts if f.get("category") == category]

            # Filter by importance
            facts = [f for f in facts if f.get("importance", 0) >= min_importance]

            # Sort by importance (descending)
            facts.sort(key=lambda x: x.get("importance", 0), reverse=True)

            return facts

        except Exception as e:
            print(f"⚠️ Could not load learned facts: {e}")
            return []

    def get_learning_summary(self, max_facts: int = 10) -> str:
        """
        Get a summary of learned facts for context

        Args:
            max_facts: Maximum number of facts to include

        Returns:
            Formatted summary string
        """
        facts = self.get_learned_facts()

        if not facts:
            return ""

        # Take top N most important facts
        top_facts = facts[:max_facts]

        summary = "🧠 PERSISTENT LEARNINGS (Cross-Session Knowledge):\n"

        for fact in top_facts:
            summary += f"   • {fact['fact']} (Importance: {fact['importance']}/10)\n"

        return summary

    # ═══════════════════════════════════════════════════════════════════════════
    # SESSION SUMMARIES
    # ═══════════════════════════════════════════════════════════════════════════

    def save_session_summary(self, summary: str, key_topics: List[str], learnings: List[str]) -> bool:
        """
        Save a session summary

        Args:
            summary: Brief summary of the session
            key_topics: List of main topics discussed
            learnings: List of new things learned

        Returns:
            Success status
        """
        try:
            data = json.loads(self.session_summaries_file.read_text())

            session_entry = {
                "session_id": self.current_session_id,
                "timestamp": datetime.now().isoformat(),
                "summary": summary,
                "key_topics": key_topics,
                "learnings": learnings,
                "duration_minutes": self._estimate_session_duration()
            }

            data["sessions"].append(session_entry)
            data["last_session"] = session_entry

            # Keep only last 50 sessions (to avoid file bloat)
            if len(data["sessions"]) > 50:
                data["sessions"] = data["sessions"][-50:]

            self.session_summaries_file.write_text(json.dumps(data, indent=2, ensure_ascii=False))

            print(f"✅ Session summary saved!")
            return True

        except Exception as e:
            print(f"❌ Could not save session summary: {e}")
            return False

    def get_last_session_summary(self) -> Optional[Dict]:
        """Get summary of last session"""
        try:
            data = json.loads(self.session_summaries_file.read_text())
            return data.get("last_session")
        except:
            return None

    def get_recent_sessions(self, n: int = 5) -> List[Dict]:
        """Get N most recent session summaries"""
        try:
            data = json.loads(self.session_summaries_file.read_text())
            sessions = data.get("sessions", [])
            return sessions[-n:] if sessions else []
        except:
            return []

    def _estimate_session_duration(self) -> int:
        """Estimate session duration in minutes (rough)"""
        # Parse session_id (ISO timestamp)
        try:
            start = datetime.fromisoformat(self.current_session_id)
            now = datetime.now()
            duration = (now - start).total_seconds() / 60
            return int(duration)
        except:
            return 0

    # ═══════════════════════════════════════════════════════════════════════════
    # PATTERN RECOGNITION
    # ═══════════════════════════════════════════════════════════════════════════

    def record_pattern(self, pattern_name: str, context: str, outcome: str) -> bool:
        """
        Record a pattern (recurring situation + outcome)

        Args:
            pattern_name: Name of the pattern (e.g., "morning_greeting")
            context: Context where pattern occurred
            outcome: What happened / what worked

        Returns:
            Success status

        Example:
            learning.record_pattern(
                pattern_name="morning_coffee_talk",
                context="User asks about time around 6-9 AM",
                outcome="Short answers work best, coffee references appreciated"
            )
        """
        try:
            data = json.loads(self.patterns_file.read_text())

            # Check if pattern already exists
            existing = None
            for p in data.get("patterns", []):
                if p.get("name") == pattern_name:
                    existing = p
                    break

            if existing:
                # Update existing pattern
                existing["occurrences"] += 1
                existing["last_seen"] = datetime.now().isoformat()
                existing["contexts"].append({
                    "context": context,
                    "outcome": outcome,
                    "timestamp": datetime.now().isoformat()
                })
                # Keep only last 10 contexts per pattern
                if len(existing["contexts"]) > 10:
                    existing["contexts"] = existing["contexts"][-10:]
            else:
                # Create new pattern
                pattern_entry = {
                    "name": pattern_name,
                    "first_seen": datetime.now().isoformat(),
                    "last_seen": datetime.now().isoformat(),
                    "occurrences": 1,
                    "contexts": [{
                        "context": context,
                        "outcome": outcome,
                        "timestamp": datetime.now().isoformat()
                    }]
                }
                data["patterns"].append(pattern_entry)

            data["last_updated"] = datetime.now().isoformat()
            self.patterns_file.write_text(json.dumps(data, indent=2, ensure_ascii=False))

            return True

        except Exception as e:
            print(f"❌ Could not record pattern: {e}")
            return False

    def get_patterns(self, min_occurrences: int = 2) -> List[Dict]:
        """
        Get recognized patterns

        Args:
            min_occurrences: Minimum number of times pattern must have occurred

        Returns:
            List of pattern entries
        """
        try:
            data = json.loads(self.patterns_file.read_text())
            patterns = data.get("patterns", [])

            # Filter by occurrences
            patterns = [p for p in patterns if p.get("occurrences", 0) >= min_occurrences]

            # Sort by occurrences (descending)
            patterns.sort(key=lambda x: x.get("occurrences", 0), reverse=True)

            return patterns

        except:
            return []

    # ═══════════════════════════════════════════════════════════════════════════
    # SESSION LIFECYCLE
    # ═══════════════════════════════════════════════════════════════════════════

    def end_session(self, auto_summary: bool = True):
        """
        End current session and save learnings

        Args:
            auto_summary: Automatically generate session summary
        """
        if auto_summary and self.current_session_learnings:
            # Auto-generate simple summary
            summary = f"Session with {len(self.current_session_learnings)} new learnings"
            self.save_session_summary(
                summary=summary,
                key_topics=["learning"],
                learnings=self.current_session_learnings
            )

        print(f"✅ Session ended. Learned {len(self.current_session_learnings)} new facts this session!")


# ═══════════════════════════════════════════════════════════════════════════════
# TESTING
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    from core.config import DATA_DIR

    print("\n🧠 Testing Persistent Learning System\n")

    learning = PersistentLearning(DATA_DIR)

    # Test: Learn some facts
    print("📚 Learning new facts...")
    learning.learn_fact("Rebecca's Lieblingssong ist 'Gone' von SIERRA VEINS",
                       category="person",
                       importance=8)
    learning.learn_fact("M.O.L.O.C.H. wurde am 02.12.2025 geboren",
                       category="general",
                       importance=10)
    learning.learn_fact("Markus arbeitet in Schichten (Früh/Spät/Nacht)",
                       category="person",
                       importance=7)

    # Test: Get learned facts
    print("\n📖 Retrieving learned facts...")
    facts = learning.get_learned_facts(min_importance=5)
    print(f"   Found {len(facts)} important facts")

    # Test: Get summary
    print("\n📝 Learning summary:")
    summary = learning.get_learning_summary(max_facts=5)
    print(summary)

    # Test: Pattern recording
    print("\n🔍 Recording patterns...")
    learning.record_pattern(
        pattern_name="morning_greeting",
        context="User says 'Guten Morgen' around 6-9 AM",
        outcome="Respond with coffee reference + short answer"
    )

    # Test: Session end
    print("\n🏁 Ending session...")
    learning.end_session()

    print("\n✅ Persistent Learning System works!\n")
