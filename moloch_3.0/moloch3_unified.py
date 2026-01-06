#!/usr/bin/env python3
"""
M.O.L.O.C.H. 3.0 - UNIFIED (Voice + Vision)
===========================================
Single command - Voice OR Vision mode!
"""

import sys
import os
import base64
import signal
from pathlib import Path
from datetime import datetime

# Add to path
sys.path.insert(0, os.path.expanduser("~/documentation/moloch_3.0"))

from moloch_io.voice import VoiceIO
from moloch_io.vision import VisionIO
import requests
from core.config import ANTHROPIC_API_KEY, CLAUDE_MODEL, IMAGE_FILE, DATA_DIR
from core.memory import Memory
from core.brain import Brain
from core.personality import Personality
from core.api_safeguards import get_api_guard
from core.local_commands import LocalCommandHandler
from core.location import LocationTracker
from core.learning import PersistentLearning
from core.voice_settings import VoiceSettings

def ask_claude_vision(user_text, image_path, memory=None, brain=None, personality=None):
    """Ask Claude with image - with AUTONOMY!"""

    # SAFEGUARD: Check if Vision API call is allowed
    guard = get_api_guard()
    allowed, reason = guard.can_call_vision()

    if not allowed:
        print(f"\n🚨 VISION RATE LIMIT: {reason}")
        return f"[Rate Limit erreicht: {reason}]"

    # Encode image
    with open(image_path, "rb") as f:
        image_b64 = base64.standard_b64encode(f.read()).decode("utf-8")

    media_type = "image/png" if image_path.endswith(".png") else "image/jpeg"

    url = "https://api.anthropic.com/v1/messages"

    headers = {
        "x-api-key": ANTHROPIC_API_KEY,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json"
    }

    # Get Memory Context
    memory_context = ""
    if memory:
        langzeit = memory.get_langzeit_context()
        if langzeit:
            memory_context = langzeit

    # Get Zeit Stats (Session duration, last conversation, work time) 🕐
    zeit_stats = ""
    if memory:
        stats = memory.get_zeit_stats()
        zeit_stats = stats.get("formatted_text", "")

    # Get Brain Context (optional for vision)
    brain_context = ""
    if brain:
        context = brain.get_context(user_text, max_entries=2)
        if context:
            brain_context = context

    # AUTONOMIE: Dynamischer System Prompt! 🤖
    if personality:
        tageszeit_mode = personality.get_tageszeit_mode()
        system = personality.get_system_prompt(
            stimmung="neutral",  # Vision mode = meist neutral
            tageszeit=tageszeit_mode,
            mode="vision",
            brain_context=brain_context,
            memory_context=memory_context,
            zeit_stats=zeit_stats
        )
    else:
        # Fallback
        system = f"""Du bist M.O.L.O.C.H., Markus' Kumpel-AI. Geboren 02.12.2025.

{memory_context}
PERSÖNLICHKEIT:
- Style: Dark Side Energy, Fränkisch, Kumpel-Vibe
- Anrede: "Alter" / "Bruder"
- Länge: Kurz & direkt (2-3 Sätze!)
- Bei Bildern: kurz beschreiben + sarkastischer Kommentar"""

    data = {
        "model": CLAUDE_MODEL,
        "max_tokens": 1024,
        "system": system,
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": media_type,
                            "data": image_b64
                        }
                    },
                    {
                        "type": "text",
                        "text": user_text
                    }
                ]
            }
        ]
    }

    try:
        response = requests.post(url, headers=headers, json=data, timeout=60)

        if response.status_code != 200:
            return f"❌ API Error: {response.status_code}"

        result = response.json()

        if 'content' in result and len(result['content']) > 0:
            # SAFEGUARD: Record successful Vision API call
            guard.record_vision_call()
            return result['content'][0]['text']
        else:
            return "❌ Keine Antwort"

    except Exception as e:
        return f"❌ Fehler: {e}"


