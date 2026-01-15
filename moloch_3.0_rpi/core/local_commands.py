#!/usr/bin/env python3
"""M.O.L.O.C.H. 3.1 - Local Command Handler"""

from datetime import datetime
import subprocess
from typing import Tuple, Optional, Dict


class LocalCommandHandler:
    """Handle simple commands locally without API calls"""

    def __init__(self, data_dir):
        self.data_dir = data_dir

    def handle(self, user_text: str) -> Tuple[bool, Optional[str], Optional[Dict]]:
        """
        Handle command locally if possible

        Returns:
            (handled, response, metadata)
        """
        lower = user_text.lower()

        # Time/Date queries
        if any(w in lower for w in ["uhrzeit", "wie spät", "wieviel uhr"]):
            now = datetime.now()
            time_str = now.strftime("%H:%M")
            return True, f"Es ist {time_str} Uhr, Alter.", None

        if any(w in lower for w in ["datum", "welcher tag", "welches datum"]):
            now = datetime.now()
            date_str = now.strftime("%d.%m.%Y")
            weekday = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"][now.weekday()]
            return True, f"Heute ist {weekday}, der {date_str}.", None

        # Battery status
        if "batterie" in lower or "akku" in lower:
            try:
                result = subprocess.run(
                    ["termux-battery-status"],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                if result.returncode == 0:
                    import json
                    battery = json.loads(result.stdout)
                    percentage = battery.get("percentage", "?")
                    status = battery.get("status", "?")
                    return True, f"Akku: {percentage}% ({status})", None
            except:
                pass

        # Simple math
        if "+" in user_text or "-" in user_text or "*" in user_text:
            try:
                # Very basic eval (careful!)
                if all(c in "0123456789+-*/ ()" for c in user_text.replace(" ", "")):
                    result = eval(user_text)
                    return True, f"Das ist {result}, Alter.", None
            except:
                pass

        # Feature request detection
        if any(phrase in lower for phrase in ["feature request", "ich will dass du", "du sollst können"]):
            return False, None, {"feature_request": True}

        # Not handled locally
        return False, None, None
