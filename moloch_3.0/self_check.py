#!/usr/bin/env python3
"""
M.O.L.O.C.H. 3.0 - Self-Check Script
======================================
Testet ALLE Funktionen & Tools systematisch
M.O.L.O.C.H. kann das selbst aufrufen!
"""

import sys
import os
from pathlib import Path

# Add to path
sys.path.insert(0, os.path.expanduser("~/documentation/moloch_3.0"))

from core.config import ANTHROPIC_API_KEY, DATA_DIR
from core.brain import Brain
from core.memory import Memory
from core.learning import PersistentLearning
from core.voice_settings import VoiceSettings
from core.location import LocationTracker
from core.tools import MOLOCH_TOOLS, execute_tool
from tools.bash import BashTool
from tools.files import FileTool
from tools.web import WebTool
from tools.search import SearchTool
import json


def print_header(text):
    """Print fancy header"""
    print(f"\n{'='*60}")
    print(f"  {text}")
    print(f"{'='*60}\n")


def test_api_key():
    """Test API key"""
    print("🔑 Testing API Key...")
    if ANTHROPIC_API_KEY and len(ANTHROPIC_API_KEY) > 20:
        print(f"   ✅ API Key configured ({len(ANTHROPIC_API_KEY)} chars)")
        return True
    else:
        print("   ❌ API Key missing or too short!")
        return False


def test_directories():
    """Test directory structure"""
    print("📁 Testing Directory Structure...")

    dirs_to_check = [
        DATA_DIR,
        DATA_DIR / "brain",
        DATA_DIR / "brain" / "personen",
        DATA_DIR / "brain" / "orte",
        DATA_DIR / "brain" / "projekte",
        DATA_DIR / "brain" / "themen",
        DATA_DIR / "brain" / "wichtig",
    ]

    all_ok = True
    for dir_path in dirs_to_check:
        if dir_path.exists():
            print(f"   ✅ {dir_path}")
        else:
            print(f"   ❌ Missing: {dir_path}")
            all_ok = False

    return all_ok


def test_brain():
    """Test Brain system"""
    print("🧠 Testing Brain System...")

    try:
        brain = Brain()

        # Test save
        test_data = {"test": "self_check", "timestamp": "now"}
        brain.save("wichtig", test_data, "self_check_test.json")
        print("   ✅ Brain save works")

        # Test list
        files = brain.list_category("wichtig")
        print(f"   ✅ Brain list works ({len(files)} files)")

        # Test find
        results = brain.find("self_check", kategorie="wichtig")
        print(f"   ✅ Brain find works ({len(results)} results)")

        # Cleanup
        test_file = DATA_DIR / "brain" / "wichtig" / "self_check_test.json"
        if test_file.exists():
            test_file.unlink()
            print("   ✅ Cleanup successful")

        return True

    except Exception as e:
        print(f"   ❌ Brain error: {e}")
        return False


def test_memory():
    """Test Memory system"""
    print("💾 Testing Memory System...")

    try:
        memory = Memory()

        # Check history
        print(f"   ✅ History loaded ({len(memory.history)} entries)")

        # Check langzeit
        print(f"   ✅ Langzeit loaded ({len(memory.langzeit)} entries)")

        return True

    except Exception as e:
        print(f"   ❌ Memory error: {e}")
        return False


def test_learning():
    """Test Learning system"""
    print("📚 Testing Learning System...")

    try:
        learning = PersistentLearning()

        # Get facts
        facts = learning.get_facts()
        print(f"   ✅ Facts loaded ({len(facts)} facts)")

        # Test add
        learning.learn_fact("Self-check test fact", "system", 5)
        print("   ✅ Learning save works")

        return True

    except Exception as e:
        print(f"   ❌ Learning error: {e}")
        return False


def test_voice_settings():
    """Test Voice settings"""
    print("🎤 Testing Voice Settings...")

    try:
        voice_settings = VoiceSettings(DATA_DIR)

        pitch = voice_settings.get_pitch()
        rate = voice_settings.get_rate()

        print(f"   ✅ Voice settings loaded (Pitch: {pitch}, Rate: {rate})")

        return True

    except Exception as e:
        print(f"   ❌ Voice settings error: {e}")
        return False


def test_location():
    """Test Location (GPS)"""
    print("📍 Testing Location/GPS...")

    try:
        location = LocationTracker()

        # Try to get location (with short timeout)
        current = location.get_current_location(timeout=5)

        if current:
            print(f"   ✅ GPS works: {current.get('city', 'Unknown')}")
            print(f"      Coordinates: {current.get('lat'):.2f}, {current.get('lon'):.2f}")
            return True
        else:
            print("   ⚠️ GPS timeout (acceptable)")

            # Check last known
            last = location.get_last_location()
            if last:
                print(f"   ✅ Last location available: {last.get('city', 'Unknown')}")
                return True
            else:
                print("   ❌ No location data available")
                return False

    except Exception as e:
        print(f"   ❌ Location error: {e}")
        return False


def test_bash_tool():
    """Test Bash tool"""
    print("⚡ Testing Bash Tool...")

    try:
        bash = BashTool()

        # Test safe command
        stdout, stderr, code = bash.execute("echo 'test'", timeout=5)
        if code == 0 and "test" in stdout:
            print("   ✅ Bash execution works")
        else:
            print(f"   ❌ Bash failed: {stderr}")
            return False

        # Test safety check
        if not bash.is_safe("rm -rf /"):
            print("   ✅ Safety checks work (blocked dangerous command)")
        else:
            print("   ❌ Safety check failed!")
            return False

        return True

    except Exception as e:
        print(f"   ❌ Bash tool error: {e}")
        return False


