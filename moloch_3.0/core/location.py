#!/usr/bin/env python3
"""
M.O.L.O.C.H. 3.0 - Location Awareness
======================================
GPS tracking + Location-based context inference

KOSTENLOS! Nutzt termux-location (kein API!)
"""

import subprocess
import json
from pathlib import Path
from typing import Optional, Dict, Tuple
from datetime import datetime


class LocationTracker:
    """
    Track user location and infer context

    Features:
    - GPS via termux-location (FREE!)
    - Detect location changes
    - Store location history
    - Reverse geocoding (city name)
    """

    def __init__(self, data_dir: Path):
        """Initialize tracker"""
        self.data_dir = data_dir
        self.location_file = data_dir / "last_location.json"

    def get_current_location(self, timeout: int = 10) -> Optional[Dict]:
        """
        Get current GPS location via termux-location

        Args:
            timeout: Max wait time for GPS fix

        Returns:
            Location data or None
        """
        try:
            print("📍 Getting GPS location...")

            result = subprocess.run(
                ["/data/data/com.termux/files/usr/bin/termux-location"],
                capture_output=True,
                timeout=timeout,
                text=True
            )

            if result.returncode == 0 and result.stdout:
                try:
                    data = json.loads(result.stdout)
                except json.JSONDecodeError:
                    print("⚠️ Invalid JSON from termux-location")
                    return None

                location = {
                    "lat": data.get("latitude"),
                    "lon": data.get("longitude"),
                    "accuracy": data.get("accuracy"),
                    "timestamp": datetime.now().isoformat()
                }

                # Add city name (simple reverse geocoding)
                location["city"] = self._reverse_geocode(location["lat"], location["lon"])

                print(f"✅ Location: {location['city']} ({location['lat']:.2f}, {location['lon']:.2f})")
                return location

            else:
                print("⚠️ GPS fix failed")
                return None

        except subprocess.TimeoutExpired:
            print("⏱️ GPS timeout (10s)")
            return None

        except FileNotFoundError:
            print("❌ termux-location not found!")
            print("   Install: pkg install termux-api")
            return None

        except Exception as e:
            print(f"❌ GPS error: {e}")
            return None

    def _reverse_geocode(self, lat: float, lon: float) -> str:
        """
        Reverse geocoding (city name from coordinates)

        Uses Nominatim (OpenStreetMap) free API with fallback to hardcoded cities
        """
        # Try Nominatim API first (FREE!)
        try:
            import requests
            url = f"https://nominatim.openstreetmap.org/reverse"
            params = {
                "lat": lat,
                "lon": lon,
                "format": "json",
                "addressdetails": 1
            }
            headers = {
                "User-Agent": "M.O.L.O.C.H./3.0"  # Required by Nominatim
            }

            response = requests.get(url, params=params, headers=headers, timeout=5)

            if response.status_code == 200:
                data = response.json()
                address = data.get("address", {})

                # Try to get city name (different keys possible)
                city = (
                    address.get("city") or
                    address.get("town") or
                    address.get("village") or
                    address.get("municipality") or
                    address.get("county")
                )

                if city:
                    return city

        except ImportError:
            print("⚠️ requests module not installed - using fallback")
        except Exception as e:
            print(f"⚠️ Nominatim API error: {e} - using fallback")

        # Fallback: Hardcoded cities (for offline use)
        cities = {
            "Nürnberg": (49.45, 11.08),
            "Berlin": (52.52, 13.40),
            "Leipzig": (51.34, 12.37),
            "München": (48.14, 11.58),
            "Hamburg": (53.55, 9.99),
            "Frankfurt": (50.11, 8.68),
            "Köln": (50.94, 6.96),
            "Stuttgart": (48.78, 9.18),
            "Dresden": (51.05, 13.74),
            "Hilpoltstein": (49.19, 11.19),
        }

        # Find closest city (simple distance)
        min_dist = float('inf')
        closest_city = "Unknown"

        for city, (city_lat, city_lon) in cities.items():
            # Simple Euclidean distance (good enough for rough matching)
            dist = ((lat - city_lat) ** 2 + (lon - city_lon) ** 2) ** 0.5

            if dist < min_dist:
                min_dist = dist
                closest_city = city

        # If too far from any known city, use "Unknown"
        if min_dist > 0.5:  # ~50km threshold
            return f"Unknown ({lat:.2f}, {lon:.2f})"

        return closest_city

    def get_last_location(self) -> Optional[Dict]:
        """Load last known location from file"""
        try:
            if self.location_file.exists():
                return json.loads(self.location_file.read_text())
            return None
        except Exception as e:
            print(f"⚠️ Could not load last location: {e}")
            return None

    def save_location(self, location: Dict):
        """Save current location to file"""
        try:
            self.location_file.write_text(json.dumps(location, indent=2))
        except Exception as e:
            print(f"⚠️ Could not save location: {e}")

    def check_location_change(self) -> Tuple[bool, Optional[str], Optional[str]]:
        """
        Check if location has changed since last session

        Returns:
            (changed, last_city, current_city)
        """
        current = self.get_current_location()

        if not current:
            return False, None, None

        last = self.get_last_location()

        if not last:
            # First run - no previous location
            self.save_location(current)
            return False, None, current["city"]

        # Compare cities
        last_city = last.get("city", "Unknown")
        current_city = current.get("city", "Unknown")

        changed = (last_city != current_city)

        # Save current location
        self.save_location(current)

        return changed, last_city, current_city

    def get_location_summary(self) -> str:
        """
        Get a nice summary of current location + change detection

        Returns:
            Summary string to display
        """
        changed, last_city, current_city = self.check_location_change()

        if not current_city:
            return "⚠️ GPS nicht verfügbar"

        if changed and last_city:
            return f"""
📍 STANDORTWECHSEL ERKANNT!
   War: {last_city}
   Jetzt: {current_city}
"""
        else:
            return f"📍 Standort: {current_city}"


# ═══════════════════════════════════════════════════════════════════════════════
# TESTING
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    from core.config import DATA_DIR

    tracker = LocationTracker(DATA_DIR)

    print("\n🌍 Testing Location Tracker\n")

    # Get current location
    location = tracker.get_current_location()

    if location:
        print(f"\n✅ Current Location:")
        print(f"   City: {location['city']}")
        print(f"   Coordinates: {location['lat']:.4f}, {location['lon']:.4f}")
        print(f"   Accuracy: {location['accuracy']:.1f}m")

    # Check for changes
    print("\n🔄 Checking for location changes...")
    summary = tracker.get_location_summary()
    print(summary)
