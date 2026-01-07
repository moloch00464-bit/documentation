#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
╔═══════════════════════════════════════════════════════════════════════════╗
║                   CLIPBOARD MONITOR - M.O.L.O.C.H. v3.0                   ║
║                   Phase 4: Advanced Awareness Features                     ║
╚═══════════════════════════════════════════════════════════════════════════╝

Überwacht die Zwischenablage und triggert intelligente Reaktionen:
- Text-Analyse (URLs, Nummern, Links)
- Automatische Aktion (Öffnen, Speichern, Verarbeiten)
- Integration mit Brain & Memory System
- Filtermechanismus gegen Spam

Quelle: Termux API + Android ClipboardManager
Status: Phase 4 Optional Feature
"""

import json
import os
import sys
import time
import hashlib
import re
import subprocess
from datetime import datetime
from pathlib import Path
from collections import defaultdict
from threading import Thread, Event


class ClipboardMonitor:
    """Überwacht Zwischenablage und triggert automatische Reaktionen"""
    
    def __init__(self):
        """Initialisiere Clipboard Monitor"""
        self.home = Path.home()
        self.moloch_dir = self.home / ".moloch"
        self.moloch_dir.mkdir(exist_ok=True)
        
        self.config_file = self.moloch_dir / "clipboard_config.json"
        self.history_file = self.moloch_dir / "clipboard_history.json"
        self.whitelist_file = self.moloch_dir / "clipboard_whitelist.json"
        
        # Lädt oder erstellt Config
        self.config = self.load_config()
        self.history = self.load_history()
        self.whitelist = self.load_whitelist()
        
        # State für Daemon
        self.last_clipboard = None
        self.last_hash = None
        self.stop_daemon = Event()
        
    def load_config(self):
        """Lade Konfiguration"""
        if self.config_file.exists():
            with open(self.config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        
        config = {
            "enabled": True,
            "check_interval": 3,  # Sekunden
            "max_history": 100,
            "auto_actions": {
                "url": True,
                "email": True,
                "phone": True,
                "markdown": False,
                "code": False
            },
            "filters": {
                "min_length": 3,
                "max_length": 10000,
                "ignore_duplicates": True,
                "ignore_patterns": [
                    "^\\s+$",  # Nur Leerzeichen
                    "^[.]*$",  # Nur Punkte
                ]
            },
            "integrations": {
                "brain_save": True,
                "speak": True,
                "log": True
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
    
    def load_history(self):
        """Lade Clipboard History"""
        if self.history_file.exists():
            with open(self.history_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
    
    def save_history(self):
        """Speichere Clipboard History"""
        # Behalte nur die letzten N Einträge
        max_h = self.config.get("max_history", 100)
        history = self.history[-max_h:]
        
        with open(self.history_file, 'w', encoding='utf-8') as f:
            json.dump(history, f, ensure_ascii=False, indent=2)
    
    def load_whitelist(self):
        """Lade Whitelist"""
        if self.whitelist_file.exists():
            with open(self.whitelist_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {
            "apps": ["moloch", "keepass", "bitwarden"],
            "patterns": ["moloch", "password"]
        }
    
    def get_clipboard_text(self):
        """Hole aktuellen Clipboard-Text (Termux API)"""
        try:
            # Versuche mit termux-clipboard-get
            result = subprocess.run(
                ["termux-clipboard-get"],
                capture_output=True,
                text=True,
                timeout=5
            )

            if result.returncode == 0:
                return result.stdout.strip()

            # Fallback: Versuche xclip/xsel
            for cmd in ["xclip -selection clipboard -o", "xsel -b"]:
                try:
                    result = subprocess.run(
                        cmd.split(),
                        capture_output=True,
                        text=True,
                        timeout=5
                    )
                    if result.returncode == 0:
                        return result.stdout.strip()
                except:
                    pass

            # Windows / generic fallback: use pyperclip if installed
            try:
                import pyperclip
                text = pyperclip.paste()
                if text:
                    return text.strip()
            except Exception:
                pass
                    
        except Exception as e:
            print(f"❌ Clipboard Fehler: {e}")
        
        return None
    
    def set_clipboard_text(self, text):
        """Setze Clipboard-Text"""
        try:
            # Versuche mit termux-clipboard-set
            subprocess.run(
                ["termux-clipboard-set"],
                input=text,
                text=True,
                timeout=5
            )
        except Exception as e:
            # Fallback to pyperclip on desktop/Windows
            try:
                import pyperclip
                pyperclip.copy(text)
            except Exception:
                print(f"❌ Clipboard Set Fehler: {e}")
    
    def analyze_content(self, text):
        """Analysiere Clipboard-Inhalt und erkenne Typ"""
        if not text or len(text) < self.config["filters"]["min_length"]:
            return None
        
        analysis = {
            "type": "text",
            "subtype": [],
            "content": text,
            "timestamp": datetime.now().isoformat(),
            "length": len(text),
            "language": "unknown"
        }
        
        # URL-Erkennung
        url_pattern = r'https?://[^\s]+'
        if re.search(url_pattern, text):
            analysis["type"] = "link"
            analysis["subtype"].append("url")
            urls = re.findall(url_pattern, text)
            analysis["urls"] = urls
        
        # Email-Erkennung
        email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        if re.search(email_pattern, text):
            analysis["subtype"].append("email")
            analysis["emails"] = re.findall(email_pattern, text)
        
        # Telefon-Erkennung
        phone_pattern = r'\+?[0-9\s\-()]{7,}'
        if re.search(phone_pattern, text):
            analysis["subtype"].append("phone")
            analysis["phones"] = re.findall(phone_pattern, text)
        
        # Code-Erkennung
        code_indicators = ["import ", "def ", "class ", "function ", "=>", "const "]
        if any(ind in text for ind in code_indicators):
            analysis["subtype"].append("code")
        
        # Markdown-Erkennung
        markdown_indicators = ["# ", "## ", "- ", "* ", "[", "]", "```"]
        if any(ind in text for ind in markdown_indicators):
            analysis["subtype"].append("markdown")
        
        # JSON-Erkennung
        try:
            json.loads(text)
            analysis["subtype"].append("json")
        except:
            pass
        
        # Sprache erkennen (einfach)
        if any(ord(c) > 127 for c in text):
            analysis["language"] = "multi-byte"
        
        return analysis
    
    def should_filter(self, text, analysis):
        """Prüfe ob Text gefiltert werden sollte"""
        filters = self.config["filters"]
        
        # Länge prüfen
        if len(text) < filters["min_length"] or len(text) > filters["max_length"]:
            return True
        
        # Muster prüfen
        for pattern in filters.get("ignore_patterns", []):
            if re.match(pattern, text):
                return True
        
        # Duplikate ignorieren?
        if filters.get("ignore_duplicates"):
            if self.last_hash == hashlib.md5(text.encode()).hexdigest():
                return True
        
        return False
    
    def process_link(self, urls):
        """Verarbeite erkannte Links"""
        print(f"🔗 {len(urls)} Link(s) erkannt!")
        for url in urls:
            print(f"  → {url}")
            
            # Könnte hier automatisch öffnen, aber Sicherheit zuerst!
            # subprocess.run(["am", "start", "-a", "android.intent.action.VIEW", "-d", url])
            
            return {
                "action": "link_detected",
                "urls": urls,
                "suggested": "Am besten manuell öffnen!"
            }
    
    def process_email(self, emails):
        """Verarbeite erkannte Emails"""
        print(f"📧 {len(emails)} Email(s) erkannt!")
        for email in emails:
            print(f"  → {email}")
        
        return {
            "action": "email_detected",
            "emails": emails
        }
    
    def process_phone(self, phones):
        """Verarbeite erkannte Telefonnummern"""
        print(f"☎️  {len(phones)} Telefonnummer(n) erkannt!")
        for phone in phones:
            print(f"  → {phone}")
        
        return {
            "action": "phone_detected",
            "phones": phones
        }
    
    def process_code(self, content):
        """Verarbeite erkannte Code"""
        print(f"💻 Code erkannt! ({len(content)} Zeichen)")
        
        # Könnte Code syntax-highlighting hinzufügen
        lines = content.split('\n')
        print(f"  📝 {len(lines)} Zeilen Code")
        
        return {
            "action": "code_detected",
            "lines": len(lines),
            "stored": True
        }
    
    def add_to_history(self, analysis):
        """Füge zu History hinzu"""
        entry = {
            "timestamp": analysis["timestamp"],
            "type": analysis["type"],
            "subtype": analysis["subtype"],
            "length": analysis["length"],
            "preview": analysis["content"][:100],
            "action": "stored"
        }
        
        self.history.append(entry)
        self.save_history()
    
    def process_clipboard(self, text):
        """Verarbeite Clipboard-Text"""
        if not text:
            return None
        
        # Analysiere
        analysis = self.analyze_content(text)
        if not analysis:
            return None
        
        # Filtere
        if self.should_filter(text, analysis):
            return None
        
        # Aktualisiere Hash
        self.last_hash = hashlib.md5(text.encode()).hexdigest()
        
        # Spreche Erkenntnisse
        if self.config["integrations"]["speak"]:
            self.speak_detection(analysis)
        
        # Verarbeite je nach Typ
        result = None
        if "url" in analysis.get("subtype", []):
            result = self.process_link(analysis.get("urls", []))
        elif "email" in analysis.get("subtype", []):
            result = self.process_email(analysis.get("emails", []))
        elif "phone" in analysis.get("subtype", []):
            result = self.process_phone(analysis.get("phones", []))
        elif "code" in analysis.get("subtype", []):
            result = self.process_code(text)
        
        # Speichere in History
        if self.config["integrations"]["log"]:
            self.add_to_history(analysis)
        
        return result
    
    def speak_detection(self, analysis):
        """Spreche Erkennung an"""
        try:
            msg_map = {
                "url": f"Link erkannt!",
                "email": f"Email-Adresse in der Zwischenablage",
                "phone": f"Telefonnummer erkannt",
                "code": f"Code-Fragment erkannt",
                "markdown": f"Markdown-Text erkannt"
            }
            
            for subtype in analysis.get("subtype", []):
                msg = msg_map.get(subtype)
                if msg:
                    # Könnte hier speak() aufrufen wenn verfügbar
                    print(f"🔊 {msg}")
                    break
        except:
            pass
    
    def daemon_loop(self, interval=3, max_iterations=None):
        """Kontinuierliche Überwachung"""
        print(f"\n🔄 Clipboard Monitor Daemon startet...")
        print(f"   Prüfintervall: {interval}s")
        print(f"   Zum Beenden: Ctrl+C\n")
        
        iteration = 0
        while not self.stop_daemon.is_set():
            try:
                iteration += 1
                
                # Hole Clipboard
                clipboard_text = self.get_clipboard_text()
                
                # Wenn neu, verarbeite
                if clipboard_text and clipboard_text != self.last_clipboard:
                    self.last_clipboard = clipboard_text
                    result = self.process_clipboard(clipboard_text)
                    
                    if result:
                        print(f"✅ Verarbeitet: {result.get('action', 'unknown')}")
                
                # Beende nach N Iterationen?
                if max_iterations and iteration >= max_iterations:
                    break
                
                time.sleep(interval)
                
            except KeyboardInterrupt:
                print("\n\n⏹  Daemon gestoppt!")
                break
            except Exception as e:
                print(f"❌ Daemon Fehler: {e}")
                time.sleep(interval)
    
    def start_daemon(self, interval=3):
        """Starte Daemon im Background Thread"""
        thread = Thread(target=self.daemon_loop, args=(interval,), daemon=True)
        thread.start()
        return thread
    
    def get_history(self, limit=10):
        """Hole letzte History-Einträge"""
        return self.history[-limit:]
    
    def clear_history(self):
        """Lösche History"""
        self.history = []
        self.save_history()
        print("🗑️  Clipboard-History gelöscht")
    
    def get_stats(self):
        """Gebe Statistiken aus"""
        stats = {
            "total_items": len(self.history),
            "types": defaultdict(int),
            "subtypes": defaultdict(int),
            "avg_length": 0
        }
        
        if self.history:
            total_length = 0
            for entry in self.history:
                stats["types"][entry.get("type", "unknown")] += 1
                total_length += entry.get("length", 0)
                
                for subtype in entry.get("subtype", []):
                    stats["subtypes"][subtype] += 1
            
            stats["avg_length"] = int(total_length / len(self.history))
        
        return stats
    
    def display_dashboard(self):
        """Zeige Dashboard"""
        print("\n" + "="*60)
        print("📋 CLIPBOARD MONITOR DASHBOARD")
        print("="*60)
        
        stats = self.get_stats()
        print(f"\n📊 Statistiken:")
        print(f"   Total Items: {stats['total_items']}")
        print(f"   Avg Länge: {stats['avg_length']} Zeichen")
        
        if stats['types']:
            print(f"\n   Typen:")
            for typ, count in sorted(stats['types'].items()):
                print(f"     • {typ}: {count}")
        
        if stats['subtypes']:
            print(f"\n   Subtypen:")
            for subtype, count in sorted(stats['subtypes'].items()):
                print(f"     • {subtype}: {count}")
        
        recent = self.get_history(5)
        if recent:
            print(f"\n📝 Letzte Einträge:")
            for entry in recent:
                print(f"   [{entry['timestamp'][:10]}] {entry['type']}")
                print(f"     → {entry['preview'][:60]}")
        
        print("\n" + "="*60)


def main():
    """CLI Interface"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Clipboard Monitor für M.O.L.O.C.H.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Beispiele:
  python clipboard_monitor.py daemon          # Starte Daemon
  python clipboard_monitor.py history         # Zeige History
  python clipboard_monitor.py stats           # Statistiken
  python clipboard_monitor.py clear           # Lösche History
  python clipboard_monitor.py dashboard       # Dashboard
        """
    )
    
    parser.add_argument(
        "command",
        choices=["daemon", "history", "stats", "clear", "dashboard", "test"],
        help="Befehl zum Ausführen"
    )
    
    parser.add_argument(
        "-i", "--interval",
        type=int,
        default=3,
        help="Prüf-Intervall in Sekunden (default: 3)"
    )
    
    parser.add_argument(
        "-n", "--number",
        type=int,
        default=10,
        help="Anzahl der Einträge (default: 10)"
    )
    
    args = parser.parse_args()
    
    monitor = ClipboardMonitor()
    
    if args.command == "daemon":
        print(f"\n🎯 Starte Clipboard Monitor Daemon...")
        monitor.daemon_loop(interval=args.interval)
    
    elif args.command == "history":
        history = monitor.get_history(args.number)
        print(f"\n📋 Letzte {len(history)} Einträge:")
        for i, entry in enumerate(history, 1):
            print(f"\n{i}. [{entry['timestamp']}]")
            print(f"   Typ: {entry['type']} ({', '.join(entry['subtype'])})")
            print(f"   Länge: {entry['length']} Zeichen")
            print(f"   Preview: {entry['preview'][:80]}")
    
    elif args.command == "stats":
        stats = monitor.get_stats()
        print(f"\n📊 Statistiken:")
        print(f"   Total: {stats['total_items']}")
        print(f"   Avg Länge: {stats['avg_length']}")
        if stats['types']:
            print(f"   Typen: {dict(stats['types'])}")
        if stats['subtypes']:
            print(f"   Subtypen: {dict(stats['subtypes'])}")
    
    elif args.command == "clear":
        monitor.clear_history()
    
    elif args.command == "dashboard":
        monitor.display_dashboard()
    
    elif args.command == "test":
        print("🧪 Test Mode...")
        test_texts = [
            "Check this out: https://example.com/page?param=value",
            "Contact me: support@example.com",
            "Call me: +49 123 456789",
            "def hello():\n    print('world')",
            "# Markdown\n## Header\n- List item"
        ]
        
        for text in test_texts:
            print(f"\n📋 Testing: {text[:50]}")
            analysis = monitor.analyze_content(text)
            if analysis:
                print(f"   Type: {analysis['type']}")
                print(f"   Subtypes: {analysis['subtype']}")


if __name__ == "__main__":
    main()
