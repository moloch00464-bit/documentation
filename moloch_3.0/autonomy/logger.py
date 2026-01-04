#!/usr/bin/env python3
"""
M.O.L.O.C.H. 3.0 - Smart Logger
=================================
Intelligent logging with pattern detection
"""

import logging
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, List
from collections import defaultdict

from core.config import LOGS_DIR, LOG_LEVEL, LOG_FORMAT


class SmartLogger:
    """
    Smart Logger for M.O.L.O.C.H. 3.0

    Features:
    - Multi-level logging (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    - Pattern detection (repeated errors)
    - Context tracking
    - Auto-rotate logs
    """

    def __init__(self, name: str = "moloch"):
        """
        Initialize Smart Logger

        Args:
            name: Logger name
        """
        self.name = name
        self.error_patterns = defaultdict(int)  # Track error patterns

        # Setup logging
        self._setup_logging()

    def _setup_logging(self):
        """Setup logging configuration"""
        # Ensure logs directory exists
        LOGS_DIR.mkdir(parents=True, exist_ok=True)

        # Create logger
        self.logger = logging.getLogger(self.name)
        self.logger.setLevel(getattr(logging, LOG_LEVEL))

        # File handler
        log_file = LOGS_DIR / "moloch.log"
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(logging.Formatter(LOG_FORMAT))
        self.logger.addHandler(file_handler)

        # Error file handler (separate file for errors)
        error_file = LOGS_DIR / "errors.log"
        error_handler = logging.FileHandler(error_file)
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(logging.Formatter(LOG_FORMAT))
        self.logger.addHandler(error_handler)

    # ═══════════════════════════════════════════════════════════════════════════
    # LOGGING METHODS
    # ═══════════════════════════════════════════════════════════════════════════

    def debug(self, message: str, context: Optional[Dict] = None):
        """Log debug message"""
        self._log(logging.DEBUG, message, context)

    def info(self, message: str, context: Optional[Dict] = None):
        """Log info message"""
        self._log(logging.INFO, message, context)

    def warning(self, message: str, context: Optional[Dict] = None):
        """Log warning message"""
        self._log(logging.WARNING, message, context)

    def error(self, message: str, context: Optional[Dict] = None):
        """Log error message"""
        self._log(logging.ERROR, message, context)

        # Track error pattern
        self._track_error_pattern(message)

    def critical(self, message: str, context: Optional[Dict] = None):
        """Log critical message"""
        self._log(logging.CRITICAL, message, context)

        # Track error pattern
        self._track_error_pattern(message)

        # Critical errors might trigger auto-debug
        self._handle_critical_error(message, context)

    def _log(self, level: int, message: str, context: Optional[Dict] = None):
        """Internal log method"""
        # Add context if provided
        if context:
            message = f"{message} | Context: {context}"

        self.logger.log(level, message)

    # ═══════════════════════════════════════════════════════════════════════════
    # PATTERN DETECTION
    # ═══════════════════════════════════════════════════════════════════════════

    def _track_error_pattern(self, message: str):
        """
        Track error patterns

        If same error appears 3+ times, flag for auto-debug
        """
        # Normalize error message
        error_key = self._normalize_error(message)

        # Increment counter
        self.error_patterns[error_key] += 1

        # Check if pattern is repeating
        count = self.error_patterns[error_key]
        if count >= 3:
            self.warning(f"PATTERN DETECTED: Error '{error_key}' occurred {count} times!")
            # Could trigger auto-debugger here
            return True

        return False

    def _normalize_error(self, message: str) -> str:
        """
        Normalize error message to detect patterns

        Example:
        "File not found: /path/to/file1.txt" → "File not found: *"
        "Connection timeout after 30s" → "Connection timeout after *"
        """
        import re

        # Remove numbers
        normalized = re.sub(r'\d+', '*', message)

        # Remove paths
        normalized = re.sub(r'[/\\][^\s]+', '*', normalized)

        # Remove quotes content
        normalized = re.sub(r'"[^"]*"', '"*"', normalized)
        normalized = re.sub(r"'[^']*'", "'*'", normalized)

        return normalized[:100]  # Limit length

    def get_error_patterns(self) -> List[Dict]:
        """
        Get detected error patterns

        Returns:
            List of error patterns with counts
        """
        return [
            {"pattern": pattern, "count": count}
            for pattern, count in sorted(
                self.error_patterns.items(),
                key=lambda x: x[1],
                reverse=True
            )
        ]

    # ═══════════════════════════════════════════════════════════════════════════
    # CRITICAL ERROR HANDLING
    # ═══════════════════════════════════════════════════════════════════════════

    def _handle_critical_error(self, message: str, context: Optional[Dict]):
        """
        Handle critical errors

        Could trigger:
        - Auto-debugger
        - Notification
        - Emergency fallback
        """
        # For now, just log
        self.logger.critical(f"CRITICAL ERROR HANDLER: {message}")

        # In future: Call auto-debugger
        # from autonomy.debugger import SelfDebugger
        # debugger = SelfDebugger()
        # debugger.analyze_error(message, context)

    # ═══════════════════════════════════════════════════════════════════════════
    # LOG READING
    # ═══════════════════════════════════════════════════════════════════════════

    def get_recent_logs(self, n: int = 100) -> List[str]:
        """
        Get recent log entries

        Args:
            n: Number of recent entries

        Returns:
            List of log lines
        """
        log_file = LOGS_DIR / "moloch.log"

        if not log_file.exists():
            return []

        try:
            with open(log_file, "r") as f:
                lines = f.readlines()
                return lines[-n:]
        except Exception as e:
            print(f"⚠️ Error reading logs: {e}")
            return []

    def get_recent_errors(self, n: int = 50) -> List[str]:
        """Get recent error entries"""
        error_file = LOGS_DIR / "errors.log"

        if not error_file.exists():
            return []

        try:
            with open(error_file, "r") as f:
                lines = f.readlines()
                return lines[-n:]
        except Exception as e:
            print(f"⚠️ Error reading error log: {e}")
            return []


# ═══════════════════════════════════════════════════════════════════════════════
# TESTING
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("\n📝 M.O.L.O.C.H. 3.0 Smart Logger Test\n")

    logger = SmartLogger()

    # Test logging
    print("✅ Testing logging levels...")
    logger.debug("Debug message")
    logger.info("Info message")
    logger.warning("Warning message")
    logger.error("Error message")

    # Test context
    print("\n✅ Testing context logging...")
    logger.info("User login", context={"user": "Markus", "mode": "voice"})

    # Test pattern detection
    print("\n🔍 Testing error pattern detection...")
    for i in range(4):
        logger.error(f"Connection timeout after {i*10}s")

    patterns = logger.get_error_patterns()
    print(f"   Detected {len(patterns)} patterns:")
    for p in patterns:
        print(f"     - {p['pattern']}: {p['count']} times")

    # Check logs
    print("\n📖 Recent logs:")
    recent = logger.get_recent_logs(n=5)
    for line in recent:
        print(f"   {line.strip()}")

    print()
