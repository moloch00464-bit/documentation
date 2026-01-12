#!/usr/bin/env python3
"""
ADVERSARIAL MEMORY LEAK TEST
100k messages - does Memory grow unbounded?
"""

import sys
import gc
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from core.memory import Memory

# Setup
test_dir = Path(tempfile.mkdtemp())
history_file = test_dir / "history.json"
memory_file = test_dir / "langzeit.json"

memory = Memory(history_file=history_file, memory_file=memory_file)

print("=" * 80)
print("ADVERSARIAL MEMORY LEAK TEST")
print("=" * 80)
print("Adding 100,000 messages and monitoring growth...")
print()

# Baseline
gc.collect()
baseline_objects = len(gc.get_objects())

print(f"Baseline: {baseline_objects} objects in memory")
print()

# Track growth
growth_data = []

for i in range(100000):
    memory.add_to_history("user", f"Message {i}: " + "x" * 100)

    # Check every 10k messages
    if (i + 1) % 10000 == 0:
        gc.collect()
        current_objects = len(gc.get_objects())
        growth = current_objects - baseline_objects
        history_size = len(memory.history)

        growth_data.append({
            "messages": i + 1,
            "objects": current_objects,
            "growth": growth,
            "history_size": history_size
        })

        print(f"After {i+1:6d} messages:")
        print(f"  Objects:      {current_objects:8d} (+{growth:6d})")
        print(f"  History size: {history_size:8d}")
        print()

# Cleanup
import shutil
shutil.rmtree(test_dir)

print("=" * 80)
print("ANALYSIS:")
print("=" * 80)

# Check if growth is linear (acceptable) or exponential (leak)
if len(growth_data) >= 2:
    first = growth_data[0]
    last = growth_data[-1]

    messages_ratio = last["messages"] / first["messages"]
    growth_ratio = last["growth"] / first["growth"] if first["growth"] > 0 else 0

    print(f"Messages grew:    {messages_ratio:.1f}x ({first['messages']} → {last['messages']})")
    print(f"Object count grew: {growth_ratio:.1f}x ({first['growth']} → {last['growth']})")
    print()

    # Linear growth is OK (O(n))
    # Super-linear growth (>2x) indicates leak
    if growth_ratio > messages_ratio * 1.5:
        print("❌ FAIL: Super-linear growth detected!")
        print(f"   Objects grew {growth_ratio:.1f}x while messages grew {messages_ratio:.1f}x")
        print("   Possible memory leak")
        sys.exit(1)
    else:
        print("✅ PASS: Linear growth (acceptable)")
        print("   Memory grows proportionally with data size")
        print()

        # Check if history has a limit
        if last["history_size"] == last["messages"]:
            print("⚠️  WARNING: No history size limit detected")
            print("   Memory will grow unbounded in long-running processes")
            print("   Consider implementing history rotation/truncation")
        else:
            print("✅ History limit active")
            print(f"   Keeping {last['history_size']} of {last['messages']} messages")

        sys.exit(0)
else:
    print("⚠️  Not enough data to analyze")
    sys.exit(0)
