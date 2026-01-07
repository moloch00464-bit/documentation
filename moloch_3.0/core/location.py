#!/usr/bin/env python3
"""M.O.L.O.C.H. 3.1 - Location Tracking"""

import json
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict


class LocationTracker:
    """GPS location awareness"""

    def __init__(self, data_dir):
        self.data_dir = data_dir
        self.location_file = data_dir / "last_location.json"
        self.last_location = self._load_last_location()

    def _load_last_location(self) -> Optional[Dict]:
        """Load last known location"""
        if self.location_file.exists():
            try:
                with open(self.location_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        return None

    def _save_location(self, location: Dict):
        """Save location"""
        try:
            with open(self.location_file, 'w') as f:
                json.dump(location, f, indent=2)
        except Exception as e:
            print(f"⚠️  Failed to save location: {e}")

    def get_current_location(self) -> Optional[Dict]:
        """Get current GPS location"""
        try:
            result = subprocess.run(
                ["termux-location"],
                capture_output=True,
                text=True,
                timeout=10
            )

            if result.returncode == 0:
                location = json.loads(result.stdout)
                location["timestamp"] = datetime.now().isoformat()
                return location

        except Exception as e:
            print(f"⚠️  Location failed: {e}")

        return None

    def get_location_summary(self) -> str:
        """Get location summary"""
        current = self.get_current_location()

        if not current:
            return "📍 Location: Nicht verfügbar"

        lat = current.get("latitude", "?")
        lon = current.get("longitude", "?")

        # Simple city detection based on coordinates
        city = "Unbekannt"
        if isinstance(lat, (int, float)) and isinstance(lon, (int, float)):
            # Nürnberg: ~49.45, 11.07
            if 49.3 < lat < 49.6 and 10.9 < lon < 11.2:
                city = "Nürnberg"
            # Leipzig: ~51.34, 12.37
            elif 51.2 < lat < 51.5 and 12.2 < lon < 12.5:
                city = "Leipzig"
            # Berlin: ~52.52, 13.40
            elif 52.3 < lat < 52.7 and 13.2 < lon < 13.6:
                city = "Berlin"

        # Check if location changed
        changed = False
        if self.last_location:
            last_city = self.last_location.get("detected_city", "?")
            if city != last_city:
                changed = True

        # Save current location
        current["detected_city"] = city
        self._save_location(current)
        self.last_location = current

        if changed:
            return f"📍 Location: {city} (CHANGED!)"
        else:
            return f"📍 Location: {city}"
