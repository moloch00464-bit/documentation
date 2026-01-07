#!/usr/bin/env python3
"""
Spotify Control für M.O.L.O.C.H.
Spiele Musik, Playlists, Künstler direkt an

Requires: Spotify API Setup
  1. https://developer.spotify.com/dashboard
  2. Create App → copy Client ID + Client Secret
  3. Redirect URI: http://localhost:8888/callback
  4. Save to ~/moloch/spotify_config.json

Usage:
  python spotify_control.py --setup          # OAuth Flow
  python spotify_control.py play "artist"    # Spiele Künstler
  python spotify_control.py play:album       # Spiele Album
  python spotify_control.py play:playlist    # Spiele Playlist
  python spotify_control.py next             # Nächster Track
  python spotify_control.py previous         # Vorheriger Track
  python spotify_control.py pause            # Pausiere
  python spotify_control.py resume           # Fortsetzen
  python spotify_control.py volume 80        # Volume 0-100
  python spotify_control.py now              # Zeige aktuellen Song
"""

import os
import sys
import json
import base64
import requests
import webbrowser
import time
from urllib.parse import urlencode

# Konfiguration
SPOTIFY_CONFIG_PATH = os.path.expanduser("~/moloch/spotify_config.json")
SPOTIFY_API = "https://api.spotify.com/v1"
AUTH_URL = "https://accounts.spotify.com/authorize"
TOKEN_URL = "https://accounts.spotify.com/api/token"

