#!/usr/bin/env python3
"""
M.O.L.O.C.H. 3.0 - Voice Calibration Tool
==========================================
Misst Background-Noise und Stimme → findet optimalen SPEECH_THRESHOLD
"""

import subprocess
import os
import time
from pathlib import Path

# Paths
HOME = Path.home()
DATA_DIR = HOME / "documentation/moloch_3.0/data"
CONFIG_FILE = HOME / "documentation/moloch_3.0/core/config.py"
TEST_FILE = DATA_DIR / "calibration_test.mp4"

def record_audio(duration: int, description: str) -> list:
    """
    Record audio and measure byte growth per 200ms

    Args:
        duration: Recording duration in seconds
        description: What to tell the user

    Returns:
        List of byte growth values
    """
    # Ensure data dir exists
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    # Remove old test file
    if TEST_FILE.exists():
        TEST_FILE.unlink()

    print(f"\n{'='*60}")
    print(f"📊 {description}")
    print(f"{'='*60}")
    print(f"⏱️  {duration} Sekunden...")
    time.sleep(2)  # Give user time to prepare

    # Start recording
    try:
        proc = subprocess.Popen(
            ["termux-microphone-record", "-f", str(TEST_FILE), "-l", "0"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
    except FileNotFoundError:
        print("❌ termux-microphone-record nicht gefunden!")
        return []

    # Measure byte growth
    start_time = time.time()
    last_size = 0
    growth_values = []

    time.sleep(0.5)  # Wait for file to be created

    print("🎤 ", end="", flush=True)

    while time.time() - start_time < duration:
        if TEST_FILE.exists():
            try:
                current_size = TEST_FILE.stat().st_size
                growth = current_size - last_size
                last_size = current_size

                growth_values.append(growth)

                # Visual feedback
                if growth > 100:
                    print("█", end="", flush=True)
                else:
                    print(".", end="", flush=True)

            except:
                pass

        time.sleep(0.2)  # Check every 200ms

    print()

    # Stop recording
    for _ in range(3):
        subprocess.run(
            ["termux-microphone-record", "-q"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        time.sleep(0.1)

    time.sleep(0.3)

    return growth_values


def analyze_growth(values: list, label: str) -> dict:
    """Analyze byte growth values"""
    if not values:
        return {"min": 0, "max": 0, "avg": 0, "median": 0}

    sorted_values = sorted(values)

    stats = {
        "min": min(values),
        "max": max(values),
        "avg": sum(values) / len(values),
        "median": sorted_values[len(sorted_values) // 2]
    }

    print(f"\n📈 {label}:")
    print(f"   Min:    {stats['min']:.0f} bytes/200ms")
    print(f"   Max:    {stats['max']:.0f} bytes/200ms")
    print(f"   Avg:    {stats['avg']:.0f} bytes/200ms")
    print(f"   Median: {stats['median']:.0f} bytes/200ms")

    return stats


def suggest_threshold(noise_stats: dict, voice_stats: dict):
    """Suggest optimal SPEECH_THRESHOLD"""

    print(f"\n{'='*60}")
    print("🎯 EMPFEHLUNG")
    print(f"{'='*60}")

    # Noise level (use max to be safe)
    noise_level = noise_stats['max']

    # Voice level (use median - typical speaking)
    voice_level = voice_stats['median']

    # Threshold should be between noise and voice
    # Add 50% safety margin above noise
    suggested = int(noise_level + (voice_level - noise_level) * 0.3)

    # Minimum threshold
    if suggested < 150:
        suggested = 150

    print(f"\n📊 Hintergrund-Noise (max): {noise_level:.0f} bytes/200ms")
    print(f"📊 Deine Stimme (median):   {voice_level:.0f} bytes/200ms")
    print(f"\n✅ EMPFOHLENER THRESHOLD:   {suggested} bytes/200ms")

    # Quality check
    if voice_level < noise_level * 1.5:
        print("\n⚠️  WARNUNG: Deine Stimme ist zu leise für die Umgebung!")
        print("   → Sprich LAUTER oder reduziere Background-Noise (TV leiser!)")
        return None

    return suggested


def apply_threshold(threshold: int) -> bool:
    """Apply threshold to config.py"""

    print(f"\n{'='*60}")
    print("💾 AUTO-CONFIG")
    print(f"{'='*60}")

    try:
        # Read config
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        # Find and replace SPEECH_THRESHOLD line
        modified = False
        for i, line in enumerate(lines):
            if 'SPEECH_THRESHOLD' in line and '=' in line and not line.strip().startswith('#'):
                # Replace the line
                old_line = line.strip()
                lines[i] = f"SPEECH_THRESHOLD = {threshold}        # Auto-configured by calibrate_voice.py\n"
                modified = True
                print(f"\n📝 Alte Einstellung: {old_line}")
                print(f"✅ Neue Einstellung: SPEECH_THRESHOLD = {threshold}")
                break

        if not modified:
            print("\n❌ SPEECH_THRESHOLD Zeile nicht gefunden in config.py!")
            return False

        # Write back
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            f.writelines(lines)

        print(f"\n✅ Config gespeichert: {CONFIG_FILE}")
        return True

    except Exception as e:
        print(f"\n❌ Fehler beim Schreiben: {e}")
        return False


def main():
    """Main calibration routine"""

    print("""
    ███╗   ███╗ ██████╗ ██╗      ██████╗  ██████╗██╗  ██╗
    ████╗ ████║██╔═══██╗██║     ██╔═══██╗██╔════╝██║  ██║
    ██╔████╔██║██║   ██║██║     ██║   ██║██║     ███████║
    ██║╚██╔╝██║██║   ██║██║     ██║   ██║██║     ██╔══██║
    ██║ ╚═╝ ██║╚██████╔╝███████╗╚██████╔╝╚██████╗██║  ██║
    ╚═╝     ╚═╝ ╚═════╝ ╚══════╝ ╚═════╝  ╚═════╝╚═╝  ╚═╝

    M.O.L.O.C.H. 3.0 - Voice Calibration
    Findet den optimalen SPEECH_THRESHOLD für deine Umgebung!
    """)

    input("\n👉 Drücke ENTER um zu starten...")

    # Test 1: Background noise (TV, Umgebung)
    print("\n\n" + "="*60)
    print("TEST 1: HINTERGRUND-NOISE")
    print("="*60)
    print("\n📺 Lass den Fernseher/Musik laufen wie normal!")
    print("⚠️  Aber NICHT SPRECHEN während der Aufnahme!")

    input("\n👉 Bereit? Drücke ENTER...")

    noise_values = record_audio(
        duration=10,
        description="Messe Background-Noise (10s) - NICHT SPRECHEN!"
    )

    noise_stats = analyze_growth(noise_values, "Background-Noise")

    # Test 2: Normal speaking
    print("\n\n" + "="*60)
    print("TEST 2: DEINE STIMME")
    print("="*60)
    print("\n🗣️  Sprich NORMAL und KONTINUIERLICH!")
    print("   (z.B. zähle von 1 bis 100, oder erzähl was)")

    input("\n👉 Bereit? Drücke ENTER...")

    voice_values = record_audio(
        duration=10,
        description="Messe deine Stimme (10s) - JETZT SPRECHEN!"
    )

    voice_stats = analyze_growth(voice_values, "Deine Stimme")

    # Suggest threshold
    suggested = suggest_threshold(noise_stats, voice_stats)

    if suggested:
        print(f"\n✅ Kalibrierung erfolgreich!")

        # Ask if auto-apply
        print(f"\n{'='*60}")
        response = input("\n🤖 Soll ich SPEECH_THRESHOLD automatisch setzen? [J/n]: ").strip().lower()

        if response in ['', 'j', 'ja', 'y', 'yes']:
            if apply_threshold(suggested):
                print(f"\n🎉 FERTIG! Config wurde aktualisiert!")
                print(f"\n📝 Nächster Schritt:")
                print(f"   python3 moloch3_voice.py")
                print(f"\n   → Du solltest jetzt █ sehen wenn du sprichst!")
                print(f"   → Recording stoppt automatisch nach 1.5s Pause!")
            else:
                print(f"\n⚠️  Auto-Config fehlgeschlagen!")
                print(f"   Manuelle Änderung: nano {CONFIG_FILE}")
                print(f"   Setze: SPEECH_THRESHOLD = {suggested}")
        else:
            print(f"\n💡 Manuelle Änderung:")
            print(f"   nano {CONFIG_FILE}")
            print(f"   Setze: SPEECH_THRESHOLD = {suggested}")

    # Cleanup
    if TEST_FILE.exists():
        TEST_FILE.unlink()

    print()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Abgebrochen")
    except Exception as e:
        print(f"\n❌ Fehler: {e}")
