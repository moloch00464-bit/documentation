#!/usr/bin/env python3
"""
Camera OCR & Screenshot Analyse für M.O.L.O.C.H.
Lese Text von Bildern, Screens, analysiere Inhalte

Requires: pytesseract, PIL
  pip install pytesseract pillow

Optional: pytesseract braucht Tesseract System Binary
  Android/Termux: pkg install tesseract
  Desktop: choco install tesseract

Usage:
  python camera_ocr.py --screenshot       # Mache Screenshot & OCR
  python camera_ocr.py --camera           # Kamera & OCR (real-time)
  python camera_ocr.py --file <path>      # OCR auf Datei
  python camera_ocr.py --analyze <path>   # Screenshot analysieren
  python camera_ocr.py --daemon           # Continuous monitoring
"""

import os
import sys
import json
import time
import subprocess
from datetime import datetime
from pathlib import Path

try:
    import pytesseract
    from PIL import Image
    import numpy as np
    TESSERACT_AVAILABLE = True
except ImportError:
    TESSERACT_AVAILABLE = False

# Config
OCR_CONFIG = os.path.expanduser("~/moloch/ocr_config.json")
OCR_DIR = os.path.expanduser("~/moloch/ocr_cache")
os.makedirs(OCR_DIR, exist_ok=True)