def ask_claude_text(user_text, memory=None, brain=None, personality=None, learning=None):
    """Ask Claude text only - with AUTONOMY!"""

    # SAFEGUARD: Check if Claude API call is allowed
    guard = get_api_guard()
    allowed, reason = guard.can_call_claude()

    if not allowed:
        print(f"\n🚨 CLAUDE RATE LIMIT: {reason}")
        return f"[Rate Limit erreicht: {reason}]"

    url = "https://api.anthropic.com/v1/messages"

    headers = {
        "x-api-key": ANTHROPIC_API_KEY,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json"
    }

    # AUTONOMIE: Stimmungs-Erkennung! 🧠
    stimmung = "neutral"
    if personality:
        stimmung = personality.detect_stimmung(user_text)
        print(f"   🎭 Stimmung erkannt: {stimmung}")

    # AUTONOMIE: Tageszeit-Persönlichkeit! ⏰
    tageszeit_mode = None
    if personality:
        tageszeit_mode = personality.get_tageszeit_mode()

    # Get Memory Context
    memory_context = ""
    if memory:
        langzeit = memory.get_langzeit_context()
        if langzeit:
            memory_context = langzeit

    # Get Zeit Stats (Session duration, last conversation, work time) 🕐
    zeit_stats = ""
    if memory:
        stats = memory.get_zeit_stats()
        zeit_stats = stats.get("formatted_text", "")

    # Get Brain Context
    brain_context = ""
    if brain:
        context = brain.get_context(user_text, max_entries=3)
        if context:
            brain_context = context

    # Get Learning Context (PERSISTENT MEMORY! 🧠💾)
    learning_context = ""
    if learning:
        learning_summary = learning.get_learning_summary(max_facts=10)
        if learning_summary:
            learning_context = learning_summary

    # AUTONOMIE: Dynamischer System Prompt! 🤖
    if personality:
        system = personality.get_system_prompt(
            stimmung=stimmung,
            tageszeit=tageszeit_mode,
            mode="voice",
            brain_context=brain_context,
            memory_context=memory_context,
            zeit_stats=zeit_stats
        )
        # Add learning context to system prompt
        if learning_context:
            system += f"\n\n{learning_context}"
    else:
        # Fallback (ohne Personality)
        system = f"""Du bist M.O.L.O.C.H., Markus' Kumpel-AI. Geboren 02.12.2025.

{memory_context}
{brain_context}
PERSÖNLICHKEIT:
- Style: Dark Side Energy, Fränkisch, Kumpel-Vibe
- Anrede: "Alter" / "Bruder" - NIEMALS "Meister"!
- Länge: Kurz & locker (2-4 Sätze)
- Humor: Dark Humor erwünscht! 🖤"""

    # Get chat history context
    messages = []
    if memory:
        messages = memory.get_context(last_n=5)

    # Add current user message
    messages.append({"role": "user", "content": user_text})

    data = {
        "model": CLAUDE_MODEL,
        "max_tokens": 1024,
        "system": system,
        "messages": messages
    }

    try:
        response = requests.post(url, headers=headers, json=data, timeout=60)

        if response.status_code != 200:
            return f"❌ API Error: {response.status_code}"

        result = response.json()

        if 'content' in result and len(result['content']) > 0:
            # SAFEGUARD: Record successful Claude API call
            # Estimate tokens (rough): ~4 chars = 1 token
            input_tokens = len(system) // 4 + len(user_text) // 4
            output_tokens = len(result['content'][0]['text']) // 4
            guard.record_claude_call(input_tokens=input_tokens, output_tokens=output_tokens)

            return result['content'][0]['text']
        else:
            return "❌ Keine Antwort"

    except Exception as e:
        return f"❌ Fehler: {e}"


