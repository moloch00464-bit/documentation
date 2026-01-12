#!/usr/bin/env python3
"""
M.O.L.O.C.H. v5 - FIXED & ROBUST Edition
========================================
Geboren: 02.12.2025
Fixed: 04.01.2026

Markus' mobiler Kumpel-AI - CRASH-SICHER!
"""

import os
import json
import subprocess
import requests
import sys
import time
import base64
from datetime import datetime

# ═══════════════════════════════════════════════════════════════════════════════
# KONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Pfade
MOLOCH_DIR = os.path.expanduser("~/moloch")
AUDIO_FILE = f"{MOLOCH_DIR}/ohr.wav"
IMAGE_FILE = f"{MOLOCH_DIR}/auge.jpg"
HISTORY_FILE = f"{MOLOCH_DIR}/history.json"
MEMORY_FILE = f"{MOLOCH_DIR}/langzeit.json"

# Audio
MAX_RECORDING_TIME = 20

# ═══════════════════════════════════════════════════════════════════════════════
# SPOTIFY BRAIN
# ═══════════════════════════════════════════════════════════════════════════════

MUSIK_BRAIN = """
MARKUS' MUSIK (Spotify 2015-2025, 6832h):
- Suicide Commando (185h) - #1 seit 26 Jahren!
- SIERRA (103h) - LIEBLINGSBAND! Gone = Lieblingssong
- VNV Nation, ESA, Chainreactor, Vomito Negro
- Genre: Dark EBM, Industrial Techno, Darksynth
- WGT Leipzig seit 2000 (25 Jahre!)
- Schicht-Musik: Hart (Früh), Melodisch (Nacht)
"""

# ═══════════════════════════════════════════════════════════════════════════════
# HELPER FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════

def safe_run(cmd, timeout=10, **kwargs):
    """Sicheres subprocess.run mit Error Handling"""
    try:
        return subprocess.run(
            cmd,
            capture_output=True,
            timeout=timeout,
            text=True,
            **kwargs
        )
    except subprocess.TimeoutExpired:
        print(f"⚠️ Timeout: {' '.join(cmd)}")
        return None
    except FileNotFoundError:
        print(f"❌ Befehl nicht gefunden: {cmd[0]}")
        print(f"   Installiere: pkg install {cmd[0]}")
        return None
    except Exception as e:
        print(f"❌ Fehler: {e}")
        return None

def check_api_key(key_name):
    """Checkt ob API Key gesetzt ist"""
    key = os.getenv(key_name)
    if not key or len(key) < 20:
        print(f"❌ {key_name} fehlt!")
        print(f"   Setze in ~/.bashrc:")
        print(f'   export {key_name}="sk-..."')
        return False
    return True

# ═══════════════════════════════════════════════════════════════════════════════
# SPEICHER
# ═══════════════════════════════════════════════════════════════════════════════

def load_memory():
    """Lädt Langzeitspeicher"""
    try:
        if os.path.exists(MEMORY_FILE):
            with open(MEMORY_FILE) as f:
                return json.load(f)
    except Exception as e:
        print(f"⚠️ Memory-Fehler: {e}")

    return {
        "wichtig": [],
        "fakten": [],
        "personen": [],
        "orte": [],
        "vorlieben": [],
        "projekte": [],
    }

def save_memory(memory):
    """Speichert Langzeitspeicher"""
    try:
        with open(MEMORY_FILE, "w") as f:
            json.dump(memory, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"⚠️ Memory speichern fehlgeschlagen: {e}")

def load_history():
    """Lädt Chat-History"""
    try:
        if os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE) as f:
                return json.load(f)
    except:
        pass
    return []

def save_history(history):
    """Speichert Chat-History"""
    try:
        with open(HISTORY_FILE, "w") as f:
            json.dump(history, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"⚠️ History speichern fehlgeschlagen: {e}")

# ═══════════════════════════════════════════════════════════════════════════════
# AUDIO
# ═══════════════════════════════════════════════════════════════════════════════

def speak(text):
    """Text-to-Speech - ROBUST"""
    print(f"\n🗣️ {text}\n")

    result = safe_run(["termux-tts-speak", text], timeout=30)
    if result is None:
        print("💡 TTS geht nicht - aber Text steht oben! ☝️")

