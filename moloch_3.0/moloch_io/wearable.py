#!/usr/bin/env python3
"""
M.O.L.O.C.H. 3.0 - Wearable I/O
================================
Xiaomi Smart Band 8 Pro Integration
"""

import subprocess
import json
import sqlite3
from pathlib import Path
from typing import Optional, Dict
from datetime import datetime, timedelta


class WearableIO:
    """
    Wearable Integration for M.O.L.O.C.H. 3.0

    Supports:
    - Xiaomi Smart Band 8 Pro (via Gadgetbridge)
    - Notifications to wearable
    - Health data reading (Heart rate, Steps, Sleep, etc.)
    - Context awareness
    """

    def __init__(self, gadgetbridge_db: str = None):
        """
        Initialize Wearable I/O

        Args:
            gadgetbridge_db: Path to Gadgetbridge database
                Default: /data/data/nodomain.freeyourgadget.gadgetbridge/databases/Gadgetbridge
        """
        if gadgetbridge_db is None:
            # Default Gadgetbridge database path
            self.gadgetbridge_db = "/data/data/nodomain.freeyourgadget.gadgetbridge/databases/Gadgetbridge"
        else:
            self.gadgetbridge_db = gadgetbridge_db

    # ═══════════════════════════════════════════════════════════════════════════
    # NOTIFICATIONS TO WEARABLE
    # ═══════════════════════════════════════════════════════════════════════════

    def send_notification(
        self,
        title: str,
        message: str,
        vibrate: bool = True,
        id: str = "moloch"
    ) -> bool:
        """
        Send notification to wearable

        Args:
            title: Notification title
            message: Notification message
            vibrate: Vibrate on wearable
            id: Notification ID

        Returns:
            Success status

        Example:
            wearable.send_notification("M.O.L.O.C.H.", "Processing complete! ✅")
        """
        try:
            cmd = [
                "termux-notification",
                "--title", title,
                "--content", message,
                "--id", id
            ]

            if vibrate:
                # Vibrate pattern: buzz-pause-buzz
                cmd.extend(["--vibrate", "200,100,200"])

            subprocess.run(cmd, capture_output=True, timeout=5)
            return True

        except FileNotFoundError:
            print("⚠️ termux-notification not available")
            return False
        except Exception as e:
            print(f"⚠️ Notification error: {e}")
            return False

    def send_alert(self, message: str) -> bool:
        """
        Send urgent alert to wearable (stronger vibration)

        Args:
            message: Alert message

        Returns:
            Success status
        """
        return self.send_notification(
            title="⚠️ M.O.L.O.C.H. ALERT",
            message=message,
            vibrate=True,
            id="moloch_alert"
        )

    # ═══════════════════════════════════════════════════════════════════════════
    # HEALTH DATA READING (via Gadgetbridge)
    # ═══════════════════════════════════════════════════════════════════════════

    def _query_gadgetbridge(self, query: str) -> Optional[list]:
        """
        Query Gadgetbridge database

        Args:
            query: SQL query

        Returns:
            Query results or None

        Note:
            Requires root or Gadgetbridge database access permission
        """
        try:
            conn = sqlite3.connect(self.gadgetbridge_db)
            cursor = conn.cursor()
            cursor.execute(query)
            results = cursor.fetchall()
            conn.close()
            return results

        except sqlite3.OperationalError as e:
            print(f"⚠️ Gadgetbridge database error: {e}")
            print("   Make sure Gadgetbridge is installed and has permission")
            return None
        except Exception as e:
            print(f"⚠️ Database query error: {e}")
            return None

    def get_heart_rate(self, minutes_ago: int = 5) -> Optional[int]:
        """
        Get recent heart rate

        Args:
            minutes_ago: How many minutes back to check

        Returns:
            Heart rate (BPM) or None

        Example:
            hr = wearable.get_heart_rate()
            print(f"Heart rate: {hr} BPM")
        """
        try:
            # Query heart rate from last N minutes
            timestamp = int((datetime.now() - timedelta(minutes=minutes_ago)).timestamp() * 1000)

            query = f"""
                SELECT heartRate
                FROM MI_BAND_ACTIVITY_SAMPLE
                WHERE TIMESTAMP > {timestamp}
                AND heartRate > 0
                ORDER BY TIMESTAMP DESC
                LIMIT 1
            """

            results = self._query_gadgetbridge(query)
            if results and len(results) > 0:
                return results[0][0]

            return None

        except Exception as e:
            print(f"⚠️ Heart rate error: {e}")
            return None

    def get_steps_today(self) -> Optional[int]:
        """
        Get steps count for today

        Returns:
            Steps count or None
        """
        try:
            # Get today's timestamp (midnight)
            today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
            timestamp = int(today.timestamp() * 1000)

            query = f"""
                SELECT SUM(steps)
                FROM MI_BAND_ACTIVITY_SAMPLE
                WHERE TIMESTAMP > {timestamp}
            """

            results = self._query_gadgetbridge(query)
            if results and len(results) > 0 and results[0][0]:
                return results[0][0]

            return None

        except Exception as e:
            print(f"⚠️ Steps error: {e}")
            return None

    def get_sleep_last_night(self) -> Optional[Dict]:
        """
        Get sleep data from last night

        Returns:
            Sleep data dict or None
            {
                "total_minutes": 450,
                "deep_sleep_minutes": 120,
                "light_sleep_minutes": 330
            }
        """
        try:
            # Get yesterday's sleep (usually 20:00 to 08:00)
            yesterday = datetime.now() - timedelta(days=1)
            sleep_start = yesterday.replace(hour=20, minute=0, second=0)
            sleep_end = datetime.now().replace(hour=8, minute=0, second=0)

            start_ts = int(sleep_start.timestamp() * 1000)
            end_ts = int(sleep_end.timestamp() * 1000)

            query = f"""
                SELECT activityKind, COUNT(*)
                FROM MI_BAND_ACTIVITY_SAMPLE
                WHERE TIMESTAMP BETWEEN {start_ts} AND {end_ts}
                AND activityKind IN (4, 5)
                GROUP BY activityKind
            """

            results = self._query_gadgetbridge(query)
            if not results:
                return None

            # Parse results (activityKind: 4=light sleep, 5=deep sleep)
            sleep_data = {"total_minutes": 0, "deep_sleep_minutes": 0, "light_sleep_minutes": 0}

            for kind, count in results:
                if kind == 4:  # Light sleep
                    sleep_data["light_sleep_minutes"] = count
                elif kind == 5:  # Deep sleep
                    sleep_data["deep_sleep_minutes"] = count

            sleep_data["total_minutes"] = sleep_data["light_sleep_minutes"] + sleep_data["deep_sleep_minutes"]

            return sleep_data if sleep_data["total_minutes"] > 0 else None

        except Exception as e:
            print(f"⚠️ Sleep data error: {e}")
            return None

    # ═══════════════════════════════════════════════════════════════════════════
    # CONTEXT AWARENESS
    # ═══════════════════════════════════════════════════════════════════════════

    def get_user_context(self) -> Dict:
        """
        Get user context from wearable data

        Returns:
            Context dict with health metrics

        Example:
            context = wearable.get_user_context()
            # {
            #     "heart_rate": 72,
            #     "steps": 12543,
            #     "is_active": True,
            #     "is_stressed": False
            # }
        """
        context = {
            "heart_rate": self.get_heart_rate(),
            "steps": self.get_steps_today(),
            "is_active": False,
            "is_stressed": False,
            "is_sleeping": False
        }

        # Determine activity status
        if context["heart_rate"]:
            if context["heart_rate"] > 100:
                context["is_active"] = True
            if context["heart_rate"] > 90 and context["is_active"]:
                context["is_stressed"] = True

        # Determine sleep status (simple heuristic)
        hour = datetime.now().hour
        if 22 <= hour or hour < 7:
            if context["heart_rate"] and context["heart_rate"] < 65:
                context["is_sleeping"] = True

        return context

    def format_context_for_prompt(self, context: Dict) -> str:
        """
        Format context for M.O.L.O.C.H. system prompt

        Args:
            context: Context dict from get_user_context()

        Returns:
            Formatted string for system prompt
        """
        lines = ["WEARABLE CONTEXT:"]

        if context.get("heart_rate"):
            lines.append(f"- Heart Rate: {context['heart_rate']} BPM")

        if context.get("steps"):
            lines.append(f"- Steps Today: {context['steps']:,}")

        if context.get("is_active"):
            lines.append("- Status: ACTIVE (high heart rate)")

        if context.get("is_stressed"):
            lines.append("- Status: POSSIBLY STRESSED (high heart rate)")

        if context.get("is_sleeping"):
            lines.append("- Status: SLEEPING (low heart rate, late hour)")

        return "\n".join(lines)


# ═══════════════════════════════════════════════════════════════════════════════
# TESTING
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("\n⌚ M.O.L.O.C.H. 3.0 Wearable I/O Test\n")

    wearable = WearableIO()

    # Test notification
    print("📱 Testing notification to wearable...")
    wearable.send_notification("M.O.L.O.C.H. 3.0", "Test notification! ⌚")

    # Test health data (requires Gadgetbridge)
    print("\n💓 Testing health data...")
    hr = wearable.get_heart_rate()
    if hr:
        print(f"   Heart Rate: {hr} BPM")
    else:
        print("   ⚠️ No heart rate data (install Gadgetbridge)")

    steps = wearable.get_steps_today()
    if steps:
        print(f"   Steps: {steps:,}")
    else:
        print("   ⚠️ No steps data")

    # Test context
    print("\n🧠 Testing context...")
    context = wearable.get_user_context()
    print(wearable.format_context_for_prompt(context))

    print()
