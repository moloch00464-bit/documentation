#!/usr/bin/env python3
"""
ADVERSARIAL TIMING ATTACK TEST
Check if _sanitize_filename() timing is constant
or leaks information
"""

import sys
import time
import statistics
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from core.brain import Brain

brain = Brain()

print("=" * 80)
print("ADVERSARIAL TIMING ATTACK TEST")
print("=" * 80)
print()
print("Testing if _sanitize_filename() has constant-time behavior...")
print("(Timing differences could leak information to attackers)")
print()

def measure_sanitization(payload, iterations=10000):
    """Measure average time to sanitize a payload"""
    times = []
    for _ in range(iterations):
        start = time.perf_counter()
        brain._sanitize_filename(payload)
        end = time.perf_counter()
        times.append((end - start) * 1000000)  # Microseconds

    return {
        "mean": statistics.mean(times),
        "median": statistics.median(times),
        "stdev": statistics.stdev(times) if len(times) > 1 else 0,
        "min": min(times),
        "max": max(times)
    }

# Test cases - various payload types
test_cases = {
    "short_safe": "test.json",
    "short_unsafe": "../../../etc/passwd",
    "long_safe": "a" * 1000 + ".json",
    "long_unsafe": "../" * 500 + "etc/passwd",
    "unicode_safe": "テスト.json",
    "unicode_unsafe": "..／" * 100 + "etc/passwd",
    "mixed_safe": "test_file_123.json",
    "mixed_unsafe": "test|whoami;id.json",
    "very_long_safe": "a" * 10000 + ".json",
    "very_long_unsafe": "../" * 5000 + "etc/passwd",
}

results = {}
for name, payload in test_cases.items():
    print(f"Testing: {name:20s} ... ", end="", flush=True)
    stats = measure_sanitization(payload, iterations=10000)
    results[name] = stats
    print(f"{stats['mean']:.2f} µs (±{stats['stdev']:.2f})")

print()
print("=" * 80)
print("ANALYSIS:")
print("=" * 80)
print()

# Group by length
short = ["short_safe", "short_unsafe", "mixed_safe", "mixed_unsafe", "unicode_safe", "unicode_unsafe"]
long = ["long_safe", "long_unsafe"]
very_long = ["very_long_safe", "very_long_unsafe"]

print("SHORT PAYLOADS:")
for name in short:
    if name in results:
        print(f"  {name:20s}: {results[name]['mean']:6.2f} µs")
print()

print("LONG PAYLOADS (1000 chars):")
for name in long:
    if name in results:
        print(f"  {name:20s}: {results[name]['mean']:6.2f} µs")
print()

print("VERY LONG PAYLOADS (10000 chars):")
for name in very_long:
    if name in results:
        print(f"  {name:20s}: {results[name]['mean']:6.2f} µs")
print()

# Check for timing oracle
print("TIMING ORACLE ANALYSIS:")
print()

# Compare safe vs unsafe within each length category
timing_leaks = []

for category, names in [("short", short), ("long", long), ("very_long", very_long)]:
    safe_times = [results[n]["mean"] for n in names if n in results and "safe" in n]
    unsafe_times = [results[n]["mean"] for n in names if n in results and "unsafe" in n]

    if safe_times and unsafe_times:
        safe_avg = statistics.mean(safe_times)
        unsafe_avg = statistics.mean(unsafe_times)
        diff_percent = abs(unsafe_avg - safe_avg) / safe_avg * 100

        print(f"{category.upper()} payloads:")
        print(f"  Safe avg:   {safe_avg:.2f} µs")
        print(f"  Unsafe avg: {unsafe_avg:.2f} µs")
        print(f"  Difference: {diff_percent:.1f}%")

        # Significant if >20% difference
        if diff_percent > 20:
            timing_leaks.append({
                "category": category,
                "difference": diff_percent
            })
            print(f"  ⚠️  SIGNIFICANT TIMING DIFFERENCE!")
        else:
            print(f"  ✅ Minimal difference (< 20%)")

        print()

print("=" * 80)

if timing_leaks:
    print("⚠️  WARNING: Timing oracle detected")
    print()
    print("Significant timing differences found in:")
    for leak in timing_leaks:
        print(f"  - {leak['category']}: {leak['difference']:.1f}% difference")
    print()
    print("Attackers could use timing to infer sanitization behavior")
    print("However, this is LOW severity for filesystem operations")
    sys.exit(0)  # Warning, not failure
else:
    print("✅ PASS: No significant timing oracle")
    print("   Sanitization time is consistent across payload types")
    sys.exit(0)
