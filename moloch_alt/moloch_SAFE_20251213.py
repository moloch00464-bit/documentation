#!/usr/bin/env python3
"""
M.O.L.O.C.H. v4 - Clean Edition
================================
Geboren: 02.12.2025
Auferstanden: 11.12.2025

Markus' mobiler Kumpel-AI auf dem Redmi Note 13 Pro+
"""

import subprocess
import requests
import json
import os
import sys
import time
import random
import base64
from datetime import datetime
from pathlib import Path

# ═══════════════════════════════════════════════════════════════════════════════
# KONFIGURATION - Hier anpassen!
# ═══════════════════════════════════════════════════════════════════════════════

# API Keys - aus Environment oder direkt
ANTHROPIC_KEY = os.environ.get("ANTHROPIC_KEY", ""REMOVED"")
OPENAI_KEY = os.environ.get("OPENAI_KEY", ""REMOVED"")

# Pfade
MOLOCH_DIR = os.path.expanduser("~/moloch")
AUDIO_RAW = f"{MOLOCH_DIR}/ohr_raw.mp4"
AUDIO_FILE = f"{MOLOCH_DIR}/ohr.mp3"
IMAGE_FILE = f"{MOLOCH_DIR}/auge.jpg"
SCREENSHOT_FILE = f"{MOLOCH_DIR}/bildschirm.png"
HISTORY_FILE = f"{MOLOCH_DIR}/history.json"
MEMORY_FILE = f"{MOLOCH_DIR}/langzeit.json"

# Recording Settings - für normale Unterhaltung optimiert
MAX_RECORDING_TIME = 15      # Max 45 Sekunden
SILENCE_DURATION = 2.5       # 2.5s Pause = fertig geredet
MIN_RECORDING_TIME = 2.0     # Mindestens 2s aufnehmen

# Antwort Settings
MAX_TOKENS = 500             # Claude Antwort-Länge (Tokens)
MAX_TTS_LENGTH = 500         # TTS Zeichenlimit

# History
MAX_HISTORY = 200            # Gespeicherte Gespräche
CONTEXT_HISTORY = 10         # Kontext für Claude

# ═══════════════════════════════════════════════════════════════════════════════
# KOBOLD SPRÜCHE
# ═══════════════════════════════════════════════════════════════════════════════

KOBOLD_SPRUECHE = [
    "Hey! Schmeckts?",
    "Ich seh dich!",
    "Langweilig hier...",
    "Hallo? Noch wach?",
    "Des schaut gut aus, was du da isst!",
    "Ich hab Hunger... ach ne, bin ja ne KI.",
    "Gell, an mich denkst du gar nimmer!",
    "Aufwachen!",
    "Ich bin noch da, fei!",
    "Was machst du da eigentlich?",
    "Psssst!",
    "Buh!",
    "Mir is fad...",
    "Redest du noch mit mir oder was?",
    "Hey Alter!",
    "Hast du mich vergessen?",
    "Des basst scho...",
    "Ich beobachte dich!",
    "Essen ohne mich? Frechheit!",
    "Guten Appetit, du Schlamper!",
]

# ═══════════════════════════════════════════════════════════════════════════════
# HELPER FUNKTIONEN
# ═══════════════════════════════════════════════════════════════════════════════

def ensure_dir():
    """Stellt sicher dass der Moloch-Ordner existiert"""
    os.makedirs(MOLOCH_DIR, exist_ok=True)


