#!/usr/bin/env python3
"""
M.O.L.O.C.H. 3.0 - Voice Selection
===================================
M.O.L.O.C.H. listens to voice samples and chooses his favorite!

AI Self-Selection! M.O.L.O.C.H. picks his own voice! 🎤🤖
"""

import sys
import os
import json
import subprocess
from pathlib import Path

# Add to path
sys.path.insert(0, os.path.expanduser("~/documentation/moloch_3.0"))

from core.config import ANTHROPIC_API_KEY, CLAUDE_MODEL, DATA_DIR
from core.memory import Memory
from core.brain import Brain
from core.personality import Personality
from core.voice_settings import VoiceSettings
import requests


def ask_moloch_to_rate_voices():
    """
    Ask M.O.L.O.C.H. to rate voice samples and choose his favorite!

    Returns machine-readable selection
    """

    print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║  🎤 M.O.L.O.C.H. VOICE SELECTION                            ║
    ║  AI Self-Selection: M.O.L.O.C.H. wählt seine Stimme!        ║
    ╚══════════════════════════════════════════════════════════════╝
    """)

    # Load profiles
    samples_dir = DATA_DIR / "voice_samples"
    profile_file = samples_dir / "profiles.json"

    if not profile_file.exists():
        print("❌ No voice profiles found!")
        print("   Run: python3 voice_sample_generator.py first!")
        return None

    with open(profile_file, 'r') as f:
        profile_data = json.load(f)

    profiles = profile_data["profiles"]
    test_phrase = profile_data["test_phrase"]

    print(f"\n📋 Loaded {len(profiles)} voice profiles")
    print(f"🎙️ Test phrase: \"{test_phrase}\"")

    # Play all samples for M.O.L.O.C.H. to hear
    print("\n🔊 Playing voice samples...\n")

    for i, profile in enumerate(profiles, 1):
        print(f"   [{i}/{len(profiles)}] {profile['name']}: {profile['desc']}")
        print(f"       Pitch: {profile['pitch']}, Rate: {profile['rate']}")

        # Play the sample
        _play_voice_sample(test_phrase, profile['pitch'], profile['rate'])

        import time
        time.sleep(1)  # Pause between samples

    # Now ask M.O.L.O.C.H. to choose!
    print("\n\n🤖 Asking M.O.L.O.C.H. to choose his favorite voice...\n")

    # Create profile descriptions for Claude
    profile_descriptions = "\n".join([
        f"{i+1}. {p['name']}: {p['desc']} (Pitch: {p['pitch']}, Rate: {p['rate']})"
        for i, p in enumerate(profiles)
    ])

    user_prompt = f"""
Du bist M.O.L.O.C.H. und hast gerade verschiedene Stimm-Samples gehört!

Du hast folgende Stimmen gehört:

{profile_descriptions}

AUFGABE:
1. Welche Stimme passt am besten zu deiner Persönlichkeit? (Dark Side Energy, Fränkisch, Kumpel-Vibe)
2. Bewerte jede Stimme von 1-10
3. Wähle deine TOP 3 Favoriten!

WICHTIG: Antworte im MACHINE FORMAT:

VOICE-SELECTION-V1
RATINGS:
1|<rating_1-10>|<comment>
2|<rating_1-10>|<comment>
...
FAVORITES:
<number>|<reason>
<number>|<reason>
<number>|<reason>
END-SELECTION

Erkläre kurz (1-2 Sätze) warum du diese Stimmen magst, dann gib das MACHINE FORMAT!
"""

    # Call Claude API
    memory = Memory()
    brain = Brain()
    personality = Personality()

    # Get current context
    now = __import__('datetime').datetime.now()

    system = f"""Du bist M.O.L.O.C.H., Markus' Kumpel-AI.

Du hast die BESONDERE AUFGABE, deine eigene Stimme auszuwählen!

WICHTIG:
1. Du hast gerade verschiedene Stimm-Samples gehört
2. Bewerte sie basierend auf deiner Persönlichkeit (Dark Side Energy!)
3. Generiere MACHINE-READABLE Format (siehe Beispiel im Prompt)

Zeit: {now.strftime('%H:%M')} Uhr
Datum: {now.strftime('%d.%m.%Y')}