class SpotifyMoloch:
    def __init__(self):
        self.config = self.load_config()
        self.access_token = None
        self.refresh_token = None
        self.token_expires = 0
    
    def load_config(self):
        """Lade Spotify Config."""
        if os.path.exists(SPOTIFY_CONFIG_PATH):
            try:
                with open(SPOTIFY_CONFIG_PATH, 'r') as f:
                    return json.load(f)
            except:
                pass
        
        return {
            "client_id": "",
            "client_secret": "",
            "redirect_uri": "http://localhost:8888/callback",
            "refresh_token": "",
            "device_id": ""
        }
    
    def save_config(self):
        """Speichere Spotify Config."""
        os.makedirs(os.path.dirname(SPOTIFY_CONFIG_PATH), exist_ok=True)
        with open(SPOTIFY_CONFIG_PATH, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def setup_oauth(self):
        """OAuth Flow für Spotify."""
        if not self.config.get("client_id") or not self.config.get("client_secret"):
            print("❌ Bitte Client ID + Secret in spotify_config.json setzen")
            print(f"📁 Config: {SPOTIFY_CONFIG_PATH}")
            return False
        
        print("🎵 Spotify OAuth Setup...")
        
        # Step 1: Authorization Request
        params = {
            "client_id": self.config["client_id"],
            "response_type": "code",
            "redirect_uri": self.config["redirect_uri"],
            "scope": "user-read-private user-read-email user-modify-playback-state user-read-playback-state"
        }
        
        auth_url = f"{AUTH_URL}?{urlencode(params)}"
        print(f"\n🌐 Öffne Browser: {auth_url}\n")
        
        try:
            webbrowser.open(auth_url)
        except:
            print(f"Browser konnte nicht geöffnet werden. Öffne manuell:\n{auth_url}")
        
        # Step 2: User gibt Code ein
        code = input("Paste den Code aus der Redirect-URL: ").strip()
        
        if not code:
            print("❌ Kein Code eingegeben")
            return False
        
        # Step 3: Token Request
        auth_str = f"{self.config['client_id']}:{self.config['client_secret']}"
        auth_b64 = base64.b64encode(auth_str.encode()).decode()
        
        headers = {
            "Authorization": f"Basic {auth_b64}",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        
        data = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": self.config["redirect_uri"]
        }
        
        try:
            resp = requests.post(TOKEN_URL, headers=headers, data=data, timeout=10)
            token_data = resp.json()
            
            if "access_token" in token_data:
                self.config["refresh_token"] = token_data.get("refresh_token", "")
                self.save_config()
                
                print("✅ Spotify OAuth erfolgreich!")
                print(f"🔑 Refresh Token gespeichert")
                
                self.access_token = token_data["access_token"]
                self.token_expires = time.time() + token_data.get("expires_in", 3600)
                
                return True
            else:
                print(f"❌ Token Error: {token_data}")
                return False
        
        except Exception as e:
            print(f"❌ OAuth Error: {e}")
            return False
    
    def refresh_access_token(self):
        """Hole neuen Access Token mit Refresh Token."""
        if not self.config.get("refresh_token"):
            print("❌ Kein Refresh Token vorhanden - führe Setup durch")
            return False
        
        auth_str = f"{self.config['client_id']}:{self.config['client_secret']}"
        auth_b64 = base64.b64encode(auth_str.encode()).decode()
        
        headers = {
            "Authorization": f"Basic {auth_b64}",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        
        data = {
            "grant_type": "refresh_token",
            "refresh_token": self.config["refresh_token"]
        }
        
        try:
            resp = requests.post(TOKEN_URL, headers=headers, data=data, timeout=10)
            token_data = resp.json()
            
            if "access_token" in token_data:
                self.access_token = token_data["access_token"]
                self.token_expires = time.time() + token_data.get("expires_in", 3600)
                return True
            else:
                print(f"❌ Token Refresh Error: {token_data}")
                return False
        
        except Exception as e:
            print(f"❌ Refresh Error: {e}")
            return False
    
    def ensure_token(self):
        """Stelle sicher, dass gültiger Token existiert."""
        if self.access_token and time.time() < self.token_expires:
            return True
        
        return self.refresh_access_token()
    
    def api_call(self, endpoint: str, method: str = "GET", data: dict = None):
        """Mache Spotify API Request."""
        if not self.ensure_token():
            return None
        
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        
        url = f"{SPOTIFY_API}{endpoint}"
        
        try:
            if method == "GET":
                resp = requests.get(url, headers=headers, timeout=10)
            elif method == "POST":
                resp = requests.post(url, headers=headers, json=data, timeout=10)
            elif method == "PUT":
                resp = requests.put(url, headers=headers, json=data, timeout=10)
            else:
                return None
            
            if resp.status_code in [200, 201, 204]:
                return resp.json() if resp.text else {"success": True}
            else:
                print(f"⚠️ API Error {resp.status_code}: {resp.text}")
                return None
        
        except Exception as e:
            print(f"❌ API Call Error: {e}")
            return None
    
    def search_and_play(self, query: str, search_type: str = "artist"):
        """Suche und spiele einen Künstler/Song/Album."""
        print(f"🔍 Suche {search_type}: {query}...")
        
        # Search
        result = self.api_call(
            f"/search?q={query}&type={search_type}&limit=1"
        )
        
        if not result:
            print(f"❌ Suche fehlgeschlagen")
            return False
        
        items_key = f"{search_type}s"
        if search_type == "track":
            items_key = "tracks"
        
        if not result.get(items_key, {}).get("items"):
            print(f"❌ Kein {search_type} gefunden")
            return False
        
        item = result[items_key]["items"][0]
        item_uri = item["uri"]
        item_name = item.get("name", "Unknown")
        
        print(f"▶️ Starte: {item_name}")
        
        # Get devices
        devices_result = self.api_call("/me/player/devices")
        if not devices_result or not devices_result.get("devices"):
            print("❌ Kein aktives Spotify Device gefunden")
            return False
        
        device_id = devices_result["devices"][0]["id"]
        
        # Play
        play_result = self.api_call(
            f"/me/player/play?device_id={device_id}",
            method="PUT",
            data={
                "context_uri": item_uri if search_type != "track" else None,
                "uris": [item_uri] if search_type == "track" else None
            }
        )
        
        return play_result is not None
    
    def next_track(self):
        """Nächster Track."""
        result = self.api_call("/me/player/next", method="POST")
        if result:
            print("⏭️ Nächster Track")
            return True
        return False
    
    def previous_track(self):
        """Vorheriger Track."""
        result = self.api_call("/me/player/previous", method="POST")
        if result:
            print("⏮️ Vorheriger Track")
            return True
        return False
    
    def pause(self):
        """Pausiere Wiedergabe."""
        result = self.api_call("/me/player/pause", method="PUT")
        if result:
            print("⏸️ Pausiert")
            return True
        return False
    
    def resume(self):
        """Fortsetzen."""
        result = self.api_call("/me/player/play", method="PUT")
        if result:
            print("▶️ Fortgesetzt")
            return True
        return False
    
    def set_volume(self, percent: int):
        """Stelle Lautstärke."""
        percent = max(0, min(100, percent))
        result = self.api_call(f"/me/player/volume?volume_percent={percent}", method="PUT")
        if result:
            print(f"🔊 Lautstärke: {percent}%")
            return True
        return False
    
    def now_playing(self):
        """Zeige aktuellen Song."""
        result = self.api_call("/me/player/currently-playing")
        
        if not result:
            print("❌ Kein Song aktuell")
            return
        
        item = result.get("item")
        if not item:
            print("⏸️ Nichts spielt")
            return
        
        artist = ", ".join([a["name"] for a in item.get("artists", [])])
        name = item.get("name", "Unknown")
        progress = result.get("progress_ms", 0) // 1000
        duration = item.get("duration_ms", 0) // 1000
        is_playing = result.get("is_playing", False)
        
        status = "▶️" if is_playing else "⏸️"
        
        print(f"{status} {artist} - {name}")
        print(f"   ⏱️ {progress}s / {duration}s")

if __name__ == "__main__":
    spotify = SpotifyMoloch()
    
    if len(sys.argv) < 2:
        print(__doc__)
    
    elif sys.argv[1] == "--setup":
        spotify.setup_oauth()
    
    elif sys.argv[1] == "play":
        if len(sys.argv) > 2:
            query = " ".join(sys.argv[2:])
            if ":" in query:
                search_type = query.split(":")[0]
                query = query.split(":", 1)[1]
            else:
                search_type = "artist"
            
            spotify.search_and_play(query, search_type)
    
    elif sys.argv[1] == "next":
        spotify.next_track()
    
    elif sys.argv[1] == "previous":
        spotify.previous_track()
    
    elif sys.argv[1] == "pause":
        spotify.pause()
    
    elif sys.argv[1] == "resume":
        spotify.resume()
    
    elif sys.argv[1] == "volume":
        if len(sys.argv) > 2:
            spotify.set_volume(int(sys.argv[2]))
    
    elif sys.argv[1] == "now":
        spotify.now_playing()
