#!/usr/bin/env python3
"""
M.O.L.O.C.H. 3.0 - API Safeguards
==================================
Rate Limiting, Cost Tracking, Error Recovery

CRITICAL: Prevents API cost explosion!
"""

import time
import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional, Dict
from dataclasses import dataclass, asdict

from core.config import DATA_DIR


# API Limits Configuration
@dataclass
class APILimits:
    """API Call Limits"""
    # Whisper API (Voice Input)
    whisper_max_per_hour: int = 60  # Max 60 voice inputs/hour
    whisper_max_per_day: int = 200  # Max 200 voice inputs/day
    whisper_cost_per_call: float = 0.006  # $0.006 per minute (~20s = $0.002)

    # Claude API (Text)
    claude_max_per_hour: int = 100  # Max 100 chat calls/hour
    claude_max_per_day: int = 500   # Max 500 chat calls/day
    claude_cost_per_1k_tokens: float = 0.003  # Sonnet 4 input

    # Claude Vision API
    vision_max_per_hour: int = 30   # Max 30 vision calls/hour (expensive!)
    vision_max_per_day: int = 100   # Max 100 vision calls/day
    vision_cost_per_call: float = 0.048  # ~$0.048 per image (1600 tokens)

    # Total Daily Budget
    max_daily_cost_usd: float = 10.0  # Max $10/day total (erhöht für mehr Spielraum!)


@dataclass
class APIStats:
    """API Usage Statistics"""
    # Counters
    whisper_calls_today: int = 0
    whisper_calls_hour: int = 0
    claude_calls_today: int = 0
    claude_calls_hour: int = 0
    vision_calls_today: int = 0
    vision_calls_hour: int = 0

    # Cost tracking
    total_cost_today: float = 0.0
    whisper_cost_today: float = 0.0
    claude_cost_today: float = 0.0
    vision_cost_today: float = 0.0

    # Timestamps
    last_reset_date: str = ""
    last_reset_hour: str = ""
    last_whisper_call: float = 0.0
    last_claude_call: float = 0.0
    last_vision_call: float = 0.0


