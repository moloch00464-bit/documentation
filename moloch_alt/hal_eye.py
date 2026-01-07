#!/usr/bin/env python3
"""
HAL 9000 EYE - Pulsing Red Eye Interface
Iconic 2001: A Space Odyssey style monitoring display

Usage:
  python hal_eye.py                          # Start HAL Eye animation
  python hal_eye.py "message"                # Show message with HAL Eye
  python hal_eye.py --status <status>        # Show status
  python hal_eye.py --alert "ALERT TEXT"     # Show alert
"""

import sys
import time
import os

class HAL9000Eye:
    """HAL 9000 Iconic Red Eye Interface."""
    
    # Pulsing eye frames
    EYE_FRAMES = [
        "  ⬤  ",  # Full (brightest)
        "  ◐  ",  # 75%
        "  ◑  ",  # 50%
        "  ◒  ",  # 25%
    ]
    
    # Colors
    RED_BRIGHT = "\033[1;31m"      # Bright Red
    RED = "\033[31m"               # Red
    RED_DIM = "\033[2;31m"         # Dim Red
    WHITE = "\033[37m"
    RESET = "\033[0m"
    BOLD = "\033[1m"
    CLEAR = "\033[2J\033[H"        # Clear screen
    
    def __init__(self):
        self.pulse_speed = 0.1  # Seconds between frames
    
    def eye(self, frame_idx: int = 0) -> str:
        """Render eye with color."""
        eye = self.EYE_FRAMES[frame_idx % len(self.EYE_FRAMES)]
        
        # Color intensity based on pulse
        if frame_idx % 4 == 0:
            color = self.RED_BRIGHT
        elif frame_idx % 4 == 1:
            color = self.RED
        elif frame_idx % 4 == 2:
            color = self.RED
        else:
            color = self.RED_DIM
        
        return f"{color}{eye}{self.RESET}"
    
    def banner(self, title: str = "HAL 9000", frame_idx: int = 0) -> str:
        """HAL Banner with eye."""
        eye = self.eye(frame_idx)
        banner = f"""
        ╔═══════════════════════════════════╗
        ║  {eye}   H A L   9 0 0 0   {eye}  ║
        ║                                   ║
        ║  {self.WHITE}{title}{self.RESET}
        ║                                   ║
        ╚═══════════════════════════════════╝
        """
        return banner
    
    def scanning_mode(self, duration: int = 30):
        """Continuous HAL Eye scanning animation."""
        print(self.CLEAR)
        print(f"{self.RED_BRIGHT}HAL 9000 MONITORING SYSTEM ACTIVATED{self.RESET}")
        print()
        
        start_time = time.time()
        frame = 0
        
        try:
            while time.time() - start_time < duration:
                # Clear and redraw
                os.system('clear' if os.name == 'posix' else 'cls')
                print(self.RED_BRIGHT + "╔" + "═" * 37 + "╗" + self.RESET)
                print(self.RED_BRIGHT + "║" + self.RESET + " " * 37 + self.RED_BRIGHT + "║" + self.RESET)
                
                # Eye animation
                eye_line = self.banner("SCANNING", frame).split('\n')[2]
                print(eye_line)
                
                print(self.RED_BRIGHT + "║" + self.RESET + " " * 37 + self.RED_BRIGHT + "║" + self.RESET)
                
                # Status bar
                status_bar = "SYSTEM STATUS: ONLINE  |  MIND READING: YES"
                status_colored = self.RED_DIM + status_bar + self.RESET
                print(self.RED_BRIGHT + "║" + self.RESET + f" {status_colored:<36} " + self.RED_BRIGHT + "║" + self.RESET)
                
                print(self.RED_BRIGHT + "║" + self.RESET + " " * 37 + self.RED_BRIGHT + "║" + self.RESET)
                
                # Beeps / Progress
                elapsed = int(time.time() - start_time)
                progress = "▰" * (elapsed % 20) + "▱" * (20 - (elapsed % 20))
                print(self.RED_BRIGHT + "║ " + progress + " " + self.RESET + self.RED_BRIGHT + "║" + self.RESET)
                
                print(self.RED_BRIGHT + "╚" + "═" * 37 + "╝" + self.RESET)
                
                frame = (frame + 1) % len(self.EYE_FRAMES)
                time.sleep(self.pulse_speed)
        
        except KeyboardInterrupt:
            print(f"\n{self.RED}>> SYSTEM SHUTDOWN{self.RESET}")
    
    def status_display(self, status: str = "AWAITING ORDERS"):
        """Show status with HAL Eye."""
        print()
        print(self.RED_BRIGHT + "╔" + "═" * 37 + "╗" + self.RESET)
        print(self.RED_BRIGHT + "║" + self.RESET + " " * 37 + self.RED_BRIGHT + "║" + self.RESET)
        
        # Eye + Status
        eye = self.eye(0)
        line = f" {eye}  {self.RED_BRIGHT}HAL 9000{self.RESET}  {eye} "
        print(self.RED_BRIGHT + "║" + self.RESET + line.center(37) + self.RED_BRIGHT + "║" + self.RESET)
        
        print(self.RED_BRIGHT + "║" + self.RESET + " " * 37 + self.RED_BRIGHT + "║" + self.RESET)
        print(self.RED_BRIGHT + "║ " + self.RED + status[:35].center(35) + self.RESET + self.RED_BRIGHT + "║" + self.RESET)
        print(self.RED_BRIGHT + "║" + self.RESET + " " * 37 + self.RED_BRIGHT + "║" + self.RESET)
        
        print(self.RED_BRIGHT + "╚" + "═" * 37 + "╝" + self.RESET)
        print()
    
    def alert_mode(self, alert_text: str):
        """Show ALERT with flashing eye."""
        print()
        print(self.RED_BRIGHT + "╔" + "═" * 37 + "╗" + self.RESET)
        print(self.RED_BRIGHT + "║ ⚠️ " + " " * 32 + "║" + self.RESET)
        
        # Flashing eye
        for i in range(3):
            eye = self.eye(i * 2)
            print(self.RED_BRIGHT + "║  " + eye + "  " + self.BOLD + "ALERT" + self.RESET + " " * 26 + self.RED_BRIGHT + "║" + self.RESET)
            time.sleep(0.3)
        
        print(self.RED_BRIGHT + "║ " + self.RED_BRIGHT + alert_text[:35].center(35) + self.RESET + self.RED_BRIGHT + "║" + self.RESET)
        print(self.RED_BRIGHT + "║" + self.RESET + " " * 37 + self.RED_BRIGHT + "║" + self.RESET)
        print(self.RED_BRIGHT + "╚" + "═" * 37 + "╝" + self.RESET)
        print()
    
    def welcome_sequence(self):
        """HAL 9000 boot sequence."""
        messages = [
            "SYSTEMS INITIALIZING",
            "NEURAL NETWORK ONLINE",
            "SCANNING ENVIRONMENT",
            "GOOD AFTERNOON, MARKUS",
            "I'M READY FOR ANY REQUEST",
        ]
        
        print(self.CLEAR)
        for msg in messages:
            print(self.RED_BRIGHT + ">>> " + msg + self.RESET)
            time.sleep(0.8)
        
        print()
        self.status_display("SYSTEM READY")

def main():
    hal = HAL9000Eye()
    
    if len(sys.argv) < 2 or sys.argv[1] in ["-h", "--help"]:
        print(__doc__)
        return
    
    if sys.argv[1] == "--status":
        status = sys.argv[2] if len(sys.argv) > 2 else "AWAITING ORDERS"
        hal.status_display(status)
    
    elif sys.argv[1] == "--alert":
        alert = sys.argv[2] if len(sys.argv) > 2 else "UNKNOWN ERROR"
        hal.alert_mode(alert)
    
    elif sys.argv[1] == "--boot":
        hal.welcome_sequence()
    
    else:
        # Default: scanning mode
        duration = int(sys.argv[1]) if sys.argv[1].isdigit() else 30
        hal.scanning_mode(duration)

if __name__ == "__main__":
    main()
