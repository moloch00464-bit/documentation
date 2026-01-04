#!/usr/bin/env python3
"""
M.O.L.O.C.H. 3.0 - Text I/O
============================
Simple text input/output
"""


class TextIO:
    """
    Text Input/Output for M.O.L.O.C.H. 3.0

    Simple wrapper for terminal I/O
    """

    @staticmethod
    def input(prompt: str = "") -> str:
        """
        Get user text input

        Args:
            prompt: Optional prompt to show

        Returns:
            User input string
        """
        try:
            if prompt:
                return input(prompt)
            else:
                return input()
        except KeyboardInterrupt:
            print("\n\n⚠️ Interrupted")
            return ""
        except EOFError:
            return ""

    @staticmethod
    def output(text: str, prefix: str = ""):
        """
        Print text to terminal

        Args:
            text: Text to print
            prefix: Optional prefix (e.g., "🤖 ")
        """
        if prefix:
            print(f"{prefix}{text}")
        else:
            print(text)

    @staticmethod
    def output_multiline(lines: list, prefix: str = ""):
        """
        Print multiple lines

        Args:
            lines: List of lines to print
            prefix: Optional prefix for each line
        """
        for line in lines:
            TextIO.output(line, prefix)


# ═══════════════════════════════════════════════════════════════════════════════
# TESTING
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("\n💬 M.O.L.O.C.H. 3.0 Text I/O Test\n")

    # Test output
    print("📝 Testing output...")
    TextIO.output("Test message", prefix="🤖 ")
    print("   ✅ Output works")

    # Test multiline
    print("\n📝 Testing multiline...")
    TextIO.output_multiline([
        "Line 1",
        "Line 2",
        "Line 3"
    ], prefix="  - ")
    print("   ✅ Multiline works")

    # Note: Input test requires user interaction
    print("\n💡 Input test requires user interaction - skipped")

    print()