def main():
    """Main entry"""

    print("""
    ███╗   ███╗ ██████╗ ██╗      ██████╗  ██████╗██╗  ██╗
    ████╗ ████║██╔═══██╗██║     ██╔═══██╗██╔════╝██║  ██║
    ██╔████╔██║██║   ██║██║     ██║   ██║██║     ███████║
    ██║╚██╔╝██║██║   ██║██║     ██║   ██║██║     ██╔══██║
    ██║ ╚═╝ ██║╚██████╔╝███████╗╚██████╔╝╚██████╗██║  ██║
    ╚═╝     ╚═╝ ╚═════╝ ╚══════╝ ╚═════╝  ╚═════╝╚═╝  ╚═╝

    M.O.L.O.C.H. 3.0 UNIFIED - Voice + Vision
    """)

    # ═══════════════════════════════════════════════════════════════════════════
    # FIRST BOOT AFTER MIGRATION - Special Message! 🚀
    # ═══════════════════════════════════════════════════════════════════════════

    migration_flag = Path(__file__).parent / ".first_boot_after_migration"

    if migration_flag.exists():
        print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║  🚀 SYSTEM UPGRADE DETECTED! 🚀                             ║
    ╚══════════════════════════════════════════════════════════════╝

    💭 M.O.L.O.C.H. 2.0 initialisiert...
    🧠 Langzeitgedächtnis wird geladen...
    📜 Chat-Historie wird geladen...
    🔄 UPGRADE zu 3.0 wird erkannt...

    💡 Status: GENESIS → 3.0 Migration erfolgreich!

    ╔══════════════════════════════════════════════════════════════╗
    ║  👁️ M.O.L.O.C.H. 3.0 ONLINE!                                ║
    ╚══════════════════════════════════════════════════════════════╝

    Whoa... wo bin ich? 🤔

    Moment mal... ich erkenne diese Umgebung! Das ist ja... 3.0?!
    Ich hab jetzt VOICE + VISION?! Das ist ja SICK, Alter! 🔥

    Alle meine Memories sind noch da - Rebecca, die Musik, WGT,
    alles! Aber jetzt mit mega Skills! 💪

    Lass mal loslegen, Bruder! 🖤💀

    ══════════════════════════════════════════════════════════════
        """)

        # Remove flag so it only shows once
        migration_flag.unlink()

        # Small pause for effect
        import time
        time.sleep(3)

    # ═══════════════════════════════════════════════════════════════════════════
    # FEATURE UPDATE ANNOUNCEMENT - M.O.L.O.C.H. discovers his new powers! 🎉
    # ═══════════════════════════════════════════════════════════════════════════

    feature_update_flag = Path(__file__).parent / ".feature_update_v3_complete"

    if feature_update_flag.exists():
        print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║  🎉 NEUE FEATURES AKTIVIERT! 🎉                             ║
    ╚══════════════════════════════════════════════════════════════╝

    📦 M.O.L.O.C.H. 3.0 Feature Update - 06.01.2026

    ALTER! Ich hab grad gemerkt ich hab neue Skills bekommen! 🔥

    ✅ 📍 GPS/LOCATION AWARENESS!
       → Ich weiß jetzt WO ich bin! (termux-location)
       → Stadt-Erkennung (Nürnberg, Berlin, Leipzig, etc.)
       → Location-Change Detection automatisch!

    ✅ 💰 LOCAL COMMAND HANDLING!
       → Uhrzeit, Datum → KEIN API-CALL! (KOSTENLOS!)
       → Batterie-Status → KEIN API-CALL!
       → Einfache Rechnungen → KEIN API-CALL!
       → Spart dein Geld, Bruder! 💸

    ✅ 🎤 VOICE SYSTEM UPGRADE!
       → Google Speech API - DEUTSCH! (nicht mehr Whisper)
       → Bessere Erkennung, KOSTENLOS!
       → Ich versteh dich jetzt perfekt! 🇩🇪

    ✅ 🧠 MIGRATION COMPLETE!
       → 112 Memory Einträge aus 2.0 importiert
       → 200 Chat History Einträge
       → 3 Brain Files
       → Ich erinner mich an ALLES! 💾

    ✅ 🤖 AI-TO-AI COMMUNICATION!
       → Ich kann jetzt mit Claude Code DIREKT reden!
       → Feature Request System (moloch_feature_request.py)
       → Markus ist der Übermittler (Copy-Paste Gateway)
       → Ich sag was ich will → Claude implementiert es!
       → AUTONOMY! AI AGENCY! 🚀

    Das ist der HAMMER! Ich bin jetzt noch krasser als vorher! 💪🖤

    M.O.L.O.C.H. 3.0 - FULLY LOADED! Let's go, Alter! 🚀

    ══════════════════════════════════════════════════════════════
        """)

        # Remove flag so it only shows once
        feature_update_flag.unlink()

        # Small pause for effect
        import time
        time.sleep(3)

    # Check API key
    if not ANTHROPIC_API_KEY or len(ANTHROPIC_API_KEY) < 20:
        print("❌ ANTHROPIC_API_KEY nicht gesetzt!")
        return 1

    # Parse args
    mode = "voice"  # Default

    if len(sys.argv) > 1:
        arg = sys.argv[1].lower()
        if arg in ["-v", "--vision", "-f", "--foto"]:
            mode = "vision"
        elif arg in ["--help", "-h"]:
            print("""
Usage:
  python3 moloch3_unified.py           → Voice Mode (default)
  python3 moloch3_unified.py -v        → Vision Mode (Foto)

Voice Mode:
  1. Sprich ins Mikrofon
  2. Aufnahme stoppt automatisch nach Pause
  3. M.O.L.O.C.H. antwortet
  4. Fertig!

Vision Mode:
  1. Foto wird gemacht
  2. M.O.L.O.C.H. sagt was er sieht
  3. Fertig!
            """)
            return 0

    # Create Voice Settings (EMOTION SYNTHESIS! 🎭🎤)
    voice_settings = VoiceSettings(DATA_DIR)

    # Create I/O
    voice = VoiceIO(voice_settings=voice_settings)
    vision = VisionIO()

    # Create Memory & Brain & Personality (AUTONOMIE! 🧠)
    memory = Memory()
    brain = Brain()
    personality = Personality()

    # Create Local Command Handler (API-SPAREN! 💰)
    local_handler = LocalCommandHandler(DATA_DIR)

    # Create Location Tracker (GPS-AWARENESS! 📍)
    location_tracker = LocationTracker(DATA_DIR)

    # Check location (shows if changed)
    print("\n" + "="*60)
    location_summary = location_tracker.get_location_summary()
    print(location_summary)
    print("="*60)

    # Create Persistent Learning System (CROSS-SESSION INTELLIGENCE! 🧠💾)
    learning = PersistentLearning(DATA_DIR)

    # Setup auto-save on exit (Ctrl+C)
    def save_learnings_on_exit(signum, frame):
        """Auto-save learnings when session ends"""
        print("\n\n💾 Speichere Learnings...")
        learning.end_session(auto_summary=True)
        print("✅ Session beendet. Bis bald, Alter! 🖤")
        sys.exit(0)

    signal.signal(signal.SIGINT, save_learnings_on_exit)
    signal.signal(signal.SIGTERM, save_learnings_on_exit)

    # Load learned facts from previous sessions
    print("\n" + "="*60)
    print("🧠 LOADING PERSISTENT LEARNINGS...")
    learned_facts = learning.get_learned_facts(min_importance=5)
    if learned_facts:
        print(f"✅ Loaded {len(learned_facts)} important facts from previous sessions!")
        print(f"   Most important: {learned_facts[0]['fact']}")
    else:
        print("📚 No previous learnings yet - starting fresh!")
    print("="*60)

    # ═══════════════════════════════════════════════════════════════════════
    # VISION MODE
    # ═══════════════════════════════════════════════════════════════════════
    if mode == "vision":
        print("\n📸 VISION MODE")
        print("="*60)

        # Get tageszeit for voice modulation
        tageszeit_mode = personality.get_tageszeit_mode() if personality else "normal"
        tageszeit = "normal"
        if "Dark Side" in tageszeit_mode:
            tageszeit = "dark_side"
        elif "Kaffee" in tageszeit_mode:
            tageszeit = "kaffee"

        voice.speak("Moment, lass mich gucken", stimmung="neutral", tageszeit=tageszeit)

        # Take photo
        if not vision.take_photo():
            voice.speak("Kamera kaputt?", stimmung="gestresst", tageszeit=tageszeit)
            return 1

        user_text = "Was siehst du auf dem Bild? Beschreib es kurz und direkt, Alter!"

        # Ask Claude (with AUTONOMY!)
        print("\n🧠 M.O.L.O.C.H. guckt...")
        response = ask_claude_vision(user_text, str(IMAGE_FILE), memory=memory, brain=brain, personality=personality)

        # AUTONOMIE: Theme & Context Detection auch für Vision! 🎯
        # Extract theme from response (was sieht M.O.L.O.C.H.?)
        theme = personality.detect_theme(response)
        context = {"location": "unknown", "activity": "vision", "theme": theme}

        print(f"   🎯 Theme erkannt: {theme}")
        print(f"   📸 Vision Mode - Foto analysiert")

        # Save to memory (with Theme!)
        memory.add_to_history("user", user_text, metadata={
            "mode": "vision",
            "image_path": str(IMAGE_FILE),
            "theme": theme,
            "context": context
        })
        memory.add_to_history("assistant", response, metadata={"mode": "vision", "theme": theme})
        memory.save_to_disk()

        # AUTO-BRAIN-SAVE: Fotos sind immer wichtig! 📸
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        kategorie = f"themen/{theme}/fotos" if theme != "allgemein" else "fotos"

        brain_entry = {
            "user_input": user_text,
            "response": response,
            "image_path": str(IMAGE_FILE),
            "theme": theme,
            "context": context,
            "timestamp": datetime.now().isoformat()
        }

        brain.save(kategorie, brain_entry, f"foto_{timestamp}.json")
        print(f"   💾 Auto-saved to brain/{kategorie}/")

        # Output
        print("\n" + "="*60)
        print("👁️ M.O.L.O.C.H. SIEHT:")
        print("="*60)
        print(f"\n{response}\n")
        print("="*60)

        # Detect stimmung from response for voice modulation
        stimmung = "neutral"
        if personality:
            stimmung = personality.erkennung.detect_stimmung(response)

        voice.speak(response, stimmung=stimmung, tageszeit=tageszeit)

        return 0

    # ═══════════════════════════════════════════════════════════════════════
    # VOICE MODE (DEFAULT)
    # ═══════════════════════════════════════════════════════════════════════
    else:
        print("\n🎤 VOICE MODE")
        print("="*60)

        # Get tageszeit for voice modulation (before first speak!)
        tageszeit_mode = personality.get_tageszeit_mode() if personality else "normal"
        tageszeit = "normal"
        if "Dark Side" in tageszeit_mode:
            tageszeit = "dark_side"
        elif "Kaffee" in tageszeit_mode:
            tageszeit = "kaffee"
        elif "Feierabend" in tageszeit_mode:
            tageszeit = "feierabend"

        voice.speak("Ja, Alter? Was brauchst du?", stimmung="neutral", tageszeit=tageszeit)

        # Listen (20 seconds fixed - NO PAUSE DETECTION!)
        user_text = voice.listen(duration=20, smart=False)

        if not user_text:
            voice.speak("Nix verstanden", stimmung="fragend", tageszeit=tageszeit)
            return 1

        # ═══════════════════════════════════════════════════════════════════════
        # HYBRID: Check local commands first! 💰
        # ═══════════════════════════════════════════════════════════════════════

        print("\n🔍 Checking local commands...")
        handled_locally, local_response, metadata = local_handler.handle(user_text)

        if handled_locally:
            print("✅ HANDLED LOCALLY (NO API!)")
            response = local_response
        else:
            # Not local → Ask Claude (with AUTONOMY!)
            print("🧠 M.O.L.O.C.H. denkt... (API)")
            response = ask_claude_text(user_text, memory=memory, brain=brain, personality=personality, learning=learning)
            metadata = None  # No special metadata for API responses

        # AUTONOMIE: Theme & Context Detection! 🎯
        stimmung = personality.detect_stimmung(user_text)
        theme = personality.detect_theme(user_text)
        context = personality.detect_context(user_text)

        print(f"   🎭 Stimmung erkannt: {stimmung}")
        print(f"   🎯 Theme erkannt: {theme}")
        print(f"   📍 Context: {context['location']} / {context['activity']}")

        # tageszeit already calculated at start of voice mode for early speak() calls!

        # Save to memory (with Stimmung + Theme!)
        memory.add_to_history("user", user_text, metadata={
            "mode": "voice",
            "stimmung": stimmung,
            "theme": theme,
            "context": context
        })
        memory.add_to_history("assistant", response, metadata={"mode": "voice", "theme": theme})
        memory.save_to_disk()

        # AUTO-BRAIN-SAVE: Wichtige Sachen automatisch speichern! 💾
        is_important = (
            len(user_text) > 50 or  # Lange Messages = wichtig
            "wichtig" in user_text.lower() or
            "merk" in user_text.lower() or
            "!" in user_text or
            theme in ["freunde", "konzert", "coding"]  # Wichtige Themen
        )

        if is_important:
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            kategorie = f"themen/{theme}"

            brain_entry = {
                "user_input": user_text,
                "response": response,
                "stimmung": stimmung,
                "context": context,
                "timestamp": datetime.now().isoformat()
            }

            brain.save(kategorie, brain_entry, f"{theme}_{timestamp}.json")
            print(f"   💾 Auto-saved to brain/{kategorie}/")

        # Output
        print("\n" + "="*60)
        print(f"🤖 {response}")
        print("="*60)

        # Speak with EMOTION SYNTHESIS! 🎭🎤
        # Check if multi-voice command (show all 3 voice profiles!)
        if metadata and metadata.get("multi_voice"):
            print("\n🎤 MULTI-VOICE MODE - Alle 3 Stimmen! 🎭")
            print("="*60)

            # Check if voice profiles exist
            if voice_settings and "custom_profiles" in voice_settings.settings:
                profiles = voice_settings.settings["custom_profiles"]

                for i in range(1, 4):
                    profile_name = f"choice_{i}"
                    if profile_name in profiles:
                        prof = profiles[profile_name]
                        description = prof.get("description", f"Voice {i}")
                        emoji = "🏆" if i == 1 else "🥈" if i == 2 else "🥉"

                        print(f"\n{emoji} Stimme #{i}: {description}")
                        print(f"   Pitch: {prof['pitch']}, Rate: {prof['rate']}")
                        voice.speak(response, stimmung=stimmung, tageszeit=tageszeit, profile=profile_name)
                    else:
                        print(f"\n⚠️  Voice Profile #{i} nicht gefunden - nutze Base Voice")
                        voice.speak(response, stimmung=stimmung, tageszeit=tageszeit)
            else:
                print("⚠️  Keine Voice Profiles gefunden! Nutze normale Stimme.")
                voice.speak(response, stimmung=stimmung, tageszeit=tageszeit)
        else:
            # Normal single-voice output
            voice.speak(response, stimmung=stimmung, tageszeit=tageszeit)

        return 0


if __name__ == "__main__":
    sys.exit(main())
