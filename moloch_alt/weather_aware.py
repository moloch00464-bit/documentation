#!/usr/bin/env python3
"""
Weather Awareness für M.O.L.O.C.H.
Wetterdaten integrieren, adaptive Persönlichkeit

Nutzt Open-Meteo API (kostenlos, keine Key erforderlich)

Usage:
  python weather_aware.py --current          # Aktuelles Wetter
  python weather_aware.py --forecast         # Vorhersage
  python weather_aware.py --daemon           # Background Monitor
"""

import os
import sys
import json
import requests
from datetime import datetime

WEATHER_CONFIG = os.path.expanduser("~/moloch/weather.json")
WEATHER_CACHE = os.path.expanduser("~/moloch/weather_cache.json")

class WeatherAwareness:
    def __init__(self, latitude=None, longitude=None):
        self.config = self.load_config()
        self.latitude = latitude or self.config.get("latitude")
        self.longitude = longitude or self.config.get("longitude")
        self.current_weather = None
    
    def load_config(self):
        """Lade Wetter Config."""
        if os.path.exists(WEATHER_CONFIG):
            try:
                with open(WEATHER_CONFIG, 'r') as f:
                    return json.load(f)
            except:
                pass
        
        # Default: Berlin
        return {
            "latitude": 52.52,
            "longitude": 13.40,
            "city": "Berlin"
        }
    
    def save_config(self):
        """Speichere Wetter Config."""
        os.makedirs(os.path.dirname(WEATHER_CONFIG), exist_ok=True)
        with open(WEATHER_CONFIG, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def load_cache(self):
        """Lade Cache."""
        if os.path.exists(WEATHER_CACHE):
            try:
                with open(WEATHER_CACHE, 'r') as f:
                    return json.load(f)
            except:
                pass
        
        return {}
    
    def save_cache(self, data):
        """Speichere Cache."""
        os.makedirs(os.path.dirname(WEATHER_CACHE), exist_ok=True)
        with open(WEATHER_CACHE, 'w') as f:
            json.dump(data, f, indent=2)
    
    def fetch_weather(self):
        """Hole Wetterdaten von Open-Meteo."""
        if not self.latitude or not self.longitude:
            print("❌ Koordinaten nicht gesetzt")
            return None
        
        try:
            url = "https://api.open-meteo.com/v1/forecast"
            params = {
                "latitude": self.latitude,
                "longitude": self.longitude,
                "current": "temperature_2m,weather_code,wind_speed_10m",
                "hourly": "temperature_2m,weather_code",
                "daily": "weather_code,temperature_2m_max,temperature_2m_min",
                "timezone": "Europe/Berlin"
            }
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                # Cache
                cache = self.load_cache()
                cache["last_update"] = datetime.now().isoformat()
                cache["weather"] = data
                self.save_cache(cache)
                
                self.current_weather = data
                return data
            else:
                print(f"⚠️ Wetter API Error: {response.status_code}")
                return None
        
        except Exception as e:
            print(f"❌ Wetter Fehler: {e}")
            return None
    
    def get_weather_description(self, weather_code):
        """Übersetze Weather Code zu Beschreibung."""
        codes = {
            0: "Klar",
            1: "Leicht bewölkt",
            2: "Teilweise bewölkt",
            3: "Überwiegend bewölkt",
            45: "Nebelig",
            48: "Gefrierender Nebel",
            51: "Leichter Regen",
            53: "Mäßiger Regen",
            55: "Starker Regen",
            61: "Regen",
            63: "Mäßiger Regen",
            65: "Starker Regen",
            71: "Leichter Schnee",
            73: "Mäßiger Schnee",
            75: "Starker Schnee",
            77: "Schneegraupel",
            80: "Regenschauer",
            81: "Mäßiger Regenschauer",
            82: "Heftiger Regenschauer",
            85: "Leichter Schneeschauer",
            86: "Heftiger Schneeschauer",
            95: "Gewitter",
            96: "Gewitter mit Hagel",
            99: "Gewitter mit Hagel"
        }
        
        return codes.get(weather_code, "Unbekannt")
    
    def get_personality_by_weather(self):
        """Bestimme Persönlichkeit basierend auf Wetter."""
        if not self.current_weather:
            return "hal"  # Default
        
        current = self.current_weather.get("current", {})
        weather_code = current.get("weather_code", 0)
        temp = current.get("temperature_2m", 15)
        
        # Sonnig & warm = frech (Pumuckl)
        if weather_code in [0, 1] and temp > 20:
            return "pumuckl"
        
        # Regnerisch & kalt = ernst (HAL)
        if weather_code in [51, 53, 55, 61, 63, 65]:
            return "hal"
        
        # Bewölkt & kühl = normal
        if weather_code in [2, 3] and temp < 15:
            return "hal"
        
        # Gewitter = dramatisch
        if weather_code >= 80:
            return "max_headroom"  # Cyberpunk Mode!
        
        return "hal"
    
    def get_mood_bonus(self):
        """Bestimme Mood Bonus basierend auf Wetter."""
        if not self.current_weather:
            return "neutral"
        
        weather_code = self.current_weather.get("current", {}).get("weather_code", 0)
        temp = self.current_weather.get("current", {}).get("temperature_2m", 15)
        
        if weather_code == 0 and temp > 22:
            return "euphoric"
        elif weather_code in [51, 53, 55, 61, 63, 65]:
            return "melancholic"
        elif weather_code >= 95:
            return "energetic"
        elif temp < 5:
            return "cozy"
        
        return "neutral"
    
    def display_weather(self):
        """Zeige Wetter an."""
        if not self.fetch_weather():
            print("❌ Wetter konnte nicht abgerufen werden")
            return
        
        print("\n" + "="*70)
        print("🌤️  M.O.L.O.C.H. WEATHER STATUS")
        print("="*70 + "\n")
        
        current = self.current_weather.get("current", {})
        
        # Aktuelle Werte
        temp = current.get("temperature_2m")
        weather_code = current.get("weather_code")
        wind = current.get("wind_speed_10m")
        
        description = self.get_weather_description(weather_code)
        personality = self.get_personality_by_weather()
        mood = self.get_mood_bonus()
        
        print(f"📍 Standort: {self.config.get('city', 'Unknown')}")
        print(f"   Lat: {self.latitude}, Lon: {self.longitude}\n")
        
        print(f"🌡️  Temperatur: {temp}°C")
        print(f"☁️  Wetter: {description}")
        print(f"💨 Wind: {wind} km/h\n")
        
        print(f"🎭 Personality: {personality.upper()}")
        print(f"😊 Mood: {mood.upper()}\n")
        
        # Vorhersage (nächste 6h)
        hourly = self.current_weather.get("hourly", {})
        if hourly and "temperature_2m" in hourly:
            temps = hourly["temperature_2m"][:6]
            print(f"📊 Temperatur nächste 6 Stunden:")
            print(f"   {' → '.join([f'{t}°C' for t in temps])}")
        
        print("\n" + "="*70 + "\n")
    
    def display_forecast(self):
        """Zeige Vorhersage."""
        if not self.fetch_weather():
            return
        
        print("\n" + "="*70)
        print("📅 WETTER-VORHERSAGE (7 Tage)")
        print("="*70 + "\n")
        
        daily = self.current_weather.get("daily", {})
        
        if not daily or "weather_code" not in daily:
            print("Keine Vorhersage verfügbar")
            return
        
        dates = daily.get("time", [])
        codes = daily.get("weather_code", [])
        temps_max = daily.get("temperature_2m_max", [])
        temps_min = daily.get("temperature_2m_min", [])
        
        for i in range(min(7, len(dates))):
            date = datetime.fromisoformat(dates[i])
            code = codes[i]
            t_max = temps_max[i]
            t_min = temps_min[i]
            description = self.get_weather_description(code)
            
            day_name = date.strftime("%A")
            date_str = date.strftime("%d.%m")
            
            print(f"📅 {day_name}, {date_str}")
            print(f"   {description}")
            print(f"   🌡️  {t_max}°C / {t_min}°C\n")
        
        print("="*70 + "\n")
    
    def weather_daemon(self, check_interval=1800):
        """Wetter Daemon (Update alle 30 min)."""
        import time
        
        print(f"🌤️  Wetter Daemon gestartet (Update alle {check_interval}s)")
        
        try:
            while True:
                self.fetch_weather()
                
                if self.current_weather:
                    current = self.current_weather.get("current", {})
                    temp = current.get("temperature_2m")
                    desc = self.get_weather_description(current.get("weather_code", 0))
                    
                    print(f"⏰ {datetime.now().strftime('%H:%M')} - {temp}°C, {desc}")
                
                time.sleep(check_interval)
        
        except KeyboardInterrupt:
            print("\n⛔ Wetter Daemon gestoppt")

if __name__ == "__main__":
    weather = WeatherAwareness()
    
    if len(sys.argv) < 2:
        print(__doc__)
    
    elif sys.argv[1] == "--current":
        weather.display_weather()
    
    elif sys.argv[1] == "--forecast":
        weather.display_forecast()
    
    elif sys.argv[1] == "--daemon":
        interval = int(sys.argv[2]) if len(sys.argv) > 2 else 1800
        weather.weather_daemon(interval)
    
    elif sys.argv[1] == "--set-location":
        if len(sys.argv) > 3:
            weather.latitude = float(sys.argv[2])
            weather.longitude = float(sys.argv[3])
            weather.config["latitude"] = weather.latitude
            weather.config["longitude"] = weather.longitude
            if len(sys.argv) > 4:
                weather.config["city"] = sys.argv[4]
            weather.save_config()
            print(f"✅ Standort gespeichert")
    
    else:
        print(__doc__)
