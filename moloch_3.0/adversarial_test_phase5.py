#!/usr/bin/env python3
"""
ADVERSARIAL CORRUPT FILE TEST
Test Brain with EVERY kind of corrupted JSON
"""

import sys
import tempfile
import shutil
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from core.brain import Brain

# Setup
test_dir = Path(tempfile.mkdtemp())
brain_dir = test_dir / "brain"
brain_dir.mkdir(parents=True, exist_ok=True)

brain = Brain(brain_dir=str(brain_dir))

print("=" * 80)
print("ADVERSARIAL CORRUPT FILE TEST")
print("=" * 80)
print()

# Corrupt file test cases
corrupt_files = {
    # Empty file
    "empty.json": "",

    # Only whitespace
    "whitespace.json": "   \n\t  ",

    # Almost valid JSON
    "almost_valid.json": '{"content": {"test": true}',  # Missing }

    # Binary garbage
    "binary.json": b'\x00\x01\x02\xff\xfe'.decode('latin-1', errors='replace'),

    # Huge number
    "huge_number.json": '{"value": ' + '9' * 10000 + '}',

    # Deeply nested (JSON bomb)
    "nested.json": '{"a":' * 1000 + '1' + '}' * 1000,

    # Unicode BOM
    "bom.json": '\ufeff{"content": {}}',

    # Null bytes in JSON
    "null_bytes.json": '{"content": "test\x00test"}',

    # Truncated UTF-8
    "truncated_utf8.json": '{"text": "' + '\xc3' + '"}',  # Incomplete UTF-8

    # Only opening brace
    "only_brace.json": "{",

    # Only closing brace
    "only_close.json": "}",

    # Array instead of object
    "array.json": '[1, 2, 3]',

    # String instead of object
    "string.json": '"just a string"',

    # Number
    "number.json": "42",

    # Boolean
    "boolean.json": "true",

    # Null
    "null.json": "null",

    # Multiple JSON objects
    "multiple.json": '{"a": 1}\n{"b": 2}',

    # Comments (invalid JSON)
    "comments.json": '{"test": "value"} // comment',

    # Trailing comma
    "trailing_comma.json": '{"test": "value",}',

    # Single quotes (invalid JSON)
    "single_quotes.json": "{'test': 'value'}",

    # Unquoted keys
    "unquoted_keys.json": '{test: "value"}',
}

crashed = []
handled = []

for filename, content in corrupt_files.items():
    # Write corrupt file directly (bypass Brain.save())
    category_path = brain.brain_dir / "was"
    category_path.mkdir(parents=True, exist_ok=True)
    file_path = category_path / filename

    try:
        with open(file_path, 'w', encoding='utf-8', errors='replace') as f:
            f.write(content)
    except Exception as e:
        print(f"⚠️  Could not write {filename}: {e}")
        continue

    # Try to read it
    try:
        result = brain.read("was", filename)

        if result is None:
            # Graceful failure - returned None
            handled.append(filename)
            print(f"✅ {filename:25s} → Gracefully returned None")
        elif isinstance(result, dict) and "_error" in result:
            # Graceful failure with error info
            handled.append(filename)
            print(f"✅ {filename:25s} → Returned error dict")
        else:
            # Successfully parsed (somehow)
            handled.append(filename)
            print(f"✅ {filename:25s} → Parsed as {type(result).__name__}")

    except Exception as e:
        # CRASH - unhandled exception
        crashed.append({
            "filename": filename,
            "exception": f"{type(e).__name__}: {e}"
        })
        print(f"❌ {filename:25s} → CRASHED: {type(e).__name__}")

# Cleanup
shutil.rmtree(test_dir)

print()
print("=" * 80)
print("RESULTS:")
print("=" * 80)
print(f"Handled gracefully: {len(handled)}/{len(corrupt_files)}")
print(f"Crashed:            {len(crashed)}/{len(corrupt_files)}")
print()

if crashed:
    print("CRASHES:")
    for crash in crashed:
        print(f"  - {crash['filename']}")
        print(f"    {crash['exception']}")
    print()

print("=" * 80)

if crashed:
    print("❌ FAIL: Brain crashes on some corrupt files")
    print("   All corrupt files must be handled gracefully")
    sys.exit(1)
else:
    print("✅ PASS: All corrupt files handled gracefully")
    print("   No crashes, no unhandled exceptions")
    sys.exit(0)
