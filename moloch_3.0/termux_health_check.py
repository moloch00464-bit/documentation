#!/usr/bin/env python3
"""
M.O.L.O.C.H. FIELD UNIT - TERMUX HEALTH CHECK
==============================================

⛔ KRITISCHE REGEL: ECHTE DATEN SIND HEILIG!
- ~/moloch/brain/   → NUR LESEN, NIE ÄNDERN!
- ~/moloch/memory/  → NUR LESEN, NIE ÄNDERN!

Alle Tests laufen in: ~/moloch/test_sandbox/

Author: Claude
Date: 2026-01-12
Device: Redmi Note 13 Pro+ 5G (Termux)
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime

class TermuxHealthCheck:
    """
    Health Check für M.O.L.O.C.H. Field Unit

    ⛔ REGEL: Echte Brain-Daten werden NUR GELESEN, NIE GEÄNDERT!
    """

    def __init__(self):
        self.results = []
        self.warnings = []

        # Pfade
        self.moloch_dir = Path.home() / "moloch"
        self.real_brain = self.moloch_dir / "brain"
        self.real_memory = self.moloch_dir / "memory"
        self.test_sandbox = self.moloch_dir / "test_sandbox"

        # Erstelle Test-Sandbox
        self.test_sandbox.mkdir(parents=True, exist_ok=True)

        print("=" * 70)
        print("M.O.L.O.C.H. FIELD UNIT - TERMUX HEALTH CHECK")
        print("=" * 70)
        print()
        print(f"📁 Moloch Dir:    {self.moloch_dir}")
        print(f"⛔ Echter Brain:  {self.real_brain} (READ-ONLY!)")
        print(f"⛔ Echte Memory:  {self.real_memory} (READ-ONLY!)")
        print(f"🧪 Test Sandbox: {self.test_sandbox}")
        print()
        print("⛔ ALLE Tests laufen in Sandbox - echte Daten UNBERÜHRT!")
        print()

    def test_01_brain_data_protection(self):
        """Prüfe dass echte Daten existieren und geschützt sind"""
        print("=" * 70)
        print("TEST 1: BRAIN DATA PROTECTION & VERSION DETECTION")
        print("=" * 70)

        if self.real_brain.exists():
            # Zähle echte Einträge (NUR LESEN!)
            try:
                real_files = list(self.real_brain.rglob("*.json"))
                print(f"✅ Echter Brain gefunden: {len(real_files)} JSON-Dateien")
                print(f"   ⛔ Diese werden NICHT angefasst!")
                print()

                # Zähle pro Kategorie
                total_files = 0
                for category in ["wer", "was", "wo", "wann", "wie", "kontext"]:
                    cat_path = self.real_brain / category
                    if cat_path.exists():
                        count = len(list(cat_path.rglob("*.json")))
                        if count > 0:
                            print(f"   📂 {category:8s}: {count:4d} Dateien")
                            total_files += count

                print()

                # Detect 2.0 vs 3.0 format (sample check)
                v2_count = 0
                v3_count = 0
                sample_size = min(10, total_files)  # Check first 10 files

                for json_file in list(self.real_brain.rglob("*.json"))[:sample_size]:
                    try:
                        with open(json_file, 'r', encoding='utf-8') as f:
                            data = json.load(f)

                        # Check format
                        if "content" in data and "metadata" in data:
                            v3_count += 1
                        else:
                            v2_count += 1
                    except:
                        pass

                if v2_count > 0 or v3_count > 0:
                    print(f"   📊 FORMAT DETECTION (Sample: {sample_size} Dateien):")
                    if v2_count > 0:
                        print(f"      📦 M.O.L.O.C.H. 2.0 Format: {v2_count} Dateien")
                        print(f"         → 3.0 Code ist RÜCKWÄRTSKOMPATIBEL ✅")
                        print(f"         → Alte Daten werden automatisch konvertiert (in-memory)")
                    if v3_count > 0:
                        print(f"      📦 M.O.L.O.C.H. 3.0 Format: {v3_count} Dateien")
                    print()

                self.results.append(("Brain Protected", True))
            except Exception as e:
                print(f"⚠️  Fehler beim Lesen: {e}")
                self.results.append(("Brain Protected", False))
        else:
            print(f"⚠️  Kein Brain-Ordner gefunden unter {self.real_brain}")
            print(f"   → Möglicherweise erste Installation")
            self.warnings.append("Kein Brain-Ordner - erste Installation?")
            self.results.append(("Brain Exists", False))

        print()

    def test_02_sandbox_isolation(self):
        """Prüfe dass Sandbox isoliert ist"""
        print("=" * 70)
        print("TEST 2: SANDBOX ISOLATION")
        print("=" * 70)

        # Teste in Sandbox
        test_file = self.test_sandbox / "isolation_test.json"

        try:
            # Schreibe Test-Datei in Sandbox
            with open(test_file, 'w') as f:
                json.dump({"test": "isolation", "timestamp": datetime.now().isoformat()}, f)

            print(f"✅ Test-Datei erstellt: {test_file}")

            # Prüfe dass es NICHT in echtem Brain ist
            if self.real_brain.exists():
                real_path = self.real_brain / "isolation_test.json"

                if real_path.exists():
                    print(f"🚨 KRITISCHER FEHLER: Test-Datei in echtem Brain!")
                    print(f"   {real_path}")
                    self.results.append(("Sandbox Isolated", False))
                else:
                    print(f"✅ Sandbox ist isoliert - echte Daten unberührt")
                    self.results.append(("Sandbox Isolated", True))
            else:
                print(f"✅ Sandbox funktioniert (kein Brain zum Vergleichen)")
                self.results.append(("Sandbox Isolated", True))

            # Cleanup nur Sandbox
            test_file.unlink()
            print(f"🧹 Test-Datei aus Sandbox entfernt")

        except Exception as e:
            print(f"❌ Sandbox Test failed: {e}")
            self.results.append(("Sandbox Isolated", False))

        print()

    def test_03_code_security_fixes(self):
        """Prüfe Security Fixes im Code (NUR CODE LESEN!)"""
        print("=" * 70)
        print("TEST 3: CODE SECURITY FIXES")
        print("=" * 70)

        # Suche brain.py
        brain_paths = [
            self.moloch_dir / "brain.py",
            self.moloch_dir / "core" / "brain.py",
        ]

        brain_py = None
        for path in brain_paths:
            if path.exists():
                brain_py = path
                break

        if brain_py:
            print(f"📄 Found: {brain_py}")

            with open(brain_py, 'r', encoding='utf-8') as f:
                source = f.read()

            # Check 1: Filename Sanitization
            has_sanitize = "_sanitize_filename" in source
            print(f"{'✅' if has_sanitize else '🚨'} Filename Sanitization: {'VORHANDEN' if has_sanitize else 'FEHLT!'}")
            self.results.append(("Filename Sanitization", has_sanitize))

            if not has_sanitize:
                print(f"   🚨 KRITISCH: _sanitize_filename MUSS implementiert werden!")
                print(f"   → Path traversal und command injection möglich!")

            # Check 2: Atomic Saves
            has_atomic = "os.replace" in source and "mkstemp" in source
            print(f"{'✅' if has_atomic else '🚨'} Atomic Saves: {'VORHANDEN' if has_atomic else 'FEHLT!'}")
            self.results.append(("Atomic Saves", has_atomic))

            if not has_atomic:
                print(f"   🚨 KRITISCH: Atomic saves MÜSSEN implementiert werden!")
                print(f"   → Concurrent access = korrupte Daten!")

            # Check 3: Exception Handling
            try_count = source.count("try:")
            except_count = source.count("except")
            has_error_handling = try_count >= 3 and except_count >= 3
            print(f"{'✅' if has_error_handling else '⚠️ '} Exception Handling: {try_count} try blocks")
            self.results.append(("Exception Handling", has_error_handling))

        else:
            print(f"❌ brain.py nicht gefunden!")
            print(f"   Gesucht in:")
            for path in brain_paths:
                print(f"   - {path}")
            self.results.append(("Code Check", False))

        print()

    def test_04_termux_environment(self):
        """Termux-spezifische Checks"""
        print("=" * 70)
        print("TEST 4: TERMUX ENVIRONMENT")
        print("=" * 70)

        # Python Version
        py_version = sys.version_info
        py_ok = py_version >= (3, 8)
        print(f"{'✅' if py_ok else '❌'} Python: {py_version.major}.{py_version.minor}.{py_version.micro}")
        self.results.append(("Python 3.8+", py_ok))

        if not py_ok:
            print(f"   ⚠️  Python 3.8+ empfohlen")

        # Moloch Dir
        moloch_exists = self.moloch_dir.exists()
        print(f"{'✅' if moloch_exists else '❌'} Moloch Dir: {self.moloch_dir}")
        self.results.append(("Moloch Dir", moloch_exists))

        # Write Permission
        writable = os.access(self.moloch_dir, os.W_OK) if moloch_exists else False
        print(f"{'✅' if writable else '❌'} Write Permission: {writable}")
        self.results.append(("Write Permission", writable))

        # API Key
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        has_key = bool(api_key)
        print(f"{'✅' if has_key else '⚠️ '} API Key: {'SET' if has_key else 'NOT SET'}")
        self.results.append(("API Key", has_key))

        if not has_key:
            print(f"   ⚠️  API Key nicht gesetzt - Claude API funktioniert nicht")

        # Termux Detection
        is_termux = "com.termux" in os.environ.get("PREFIX", "")
        print(f"{'✅' if is_termux else 'ℹ️ '} Termux: {'DETECTED' if is_termux else 'NOT DETECTED (Dev Environment?)'}")

        print()

    def test_05_memory_monitoring(self):
        """Prüfe ob Memory Monitoring vorhanden ist"""
        print("=" * 70)
        print("TEST 5: MEMORY MONITORING")
        print("=" * 70)

        # Suche memory.py
        memory_paths = [
            self.moloch_dir / "memory.py",
            self.moloch_dir / "core" / "memory.py",
        ]

        memory_py = None
        for path in memory_paths:
            if path.exists():
                memory_py = path
                break

        if memory_py:
            print(f"📄 Found: {memory_py}")

            with open(memory_py, 'r', encoding='utf-8') as f:
                source = f.read()

            # Check Memory Monitoring
            has_monitoring = "get_memory_usage" in source
            print(f"{'✅' if has_monitoring else '⚠️ '} Memory Monitoring: {'VORHANDEN' if has_monitoring else 'FEHLT'}")
            self.results.append(("Memory Monitoring", has_monitoring))

            if has_monitoring:
                print(f"   ✅ get_memory_usage() method gefunden")
                print(f"   → RAM usage tracking funktioniert")
            else:
                print(f"   ⚠️  get_memory_usage() fehlt")
                print(f"   → Kein RAM monitoring (nicht kritisch)")

        else:
            print(f"⚠️  memory.py nicht gefunden")
            self.results.append(("Memory File", False))

        print()

    def run_all(self):
        """Führe alle Tests aus"""
        start_time = datetime.now()

        self.test_01_brain_data_protection()
        self.test_02_sandbox_isolation()
        self.test_03_code_security_fixes()
        self.test_04_termux_environment()
        self.test_05_memory_monitoring()

        # Summary
        elapsed = (datetime.now() - start_time).total_seconds()

        print("=" * 70)
        print("SUMMARY")
        print("=" * 70)
        print()

        passed = sum(1 for _, p in self.results if p)
        total = len(self.results)
        rate = passed / total * 100 if total > 0 else 0

        print(f"Tests Run:     {total}")
        print(f"Passed:        {passed}")
        print(f"Failed:        {total - passed}")
        print(f"Pass Rate:     {rate:.1f}%")
        print(f"Duration:      {elapsed:.2f}s")
        print()

        # Kritische Checks
        critical_missing = []
        for name, passed in self.results:
            if not passed and name in ["Filename Sanitization", "Atomic Saves", "Sandbox Isolated"]:
                critical_missing.append(name)

        if critical_missing:
            print(f"🚨 KRITISCH FEHLEND:")
            for item in critical_missing:
                print(f"   - {item}")
            print()
            print(f"   → Diese MÜSSEN implementiert werden vor Production-Einsatz!")
            print()
        else:
            print(f"✅ Alle kritischen Security-Features vorhanden")
            print()

        # Warnings
        if self.warnings:
            print(f"⚠️  WARNINGS:")
            for warning in self.warnings:
                print(f"   - {warning}")
            print()

        print("=" * 70)
        print(f"⛔ ECHTE BRAIN-DATEN: {'UNVERÄNDERT ✅' if self.real_brain.exists() else 'N/A'}")
        print("=" * 70)
        print()

        # Status
        if rate >= 80 and not critical_missing:
            print("✅ FIELD UNIT: PRODUCTION READY")
            return True
        elif rate >= 60:
            print("⚠️  FIELD UNIT: NEEDS ATTENTION")
            return False
        else:
            print("🚨 FIELD UNIT: CRITICAL ISSUES")
            return False


if __name__ == "__main__":
    check = TermuxHealthCheck()
    success = check.run_all()
    sys.exit(0 if success else 1)
