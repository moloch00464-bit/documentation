#!/usr/bin/env python3
"""
M.O.L.O.C.H. 3.0 - Voice Profile Test
Test all 3 selected voice profiles!
"""

import sys
from pathlib import Path

# Add moloch_3.0 to path
SCRIPT_DIR = Path(__file__).parent.absolute()
sys.path.insert(0, str(SCRIPT_DIR))

from core.voice_settings import VoiceSettings
from moloch_io.voice import VoiceIO

DATA_DIR = SCRIPT_DIR / "data"


def test_all_voices():
    """Test all 3 voice profiles M.O.L.O.C.H. chose!"""

    print("\n" + "="*60)
    print("🎤 M.O.L.O.C.H. VOICE PROFILE TEST")
    print("="*60)
    print("Testing all 3 selected voices!\n")

    # Create voice settings
    voice_settings = VoiceSettings(DATA_DIR)
    voice = VoiceIO(voice_settings=voice_settings)

    # Test phrase
    test_phrase = "Ich bin M.O.L.O.C.H., dein Kumpel-AI. Dark Side Energy, Alter!"

    # Check if custom profiles exist
    if "custom_profiles" not in voice_settings.settings:
        print("❌ Keine Voice Profiles gefunden!")
        print("   Führe erst 'python3 moloch_voice_selection.py' aus!")
        return

    profiles = voice_settings.settings.get("custom_profiles", {})

    if not profiles:
        print("❌ Keine Voice Profiles gefunden!")
        print("   Führe erst 'python3 moloch_voice_selection.py' aus!")
        return

    # Test each profile
    print("🎤 Teste alle Voice Profiles:\n")

    for i in range(1, 4):
        profile_name = f"choice_{i}"

        if profile_name in profiles:
            prof = profiles[profile_name]
            description = prof.get("description", "")
            pitch = prof.get("pitch", 1.0)
            rate = prof.get("rate", 1.0)

            emoji = "🏆" if i == 1 else "🥈" if i == 2 else "🥉"

            print(f"{emoji} Profile #{i}: {description}")
            print(f"   Pitch: {pitch}, Rate: {rate}")
            print(f"   🗣️  Höre...")

            # Speak with this profile!
            voice.speak(test_phrase, profile=profile_name)

            print()

        else:
            print(f"⚠️  Profile #{i} nicht gefunden!")

    # Test base voice (without profile)
    print("\n📢 Base Voice (ohne Profile):")
    base = voice_settings.settings["base_voice"]
    print(f"   Pitch: {base['pitch']}, Rate: {base['rate']}")
    print(f"   🗣️  Höre...")
    voice.speak(test_phrase)

    print("\n" + "="*60)
    print("✅ VOICE PROFILE TEST COMPLETE!")
    print("="*60)
    print()
    print("M.O.L.O.C.H. kann jetzt zwischen seinen 3 Stimmen switchen:")
    print("  voice.speak(text, profile='choice_1')  # Top choice! 🏆")
    print("  voice.speak(text, profile='choice_2')  # 2. Wahl 🥈")
    print("  voice.speak(text, profile='choice_3')  # 3. Wahl 🥉")
    print()


if __name__ == "__main__":
    test_all_voices()