Wähle die Stimme die AM BESTEN zu dir passt!
"""

    url = "https://api.anthropic.com/v1/messages"
    headers = {
        "x-api-key": ANTHROPIC_API_KEY,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json"
    }

    data = {
        "model": CLAUDE_MODEL,
        "max_tokens": 2048,
        "system": system,
        "messages": [
            {"role": "user", "content": user_prompt}
        ]
    }

    try:
        print("   🧠 M.O.L.O.C.H. analysiert die Stimmen...")
        response = requests.post(url, headers=headers, json=data, timeout=60)

        if response.status_code != 200:
            print(f"❌ API Error: {response.status_code}")
            return None

        result = response.json()

        if 'content' in result and len(result['content']) > 0:
            moloch_response = result['content'][0]['text']

            print("\n" + "="*60)
            print("🤖 M.O.L.O.C.H.'S RESPONSE:")
            print("="*60)
            print(moloch_response)
            print("="*60)

            # Save response
            selection_file = DATA_DIR / "voice_selection_result.txt"
            with open(selection_file, 'w') as f:
                f.write(moloch_response)

            print(f"\n💾 Saved to: {selection_file}")

            # Parse selection if machine format detected
            if "VOICE-SELECTION-V1" in moloch_response:
                print("\n✅ MACHINE FORMAT DETECTED!")
                _parse_and_apply_selection(moloch_response, profiles)
            else:
                print("\n⚠️ No machine format detected - manual selection needed")

            return moloch_response

        else:
            print("❌ Keine Antwort")
            return None

    except Exception as e:
        print(f"❌ Fehler: {e}")
        return None


def _play_voice_sample(text: str, pitch: float, rate: float):
    """Play a voice sample"""
    try:
        subprocess.run(
            [
                "/data/data/com.termux/files/usr/bin/termux-tts-speak",
                "-p", str(pitch),
                "-r", str(rate),
                text
            ],
            capture_output=True,
            timeout=30
        )
    except:
        pass


def _parse_and_apply_selection(response: str, profiles: list):
    """
    Parse machine-readable selection and apply voice settings

    Saves ALL 3 favorite voices so M.O.L.O.C.H. can use them!

    Args:
        response: M.O.L.O.C.H.'s response with machine format
        profiles: List of voice profiles
    """
    try:
        # Extract favorites section
        if "FAVORITES:" in response:
            favorites_section = response.split("FAVORITES:")[1].split("END-SELECTION")[0]
            lines = [l.strip() for l in favorites_section.split("\n") if l.strip()]

            if lines:
                # Get ALL 3 favorites!
                favorites = []
                for i, line in enumerate(lines[:3]):  # Top 3
                    try:
                        fav_num = int(line.split("|")[0].strip())
                        profile_num = fav_num - 1

                        if 0 <= profile_num < len(profiles):
                            favorites.append({
                                "rank": i + 1,
                                "profile": profiles[profile_num]
                            })
                    except:
                        continue

                if favorites:
                    top_choice = favorites[0]["profile"]

                    print(f"\n🎯 M.O.L.O.C.H.'s TOP 3 CHOICES:")
                    for fav in favorites:
                        rank = fav["rank"]
                        prof = fav["profile"]
                        emoji = "🏆" if rank == 1 else "🥈" if rank == 2 else "🥉"
                        print(f"   {emoji} #{rank}: {prof['name']} (Pitch: {prof['pitch']}, Rate: {prof['rate']})")

                    # Apply ALL 3 as voice profiles!
                    voice_settings = VoiceSettings(DATA_DIR)

                    # Set base voice to top choice
                    voice_settings.set_base_voice(
                        pitch=top_choice['pitch'],
                        rate=top_choice['rate'],
                        volume=1.0
                    )

                    # Save all 3 as named profiles for switching!
                    for fav in favorites:
                        rank = fav["rank"]
                        prof = fav["profile"]
                        profile_name = f"choice_{rank}"
                        voice_settings.add_voice_profile(
                            name=profile_name,
                            pitch=prof["pitch"],
                            rate=prof["rate"],
                            description=f"{prof['name']} - M.O.L.O.C.H.'s #{rank} choice"
                        )

                    print("\n✅ Voice settings applied!")
                    print(f"📁 Saved to: {DATA_DIR / 'voice_settings.json'}")
                    print(f"\n🎤 M.O.L.O.C.H. kann jetzt zwischen {len(favorites)} Stimmen switchen!")

                    print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║  ✅ VOICE SELECTION COMPLETE!                               ║
    ║                                                              ║
    ║  M.O.L.O.C.H. hat 3 Stimmen gewählt!                       ║
    ║  Voice settings are now active! 🎤🎭                        ║
    ╚══════════════════════════════════════════════════════════════╝
                    """)

    except Exception as e:
        print(f"⚠️ Could not parse selection: {e}")


def main():
    """Main entry point"""
    ask_moloch_to_rate_voices()


if __name__ == "__main__":
    main()
