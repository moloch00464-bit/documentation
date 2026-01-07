#!/usr/bin/env python3
"""
Location Awareness für M.O.L.O.C.H.
Ortsbewusstsein & Geofencing

Abhängig von Standort:
- Andere Persönlichkeit
- Automatische Anpassungen
- Context-sensitive Responses

Usage:
  python location_aware.py --current           # Aktueller Ort
  python location_aware.py --add <name>       # Ort hinzufügen
  python location_aware.py --list             # Alle Orte
  python location_aware.py --daemon           # Geofencing Monitor
"""

import os
import sys
import json
import subprocess
from datetime import datetime

LOCATION_CONFIG = os.path.expanduser("~/moloch/locations.json")
LOCATION_MODE = os.path.expanduser("~/moloch/current_location.json")

class LocationAwareness:
    def __init__(self):
        self.config = self.load_config()
        self.current_location = self.load_current_location()
    
    def load_config(self):
        """Lade Locations Config."""
        if os.path.exists(LOCATION_CONFIG):
            try:
                with open(LOCATION_CONFIG, 'r') as f:
                    return json.load(f)
            except:
                pass
        
        return {
            "locations": {
                "home": {
                    "name": "Zuhause",
                    "personality": "pumuckl",  # Zuhause = frecher Kobold
                    "mood_bonus": "relaxed",
                    "ai_style": "casual",
                    "emoji": "🏠"
                },
                "work": {
                    "name": "Arbeit",
                    "personality": "hal",  # Arbeit = professionell
                    "mood_bonus": "focused",
                    "ai_style": "professional",
                    "emoji": "💼"
                },
                "gym": {
                    "name": "Fitnessstudio",
                    "personality": "hal",
                    "mood_bonus": "energetic",
                    "ai_style": "motivating",
                    "emoji": "💪"
                }
            },
            "geofence_radius": 100  # Meter
        }
    
    def save_config(self):
        """Speichere Locations Config."""
        os.makedirs(os.path.dirname(LOCATION_CONFIG), exist_ok=True)
        with open(LOCATION_CONFIG, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def load_current_location(self):
        """Lade aktuellen Standort."""
        if os.path.exists(LOCATION_MODE):
            result = subprocess.run(["termux-location"], capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                data = json.loads(result.stdout)
                return data.get('latitude'), data.get('longitude')
        os.makedirs(os.path.dirname(LOCATION_MODE), exist_ok=True)
            print(f"⚠️ GPS Error: {e}")

        # Fallback: try IP-based geolocation (free service)
        try:
            resp = requests.get('https://ipinfo.io/json', timeout=5)
            if resp.status_code == 200:
                d = resp.json()
                loc = d.get('loc')
                if loc:
                    lat, lon = loc.split(',')
                    return float(lat), float(lon)
            json.dump(self.current_location, f, indent=2)
    
            print(f"⚠️ GPS Error fallback: {e}")

        """Hole aktuellen GPS Standort."""
        try:
            # Termux GPS
            result = subprocess.run(
                ["termux-location"],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                data = json.loads(result.stdout)
                return {
                    "lat": data.get("latitude"),
                    "lon": data.get("longitude"),
                    "accuracy": data.get("accuracy")
                }
        except Exception as e:
            print(f"⚠️ GPS Error: {e}")
        
        return None
    
    def calculate_distance(self, lat1, lon1, lat2, lon2):
        """Berechne Distanz zwischen zwei Koordinaten (Haversine)."""
        from math import radians, sin, cos, sqrt, atan2
        
        R = 6371000  # Erde Radius in Metern
        
        lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * atan2(sqrt(a), sqrt(1-a))
        distance = R * c
        
        return distance
    
    def add_location(self, name, personality="hal", mood="neutral"):
        """Füge neuen Ort hinzu."""
        print(f"📍 Registriere Ort: {name}")
        
        gps = self.get_gps_location()
        
        if not gps:
            print("❌ GPS nicht verfügbar")
            return False
        
        self.config["locations"][name.lower()] = {
            "name": name,
            "latitude": gps["lat"],
            "longitude": gps["lon"],
            "personality": personality,
            "mood_bonus": mood,
            "ai_style": "adaptive",
            "emoji": "📍"
        }
        
        self.save_config()
        print(f"✅ Ort '{name}' gespeichert")
        print(f"   Position: {gps['lat']:.4f}, {gps['lon']:.4f}")
        print(f"   Genauigkeit: {gps['accuracy']}m")
        
        return True
    
    def detect_current_location(self):
        """Erkenne aktuellen Ort via GPS."""
        gps = self.get_gps_location()
        
        if not gps:
            return None
        
        current_lat = gps["lat"]
        current_lon = gps["lon"]
        radius = self.config.get("geofence_radius", 100)
        
        # Vergleiche mit allen bekannten Orten
        closest_location = None
        closest_distance = float('inf')
        
        for loc_key, loc_data in self.config.get("locations", {}).items():
            if "latitude" not in loc_data:
                continue
            
            distance = self.calculate_distance(
                current_lat, current_lon,
                loc_data["latitude"], loc_data["longitude"]
            )
            
            if distance < closest_distance:
                closest_distance = distance
                closest_location = (loc_key, loc_data, distance)
        
        if closest_location and closest_location[2] <= radius:
            return closest_location
        
        return None
    
    def get_current_status(self):
        """Zeige aktuellen Standort Status."""
        print("\n" + "="*70)
        print("📍 M.O.L.O.C.H. LOCATION STATUS")
        print("="*70 + "\n")
        
        gps = self.get_gps_location()
        
        if gps:
            print(f"📡 GPS Aktiv")
            print(f"   Position: {gps['lat']:.4f}, {gps['lon']:.4f}")
            print(f"   Genauigkeit: {gps['accuracy']}m\n")
            
            # Erkenne Ort
            location_info = self.detect_current_location()
            
            if location_info:
                loc_key, loc_data, distance = location_info
                print(f"🎯 Erkannter Ort: {loc_data['name']} {loc_data.get('emoji', '')}")
                print(f"   Entfernung: {distance:.0f}m")
                print(f"   Personality: {loc_data.get('personality', 'unknown')}")
                print(f"   Mood Bonus: {loc_data.get('mood_bonus', 'neutral')}")
                print(f"   AI Style: {loc_data.get('ai_style', 'unknown')}")
            else:
                print(f"❓ Ort nicht erkannt")
        else:
            print("❌ GPS nicht verfügbar")
        
        print("\n" + "="*70 + "\n")
    
    def list_locations(self):
        """Liste alle Orte."""
        locations = self.config.get("locations", {})
        
        if not locations:
            print("📭 Keine Orte registriert")
            return
        
        print("\n📍 Registrierte Orte:\n")
        
        for loc_key, loc_data in locations.items():
            emoji = loc_data.get("emoji", "📍")
            name = loc_data.get("name", loc_key)
            personality = loc_data.get("personality", "?")
            
            if "latitude" in loc_data:
                print(f"{emoji} {name}")
                print(f"   Position: {loc_data['latitude']:.4f}, {loc_data['longitude']:.4f}")
            else:
                print(f"{emoji} {name} (Predefined)")
            
            print(f"   Personality: {personality}")
            print(f"   Mood: {loc_data.get('mood_bonus', 'neutral')}\n")
    
    def geofencing_daemon(self, interval=30):
        """Geofencing Daemon - monitore Standort."""
        import time
        
        print(f"🚀 Geofencing Daemon gestartet (Check alle {interval}s)")
        
        last_location = None
        
        try:
            while True:
                location_info = self.detect_current_location()
                
                if location_info:
                    current_location = location_info[0]
                    loc_data = location_info[1]
                    
                    if current_location != last_location:
                        print(f"\n📍 LOCATION CHANGED: {loc_data['name']}")
                        print(f"   Personality: {loc_data.get('personality')}")
                        print(f"   Mood: {loc_data.get('mood_bonus')}")
                        
                        # Speichere neue Location
                        self.save_current_location(current_location)
                        
                        # Trigger Personality Change (falls moloch.py läuft)
                        try:
                            sys.path.insert(0, os.path.expanduser("~/moloch"))
                            from moloch import speak
                            
                            speak(f"Ich bin angekommen in {loc_data['name']}")
                        except:
                            pass
                        
                        last_location = current_location
                
                time.sleep(interval)
        
        except KeyboardInterrupt:
            print("\n⛔ Geofencing Daemon gestoppt")

if __name__ == "__main__":
    awareness = LocationAwareness()
    
    if len(sys.argv) < 2:
        print(__doc__)
    
    elif sys.argv[1] == "--current":
        awareness.get_current_status()
    
    elif sys.argv[1] == "--list":
        awareness.list_locations()
    
    elif sys.argv[1] == "--add":
        if len(sys.argv) > 2:
            name = sys.argv[2]
            personality = sys.argv[3] if len(sys.argv) > 3 else "hal"
            awareness.add_location(name, personality)
    
    elif sys.argv[1] == "--daemon":
        interval = int(sys.argv[2]) if len(sys.argv) > 2 else 30
        awareness.geofencing_daemon(interval)
    
    else:
        print(__doc__)
