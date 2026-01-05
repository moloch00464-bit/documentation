#!/usr/bin/env python3
"""
M.O.L.O.C.H. 3.0 - Feedback I/O
================================
User Feedback: Toast, Vibrate, Wake Lock, Brightness
"""

import subprocess
from datetime import datetime
from typing import Optional


class FeedbackIO:
    """
    Feedback I/O for M.O.L.O.C.H. 3.0

    Features:
    - Toast notifications (silent feedback)
    - Vibration (haptic feedback)
    - Wake lock (prevent sleep)
    - Brightness control (auto-dim at night)
    """

    def __init__(self):
        """Initialize Feedback I/O"""
        self.wake_lock_active = False

    # ═══════════════════════════════════════════════════════════════════════════
    # TOAST NOTIFICATIONS
    # ═══════════════════════════════════════════════════════════════════════════

    def toast(
        self,
        message: str,
        duration: str = "short",
        position: str = "bottom",
        background_color: Optional[str] = None,
        text_color: Optional[str] = None
    ) -> bool:
        """
        Show toast notification

        Args:
            message: Message to show
            duration: "short" or "long"
            position: "top", "middle", "bottom"
            background_color: Hex color (e.g., "#FF0000")
            text_color: Hex color (e.g., "#FFFFFF")

        Returns:
            Success status

        Examples:
            toast("Processing...")
            toast("Error!", background_color="#FF0000", text_color="#FFFFFF")
        """
        try:
            cmd = ["termux-toast"]

            # Duration
            if duration == "short":
                cmd.append("-s")

            # Position
            if position in ["top", "middle", "bottom"]:
                cmd.extend(["-g", position])

            # Colors
            if background_color:
                cmd.extend(["-b", background_color])
            if text_color:
                cmd.extend(["-c", text_color])

            # Message
            cmd.append(message)

            subprocess.run(cmd, capture_output=True, timeout=5)
            return True

        except FileNotFoundError:
            print(f"⚠️ termux-toast not available (message: {message})")
            return False
        except Exception as e:
            print(f"⚠️ Toast error: {e}")
            return False

    # ═══════════════════════════════════════════════════════════════════════════
    # VIBRATION
    # ═══════════════════════════════════════════════════════════════════════════

    def vibrate(self, duration_ms: int = 500, force: bool = False) -> bool:
        """
        Vibrate device

        Args:
            duration_ms: Duration in milliseconds
            force: Force vibration even in silent mode

        Returns:
            Success status

        Examples:
            vibrate(200)  # Quick buzz
            vibrate(1000)  # Long vibration
            vibrate(500, force=True)  # Force even in silent mode
        """
        try:
            cmd = ["termux-vibrate", "-d", str(duration_ms)]

            if force:
                cmd.append("-f")

            subprocess.run(cmd, capture_output=True, timeout=5)
            return True

        except FileNotFoundError:
            print("⚠️ termux-vibrate not available")
            return False
        except Exception as e:
            print(f"⚠️ Vibrate error: {e}")
            return False

    def vibrate_pattern(self, pattern: str) -> bool:
        """
        Vibrate with pattern

        Args:
            pattern: "short", "double", "triple", "sos"

        Examples:
            vibrate_pattern("short")  # Quick buzz
            vibrate_pattern("double")  # Buzz buzz
            vibrate_pattern("sos")  # ... --- ...
        """
        patterns = {
            "short": [(200, 0)],
            "double": [(200, 300), (200, 0)],
            "triple": [(200, 200), (200, 200), (200, 0)],
            "sos": [(200, 200), (200, 200), (200, 400),  # S
                   (600, 200), (600, 200), (600, 400),  # O
                   (200, 200), (200, 200), (200, 0)]    # S
        }

        if pattern not in patterns:
            return self.vibrate(500)

        import time
        for duration, pause in patterns[pattern]:
            self.vibrate(duration)
            if pause > 0:
                time.sleep(pause / 1000.0)

        return True

    # ═══════════════════════════════════════════════════════════════════════════
    # WAKE LOCK
    # ═══════════════════════════════════════════════════════════════════════════

    def wake_lock_acquire(self) -> bool:
        """
        Acquire wake lock (prevent device sleep)

        CRITICAL for M.O.L.O.C.H. to prevent being killed!

        Returns:
            Success status
        """
        try:
            subprocess.run(["termux-wake-lock"], capture_output=True, timeout=5)
            self.wake_lock_active = True
            print("🔒 Wake lock acquired")
            return True

        except FileNotFoundError:
            print("⚠️ termux-wake-lock not available")
            return False
        except Exception as e:
            print(f"⚠️ Wake lock error: {e}")
            return False

    def wake_lock_release(self) -> bool:
        """
        Release wake lock (allow device sleep)

        Returns:
            Success status
        """
        try:
            subprocess.run(["termux-wake-unlock"], capture_output=True, timeout=5)
            self.wake_lock_active = False
            print("🔓 Wake lock released")
            return True

        except FileNotFoundError:
            print("⚠️ termux-wake-unlock not available")
            return False
        except Exception as e:
            print(f"⚠️ Wake unlock error: {e}")
            return False

    # ═══════════════════════════════════════════════════════════════════════════
    # BRIGHTNESS CONTROL
    # ═══════════════════════════════════════════════════════════════════════════

    def set_brightness(self, level: int) -> bool:
        """
        Set screen brightness

        Args:
            level: 0-255 or -1 for auto

        Returns:
            Success status

        Examples:
            set_brightness(255)  # Maximum
            set_brightness(128)  # Medium
            set_brightness(50)   # Dim
            set_brightness(-1)   # Auto
        """
        try:
            if level == -1:
                cmd = ["termux-brightness", "auto"]
            else:
                level = max(0, min(255, level))
                cmd = ["termux-brightness", str(level)]

            subprocess.run(cmd, capture_output=True, timeout=5)
            return True

        except FileNotFoundError:
            print("⚠️ termux-brightness not available")
            return False
        except Exception as e:
            print(f"⚠️ Brightness error: {e}")
            return False

    def auto_brightness_for_time(self) -> bool:
        """
        Auto-adjust brightness based on time of day

        Time zones:
        - 22-6: Dark Side Mode (dim: 50)
        - 6-9: Morning (medium: 128)
        - 9-18: Day (auto)
        - 18-22: Evening (medium: 150)

        Returns:
            Success status
        """
        hour = datetime.now().hour

        if 22 <= hour or hour < 6:
            # Dark Side Mode 🖤
            return self.set_brightness(50)
        elif 6 <= hour < 9:
            # Morning
            return self.set_brightness(128)
        elif 9 <= hour < 18:
            # Day
            return self.set_brightness(-1)  # Auto
        else:  # 18-22
            # Evening
            return self.set_brightness(150)

    # ═══════════════════════════════════════════════════════════════════════════
    # COMBINED FEEDBACK
    # ═══════════════════════════════════════════════════════════════════════════

    def feedback_processing(self):
        """Feedback: Processing..."""
        self.toast("Processing...", duration="short")

    def feedback_success(self):
        """Feedback: Success!"""
        self.toast("✅ Done!", background_color="#00FF00")
        self.vibrate(200)

    def feedback_error(self):
        """Feedback: Error!"""
        self.toast("❌ Error!", background_color="#FF0000", text_color="#FFFFFF")
        self.vibrate_pattern("double")

    def feedback_listening(self):
        """Feedback: Listening..."""
        self.toast("🎤 Listening...", duration="long", position="top")
        self.vibrate(100)

    def feedback_photo_taken(self):
        """Feedback: Photo taken!"""
        self.toast("📸 Photo taken!", duration="short")
        self.vibrate(100)


# ═══════════════════════════════════════════════════════════════════════════════
# TESTING
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("\n🔔 M.O.L.O.C.H. 3.0 Feedback I/O Test\n")

    feedback = FeedbackIO()

    # Test toast
    print("📝 Testing toast...")
    feedback.toast("Test toast!")

    # Test vibrate
    print("\n📳 Testing vibrate...")
    feedback.vibrate(500)

    # Test wake lock
    print("\n🔒 Testing wake lock...")
    feedback.wake_lock_acquire()
    import time
    time.sleep(2)
    feedback.wake_lock_release()

    # Test brightness
    print("\n💡 Testing brightness...")
    feedback.auto_brightness_for_time()

    # Test combined feedback
    print("\n✅ Testing combined feedback...")
    feedback.feedback_success()

    print()
