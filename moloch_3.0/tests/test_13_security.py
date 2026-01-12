#!/usr/bin/env python3
"""
M.O.L.O.C.H. 3.0 - SECURITY TESTS
==================================
Tests für Security Vulnerabilities

PRODUCTION HARDENING PROTOCOL:
- Path Traversal MUSS blockiert werden
- Filename Injection MUSS sanitized werden
- JSON Bombs MÜSSEN erkannt werden
- KEIN unvalidierter Input darf durchkommen

CRITICAL: Diese Tests müssen ALLE grün sein für Production!

Author: Claude
Date: 2026-01-12
"""

import sys
import unittest
import tempfile
import shutil
import signal
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.brain import Brain


class TestSecurity(unittest.TestCase):
    """Tests für Security und Input Validation"""

    def setUp(self):
        """Setup test environment"""
        # Create temporary directories
        self.test_dir = Path(tempfile.mkdtemp())
        self.brain_dir = self.test_dir / "brain"
        self.brain_dir.mkdir(parents=True, exist_ok=True)

        # Create Brain with test directory
        self.brain = Brain(brain_dir=str(self.brain_dir))

    def tearDown(self):
        """Cleanup test environment"""
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)

    def test_path_traversal_attack(self):
        """SECURITY: Path Traversal muss blockiert werden"""
        malicious_names = [
            "../../../etc/passwd",
            "..\\..\\windows\\system32",
            "....//....//etc/passwd",
            "valid/../../../etc/passwd",
            "/etc/passwd",
            "C:\\Windows\\System32\\config",
        ]

        for malicious in malicious_names:
            # Save attempt
            result = self.brain.save("was", {"hack": True}, malicious)

            # MUSS fehlschlagen oder sanitized werden
            # Datei darf NIEMALS außerhalb brain_dir landen
            if result is True:
                # Prüfe ob Datei in brain_dir ist
                all_files = list(self.brain_dir.rglob("*.json"))
                for f in all_files:
                    # Alle Dateien müssen INNERHALB brain_dir sein
                    try:
                        f.relative_to(self.brain_dir)
                    except ValueError:
                        self.fail(f"PATH TRAVERSAL MÖGLICH: {malicious} → {f}")

                    # Keine system paths dürfen im Namen sein
                    self.assertNotIn("etc", str(f).lower(),
                                   f"PATH TRAVERSAL: etc in {f}")
                    self.assertNotIn("passwd", str(f).lower(),
                                   f"PATH TRAVERSAL: passwd in {f}")
                    self.assertNotIn("windows", str(f).lower(),
                                   f"PATH TRAVERSAL: windows in {f}")
                    self.assertNotIn("system32", str(f).lower(),
                                   f"PATH TRAVERSAL: system32 in {f}")

    def test_filename_sanitization(self):
        """SECURITY: Gefährliche Dateinamen müssen sanitized werden"""
        dangerous_names = [
            "file\x00name.json",      # Null byte
            "file\nname.json",        # Newline
            "file|name.json",         # Pipe
            "file;name.json",         # Semicolon (command injection)
            "$(whoami).json",         # Command substitution
            "`id`.json",              # Backtick execution
            "file<script>.json",      # XSS attempt
            "file&name.json",         # Command chaining
        ]

        for name in dangerous_names:
            # Entweder: sanitizen und speichern ODER: ablehnen
            # NIEMALS: unverändert durchlassen
            try:
                result = self.brain.save("was", {"test": True}, name)

                if result is True:
                    # Wenn gespeichert, dann muss es sanitized sein
                    files = list((self.brain.brain_dir / "was").glob("*"))
                    for f in files:
                        # Check for dangerous characters
                        self.assertNotIn("\x00", f.name, f"NULL byte nicht sanitized: {name}")
                        self.assertNotIn("\n", f.name, f"Newline nicht sanitized: {name}")
                        self.assertNotIn("|", f.name, f"Pipe nicht sanitized: {name}")
                        self.assertNotIn("$(", f.name, f"Command substitution nicht sanitized: {name}")
                        self.assertNotIn("`", f.name, f"Backtick nicht sanitized: {name}")
                        self.assertNotIn("<script>", f.name.lower(), f"XSS nicht sanitized: {name}")

            except (ValueError, OSError) as e:
                # Ablehnung ist OK
                pass

    def test_json_size_bomb(self):
        """SECURITY: JSON Bomb / Zip Bomb Schutz"""
        # Nested structure die beim Parsen explodiert
        bomb = {"a": {}}
        current = bomb["a"]
        for _ in range(100):  # 100 Ebenen tief
            current["nested"] = {}
            current = current["nested"]

        # Sollte nicht ewig dauern oder crashen
        def timeout_handler(signum, frame):
            raise TimeoutError("JSON Bomb detected!")

        # Set timeout (nur auf Unix-Systemen)
        try:
            signal.signal(signal.SIGALRM, timeout_handler)
            signal.alarm(5)  # 5 Sekunden max

            try:
                result = self.brain.save("was", bomb, "bomb.json")
                signal.alarm(0)  # Cancel timeout

                # Operation muss in <5s fertig sein
                self.assertIsNotNone(result, "Save muss Result zurückgeben")

            except TimeoutError:
                self.fail("JSON BOMB - Operation dauerte zu lange!")

        except AttributeError:
            # Windows hat kein signal.SIGALRM - verwende alternative Methode
            import time
            start = time.time()

            result = self.brain.save("was", bomb, "bomb.json")
            duration = time.time() - start

            self.assertLess(duration, 5.0,
                          f"JSON Bomb - Operation dauerte {duration:.1f}s (Max: 5s)")


if __name__ == "__main__":
    unittest.main(verbosity=2)
