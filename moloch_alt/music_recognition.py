#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
╔═══════════════════════════════════════════════════════════════════════════╗
║              MUSIC RECOGNITION - M.O.L.O.C.H. v3.0                        ║
║                   Phase 4: Advanced Awareness Features                     ║
╚═══════════════════════════════════════════════════════════════════════════╝

Erkenne Musik im Hintergrund und integriere mit:
- Shazam-ähnliche Fingerprinting (AcoustID)
- Spotify Integration
- Lyrics & Info Anzeige
- Playlist Auto-Add
- Mood Integration

APIs:
- AcoustID (kostenlos, Open Source)
- MusicBrainz (kostenlos, Open Source)
- Spotify Web API (optional)

Status: Phase 4 Optional Feature
"""

import json
import os
import sys
import time
import subprocess
from pathlib import Path
from datetime import datetime
from threading import Thread, Event
import hashlib


class MusicRecognition:
    """Erkenne und verarbeite Musik aus Audio"""
    
    def __init__(self):
        """Initialisiere Music Recognition"""
        self.home = Path.home()
        self.moloch_dir = self.home / ".moloch"
        self.moloch_dir.mkdir(exist_ok=True)
        
        self.config_file = self.moloch_dir / "music_config.json"
        self.cache_file = self.moloch_dir / "music_cache.json"
        self.history_file = self.moloch_dir / "music_history.json"
        
        self.config = self.load_config()
        self.cache = self.load_cache()
        self.history = self.load_history()
        
        # API Keys
        self.acoustid_key = self.config.get("acoustid_key", "")  # Free tier no key needed
        self.spotify_client_id = self.config.get("spotify_client_id", "")
        self.spotify_token = None
        
        self.stop_daemon = Event()
    
    def load_config(self):
        """Lade Konfiguration"""
        if self.config_file.exists():
            with open(self.config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        
        config = {
            "enabled": True,
            "backend": "acoustid",  # acoustid oder shazam
            "check_interval": 10,
            "min_confidence": 0.8,
            "cache_results": True,
            "spotify_integration": False,
            "auto_add_to_playlist": False,
            "spotify_client_id": "",
            "spotify_client_secret": "",
            "acoustid_key": "",
            "output": {
                "speak": True,
                "console": True,
                "save": True
            }
        }
        
        self.save_config(config)
        return config
    
    def save_config(self, config=None):
        """Speichere Konfiguration"""
        if config is None:
            config = self.config
        
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
    
    def load_cache(self):
        """Lade Cache erkannter Songs"""
        if self.cache_file.exists():
            with open(self.cache_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def save_cache(self):
        """Speichere Cache"""
        with open(self.cache_file, 'w', encoding='utf-8') as f:
            json.dump(self.cache, f, ensure_ascii=False, indent=2)
    
    def load_history(self):
        """Lade History erkannter Songs"""
        if self.history_file.exists():
            with open(self.history_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
    
    def save_history(self):
        """Speichere History"""
        with open(self.history_file, 'w', encoding='utf-8') as f:
            json.dump(self.history, f, ensure_ascii=False, indent=2)
    
    def record_audio(self, duration=10, output_file=None):
        """Nimm Audio auf für Erkennung (Termux)"""
        if output_file is None:
            output_file = "/tmp/moloch_audio_sample.m4a"
        
        try:
            print(f"🎤 Nehme {duration}s Audio auf...")
            
            # Nutze termux-record oder ffmpeg
            # Prefer ffmpeg when available
            try:
                subprocess.run(["ffmpeg", "-version"], capture_output=True, timeout=5)
                cmd = [
                    "ffmpeg",
                    "-f", "alsa" if os.name != 'nt' else "dshow",
                    "-i", "hw:0,0" if os.name != 'nt' else "audio=default",
                    "-t", str(duration),
                    "-q:a", "9",
                    "-acodec", "libmp3lame",
                    output_file
                ]
                result = subprocess.run(cmd, capture_output=True, timeout=duration+10)
                if result.returncode == 0 and Path(output_file).exists():
                    print(f"✅ Audio gespeichert: {output_file}")
                    return output_file
            except Exception:
                # ffmpeg nicht verfügbar oder Aufnahme fehlgeschlagen
                pass

            # Termux/Android fallback
            try:
                return self._record_with_termux(duration)
            except Exception:
                pass
        
        except Exception as e:
            print(f"❌ Recording Fehler: {e}")
            return None
    
    def _record_with_termux(self, duration=10):
        """Fallback: Nutze Termux termux-media-record"""
        output = "/tmp/moloch_audio_sample.m4a"
        try:
            subprocess.run(
                ["termux-media-record", str(duration), output],
                timeout=duration+5
            )
            if Path(output).exists():
                return output
        except:
            pass
        return None
    
    def recognize_acoustid(self, audio_file):
        """Erkenne Song via AcoustID API"""
        print(f"🔍 Erkenne Audio mit AcoustID...")
        
        try:
            # Benötige fpcalc zur Fingerprint-Generierung
            # fpcalc ist Part of chromaprint
            cmd = ["fpcalc", "-json", audio_file]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            if result.returncode != 0:
                print("❌ fpcalc nicht gefunden. Installiere: apt install chromaprint")
                return None
            
            fp_data = json.loads(result.stdout)
            fingerprint = fp_data.get("fingerprint")
            duration = fp_data.get("duration")
            
            if not fingerprint:
                return None
            
            # Query AcoustID
            params = {
                "fingerprint": fingerprint,
                "duration": duration,
                "client": "moloch-v3",
                "format": "json"
            }
            
            if self.acoustid_key:
                params["clientkey"] = self.acoustid_key
            
            query_str = "&".join([f"{k}={v}" for k, v in params.items()])
            url = f"https://api.acoustid.org/v2/lookup?{query_str}"
            
            print(f"🌐 Query AcoustID...")
            response = subprocess.run(
                ["curl", "-s", url],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if response.returncode == 0:
                result_data = json.loads(response.stdout)
                
                if result_data.get("status") == "ok":
                    results = result_data.get("results", [])
                    if results:
                        return self._parse_acoustid_result(results[0])
            
        except Exception as e:
            print(f"❌ AcoustID Fehler: {e}")
        
        return None
    
    def _parse_acoustid_result(self, result):
        """Parsiere AcoustID Ergebnis"""
        score = result.get("score", 0)
        
        if score < self.config.get("min_confidence", 0.8):
            print(f"⚠️  Score zu niedrig: {score:.2f} < {self.config['min_confidence']}")
            return None
        
        recordings = result.get("recordings", [])
        if not recordings:
            return None
        
        recording = recordings[0]
        title = recording.get("title", "Unknown")
        
        artists = []
        for artist in recording.get("artists", []):
            artists.append(artist.get("name", "Unknown Artist"))
        
        return {
            "title": title,
            "artists": artists,
            "score": score,
            "acoustid_id": result.get("id", ""),
            "release_group": recording.get("releases", [{}])[0].get("release_group", {}),
            "timestamp": datetime.now().isoformat()
        }
    
    def get_song_info(self, song_data):
        """Hole zusätzliche Song-Information"""
        info = {
            "title": song_data.get("title", ""),
            "artists": song_data.get("artists", []),
            "album": "Unknown",
            "year": "",
            "genres": [],
            "lyrics_url": "",
            "spotify_url": ""
        }
        
        # Nutze MusicBrainz für mehr Info
        artist_str = ", ".join(song_data.get("artists", []))
        title = song_data.get("title", "")
        
        try:
            mb_search = f"{title} {artist_str}"
            # Könnte MusicBrainz API abfragen
            print(f"🎵 Info: {title} by {artist_str}")
        except:
            pass
        
        return info
    
    def add_to_spotify_playlist(self, song_data):
        """Füge zu Spotify Playlist hinzu (optional)"""
        if not self.config.get("spotify_integration"):
            return False
        
        try:
            print(f"▶️  Versuche zu Spotify Playlist hinzufügen...")
            # Würde Spotify API nutzen
            # Benötigt OAuth Token und Playlist ID
            return False
        except Exception as e:
            print(f"❌ Spotify Add Fehler: {e}")
            return False
    
    def add_to_history(self, song_data):
        """Füge zu History hinzu"""
        entry = {
            "timestamp": song_data.get("timestamp", datetime.now().isoformat()),
            "title": song_data.get("title", "Unknown"),
            "artists": song_data.get("artists", []),
            "score": song_data.get("score", 0),
            "acoustid_id": song_data.get("acoustid_id", "")
        }
        
        self.history.append(entry)
        
        # Behalte nur letzte 500
        self.history = self.history[-500:]
        self.save_history()
    
    def recognize_music(self, audio_file=None, duration=10):
        """Erkenne Musik im Audio"""
        
        if audio_file is None:
            # Nimm Audio auf
            audio_file = self.record_audio(duration)
        
        if not audio_file:
            print("❌ Kein Audio für Erkennung")
            return None
        
        # Erkenne mit AcoustID
        song_data = self.recognize_acoustid(audio_file)
        
        if not song_data:
            print("❌ Konnte Song nicht erkennen")
            return None
        
        print(f"\n✅ SONG ERKANNT!")
        print(f"   Titel: {song_data.get('title', 'Unknown')}")
        print(f"   Künstler: {', '.join(song_data.get('artists', []))}")
        print(f"   Confidence: {song_data.get('score', 0):.2%}")
        
        # Hole weitere Info
        info = self.get_song_info(song_data)
        
        # Spreche an
        if self.config["output"]["speak"]:
            msg = f"Ich höre {song_data.get('title')} von {', '.join(song_data.get('artists', []))}"
            print(f"🔊 {msg}")
            # Könnte speak() aufrufen
        
        # Speichere
        if self.config["output"]["save"]:
            self.add_to_history(song_data)
        
        # Füge zu Spotify hinzu?
        if self.config.get("auto_add_to_playlist"):
            self.add_to_spotify_playlist(song_data)
        
        # Cache
        if self.config.get("cache_results"):
            hash_key = hashlib.md5(
                f"{song_data['title']}{song_data['artists']}".encode()
            ).hexdigest()
            self.cache[hash_key] = song_data
            self.save_cache()
        
        return song_data
    
    def daemon_loop(self, interval=30):
        """Kontinuierliche Musik-Erkennung"""
        print(f"\n🎵 Music Recognition Daemon startet...")
        print(f"   Check-Intervall: {interval}s")
        print(f"   Zum Beenden: Ctrl+C\n")
        
        while not self.stop_daemon.is_set():
            try:
                print(f"🎤 Höre zu...")
                song = self.recognize_music(duration=5)
                
                if song:
                    print(f"✅ {song['title']} erkannt!")
                else:
                    print(f"❌ Kein Song erkannt")
                
                time.sleep(interval)
                
            except KeyboardInterrupt:
                print("\n⏹  Daemon gestoppt!")
                break
            except Exception as e:
                print(f"❌ Daemon Fehler: {e}")
                time.sleep(interval)
    
    def get_history(self, limit=20):
        """Hole letzte erkannte Songs"""
        return self.history[-limit:]
    
    def get_stats(self):
        """Statistiken"""
        artists = {}
        for entry in self.history:
            for artist in entry.get("artists", []):
                artists[artist] = artists.get(artist, 0) + 1
        
        return {
            "total_songs": len(self.history),
            "unique_artists": len(artists),
            "top_artists": sorted(artists.items(), key=lambda x: x[1], reverse=True)[:5]
        }
    
    def display_dashboard(self):
        """Zeige Dashboard"""
        print("\n" + "="*60)
        print("🎵 MUSIC RECOGNITION DASHBOARD")
        print("="*60)
        
        stats = self.get_stats()
        print(f"\n📊 Statistiken:")
        print(f"   Songs erkannt: {stats['total_songs']}")
        print(f"   Einzigartige Künstler: {stats['unique_artists']}")
        
        if stats['top_artists']:
            print(f"\n   Top Künstler:")
            for artist, count in stats['top_artists']:
                print(f"     • {artist}: {count}x")
        
        recent = self.get_history(5)
        if recent:
            print(f"\n🎼 Letzte Songs:")
            for entry in recent:
                artists = ", ".join(entry.get("artists", []))
                print(f"   {entry['timestamp'][:10]}: {entry['title']}")
                print(f"      by {artists}")
        
        print("\n" + "="*60)


def main():
    """CLI Interface"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Music Recognition für M.O.L.O.C.H.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Beispiele:
  python music_recognition.py recognize     # Erkenne einen Song
  python music_recognition.py daemon        # Daemon Mode
  python music_recognition.py history       # Zeige History
  python music_recognition.py stats         # Statistiken
  python music_recognition.py dashboard     # Dashboard
        """
    )
    
    parser.add_argument(
        "command",
        choices=["recognize", "daemon", "history", "stats", "dashboard"],
        help="Befehl zum Ausführen"
    )
    
    parser.add_argument(
        "-d", "--duration",
        type=int,
        default=10,
        help="Aufnahmedauer in Sekunden (default: 10)"
    )
    
    parser.add_argument(
        "-f", "--file",
        help="Audio-Datei zum Analysieren"
    )
    
    args = parser.parse_args()
    
    music = MusicRecognition()
    
    if args.command == "recognize":
        song = music.recognize_music(
            audio_file=args.file,
            duration=args.duration
        )
        if song:
            print(f"\n📌 Song gespeichert!")
    
    elif args.command == "daemon":
        music.daemon_loop(interval=30)
    
    elif args.command == "history":
        history = music.get_history(20)
        print(f"\n🎵 Letzte {len(history)} erkannte Songs:")
        for i, entry in enumerate(history, 1):
            artists = ", ".join(entry.get("artists", []))
            print(f"\n{i}. {entry['title']}")
            print(f"   Artists: {artists}")
            print(f"   Zeit: {entry['timestamp']}")
    
    elif args.command == "stats":
        music.display_dashboard()
    
    elif args.command == "dashboard":
        music.display_dashboard()


if __name__ == "__main__":
    main()