def test_file_tool():
    """Test File tool"""
    print("📄 Testing File Tool...")

    try:
        files = FileTool()

        # Test write
        test_file = "/tmp/moloch_self_check.txt"
        success = files.write(test_file, "Self-check test", backup=False)
        if success:
            print("   ✅ File write works")
        else:
            print("   ❌ File write failed")
            return False

        # Test read
        content = files.read(test_file)
        if content and "Self-check" in content:
            print("   ✅ File read works")
        else:
            print("   ❌ File read failed")
            return False

        # Cleanup
        import os
        os.remove(test_file)
        print("   ✅ Cleanup successful")

        return True

    except Exception as e:
        print(f"   ❌ File tool error: {e}")
        return False


def test_web_tool():
    """Test Web tool (requires internet!)"""
    print("🌐 Testing Web Tool...")

    try:
        web = WebTool()

        # Test search
        results = web.search("Python programming", max_results=3)

        if results and len(results) > 0:
            print(f"   ✅ Web search works ({len(results)} results)")
            print(f"      First result: {results[0].get('title', 'N/A')[:50]}...")
            return True
        else:
            print("   ⚠️ Web search returned no results (might be offline)")
            return False

    except Exception as e:
        print(f"   ❌ Web tool error: {e}")
        return False


def test_search_tool():
    """Test Code search tool"""
    print("🔍 Testing Search Tool...")

    try:
        search = SearchTool()

        # Test grep in current directory
        results = search.grep("def ", path=".", file_pattern="*.py", max_results=5)

        if results:
            print(f"   ✅ Code search works ({len(results)} matches)")
        else:
            print("   ⚠️ No matches found (expected in some cases)")

        return True

    except Exception as e:
        print(f"   ❌ Search tool error: {e}")
        return False


def test_function_calling_tools():
    """Test Function Calling integration"""
    print("🛠️ Testing Function Calling Tools...")

    # Count tools
    print(f"   ℹ️  {len(MOLOCH_TOOLS)} tools defined:")
    for i, tool in enumerate(MOLOCH_TOOLS, 1):
        print(f"      {i}. {tool['name']}")

    # Test tool execution (get_current_stats - safe to test)
    try:
        # Create mock instances
        brain = Brain()
        memory = Memory()
        learning = PersistentLearning()
        sm = None  # Not needed for stats

        result = execute_tool(
            "get_current_stats",
            {"stat_type": "all"},
            brain, memory, learning, sm
        )

        if result.get("success"):
            print("   ✅ Tool execution works")
            stats = result.get("stats", {})
            print(f"      Brain: {len(stats.get('brain', {}))} categories")
            print(f"      Memory: {stats.get('memory', {}).get('total_entries', 0)} entries")
        else:
            print("   ❌ Tool execution failed")
            return False

        return True

    except Exception as e:
        print(f"   ❌ Function calling error: {e}")
        return False


def generate_mfr_report(results):
    """Generate MFR-V1 format report for Claude Code"""
    from datetime import datetime

    passed = sum(1 for v in results.values() if v)
    failed = len(results) - passed
    failed_systems = [name for name, result in results.items() if not result]

    # Build MFR-V1 formatted report
    report = []
    report.append("🤖MFR-V1🤖")

    if failed == 0:
        # All systems OK - just status report
        report.append(f"F:self_check_all_ok|P:1|S:All {len(results)} systems operational|R:Status report - no issues")
    else:
        # Some systems failed
        priority = min(10, 3 + failed * 2)  # Scale priority by failures
        failed_list = ", ".join(failed_systems)

        report.append(f"F:self_check_failures|P:{priority}|S:{failed}/{len(results)} systems failed: {failed_list}|R:Auto-diagnostic detected issues")

        # Add individual failures
        for system_name, result in results.items():
            if not result:
                safe_name = system_name.lower().replace(" ", "_").replace("/", "_")
                report.append(f"F:{safe_name}_broken|P:{priority}|S:{system_name} test failed|R:Needs investigation")

    report.append("END-MFR")

    return "\n".join(report)


def main():
    """Run all tests"""
    import sys

    # Check for --mfr flag (machine-readable output only)
    mfr_only = "--mfr" in sys.argv

    if not mfr_only:
        print_header("M.O.L.O.C.H. 3.0 - SELF-CHECK")
        print("Testing all systems & tools...\n")

    results = {}

    # Run tests
    results["API Key"] = test_api_key()
    results["Directories"] = test_directories()
    results["Brain"] = test_brain()
    results["Memory"] = test_memory()
    results["Learning"] = test_learning()
    results["Voice Settings"] = test_voice_settings()
    results["Location/GPS"] = test_location()
    results["Bash Tool"] = test_bash_tool()
    results["File Tool"] = test_file_tool()
    results["Web Tool"] = test_web_tool()
    results["Search Tool"] = test_search_tool()
    results["Function Calling"] = test_function_calling_tools()

    # Summary
    passed = sum(1 for v in results.values() if v)
    failed = len(results) - passed

    if not mfr_only:
        print_header("SUMMARY")

        for test_name, result in results.items():
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"{status:10} {test_name}")

        print(f"\n{'='*60}")
        print(f"  TOTAL: {passed}/{len(results)} tests passed")

        if failed == 0:
            print(f"  🎉 ALL SYSTEMS OPERATIONAL!")
        else:
            print(f"  ⚠️  {failed} systems need attention")

        print(f"{'='*60}\n")

    # Always generate MFR report
    if mfr_only:
        # Only output MFR format
        print(generate_mfr_report(results))
    else:
        # Show both
        print_header("MFR-V1 REPORT (Copy & Send to Claude Code)")
        print(generate_mfr_report(results))
        print()

    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
