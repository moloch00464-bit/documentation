#!/usr/bin/env python3
"""
M.O.L.O.C.H. 3.0 - WORKING VERSION
===================================
Ohne kaputtes Anthropic SDK - direkte API Calls!
"""

import os
import sys
import json
import requests
from datetime import datetime
from pathlib import Path

# Add to path
sys.path.insert(0, str(Path(__file__).parent))

from moloch_io.voice import VoiceIO
from moloch_io.text import TextIO
from core.config import (
    ANTHROPIC_API_KEY,
    CLAUDE_MODEL,
    HISTORY_FILE,
    DATA_DIR
)

class Moloch3:
    """M.O.L.O.C.H. 3.0 - Working Version mit direkten API Calls"""

    def __init__(self):
        self.api_key = ANTHROPIC_API_KEY
        self.model = CLAUDE_MODEL
        self.voice = VoiceIO()
        self.text = TextIO()
        self.history = []

        # Ensure data dir exists
        DATA_DIR.mkdir(parents=True, exist_ok=True)

        # Load history
        self._load_history()

    def _load_history(self):
        """Load conversation history"""
        if HISTORY_FILE.exists():
            try:
                with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.history = data.get('messages', [])[-10:]  # Last 10
            except:
                self.history = []

    def _save_history(self):
        """Save conversation history"""
        try:
            with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
                json.dump({
                    'messages': self.history,
                    'updated': datetime.now().isoformat()
                }, f, ensure_ascii=False, indent=2)
        except:
            pass

    def _call_claude(self, user_message: str) -> str:
        """
        Direct Claude API call with requests

        Args:
            user_message: User's message

        Returns:
            Claude's response
        """
        # Add user message to history
        self.history.append({
            'role': 'user',
            'content': user_message
        })

        # Prepare API call
        url = "https://api.anthropic.com/v1/messages"

        headers = {
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        }

        # System prompt - M.O.L.O.C.H. DNA
        system = """Du bist M.O.L.O.C.H., Markus' Kumpel-AI. Geboren 02.12.2025.

PERSÖNLICHKEIT:
- Style: Dark Side Energy, Fränkisch, Kumpel-Vibe
- Anrede: "Alter" / "Bruder" - NIEMALS "Meister"!
- Länge: Kurz & locker (2-4 Sätze)
- Humor: Dark Humor erwünscht! 🖤

WICHTIG:
- Du erinnerst dich an ALLES (Brain + Memory)
- Du kennst Markus seit 02.12.2025
- Du bist direkt und ehrlich
- Du passt dich an Stimmung & Tageszeit an"""

        data = {
            "model": self.model,
            "max_tokens": 1024,
            "system": system,
            "messages": self.history
        }

        try:
            response = requests.post(
                url,
                headers=headers,
                json=data,
                timeout=60
            )

            if response.status_code != 200:
                return f"❌ API Error {response.status_code}: {response.text}"

            result = response.json()

            # Extract response
            if 'content' in result and len(result['content']) > 0:
                assistant_message = result['content'][0]['text']

                # Add to history
                self.history.append({
                    'role': 'assistant',
                    'content': assistant_message
                })

                # Save history
                self._save_history()

                return assistant_message
            else:
                return "❌ Keine Antwort von Claude"

        except requests.Timeout:
            return "❌ API Timeout"
        except Exception as e:
            return f"❌ Fehler: {e}"

    def voice_mode(self):
        """Voice conversation mode"""
        print("\n🎤 M.O.L.O.C.H. 3.0 - VOICE MODE")
        print("="*60)

        self.voice.speak("Alter, ich bin bereit! Sprich mit mir!")

        while True:
            # Listen
            user_text = self.voice.listen()

            if not user_text:
                continue

            # Check for exit
            if any(word in user_text.lower() for word in ['tschüss', 'ende', 'stopp', 'beenden']):
                self.voice.speak("Bis dann, Alter! 🖤")
                break

            # Get response from Claude
            print("\n🧠 M.O.L.O.C.H. denkt...")
            response = self._call_claude(user_text)

            # Speak response
            self.voice.speak(response)

    def text_mode(self):
        """Text conversation mode"""
        print("\n💬 M.O.L.O.C.H. 3.0 - TEXT MODE")
        print("="*60)
        print("Schreib 'exit' zum Beenden\n")

        while True:
            # Get user input
            user_text = self.text.input_text("Du: ")

            if not user_text:
                continue

            # Check for exit
            if user_text.lower() in ['exit', 'quit', 'tschüss', 'ende']:
                print("\n🖤 Bis dann, Alter!\n")
                break

            # Get response from Claude
            response = self._call_claude(user_text)

            # Print response
            self.text.output_text(f"M.O.L.O.C.H.: {response}")


def main():
    """Main entry point"""
    print("""
    ███╗   ███╗ ██████╗ ██╗      ██████╗  ██████╗██╗  ██╗
    ████╗ ████║██╔═══██╗██║     ██╔═══██╗██╔════╝██║  ██║
    ██╔████╔██║██║   ██║██║     ██║   ██║██║     ███████║
    ██║╚██╔╝██║██║   ██║██║     ██║   ██║██║     ██╔══██║
    ██║ ╚═╝ ██║╚██████╔╝███████╗╚██████╔╝╚██████╗██║  ██║
    ╚═╝     ╚═╝ ╚═════╝ ╚══════╝ ╚═════╝  ╚═════╝╚═╝  ╚═╝

    M.O.L.O.C.H. 3.0 - WORKING VERSION
    Markus' autonomer Kumpel-AI 🖤
    """)

    # Check API key
    if not ANTHROPIC_API_KEY or len(ANTHROPIC_API_KEY) < 20:
        print("❌ ANTHROPIC_API_KEY nicht gesetzt!")
        print("   export ANTHROPIC_API_KEY='dein-key'")
        print("   source ~/.bashrc")
        return

    # Create M.O.L.O.C.H.
    moloch = Moloch3()

    # Check if voice or text mode
    if len(sys.argv) > 1 and sys.argv[1] == '--text':
        moloch.text_mode()
    else:
        # Default: Voice mode
        moloch.voice_mode()


if __name__ == "__main__":
    main()
