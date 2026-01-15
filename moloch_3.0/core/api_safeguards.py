#!/usr/bin/env python3
"""M.O.L.O.C.H. 3.1 - API Safeguards"""

import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import Tuple
from core.config import DATA_DIR, MAX_CLAUDE_CALLS_PER_HOUR, MAX_VISION_CALLS_PER_HOUR, DAILY_BUDGET


class APIGuard:
    """API rate limiting and budget tracking"""

    def __init__(self):
        self.data_dir = DATA_DIR
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.stats_file = self.data_dir / "api_stats.json"

        # Load stats
        self.stats = self._load_stats()

    def _load_stats(self):
        """Load API stats"""
        if self.stats_file.exists():
            try:
                with open(self.stats_file, 'r') as f:
                    return json.load(f)
            except:
                pass

        return {
            "claude_calls": [],
            "vision_calls": [],
            "daily_spend": {}
        }

    def _save_stats(self):
        """Save API stats"""
        try:
            with open(self.stats_file, 'w') as f:
                json.dump(self.stats, f, indent=2)
        except Exception as e:
            print(f"⚠️  Failed to save API stats: {e}")

    def _clean_old_entries(self):
        """Remove old entries"""
        now = datetime.now()
        cutoff = now - timedelta(hours=1)

        # Clean claude calls
        self.stats["claude_calls"] = [
            call for call in self.stats["claude_calls"]
            if datetime.fromisoformat(call["timestamp"]) > cutoff
        ]

        # Clean vision calls
        self.stats["vision_calls"] = [
            call for call in self.stats["vision_calls"]
            if datetime.fromisoformat(call["timestamp"]) > cutoff
        ]

    def can_call_claude(self) -> Tuple[bool, str]:
        """Check if Claude API call is allowed"""
        self._clean_old_entries()

        calls_last_hour = len(self.stats["claude_calls"])

        if calls_last_hour >= MAX_CLAUDE_CALLS_PER_HOUR:
            return False, f"Rate limit: {calls_last_hour}/{MAX_CLAUDE_CALLS_PER_HOUR} calls/hour"

        return True, "OK"

    def can_call_vision(self) -> Tuple[bool, str]:
        """Check if Vision API call is allowed"""
        self._clean_old_entries()

        calls_last_hour = len(self.stats["vision_calls"])

        if calls_last_hour >= MAX_VISION_CALLS_PER_HOUR:
            return False, f"Rate limit: {calls_last_hour}/{MAX_VISION_CALLS_PER_HOUR} calls/hour"

        return True, "OK"

    def record_claude_call(self, input_tokens: int = 0, output_tokens: int = 0):
        """Record a Claude API call"""
        self.stats["claude_calls"].append({
            "timestamp": datetime.now().isoformat(),
            "input_tokens": input_tokens,
            "output_tokens": output_tokens
        })
        self._save_stats()

    def record_vision_call(self):
        """Record a Vision API call"""
        self.stats["vision_calls"].append({
            "timestamp": datetime.now().isoformat()
        })
        self._save_stats()


# Global singleton
_guard = None


def get_api_guard() -> APIGuard:
    """Get global API guard instance"""
    global _guard
    if _guard is None:
        _guard = APIGuard()
    return _guard
