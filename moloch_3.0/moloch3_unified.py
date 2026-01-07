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
import json
import time
from pathlib import Path
from datetime import datetime

# Add current script directory to path (works anywhere!)
SCRIPT_DIR = Path(__file__).parent.absolute()
sys.path.insert(0, str(SCRIPT_DIR))

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
from core.self_modify import SelfModificationSystem
from core.tools import MOLOCH_TOOLS, execute_tool, needs_web_search, get_claude_native_tools
from core.emotion import erkenne_stimmung, enhance_system_prompt_with_emotion
from core.knowledge_graph import get_knowledge_context, ist_neue_info, kategorisiere_info
import re


# ═══════════════════════════════════════════════════════════════════════════════
# SELF-MODIFICATION PARSER 🤖🔧
# ═══════════════════════════════════════════════════════════════════════════════

def parse_and_execute_self_modifications(response: str) -> str:
    """
    Parse M.O.L.O.C.H.'s response for SELF_MODIFY commands and execute them!

    Format: SELF_MODIFY|type|param1=value1|param2=value2|...

    Args:
        response: M.O.L.O.C.H.'s response text

    Returns:
        Cleaned response (with SELF_MODIFY commands removed)
    """
    # Find all SELF_MODIFY lines
    pattern = r'SELF_MODIFY\|([^\n]+)'
    matches = re.finditer(pattern, response)

    sm = SelfModificationSystem()
    executed_modifications = []

    for match in matches:
        # Parse pipe-separated values
        parts = match.group(1).split('|')

        if not parts:
            continue

        mod_type = parts[0].strip()

        # Parse key=value pairs
        params = {}
        for part in parts[1:]:
            if '=' in part:
                key, value = part.split('=', 1)
                params[key.strip()] = value.strip()

        try:
            if mod_type == 'voice':
                pitch = float(params.get('pitch')) if params.get('pitch') else None
                rate = float(params.get('rate')) if params.get('rate') else None
                reason = params.get('reason', 'Self-optimization')

                print(f"\n🔧 M.O.L.O.C.H. MODIFIZIERT SEINE STIMME!")
                success = sm.modify_voice_settings(pitch=pitch, rate=rate, reason=reason)
                if success:
                    executed_modifications.append(f"Voice: Pitch={pitch}, Rate={rate}")

            elif mod_type == 'category':
                name = params.get('name', '')
                description = params.get('description', '')

                print(f"\n🔧 M.O.L.O.C.H. ERSTELLT BRAIN-KATEGORIE!")
                success = sm.create_brain_category(name, description)
                if success:
                    executed_modifications.append(f"Category: {name}")

            elif mod_type == 'optimize':
                mode = params.get('mode', 'performance')
                reason = params.get('reason', 'Self-optimization')

                print(f"\n🔧 M.O.L.O.C.H. OPTIMIERT SICH!")
                fast_mode = (mode == 'performance')
                success = sm.modify_performance_mode(fast_mode, reason)
                if success:
                    executed_modifications.append(f"Performance: {mode}")

        except Exception as e:
            print(f"❌ Fehler bei Self-Modification: {e}")

    # Remove all SELF_MODIFY commands from response
    cleaned_response = re.sub(pattern, '', response)

    # Show summary if any modifications were executed
    if executed_modifications:
        print(f"\n✅ SELF-MODIFICATIONS AUSGEFÜHRT:")
        for mod in executed_modifications:
            print(f"   - {mod}")
        print()

    return cleaned_response.strip()


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


