#!/usr/bin/env python3
"""
M.O.L.O.C.H. 3.0 - UNICODE EDGE CASES TESTS
============================================
Tests für Unicode und Special Characters

PRODUCTION HARDENING PROTOCOL:
- Umlaute (äöüÄÖÜß) müssen funktionieren
- Emojis müssen funktionieren (🖤😈🔥💀🚀)
- Internationaler Text (Chinese, Arabic, Russian, etc.)
- Math symbols, Currency, RTL text
- Null bytes und andere Edge Cases

Critical für Industrial Use:
- Internationales Team
- Verschiedene Sprachen
- Emoji-Kommunikation (Gen-Z Workers!)

Author: Claude
Date: 2026-01-12
"""

import sys
import unittest
import tempfile
import shutil
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.brain import Brain


class TestUnicodeEdgeCases(unittest.TestCase):
    """Tests für Unicode und Special Characters"""

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

    def test_unicode_comprehensive(self):
        """Alle Unicode Edge Cases"""
        test_cases = {
            "umlaute": "äöüÄÖÜß",
            "emoji": "🖤😈🔥💀🚀",
            "chinese": "中文测试",
            "arabic": "اختبار",
            "russian": "тест",
            "japanese": "テスト",
            "korean": "테스트",
            "math": "∑∏∫∂√∞",
            "currency": "€£¥₿",
            "special": "™®©℗",
            "zalgo": "H̷̲̎ë̴̢l̶̰̀l̸̥̾o̴̱͝",
            "rtl": "مرحبا",  # Right-to-left
            "mixed": "Hello مرحبا 你好 🌍",
            "null_char": "test\x00test",  # Null byte - MUSS gehandled werden
            "newlines": "line1\nline2\r\nline3",
            "tabs": "col1\tcol2\tcol3",
            "quotes": "\"quoted\" and 'single'",
            "backslash": "path\\to\\file",
            "combined": "äöü🔥中文€∑",  # Mix everything
        }

        for name, value in test_cases.items():
            content = {
                "type": name,
                "value": value,
                "length": len(value)
            }

            # Save
            result = self.brain.save("was", content, f"unicode_{name}.json")
            self.assertTrue(result, f"Failed to save: {name} = {repr(value)}")

            # Read
            loaded = self.brain.read("was", f"unicode_{name}.json")
            self.assertIsNotNone(loaded, f"Failed to read: {name} = {repr(value)}")

            # Validate content
            # Null char könnte sanitized werden - das ist OK
            if name != "null_char":
                self.assertEqual(
                    loaded["content"]["value"], value,
                    f"Value mismatch for {name}: expected {repr(value)}, got {repr(loaded['content']['value'])}"
                )
            else:
                # Null char muss entweder gleich sein ODER sanitized
                loaded_value = loaded["content"]["value"]
                self.assertTrue(
                    loaded_value == value or "\x00" not in loaded_value,
                    f"Null char nicht richtig gehandled: {repr(loaded_value)}"
                )

        print(f"    → {len(test_cases)} Unicode test cases PASSED")

    def test_unicode_in_keys(self):
        """Unicode auch in Keys, nicht nur Values"""
        content = {
            "äöü": "umlaute_key",
            "🔥emoji": "emoji_key",
            "中文": "chinese_key",
            "normal": "works too"
        }

        result = self.brain.save("was", content, "unicode_keys.json")
        self.assertTrue(result, "Unicode in keys muss funktionieren")

        loaded = self.brain.read("was", "unicode_keys.json")
        self.assertIsNotNone(loaded, "Read mit Unicode keys muss funktionieren")

        # Verify keys
        self.assertIn("äöü", loaded["content"], "Umlaut key fehlt")
        self.assertIn("🔥emoji", loaded["content"], "Emoji key fehlt")
        self.assertIn("中文", loaded["content"], "Chinese key fehlt")

    def test_unicode_filename(self):
        """Unicode auch in Dateinamen (wenn filesystem unterstützt)"""
        unicode_filenames = [
            "test_äöü.json",
            "test_中文.json",
            "test_🔥.json",  # Emoji in filename - möglicherweise nicht supported
        ]

        for filename in unicode_filenames:
            try:
                result = self.brain.save("was", {"unicode_filename": True}, filename)

                # Wenn save erfolgreich war, muss read auch funktionieren
                if result:
                    loaded = self.brain.read("was", filename)
                    self.assertIsNotNone(loaded,
                                        f"Unicode filename save/read failed: {filename}")
            except (OSError, ValueError) as e:
                # Filesystem unterstützt möglicherweise nicht alle Unicode chars in Namen
                # Das ist OK - wir testen nur dass es nicht crasht
                pass


if __name__ == "__main__":
    unittest.main(verbosity=2)
