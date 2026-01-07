#!/usr/bin/env python3
"""
Share Intent Handler für M.O.L.O.C.H.
Android Apps können Text/Links/Dateien an M.O.L.O.C.H. senden

Integration mit Tasker:
  1. Neu Intent Filter: android.intent.action.SEND
  2. Data Type: text/plain, text/uri-list, etc
  3. Call: termux-open 'moloch://share?text=...'
  4. oder: python share_handler.py --from-intent <text>

Usage:
  python share_handler.py --from-intent "text"    # Handle shared text
  python share_handler.py --process "text"        # Process & analyze
  python share_handler.py --link "url"            # Process link
  python share_handler.py --file "path"           # Process file
  python share_handler.py --list                  # Liste shared items
"""

import os
import sys
import json
import subprocess
import time
import requests
import re
from datetime import datetime
from urllib.parse import urlparse, parse_qs

# Pfade
SHARE_DIR = os.path.expanduser("~/moloch/shared")
SHARE_LOG = os.path.join(SHARE_DIR, "share_log.json")
SHARE_HISTORY = os.path.expanduser("~/moloch/share_history.json")

class ShareIntentHandler:
    def __init__(self):
        os.makedirs(SHARE_DIR, exist_ok=True)
        self.history = self.load_history()
    
    def load_history(self):
        """Lade Share History."""
        if os.path.exists(SHARE_HISTORY):
            try:
                with open(SHARE_HISTORY, 'r') as f:
                    return json.load(f)
            except:
                pass
        return []
    
    def save_history(self):
        """Speichere Share History."""
        with open(SHARE_HISTORY, 'w') as f:
            json.dump(self.history[-100:], f, indent=2)  # Letzte 100
    
    def add_to_history(self, item_type: str, content: str, result: str = ""):
        """Füge zu History hinzu."""
        self.history.append({
            "timestamp": datetime.now().isoformat(),
            "type": item_type,
            "content": content[:200],  # Kürze
            "result": result[:200]
        })
        self.save_history()
    
    def process_text(self, text: str):
        """Verarbeite gemeinsamer Text."""
        print(f"📝 Text erhalten: {text[:100]}...")
        
        # Kurze Texte: direkt an Claude
        if len(text) < 500:
            print("💭 Sende zu Claude für Analyse...")
            
            try:
                sys.path.insert(0, os.path.expanduser("~/moloch"))
                from moloch import ask_claude, speak, auto_brain_save_genesis
                
                response = ask_claude(text)
                self.add_to_history("text_analysis", text, response)
                
                # Spreche Antwort
                speak(response)
                
                print(f"✅ Antwort: {response[:100]}...")
                
                # Speichere in Brain
                auto_brain_save_genesis({
                    "type": "shared_text_analysis",
                    "input": text,
                    "response": response,
                    "timestamp": datetime.now().isoformat()
                })
                
                return response
            
            except Exception as e:
                print(f"❌ Claude Error: {e}")
                self.add_to_history("text_analysis_error", text, str(e))
                return None
        
        # Lange Texte: Speichere & Zusammenfassung
        else:
            print("📄 Lange Text - speichere & fasse zusammen...")
            
            filename = f"shared_text_{int(time.time())}.txt"
            filepath = os.path.join(SHARE_DIR, filename)
            
            with open(filepath, 'w') as f:
                f.write(text)
            
            try:
                sys.path.insert(0, os.path.expanduser("~/moloch"))
                from moloch import ask_claude, speak, auto_brain_save_genesis
                
                # Fasse zusammen (nur erste 1000 Zeichen)
                summary_prompt = f"Fasse prägnant zusammen:\n{text[:1000]}"
                summary = ask_claude(summary_prompt)
                
                self.add_to_history("text_summary", text[:100], summary)
                
                speak(f"Text gespeichert. Zusammenfassung: {summary}")
                
                auto_brain_save_genesis({
                    "type": "shared_text_storage",
                    "file": filename,
                    "summary": summary
                })
                
                return summary
            
            except Exception as e:
                print(f"❌ Error: {e}")
                return None
    
    def process_link(self, url: str):
        """Verarbeite shared Link."""
        print(f"🔗 Link erhalten: {url}")
        
        # Validiere URL
        try:
            result = urlparse(url)
            if not result.scheme:
                url = f"https://{url}"
        except:
            print(f"❌ Ungültige URL")
            return None
        
        try:
            # Fetch Page Content
            print("📡 Lade Page...")
            response = requests.get(url, timeout=10, headers={
                "User-Agent": "Mozilla/5.0"
            })
            
            # Einfache Extraktion von Content
            content = response.text
            
            # Entferne HTML Tags
            import re
            text = re.sub(r'<[^>]+>', ' ', content)
            text = ' '.join(text.split())[:2000]  # Erste 2000 Zeichen
            
            print(f"✅ Page geladen ({len(text)} chars)")
            
            # Analysiere mit Claude
            sys.path.insert(0, os.path.expanduser("~/moloch"))
            from moloch import ask_claude, speak, auto_brain_save_genesis
            
            analysis_prompt = f"Analyse diese Webpage:\nURL: {url}\n\nContent:\n{text}"
            analysis = ask_claude(analysis_prompt)
            
            self.add_to_history("link_analysis", url, analysis)
            
            # Spreche Zusammenfassung
            speak(f"Link analysiert. {analysis[:200]}")
            
            auto_brain_save_genesis({
                "type": "shared_link",
                "url": url,
                "analysis": analysis,
                "timestamp": datetime.now().isoformat()
            })
            
            print(f"📊 Analyse: {analysis[:100]}...")
            return analysis
        
        except Exception as e:
            print(f"❌ Link Processing Error: {e}")
            self.add_to_history("link_error", url, str(e))
            return None
    
    def process_file(self, filepath: str):
        """Verarbeite shared Datei."""
        print(f"📁 Datei erhalten: {filepath}")
        
        if not os.path.exists(filepath):
            print(f"❌ Datei nicht gefunden: {filepath}")
            return None
        
        # Bestimme Dateityp
        _, ext = os.path.splitext(filepath)
        
        try:
            if ext.lower() in ['.txt', '.md', '.log']:
                # Text-Datei
                with open(filepath, 'r') as f:
                    content = f.read()[:2000]
                
                return self.process_text(content)
            
            elif ext.lower() in ['.jpg', '.jpeg', '.png', '.gif']:
                # Bild - Analyse mit Vision (wenn verfügbar)
                print("🖼️ Bild erkannt - versuche Analyse...")
                
                try:
                    sys.path.insert(0, os.path.expanduser("~/moloch"))
                    from moloch import ask_claude, speak, auto_brain_save_genesis
                    
                    # Lese Bild und sende zu Claude Vision
                    with open(filepath, 'rb') as f:
                        image_data = f.read()
                    
                    analysis = ask_claude(f"Analysiere dieses Bild: {filepath}")
                    
                    self.add_to_history("image_analysis", filepath, analysis)
                    speak(f"Bild analysiert: {analysis[:200]}")
                    
                    return analysis
                
                except:
                    print("⚠️ Vision Analyse nicht verfügbar")
                    return None
            
            else:
                print(f"⚠️ Dateityp nicht unterstützt: {ext}")
                return None
        
        except Exception as e:
            print(f"❌ File Processing Error: {e}")
            self.add_to_history("file_error", filepath, str(e))
            return None
    
    def list_shared(self):
        """Liste geteilt Items."""
        if not self.history:
            print("📭 Keine geteilten Items")
            return
        
        print(f"📝 Share History ({len(self.history)} Items):\n")
        
        # Zeige letzte 10
        for item in self.history[-10:][::-1]:
            timestamp = item.get("timestamp", "")
            item_type = item.get("type", "unknown")
            content = item.get("content", "")
            
            print(f"⏰ {timestamp}")
            print(f"   Type: {item_type}")
            print(f"   Content: {content[:100]}...")
            print()
    
    def handle_from_intent(self, text: str):
        """Handle Share Intent direkt."""
        print("📨 Share Intent empfangen")
        
        # Erkenne Typ
        if text.startswith("http://") or text.startswith("https://"):
            return self.process_link(text)
        
        elif text.startswith("/") or text.startswith("file://"):
            return self.process_file(text)
        
        else:
            # Text
            return self.process_text(text)

if __name__ == "__main__":
    handler = ShareIntentHandler()
    
    if len(sys.argv) < 2:
        print(__doc__)
    
    elif sys.argv[1] == "--from-intent":
        if len(sys.argv) > 2:
            content = " ".join(sys.argv[2:])
            handler.handle_from_intent(content)
    
    elif sys.argv[1] == "--process":
        if len(sys.argv) > 2:
            text = " ".join(sys.argv[2:])
            handler.process_text(text)
    
    elif sys.argv[1] == "--link":
        if len(sys.argv) > 2:
            url = " ".join(sys.argv[2:])
            handler.process_link(url)
    
    elif sys.argv[1] == "--file":
        if len(sys.argv) > 2:
            filepath = " ".join(sys.argv[2:])
            handler.process_file(filepath)
    
    elif sys.argv[1] == "--list":
        handler.list_shared()
    
    else:
        print(__doc__)
