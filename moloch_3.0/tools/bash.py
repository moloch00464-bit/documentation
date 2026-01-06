#!/usr/bin/env python3
"""
M.O.L.O.C.H. 3.0 - Bash Tool
=============================
Safe shell command execution
"""

import subprocess
from typing import Tuple, Optional
import shlex

from core.config import BASH_SAFE_COMMANDS, BASH_DANGEROUS_COMMANDS, BASH_DANGEROUS_PATTERNS
import re


class BashTool:
    """
    Bash Command Execution Tool

    Features:
    - Safe command execution
    - Timeout protection
    - Dangerous command blocking
    - stdout/stderr capture
    """

    def __init__(self):
        """Initialize Bash Tool"""
        pass

    def execute(
        self,
        command: str,
        timeout: int = 30,
        check_safety: bool = True
    ) -> Tuple[str, str, int]:
        """
        Execute shell command

        Args:
            command: Command to execute
            timeout: Timeout in seconds
            check_safety: If True, check if command is safe

        Returns:
            (stdout, stderr, returncode)
        """
        # Safety check
        if check_safety and not self.is_safe(command):
            return "", f"❌ DANGEROUS COMMAND BLOCKED: {command}", 1

        try:
            # Execute
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                timeout=timeout,
                text=True
            )

            return result.stdout, result.stderr, result.returncode

        except subprocess.TimeoutExpired:
            return "", f"⚠️ Command timeout ({timeout}s): {command}", 1

        except Exception as e:
            return "", f"❌ Execution error: {e}", 1

    def is_safe(self, command: str) -> bool:
        """
        Check if command is safe to execute

        Args:
            command: Command string

        Returns:
            True if safe, False if dangerous
        """
        # Use regex patterns for robust matching
        for pattern in BASH_DANGEROUS_PATTERNS:
            if re.search(pattern, command, re.IGNORECASE):
                print(f"🚨 Blocked dangerous command pattern: {pattern[:30]}...")
                return False

        # Legacy blacklist check (backward compatibility)
        command_lower = command.lower()
        for dangerous in BASH_DANGEROUS_COMMANDS:
            if dangerous.lower() in command_lower:
                print(f"🚨 Blocked dangerous command: {dangerous}")
                return False

        # Additional safety checks

        # No root operations without explicit permission
        if command_lower.startswith("sudo ") or command_lower.startswith("su "):
            print("🚨 Blocked root command (needs explicit permission)")
            return False

        # No pipe to bash/sh (code injection risk)
        if re.search(r'\|\s*(sh|bash)\b', command_lower):
            print("🚨 Blocked pipe to shell (injection risk)")
            return False

        # Check for command parsing issues
        try:
            shlex.split(command)
        except ValueError:
            print("🚨 Blocked malformed command (potential injection)")
            return False

        return True

    def execute_safe_only(self, command: str, timeout: int = 30) -> Tuple[str, str, int]:
        """
        Execute only if command starts with a known safe command

        Args:
            command: Command to execute
            timeout: Timeout in seconds

        Returns:
            (stdout, stderr, returncode)
        """
        # Extract first command
        try:
            parts = shlex.split(command)
            if not parts:
                return "", "❌ Empty command", 1

            cmd_name = parts[0]

            # Check if in safe list
            if cmd_name not in BASH_SAFE_COMMANDS:
                return "", f"❌ Command not in safe list: {cmd_name}", 1

        except Exception as e:
            return "", f"❌ Command parsing error: {e}", 1

        # Execute
        return self.execute(command, timeout=timeout, check_safety=True)


# ═══════════════════════════════════════════════════════════════════════════════
# TESTING
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("\n⚡ M.O.L.O.C.H. 3.0 Bash Tool Test\n")

    bash = BashTool()

    # Test safe command
    print("✅ Testing safe command (ls)...")
    stdout, stderr, code = bash.execute("ls /tmp", timeout=5)
    print(f"   Return code: {code}")
    if stdout:
        print(f"   Output: {stdout[:100]}...")

    # Test dangerous command (should be blocked)
    print("\n🚨 Testing dangerous command (should be blocked)...")
    stdout, stderr, code = bash.execute("rm -rf /", timeout=5)
    print(f"   {stderr}")

    # Test safe-only mode
    print("\n✅ Testing safe-only mode (echo)...")
    stdout, stderr, code = bash.execute_safe_only("echo 'Test'", timeout=5)
    print(f"   Output: {stdout.strip()}")

    print()
