#!/usr/bin/env python3
"""
DGM Vision System - Face Recognition für M.O.L.O.C.H.
Verwaltung von bekannten Gesichtern (Markus, Kollegen)

Usage:
  python face_manager.py register <name> <image_path>    # Registriere Gesicht
  python face_manager.py list                             # Zeige bekannte Gesichter
  python face_manager.py delete <name>                    # Lösche Gesicht
  python face_manager.py test <image_path>                # Teste Erkennung
"""

import os
import sys
import json
import face_recognition
import numpy as np
from PIL import Image
import pickle

# Config
FACES_DIR = os.path.expanduser("~/moloch/faces")
FACES_DB = os.path.expanduser("~/moloch/faces_database.pkl")

def ensure_faces_dir():
    """Erstelle faces Verzeichnis."""
    os.makedirs(FACES_DIR, exist_ok=True)

def load_face_database():
    """Lade bekannte Gesichter aus Datenbank."""
    if os.path.exists(FACES_DB):
        try:
            with open(FACES_DB, 'rb') as f:
                return pickle.load(f)
        except:
            pass
    return {"names": [], "encodings": []}

def save_face_database(db):
    """Speichere Gesichter-Datenbank."""
    with open(FACES_DB, 'wb') as f:
        pickle.dump(db, f)

def register_face(name, image_path):
    """Registriere ein neues Gesicht."""
    ensure_faces_dir()
    
    if not os.path.exists(image_path):
        print(f"❌ Bild nicht gefunden: {image_path}")
        return False
    
    try:
        # Lade Bild
        image = face_recognition.load_image_file(image_path)
        face_encodings = face_recognition.face_encodings(image)
        
        if not face_encodings:
            print(f"❌ Kein Gesicht in {image_path} erkannt")
            return False
        
        if len(face_encodings) > 1:
            print(f"⚠️ Mehrere Gesichter gefunden, nutze das erste")
        
        # Speichere Encoding
        db = load_face_database()
        
        # Überprüfe Duplikate
        if name in db["names"]:
            idx = db["names"].index(name)
            db["encodings"][idx] = face_encodings[0]
            print(f"♻️ {name} aktualisiert")
        else:
            db["names"].append(name)
            db["encodings"].append(face_encodings[0])
            print(f"✅ {name} registriert")
        
        save_face_database(db)
        
        # Speichere auch Bild als Backup
        img_backup = os.path.join(FACES_DIR, f"{name}.jpg")
        Image.open(image_path).save(img_backup)
        print(f"📸 Bild gespeichert: {img_backup}")
        
        return True
    
    except Exception as e:
        print(f"❌ Fehler: {e}")
        return False

def list_faces():
    """Liste alle bekannten Gesichter."""
    db = load_face_database()
    if not db["names"]:
        print("📭 Keine bekannten Gesichter")
        return
    
    print("\n🎭 Bekannte Gesichter:")
    for i, name in enumerate(db["names"]):
        backup_path = os.path.join(FACES_DIR, f"{name}.jpg")
        exists = "✅" if os.path.exists(backup_path) else "❌"
        print(f"  {i+1}. {name} {exists}")
    print()

def delete_face(name):
    """Lösche ein Gesicht."""
    db = load_face_database()
    
    if name not in db["names"]:
        print(f"❌ {name} nicht gefunden")
        return False
    
    idx = db["names"].index(name)
    db["names"].pop(idx)
    db["encodings"].pop(idx)
    save_face_database(db)
    
    # Lösche auch Backup-Bild
    img_backup = os.path.join(FACES_DIR, f"{name}.jpg")
    if os.path.exists(img_backup):
        os.remove(img_backup)
    
    print(f"🗑️ {name} gelöscht")
    return True

def recognize_faces(image_path, tolerance=0.6):
    """Erkenne Gesichter in einem Bild."""
    if not os.path.exists(image_path):
        print(f"❌ Bild nicht gefunden: {image_path}")
        return []
    
    try:
        db = load_face_database()
        if not db["names"]:
            print("❌ Keine bekannten Gesichter in Datenbank")
            return []
        
        # Lade Test-Bild
        test_image = face_recognition.load_image_file(image_path)
        test_encodings = face_recognition.face_encodings(test_image)
        
        if not test_encodings:
            print("⚠️ Kein Gesicht im Bild erkannt")
            return []
        
        results = []
        for test_encoding in test_encodings:
            # Vergleiche mit bekannten Gesichtern
            distances = face_recognition.face_distance(db["encodings"], test_encoding)
            best_match_idx = np.argmin(distances)
            best_distance = distances[best_match_idx]
            
            if best_distance < tolerance:
                name = db["names"][best_match_idx]
                confidence = 1 - best_distance
                results.append({"name": name, "confidence": confidence})
                print(f"✅ {name} erkannt (Sicherheit: {confidence:.1%})")
            else:
                results.append({"name": "UNKNOWN", "confidence": 0})
                print(f"❓ Unbekannte Person (Distanz: {best_distance:.2f})")
        
        return results
    
    except Exception as e:
        print(f"❌ Fehler: {e}")
        return []

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    
    cmd = sys.argv[1].lower()
    
    if cmd == "register" and len(sys.argv) >= 4:
        register_face(sys.argv[2], sys.argv[3])
    elif cmd == "list":
        list_faces()
    elif cmd == "delete" and len(sys.argv) >= 3:
        delete_face(sys.argv[2])
    elif cmd == "test" and len(sys.argv) >= 3:
        recognize_faces(sys.argv[2])
    else:
        print(__doc__)
