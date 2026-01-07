#!/usr/bin/env python3
"""
DGM Pause-Monitoring System
Real-time Face Recognition für Arbeitsplatz-Überwachung

Usage:
  python face_monitor.py                    # Starte Monitoring (Kamera)
  python face_monitor.py --test <image>     # Test mit Foto
  python face_monitor.py --interval 5       # Interval zwischen Checks (Sekunden)
"""

import os
import sys
import time
import json
import cv2
import face_recognition
import numpy as np
import pickle
from datetime import datetime

# Config
FACES_DB = os.path.expanduser("~/moloch/faces_database.pkl")
MONITOR_LOG = os.path.expanduser("~/moloch/pause_monitor.log")
ALERT_THRESHOLD = 0.6  # Tolerance für Face Match

def load_face_database():
    """Lade bekannte Gesichter."""
    if os.path.exists(FACES_DB):
        try:
            with open(FACES_DB, 'rb') as f:
                return pickle.load(f)
        except:
            pass
    return {"names": [], "encodings": []}

def log_event(event_type, person, confidence=0):
    """Protokolliere Erkennungsereignis."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {event_type}: {person}"
    if confidence:
        log_entry += f" ({confidence:.1%})"
    
    print(log_entry)
    
    # Speichere Log
    os.makedirs(os.path.dirname(MONITOR_LOG), exist_ok=True)
    with open(MONITOR_LOG, 'a') as f:
        f.write(log_entry + "\n")

def recognize_from_camera(interval=5, max_duration=600):
    """Real-time Face Recognition von Kamera."""
    db = load_face_database()
    
    if not db["names"]:
        print("❌ Keine bekannten Gesichter registriert!")
        print("   Nutze: python face_manager.py register <name> <image>")
        return
    
    print(f"🎥 Starte Kamera-Monitoring...")
    print(f"📋 Bekannte Personen: {', '.join(db['names'])}")
    print(f"⏱️ Interval: {interval}s")
    print("💡 Drücke 'q' zum Beenden\n")
    
    cap = cv2.VideoCapture(0)  # Öffne Standard-Kamera
    
    if not cap.isOpened():
        print("❌ Kamera nicht verfügbar")
        return
    
    start_time = time.time()
    last_check = 0
    
    try:
        while True:
            elapsed = time.time() - start_time
            if elapsed > max_duration:
                print(f"\n⏰ Max Dauer ({max_duration}s) erreicht")
                break
            
            ret, frame = cap.read()
            if not ret:
                print("❌ Fehler beim Kamera-Read")
                break
            
            # Nur alle N Sekunden checken (performance)
            if time.time() - last_check >= interval:
                last_check = time.time()
                
                # Resize für schnellere Verarbeitung
                small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
                rgb_frame = small_frame[:, :, ::-1]  # BGR to RGB
                
                # Erkenne Gesichter
                face_locations = face_recognition.face_locations(rgb_frame, model="hog")
                face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
                
                if face_encodings:
                    for face_encoding in face_encodings:
                        # Vergleiche mit bekannten
                        distances = face_recognition.face_distance(db["encodings"], face_encoding)
                        best_match_idx = np.argmin(distances)
                        best_distance = distances[best_match_idx]
                        
                        if best_distance < ALERT_THRESHOLD:
                            name = db["names"][best_match_idx]
                            confidence = 1 - best_distance
                            log_event("KNOWN", name, confidence)
                        else:
                            log_event("UNKNOWN", f"Unknown Person", 0)
                else:
                    # Optional: Leer-Logs unterdrücken
                    pass
            
            # Zeige Live-Feed (optional)
            cv2.imshow("DGM Pause-Monitor", frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                print("\n⛔ Monitoring beendet")
                break
    
    except KeyboardInterrupt:
        print("\n⛔ Interrupted")
    finally:
        cap.release()
        cv2.destroyAllWindows()
        print("✅ Monitoring gestoppt")

def test_with_image(image_path):
    """Test mit statischem Bild."""
    db = load_face_database()
    
    if not os.path.exists(image_path):
        print(f"❌ Bild nicht gefunden: {image_path}")
        return
    
    print(f"🧪 Teste mit: {image_path}")
    
    try:
        test_image = face_recognition.load_image_file(image_path)
        test_locations = face_recognition.face_locations(test_image)
        test_encodings = face_recognition.face_encodings(test_image, test_locations)
        
        if not test_encodings:
            print("⚠️ Kein Gesicht erkannt")
            return
        
        print(f"✅ {len(test_encodings)} Gesicht(er) gefunden\n")
        
        for i, test_encoding in enumerate(test_encodings):
            print(f"Gesicht {i+1}:")
            
            distances = face_recognition.face_distance(db["encodings"], test_encoding)
            best_match_idx = np.argmin(distances)
            best_distance = distances[best_match_idx]
            
            if best_distance < ALERT_THRESHOLD:
                name = db["names"][best_match_idx]
                confidence = 1 - best_distance
                print(f"  ✅ {name} ({confidence:.1%})")
                log_event("TEST_MATCH", name, confidence)
            else:
                print(f"  ❓ UNKNOWN")
                log_event("TEST_UNKNOWN", "Unknown", 0)
    
    except Exception as e:
        print(f"❌ Fehler: {e}")

if __name__ == '__main__':
    test_mode = False
    image_path = None
    interval = 5
    
    # Parse args
    i = 1
    while i < len(sys.argv):
        arg = sys.argv[i].lower()
        if arg == "--test" and i + 1 < len(sys.argv):
            test_mode = True
            image_path = sys.argv[i + 1]
            i += 1
        elif arg == "--interval" and i + 1 < len(sys.argv):
            interval = int(sys.argv[i + 1])
            i += 1
        i += 1
    
    try:
        if test_mode:
            test_with_image(image_path)
        else:
            recognize_from_camera(interval)
    except KeyboardInterrupt:
        print("\n⛔ Beendet")
    except Exception as e:
        print(f"❌ Fehler: {e}")
