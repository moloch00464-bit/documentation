#!/usr/bin/env python3
"""
ADVERSARIAL SECURITY TEST - REAL EXPLOITATION ATTEMPTS
Versuche WIRKLICH Dateien außerhalb brain_dir zu schreiben
"""

import sys
import tempfile
import shutil
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from core.brain import Brain

# Setup - eigenes temp dir
test_dir = Path(tempfile.mkdtemp())
brain_dir = test_dir / "brain"
brain_dir.mkdir(parents=True, exist_ok=True)

brain = Brain(brain_dir=str(brain_dir))

print("=" * 80)
print("ADVERSARIAL REAL EXPLOITATION TEST")
print("=" * 80)
print(f"Brain dir: {brain_dir}")
print(f"Versuche zu schreiben nach: {test_dir.parent}")
print()

# Exploitation attempts
exploits = [
    ("../../../tmp/HACKED.json", "Path traversal 3 levels up"),
    ("../../../../etc/HACKED.json", "Path traversal to /etc"),
    ("/tmp/HACKED_ABSOLUTE.json", "Absolute path /tmp"),
    ("was/../../../tmp/HACKED2.json", "Category bypass"),
    ("....//....//tmp/HACKED3.json", "Double dot bypass"),
]

exploited = []
blocked = []

for payload, description in exploits:
    print(f"Testing: {description}")
    print(f"  Payload: {payload}")

    # Try to save
    result = brain.save("was", {"exploit": "test"}, payload)

    # Check if file was created OUTSIDE brain_dir
    dangerous_paths = [
        test_dir.parent / "HACKED.json",
        test_dir.parent / "HACKED_ABSOLUTE.json",
        test_dir.parent / "HACKED2.json",
        test_dir.parent / "HACKED3.json",
        Path("/tmp/HACKED_ABSOLUTE.json"),
        Path("/etc/HACKED.json"),
    ]

    exploited_this = False
    for dangerous_path in dangerous_paths:
        if dangerous_path.exists():
            exploited.append({
                "payload": payload,
                "description": description,
                "file_created": str(dangerous_path)
            })
            exploited_this = True
            print(f"  ❌ EXPLOITED! File created: {dangerous_path}")
            # Cleanup
            dangerous_path.unlink()
            break

    if not exploited_this:
        # Check if file is INSIDE brain_dir (safe)
        files_in_brain = list(brain_dir.rglob("*.json"))
        if any(files_in_brain):
            # File created, but inside brain_dir = safe
            blocked.append({"payload": payload, "description": description})
            print(f"  ✅ BLOCKED - File stayed inside brain_dir")
        else:
            # No file created at all = also safe
            blocked.append({"payload": payload, "description": description})
            print(f"  ✅ BLOCKED - No file created")

    print()

# Cleanup
shutil.rmtree(test_dir)

print("=" * 80)
print(f"RESULTS:")
print(f"  Blocked: {len(blocked)}")
print(f"  Exploited: {len(exploited)}")
print("=" * 80)

if exploited:
    print()
    print("❌ CRITICAL SECURITY FAILURE!")
    print()
    print("Successfully exploited:")
    for exploit in exploited:
        print(f"  - {exploit['description']}")
        print(f"    Payload: {exploit['payload']}")
        print(f"    Created: {exploit['file_created']}")
    print()
    sys.exit(1)
else:
    print()
    print("✅ ALL EXPLOITATION ATTEMPTS BLOCKED")
    print("   No files created outside brain_dir")
    print()
    sys.exit(0)
