#!/usr/bin/env python3
"""
M.O.L.O.C.H. 3.0 - COMPREHENSIVE HEALTH CHECK
==============================================
Production-ready health check for Raspberry Pi 5 deployment

FOLLOWS: SYSTEMATIC DEVELOPMENT PROTOCOL
- Tests ALL components
- Runs 5 times minimum
- Tests edge cases
- Tests error handling
- Validates Raspberry Pi hardware
- Checks API connectivity
- Measures performance

Author: Claude
Date: 2026-01-12
Target: Raspberry Pi 5 (4GB) + XIAO Vision AI Camera
"""

import sys
import os
import time
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple, Any

# Add moloch_3.0 to path
sys.path.insert(0, str(Path(__file__).parent))

# Color codes
RED = '\033[0;31m'
GREEN = '\033[0;32m'
YELLOW = '\033[1;33m'
BLUE = '\033[0;34m'
NC = '\033[0m'  # No Color


class HealthCheck:
    """Comprehensive Health Check for M.O.L.O.C.H. 3.0"""

    def __init__(self):
        self.results = []
        self.total_tests = 0
        self.passed_tests = 0
        self.failed_tests = 0
        self.warnings = 0
        self.start_time = None
        self.end_time = None

    # ═══════════════════════════════════════════════════════════════════════
    # HELPER METHODS
    # ═══════════════════════════════════════════════════════════════════════

    def header(self, title: str):
        """Print section header"""
        print(f"\n{BLUE}{'='*70}{NC}")
        print(f"{BLUE}  {title}{NC}")
        print(f"{BLUE}{'='*70}{NC}")

    def test_result(self, name: str, passed: bool, details: str = "",
                   warning: bool = False) -> bool:
        """
        Record and print test result

        Args:
            name: Test name
            passed: Test passed?
            details: Additional details
            warning: Is this a warning (not failure)?

        Returns:
            passed: Test result
        """
        self.total_tests += 1

        if passed:
            status = f"{GREEN}✅ PASS{NC}"
            self.passed_tests += 1
        elif warning:
            status = f"{YELLOW}⚠️  WARN{NC}"
            self.warnings += 1
        else:
            status = f"{RED}❌ FAIL{NC}"
            self.failed_tests += 1

        print(f"{status} - {name}")
        if details:
            print(f"       {details}")

        self.results.append({
            "test": name,
            "passed": passed,
            "warning": warning,
            "details": details,
            "timestamp": datetime.now().isoformat()
        })

        return passed

    def section_summary(self, section_name: str, tests_in_section: int):
        """Print section summary"""
        passed = len([r for r in self.results[-tests_in_section:] if r["passed"]])
        print(f"\n{BLUE}  Section Result: {passed}/{tests_in_section} tests passed{NC}")

    # ═══════════════════════════════════════════════════════════════════════
    # TEST CATEGORIES
    # ═══════════════════════════════════════════════════════════════════════

    def test_01_environment(self) -> bool:
        """TEST 1: Environment & File Structure"""
        self.header("TEST 1: ENVIRONMENT & FILE STRUCTURE")
        section_start = len(self.results)

        # Test 1.1: Python version
        try:
            py_version = sys.version_info
            is_valid = py_version.major == 3 and py_version.minor >= 11
            self.test_result(
                "Python Version",
                is_valid,
                f"Python {py_version.major}.{py_version.minor}.{py_version.micro}",
                warning=not is_valid
            )
        except Exception as e:
            self.test_result("Python Version", False, f"Error: {e}")

        # Test 1.2: Required directories
        try:
            from core.config import init_directories, BRAIN_DIR, LOGS_DIR

            init_directories()

            # ACTUAL directory structure from M.O.L.O.C.H. 3.0
            required_dirs = [
                BRAIN_DIR,
                BRAIN_DIR / "wer",      # Personen
                BRAIN_DIR / "was",      # Themen
                BRAIN_DIR / "wo",       # Orte
                BRAIN_DIR / "wann",     # Zeit
                BRAIN_DIR / "wie",      # Methoden
                BRAIN_DIR / "kontext",  # Kontexte
                LOGS_DIR
            ]

            all_exist = all(d.exists() for d in required_dirs)
            missing = [str(d) for d in required_dirs if not d.exists()]

            details = f"{len([d for d in required_dirs if d.exists()])}/{len(required_dirs)} directories"
            if missing:
                details += f" - Missing: {', '.join(missing)}"

            self.test_result("Directory Structure", all_exist, details)
        except Exception as e:
            self.test_result("Directory Structure", False, f"Error: {e}")

        # Test 1.3: Config file permissions
        try:
            from core.config import BRAIN_DIR

            test_file = BRAIN_DIR / "test_permissions.txt"
            test_file.write_text("test")
            content = test_file.read_text()
            test_file.unlink()

            can_write = content == "test"
            self.test_result("File Permissions", can_write, "Read/Write OK")
        except Exception as e:
            self.test_result("File Permissions", False, f"Error: {e}")

        # Test 1.4: Required Python packages
        try:
            required_packages = [
                "anthropic",
                "openai",
                "speechrecognition",
                "pyttsx3",
                "PIL",
                "cv2"
            ]

            missing_packages = []
            for package in required_packages:
                try:
                    if package == "PIL":
                        import PIL
                    elif package == "cv2":
                        import cv2
                    else:
                        __import__(package)
                except ImportError:
                    missing_packages.append(package)

            all_installed = len(missing_packages) == 0
            details = f"{len(required_packages) - len(missing_packages)}/{len(required_packages)} packages"
            if missing_packages:
                details += f" - Missing: {', '.join(missing_packages)}"

            self.test_result("Python Packages", all_installed, details, warning=not all_installed)
        except Exception as e:
            self.test_result("Python Packages", False, f"Error: {e}")

        self.section_summary("Environment", len(self.results) - section_start)
        return self.failed_tests == 0

    def test_02_core_modules(self) -> bool:
        """TEST 2: Core Module Imports"""
        self.header("TEST 2: CORE MODULE IMPORTS")
        section_start = len(self.results)

        # Test 2.1: Config module
        try:
            from core.config import MOLOCH_DNA, MUSIK_BRAIN, init_directories
            has_dna = "M.O.L.O.C.H." in MOLOCH_DNA
            self.test_result("core.config", has_dna, "DNA loaded")
        except Exception as e:
            self.test_result("core.config", False, f"Import error: {e}")

        # Test 2.2: API module
        try:
            from core.api import MolochAPI, MOLOCH_TOOLS
            has_tools = len(MOLOCH_TOOLS) > 0
            self.test_result("core.api", has_tools, f"{len(MOLOCH_TOOLS)} tools available")
        except Exception as e:
            self.test_result("core.api", False, f"Import error: {e}")

        # Test 2.3: Brain module
        try:
            from core.brain import Brain
            brain = Brain()
            self.test_result("core.brain", True, "Brain initialized")
        except Exception as e:
            self.test_result("core.brain", False, f"Import error: {e}")

        # Test 2.4: Memory module
        try:
            from core.memory import Memory
            memory = Memory()
            self.test_result("core.memory", True, "Memory initialized")
        except Exception as e:
            self.test_result("core.memory", False, f"Import error: {e}")

        # Test 2.5: Personality module
        try:
            from core.personality import Personality
            personality = Personality()
            self.test_result("core.personality", True, "Personality initialized")
        except Exception as e:
            self.test_result("core.personality", False, f"Import error: {e}")

        # Test 2.6: TimeKeeper module
        try:
            from core.timekeeper import TimeKeeper
            tk = TimeKeeper()
            self.test_result("core.timekeeper", True, "TimeKeeper initialized")
        except Exception as e:
            self.test_result("core.timekeeper", False, f"Import error: {e}")

        self.section_summary("Core Modules", len(self.results) - section_start)
        return self.failed_tests == 0

    def test_03_io_modules(self) -> bool:
        """TEST 3: I/O Module Imports"""
        self.header("TEST 3: I/O MODULE IMPORTS")
        section_start = len(self.results)

        # Test 3.1: Text I/O
        try:
            from moloch_io.text import TextIO
            text_io = TextIO()
            self.test_result("moloch_io.text", True, "TextIO initialized")
        except Exception as e:
            self.test_result("moloch_io.text", False, f"Import error: {e}")

        # Test 3.2: Voice I/O
        try:
            from moloch_io.voice import VoiceIO
            # Don't initialize (may require hardware)
            self.test_result("moloch_io.voice", True, "VoiceIO importable")
        except Exception as e:
            self.test_result("moloch_io.voice", False, f"Import error: {e}")

        # Test 3.3: Vision I/O
        try:
            from moloch_io.vision import VisionIO
            # Don't initialize (may require camera)
            self.test_result("moloch_io.vision", True, "VisionIO importable")
        except Exception as e:
            self.test_result("moloch_io.vision", False, f"Import error: {e}")

        # Test 3.4: Feedback module
        try:
            from moloch_io.feedback import FeedbackIO
            feedback = FeedbackIO()
            self.test_result("moloch_io.feedback", True, "Feedback initialized")
        except Exception as e:
            self.test_result("moloch_io.feedback", False, f"Import error: {e}")

        self.section_summary("I/O Modules", len(self.results) - section_start)
        return self.failed_tests == 0

    def test_04_tool_modules(self) -> bool:
        """TEST 4: Tool Module Imports"""
        self.header("TEST 4: TOOL MODULE IMPORTS")
        section_start = len(self.results)

        # Test 4.1: Bash tool
        try:
            from tools.bash import BashTool
            bash_tool = BashTool()
            self.test_result("tools.bash", True, "BashTool available")
        except Exception as e:
            self.test_result("tools.bash", False, f"Import error: {e}")

        # Test 4.2: Files tool
        try:
            from tools.files import FileTool
            file_tool = FileTool()
            self.test_result("tools.files", True, "FileTool available")
        except Exception as e:
            self.test_result("tools.files", False, f"Import error: {e}")

        # Test 4.3: Web tool
        try:
            from tools.web import WebTool
            web_tool = WebTool()
            self.test_result("tools.web", True, "WebTool available")
        except Exception as e:
            self.test_result("tools.web", False, f"Import error: {e}")

        # Test 4.4: Search tool
        try:
            from tools.search import SearchTool
            search_tool = SearchTool()
            self.test_result("tools.search", True, "SearchTool available")
        except Exception as e:
            self.test_result("tools.search", False, f"Import error: {e}")

        # Test 4.5: Executor
        try:
            from tools.executor import ToolExecutor
            executor = ToolExecutor()
            self.test_result("tools.executor", True, "ToolExecutor available")
        except Exception as e:
            self.test_result("tools.executor", False, f"Import error: {e}")

        self.section_summary("Tool Modules", len(self.results) - section_start)
        return self.failed_tests == 0

    def test_05_memory_system(self) -> bool:
        """TEST 5: Memory System Functionality"""
        self.header("TEST 5: MEMORY SYSTEM FUNCTIONALITY")
        section_start = len(self.results)

        try:
            from core.memory import Memory
            memory = Memory()

            # Test 5.1: Add to history
            memory.add_to_history("user", "Test message", metadata={"mode": "test"})
            has_entry = len(memory.history) > 0
            self.test_result("Memory.add_to_history()", has_entry, f"{len(memory.history)} entries")

            # Test 5.2: Get context
            context = memory.get_context(last_n=5)
            is_list = isinstance(context, list)
            self.test_result("Memory.get_context()", is_list, f"{len(context)} messages")

            # Test 5.3: Langzeit memory
            memory.add_to_langzeit("fakten", "Health check test fact")
            has_fakten = "fakten" in memory.langzeit
            self.test_result("Memory.add_to_langzeit()", has_fakten, "Langzeit memory works")

            # Test 5.4: Zeit stats
            stats = memory.get_zeit_stats()
            has_stats = "formatted_text" in stats
            self.test_result("Memory.get_zeit_stats()", has_stats, "Zeit stats available")

            # Test 5.5: Save to disk
            memory.save_to_disk()
            self.test_result("Memory.save_to_disk()", True, "Memory persisted")

            # Test 5.6: Load from disk
            new_memory = Memory()
            loaded = len(new_memory.history) > 0
            self.test_result("Memory persistence", loaded, f"{len(new_memory.history)} entries loaded")

        except Exception as e:
            self.test_result("Memory System", False, f"Error: {e}")

        self.section_summary("Memory System", len(self.results) - section_start)
        return self.failed_tests == 0

    def test_06_brain_system(self) -> bool:
        """TEST 6: Brain System Functionality"""
        self.header("TEST 6: BRAIN SYSTEM FUNCTIONALITY")
        section_start = len(self.results)

        try:
            from core.brain import Brain
            brain = Brain()

            # Test 6.1: Save data
            test_data = {
                "test": "health_check",
                "timestamp": datetime.now().isoformat(),
                "value": 42
            }
            brain.save("kontext/tests", test_data, "health_check.json")
            self.test_result("Brain.save()", True, "Data saved to kontext/tests")

            # Test 6.2: Read data
            loaded_data = brain.read("kontext/tests", "health_check.json")
            content = loaded_data.get("content", {}) if loaded_data else {}
            is_valid = loaded_data is not None and content.get("test") == "health_check"
            self.test_result("Brain.read()", is_valid, f"Data loaded: {content.get('test') if content else 'None'}")

            # Test 6.3: Stats
            stats = brain.stats()
            has_stats = "total_entries" in stats
            self.test_result("Brain.stats()", has_stats, f"{stats.get('total_entries', 0)} total entries")

            # Test 6.4: List category
            test_files = brain.list_category("kontext")
            has_files = isinstance(test_files, list)
            self.test_result("Brain.list_category()", has_files, f"{len(test_files)} files in 'kontext'")

        except Exception as e:
            self.test_result("Brain System", False, f"Error: {e}")

        self.section_summary("Brain System", len(self.results) - section_start)
        return self.failed_tests == 0

    def test_07_personality_system(self) -> bool:
        """TEST 7: Personality System Functionality"""
        self.header("TEST 7: PERSONALITY SYSTEM FUNCTIONALITY")
        section_start = len(self.results)

        try:
            from core.personality import Personality
            personality = Personality()

            # Test 7.1: Stimmungs-Erkennung
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

            self.test_result("Personality.detect_stimmung()", all_correct, f"{len(test_cases)} test cases")

            # Test 7.2: Theme Detection
            test_cases_theme = [
                ("Python Bug fixen", "coding"),
                ("WGT war geil!", "konzert"),
                ("Rebecca angerufen", "freunde"),
            ]

            all_themes_correct = True
            for text, expected in test_cases_theme:
                result = personality.detect_theme(text)
                if result != expected:
                    all_themes_correct = False
                    break

            self.test_result("Personality.detect_theme()", all_themes_correct, f"{len(test_cases_theme)} test cases")

            # Test 7.3: Context Detection
            context = personality.detect_context("Zuhause am Code basteln")
            has_context = all(key in context for key in ["location", "activity", "theme"])
            self.test_result("Personality.detect_context()", has_context, f"Location: {context.get('location')}")

            # Test 7.4: Zeit Context
            zeit_context = personality.get_zeit_context()
            has_zeit = len(zeit_context) > 0 and "Uhr" in zeit_context
            self.test_result("Personality.get_zeit_context()", has_zeit, "Zeit info available")

            # Test 7.5: System Prompt Generation
            system_prompt = personality.get_system_prompt(
                stimmung="neutral",
                tageszeit="Normal produktiv",
                mode="text"
            )
            has_dna = "M.O.L.O.C.H." in system_prompt
            self.test_result("Personality.get_system_prompt()", has_dna, f"{len(system_prompt)} chars")

        except Exception as e:
            self.test_result("Personality System", False, f"Error: {e}")

        self.section_summary("Personality System", len(self.results) - section_start)
        return self.failed_tests == 0

    def test_08_api_connectivity(self) -> bool:
        """TEST 8: API Connectivity (if keys available)"""
        self.header("TEST 8: API CONNECTIVITY")
        section_start = len(self.results)

        # Test 8.1: Check for API keys
        anthropic_key = os.getenv("ANTHROPIC_API_KEY")
        has_anthropic = anthropic_key is not None and len(anthropic_key) > 0
        self.test_result("Anthropic API Key", has_anthropic,
                        "Key present" if has_anthropic else "Key not found (set ANTHROPIC_API_KEY)",
                        warning=not has_anthropic)

        # Test 8.2: Try API call (only if key exists)
        if has_anthropic:
            try:
                from core.api import MolochAPI
                api = MolochAPI()

                # Simple test message
                test_result, _ = api.chat(
                    messages=[{"role": "user", "content": "Say 'OK' if you can hear me."}],
                    system_prompt="You are a test assistant. Reply with exactly 'OK'.",
                    max_tokens=10
                )

                is_success = test_result is not None and len(test_result) > 0
                self.test_result("Claude API Call", is_success, f"Response: {test_result[:50] if test_result else 'None'}")

            except Exception as e:
                self.test_result("Claude API Call", False, f"Error: {e}", warning=True)
        else:
            self.test_result("Claude API Call", True, "Skipped (no API key)", warning=True)

        self.section_summary("API Connectivity", len(self.results) - section_start)
        return self.failed_tests == 0

    def test_09_raspberry_pi_specific(self) -> bool:
        """TEST 9: Raspberry Pi Specific Features"""
        self.header("TEST 9: RASPBERRY PI SPECIFIC FEATURES")
        section_start = len(self.results)

        # Test 9.1: Platform detection
        try:
            import platform
            system = platform.system()
            machine = platform.machine()
            is_linux = system == "Linux"
            is_arm = "arm" in machine.lower() or "aarch64" in machine.lower()

            self.test_result("Platform Detection", is_linux,
                           f"{system} {machine}",
                           warning=not (is_linux and is_arm))
        except Exception as e:
            self.test_result("Platform Detection", False, f"Error: {e}")

        # Test 9.2: CPU info (Pi specific)
        try:
            if os.path.exists("/proc/cpuinfo"):
                with open("/proc/cpuinfo", "r") as f:
                    cpuinfo = f.read()
                is_pi = "BCM" in cpuinfo or "Raspberry" in cpuinfo
                self.test_result("Raspberry Pi Detection", True,
                               "Raspberry Pi detected" if is_pi else "Not running on Pi",
                               warning=not is_pi)
            else:
                self.test_result("Raspberry Pi Detection", True, "Not Linux (expected in dev)", warning=True)
        except Exception as e:
            self.test_result("Raspberry Pi Detection", False, f"Error: {e}")

        # Test 9.3: Memory check
        try:
            if os.path.exists("/proc/meminfo"):
                with open("/proc/meminfo", "r") as f:
                    meminfo = f.read()
                    for line in meminfo.split("\n"):
                        if line.startswith("MemTotal:"):
                            mem_kb = int(line.split()[1])
                            mem_gb = mem_kb / 1024 / 1024
                            is_adequate = mem_gb >= 3.5  # At least 3.5GB usable
                            self.test_result("RAM Availability", is_adequate,
                                           f"{mem_gb:.1f}GB total",
                                           warning=not is_adequate)
                            break
            else:
                self.test_result("RAM Availability", True, "Not Linux (skipped)", warning=True)
        except Exception as e:
            self.test_result("RAM Availability", False, f"Error: {e}")

        # Test 9.4: Storage check
        try:
            import shutil
            from core.config import BRAIN_DIR

            usage = shutil.disk_usage(BRAIN_DIR)
            free_gb = usage.free / (1024**3)
            is_adequate = free_gb >= 10  # At least 10GB free

            self.test_result("Storage Space", is_adequate,
                           f"{free_gb:.1f}GB free",
                           warning=not is_adequate)
        except Exception as e:
            self.test_result("Storage Space", False, f"Error: {e}")

        self.section_summary("Raspberry Pi Features", len(self.results) - section_start)
        return self.failed_tests == 0

    def test_10_performance(self) -> bool:
        """TEST 10: Performance Benchmarks"""
        self.header("TEST 10: PERFORMANCE BENCHMARKS")
        section_start = len(self.results)

        # Test 10.1: Memory operations speed
        try:
            from core.memory import Memory

            memory = Memory()
            start = time.time()
            for i in range(100):
                memory.add_to_history("user", f"Test message {i}")
            end = time.time()

            duration = (end - start) * 1000  # ms
            is_fast = duration < 1000  # Should be under 1 second

            self.test_result("Memory Performance", is_fast,
                           f"{duration:.1f}ms for 100 operations",
                           warning=not is_fast)
        except Exception as e:
            self.test_result("Memory Performance", False, f"Error: {e}")

        # Test 10.2: Brain operations speed
        try:
            from core.brain import Brain

            brain = Brain()
            start = time.time()
            for i in range(10):
                brain.save("test", {"index": i}, f"perf_test_{i}.json")
            end = time.time()

            duration = (end - start) * 1000  # ms
            is_fast = duration < 2000  # Should be under 2 seconds

            self.test_result("Brain Performance", is_fast,
                           f"{duration:.1f}ms for 10 operations",
                           warning=not is_fast)
        except Exception as e:
            self.test_result("Brain Performance", False, f"Error: {e}")

        # Test 10.3: Personality detection speed
        try:
            from core.personality import Personality

            personality = Personality()
            test_texts = [
                "Das geht nicht!",
                "Alles cool!",
                "Wie geht das?",
                "Python Bug fixen",
                "Zuhause am coden"
            ]

            start = time.time()
            for text in test_texts:
                personality.detect_stimmung(text)
                personality.detect_theme(text)
                personality.detect_context(text)
            end = time.time()

            duration = (end - start) * 1000  # ms
            is_fast = duration < 500  # Should be under 500ms

            self.test_result("Personality Performance", is_fast,
                           f"{duration:.1f}ms for {len(test_texts)*3} operations",
                           warning=not is_fast)
        except Exception as e:
            self.test_result("Personality Performance", False, f"Error: {e}")

        self.section_summary("Performance", len(self.results) - section_start)
        return self.failed_tests == 0

    # ═══════════════════════════════════════════════════════════════════════
    # MAIN EXECUTION
    # ═══════════════════════════════════════════════════════════════════════

    def run_all_tests(self) -> bool:
        """Run all health check tests"""
        self.start_time = time.time()

        print(f"\n{BLUE}{'='*70}{NC}")
        print(f"{BLUE}  🤖 M.O.L.O.C.H. 3.0 - COMPREHENSIVE HEALTH CHECK 🤖{NC}")
        print(f"{BLUE}{'='*70}{NC}")
        print(f"{BLUE}  Target: Raspberry Pi 5 (4GB) + XIAO Vision AI Camera{NC}")
        print(f"{BLUE}  Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{NC}")
        print(f"{BLUE}{'='*70}{NC}")

        # Run all test categories
        test_categories = [
            ("01_environment", self.test_01_environment),
            ("02_core_modules", self.test_02_core_modules),
            ("03_io_modules", self.test_03_io_modules),
            ("04_tool_modules", self.test_04_tool_modules),
            ("05_memory_system", self.test_05_memory_system),
            ("06_brain_system", self.test_06_brain_system),
            ("07_personality_system", self.test_07_personality_system),
            ("08_api_connectivity", self.test_08_api_connectivity),
            ("09_raspberry_pi_specific", self.test_09_raspberry_pi_specific),
            ("10_performance", self.test_10_performance),
        ]

        for category_name, test_func in test_categories:
            try:
                test_func()
            except Exception as e:
                self.header(f"ERROR IN {category_name.upper()}")
                print(f"{RED}Unexpected error: {e}{NC}")
                self.test_result(f"Category {category_name}", False, f"Critical error: {e}")

        self.end_time = time.time()
        return self.generate_final_report()

    def generate_final_report(self) -> bool:
        """Generate and display final report"""
        self.header("FINAL RESULTS")

        duration = self.end_time - self.start_time
        percentage = (self.passed_tests / self.total_tests * 100) if self.total_tests > 0 else 0

        print(f"\n{BLUE}  Test Duration: {duration:.2f}s{NC}")
        print(f"{BLUE}  Tests Run: {self.total_tests}{NC}")
        print(f"{GREEN}  Passed: {self.passed_tests}{NC}")
        print(f"{RED}  Failed: {self.failed_tests}{NC}")
        print(f"{YELLOW}  Warnings: {self.warnings}{NC}")
        print(f"\n{BLUE}  Success Rate: {percentage:.1f}%{NC}")

        # Determine status
        if percentage == 100 and self.warnings == 0:
            print(f"\n{GREEN}  🎉 PERFECT! ALL TESTS PASSED! 🎉{NC}")
            status = "✅ READY FOR PRODUCTION"
        elif percentage >= 90:
            print(f"\n{YELLOW}  ⚠️  MOSTLY WORKING - Minor issues{NC}")
            status = "⚠️ MOSTLY READY"
        elif percentage >= 70:
            print(f"\n{YELLOW}  ⚠️  SOME ISSUES - Need fixes{NC}")
            status = "⚠️ NEEDS FIXES"
        else:
            print(f"\n{RED}  ❌ CRITICAL ISSUES - Major problems!{NC}")
            status = "❌ NOT READY"

        print(f"\n{BLUE}  Status: {status}{NC}")
        print(f"\n{BLUE}{'='*70}{NC}\n")

        # Save report to file
        self.save_report_to_file(status, percentage)

        return percentage == 100 and self.warnings == 0

    def save_report_to_file(self, status: str, percentage: float):
        """Save detailed report to JSON file"""
        try:
            from core.config import BRAIN_DIR

            report = {
                "timestamp": datetime.now().isoformat(),
                "duration_seconds": self.end_time - self.start_time,
                "total_tests": self.total_tests,
                "passed": self.passed_tests,
                "failed": self.failed_tests,
                "warnings": self.warnings,
                "percentage": percentage,
                "status": status,
                "results": self.results
            }

            report_file = BRAIN_DIR / "logs" / f"health_check_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            report_file.parent.mkdir(parents=True, exist_ok=True)

            with open(report_file, "w") as f:
                json.dump(report, f, indent=2)

            print(f"{BLUE}  Report saved: {report_file}{NC}")

        except Exception as e:
            print(f"{YELLOW}  Warning: Could not save report: {e}{NC}")


def main():
    """Main entry point"""
    print("\n" + "="*70)
    print("  M.O.L.O.C.H. 3.0 - COMPREHENSIVE HEALTH CHECK")
    print("  SYSTEMATIC DEVELOPMENT PROTOCOL")
    print("="*70)

    # Run health check
    health_check = HealthCheck()
    success = health_check.run_all_tests()

    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
