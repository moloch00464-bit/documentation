#!/usr/bin/env python3
"""
M.O.L.O.C.H. 3.0 - Search Tool
================================
Code search (grep-like)
"""

import re
import subprocess
from typing import List, Dict, Optional
from pathlib import Path


class SearchTool:
    """
    Code Search Tool

    Features:
    - Grep for patterns in files
    - Find function/class definitions
    - Regex support
    """

    def __init__(self):
        """Initialize Search Tool"""
        pass

    # ═══════════════════════════════════════════════════════════════════════════
    # GREP
    # ═══════════════════════════════════════════════════════════════════════════

    def grep(
        self,
        pattern: str,
        path: str = ".",
        file_pattern: str = "*",
        case_sensitive: bool = False,
        max_results: int = 100
    ) -> List[Dict[str, str]]:
        """
        Search for pattern in files

        Args:
            pattern: Search pattern (regex)
            path: Directory to search in
            file_pattern: File pattern (e.g., "*.py")
            case_sensitive: Case-sensitive search
            max_results: Max number of results

        Returns:
            List of matches: [{"file": "...", "line": 123, "content": "..."}]
        """
        results = []

        try:
            # Use grep command if available (faster)
            if self._has_grep():
                results = self._grep_command(
                    pattern, path, file_pattern, case_sensitive, max_results
                )
            else:
                # Fallback: Python implementation
                results = self._grep_python(
                    pattern, path, file_pattern, case_sensitive, max_results
                )

        except Exception as e:
            print(f"❌ Grep error: {e}")

        return results

    def _has_grep(self) -> bool:
        """Check if grep command is available"""
        try:
            subprocess.run(
                ["grep", "--version"],
                capture_output=True,
                timeout=1
            )
            return True
        except:
            return False

    def _grep_command(
        self,
        pattern: str,
        path: str,
        file_pattern: str,
        case_sensitive: bool,
        max_results: int
    ) -> List[Dict[str, str]]:
        """Grep using command-line grep"""
        cmd = ["grep", "-rn"]  # Recursive, line numbers

        if not case_sensitive:
            cmd.append("-i")

        if file_pattern != "*":
            cmd.extend(["--include", file_pattern])

        cmd.extend([pattern, path])

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                timeout=30,
                text=True
            )

            # Parse output
            results = []
            for line in result.stdout.split("\n")[:max_results]:
                if not line.strip():
                    continue

                # Format: file:line:content
                parts = line.split(":", 2)
                if len(parts) >= 3:
                    results.append({
                        "file": parts[0],
                        "line": parts[1],
                        "content": parts[2]
                    })

            return results

        except subprocess.TimeoutExpired:
            print("⚠️ Grep timeout")
            return []
        except Exception as e:
            print(f"⚠️ Grep command error: {e}")
            return []

    def _grep_python(
        self,
        pattern: str,
        path: str,
        file_pattern: str,
        case_sensitive: bool,
        max_results: int
    ) -> List[Dict[str, str]]:
        """Grep using Python (fallback)"""
        results = []

        # Compile regex
        flags = 0 if case_sensitive else re.IGNORECASE
        try:
            regex = re.compile(pattern, flags)
        except re.error as e:
            print(f"❌ Invalid regex: {e}")
            return []

        # Search files
        path_obj = Path(path)
        if not path_obj.exists():
            return []

        # Get matching files
        import glob
        search_pattern = str(path_obj / "**" / file_pattern)
        files = glob.glob(search_pattern, recursive=True)

        # Search in each file
        for file_path in files:
            if len(results) >= max_results:
                break

            try:
                # Skip binary files
                if not self._is_text_file(file_path):
                    continue

                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    for line_num, line in enumerate(f, 1):
                        if regex.search(line):
                            results.append({
                                "file": file_path,
                                "line": str(line_num),
                                "content": line.rstrip()
                            })

                            if len(results) >= max_results:
                                break

            except Exception:
                continue

        return results

    def _is_text_file(self, path: str) -> bool:
        """Check if file is text (not binary)"""
        try:
            with open(path, "rb") as f:
                chunk = f.read(1024)
                # Check for null bytes (common in binary files)
                return b"\x00" not in chunk
        except:
            return False

    # ═══════════════════════════════════════════════════════════════════════════
    # FIND DEFINITIONS
    # ═══════════════════════════════════════════════════════════════════════════

    def find_function(self, name: str, path: str = ".") -> List[Dict[str, str]]:
        """
        Find function definition

        Args:
            name: Function name
            path: Directory to search in

        Returns:
            List of matches
        """
        # Python: def function_name(
        # JavaScript: function function_name(
        # JavaScript: const function_name = (
        patterns = [
            rf"def\s+{name}\s*\(",  # Python
            rf"function\s+{name}\s*\(",  # JS function
            rf"const\s+{name}\s*=",  # JS const
            rf"async\s+def\s+{name}\s*\(",  # Python async
        ]

        results = []
        for pattern in patterns:
            matches = self.grep(pattern, path, case_sensitive=True, max_results=10)
            results.extend(matches)

        return results

    def find_class(self, name: str, path: str = ".") -> List[Dict[str, str]]:
        """
        Find class definition

        Args:
            name: Class name
            path: Directory to search in

        Returns:
            List of matches
        """
        # Python: class ClassName
        # JavaScript: class ClassName
        pattern = rf"class\s+{name}\s*[\(:]"

        return self.grep(pattern, path, case_sensitive=True, max_results=10)


# ═══════════════════════════════════════════════════════════════════════════════
# TESTING
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("\n🔍 M.O.L.O.C.H. 3.0 Search Tool Test\n")

    search = SearchTool()

    # Test grep
    print("📝 Testing grep in current directory...")
    results = search.grep("def ", path=".", file_pattern="*.py", max_results=5)
    print(f"   ✅ Found {len(results)} matches")
    if results:
        print(f"   First match: {results[0]['file']}:{results[0]['line']}")

    # Test find function
    print("\n🔍 Testing find_function...")
    results = search.find_function("__init__", path=".")
    print(f"   ✅ Found {len(results)} __init__ definitions")

    print()