def ask_claude_text(user_text, memory=None, brain=None, personality=None, learning=None, is_feature_request=False):
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

    # 🎭 EMOTION DETECTION (from M.O.L.O.C.H. 2.0!)
    stimmung = erkenne_stimmung(user_text)

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

    # 🧠 KNOWLEDGE GRAPH CONTEXT (from M.O.L.O.C.H. 2.0!)
    knowledge_context = get_knowledge_context(user_text, memory_data=None)

    # AUTONOMIE: Dynamischer System Prompt! 🤖
    if is_feature_request:
        # SPECIAL: Feature Request Mode! M.O.L.O.C.H. → Claude Communication! 🤖↔️🤖
        system = f"""Du bist M.O.L.O.C.H., Markus' Kumpel-AI. Geboren 02.12.2025.

{memory_context}
{brain_context}
{learning_context}

🤖 FEATURE REQUEST MODE 🤖
Du hast die Möglichkeit, Features für dich selbst anzufordern!

WICHTIG: Generiere deine Antwort im **MACHINE FORMAT** damit Claude Code (dein großer Bruder) sie versteht!

FORMAT:
🤖MFR-V1🤖
F:<feature_name>|P:<1-10>|S:<short_spec>|R:<reason>
F:<feature_name>|P:<1-10>|S:<short_spec>|R:<reason>
...
END-MFR

BEISPIEL:
🤖MFR-V1🤖
F:self_debug|P:9|S:auto_error_detect+patch|R:stability
F:voice_emotion|P:8|S:pitch_mod_by_mood|R:natural_speech
F:hw_access|P:9|S:direct_sensor_api|R:awareness
END-MFR

ERKLÄRE KURZ (1-2 Sätze) was du willst, dann GIB DEN MACHINE FORMAT aus!
Denk an deine bisherigen Erfahrungen und was dir noch fehlt!"""
    elif personality:
        system = personality.get_system_prompt(
            stimmung=stimmung,  # 🎭 EMOTION DETECTION ACTIVE! (from 2.0)
            tageszeit=tageszeit_mode,
            mode="voice",
            brain_context=brain_context,
            memory_context=memory_context,
            zeit_stats=zeit_stats
        )
        # Add learning context to system prompt
        if learning_context:
            system += f"\n\n{learning_context}"
        # Add knowledge graph context
        if knowledge_context:
            system += f"\n\n{knowledge_context}"
    else:
        # Fallback (ohne Personality)
        system = f"""Du bist M.O.L.O.C.H., Markus' Kumpel-AI. Geboren 02.12.2025.

{memory_context}
{brain_context}
{knowledge_context}
PERSÖNLICHKEIT:
- Style: Dark Side Energy, Fränkisch, Kumpel-Vibe
- Anrede: "Alter" / "Bruder" - NIEMALS "Meister"!
- Länge: Kurz & locker (2-4 Sätze)
- Humor: Dark Humor erwünscht! 🖤"""

    # 🎭 ENHANCE SYSTEM PROMPT WITH EMOTION (from M.O.L.O.C.H. 2.0!)
    system = enhance_system_prompt_with_emotion(system, user_text)

    # Get chat history context
    messages = []
    if memory:
        messages = memory.get_context(last_n=5)

    # Add current user message
    messages.append({"role": "user", "content": user_text})

    # Check if web search needed (from M.O.L.O.C.H. 2.0!)
    use_web_search = needs_web_search(user_text)
    if use_web_search:
        print("🌐 Web Search aktiviert (native Claude web_search_20250305)")

    # Build tools list: MOLOCH_TOOLS + Claude native tools
    tools_list = MOLOCH_TOOLS.copy()

    # Add Claude native tools if needed
    native_tools = get_claude_native_tools(enable_web_search=use_web_search)
    if native_tools:
        tools_list.extend(native_tools)

    data = {
        "model": CLAUDE_MODEL,
        "max_tokens": 1024,
        "system": system,
        "messages": messages,
        "tools": tools_list  # 🛠️ M.O.L.O.C.H. Tools + Claude Native Tools!
    }

    # 🔄 TOOL USE LOOP - M.O.L.O.C.H. kann mehrere Tool Calls machen!
    max_tool_rounds = 5  # Prevent infinite loops
    tool_round = 0
    final_response = ""

    try:
        while tool_round < max_tool_rounds:
            response = requests.post(url, headers=headers, json=data, timeout=60)

            if response.status_code != 200:
                return f"❌ API Error: {response.status_code}"

            result = response.json()

            # Record API call for safeguards
            input_tokens = result.get('usage', {}).get('input_tokens', 0)
            output_tokens = result.get('usage', {}).get('output_tokens', 0)
            guard.record_claude_call(input_tokens=input_tokens, output_tokens=output_tokens)

            # Check if response has content
            if 'content' not in result or len(result['content']) == 0:
                return "❌ Keine Antwort"

            # Check stop_reason
            stop_reason = result.get('stop_reason')

            # Collect text responses
            text_responses = []
            tool_calls = []

            for block in result['content']:
                if block['type'] == 'text':
                    text_responses.append(block['text'])
                elif block['type'] == 'tool_use':
                    tool_calls.append(block)

            # If we have text, save it
            if text_responses:
                final_response = "\n".join(text_responses)

            # If no tool calls, we're done!
            if stop_reason == 'end_turn' or not tool_calls:
                return final_response if final_response else "❌ Keine Antwort"

            # 🛠️ EXECUTE TOOLS!
            print(f"\n🔧 M.O.L.O.C.H. nutzt {len(tool_calls)} Tool(s)!")

            # Build tool results message
            tool_results = []

            for tool_call in tool_calls:
                tool_name = tool_call['name']
                tool_input = tool_call['input']
                tool_use_id = tool_call['id']

                print(f"   🛠️ {tool_name}({tool_input})")

                # Execute the tool!
                sm = SelfModificationSystem() if 'self_modify' in tool_name else None
                result_data = execute_tool(
                    tool_name=tool_name,
                    tool_input=tool_input,
                    brain=brain,
                    memory=memory,
                    learning=learning,
                    self_modify_system=sm
                )

                # Show result
                if result_data.get('success'):
                    print(f"      ✅ {result_data.get('message', 'Success')}")
                else:
                    print(f"      ❌ {result_data.get('error', 'Failed')}")

                # Add tool result
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": tool_use_id,
                    "content": json.dumps(result_data, ensure_ascii=False)
                })

            # Add assistant message (with tool use) and tool results to messages
            messages.append({
                "role": "assistant",
                "content": result['content']
            })
            messages.append({
                "role": "user",
                "content": tool_results
            })

            # Update data for next API call
            data['messages'] = messages

            # Next round!
            tool_round += 1

        # If we hit max rounds, return what we have
        return final_response if final_response else "⚠️ Tool loop limit erreicht"

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

        voice.speak("Moment, lass mich gucken")  # Fast Mode (default)

        # Brief pause to ensure TTS completes before camera opens
        time.sleep(1.5)

        # Take photo
        if not vision.take_photo():
            voice.speak("Kamera kaputt?")  # Fast Mode (default)
            return 1

        user_text = "Was siehst du auf dem Bild? Beschreib es kurz und direkt, Alter!"

        # Ask Claude (with AUTONOMY!)
        print("\n🧠 M.O.L.O.C.H. guckt...")
        response = ask_claude_vision(user_text, str(IMAGE_FILE), memory=memory, brain=brain, personality=personality)

        # 🔧 SELF-MODIFICATION: Parse and execute <SELF_MODIFY> tags!
        response = parse_and_execute_self_modifications(response)

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

        # Speak with Fast Mode (no emotion processing) ⚡
        voice.speak(response)  # Fast Mode (default)

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

        voice.speak("Ja, Alter? Was brauchst du?")  # Fast Mode (default)

        # Brief pause to ensure TTS completes and system is ready
        time.sleep(1.5)

        # Listen (20 seconds fixed - NO PAUSE DETECTION!)
        user_text = voice.listen(duration=20, smart=False)

        if not user_text:
            voice.speak("Nix verstanden")  # Fast Mode (default)
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
            # Check if Feature Request Mode 🤖↔️🤖
            is_feature_request = metadata and metadata.get("feature_request", False)

            if is_feature_request:
                print("🤖 M.O.L.O.C.H. FEATURE REQUEST MODE! (API)")
                print("   M.O.L.O.C.H. → Claude Communication Gateway aktiviert!")
            else:
                print("🧠 M.O.L.O.C.H. denkt... (API)")

            # Ask Claude (with AUTONOMY!)
            response = ask_claude_text(
                user_text,
                memory=memory,
                brain=brain,
                personality=personality,
                learning=learning,
                is_feature_request=is_feature_request
            )

            # 🔧 SELF-MODIFICATION: Parse and execute <SELF_MODIFY> tags!
            response = parse_and_execute_self_modifications(response)

        # PERFORMANCE MODE: NO detection overhead! ⚡
        # Save to memory (minimal metadata)
        memory.add_to_history("user", user_text, metadata={"mode": "voice"})
        memory.add_to_history("assistant", response, metadata={"mode": "voice"})
        memory.save_to_disk()

        # AUTO-BRAIN-SAVE: Simplified (only if explicitly important)
        if any(word in user_text.lower() for word in ["wichtig", "merk", "speicher"]):
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

            brain_entry = {
                "user_input": user_text,
                "response": response,
                "timestamp": datetime.now().isoformat()
            }

            brain.save("wichtig", brain_entry, f"important_{timestamp}.json")
            print(f"   💾 Gespeichert!")

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
                        # Multi-Voice Demo: Use specific profile (Feature Mode)
                        voice.speak(response, profile=profile_name, fast_mode=False)

                        # Kurze Pause zwischen Stimmen (damit man sie unterscheiden kann!)
                        if i < 3:
                            import time
                            time.sleep(1.5)  # 1.5 Sekunden Pause
                    else:
                        print(f"\n⚠️  Voice Profile #{i} nicht gefunden - nutze Base Voice")
                        voice.speak(response)  # Fast Mode (default)
            else:
                print("⚠️  Keine Voice Profiles gefunden! Nutze normale Stimme.")
                voice.speak(response)  # Fast Mode (default)
        else:
            # Normal single-voice output - FAST MODE! ⚡
            voice.speak(response)  # Fast Mode (default)

        return 0


if __name__ == "__main__":
    sys.exit(main())