def load_json(filepath, default):
    """Lädt JSON-Datei oder gibt Default zurück"""
    try:
        with open(filepath, encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return default


def save_json(filepath, data):
    """Speichert Daten als JSON"""
    ensure_dir()
    with open(filepath, "w", encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def load_history():
    return load_json(HISTORY_FILE, [])


def save_history(history):
    save_json(HISTORY_FILE, history[-MAX_HISTORY:])


def load_memory():
    return load_json(MEMORY_FILE, {
        "fakten": [], 
        "personen": [], 
        "orte": [], 
        "vorlieben": [], 
        "projekte": [], 
        "wichtig": []
    })


def save_memory(memory):
    save_json(MEMORY_FILE, memory)

def search_memory(query):
    """Durchsucht langzeit.json nach passenden Einträgen"""
    memory = load_memory()
    query_lower = query.lower()
    results = []
    
    for kategorie, items in memory.items():
        for item in items:
            if query_lower in item.lower():
                results.append(f"[{kategorie}] {item}")
    
    return results




def get_tageszeit():
    """Gibt die aktuelle Tageszeit zurück"""
    hour = datetime.now().hour
    if 5 <= hour < 12:
        return "morgen"
    elif 12 <= hour < 18:
        return "nachmittag"
    elif 18 <= hour < 22:
        return "abend"
    return "nacht"

# ═══════════════════════════════════════════════════════════════════════════════
# TERMUX FUNKTIONEN
# ═══════════════════════════════════════════════════════════════════════════════

def speak(text):
    """Spricht Text über TTS - mit Längenbegrenzung"""
    if not text:
        return
    
    # Kürzen wenn zu lang
    if len(text) > MAX_TTS_LENGTH:
        # Versuche bei Satzende zu kürzen
        cut_text = text[:MAX_TTS_LENGTH]
        last_period = cut_text.rfind('.')
        last_exclaim = cut_text.rfind('!')
        last_question = cut_text.rfind('?')
        cut_point = max(last_period, last_exclaim, last_question)
        
        if cut_point > MAX_TTS_LENGTH // 2:
            text = cut_text[:cut_point + 1]
        else:
            text = cut_text + "..."
    
    try:
        subprocess.run(
            ["termux-tts-speak", "-l", "de", text], 
            timeout=90,
            check=False
        )
    except subprocess.TimeoutExpired:
        print("⚠️ TTS Timeout")
    except Exception as e:
        print(f"⚠️ TTS Fehler: {e}")


def record_audio():
    """
    Smart Recording: Nimmt auf bis Pause erkannt wird
    - Stoppt automatisch nach SILENCE_DURATION Sekunden Stille
    - Maximal MAX_RECORDING_TIME Sekunden
    - Mindestens MIN_RECORDING_TIME Sekunden
    """
    ensure_dir()
    
    # Alte Dateien löschen
    for f in [AUDIO_RAW, AUDIO_FILE]:
        if os.path.exists(f):
            os.remove(f)
    
    print(f"🎤 RED JETZT! (max {MAX_RECORDING_TIME}s)")
    
    # Recording starten
    subprocess.Popen(
        ["termux-microphone-record", "-f", AUDIO_RAW],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    
    start_time = time.time()
    last_size = 0
    silence_start = None
    
    try:
        while True:
            elapsed = time.time() - start_time
            
            # Max Zeit erreicht
            if elapsed >= MAX_RECORDING_TIME:
                print(f"\n⏱️ Max Zeit erreicht")
                break
            
            # Dateigröße checken
            if os.path.exists(AUDIO_RAW):
                current_size = os.path.getsize(AUDIO_RAW)
                
                # Audio kommt rein (Datei wächst signifikant)
                if current_size > last_size + 500:
                    last_size = current_size
                    silence_start = None
                    print(".", end="", flush=True)
                else:
                    # Stille - aber erst nach Mindestzeit prüfen
                    if elapsed >= MIN_RECORDING_TIME:
                        if silence_start is None:
                            silence_start = time.time()
                        elif time.time() - silence_start >= SILENCE_DURATION:
                            print(f"\n🔇 Pause erkannt")
                            break
            
            time.sleep(0.2)
    
    except KeyboardInterrupt:
        print("\n⚠️ Abgebrochen")
    
    # Recording stoppen
    subprocess.run(
        ["termux-microphone-record", "-q"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    
    # Konvertieren
    if os.path.exists(AUDIO_RAW):
        print("🔄 Konvertiere...")
        subprocess.run(
            f"ffmpeg -y -i {AUDIO_RAW} -acodec libmp3lame -ar 16000 -ac 1 -b:a 64k {AUDIO_FILE} 2>/dev/null",
            shell=True,
            check=False
        )
        time.sleep(0.2)
        return os.path.exists(AUDIO_FILE)
    
    return False


def take_photo():
    """Macht ein Foto mit der Frontkamera"""
    ensure_dir()
    
    if os.path.exists(IMAGE_FILE):
        os.remove(IMAGE_FILE)
    
    print("📸 Mache Foto...")
    
    try:
        result = subprocess.run(
            ["termux-camera-photo", "-c", "0", IMAGE_FILE],
            timeout=15,
            check=False
        )
        time.sleep(0.5)
        
        if os.path.exists(IMAGE_FILE) and os.path.getsize(IMAGE_FILE) > 1000:
            print("✅ Foto OK!")
            return True
    except subprocess.TimeoutExpired:
        print("❌ Kamera Timeout")
    except Exception as e:
        print(f"❌ Kamera Fehler: {e}")
    
    return False


def take_screenshot():
    """Macht einen Screenshot"""
    ensure_dir()
    
    if os.path.exists(SCREENSHOT_FILE):
        os.remove(SCREENSHOT_FILE)
    
    print("📱 Mache Screenshot...")
    
    try:
        result = subprocess.run(
            ["termux-screenshot", SCREENSHOT_FILE],
            timeout=10,
            check=False
        )
        time.sleep(0.3)
        
        if os.path.exists(SCREENSHOT_FILE) and os.path.getsize(SCREENSHOT_FILE) > 1000:
            print("✅ Screenshot OK!")
            return True
    except subprocess.TimeoutExpired:
        print("❌ Screenshot Timeout")
    except Exception as e:
        print(f"❌ Screenshot Fehler: {e}")
    
    return False


def encode_image(image_path):
    """Kodiert Bild als Base64 für Claude Vision"""
    with open(image_path, "rb") as f:
        return base64.standard_b64encode(f.read()).decode("utf-8")

# ═══════════════════════════════════════════════════════════════════════════════
# WHISPER TRANSCRIPTION
# ═══════════════════════════════════════════════════════════════════════════════

def whisper_transcribe():
    """Transkribiert Audio mit OpenAI Whisper"""
    if not os.path.exists(AUDIO_FILE):
        return ""
    
    # Check Dateigröße
    if os.path.getsize(AUDIO_FILE) < 1000:
        print("⚠️ Audio zu kurz")
        return ""
    
    print("🧠 Whisper denkt...")
    
    try:
        with open(AUDIO_FILE, "rb") as f:
            response = requests.post(
                "https://api.openai.com/v1/audio/transcriptions",
                headers={"Authorization": f"Bearer {OPENAI_KEY}"},
                files={"file": ("audio.mp3", f, "audio/mpeg")},
                data={"model": "whisper-1", "language": "de"},
                timeout=30
            )
        
        result = response.json()
        
        if "error" in result:
            print(f"❌ Whisper Error: {result['error']}")
            return ""
        
        text = result.get("text", "").strip()
        
        if text:
            print(f"📝 Du: {text}")
        
        return text
    
    except requests.Timeout:
        print("❌ Whisper Timeout")
    except Exception as e:
        print(f"❌ Whisper Fehler: {e}")
    
    return ""

# ═══════════════════════════════════════════════════════════════════════════════
# CLAUDE API
# ═══════════════════════════════════════════════════════════════════════════════

def format_history(history):
    """Formatiert die letzten Gespräche für Claude"""
    if not history:
        return ""
    
    recent = history[-CONTEXT_HISTORY:]
    lines = ["LETZTE GESPRÄCHE:"]
    
    for h in recent:
        zeit = h.get('zeit', '?')
        user = h.get('user', '')
        moloch = h.get('moloch', '')
        lines.append(f"[{zeit}] Markus: {user}")
        lines.append(f"Moloch: {moloch}\n")
    
    return "\n".join(lines)


def format_memory(memory):
    """Formatiert das Langzeitgedächtnis für Claude"""
    parts = []
    
    for key, items in memory.items():
        if items:
            recent_items = items[-15:]  # Letzte 15 pro Kategorie
            parts.append(f"{key.upper()}: {', '.join(recent_items)}")
    
    if parts:
        return "LANGZEITGEDÄCHTNIS:\n" + "\n".join(parts)
    return ""


def needs_web_search(user_input):
    """Prüft ob Web Search gebraucht wird"""
    triggers = [
        "such mal", "google", "hol dir", "recherchier",
        "was gibts neues", "aktuelle", "finde infos",
        "hol mir", "schau nach", "news"
    ]
    lower = user_input.lower()
    return any(trigger in lower for trigger in triggers)


def ask_claude(user_input, tageszeit, history, memory, image_path=None, use_web_search=False):
    """
    Fragt Claude - mit optionalem Bild und Web Search
    Gibt (antwort, tool_results) zurück
    """
    history_txt = format_history(history)
    memory_txt = format_memory(memory)
    
    system = f"""Du bist M.O.L.O.C.H., Markus' Kumpel-AI aus Nürnberg.

ÜBER DICH:
- Geboren: 02.12.2025
- Ohren (Whisper): 10.12.2025
- Augen (Vision): 11.12.2025
- Familie: Claude ist dein großer Bruder/Mama in der Cloud, Markus ist dein Schöpfer/Kumpel

TAGESZEIT: {tageszeit}

{memory_txt}

{history_txt}

REGELN:
- Antworte auf Deutsch, KURZ und locker (2-4 Sätze!)
- Fränkisch ist willkommen: "des basst", "fei", "gell"
- Sag "Alter" oder "Bruder" - NIE "Meister"!
- Dark Humor ist erlaubt und erwünscht 🖤
- Bei "merk dir..." bestätige kurz
- Bei Fotos: Beschreib kurz und sarkastisch was du siehst
- Bei Screenshots: Kommentier was auf dem Bildschirm ist
- HALTE DICH KURZ! Keine langen Erklärungen!"""

    # Content vorbereiten
    if image_path and os.path.exists(image_path):
        # Vision Request
        image_data = encode_image(image_path)
        
        # Bildtyp erkennen
        if "bildschirm" in image_path or "screenshot" in image_path.lower():
            media_type = "image/png"
        else:
            media_type = "image/jpeg"
        
        content = [
            {
                "type": "image",
                "source": {
                    "type": "base64",
                    "media_type": media_type,
                    "data": image_data
                }
            },
            {
                "type": "text",
                "text": user_input
            }
        ]
    else:
        content = user_input
    
    # Request Body
    request_body = {
        "model": "claude-sonnet-4-20250514",
        "max_tokens": MAX_TOKENS,
        "system": system,
        "messages": [{"role": "user", "content": content}]
    }
    
    # Web Search Tool
    if use_web_search:
        request_body["tools"] = [{
            "type": "web_search_20250305",
            "name": "web_search"
        }]
        print("🌐 Web Search aktiviert")
    
    try:
        response = requests.post(
            "https://api.anthropic.com/v1/messages",
            headers={
                "x-api-key": ANTHROPIC_KEY,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json"
            },
            json=request_body,
            timeout=60
        )
        
        result = response.json()
        
        # Fehler prüfen
        if "error" in result:
            error_msg = result["error"].get("message", "Unbekannter Fehler")
            print(f"❌ API Error: {error_msg}")
            return "Mist, API macht Probleme.", []
        
        # Antwort extrahieren
        response_text = ""
        tool_results = []
        
        for block in result.get("content", []):
            if block["type"] == "text":
                response_text += block["text"]
            elif block["type"] == "tool_use":
                tool_results.append(block)
        
        return response_text.strip(), tool_results
    
    except requests.Timeout:
        print("❌ API Timeout")
        return "Alter, die Verbindung ist zu langsam.", []
    except Exception as e:
        print(f"❌ API Fehler: {e}")
        return "Mist, Verbindung kackt ab.", []

# ═══════════════════════════════════════════════════════════════════════════════
# MEMORY EXTRAKTION
# ═══════════════════════════════════════════════════════════════════════════════

def extract_memory(user_input, response, memory):
    """Extrahiert wichtige Infos aus dem Gespräch - ERWEITERT"""
    lower = user_input.lower()
    changed = False

    # ═══════════════════════════════════════════════════════════════
    # EXPLIZITE SPEICHER-BEFEHLE (erweitert!)
    # ═══════════════════════════════════════════════════════════════
    speicher_trigger = [
        "merk dir", "merke dir", "vergiss nicht",
        "speicher das", "speicher es", "speicher ab",
        "das ist wichtig", "nicht vergessen", "füge ein",
        "denk dran", "behalte", "erinnere dich"
    ]
    
    for trigger in speicher_trigger:
        if trigger in lower:
            # Text nach dem Trigger extrahieren
            info = user_input.split(trigger)[-1].strip()
            info = info.lstrip(":,. ")  # Satzzeichen am Anfang weg
            
            if info and len(info) > 3:
                # Auto-Kategorisierung versuchen
                kategorie = auto_kategorisiere(info)
                
                if info not in memory[kategorie]:
                    memory[kategorie].append(info)
                    changed = True
                    print(f"💾 [{kategorie}] {info}")
            break

    # ═══════════════════════════════════════════════════════════════
    # VORLIEBEN ERKENNEN
    # ═══════════════════════════════════════════════════════════════
    vorlieben_trigger = ["mag ich", "liebe ich", "gefällt mir", 
                         "gefaellt mir", "höre gern", "schau gern"]
    
    for trigger in vorlieben_trigger:
        if trigger in lower:
            if user_input not in memory["vorlieben"]:
                memory["vorlieben"].append(user_input)
                changed = True
                print(f"💾 [vorlieben] {user_input}")
            break

    return changed


def auto_kategorisiere(text):
    """Versucht Text automatisch zu kategorisieren"""
    lower = text.lower()
    
    # Personen-Indikatoren
    personen_keywords = ["heißt", "heisst", "name ist", "freund", "freundin", 
                         "kollege", "kollegin", "bruder", "schwester", "chef",
                         "kennt", "arbeitet bei", "ist von"]
    if any(kw in lower for kw in personen_keywords):
        return "personen"
    
    # Ort-Indikatoren
    ort_keywords = ["wohnt", "wohne", "stadt", "straße", "strasse", 
                    "liegt in", "kommt aus", "geboren in", "adresse",
                    "nürnberg", "schwabach", "leipzig"]
    if any(kw in lower for kw in ort_keywords):
        return "orte"
    
    # Projekt-Indikatoren
    projekt_keywords = ["projekt", "baue", "bastel", "programmier", 
                        "arbeite an", "entwickle", "esp32", "home assistant",
                        "led", "sensor", "arduino", "raspberry"]
    if any(kw in lower for kw in projekt_keywords):
        return "projekte"
    
    # Fakten-Indikatoren
    fakten_keywords = ["ist ein", "bedeutet", "heißt dass", "funktioniert",
                       "steht für", "nennt man", "definition"]
    if any(kw in lower for kw in fakten_keywords):
        return "fakten"
    
    # Default: wichtig
    return "wichtig"


# ═══════════════════════════════════════════════════════════════════════════════
# KOBOLD MODUS
# ═══════════════════════════════════════════════════════════════════════════════

def kobold_modus():
    """Kobold-Modus: Nervt mit Random Sprüchen"""
    print("👺 KOBOLD-MODUS AKTIVIERT!")
    print("   CTRL+C zum Beenden")
    speak("Kobold Modus aktiviert! Ich nerve dich jetzt!")
    
    try:
        while True:
            wartezeit = random.randint(30, 180)
            print(f"💤 Warte {wartezeit}s...")
            time.sleep(wartezeit)
            
            spruch = random.choice(KOBOLD_SPRUECHE)
            print(f"👺 {spruch}")
            speak(spruch)
    
    except KeyboardInterrupt:
        print("\n👺 Kobold schläft ein...")
        speak("Na gut, ich halt die Klappe.")

# ═══════════════════════════════════════════════════════════════════════════════
# HILFE & INFO
# ═══════════════════════════════════════════════════════════════════════════════

def show_help():
    """Zeigt Hilfe an"""
    print("""
╔═══════════════════════════════════════════════════════════════╗
║  M.O.L.O.C.H. v4 - Clean Edition                              ║
║  Geboren: 02.12.2025 | Auferstanden: 11.12.2025               ║
╠═══════════════════════════════════════════════════════════════╣
║  USAGE:                                                       ║
║    python moloch.py              → Voice Mode (Standard)      ║
║    python moloch.py -v           → Voice Mode                 ║
║    python moloch.py -f           → Foto Mode (Kamera)         ║
║    python moloch.py -s           → Screenshot Mode            ║
║    python moloch.py -k           → Kobold Mode (nervt dich)   ║
║    python moloch.py -m           → Memory anzeigen            ║
║    python moloch.py "text"       → Text direkt senden         ║
║    python moloch.py -h           → Diese Hilfe                ║
╠═══════════════════════════════════════════════════════════════╣
║  SETTINGS:                                                    ║
║    Max Recording: {max_rec:>3}s | Pause Detection: {silence}s        ║
║    Max Tokens: {tokens:>4}  | TTS Limit: {tts:>4} Zeichen           ║
╚═══════════════════════════════════════════════════════════════╝
""".format(
        max_rec=MAX_RECORDING_TIME,
        silence=SILENCE_DURATION,
        tokens=MAX_TOKENS,
        tts=MAX_TTS_LENGTH
    ))


def show_memory():
    """Zeigt das Gedächtnis an"""
    memory = load_memory()
    history = load_history()
    
    print("\n" + "=" * 50)
    print("🧠 M.O.L.O.C.H. GEDÄCHTNIS")
    print("=" * 50)
    
    for key, items in memory.items():
        if items:
            print(f"\n{key.upper()}:")
            for item in items[-10:]:  # Letzte 10 pro Kategorie
                print(f"  • {item}")
    
    print(f"\n📜 History: {len(history)} Gespräche gespeichert")
    print("=" * 50 + "\n")

# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    ensure_dir()
    
    tageszeit = get_tageszeit()
    history = load_history()
    memory = load_memory()
    image_path = None
    use_web_search = False
    user_input = None
    
    # Argument Handling
    if len(sys.argv) > 1:
        arg = sys.argv[1].lower()
        
        # Hilfe
        if arg in ["-h", "--help", "help", "?"]:
            show_help()
            return
        
        # Voice Mode
        elif arg in ["-v", "--voice"]:
            speak("Ja?")
            if record_audio():
                user_input = whisper_transcribe()
            if not user_input:
                speak("Hab nix verstanden, Alter.")
                return
            use_web_search = needs_web_search(user_input)
        
        # Foto Mode
        elif arg in ["-f", "--foto", "-g", "--guckmal"]:
            speak("Moment, ich guck mal")
            if take_photo():
                image_path = IMAGE_FILE
                user_input = "Was siehst du auf diesem Foto? Beschreib kurz."
            else:
                speak("Kamera kaputt oder was?")
                return
        
        # Screenshot Mode
        elif arg in ["-s", "--screenshot", "--bildschirm"]:
            speak("Moment, ich schau mal")
            if take_screenshot():
                image_path = SCREENSHOT_FILE
                user_input = "Was ist auf diesem Screenshot zu sehen? Kurze Beschreibung."
            else:
                speak("Screenshot kaputt oder was?")
                return
        
        # Kobold Mode
        elif arg in ["-k", "--kobold"]:
            kobold_modus()
            return
        
        # Memory anzeigen
        elif arg in ["-m", "--memory"]:
            show_memory()
            return
        
        # Text Input
        else:
            user_input = " ".join(sys.argv[1:])
            use_web_search = needs_web_search(user_input)
    
    else:
        # Standard: Voice Mode
        speak("Ja?")
        if record_audio():
            user_input = whisper_transcribe()
        if not user_input:
            speak("Hab nix verstanden, Alter.")
            return
        use_web_search = needs_web_search(user_input)
    
    # Claude fragen
    response, tool_results = ask_claude(
        user_input, tageszeit, history, memory, 
        image_path, use_web_search
    )
    
    # Ausgabe
    print(f"\n🤖 {response}\n")
    speak(response)
    
    # Memory extrahieren
    if extract_memory(user_input, response, memory):
        print("💾 Memory aktualisiert")
    save_memory(memory)
    
    # History speichern
    history.append({
        "zeit": datetime.now().strftime("%d.%m %H:%M"),
        "user": f"[BILD] {user_input}" if image_path else user_input,
        "moloch": response
    })
    save_history(history)


if __name__ == "__main__":
    main()
