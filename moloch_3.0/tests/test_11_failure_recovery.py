#!/usr/bin/env python3
"""
M.O.L.O.C.H. 3.0 - FAILURE RECOVERY TESTS
==========================================
Tests für Crash Recovery und korrupte Dateien

PRODUCTION HARDENING PROTOCOL:
- Brain muss mit korrupten JSON-Dateien umgehen
- Memory muss mit korrupter History recovern
- Config muss mit Defaults starten wenn fehlt
- Kein Crash bei halben Dateien

Author: Claude
Date: 2026-01-12
"""

import sys
import unittest
import json
import tempfile
import shutil
from pathlib import Path
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.brain import Brain
from core.memory import Memory


class TestFailureRecovery(unittest.TestCase):
    """Tests für Failure Recovery und Crash Handling"""

    def setUp(self):
        """Setup test environment"""
        # Create temporary directories
        self.test_dir = Path(tempfile.mkdtemp())
        self.brain_dir = self.test_dir / "brain"
        self.memory_dir = self.test_dir / "memory"

        self.brain_dir.mkdir(parents=True, exist_ok=True)
        self.memory_dir.mkdir(parents=True, exist_ok=True)

        # Create Brain with test directory
        self.brain = Brain(brain_dir=str(self.brain_dir))

        # Create Memory with test directory
        self.memory = Memory(
            history_file=self.memory_dir / "history.json",
            memory_file=self.memory_dir / "langzeit.json"
        )

    def tearDown(self):
        """Cleanup test environment"""
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)

    def test_brain_crash_mid_write(self):
        """Simuliere Crash während save() - kann Brain recovern?"""
        # Schreibe halbe JSON-Datei (simuliert Crash während Write)
        corrupt_path = self.brain.brain_dir / "was" / "corrupt.json"
        corrupt_path.parent.mkdir(parents=True, exist_ok=True)

        with open(corrupt_path, 'w') as f:
            f.write('{"content": {"test": true}, "meta')  # Abgeschnitten!

        # Brain.read() MUSS das handlen - nicht crashen
        result = self.brain.read("was", "corrupt.json")

        # Graceful fail: None ODER dict mit _error key
        self.assertTrue(
            result is None or (isinstance(result, dict) and "_error" in result),
            "Brain muss korrupte JSON graceful handlen"
        )

    def test_brain_recover_after_corrupt(self):
        """Nach korrupter Datei müssen andere Dateien noch funktionieren"""
        # Erst korrupte Datei erstellen
        corrupt_path = self.brain.brain_dir / "was" / "corrupt.json"
        corrupt_path.parent.mkdir(parents=True, exist_ok=True)

        with open(corrupt_path, 'w') as f:
            f.write('KEINE VALIDE JSON')

        # Dann normale Datei speichern
        save_result = self.brain.save("was", {"valid": True}, "valid.json")
        self.assertTrue(save_result, "Brain muss nach korrupter Datei noch speichern können")

        # Valid muss trotzdem lesbar sein
        result = self.brain.read("was", "valid.json")
        self.assertIsNotNone(result, "Valid file muss lesbar sein trotz korrupter Datei")
        self.assertEqual(result["content"]["valid"], True, "Content muss korrekt sein")

    def test_memory_corrupt_history_file(self):
        """Memory muss mit korrupter History umgehen"""
        # Schreibe kaputte History
        history_file = self.memory_dir / "corrupt_history.json"
        history_file.parent.mkdir(parents=True, exist_ok=True)

        with open(history_file, 'w') as f:
            f.write('[{"role": "user"')  # Kaputt - fehlendes Ende

        # Load darf nicht crashen - muss mit Defaults recovern
        try:
            new_memory = Memory(history_file=history_file)
            # Muss entweder: leere History ODER Exception mit klarer Message
            self.assertTrue(hasattr(new_memory, 'history'), "Memory muss history haben")
            self.assertIsInstance(new_memory.history, list, "History muss list sein")
        except Exception as e:
            # Exception ist OK, aber sie muss klar sein
            self.assertIn("JSON", str(e).upper() or "PARSE" in str(e).upper(),
                         f"Exception muss klar sein: {e}")

    def test_config_missing_completely(self):
        """Was wenn config.json nicht existiert?"""
        # Backup config falls sie existiert
        config_path = Path(__file__).parent.parent / "config.json"
        backup_path = config_path.with_suffix(".json.test_backup")

        config_existed = False
        if config_path.exists():
            config_existed = True
            shutil.copy(config_path, backup_path)
            config_path.unlink()

        try:
            # Import Config - darf nicht crashen
            from core.config import Config
            cfg = Config()

            # Muss mit Defaults starten, nicht crashen
            self.assertIsNotNone(cfg, "Config muss instanziierbar sein")
            self.assertTrue(hasattr(cfg, '__dict__'), "Config muss Attribute haben")

        except ImportError:
            # Config module existiert nicht - das ist OK für diesen Test
            self.skipTest("Config module nicht vorhanden")

        finally:
            # Restore config
            if config_existed and backup_path.exists():
                shutil.copy(backup_path, config_path)
                backup_path.unlink()


if __name__ == "__main__":
    unittest.main(verbosity=2)
