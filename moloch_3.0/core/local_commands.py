#!/usr/bin/env python3
"""
M.O.L.O.C.H. 3.0 - Local Command Handler
=========================================
Handle simple commands WITHOUT API calls - save costs! 💰

Commands handled locally:
- Zeit/Datum
- Wetter
- Batterie
- Termine speichern
- Geburtstage speichern
- Einfache Rechnungen
"""

import subprocess
import json
from datetime import datetime
from pathlib import Path
from typing import Optional, Tuple, Dict


class LocalCommandHandler:
    """
    Handle simple commands locally (NO API!)

    Returns:
        (handled: bool, response: str)
        - If handled=True: response contains answer (no API needed!)
        - If handled=False: pass to Claude API
    """

    def __init__(self, data_dir: Path):
        """Initialize handler"""
        self.data_dir = data_dir
        self.appointments_file = data_dir / "appointments.json"
        self.birthdays_file = data_dir / "birthdays.json"

    def handle(self, text: str) -> Tuple[bool, Optional[str], Optional[Dict]]:
        """
        Try to handle command locally

        Args:
            text: User input

        Returns:
            (handled, response, metadata)
            - handled=True: Command was handled locally
            - response: Answer (if handled) or None
            - metadata: Optional dict with special instructions (e.g., {"multi_voice": True})
        """
        text_lower = text.lower()

        # VOICE COMMANDS - Alle Stimmen durchgehen! 🎤
        if any(phrase in text_lower for phrase in [
            "alle stimmen",
            "drei stimmen",
            "alle stimmlagen",
            "zeig mir deine stimmen",
            "stimmen durch",
            "verschiedene stimmen"
        ]):
            return True, "Okay, ich zeig dir meine drei Stimmen! Hör genau hin, Alter! Das ist meine Voice-Identität!", {"multi_voice": True}

        # Zeit/Datum
        if any(word in text_lower for word in ["uhrzeit", "wie spät", "welche zeit"]):
            return True, self._get_time(), None

        if any(word in text_lower for word in ["datum", "welcher tag", "welches datum"]):
            return True, self._get_date(), None

        # Wetter
        if "wetter" in text_lower:
            response = self._get_weather()
            if response:
                return True, response, None

        # Batterie
        if "batterie" in text_lower or "akku" in text_lower:
            response = self._get_battery()
            if response:
                return True, response, None

        # Termin speichern
        if "termin" in text_lower and any(word in text_lower for word in ["speicher", "merk", "notier"]):
            return True, self._save_appointment(text), None

        # Geburtstag speichern
        if "geburtstag" in text_lower and any(word in text_lower for word in ["speicher", "merk", "notier"]):
            return True, self._save_birthday(text), None

        # Rechnung (einfach)
        if any(op in text for op in ["+", "-", "*", "/", "mal", "plus", "minus", "geteilt"]):
            result = self._calculate(text)
            if result:
                return True, result, None

        # Nicht erkannt → API!
        return False, None, None

    # ═══════════════════════════════════════════════════════════════════════════
    # ZEIT & DATUM
    # ═══════════════════════════════════════════════════════════════════════════

    def _get_time(self) -> str:
        """Get current time"""
        now = datetime.now()
        return f"🕐 Es ist {now.strftime('%H:%M')} Uhr, Alter!"

    def _get_date(self) -> str:
        """Get current date"""
        now = datetime.now()
        wochentage = {
            'Monday': 'Montag', 'Tuesday': 'Dienstag', 'Wednesday': 'Mittwoch',
            'Thursday': 'Donnerstag', 'Friday': 'Freitag',
            'Saturday': 'Samstag', 'Sunday': 'Sonntag'
        }
        wochentag_de = wochentage.get(now.strftime('%A'), now.strftime('%A'))
        return f"📅 Heute ist {wochentag_de}, der {now.strftime('%d.%m.%Y')}!"

    # ═══════════════════════════════════════════════════════════════════════════
    # PHONE DATA (Termux API)
    # ═══════════════════════════════════════════════════════════════════════════

    def _get_weather(self) -> Optional[str]:
        """Get weather via Termux API"""
        try:
            # Get location first
            result = subprocess.run(
                ["termux-location"],
                capture_output=True,
                timeout=10,
                text=True
            )

            if result.returncode == 0 and result.stdout:
                location_data = json.loads(result.stdout)
                lat = location_data.get("latitude")
                lon = location_data.get("longitude")

                # For now, just return location
                # TODO: Add weather API call (free service like wttr.in)
                return f"📍 Standort: {lat:.2f}, {lon:.2f}\n⚠️ Wetter-API noch nicht implementiert, Bruder!"

            return None

        except Exception as e:
            return None

    def _get_battery(self) -> Optional[str]:
        """Get battery status via Termux API"""
        try:
            result = subprocess.run(
                ["termux-battery-status"],
                capture_output=True,
                timeout=5,
                text=True
            )

            if result.returncode == 0 and result.stdout:
                battery = json.loads(result.stdout)
                percentage = battery.get("percentage", 0)
                status = battery.get("status", "Unknown")

                emoji = "🔋" if status == "CHARGING" else "🔌"
                return f"{emoji} Akku: {percentage}% ({status})"

            return None

        except Exception as e:
            return None

    # ═══════════════════════════════════════════════════════════════════════════
    # APPOINTMENTS & BIRTHDAYS
    # ═══════════════════════════════════════════════════════════════════════════

    def _save_appointment(self, text: str) -> str:
        """Save appointment to local file"""
        # Simple implementation - just append to file
        try:
            # Ensure file exists
            if not self.appointments_file.exists():
                self.appointments_file.write_text("[]")

            # Load existing
            appointments = json.loads(self.appointments_file.read_text())

            # Add new (simplified - just save the text)
            appointments.append({
                "text": text,
                "timestamp": datetime.now().isoformat()
            })

            # Save
            self.appointments_file.write_text(json.dumps(appointments, indent=2, ensure_ascii=False))

            return f"✅ Termin gespeichert, Alter! Hab's notiert!"

        except Exception as e:
            return f"❌ Konnte Termin nicht speichern: {e}"

    def _save_birthday(self, text: str) -> str:
        """Save birthday to local file"""
        try:
            # Ensure file exists
            if not self.birthdays_file.exists():
                self.birthdays_file.write_text("[]")

            # Load existing
            birthdays = json.loads(self.birthdays_file.read_text())

            # Add new
            birthdays.append({
                "text": text,
                "timestamp": datetime.now().isoformat()
            })

            # Save
            self.birthdays_file.write_text(json.dumps(birthdays, indent=2, ensure_ascii=False))

            return f"🎂 Geburtstag gespeichert, Bruder! Vergess ich nicht!"

        except Exception as e:
            return f"❌ Konnte Geburtstag nicht speichern: {e}"

    # ═══════════════════════════════════════════════════════════════════════════
    # CALCULATIONS
    # ═══════════════════════════════════════════════════════════════════════════

    def _calculate(self, text: str) -> Optional[str]:
        """Simple calculations"""
        try:
            # Very basic - look for numbers and operators
            # Safety: only allow basic math
            allowed_chars = "0123456789+-*/(). "
            expr = "".join(c for c in text if c in allowed_chars).strip()

            if not expr:
                return None

            # Eval (SAFE because we filtered input!)
            result = eval(expr)
            return f"🔢 Ergebnis: {result}"

        except:
            return None


# ═══════════════════════════════════════════════════════════════════════════════
# TESTING
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    from core.config import DATA_DIR

    handler = LocalCommandHandler(DATA_DIR)

    test_commands = [
        "wie spät ist es?",
        "welches datum haben wir?",
        "wie ist das wetter?",
        "wie viel akku habe ich noch?",
        "speicher termin: Meeting um 15 Uhr",
        "geburtstag von Rebecca am 12.05",
        "was ist 42 * 1337?",
        "erzähl mir was über Rebecca",  # Should NOT be handled
    ]

    print("\n🧪 Testing Local Command Handler\n")

    for cmd in test_commands:
        print(f"📝 Input: {cmd}")
        handled, response = handler.handle(cmd)

        if handled:
            print(f"✅ HANDLED LOCALLY: {response}")
        else:
            print(f"➡️ PASS TO API")

        print()