class CameraOCR:
    def __init__(self):
        self.config = self.load_config()
    
    def load_config(self):
        """Lade OCR Config."""
        if os.path.exists(OCR_CONFIG):
            try:
                with open(OCR_CONFIG, 'r') as f:
                    return json.load(f)
            except:
                pass
        
        config = {
            "tesseract_enabled": TESSERACT_AVAILABLE,
            "ocr_language": "eng+deu",  # English + Deutsch
            "min_confidence": 0.3,
            "cache_screenshots": True,
            "auto_analyze": True
        }
        
        self.save_config(config)
        return config
    
    def save_config(self, config=None):
        """Speichere OCR Config."""
        if config is None:
            config = self.config
        
        os.makedirs(os.path.dirname(OCR_CONFIG), exist_ok=True)
        with open(OCR_CONFIG, 'w') as f:
            json.dump(config, f, indent=2)
    
    def take_screenshot(self):
        """Mache Screenshot."""
        print("📷 Mache Screenshot...")
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = os.path.join(OCR_DIR, f"screenshot_{timestamp}.png")
        
        try:
            # Termux: screencap
            result = subprocess.run(
                ["screencap", "-p", screenshot_path],
                timeout=5,
                check=False
            )
            
            if result.returncode == 0 and os.path.exists(screenshot_path):
                print(f"✅ Screenshot: {screenshot_path}")
                return screenshot_path
            
            # Fallback: adb (falls verfügbar)
            try:
                subprocess.run(
                    ["adb", "shell", "screencap", "-p", "/sdcard/screen.png"],
                    timeout=5,
                    check=False
                )
                subprocess.run(
                    ["adb", "pull", "/sdcard/screen.png", screenshot_path],
                    timeout=5,
                    check=False
                )
                
                if os.path.exists(screenshot_path):
                    print(f"✅ Screenshot (via ADB): {screenshot_path}")
                    return screenshot_path
            
            except:
                pass
            
            print("❌ Screenshot fehlgeschlagen")
            return None
        
        except Exception as e:
            print(f"❌ Screenshot Error: {e}")
            return None
    
    def extract_text(self, image_path: str):
        """Extrahiere Text via OCR."""
        if not TESSERACT_AVAILABLE:
            print("❌ pytesseract nicht installiert")
            print("   pip install pytesseract pillow")
            return None
        
        print(f"🔍 Führe OCR durch: {image_path}")
        
        try:
            # Lade Bild
            image = Image.open(image_path)
            
            # Optionale Vorverarbeitung
            # image = image.convert('L')  # Graustufen
            # image = image.point(lambda x: 0 if x < 128 else 255, '1')  # Binary
            
            # OCR
            text = pytesseract.image_to_string(
                image,
                lang=self.config.get("ocr_language", "eng+deu")
            )
            
            if text.strip():
                print(f"✅ Text extrahiert ({len(text)} chars)")
                return text.strip()
            else:
                print("⚠️ Kein Text gefunden")
                return None
        
        except Exception as e:
            print(f"❌ OCR Error: {e}")
            return None
    
    def analyze_text(self, text: str):
        """Analysiere extrahierten Text mit Claude."""
        if not text:
            return None
        
        print("💭 Analysiere Text mit Claude...")
        
        try:
            sys.path.insert(0, os.path.expanduser("~/moloch"))
            from moloch import ask_claude, speak, auto_brain_save_genesis
            
            analysis_prompt = f"""Analysiere diesen gescannten Text prägnant:

TEXT:
{text[:1000]}

Gebe kurz wieder:
1. Hauptthema/Inhalt
2. Wichtige Punkte
3. Notwendige Aktionen (falls vorhanden)
"""
            
            analysis = ask_claude(analysis_prompt)
            
            # Spreche Zusammenfassung
            speak(f"Text analysiert. {analysis[:300]}")
            
            # Speichere in Brain
            auto_brain_save_genesis({
                "type": "ocr_analysis",
                "text_length": len(text),
                "analysis": analysis,
                "timestamp": datetime.now().isoformat()
            })
            
            print(f"✅ Analyse: {analysis[:150]}...\n")
            return analysis
        
        except Exception as e:
            print(f"❌ Analysis Error: {e}")
            return None
    
    def process_screenshot(self):
        """Mache Screenshot, OCR, & Analyse."""
        print("\n🎬 Screenshot-Analyse Pipeline\n")
        
        # Screenshot
        screenshot_path = self.take_screenshot()
        if not screenshot_path:
            return None
        
        # OCR
        text = self.extract_text(screenshot_path)
        if not text:
            print("⚠️ Kein Text extrahiert")
            return None
        
        print(f"\n📝 Extrahierter Text:\n{text[:200]}...\n")
        
        # Analyse
        analysis = self.analyze_text(text)
        
        return {
            "screenshot": screenshot_path,
            "text": text,
            "analysis": analysis
        }
    
    def process_file(self, filepath: str):
        """Verarbeite Datei (OCR + Analyse)."""
        if not os.path.exists(filepath):
            print(f"❌ Datei nicht gefunden: {filepath}")
            return None
        
        print(f"\n📄 Verarbeite Datei: {filepath}\n")
        
        # OCR
        text = self.extract_text(filepath)
        if not text:
            return None
        
        print(f"\n📝 Extrahierter Text:\n{text[:300]}...\n")
        
        # Analyse
        analysis = self.analyze_text(text)
        
        return {
            "file": filepath,
            "text": text,
            "analysis": analysis
        }
    
    def camera_realtime(self, interval: int = 5):
        """Real-Time Kamera Monitoring mit OCR."""
        try:
            import cv2
            OPENCV_AVAILABLE = True
        except ImportError:
            print("❌ OpenCV nicht verfügbar")
            print("   pip install opencv-python")
            return
        
        print("🎥 Real-Time Camera OCR")
        print("   Drücke 'q' zum Beenden, 'c' für Screenshot")
        
        try:
            cap = cv2.VideoCapture(0)
            
            if not cap.isOpened():
                print("❌ Kamera kann nicht geöffnet werden")
                return
            
            frame_count = 0
            
            while True:
                ret, frame = cap.read()
                
                if not ret:
                    break
                
                # Zeige Frame
                cv2.imshow('M.O.L.O.C.H. Camera OCR', frame)
                
                # Periodische OCR
                frame_count += 1
                if frame_count % (30 * interval) == 0:  # Alle 5s bei 30 FPS
                    print("🔄 OCR Update...")
                    # Speichere Frame
                    temp_path = os.path.join(OCR_DIR, "temp_frame.png")
                    cv2.imwrite(temp_path, frame)
                    
                    # OCR
                    text = self.extract_text(temp_path)
                    if text:
                        print(f"📝 Text: {text[:100]}...")
                
                # Key handling
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    break
                elif key == ord('c'):
                    print("📷 Screenshot...")
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    save_path = os.path.join(OCR_DIR, f"camera_{timestamp}.png")
                    cv2.imwrite(save_path, frame)
                    print(f"✅ Gespeichert: {save_path}")
            
            cap.release()
            cv2.destroyAllWindows()
        
        except Exception as e:
            print(f"❌ Camera Error: {e}")
    
    def daemon_mode(self, interval: int = 60):
        """Hintergrund-Daemon für OCR Monitoring."""
        print(f"🤖 OCR Daemon gestartet (Interval: {interval}s)")
        
        try:
            while True:
                print(f"\n⏰ {datetime.now().isoformat()}")
                
                screenshot_path = self.take_screenshot()
                if screenshot_path:
                    text = self.extract_text(screenshot_path)
                    if text:
                        # Nur analysieren wenn interessant
                        word_count = len(text.split())
                        if word_count > 10:  # Min. 10 Wörter
                            self.analyze_text(text)
                
                time.sleep(interval)
        
        except KeyboardInterrupt:
            print("\n⛔ OCR Daemon gestoppt")

if __name__ == "__main__":
    ocr = CameraOCR()
    
    if not TESSERACT_AVAILABLE:
        print("⚠️ Tesseract nicht verfügbar!")
        print("   Installiere: pip install pytesseract pillow")
    
    if len(sys.argv) < 2:
        print(__doc__)
    
    elif sys.argv[1] == "--screenshot":
        ocr.process_screenshot()
    
    elif sys.argv[1] == "--camera":
        ocr.camera_realtime()
    
    elif sys.argv[1] == "--file":
        if len(sys.argv) > 2:
            filepath = " ".join(sys.argv[2:])
            ocr.process_file(filepath)
    
    elif sys.argv[1] == "--analyze":
        if len(sys.argv) > 2:
            filepath = " ".join(sys.argv[2:])
            ocr.process_file(filepath)
    
    elif sys.argv[1] == "--daemon":
        interval = int(sys.argv[2]) if len(sys.argv) > 2 else 60
        ocr.daemon_mode(interval)
    
    else:
        print(__doc__)
