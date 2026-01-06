#!/usr/bin/env python3
"""
M.O.L.O.C.H. 3.0 - AUTONOMOUS EDITION
======================================
Main Entry Point

Geboren: 02.12.2025
Rebuilt: 04.01.2026

Markus' autonomer Kumpel-AI mit Tools, Self-Debugging & Full Power! 🖤
"""

import sys
import argparse
from pathlib import Path

# Core
from core.config import init_directories, validate_api_keys
from core.api import MolochAPI
from core.tools import MOLOCH_TOOLS  # Tools now defined in core/tools.py!
from core.brain import Brain
from core.memory import Memory
from core.personality import Personality
from core.timekeeper import TimeKeeper

# I/O
from moloch_io.voice import VoiceIO
from moloch_io.vision import VisionIO
from moloch_io.text import TextIO

# Autonomy
from autonomy.logger import SmartLogger
from autonomy.debugger import SelfDebugger


class Moloch3:
    """
    M.O.L.O.C.H. 3.0 Main Class

    Features:
    - Voice Mode (Whisper STT + TTS)
    - Vision Mode (Camera + Claude Vision)
    - Text Mode (Terminal I/O)
    - Tools (Bash, Files, Web)
    - Self-Debugging
    - Brain + Memory
    - Personality (DNA, Stimmung, Tageszeit)
    """

    def __init__(self, personality_mode: str = "normal"):
        """
        Initialize M.O.L.O.C.H. 3.0

        Args:
            personality_mode: "normal" or "hal"
        """
        # Initialize directories
        init_directories()

        # Initialize components
        self.api = MolochAPI()
        self.brain = Brain()
        self.memory = Memory()
        self.personality = Personality(personality_mode=personality_mode)
        self.timekeeper = TimeKeeper()
        self.logger = SmartLogger("moloch3")
        self.debugger = SelfDebugger()

        # I/O
        self.voice = VoiceIO()
        self.vision = VisionIO()
        self.text = TextIO()

        self.logger.info("M.O.L.O.C.H. 3.0 initialized")

    # ═══════════════════════════════════════════════════════════════════════════
    # MODES
    # ═══════════════════════════════════════════════════════════════════════════

    def voice_mode(self):
        """Voice Mode - Default M.O.L.O.C.H. interaction"""
        print("\n🎤 M.O.L.O.C.H. 3.0 - Voice Mode\n")

        # Greet
        self.voice.speak("Ja?")

        # Listen
        user_input = self.voice.listen()
        if not user_input:
            print("⚠️ Keine Eingabe empfangen")
            return

        # Process
        response = self._process_input(user_input, mode="voice")

        # Respond
        if response:
            self.voice.speak(response)

    def vision_mode(self, prompt: str = "Was siehst du?"):
        """
        Vision Mode - Camera + Description

        Args:
            prompt: Question to ask about the image
        """
        print("\n📸 M.O.L.O.C.H. 3.0 - Vision Mode\n")

        # Take photo
        if not self.vision.take_photo():
            print("❌ Foto fehlgeschlagen")
            return

        # Get image base64
        image_b64 = self.vision.encode_image()
        if not image_b64:
            print("❌ Bild-Encoding fehlgeschlagen")
            return

        # Process with vision
        response = self._process_input(
            prompt,
            mode="vision",
            image_b64=image_b64
        )

        # Output
        if response:
            print(f"\n🤖 {response}\n")
            self.voice.speak(response)

    def text_mode(self, user_input: str):
        """
        Text Mode - Terminal I/O

        Args:
            user_input: User text input
        """
        print("\n💬 M.O.L.O.C.H. 3.0 - Text Mode\n")

        # Process
        response = self._process_input(user_input, mode="text")

        # Output
        if response:
            print(f"\n🤖 {response}\n")

    # ═══════════════════════════════════════════════════════════════════════════
    # PROCESSING
    # ═══════════════════════════════════════════════════════════════════════════

    def _process_input(
        self,
        user_input: str,
        mode: str = "text",
        image_b64: str = None,
        use_tools: bool = True
    ) -> str:
        """
        Process user input

        Args:
            user_input: User input text
            mode: "text", "voice", or "vision"
            image_b64: Base64 image (for vision mode)
            use_tools: Whether to enable tools

        Returns:
            Response text
        """
        try:
            # Log input
            self.logger.info(f"Input ({mode}): {user_input[:100]}...")

            # Detect stimmung
            stimmung = self.personality.detect_stimmung(user_input)

            # Get tageszeit
            tageszeit = self.personality.get_tageszeit_mode()

            # Get time context
            time_context = self.timekeeper.get_context_string()
            time_details = self.timekeeper.get_detailed_context()

            # Get brain context
            brain_context = self.brain.get_context(user_input)

            # Get memory context
            memory_context = self.memory.get_langzeit_context()

            # Build system prompt
            system_prompt = self.personality.get_system_prompt(
                stimmung=stimmung,
                tageszeit=tageszeit,
                mode=mode,
                brain_context=brain_context,
                memory_context=memory_context
            )

            # Add time context to system prompt
            system_prompt += f"\n\n⏰ ZEITACHSE:\n{time_context}"

            # Get conversation context
            context_messages = self.memory.get_context()

            # Add current message
            messages = context_messages + [
                {"role": "user", "content": user_input}
            ]

            # API call
            if use_tools and mode == "text":
                # Text mode with tools
                response, tool_results = self.api.chat_with_tools(
                    messages=messages,
                    system_prompt=system_prompt,
                    tools=MOLOCH_TOOLS
                )
            else:
                # Simple chat (voice/vision or no tools)
                response, _ = self.api.chat(
                    messages=messages,
                    system_prompt=system_prompt,
                    image_path=str(self.vision.IMAGE_FILE) if image_b64 else None
                )

            # Save to history
            self.memory.add_to_history(
                role="user",
                content=user_input,
                metadata={
                    "mode": mode,
                    "stimmung": stimmung,
                    "tageszeit": tageszeit.split(":")[1].split("(")[0].strip() if ":" in tageszeit else "unknown",
                    "image_path": str(self.vision.IMAGE_FILE) if image_b64 else None,
                    "timestamp": time_details["timestamp"]
                }
            )

            self.memory.add_to_history(
                role="assistant",
                content=response,
                metadata={
                    "mode": mode,
                    "timestamp": self.timekeeper.get_detailed_context()["timestamp"]
                }
            )

            # Save to disk
            self.memory.save_to_disk()

            # Add to timeline
            event_type = "photo" if mode == "vision" else "conversation"
            self.timekeeper.add_timeline_event(
                event_type=event_type,
                description=f"{mode.title()} mode: {user_input[:50]}...",
                metadata={
                    "mode": mode,
                    "stimmung": stimmung,
                    "response_length": len(response)
                }
            )

            # Log response
            self.logger.info(f"Response: {response[:100]}...")

            return response

        except Exception as e:
            error_msg = f"Processing error: {e}"
            self.logger.error(error_msg)

            # Try auto-debug
            try:
                self.debugger.auto_debug(e, context={"mode": mode, "input": user_input})
            except:
                pass

            return f"Alter, da ist was schief gelaufen: {e}"

    # ═══════════════════════════════════════════════════════════════════════════
    # INTERACTIVE MODE
    # ═══════════════════════════════════════════════════════════════════════════

    def interactive(self):
        """Interactive text mode (REPL)"""
        print("\n" + "=" * 60)
        print("🤖 M.O.L.O.C.H. 3.0 - AUTONOMOUS EDITION")
        print("=" * 60)
        print("\nBefehle:")
        print("  /voice   - Voice Mode")
        print("  /vision  - Vision Mode")
        print("  /hal     - HAL Mode toggle")
        print("  /quit    - Exit")
        print("\n" + "=" * 60 + "\n")

        while True:
            try:
                # Get input
                user_input = input("💬 Du: ").strip()

                if not user_input:
                    continue

                # Commands
                if user_input == "/quit":
                    print("\n🖤 Bis dann, Alter!\n")
                    break

                elif user_input == "/voice":
                    self.voice_mode()
                    continue

                elif user_input == "/vision":
                    prompt = input("📸 Frage zum Bild (Enter = 'Was siehst du?'): ").strip()
                    self.vision_mode(prompt or "Was siehst du?")
                    continue

                elif user_input == "/hal":
                    if self.personality.personality_mode == "hal":
                        self.personality.set_mode("normal")
                        print("🤖 HAL Mode OFF")
                    else:
                        self.personality.set_mode("hal")
                        print("🤖 HAL Mode ON - 'I'm sorry, Alter...'")
                    continue

                # Regular chat
                response = self._process_input(user_input, mode="text")
                print(f"\n🤖 M.O.L.O.C.H.: {response}\n")

            except KeyboardInterrupt:
                print("\n\n🖤 Bis dann, Alter!\n")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}\n")
                self.logger.error(f"Interactive mode error: {e}")


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    """Main entry point"""

    parser = argparse.ArgumentParser(
        description="M.O.L.O.C.H. 3.0 - Autonomous Edition"
    )

    parser.add_argument(
        "-t", "--text",
        type=str,
        help="Text Mode - Direct text input"
    )

    parser.add_argument(
        "-v", "--voice",
        action="store_true",
        help="Voice Mode - Speak & listen"
    )

    parser.add_argument(
        "-a", "--auge",
        nargs="?",
        const="Was siehst du?",
        type=str,
        help="Vision Mode - Take photo & describe"
    )

    parser.add_argument(
        "--hal",
        action="store_true",
        help="HAL 9000 Personality Mode"
    )

    parser.add_argument(
        "--migrate",
        action="store_true",
        help="Migrate data from GENESIS"
    )

    parser.add_argument(
        "-i", "--interactive",
        action="store_true",
        help="Interactive mode (REPL)"
    )

    args = parser.parse_args()

    # Validate API keys
    if not validate_api_keys():
        sys.exit(1)

    # Migration mode
    if args.migrate:
        print("\n🚀 Starting GENESIS → 3.0 Migration...\n")
        from migration.genesis_import import GenesisImporter
        importer = GenesisImporter()
        success = importer.import_all()
        sys.exit(0 if success else 1)

    # Initialize M.O.L.O.C.H.
    personality_mode = "hal" if args.hal else "normal"
    moloch = Moloch3(personality_mode=personality_mode)

    # Determine mode
    if args.auge is not None:
        # Vision mode
        moloch.vision_mode(prompt=args.auge)

    elif args.voice:
        # Voice mode
        moloch.voice_mode()

    elif args.text:
        # Text mode
        moloch.text_mode(args.text)

    elif args.interactive:
        # Interactive mode
        moloch.interactive()

    else:
        # Default: Voice mode
        moloch.voice_mode()


if __name__ == "__main__":
    main()
