#!/usr/bin/env python3
"""
M.O.L.O.C.H. 3.0 - RESOURCE EXHAUSTION TESTS
=============================================
Tests für Resource Limits auf Raspberry Pi 5

PRODUCTION HARDENING PROTOCOL:
- Memory darf nicht explodieren bei 10k Messages
- Brain muss mit 1000 Dateien performen
- 5MB Files müssen in <10s gespeichert werden
- Pi 5 hat nur 4GB RAM - kritisch!

Hardware Target:
- Raspberry Pi 5 (4GB RAM)
- Cortex-A76 @ 2.4GHz (4 Cores)
- MicroSD / NVMe Storage

Author: Claude
Date: 2026-01-12
"""

import sys
import unittest
import time
import tempfile
import shutil
from pathlib import Path
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.brain import Brain
from core.memory import Memory


class TestResourceExhaustion(unittest.TestCase):
    """Tests für Resource Limits und Performance"""

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

    def test_memory_10k_messages(self):
        """Memory mit 10.000 Messages - RAM-Check"""
        try:
            import psutil
        except ImportError:
            self.skipTest("psutil nicht installiert - OK für Dev")

        process = psutil.Process()
        initial_mb = process.memory_info().rss / 1024 / 1024

        # Add 10.000 Messages
        for i in range(10000):
            self.memory.add_to_history(
                role="user" if i % 2 == 0 else "assistant",
                content=f"Message {i}: " + "x" * 500,  # 500 Zeichen pro Message
                metadata={
                    "timestamp": datetime.now().isoformat(),
                    "id": f"msg_{i}"
                }
            )

        final_mb = process.memory_info().rss / 1024 / 1024
        growth_mb = final_mb - initial_mb

        # Max 300MB für 10k Messages auf Pi 5 (4GB total!)
        self.assertLess(
            growth_mb, 300,
            f"Memory explodiert: +{growth_mb:.1f}MB für 10k Messages (Max: 300MB)"
        )

        print(f"    → Memory Growth: {growth_mb:.1f}MB für 10.000 Messages")

    def test_brain_1000_files(self):
        """Brain mit 1000 Dateien - Performance-Check"""
        # Schreibe 1000 Dateien
        start = time.time()
        for i in range(1000):
            self.brain.save("was", {"index": i, "data": "test"}, f"mass_test_{i}.json")
        write_time = time.time() - start

        # Stats müssen schnell sein trotz vieler Dateien
        start = time.time()
        stats = self.brain.stats()
        stats_time = time.time() - start

        # Validierung
        self.assertGreaterEqual(stats["was"], 1000, "Alle 1000 Dateien müssen gezählt werden")
        self.assertLess(stats_time, 2.0,
                       f"Stats zu langsam: {stats_time:.2f}s (Max: 2.0s)")
        self.assertLess(write_time, 60,
                       f"1000 Writes zu langsam: {write_time:.1f}s (Max: 60s)")

        print(f"    → 1000 Writes: {write_time:.1f}s, Stats: {stats_time:.3f}s")

    def test_brain_5mb_file(self):
        """Brain mit 5MB Datei - Limit-Test"""
        # Create 5MB content
        large_content = {
            "huge_text": "M.O.L.O.C.H. " * 500000,  # ~5MB
            "metadata": {"size": "5MB", "test": "resource_exhaustion"}
        }

        # Save performance
        start = time.time()
        result = self.brain.save("kontext", large_content, "huge.json")
        save_time = time.time() - start

        self.assertTrue(result, "5MB Save muss erfolgreich sein")
        self.assertLess(save_time, 10,
                       f"5MB Save zu langsam: {save_time:.1f}s (Max: 10s)")

        # Read performance
        start = time.time()
        loaded = self.brain.read("kontext", "huge.json")
        read_time = time.time() - start

        self.assertIsNotNone(loaded, "5MB Read muss erfolgreich sein")
        self.assertLess(read_time, 5,
                       f"5MB Read zu langsam: {read_time:.1f}s (Max: 5s)")

        print(f"    → 5MB File: Save {save_time:.2f}s, Read {read_time:.2f}s")


if __name__ == "__main__":
    unittest.main(verbosity=2)
