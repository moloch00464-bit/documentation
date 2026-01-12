#!/usr/bin/env python3
"""
M.O.L.O.C.H. Diagnose-Script
Checkt ob alles installiert ist was M.O.L.O.C.H. braucht

Usage:
    python diagnose.py          # Human-readable output
    python diagnose.py --json   # JSON output für Claude (Copy & Paste!)
"""

import os
import sys
import subprocess
import json
from datetime import datetime

def check_command(cmd):
    """Checkt ob ein Befehl existiert"""
    try:
        result = subprocess.run(
            ["which", cmd],
            capture_output=True,
            timeout=5
        )
        return result.returncode == 0
    except:
        return False

def check_python_package(package):
    """Checkt ob Python Package installiert ist"""
    try:
        __import__(package)
        return True
    except ImportError:
        return False

def check_env_var(var):
    """Checkt ob Umgebungsvariable gesetzt ist"""
    value = os.getenv(var)
    if value and len(value) > 10:
        return True, f"{value[:10]}..."
    return False, "NICHT GESETZT"

def main():
    # Check if JSON mode
    json_mode = "--json" in sys.argv

    if not json_mode:
        print("""
╔═══════════════════════════════════════════════════════════════╗
║  M.O.L.O.C.H. DIAGNOSE                                        ║
╚═══════════════════════════════════════════════════════════════╝
""")

    # Data structures
    results = []
    problems = []
    warnings = []
    info = {}

    # ═══════════════════════════════════════════════════════════
    # TERMUX-API BEFEHLE
    # ═══════════════════════════════════════════════════════════
    if not json_mode:
        print("\n🔧 TERMUX-API BEFEHLE:")
        print("-" * 50)

    commands = {
        "termux-tts-speak": "Text-to-Speech (Stimme)",
        "termux-speech-to-text": "Speech-to-Text (Ohren)",
        "termux-microphone-record": "Audio aufnehmen (optional)",
        "termux-camera-photo": "Foto machen (Augen)",
        "termux-screenshot": "Screenshot (optional)",
        "ffmpeg": "Audio konvertieren"
    }

    termux_results = {}
    for cmd, desc in commands.items():
        status = check_command(cmd)
        termux_results[cmd] = status

        if not json_mode:
            icon = "✅" if status else "❌"
            print(f"{icon} {cmd:30} - {desc}")

        results.append((cmd, status))

        # Optional: screenshot, microphone-record
        optional_cmds = ["termux-screenshot", "termux-microphone-record"]

        if not status and cmd not in optional_cmds:
            if cmd == "ffmpeg":
                problems.append({
                    "id": f"missing_{cmd}",
                    "severity": "medium",
                    "category": "system",
                    "message": f"{cmd} nicht installiert",
                    "description": desc,
                    "fix": "pkg install ffmpeg"
                })
            else:
                problems.append({
                    "id": f"missing_{cmd}",
                    "severity": "critical",
                    "category": "termux_api",
                    "message": f"{cmd} nicht installiert",
                    "description": desc,
                    "fix": "pkg install termux-api && (Termux:API App in F-Droid installieren)"
                })

    info["termux_commands"] = termux_results

    # ═══════════════════════════════════════════════════════════
    # PYTHON PACKAGES
    # ═══════════════════════════════════════════════════════════
    if not json_mode:
        print("\n🐍 PYTHON PACKAGES:")
        print("-" * 50)

    packages = {
        "requests": "HTTP Requests (für APIs)",
        "json": "JSON (Standard Library)",
        "subprocess": "Befehle ausführen (Standard)",
    }

    python_results = {}
    for pkg, desc in packages.items():
        status = check_python_package(pkg)
        python_results[pkg] = status

        if not json_mode:
            icon = "✅" if status else "❌"
            print(f"{icon} {pkg:30} - {desc}")

        results.append((pkg, status))

        if not status:
            problems.append({
                "id": f"missing_python_{pkg}",
                "severity": "critical",
                "category": "python",
                "message": f"Python-Paket '{pkg}' fehlt",
                "description": desc,
                "fix": f"pip install {pkg}"
            })

    info["python_packages"] = python_results

    # ═══════════════════════════════════════════════════════════
    # API KEYS
    # ═══════════════════════════════════════════════════════════
    if not json_mode:
        print("\n🔑 API KEYS:")
        print("-" * 50)

    api_keys = {
        "ANTHROPIC_API_KEY": "Claude API (KRITISCH!)"
    }

    api_results = {}
    for key, desc in api_keys.items():
        status, value = check_env_var(key)
        api_results[key] = status

        if not json_mode:
            icon = "✅" if status else "❌"
            print(f"{icon} {key:30} - {desc}")
            if status:
                print(f"   └─ {value}")

        results.append((key, status))

        if not status:
            severity = "critical" if key == "ANTHROPIC_API_KEY" else "medium"
            problems.append({
                "id": f"missing_{key}",
                "severity": severity,
                "category": "api_keys",
                "message": f"{key} nicht gesetzt",
                "description": desc,
                "fix": f'echo "export {key}=your-key" >> ~/.bashrc && source ~/.bashrc'
            })

    info["api_keys"] = api_results

    # ═══════════════════════════════════════════════════════════
    # ZUSAMMENFASSUNG
    # ═══════════════════════════════════════════════════════════
    total = len(results)
    ok = sum(1 for _, status in results if status)
    failed = total - ok

    # Status bestimmen
    critical_problems = [p for p in problems if p["severity"] == "critical"]
    if critical_problems:
        status = "BROKEN"
        summary = f"❌ {len(critical_problems)} kritische Probleme"
    elif problems:
        status = "DEGRADED"
        summary = f"⚠️ {len(problems)} Probleme"
    elif warnings:
        status = "WARNING"
        summary = f"⚡ {len(warnings)} Warnungen"
    else:
        status = "HEALTHY"
        summary = "✅ Alles OK"

    # JSON MODE OUTPUT
    if json_mode:
        report = {
            "system": "M.O.L.O.C.H. 3.0",
            "timestamp": datetime.now().isoformat(),
            "status": status,
            "summary": summary,
            "stats": {
                "total_checks": total,
                "passed": ok,
                "failed": failed
            },
            "problems": problems,
            "warnings": warnings,
            "info": info
        }

        print("=" * 70)
        print("📋 COPY & PASTE FÜR CLAUDE:")
        print("=" * 70)
        print()
        print(json.dumps(report, indent=2, ensure_ascii=False))
        print()
        print("=" * 70)
        print("👆 Kopiere das JSON oben und schicke es an Claude!")
        print("=" * 70)
        return

    # HUMAN-READABLE OUTPUT
    print("\n" + "=" * 50)
    print(f"\n📊 ERGEBNIS: {ok}/{total} OK, {failed} Fehler\n")

    if failed > 0:
        print("🔧 WAS FEHLT?\n")

        # Termux-API Befehle fehlen?
        missing_cmds = [cmd for cmd, status in results[:5] if not status]
        if missing_cmds:
            print("📦 Installiere Termux-API:")
            print("   pkg install termux-api")
            if "ffmpeg" in missing_cmds:
                print("   pkg install ffmpeg")

        # Python Packages fehlen?
        missing_pkgs = [pkg for pkg, status in results[5:8] if not status]
        if missing_pkgs:
            print("\n🐍 Installiere Python Packages:")
            print("   pip install requests")

        # API Keys fehlen?
        if not check_env_var("ANTHROPIC_API_KEY")[0]:
            print("\n🔑 Setze ANTHROPIC_API_KEY in ~/.bashrc:")
            print('   echo "export ANTHROPIC_API_KEY=your-key" >> ~/.bashrc')
            print("   source ~/.bashrc")

    else:
        print("✅ ALLES INSTALLIERT! M.O.L.O.C.H. sollte funktionieren! 🤖🔥")

    print()
    print("💡 TIPP: Für JSON-Output (Copy & Paste an Claude):")
    print("   python diagnose.py --json")
    print()

if __name__ == "__main__":
    main()