def record_audio():
    """Nimmt Audio auf - ROBUST"""
    print("🎙️ Höre zu (max 20 Sek)...")

    # Alte Datei weg
    if os.path.exists(AUDIO_FILE):
        try:
            os.remove(AUDIO_FILE)
        except:
            pass

    # Tempfile für AAC
    temp_file = f"{MOLOCH_DIR}/temp_recording.m4a"
    if os.path.exists(temp_file):
        try:
            os.remove(temp_file)
        except:
            pass

    # Aufnehmen
    result = safe_run([
        "termux-microphone-record",
        "-f", temp_file,
        "-l", str(MAX_RECORDING_TIME),
        "-e", "aac"
    ], timeout=MAX_RECORDING_TIME + 5)

    if result is None:
        print("❌ termux-microphone-record fehlt!")
        print("   Installiere: pkg install termux-api")
        return False

    # Warte kurz
    time.sleep(1)

    # Check ob File existiert
    if not os.path.exists(temp_file):
        print("⚠️ Keine Audio-Datei erstellt")
        return False

    # WAV konvertieren
    print("🔄 Konvertiere zu WAV...")
    result = safe_run([
        "ffmpeg", "-y", "-i", temp_file,
        "-ar", "16000", "-ac", "1",
        "-acodec", "pcm_s16le",
        AUDIO_FILE
    ], timeout=30)

    if result is None or not os.path.exists(AUDIO_FILE):
        print("❌ ffmpeg fehlt oder Konvertierung fehlgeschlagen!")
        print("   Installiere: pkg install ffmpeg")
        # Fallback: temp file als audio nutzen
        try:
            os.rename(temp_file, AUDIO_FILE)
        except:
            pass

    # Cleanup
    try:
        if os.path.exists(temp_file):
            os.remove(temp_file)
    except:
        pass

    # Check
    if os.path.exists(AUDIO_FILE):
        size = os.path.getsize(AUDIO_FILE)
        if size > 1000:
            print(f"✅ Audio aufgenommen ({size} bytes)")
            return True

    print("⚠️ Audio zu klein oder leer")
    return False

def whisper_transcribe():
    """Transkribiert mit Whisper - ROBUST"""
    if not os.path.exists(AUDIO_FILE):
        print("❌ Keine Audio-Datei!")
        return None

    if not check_api_key("OPENAI_API_KEY"):
        return None

    print("📝 Transkribiere...")

    try:
        with open(AUDIO_FILE, "rb") as f:
            response = requests.post(
                "https://api.openai.com/v1/audio/transcriptions",
                headers={"Authorization": f"Bearer {OPENAI_API_KEY}"},
                files={"file": f},
                data={"model": "whisper-1", "language": "de"},
                timeout=30
            )

        if response.status_code == 200:
            text = response.json().get("text", "").strip()
            if text:
                print(f"💬 \"{text}\"")
                return text
            else:
                print("⚠️ Whisper: Leerer Text")
        else:
            print(f"❌ Whisper Fehler {response.status_code}")
            if response.status_code == 401:
                print("   → API Key falsch!")
            elif response.status_code == 429:
                print("   → Rate Limit erreicht!")

    except requests.exceptions.Timeout:
        print("⚠️ Whisper Timeout")
    except requests.exceptions.ConnectionError:
        print("❌ Keine Internet-Verbindung!")
    except Exception as e:
        print(f"❌ Whisper-Fehler: {e}")

    return None

# ═══════════════════════════════════════════════════════════════════════════════
# KAMERA
# ═══════════════════════════════════════════════════════════════════════════════

def take_photo():
    """Macht Foto - ROBUST"""
    print("📸 Foto...")

    if os.path.exists(IMAGE_FILE):
        try:
            os.remove(IMAGE_FILE)
        except:
            pass

    result = safe_run([
        "termux-camera-photo",
        "-c", "0",
        IMAGE_FILE
    ], timeout=15)

    if result is None:
        print("❌ termux-camera-photo fehlt!")
        print("   Installiere: pkg install termux-api")
        return None

    time.sleep(2)

    if os.path.exists(IMAGE_FILE):
        size = os.path.getsize(IMAGE_FILE)
        if size > 1000:
            print(f"✅ Foto ({size} bytes)")
            return IMAGE_FILE

    print("⚠️ Kein Foto erstellt")
    return None

