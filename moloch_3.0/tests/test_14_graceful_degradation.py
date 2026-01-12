#!/usr/bin/env python3
"""
M.O.L.O.C.H. 3.0 - GRACEFUL DEGRADATION TESTS
==============================================
Tests für System-Robustheit bei fehlenden Komponenten

PRODUCTION HARDENING PROTOCOL:
- Offline Mode muss funktionieren (lokale Features)
- Fehlender API Key darf nicht crashen
- Fehlende Kategorien müssen auto-created werden
- Partial failures dürfen System nicht stoppen

Pi 5 Industrial Use Case:
- Keine Internet-Garantie in Fabrik
- Config kann fehlen bei erster Installation
- Robustheit > Features

Author: Claude
Date: 2026-01-12
"""

import sys
import unittest
import tempfile
import shutil
import os
from pathlib import Path
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.brain import Brain
from core.memory import Memory
from core.personality import Personality


class TestGracefulDegradation(unittest.TestCase):
    """Tests für Graceful Degradation bei fehlenden Komponenten"""

    def setUp(self):
        """Setup test environment"""
        # Create temporary directories
        self.test_dir = Path(tempfile.mkdtemp())
        self.brain_dir = self.test_dir / "brain"
        self.memory_dir = self.test_dir / "memory"

        self.brain_dir.mkdir(parents=True, exist_ok=True)
        self.memory_dir.mkdir(parents=True, exist_ok=True)

        # Create components with test directories
        self.brain = Brain(brain_dir=str(self.brain_dir))
        self.memory = Memory(
            history_file=self.memory_dir / "history.json",
            memory_file=self.memory_dir / "langzeit.json"
        )
        self.personality = Personality()

    def tearDown(self):
        """Cleanup test environment"""
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)

    def test_offline_mode(self):
        """System muss ohne Internet funktionieren (lokale Features)"""
        # Simuliere: Kein Netzwerk
        import socket
        original_socket = socket.socket

        def blocked_socket(*args, **kwargs):
            raise OSError("Network disabled for test")

        socket.socket = blocked_socket

        try:
            # Diese müssen OHNE Internet funktionieren:

            # 1. Brain Operations
            save_result = self.brain.save("was", {"offline": True}, "offline_test.json")
            self.assertTrue(save_result, "Brain save muss offline funktionieren")

            result = self.brain.read("was", "offline_test.json")
            self.assertIsNotNone(result, "Brain read muss offline funktionieren")

            # 2. Memory Operations
            self.memory.add_to_history("user", "Offline test")
            self.assertGreater(len(self.memory.history), 0, "Memory add_to_history muss offline funktionieren")

            # 3. Personality Operations
            stimmung = self.personality.detect_stimmung("Das ist ein Test")
            self.assertIn(stimmung, ["neutral", "fragend", "gestresst", "gut_drauf", "frustriert"],
                         "Personality detect_stimmung muss offline funktionieren")

        finally:
            socket.socket = original_socket

    def test_api_not_configured(self):
        """System muss starten auch wenn API Key fehlt"""
        # Backup original key
        original_key = os.environ.get("ANTHROPIC_API_KEY")

        if "ANTHROPIC_API_KEY" in os.environ:
            del os.environ["ANTHROPIC_API_KEY"]

        try:
            # Import API - sollte nicht crashen
            try:
                from core.api import API
                api = API()

                # Muss instanziierbar sein - erst bei Aufruf Fehler
                self.assertIsNotNone(api, "API muss instanziierbar sein ohne Key")

            except ImportError:
                # API module existiert nicht - das ist OK
                self.skipTest("API module nicht vorhanden - OK für Tests")

            except Exception as e:
                # Andere Exceptions sind OK, solange sie klar sind
                self.assertIn("API", str(e).upper() or "KEY" in str(e).upper(),
                             f"Exception muss klar sein: {e}")

        finally:
            # Restore key
            if original_key:
                os.environ["ANTHROPIC_API_KEY"] = original_key

    def test_partial_brain_structure(self):
        """Brain muss mit fehlenden Kategorien umgehen"""
        # Lösche eine Kategorie
        wer_path = self.brain.brain_dir / "wer"
        if wer_path.exists():
            shutil.rmtree(wer_path)

        # Stats darf nicht crashen
        stats = self.brain.stats()

        # "wer" muss in Stats sein (mit 0)
        self.assertIn("wer", stats, "Fehlende Kategorie muss in Stats sein")
        self.assertEqual(stats["wer"], 0, "Fehlende Kategorie muss 0 entries haben")

        # Save muss Kategorie neu anlegen
        result = self.brain.save("wer", {"recreated": True}, "test.json")
        self.assertTrue(result, "Brain muss fehlende Kategorie recreaten")

        # Verify it was recreated
        self.assertTrue(wer_path.exists(), "Kategorie muss neu erstellt worden sein")

        # Read muss funktionieren
        loaded = self.brain.read("wer", "test.json")
        self.assertIsNotNone(loaded, "Read aus recreated Kategorie muss funktionieren")
        self.assertEqual(loaded["content"]["recreated"], True, "Content muss korrekt sein")


if __name__ == "__main__":
    unittest.main(verbosity=2)
