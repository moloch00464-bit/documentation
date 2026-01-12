#!/usr/bin/env python3
"""
Test Memory Monitoring Feature
Zeigt wie Memory Usage tracking funktioniert
"""

import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from core.memory import Memory

print("=" * 80)
print("M.O.L.O.C.H. 3.0 - MEMORY MONITORING TEST")
print("=" * 80)
print()

# Setup
test_dir = Path(tempfile.mkdtemp())
history_file = test_dir / "history.json"
memory_file = test_dir / "langzeit.json"

memory = Memory(history_file=history_file, memory_file=memory_file)

# Test 1: Empty memory
print("TEST 1: Empty Memory")
print("-" * 80)
usage = memory.get_memory_usage()
print(f"History:         {usage['history_count']} messages")
print(f"Langzeit:        {usage['langzeit_count']} entries")
print(f"Estimated RAM:   {usage['estimated_mb']:.2f} MB")
print(f"Pi 5 Capacity:   {usage['capacity_percent']:.2f}%")
print(f"Status:          {usage['status']}")
print(f"Message:         {usage['message']}")
print(f"Note:            {usage['note']}")
print()

# Test 2: 1,000 messages
print("TEST 2: After 1,000 Messages")
print("-" * 80)
for i in range(1000):
    memory.add_to_history("user", f"Message {i}: " + "x" * 100)

usage = memory.get_memory_usage()
print(f"History:         {usage['history_count']} messages")
print(f"Estimated RAM:   {usage['estimated_mb']:.2f} MB")
print(f"Pi 5 Capacity:   {usage['capacity_percent']:.2f}%")
print(f"Status:          {usage['status']}")
print(f"Message:         {usage['message']}")
print(f"Capacity Info:   {usage['capacity_info']}")
print()

# Test 3: 10,000 messages
print("TEST 3: After 10,000 Messages")
print("-" * 80)
for i in range(9000):  # Add 9000 more (total 10k)
    memory.add_to_history("user", f"Message {1000+i}: " + "x" * 100)

usage = memory.get_memory_usage()
print(f"History:         {usage['history_count']} messages")
print(f"Estimated RAM:   {usage['estimated_mb']:.2f} MB")
print(f"Pi 5 Capacity:   {usage['capacity_percent']:.2f}%")
print(f"Remaining RAM:   {usage['remaining_mb']:.2f} MB")
print(f"Status:          {usage['status']}")
print(f"Message:         {usage['message']}")
print(f"Capacity Info:   {usage['capacity_info']}")
print()

# Test 4: 50,000 messages (high usage)
print("TEST 4: After 50,000 Messages (Simulation)")
print("-" * 80)
print("(Simuliert, nicht wirklich hinzugefügt für schnelleren Test)")
# Simuliere 50k messages
simulated_count = 50000
simulated_mb = (simulated_count * 1024) / (1024 * 1024)
simulated_percent = (simulated_mb / 4096) * 100
print(f"History:         {simulated_count} messages")
print(f"Estimated RAM:   {simulated_mb:.2f} MB")
print(f"Pi 5 Capacity:   {simulated_percent:.2f}%")
print(f"Remaining RAM:   {4096 - simulated_mb:.2f} MB")

if simulated_percent < 50:
    print(f"Status:          ok")
    print(f"Message:         System läuft gut mit {simulated_count} messages")
elif simulated_percent < 75:
    print(f"Status:          high")
    print(f"Message:         ⚠️ Viel History, aber OK")
else:
    print(f"Status:          critical")
    print(f"Message:         ⚠️ Sehr große History!")

print()

# Test 5: 1 Million messages (theoretical)
print("TEST 5: Nach 1,000,000 Messages (Theoretisch)")
print("-" * 80)
million_count = 1000000
million_mb = (million_count * 1024) / (1024 * 1024)
million_percent = (million_mb / 4096) * 100
print(f"History:         {million_count:,} messages")
print(f"Estimated RAM:   {million_mb:.2f} MB")
print(f"Pi 5 Capacity:   {million_percent:.2f}%")
print(f"Remaining RAM:   {4096 - million_mb:.2f} MB")
print()

if million_mb < 4096:
    print(f"✅ Pi 5 kann {million_count:,} messages handeln!")
    print(f"   Das sind ~{million_count // 365 // 100} messages pro Tag über Jahre")
else:
    print(f"⚠️  {million_count:,} messages würden Pi 5 RAM übersteigen")

print()
print("=" * 80)
print("MEMORY MONITORING FEATURES:")
print("=" * 80)
print("✅ Tracked: Message count, RAM usage, % capacity")
print("✅ Status: 'ok' | 'high' | 'critical' (info only)")
print("✅ Estimates: Time until full (Jahre/Monate/Tage)")
print("✅ Design: Unbounded growth - System limitiert NICHT")
print("✅ Purpose: Monitoring & reporting, kein Auto-Cleanup")
print()
print("WICHTIG: Memory wächst unbegrenzt (BY DESIGN)")
print("         M.O.L.O.C.H. soll sich an ALLES erinnern!")
print("=" * 80)

# Cleanup
import shutil
shutil.rmtree(test_dir)
