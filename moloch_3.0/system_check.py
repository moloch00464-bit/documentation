#!/usr/bin/env python3
"""
M.O.L.O.C.H. 3.0 - COMPLETE SYSTEM CHECK
========================================
Tests ALL systems together!
"""

import sys
from datetime import datetime, timedelta
from pathlib import Path

# Add moloch_3.0 to path
sys.path.insert(0, str(Path(__file__).parent))

from core.memory import Memory
from core.brain import Brain
from core.personality import Personality
from core.config import MOLOCH_DNA, MUSIK_BRAIN


def test_header(title):
    """Print test header"""
    print(f"\n{'='*70}")
    print(f"  {title}")
    print(f"{'='*70}")


def test_result(name, passed, details=""):
    """Print test result"""
    status = "✅ PASS" if passed else "❌ FAIL"
    print(f"{status} - {name}")
    if details:
        print(f"       {details}")
    return passed


def main():
    print("\n" + "="*70)
    print("  🤖 M.O.L.O.C.H. 3.0 - COMPLETE SYSTEM CHECK 🤖")
    print("="*70)
    print(f"  Datum: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}")
    print("="*70)

    total_tests = 0
    passed_tests = 0

    # =========================================================================
    # TEST 1: MEMORY SYSTEM
    # =========================================================================
    test_header("TEST 1: MEMORY SYSTEM")

    memory = Memory()

    # Test 1.1: Add to history
    total_tests += 1
    try:
        memory.add_to_history("user", "Test message", metadata={"mode": "text", "stimmung": "neutral"})
        passed = test_result("Memory.add_to_history()", len(memory.history) == 1, f"{len(memory.history)} entries")
        if passed: passed_tests += 1
    except Exception as e:
        test_result("Memory.add_to_history()", False, f"Error: {e}")

    # Test 1.2: Get context
    total_tests += 1
    try:
        context = memory.get_context(last_n=5)
        passed = test_result("Memory.get_context()", isinstance(context, list), f"{len(context)} messages")
        if passed: passed_tests += 1
    except Exception as e:
        test_result("Memory.get_context()", False, f"Error: {e}")

    # Test 1.3: Langzeit memory
    total_tests += 1
    try:
        memory.add_to_langzeit("fakten", "M.O.L.O.C.H. 3.0 System-Check 05.01.2026")
        passed = test_result("Memory.add_to_langzeit()", "fakten" in memory.langzeit, f"{len(memory.langzeit.get('fakten', []))} fakten")
        if passed: passed_tests += 1
    except Exception as e:
        test_result("Memory.add_to_langzeit()", False, f"Error: {e}")

    # =========================================================================
    # TEST 2: ZEIT-STATS (NEW!)
    # =========================================================================
    test_header("TEST 2: ZEIT-STATS SYSTEM 🕐")

    # Clear memory and add test data with timestamps
    memory.history = []
    now = datetime.now()

    # Test 2.1: Add messages with timestamps
    total_tests += 1
    try:
        memory.add_to_history("user", "Test 1", metadata={"timestamp": (now - timedelta(minutes=30)).isoformat()})
        memory.add_to_history("assistant", "Antwort 1", metadata={"timestamp": (now - timedelta(minutes=29)).isoformat()})
        memory.add_to_history("user", "Test 2", metadata={"timestamp": (now - timedelta(minutes=10)).isoformat()})
        memory.add_to_history("assistant", "Antwort 2", metadata={"timestamp": (now - timedelta(minutes=9)).isoformat()})
        passed = test_result("Zeit-Stats: Add timestamped messages", len(memory.history) == 4, "4 messages with timestamps")
        if passed: passed_tests += 1
    except Exception as e:
        test_result("Zeit-Stats: Add timestamped messages", False, f"Error: {e}")

    # Test 2.2: Get zeit stats
    total_tests += 1
    try:
        stats = memory.get_zeit_stats()
        has_all = all(key in stats for key in ["last_conversation_ago", "session_duration", "messages_today", "formatted_text"])
        details = f"Last: {stats.get('last_conversation_ago')}min, Session: {stats.get('session_duration')}min"
        passed = test_result("Memory.get_zeit_stats()", has_all, details)
        if passed: passed_tests += 1
    except Exception as e:
        test_result("Memory.get_zeit_stats()", False, f"Error: {e}")

    # Test 2.3: Formatted text generation
    total_tests += 1
    try:
        formatted = stats.get("formatted_text", "")
        has_text = len(formatted) > 0
        passed = test_result("Zeit-Stats: Formatted text", has_text, f"{len(formatted)} chars")
        if has_text:
            print(f"       Preview: {formatted.split(chr(10))[0][:50]}...")
        if passed: passed_tests += 1
    except Exception as e:
        test_result("Zeit-Stats: Formatted text", False, f"Error: {e}")

    # =========================================================================
    # TEST 3: PERSONALITY SYSTEM
    # =========================================================================
    test_header("TEST 3: PERSONALITY SYSTEM")

    personality = Personality()

    # Test 3.1: Stimmungs-Erkennung
    total_tests += 1
    try:
        test_cases = [
            ("Das geht nicht! Scheiße!", "gestresst"),
            ("Alles cool, läuft! 🎉", "gut_drauf"),
            ("Wie funktioniert das?", "fragend"),
            ("Okay", "neutral")
        ]
        all_correct = True
        for text, expected in test_cases:
            result = personality.detect_stimmung(text)
            if result != expected:
                all_correct = False
                break
        passed = test_result("Personality.detect_stimmung()", all_correct, f"{len(test_cases)} test cases")
        if passed: passed_tests += 1
    except Exception as e:
        test_result("Personality.detect_stimmung()", False, f"Error: {e}")

    # Test 3.2: Theme-Detection
    total_tests += 1
    try:
        test_cases = [
            ("Python Bug fixen", "coding"),
            ("WGT war geil!", "konzert"),
            ("Rebecca angerufen", "freunde"),
            ("Schicht war stressig", "arbeit")
        ]
        all_correct = True
        for text, expected in test_cases:
            result = personality.detect_theme(text)
            if result != expected:
                all_correct = False
                break
        passed = test_result("Personality.detect_theme()", all_correct, f"{len(test_cases)} test cases")
        if passed: passed_tests += 1
    except Exception as e:
        test_result("Personality.detect_theme()", False, f"Error: {e}")

    # Test 3.3: Context-Detection
    total_tests += 1
    try:
        context = personality.detect_context("Zuhause am Code basteln")
        has_all = all(key in context for key in ["location", "activity", "theme"])
        details = f"Location: {context.get('location')}, Activity: {context.get('activity')}"
        passed = test_result("Personality.detect_context()", has_all, details)
        if passed: passed_tests += 1
    except Exception as e:
        test_result("Personality.detect_context()", False, f"Error: {e}")

    # Test 3.4: Zeit-Wissen (NEW!)
    total_tests += 1
    try:
        zeit_context = personality.get_zeit_context()
        has_date = "2026" in zeit_context or datetime.now().year in zeit_context
        has_time = "Uhr" in zeit_context
        has_day = any(day in zeit_context for day in ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"])
        all_present = has_date and has_time and has_day
        passed = test_result("Personality.get_zeit_context()", all_present, "Date + Time + Weekday")
        if all_present:
            print(f"       Preview: {zeit_context.split(chr(10))[1][:50]}...")
        if passed: passed_tests += 1
    except Exception as e:
        test_result("Personality.get_zeit_context()", False, f"Error: {e}")

    # Test 3.5: Tageszeit-Mode
    total_tests += 1
    try:
        tageszeit = personality.get_tageszeit_mode()
        valid_modes = ["Kaffee-Modus", "Normal produktiv", "Feierabend-Modus", "Dark Side Mode"]
        is_valid = any(mode in tageszeit for mode in valid_modes)
        passed = test_result("Personality.get_tageszeit_mode()", is_valid, f"Current mode detected")
        if passed: passed_tests += 1
    except Exception as e:
        test_result("Personality.get_tageszeit_mode()", False, f"Error: {e}")

    # =========================================================================
    # TEST 4: SYSTEM PROMPT GENERATION (with Zeit-Stats!)
    # =========================================================================
    test_header("TEST 4: SYSTEM PROMPT GENERATION 🕐")

    # Test 4.1: Basic system prompt
    total_tests += 1
    try:
        system = personality.get_system_prompt(
            stimmung="neutral",
            tageszeit=personality.get_tageszeit_mode(),
            mode="text"
        )
        has_dna = "M.O.L.O.C.H." in system
        has_zeit = "Heute ist" in system or "Uhrzeit" in system
        passed = test_result("System Prompt: Basic", has_dna and has_zeit, f"{len(system)} chars, has Zeit-Wissen")
        if passed: passed_tests += 1
    except Exception as e:
        test_result("System Prompt: Basic", False, f"Error: {e}")

    # Test 4.2: System prompt with Zeit-Stats
    total_tests += 1
    try:
        stats = memory.get_zeit_stats()
        zeit_stats_text = stats.get("formatted_text", "")

        system = personality.get_system_prompt(
            stimmung="neutral",
            tageszeit=personality.get_tageszeit_mode(),
            mode="text",
            zeit_stats=zeit_stats_text
        )
        has_stats = len(zeit_stats_text) > 0 and ("Session" in system or "Gespräch" in system)
        passed = test_result("System Prompt: With Zeit-Stats", has_stats, "Zeit-Stats included")
        if passed: passed_tests += 1
    except Exception as e:
        test_result("System Prompt: With Zeit-Stats", False, f"Error: {e}")

    # Test 4.3: System prompt with all contexts
    total_tests += 1
    try:
        system = personality.get_system_prompt(
            stimmung="gestresst",
            tageszeit=personality.get_tageszeit_mode(),
            mode="voice",
            brain_context="Test Brain Context",
            memory_context="Test Memory Context",
            zeit_stats=zeit_stats_text
        )
        has_all = all(x in system for x in ["M.O.L.O.C.H.", "gestresst", "Test Brain Context", "Test Memory Context"])
        passed = test_result("System Prompt: Full context", has_all, f"{len(system)} chars with all contexts")
        if passed: passed_tests += 1
    except Exception as e:
        test_result("System Prompt: Full context", False, f"Error: {e}")

    # =========================================================================
    # TEST 5: BRAIN SYSTEM
    # =========================================================================
    test_header("TEST 5: BRAIN SYSTEM")

    brain = Brain()

    # Test 5.1: Brain save
    total_tests += 1
    try:
        test_data = {
            "test": "System Check",
            "timestamp": datetime.now().isoformat()
        }
        brain.save("test", test_data, "system_check.json")
        passed = test_result("Brain.save()", True, "test/system_check.json")
        if passed: passed_tests += 1
    except Exception as e:
        test_result("Brain.save()", False, f"Error: {e}")

    # Test 5.2: Brain read
    total_tests += 1
    try:
        data = brain.read("test", "system_check.json")
        is_valid = data is not None and "test" in data
        passed = test_result("Brain.read()", is_valid, f"Read back: {data.get('test', 'N/A') if data else 'None'}")
        if passed: passed_tests += 1
    except Exception as e:
        test_result("Brain.read()", False, f"Error: {e}")

    # Test 5.3: Brain stats
    total_tests += 1
    try:
        stats = brain.stats()
        has_stats = "total_entries" in stats and "categories" in stats
        passed = test_result("Brain.stats()", has_stats, f"{stats.get('total_entries', 0)} total entries")
        if passed: passed_tests += 1
    except Exception as e:
        test_result("Brain.stats()", False, f"Error: {e}")

    # =========================================================================
    # TEST 6: INTEGRATION TEST (All systems together!)
    # =========================================================================
    test_header("TEST 6: INTEGRATION TEST - ALL SYSTEMS TOGETHER 🚀")

    # Test 6.1: Full Voice Mode Simulation
    total_tests += 1
    try:
        # Simulate user input
        user_input = "Scheiße, das geht nicht! Hilfe!"

        # Detect stimmung
        stimmung = personality.detect_stimmung(user_input)

        # Detect theme
        theme = personality.detect_theme(user_input)

        # Detect context
        context = personality.detect_context(user_input)

        # Get zeit stats
        zeit_stats_data = memory.get_zeit_stats()
        zeit_stats_text = zeit_stats_data.get("formatted_text", "")

        # Build system prompt
        system_prompt = personality.get_system_prompt(
            stimmung=stimmung,
            tageszeit=personality.get_tageszeit_mode(),
            mode="voice",
            zeit_stats=zeit_stats_text
        )

        # Add to memory
        memory.add_to_history("user", user_input, metadata={
            "mode": "voice",
            "stimmung": stimmung,
            "theme": theme,
            "context": context
        })

        # Check all worked
        all_worked = (
            stimmung == "gestresst" and
            len(system_prompt) > 0 and
            "gestresst" in system_prompt and
            len(memory.history) > 0
        )

        details = f"Stimmung: {stimmung}, Theme: {theme}, Context: {context['location']}"
        passed = test_result("Voice Mode: Full simulation", all_worked, details)
        if passed: passed_tests += 1
    except Exception as e:
        test_result("Voice Mode: Full simulation", False, f"Error: {e}")

    # Test 6.2: Memory persistence (save/load)
    total_tests += 1
    try:
        memory.save_to_disk()

        # Create new memory instance and check it loads
        new_memory = Memory()
        has_history = len(new_memory.history) > 0

        passed = test_result("Memory: Persistence", has_history, f"{len(new_memory.history)} entries loaded")
        if passed: passed_tests += 1
    except Exception as e:
        test_result("Memory: Persistence", False, f"Error: {e}")

    # =========================================================================
    # FINAL RESULTS
    # =========================================================================
    test_header("FINAL RESULTS")

    percentage = (passed_tests / total_tests * 100) if total_tests > 0 else 0

    print(f"\n  Tests Passed: {passed_tests}/{total_tests} ({percentage:.1f}%)")

    if percentage == 100:
        print(f"\n  🎉 ALL TESTS PASSED! M.O.L.O.C.H. 3.0 IS READY! 🎉")
        status = "✅ READY FOR PRODUCTION"
    elif percentage >= 90:
        print(f"\n  ⚠️  MOSTLY WORKING - Minor issues")
        status = "⚠️ MOSTLY READY"
    elif percentage >= 70:
        print(f"\n  ⚠️  SOME ISSUES - Need fixes")
        status = "⚠️ NEEDS FIXES"
    else:
        print(f"\n  ❌ CRITICAL ISSUES - Major problems!")
        status = "❌ NOT READY"

    print(f"\n  Status: {status}")
    print("\n" + "="*70 + "\n")

    return 0 if percentage == 100 else 1


if __name__ == "__main__":
    sys.exit(main())
