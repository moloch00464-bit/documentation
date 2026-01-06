#!/usr/bin/env python3
"""
M.O.L.O.C.H. Diagnose-Script
Checkt ob alles installiert ist was M.O.L.O.C.H. braucht
"""

import os
import sys
import subprocess

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
    print("""
╔═══════════════════════════════════════════════════════════════╗
║  M.O.L.O.C.H. DIAGNOSE                                        ║
╚═══════════════════════════════════════════════════════════════╝
""")

    results = []

    # ═══════════════════════════════════════════════════════════
    # TERMUX-API BEFEHLE
    # ═══════════════════════════════════════════════════════════
    print("\n🔧 TERMUX-API BEFEHLE:")
    print("-" * 50)

    commands = {
        "termux-tts-speak": "Text-to-Speech (Stimme)",
        "termux-microphone-record": "Audio aufnehmen (Ohren)",
        "termux-camera-photo": "Foto machen (Augen)",
        "termux-screenshot": "Screenshot (optional)",
        "ffmpeg": "Audio konvertieren"
    }

    for cmd, desc in commands.items():
        status = check_command(cmd)
        icon = "✅" if status else "❌"
        print(f"{icon} {cmd:30} - {desc}")
        results.append((cmd, status))

    # ═══════════════════════════════════════════════════════════
    # PYTHON PACKAGES
    # ═══════════════════════════════════════════════════════════
    print("\n🐍 PYTHON PACKAGES:")
    print("-" * 50)

    packages = {
        "requests": "HTTP Requests (für APIs)",
        "json": "JSON (Standard Library)",
        "subprocess": "Befehle ausführen (Standard)",
    }

    for pkg, desc in packages.items():
        status = check_python_package(pkg)
        icon = "✅" if status else "❌"
        print(f"{icon} {pkg:30} - {desc}")
        results.append((pkg, status))

    # ═══════════════════════════════════════════════════════════
    # API KEYS
    # ═══════════════════════════════════════════════════════════
    print("\n🔑 API KEYS:")
    print("-" * 50)

    api_keys = {
        "ANTHROPIC_API_KEY": "Claude API (KRITISCH!)",
        "OPENAI_API_KEY": "Whisper API (für Ohren)"
    }

    for key, desc in api_keys.items():
        status, value = check_env_var(key)
        icon = "✅" if status else "❌"
        print(f"{icon} {key:30} - {desc}")
        if status:
            print(f"   └─ {value}")
        results.append((key, status))

    # ═══════════════════════════════════════════════════════════
    # ZUSAMMENFASSUNG
    # ═══════════════════════════════════════════════════════════
    print("\n" + "=" * 50)
    total = len(results)
    ok = sum(1 for _, status in results if status)
    failed = total - ok

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
            print("\n🔑 Setze API Keys in ~/.bashrc:")
            print('   echo "export ANTHROPIC_API_KEY=your-key" >> ~/.bashrc')
            print("   source ~/.bashrc")

        if not check_env_var("OPENAI_API_KEY")[0]:
            print('   echo "export OPENAI_API_KEY=your-key" >> ~/.bashrc')
            print("   source ~/.bashrc")

    else:
        print("✅ ALLES INSTALLIERT! M.O.L.O.C.H. sollte funktionieren! 🤖🔥")

    print()

if __name__ == "__main__":
    main()
