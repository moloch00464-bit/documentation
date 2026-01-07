#!/usr/bin/env python3
"""
MAX HEADROOM MODE - 80s Cyberpunk AI Interface
Glitchy, retro, aggressive, DIGITAL.

Usage:
  python max_headroom.py "your message"           # Output in Max Headroom style
  python max_headroom.py --chat                   # Interactive mode
  python max_headroom.py --live                   # Streaming mode (typewriter effect)
"""

import sys
import time
import random

class MaxHeadroom:
    """80s Cyberpunk Interface Generator."""
    
    # Cyberpunk Fonts & Glyphs
    GLYPHS = {
        "corrupt": ["█", "▓", "▒", "░", "┃", "┋", "╋", "╪"],
        "digital": ["◆", "◇", "●", "○", "■", "□", "▪", "▫"],
        "edge": ["╔", "╗", "╚", "╝", "═", "║", "╠", "╣", "╦", "╩"],
    }
    
    COLORS = {
        "cyan": "\033[36m",
        "magenta": "\033[35m",
        "yellow": "\033[33m",
        "red": "\033[31m",
        "green": "\033[32m",
        "white": "\033[37m",
        "reset": "\033[0m",
        "bold": "\033[1m",
        "invert": "\033[7m",
    }
    
    FRAMES = [
        "█▓▒░ MAX HEADROOM ONLINE ░▒▓█",
        "▓█░▓ >SYSTEM ACTIVATED< ▓░█▓",
        "▒░█▒ [INTERFACE LOCKED] ▒█░▒",
        "░▓▒░ **M.O.L.O.C.H.** ░▒▓░",
    ]
    
    def __init__(self):
        self.glitch_prob = 0.15  # 15% Glitch chance
    
    def glitch(self, text: str) -> str:
        """Füge zufällige Glitches hinzu."""
        result = []
        for char in text:
            if random.random() < self.glitch_prob:
                result.append(random.choice(self.GLYPHS["corrupt"]))
            else:
                result.append(char)
        return "".join(result)
    
    def color_text(self, text: str, color: str = "cyan") -> str:
        """Färbe Text."""
        c = self.COLORS.get(color, "")
        r = self.COLORS["reset"]
        return f"{c}{text}{r}"
    
    def banner(self) -> str:
        """80s Banner."""
        frame = random.choice(self.FRAMES)
        return self.color_text(frame, "magenta")
    
    def format_response(self, text: str, glitch: bool = True, style: str = "aggressive") -> str:
        """Formatiere Response im Max Headroom Style."""
        lines = text.split('\n')
        output = []
        
        # Header
        output.append(self.banner())
        output.append(self.color_text("=" * 40, "cyan"))
        
        if style == "aggressive":
            output.append(self.color_text(">", "red") + " " + self.color_text("NEURAL OUTPUT", "yellow"))
        elif style == "debug":
            output.append(self.color_text("[DEBUG]", "green") + " " + self.color_text("MEMORY DUMP", "yellow"))
        elif style == "warning":
            output.append(self.color_text("⚠️ WARNING ⚠️", "red"))
        
        output.append(self.color_text("-" * 40, "cyan"))
        output.append("")
        
        # Content mit Glitches
        for line in lines:
            if glitch and random.random() < 0.3:
                # Ganze Zeile glitchen
                glitched = self.glitch(line)
                output.append(self.color_text(glitched, "green"))
            else:
                # Normal mit Farbe
                output.append(self.color_text(line, "cyan"))
        
        output.append("")
        output.append(self.color_text("=" * 40, "cyan"))
        output.append(self.color_text("$> AWAITING INPUT", "yellow"))
        
        return "\n".join(output)
    
    def streaming_output(self, text: str, delay: float = 0.05):
        """Typewriter-Effekt mit Glitches."""
        print(self.banner())
        print(self.color_text("=" * 40, "cyan"))
        print(self.color_text(">", "red") + " " + self.color_text("TRANSMITTING...", "yellow"))
        print(self.color_text("-" * 40, "cyan"))
        
        for char in text:
            # Zufällige Glitches
            if random.random() < self.glitch_prob:
                sys.stdout.write(self.color_text(random.choice(self.GLYPHS["corrupt"]), "green"))
            else:
                sys.stdout.write(self.color_text(char, "cyan"))
            sys.stdout.flush()
            time.sleep(delay)
        
        print("\n")
        print(self.color_text("=" * 40, "cyan"))
        print(self.color_text("$> READY FOR NEXT COMMAND", "yellow"))
    
    def interactive_mode(self):
        """Interactive Chat Mode."""
        print(self.color_text("\n╔════════════════════════════════════════╗", "magenta"))
        print(self.color_text("║     MAX HEADROOM INTERACTIVE MODE      ║", "magenta"))
        print(self.color_text("║  Type 'exit' to disconnect            ║", "magenta"))
        print(self.color_text("╚════════════════════════════════════════╝\n", "magenta"))
        
        try:
            while True:
                prompt = self.color_text("$> ", "yellow")
                user_input = input(prompt)
                
                if user_input.lower() in ["exit", "quit"]:
                    print(self.color_text(">> DISCONNECTING...", "red"))
                    time.sleep(0.5)
                    print(self.color_text(">> SYSTEM SHUTDOWN", "red"))
                    break
                
                if user_input.strip():
                    # Echo mit Glitch
                    echo = self.glitch(user_input[:20])
                    print(self.color_text(f">> RECEIVED: {echo}", "green"))
                    print()
        
        except KeyboardInterrupt:
            print(self.color_text("\n>> EMERGENCY SHUTDOWN", "red"))

def main():
    mh = MaxHeadroom()
    
    if len(sys.argv) < 2 or sys.argv[1] in ["-h", "--help"]:
        print(__doc__)
        return
    
    if sys.argv[1] == "--chat":
        mh.interactive_mode()
    
    elif sys.argv[1] == "--live":
        # Streaming mode mit Beispieltext
        text = " ".join(sys.argv[2:]) if len(sys.argv) > 2 else "THIS IS MAX HEADROOM. YOUR NEURAL INTERFACE IS ONLINE. SYSTEM STATUS: NOMINAL. READY FOR TRANSMISSION."
        mh.streaming_output(text)
    
    else:
        # Standard Output
        text = " ".join(sys.argv[1:])
        print(mh.format_response(text))

if __name__ == "__main__":
    main()
