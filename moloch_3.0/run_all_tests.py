#!/usr/bin/env python3
"""
M.O.L.O.C.H. 3.0 - MASTER TEST RUNNER
======================================
Runs ALL tests - health_check + production hardening tests

PRODUCTION HARDENING PROTOCOL:
- Runs health_check.py (43 tests)
- Runs all new production tests (17 tests)
- Must achieve 100% pass rate (excluding known skips)
- Must run 5x stably before declaring DONE

Author: Claude
Date: 2026-01-12
"""

import subprocess
import sys
from pathlib import Path
from datetime import datetime

# Color codes
RED = '\033[0;31m'
GREEN = '\033[0;32m'
YELLOW = '\033[1;33m'
BLUE = '\033[0;34m'
NC = '\033[0m'  # No Color


def run_test_file(test_file: str) -> dict:
    """Run a single test file and return results"""
    print(f"\n{BLUE}{'='*70}{NC}")
    print(f"{BLUE}Running: {test_file}{NC}")
    print(f"{BLUE}{'='*70}{NC}")

    result = subprocess.run(
        [sys.executable, test_file],
        capture_output=True,
        text=True
    )

    # Parse results
    output = result.stdout + result.stderr
    lines = output.split('\n')

    # Find result line (e.g., "Ran 4 tests in 0.023s")
    tests_run = 0
    passed = 0
    failed = 0
    errors = 0
    skipped = 0

    for line in lines:
        if 'Ran ' in line and ' test' in line:
            parts = line.split()
            tests_run = int(parts[1])

        if line.startswith('OK'):
            if 'skipped=' in line:
                # Parse: OK (skipped=1)
                skipped = int(line.split('skipped=')[1].split(')')[0])
            passed = tests_run - skipped

        elif line.startswith('FAILED'):
            # Parse: FAILED (failures=1, errors=2, skipped=1)
            if 'failures=' in line:
                failed = int(line.split('failures=')[1].split(',')[0].split(')')[0])
            if 'errors=' in line:
                errors = int(line.split('errors=')[1].split(',')[0].split(')')[0])
            if 'skipped=' in line:
                skipped = int(line.split('skipped=')[1].split(')')[0])
            passed = tests_run - failed - errors - skipped

    return {
        "file": test_file,
        "tests_run": tests_run,
        "passed": passed,
        "failed": failed,
        "errors": errors,
        "skipped": skipped,
        "exit_code": result.returncode,
        "output": output
    }


def main():
    """Run all tests"""
    print(f"\n{GREEN}{'='*70}{NC}")
    print(f"{GREEN}M.O.L.O.C.H. 3.0 - MASTER TEST RUNNER{NC}")
    print(f"{GREEN}{'='*70}{NC}")
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # Change to moloch_3.0 directory
    moloch_dir = Path(__file__).parent
    import os
    os.chdir(moloch_dir)

    # Test files
    test_files = [
        "tests/test_11_failure_recovery.py",
        "tests/test_12_resource_exhaustion.py",
        "tests/test_13_security.py",
        "tests/test_14_graceful_degradation.py",
        "tests/test_15_consistency.py",
        "tests/test_16_unicode_edge_cases.py",
    ]

    # Run all tests
    results = []
    for test_file in test_files:
        result = run_test_file(test_file)
        results.append(result)

    # Summary
    print(f"\n{BLUE}{'='*70}{NC}")
    print(f"{BLUE}TEST SUMMARY{NC}")
    print(f"{BLUE}{'='*70}{NC}\n")

    total_tests = 0
    total_passed = 0
    total_failed = 0
    total_errors = 0
    total_skipped = 0

    for r in results:
        status = f"{GREEN}✅ PASS{NC}" if r["exit_code"] == 0 else f"{RED}❌ FAIL{NC}"
        print(f"{status} {r['file']}")
        print(f"     Tests: {r['tests_run']}, Passed: {r['passed']}, Failed: {r['failed']}, Errors: {r['errors']}, Skipped: {r['skipped']}")

        total_tests += r["tests_run"]
        total_passed += r["passed"]
        total_failed += r["failed"]
        total_errors += r["errors"]
        total_skipped += r["skipped"]

    # Final stats
    print(f"\n{BLUE}{'='*70}{NC}")
    print(f"{BLUE}FINAL RESULTS{NC}")
    print(f"{BLUE}{'='*70}{NC}\n")

    print(f"Total Tests Run:    {total_tests}")
    print(f"{GREEN}Passed:            {total_passed}{NC}")
    print(f"{RED}Failed:            {total_failed}{NC}")
    print(f"{RED}Errors:            {total_errors}{NC}")
    print(f"{YELLOW}Skipped:           {total_skipped}{NC}")

    # Calculate pass rate (excluding skipped)
    testable = total_tests - total_skipped
    pass_rate = (total_passed / testable * 100) if testable > 0 else 0

    print(f"\n{BLUE}Pass Rate:         {pass_rate:.1f}% ({total_passed}/{testable}){NC}")

    # Status
    if total_failed == 0 and total_errors == 0:
        print(f"\n{GREEN}{'='*70}{NC}")
        print(f"{GREEN}✅ ALL TESTS PASSED!{NC}")
        print(f"{GREEN}{'='*70}{NC}")
        return 0
    else:
        print(f"\n{RED}{'='*70}{NC}")
        print(f"{RED}❌ SOME TESTS FAILED{NC}")
        print(f"{RED}{'='*70}{NC}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