class APIGuard:
    """
    API Safeguards System

    Features:
    - Rate Limiting (per hour, per day)
    - Cost Tracking (real-time budget monitoring)
    - Auto-reset (hourly, daily)
    - Retry Logic with Exponential Backoff
    - Emergency Shutdown (if limits exceeded)
    """

    def __init__(self, limits: APILimits = None):
        """
        Initialize API Guard

        Args:
            limits: Custom API limits (defaults to APILimits())
        """
        self.limits = limits or APILimits()
        self.stats_file = DATA_DIR / "api_stats.json"

        # Load or create stats
        self.stats = self._load_stats()

        # Auto-reset if needed
        self._auto_reset()

    # ═══════════════════════════════════════════════════════════════════════════
    # RATE LIMITING CHECKS
    # ═══════════════════════════════════════════════════════════════════════════

    def can_call_whisper(self) -> tuple[bool, str]:
        """
        Check if Whisper API call is allowed

        Returns:
            (allowed, reason)
        """
        self._auto_reset()

        # Check daily budget
        if self.stats.total_cost_today >= self.limits.max_daily_cost_usd:
            return False, f"💰 Daily budget exceeded (${self.stats.total_cost_today:.2f}/${self.limits.max_daily_cost_usd})"

        # Check hourly limit
        if self.stats.whisper_calls_hour >= self.limits.whisper_max_per_hour:
            return False, f"⏰ Whisper hourly limit ({self.limits.whisper_max_per_hour}/h)"

        # Check daily limit
        if self.stats.whisper_calls_today >= self.limits.whisper_max_per_day:
            return False, f"📅 Whisper daily limit ({self.limits.whisper_max_per_day}/day)"

        return True, "OK"

    def can_call_claude(self) -> tuple[bool, str]:
        """Check if Claude API call is allowed"""
        self._auto_reset()

        if self.stats.total_cost_today >= self.limits.max_daily_cost_usd:
            return False, f"💰 Daily budget exceeded"

        if self.stats.claude_calls_hour >= self.limits.claude_max_per_hour:
            return False, f"⏰ Claude hourly limit ({self.limits.claude_max_per_hour}/h)"

        if self.stats.claude_calls_today >= self.limits.claude_max_per_day:
            return False, f"📅 Claude daily limit ({self.limits.claude_max_per_day}/day)"

        return True, "OK"

    def can_call_vision(self) -> tuple[bool, str]:
        """Check if Vision API call is allowed"""
        self._auto_reset()

        if self.stats.total_cost_today >= self.limits.max_daily_cost_usd:
            return False, f"💰 Daily budget exceeded"

        if self.stats.vision_calls_hour >= self.limits.vision_max_per_hour:
            return False, f"⏰ Vision hourly limit ({self.limits.vision_max_per_hour}/h)"

        if self.stats.vision_calls_today >= self.limits.vision_max_per_day:
            return False, f"📅 Vision daily limit ({self.limits.vision_max_per_day}/day)"

        return True, "OK"

    # ═══════════════════════════════════════════════════════════════════════════
    # RECORDING API CALLS
    # ═══════════════════════════════════════════════════════════════════════════

    def record_whisper_call(self, duration_seconds: int = 20):
        """
        Record a Whisper API call

        Args:
            duration_seconds: Audio duration in seconds
        """
        cost = (duration_seconds / 60.0) * self.limits.whisper_cost_per_call

        self.stats.whisper_calls_today += 1
        self.stats.whisper_calls_hour += 1
        self.stats.whisper_cost_today += cost
        self.stats.total_cost_today += cost
        self.stats.last_whisper_call = time.time()

        self._save_stats()

    def record_claude_call(self, input_tokens: int = 1000, output_tokens: int = 500):
        """
        Record a Claude API call

        Args:
            input_tokens: Number of input tokens
            output_tokens: Number of output tokens
        """
        # Sonnet 4: $3/MTok input, $15/MTok output
        cost_input = (input_tokens / 1000.0) * self.limits.claude_cost_per_1k_tokens
        cost_output = (output_tokens / 1000.0) * (self.limits.claude_cost_per_1k_tokens * 5)
        cost = cost_input + cost_output

        self.stats.claude_calls_today += 1
        self.stats.claude_calls_hour += 1
        self.stats.claude_cost_today += cost
        self.stats.total_cost_today += cost
        self.stats.last_claude_call = time.time()

        self._save_stats()

    def record_vision_call(self, image_tokens: int = 1600):
        """
        Record a Vision API call

        Args:
            image_tokens: Number of image tokens (default ~1600 for typical image)
        """
        cost = self.limits.vision_cost_per_call

        self.stats.vision_calls_today += 1
        self.stats.vision_calls_hour += 1
        self.stats.vision_cost_today += cost
        self.stats.total_cost_today += cost
        self.stats.last_vision_call = time.time()

        self._save_stats()

    # ═══════════════════════════════════════════════════════════════════════════
    # AUTO-RESET
    # ═══════════════════════════════════════════════════════════════════════════

    def _auto_reset(self):
        """Auto-reset counters (hourly/daily)"""
        now = datetime.now()

        # Daily reset
        today = now.strftime("%Y-%m-%d")
        if self.stats.last_reset_date != today:
            self._reset_daily()
            self.stats.last_reset_date = today

        # Hourly reset
        current_hour = now.strftime("%Y-%m-%d %H:00")
        if self.stats.last_reset_hour != current_hour:
            self._reset_hourly()
            self.stats.last_reset_hour = current_hour

    def _reset_daily(self):
        """Reset daily counters"""
        print(f"\n📊 Daily API Stats Reset")
        print(f"   Total Cost Yesterday: ${self.stats.total_cost_today:.2f}")

        self.stats.whisper_calls_today = 0
        self.stats.claude_calls_today = 0
        self.stats.vision_calls_today = 0
        self.stats.total_cost_today = 0.0
        self.stats.whisper_cost_today = 0.0
        self.stats.claude_cost_today = 0.0
        self.stats.vision_cost_today = 0.0

        self._save_stats()

    def manual_reset(self):
        """
        Manual reset of API counters

        WICHTIG: Nur für Notfälle oder zum Testen!
        Normal wird automatisch um Mitternacht resettet.
        """
        print("\n⚠️  MANUELLER API RESET")
        print(f"   Aktuelle Kosten heute: ${self.stats.total_cost_today:.2f}")
        print(f"   Whisper Calls: {self.stats.whisper_calls_today}")
        print(f"   Claude Calls: {self.stats.claude_calls_today}")
        print(f"   Vision Calls: {self.stats.vision_calls_today}")

        # Reset everything
        self._reset_daily()
        self._reset_hourly()

        print("\n✅ API Counters wurden zurückgesetzt!")
        print(f"   Neues Budget: ${self.limits.max_daily_cost_usd:.2f}")
        print()

    def _reset_hourly(self):
        """Reset hourly counters"""
        self.stats.whisper_calls_hour = 0
        self.stats.claude_calls_hour = 0
        self.stats.vision_calls_hour = 0

        self._save_stats()

    # ═══════════════════════════════════════════════════════════════════════════
    # STATS PERSISTENCE
    # ═══════════════════════════════════════════════════════════════════════════

    def _load_stats(self) -> APIStats:
        """Load stats from disk"""
        if not self.stats_file.exists():
            return APIStats(
                last_reset_date=datetime.now().strftime("%Y-%m-%d"),
                last_reset_hour=datetime.now().strftime("%Y-%m-%d %H:00")
            )

        try:
            with open(self.stats_file, "r") as f:
                data = json.load(f)
                return APIStats(**data)
        except Exception as e:
            print(f"⚠️ Failed to load API stats: {e}")
            return APIStats()

    def _save_stats(self):
        """Save stats to disk"""
        try:
            with open(self.stats_file, "w") as f:
                json.dump(asdict(self.stats), f, indent=2)
        except Exception as e:
            print(f"⚠️ Failed to save API stats: {e}")

    # ═══════════════════════════════════════════════════════════════════════════
    # REPORTING
    # ═══════════════════════════════════════════════════════════════════════════

    def get_status(self) -> Dict:
        """Get current API usage status"""
        self._auto_reset()

        return {
            "whisper": {
                "hour": f"{self.stats.whisper_calls_hour}/{self.limits.whisper_max_per_hour}",
                "day": f"{self.stats.whisper_calls_today}/{self.limits.whisper_max_per_day}",
                "cost_today": f"${self.stats.whisper_cost_today:.3f}"
            },
            "claude": {
                "hour": f"{self.stats.claude_calls_hour}/{self.limits.claude_max_per_hour}",
                "day": f"{self.stats.claude_calls_today}/{self.limits.claude_max_per_day}",
                "cost_today": f"${self.stats.claude_cost_today:.3f}"
            },
            "vision": {
                "hour": f"{self.stats.vision_calls_hour}/{self.limits.vision_max_per_hour}",
                "day": f"{self.stats.vision_calls_today}/{self.limits.vision_max_per_day}",
                "cost_today": f"${self.stats.vision_cost_today:.3f}"
            },
            "total": {
                "cost_today": f"${self.stats.total_cost_today:.2f}",
                "budget": f"${self.limits.max_daily_cost_usd:.2f}",
                "remaining": f"${self.limits.max_daily_cost_usd - self.stats.total_cost_today:.2f}"
            }
        }

    def print_status(self):
        """Print API usage status"""
        status = self.get_status()

        print("\n" + "="*60)
        print("📊 API USAGE STATUS")
        print("="*60)
        print(f"🎤 Whisper:  Hour {status['whisper']['hour']}  |  Day {status['whisper']['day']}  |  Cost {status['whisper']['cost_today']}")
        print(f"🤖 Claude:   Hour {status['claude']['hour']}   |  Day {status['claude']['day']}   |  Cost {status['claude']['cost_today']}")
        print(f"👁️  Vision:   Hour {status['vision']['hour']}   |  Day {status['vision']['day']}   |  Cost {status['vision']['cost_today']}")
        print("="*60)
        print(f"💰 Total Cost: {status['total']['cost_today']} / {status['total']['budget']}  (Remaining: {status['total']['remaining']})")
        print("="*60 + "\n")


# ═══════════════════════════════════════════════════════════════════════════════
# GLOBAL INSTANCE
# ═══════════════════════════════════════════════════════════════════════════════

# Global API Guard instance (singleton)
_api_guard = None

def get_api_guard() -> APIGuard:
    """Get global API Guard instance"""
    global _api_guard
    if _api_guard is None:
        _api_guard = APIGuard()
    return _api_guard


# ═══════════════════════════════════════════════════════════════════════════════
# TESTING
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("\n🛡️ M.O.L.O.C.H. 3.0 API Safeguards Test\n")

    guard = APIGuard()

    # Test rate limiting
    print("Testing Whisper calls...")
    for i in range(5):
        allowed, reason = guard.can_call_whisper()
        print(f"  Call {i+1}: {allowed} - {reason}")
        if allowed:
            guard.record_whisper_call(duration_seconds=20)

    # Print status
    guard.print_status()

    print("✅ API Safeguards test complete\n")
