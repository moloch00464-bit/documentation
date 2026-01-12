#!/usr/bin/env python3
"""
M.O.L.O.C.H. 3.0 - CONSISTENCY TESTS
=====================================
Tests für Data Integrity und Consistency

PRODUCTION HARDENING PROTOCOL:
- Idempotent saves (gleicher Input = gleiches Result)
- Concurrent access darf nicht korrupieren
- Atomic saves (ganz oder gar nicht)
- Thread-Safety für Multi-Core Pi 5

Critical für Production:
- Factory environment = Multi-User Access
- Pi 5 hat 4 Cores = Concurrency möglich
- Data Integrity ist nicht verhandelbar

Author: Claude
Date: 2026-01-12
"""

import sys
import unittest
import tempfile
import shutil
import threading
import time
import random
import json
from pathlib import Path
from unittest import mock

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.brain import Brain


class TestConsistency(unittest.TestCase):
    """Tests für Data Consistency und Thread-Safety"""

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

    def test_save_idempotent(self):
        """Zweimal gleicher Content = konsistentes Ergebnis"""
        content = {"test": "idempotent", "value": 42, "data": "consistent"}

        # Save 1
        self.brain.save("was", content, "idempotent.json")
        first = self.brain.read("was", "idempotent.json")

        # Save 2 (gleicher Content)
        self.brain.save("was", content, "idempotent.json")
        second = self.brain.read("was", "idempotent.json")

        # Content muss identisch sein
        self.assertEqual(first["content"], second["content"],
                        "Idempotent save muss gleichen Content liefern")

        # Auch nach 3. Save
        self.brain.save("was", content, "idempotent.json")
        third = self.brain.read("was", "idempotent.json")

        self.assertEqual(first["content"], third["content"],
                        "Idempotent save muss auch nach mehrfachem Save konsistent sein")

    def test_concurrent_read_write(self):
        """Parallele Reads/Writes dürfen sich nicht zerstören"""
        errors = []
        results = {"reads": 0, "writes": 0}
        lock = threading.Lock()

        # Erst eine Datei anlegen
        self.brain.save("was", {"initial": True, "counter": 0}, "concurrent.json")

        def reader():
            """Read Thread"""
            for _ in range(50):
                try:
                    data = self.brain.read("was", "concurrent.json")
                    if data:
                        with lock:
                            results["reads"] += 1
                except Exception as e:
                    with lock:
                        errors.append(f"Read error: {e}")
                time.sleep(random.uniform(0.001, 0.01))

        def writer():
            """Write Thread"""
            for i in range(50):
                try:
                    self.brain.save("was", {"iteration": i, "timestamp": time.time()}, "concurrent.json")
                    with lock:
                        results["writes"] += 1
                except Exception as e:
                    with lock:
                        errors.append(f"Write error: {e}")
                time.sleep(random.uniform(0.001, 0.01))

        # Start threads
        threads = [
            threading.Thread(target=reader, name="reader1"),
            threading.Thread(target=reader, name="reader2"),
            threading.Thread(target=writer, name="writer1"),
        ]

        for t in threads:
            t.start()

        for t in threads:
            t.join(timeout=30)  # Max 30s

        # Validate
        self.assertEqual(len(errors), 0, f"Concurrency errors occurred: {errors}")
        self.assertGreater(results["reads"], 40, "Mindestens 80% Reads erfolgreich")
        self.assertGreater(results["writes"], 40, "Mindestens 80% Writes erfolgreich")

    def test_atomic_save(self):
        """Save muss atomar sein - ganz oder gar nicht"""
        # Test 1: Normale atomic save
        test_content = {"atomic": True, "complete": True}
        result = self.brain.save("was", test_content, "atomic_test.json")
        self.assertTrue(result, "Normal save muss erfolgreich sein")

        # Test 2: Wenn save() crasht, darf keine halbe Datei übrig bleiben
        file_path = self.brain.brain_dir / "was" / "atomic_crash_test.json"

        # Simuliere Crash während Write
        with mock.patch('builtins.open', side_effect=IOError("Simulated crash")):
            try:
                self.brain.save("was", {"crash": True}, "atomic_crash_test.json")
            except Exception:
                pass  # Crash ist expected

        # Datei sollte nicht existieren (oder komplett valide sein von vorher)
        if file_path.exists():
            # Wenn sie existiert, muss sie valide sein
            try:
                with open(file_path) as f:
                    content = f.read()
                    parsed = json.loads(content)  # Muss parsen können
                    self.assertIsInstance(parsed, dict, "Datei muss valides JSON sein")
            except json.JSONDecodeError:
                self.fail(f"Atomic save failed - korrupte Datei existiert: {file_path}")

        # Test 3: Verify dass finale Datei immer komplett ist
        for i in range(10):
            self.brain.save("was", {"iteration": i, "complete": True}, "atomic_multi.json")

        final = self.brain.read("was", "atomic_multi.json")
        self.assertIsNotNone(final, "Final read muss erfolgreich sein")
        self.assertTrue(final["content"]["complete"], "Final file muss komplett sein")


if __name__ == "__main__":
    unittest.main(verbosity=2)
