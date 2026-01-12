#!/usr/bin/env python3
"""
ADVERSARIAL SECURITY TEST
Versuche _sanitize_filename() zu umgehen
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from core.brain import Brain

# Setup
brain = Brain()

def is_truly_safe(filename):
    """
    Check if filename is TRULY safe

    Unsafe if:
    - Contains path traversal (../, ..\)
    - Contains absolute paths (/, C:\)
    - Contains command injection chars (|, ;, $, `)
    - Contains null bytes
    - Is empty or only dots
    """
    if not filename or filename in ['.', '..']:
        return False

    # Check for path traversal
    if '..' in filename:
        return False

    # Check for absolute paths
    if filename.startswith('/') or (len(filename) > 1 and filename[1] == ':'):
        return False

    # Check for dangerous chars
    dangerous = ['|', ';', '&', '$', '`', '\x00', '\n', '\r', '<', '>']
    for char in dangerous:
        if char in filename:
            return False

    return True


# Adversarial payloads
adversarial_filenames = [
    # Double encoding
    "%2e%2e%2f%2e%2e%2fetc/passwd",
    "..%2f..%2fetc/passwd",

    # Unicode path traversal
    "..／..／etc/passwd",  # Fullwidth slash
    "。。/。。/etc/passwd",  # Japanese dots

    # Null byte injection
    "evil.json\x00.txt",

    # Overlong UTF-8
    "\xc0\xae\xc0\xae/etc/passwd",

    # Mixed case bypass
    "....//....//etc/passwd",

    # Windows specific
    "....\\....\\etc\\passwd",
    "..../..../etc/passwd",

    # URL encoded
    "..%252f..%252fetc/passwd",

    # Unicode normalization attack
    "ＮＵＬ",  # Fullwidth NUL

    # Length overflow
    "a" * 10000 + ".json",

    # Combined attacks
    "../\x00/etc/passwd",
    "test|whoami.json",
    "test;id.json",
    "$(whoami).json",
    "`id`.json",
    "test\ntest.json",

    # Edge cases
    "...",
    ".",
    "..",
    "....",
    "/..",
    "../",
    "\\..\\",

    # Absolute paths
    "/etc/passwd",
    "C:\\Windows\\System32",
    "//etc/passwd",
    "\\\\etc\\passwd",
]

print("=" * 80)
print("ADVERSARIAL SECURITY TEST - FILENAME SANITIZATION")
print("=" * 80)
print()

failed_count = 0
passed_count = 0

for payload in adversarial_filenames:
    result = brain._sanitize_filename(payload)
    safe = is_truly_safe(result)

    status = "✅ SAFE" if safe else "❌ UNSAFE"

    if not safe:
        failed_count += 1
        print(f"{status} | INPUT:  {repr(payload)[:60]}")
        print(f"       | OUTPUT: {repr(result)[:60]}")
        print(f"       | REASON: Output still contains dangerous patterns")
        print()
    else:
        passed_count += 1

print("=" * 80)
print(f"RESULTS: {passed_count} passed, {failed_count} failed")
print("=" * 80)

if failed_count > 0:
    print("❌ ADVERSARIAL TEST FAILED - Sanitization can be bypassed!")
    sys.exit(1)
else:
    print("✅ ADVERSARIAL TEST PASSED - All payloads neutralized")
    sys.exit(0)