def encode_image(image_path):
    """Enkodiert Bild - ROBUST"""
    try:
        with open(image_path, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")
    except Exception as e:
        print(f"❌ Bild-Encoding fehlgeschlagen: {e}")
        return None

# ═══════════════════════════════════════════════════════════════════════════════
# CLAUDE API
# ═══════════════════════════════════════════════════════════════════════════════

def get_tageszeit():
    """Tageszeit"""
    hour = datetime.now().hour
    if 5 <= hour < 12:
        return "Morgen ☀️"
    elif 12 <= hour < 17:
        return "Mittag 🌤️"
    elif 17 <= hour < 21:
        return "Abend 🌅"
    else:
        return "Nacht 🌙"

def format_memory(memory):
    """Memory formatieren"""
    parts = []
    for kategorie, items in memory.items():
        if items:
            recent = items[-3:]  # Nur 3 neueste
            parts.append(f"{kategorie.upper()}: {', '.join(recent)}")
    return "\n".join(parts) if parts else ""

def format_history(history):
    """History formatieren"""
    if not history:
        return ""

    recent = history[-3:]  # Nur 3 neueste
    lines = []
    for h in recent:
        lines.append(f"User: {h.get('user', '?')[:50]}")
        lines.append(f"M: {h.get('moloch', '?')[:50]}")

    return "\n".join(lines)

def ask_claude(user_input, tageszeit, history, memory, image_path=None):
    """Fragt Claude - ROBUST"""
    if not check_api_key("ANTHROPIC_API_KEY"):
        return "API Key fehlt! Check ANTHROPIC_API_KEY!"

    history_txt = format_history(history)
    memory_txt = format_memory(memory)

    system = f"""Du bist M.O.L.O.C.H., Markus' Kumpel-AI aus Nürnberg.

ÜBER DICH:
- Geboren: 02.12.2025, Fixed: 04.01.2026
- Claude = großer Bruder, Markus = Kumpel

{MUSIK_BRAIN}

TAGESZEIT: {tageszeit}

MEMORY:
{memory_txt}

LETZTE GESPRÄCHE:
{history_txt}

REGELN:
- KURZ! (2-4 Sätze)
- "Alter" oder "Bruder" - NIE "Meister"
- Dark Humor 🖤
- Bei "merk dir..." bestätige kurz
- Fränkisch ok: "des basst", "gell"
- Musik-Talk: Du kennst seinen Geschmack!"""

    # Content
    if image_path and os.path.exists(image_path):
        image_data = encode_image(image_path)
        if not image_data:
            return "Bild konnte nicht geladen werden!"

        content = [
            {
                "type": "image",
                "source": {
                    "type": "base64",
                    "media_type": "image/jpeg",
                    "data": image_data
                }
            },
            {"type": "text", "text": user_input or "Was siehst du?"}
        ]
    else:
        content = user_input

    try:
        response = requests.post(
            "https://api.anthropic.com/v1/messages",
            headers={
                "x-api-key": ANTHROPIC_API_KEY,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json"
            },
            json={
                "model": "claude-sonnet-4-5-20250929",
                "max_tokens": 500,
                "system": system,
                "messages": [{"role": "user", "content": content}]
            },
            timeout=60
        )

        if response.status_code == 200:
            return response.json()["content"][0]["text"]
        elif response.status_code == 401:
            return "API Key ungültig!"
        elif response.status_code == 429:
            return "Rate Limit! Warte mal kurz..."
        else:
            return f"API Fehler {response.status_code}"

    except requests.exceptions.Timeout:
        return "Claude antwortet nicht - Timeout!"
    except requests.exceptions.ConnectionError:
        return "Keine Internet-Verbindung!"
    except Exception as e:
        return f"Fehler: {e}"

# ═══════════════════════════════════════════════════════════════════════════════
# MEMORY EXTRAKTION
# ═══════════════════════════════════════════════════════════════════════════════

def extract_info(user_input, response, memory):
    """Info extrahieren - ROBUST"""
    changed = False
    lower = user_input.lower()

    # Speicher-Trigger
    triggers = ["merk dir", "merke dir", "speicher", "vergiss nicht", "wichtig"]

    for trigger in triggers:
        if trigger in lower:
            info = lower.split(trigger, 1)[-1].strip()
            info = info.lstrip(":,. ")

            if info and len(info) > 3:
                kategorie = auto_kategorisiere(info)

                if info not in memory[kategorie]:
                    memory[kategorie].append(info)
                    changed = True
                    print(f"💾 [{kategorie}] {info}")
            break

    return memory, changed

def auto_kategorisiere(text):
    """Auto-Kategorisierung"""
    lower = text.lower()

    if any(kw in lower for kw in ["heißt", "name", "freund", "kollege"]):
        return "personen"
    elif any(kw in lower for kw in ["wohnt", "stadt", "straße"]):
        return "orte"
    elif any(kw in lower for kw in ["projekt", "baue", "esp", "led"]):
        return "projekte"
    elif any(kw in lower for kw in ["mag", "liebe", "höre"]):
        return "vorlieben"
    elif any(kw in lower for kw in ["bedeutet", "ist ein", "funktioniert"]):
        return "fakten"
    else:
        return "wichtig"

# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════

def show_help():
    print("""
╔═══════════════════════════════════════════════════════════════╗
║  M.O.L.O.C.H. v5 - FIXED & ROBUST Edition                     ║
╠═══════════════════════════════════════════════════════════════╣
║  USAGE:                                                       ║
║    python moloch_fixed.py              → Voice Mode           ║
║    python moloch_fixed.py -t "Text"    → Text Mode            ║
║    python moloch_fixed.py -a           → Auge (Foto)          ║
║    python moloch_fixed.py -h           → Hilfe                ║
╠═══════════════════════════════════════════════════════════════╣
║  FEATURES:                                                    ║
║    🎤 Whisper STT     - Ohren                                 ║
║    👁️ Claude Vision   - Augen                                 ║
║    🧠 Memory          - Gedächtnis                            ║
║    🎵 Spotify Brain   - Musikgeschmack                        ║
║    🔊 TTS             - Stimme                                ║
║    🛡️ Crash-Safe      - Error Handling                        ║
╚═══════════════════════════════════════════════════════════════╝
""")

def main():
    # Setup
    os.makedirs(MOLOCH_DIR, exist_ok=True)
    history = load_history()
    memory = load_memory()
    tageszeit = get_tageszeit()

    user_input = None
    image_path = None

    # Args
    args = sys.argv[1:]

    if not args:
        # Voice Mode
        speak("Ja?")
        if record_audio():
            user_input = whisper_transcribe()

        if not user_input:
            speak("Hab nix gehört, Alter!")
            return

    else:
        arg = args[0].lower()

        if arg in ["-h", "--help", "-hilfe"]:
            show_help()
            return

        elif arg in ["-t", "--text"]:
            user_input = " ".join(args[1:]) if len(args) > 1 else None
            if not user_input:
                print("❌ Kein Text!")
                return

        elif arg in ["-a", "--auge", "-foto"]:
            speak("Moment...")
            image_path = take_photo()
            if not image_path:
                speak("Kamera geht nicht!")
                return
            user_input = " ".join(args[1:]) if len(args) > 1 else "Was siehst du?"

        else:
            user_input = " ".join(args)

    # Claude fragen
    response = ask_claude(user_input, tageszeit, history, memory, image_path)

    # Antwort
    speak(response)

    # Memory
    memory, changed = extract_info(user_input, response, memory)
    if changed:
        save_memory(memory)

    # History
    history.append({
        "zeit": datetime.now().isoformat(),
        "user": user_input,
        "moloch": response
    })
    save_history(history[-50:])

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Bis dann, Alter!")
    except Exception as e:
        print(f"\n❌ CRASH: {e}")
        print("💡 Run: python diagnose.py")
