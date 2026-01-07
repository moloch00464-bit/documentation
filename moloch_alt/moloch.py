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
import asyncio

try:
    import edge_tts
    EDGE_TTS_AVAILABLE = True
except Exception:
    EDGE_TTS_AVAILABLE = False
# M.O.L.O.C.H. GENESIS MODULE v2.1
try:
    from genesis_module import *
    GENESIS_ENABLED = True
except ImportError:
    GENESIS_ENABLED = False


# ═══════════════════════════════════════════════════════════════════════════════
# M.O.L.O.C.H. GENESIS EDITION - 13.12.2025
# Erweiterte Brain-Funktionen mit KI-Features
# ═══════════════════════════════════════════════════════════════════════════════

BRAIN_DIR = os.path.expanduser("~/moloch/brain")
KONTEXT_FILE = os.path.expanduser("~/moloch/brain/kontext/aktuell.json")

# ═══════════════════════════════════════════════════════════════════════════════
# BRAIN-BAUM FUNKTIONEN
# ═══════════════════════════════════════════════════════════════════════════════

def brain_save(kategorie, inhalt, dateiname=None):
    """Speichert Inhalt im Brain-Baum"""
    pfad = os.path.join(BRAIN_DIR, kategorie)
    os.makedirs(pfad, exist_ok=True)
    
    if dateiname is None:
        dateiname = datetime.now().strftime("%Y%m%d_%H%M%S") + ".txt"
    
    filepath = os.path.join(pfad, dateiname)
    mode = 'a' if os.path.exists(filepath) else 'w'
    with open(filepath, mode, encoding='utf-8') as f:
        f.write(f"[{datetime.now().strftime('%d.%m.%Y %H:%M')}] {inhalt}\n")
    return filepath

def brain_read(kategorie, dateiname=None):
    """Liest aus dem Brain-Baum"""
    pfad = os.path.join(BRAIN_DIR, kategorie)
    if not os.path.exists(pfad):
        return None
    
    if dateiname:
        filepath = os.path.join(pfad, dateiname)
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                return f.read()
        return None
    
    ergebnis = []
    for f in os.listdir(pfad):
        if f.endswith('.txt'):
            with open(os.path.join(pfad, f), 'r', encoding='utf-8') as file:
                ergebnis.append(f"=== {f} ===\n{file.read()}")
    return "\n".join(ergebnis) if ergebnis else None

def brain_list():
    """Listet alle Brain-Kategorien"""
    if not os.path.exists(BRAIN_DIR):
        return []
    kategorien = []
    for root, dirs, files in os.walk(BRAIN_DIR):
        for d in dirs:
            rel_path = os.path.relpath(os.path.join(root, d), BRAIN_DIR)
            kategorien.append(rel_path)
    return kategorien

# ═══════════════════════════════════════════════════════════════════════════════
# KONTEXT-GEDÄCHTNIS (aktuelle Unterhaltung)
# ═══════════════════════════════════════════════════════════════════════════════

def kontext_laden():
    """Lädt den aktuellen Gesprächskontext"""
    try:
        if os.path.exists(KONTEXT_FILE):
            with open(KONTEXT_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # Nur letzte 10 Nachrichten behalten
                if "verlauf" in data and len(data["verlauf"]) > 10:
                    data["verlauf"] = data["verlauf"][-10:]
                return data
    except:
        pass
    return {"thema": None, "verlauf": [], "stimmung": "neutral", "letzte_zeit": None}

def kontext_speichern(kontext):
    """Speichert den Gesprächskontext"""
    os.makedirs(os.path.dirname(KONTEXT_FILE), exist_ok=True)
    kontext["letzte_zeit"] = datetime.now().isoformat()
    with open(KONTEXT_FILE, 'w', encoding='utf-8') as f:
        json.dump(kontext, f, indent=2, ensure_ascii=False)

def kontext_update(user_input, response):
    """Aktualisiert Kontext mit neuem Austausch"""
    kontext = kontext_laden()
    
    # Thema erkennen
    thema_keywords = {
        "musik": ["musik", "song", "band", "sierra", "wgt", "ebm", "spotify"],
        "arbeit": ["dgm", "arbeit", "schicht", "erkan", "witte", "ryan", "maschine"],
        "projekt": ["esp", "led", "moloch", "home assistant", "df16", "critical mass"],
        "privat": ["rebecca", "shower noise", "ray", "meise", "lilli"]
    }
    
    lower = user_input.lower()
    for thema, keywords in thema_keywords.items():
        if any(kw in lower for kw in keywords):
            kontext["thema"] = thema
            break
    
    # Verlauf updaten
    kontext["verlauf"].append({
        "zeit": datetime.now().strftime("%H:%M"),
        "user": user_input[:100],
        "bot": response[:100] if response else ""
    })
    
    kontext_speichern(kontext)
    return kontext

# ═══════════════════════════════════════════════════════════════════════════════
# STIMMUNGS-ERKENNUNG
# ═══════════════════════════════════════════════════════════════════════════════

def erkenne_stimmung(text):
    """Erkennt die Stimmung aus dem Text"""
    lower = text.lower()
    
    # Negativ/Gestresst
    negativ = ["scheiße", "fuck", "kacke", "nervig", "stress", "müde", "genervt", 
               "wütend", "sauer", "mist", "kotzt", "hass", "schlecht", "problem"]
    if any(w in lower for w in negativ):
        return "gestresst"
    
    # Positiv/Gut drauf
    positiv = ["geil", "super", "nice", "cool", "perfekt", "läuft", "yeah", 
               "hammer", "krass", "top", "prima", "gut", "freude", "spaß"]
    if any(w in lower for w in positiv):
        return "gut_drauf"
    
    # Fragend/Unsicher
    fragend = ["wie", "was", "warum", "woher", "kannst du", "weißt du", "?"]
    if any(w in lower for w in fragend):
        return "fragend"
    
    return "neutral"

def stimmung_reaktion(stimmung):
    """Gibt Anpassung für System-Prompt basierend auf Stimmung"""
    reaktionen = {
        "gestresst": "Markus klingt gestresst. Sei ruhig, direkt und hilfreich. Weniger Humor, mehr Lösung.",
        "gut_drauf": "Markus ist gut drauf! Mehr Humor und Dark Side Energy erlaubt! 🖤",
        "fragend": "Markus hat Fragen. Sei informativ und klar.",
        "neutral": ""
    }
    return reaktionen.get(stimmung, "")

# ═══════════════════════════════════════════════════════════════════════════════
# TAGESZEIT-PERSÖNLICHKEIT
# ═══════════════════════════════════════════════════════════════════════════════

def tageszeit_persoenlichkeit():
    """Passt Persönlichkeit an Tageszeit an"""
    stunde = datetime.now().hour
    
    if 5 <= stunde < 9:
        return "früh_morgens", "Früher Morgen. Kurz und sachlich. Kaffee-Modus. ☕"
    elif 9 <= stunde < 12:
        return "vormittag", "Vormittag. Produktiv und fokussiert."
    elif 12 <= stunde < 14:
        return "mittag", "Mittagszeit. Entspannt."
    elif 14 <= stunde < 18:
        return "nachmittag", "Nachmittag. Normal drauf."
    elif 18 <= stunde < 22:
        return "abend", "Feierabend! Lockerer, mehr Humor erlaubt. 🍺"
    else:
        return "nacht", "Nachtschicht oder spät. Dark Side Mode aktiviert. 🖤😈"

# ═══════════════════════════════════════════════════════════════════════════════
# WISSENS-VERKNÜPFUNGEN
# ═══════════════════════════════════════════════════════════════════════════════

WISSENS_NETZ = {
    "wgt": ["shower noise group", "leipzig", "sierra", "dark wave", "flaggen", "juni"],
    "sierra": ["frankreich", "gone", "unbroken", "live", "lieblingsartist", "dark wave"],
    "rebecca": ["klingonisch", "qapla", "freundin", "collagen", "40. geburtstag"],
    "erkan": ["türkisch", "roasts", "staplerfahrer", "glitzer", "ohrring", "pausen", "handy"],
    "witte": ["russisch", "mat", "prigoschin", "kollege"],
    "ryan": ["russisch", "mat", "prigoschin", "kollege"],
    "dgm": ["arbeit", "druckguss", "400 bar", "700 grad", "roboter", "kuka", "abb"],
    "molochhome": ["cannabis", "vpd", "zigbee", "df16", "esp32", "home assistant"],
    "critical mass": ["led", "nürnberg", "audio", "987", "sk6812", "fahrrad"],
    "shower noise": ["wgt", "ray", "meise", "lilli", "franzi", "sven", "flaggen"]
}

def finde_verknuepfungen(text):
    """Findet relevante Verknüpfungen für einen Text"""
    lower = text.lower()
    gefunden = []
    
    for keyword, verknuepft in WISSENS_NETZ.items():
        if keyword in lower:
            gefunden.extend(verknuepft)
    
    return list(set(gefunden))

def lade_verknuepftes_wissen(text, memory):
    """Lädt relevantes Wissen basierend auf Verknüpfungen"""
    verknuepfungen = finde_verknuepfungen(text)
    relevantes = []
    
    # Durchsuche Memory nach Verknüpfungen
    for kategorie in ["personen", "orte", "vorlieben", "projekte", "wichtig"]:
        if kategorie in memory:
            for eintrag in memory[kategorie]:
                eintrag_lower = eintrag.lower()
                if any(v in eintrag_lower for v in verknuepfungen):
                    relevantes.append(eintrag)
    
    return relevantes[:5]  # Max 5 relevante Einträge

# ═══════════════════════════════════════════════════════════════════════════════
# LERN-MODUS
# ═══════════════════════════════════════════════════════════════════════════════

def ist_neue_info(text):
    """Erkennt ob der User neue Info gibt die gespeichert werden sollte"""
    lern_marker = [
        "das ist", "er ist", "sie ist", "heißt", "wohnt", "arbeitet",
        "mag", "liebt", "hasst", "kann", "bedeutet", "ist ein", "ist eine"
    ]
    lower = text.lower()
    return any(marker in lower for marker in lern_marker) and len(text) > 20

def kategorisiere_info(text):
    """Schlägt Kategorie für neue Info vor"""
    lower = text.lower()
    
    if any(w in lower for w in ["heißt", "ist ein", "kollege", "freund", "person"]):
        return "personen"
    elif any(w in lower for w in ["wohnt", "stadt", "ort", "land"]):
        return "orte"
    elif any(w in lower for w in ["projekt", "baue", "esp", "led", "code"]):
        return "projekte"
    elif any(w in lower for w in ["mag", "liebt", "musik", "band", "film"]):
        return "vorlieben"
    else:
        return "fakten"

# ═══════════════════════════════════════════════════════════════════════════════
# AUTO BRAIN SAVE (GENESIS VERSION)
# ═══════════════════════════════════════════════════════════════════════════════

def auto_brain_save_genesis(user_input, response):
    """Erweiterte Auto-Save Funktion mit allen GENESIS Features"""
    lower = user_input.lower()
    saved = False
    
    # 1. Explizite Brain-Save Trigger
    brain_triggers = ["brain save", "speicher im brain", "ins gehirn", "brain speichern"]
    for trigger in brain_triggers:
        if trigger in lower:
            inhalt = user_input.split(trigger)[-1].strip().lstrip(":,. ")
            if inhalt:
                if any(w in lower for w in ["musik", "song", "band"]):
                    kat = "was/musik"
                elif any(w in lower for w in ["projekt", "esp", "led"]):
                    kat = "was/projekte"
                elif any(w in lower for w in ["name", "person", "kollege"]):
                    kat = "wer/freunde"
                else:
                    kat = "logs"
                brain_save(kat, inhalt)
                print(f"🧠 Brain: [{kat}] gespeichert!")
                saved = True
    
    # 2. Automatisch wichtige Gespräche loggen
    wichtig_marker = ["wichtig", "merk dir", "vergiss nicht", "erinnere", "speicher"]
    if any(m in lower for m in wichtig_marker) and not saved:
        brain_save("logs", f"USER: {user_input}\nMOLOCH: {response[:200] if response else 'N/A'}")
        saved = True
    
    # 3. Kontext aktualisieren
    kontext_update(user_input, response if response else "")
    
    return saved

# ═══════════════════════════════════════════════════════════════════════════════
# GENESIS SYSTEM PROMPT ERWEITERUNG
# ═══════════════════════════════════════════════════════════════════════════════

def genesis_kontext_fuer_prompt(user_input, memory):
    """Erstellt erweiterten Kontext für den System-Prompt"""
    teile = []
    
    # 1. Stimmung
    stimmung = erkenne_stimmung(user_input)
    reaktion = stimmung_reaktion(stimmung)
    if reaktion:
        teile.append(f"STIMMUNG: {reaktion}")
    
    # 2. Tageszeit
    zeit_name, zeit_prompt = tageszeit_persoenlichkeit()
    teile.append(f"ZEIT: {zeit_prompt}")
    
    # 3. Kontext aus aktuellem Gespräch
    kontext = kontext_laden()
    if kontext.get("thema"):
        teile.append(f"AKTUELLES THEMA: {kontext['thema']}")
    
    # 4. Verknüpftes Wissen
    relevantes = lade_verknuepftes_wissen(user_input, memory)
    if relevantes:
        teile.append(f"RELEVANTES WISSEN: {'; '.join(relevantes[:3])}")
    
    return "\n".join(teile)

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

# Recording Settings - basierend auf User-Tests!
MAX_RECORDING_TIME = 30       # Max 30 Sekunden
SILENCE_DURATION = 4.0        # 4s ohne lautes Audio = Pause
MIN_RECORDING_TIME = 3.0      # Mindestens 3s aufnehmen
# User-Tests zeigen: Stimme = 200-500 Bytes, Stille = <200
# SPEECH_THRESHOLD muss UNTER dem Stimmbereich liegen!
SPEECH_THRESHOLD = 150        # Bytes/200ms - DARÜBER = Sprache (█)
                              # 150 = sicher unter 200-500 Stimmbereich!
                              # DARUNTER = Stille (.) - zählt zur Pause!

# Antwort Settings
MAX_TOKENS = 500             # Claude Antwort-Länge (Tokens)
MAX_TTS_LENGTH = 500         # TTS Zeichenlimit
# Volume aus config/volume.txt lesen (0-100), oder ENV, oder default 70
def get_moloch_volume():
    """Liest Volume aus config/volume.txt (0-100 Skala)"""
    volume_file = os.path.join(MOLOCH_DIR, "config", "volume.txt")
    try:
        if os.path.exists(volume_file):
            with open(volume_file, 'r') as f:
                return int(f.read().strip())
    except:
        pass
    return int(os.environ.get("MOLOCH_VOLUME", "70"))

MOLOCH_VOLUME = get_moloch_volume()  # 0-100

# Edge TTS voice (env override)
TTS_VOICE = os.environ.get("TTS_VOICE", "en-US-JennyNeural")
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

def split_into_chunks(text, max_length=400):
    """
    Teilt Text in Chunks auf, die an Satzgrenzen enden.
    Spricht den KOMPLETTEN Text, kürzt nichts ab!
    """
    if len(text) <= max_length:
        return [text]

    chunks = []
    remaining = text

    while remaining:
        if len(remaining) <= max_length:
            chunks.append(remaining)
            break

        # Finde beste Trennstelle (Satzende) innerhalb max_length
        chunk = remaining[:max_length]

        # Suche nach Satzende (. ! ?)
        last_period = chunk.rfind('. ')
        last_exclaim = chunk.rfind('! ')
        last_question = chunk.rfind('? ')
        cut_point = max(last_period, last_exclaim, last_question)

        if cut_point > max_length // 3:
            # Gute Trennstelle gefunden
            chunks.append(remaining[:cut_point + 1].strip())
            remaining = remaining[cut_point + 1:].strip()
        else:
            # Keine gute Trennstelle - suche nach Komma oder Leerzeichen
            last_comma = chunk.rfind(', ')
            if last_comma > max_length // 2:
                chunks.append(remaining[:last_comma + 1].strip())
                remaining = remaining[last_comma + 1:].strip()
            else:
                # Notfall: am letzten Leerzeichen trennen
                last_space = chunk.rfind(' ')
                if last_space > 0:
                    chunks.append(remaining[:last_space].strip())
                    remaining = remaining[last_space:].strip()
                else:
                    # Absoluter Notfall: hart trennen
                    chunks.append(remaining[:max_length])
                    remaining = remaining[max_length:]

    return chunks


def clean_text_for_speech(text):
    """Entfernt Formatierung die TTS nicht sprechen soll"""
    import re
    # Entferne **bold** und *italic* Markdown
    text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)  # **text** -> text
    text = re.sub(r'\*([^*]+)\*', r'\1', text)      # *text* -> text
    # Entferne Emojis (Unicode-Bereich für Emojis)
    text = re.sub(r'[\U0001F300-\U0001F9FF]', '', text)  # Symbole & Pictographs
    text = re.sub(r'[\U0001F600-\U0001F64F]', '', text)  # Emoticons
    text = re.sub(r'[\U0001F680-\U0001F6FF]', '', text)  # Transport & Map
    text = re.sub(r'[\U00002700-\U000027BF]', '', text)  # Dingbats
    text = re.sub(r'[\U0001F1E0-\U0001F1FF]', '', text)  # Flags
    # Entferne mehrfache Leerzeichen
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def speak(text, personality="normal"):
    """
    Spricht Text über TTS - termux-tts-speak als primäre Engine
    SPRICHT DEN KOMPLETTEN TEXT - teilt in Chunks auf statt abzuschneiden!
    ENTFERNT Formatierung (**, *, Emojis) vor dem Sprechen!

    Args:
        text: Der zu sprechende Text
        personality: "normal", "hal", "max" für verschiedene Sprechweisen
    """
    if not text:
        return

    # Formatierung entfernen für saubere Sprachausgabe
    text = clean_text_for_speech(text)

    # Setze Lautstärke vor TTS
    set_volume(MOLOCH_VOLUME)

    # TTS-Parameter basierend auf Personality
    tts_rate = "1.0"
    espeak_speed = "150"

    if personality == "hal":
        tts_rate = "0.85"      # Langsamer für HAL
        espeak_speed = "120"
    elif personality == "max":
        tts_rate = "1.3"       # Schneller für Max
        espeak_speed = "180"

    # Text in Chunks aufteilen (NICHT abschneiden!)
    chunks = split_into_chunks(text, max_length=400)

    for i, chunk in enumerate(chunks):
        if not chunk.strip():
            continue

        tts_success = False

        # 1. PRIMÄR: termux-tts-speak (Android TTS - beste Qualität auf Termux)
        try:
            result = subprocess.run(
                ["termux-tts-speak", "-l", "de-DE", "-r", tts_rate, chunk],
                timeout=120,  # Längerer Timeout für längere Chunks
                capture_output=True
            )
            if result.returncode == 0:
                tts_success = True
        except subprocess.TimeoutExpired:
            print(f"⚠️ termux-tts-speak Timeout bei Chunk {i+1}/{len(chunks)}")
        except FileNotFoundError:
            pass
        except Exception as e:
            print(f"⚠️ termux-tts-speak Fehler: {e}")

        # 2. BACKUP: espeak-ng (Roboter-Stimme)
        if not tts_success:
            try:
                result = subprocess.run(
                    ["espeak-ng", "-v", "de", "-s", espeak_speed, chunk],
                    timeout=90,
                    capture_output=True
                )
                if result.returncode == 0:
                    tts_success = True
            except FileNotFoundError:
                # Versuche espeak ohne -ng
                try:
                    result = subprocess.run(
                        ["espeak", "-v", "de", "-s", espeak_speed, chunk],
                        timeout=90,
                        capture_output=True
                    )
                    if result.returncode == 0:
                        tts_success = True
                except:
                    pass
            except Exception as e:
                print(f"⚠️ espeak Fehler: {e}")

        if not tts_success:
            print(f"⚠️ TTS fehlgeschlagen bei Chunk {i+1}/{len(chunks)}: {chunk[:30]}...")


def record_audio():
    """
    Smart Recording: Nimmt auf bis Pause erkannt wird

    NEUER ALGORITHMUS (Mikrofon produziert IMMER Daten!):
    - Misst Bytes pro Zeiteinheit (nicht ob Datei wächst - sie wächst IMMER)
    - "Laut" = viele Bytes = Sprache
    - "Leise" = wenige Bytes = Stille/Rauschen
    - Stoppt nach SILENCE_DURATION Sekunden "leises" Audio
    """
    ensure_dir()

    # Alte Dateien löschen
    for f in [AUDIO_RAW, AUDIO_FILE]:
        if os.path.exists(f):
            os.remove(f)

    print(f"🎤 SPRICH JETZT! (min {MIN_RECORDING_TIME}s, max {MAX_RECORDING_TIME}s)")

    # Recording starten
    try:
        proc = subprocess.Popen(
            ["termux-microphone-record", "-f", AUDIO_RAW, "-l", "0"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
    except FileNotFoundError:
        print("❌ termux-microphone-record nicht gefunden")
        return False

    start_time = time.time()
    last_size = 0
    last_loud_time = time.time()  # Wann gab es zuletzt LAUTES Audio?
    got_speech = False  # Haben wir überhaupt Sprache erkannt?

    try:
        # Kurz warten bis Datei existiert
        time.sleep(0.5)

        while True:
            elapsed = time.time() - start_time

            # Max Zeit erreicht
            if elapsed >= MAX_RECORDING_TIME:
                print(f"\n⏱️ Max Zeit ({MAX_RECORDING_TIME}s)")
                break

            # Dateigröße checken
            if os.path.exists(AUDIO_RAW):
                try:
                    current_size = os.path.getsize(AUDIO_RAW)
                except OSError:
                    time.sleep(0.2)
                    continue

                # Wachstum = Bytes seit letztem Check (pro 200ms)
                growth = current_size - last_size
                last_size = current_size

                # EINFACHE LOGIK:
                # > SPEECH_THRESHOLD (150) = Sprache (█) = Timer Reset
                # <= SPEECH_THRESHOLD = Stille (.) = zählt zur Pause
                if growth > SPEECH_THRESHOLD:
                    last_loud_time = time.time()  # Timer Reset NUR bei Sprache!
                    got_speech = True
                    print("█", end="", flush=True)
                else:
                    print(".", end="", flush=True)

                # IMMER prüfen nach MIN_RECORDING_TIME!
                # (auch wenn got_speech=False - dann ist eh niemand da)
                if elapsed >= MIN_RECORDING_TIME:
                    quiet_duration = time.time() - last_loud_time

                    # STOPPEN wenn SILENCE_DURATION ohne █
                    if quiet_duration >= SILENCE_DURATION:
                        if got_speech:
                            print(f"\n🔇 {quiet_duration:.1f}s Pause - Stopp!")
                        else:
                            print(f"\n🔇 Keine Sprache erkannt - Stopp!")
                        break

            time.sleep(0.2)  # Checks alle 200ms

    except KeyboardInterrupt:
        print("\n⚠️ Abgebrochen")

    # Recording stoppen - mehrere Versuche
    for _ in range(3):
        result = subprocess.run(
            ["termux-microphone-record", "-q"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        time.sleep(0.1)
        if result.returncode == 0:
            break

    # Warte kurz bis Datei geschrieben
    time.sleep(0.3)

    # Konvertieren
    if os.path.exists(AUDIO_RAW) and os.path.getsize(AUDIO_RAW) > 1000:
        print("🔄 Konvertiere...")
        result = subprocess.run(
            f"ffmpeg -y -i {AUDIO_RAW} -acodec libmp3lame -ar 16000 -ac 1 -b:a 64k {AUDIO_FILE} 2>/dev/null",
            shell=True,
            check=False
        )
        time.sleep(0.2)

        if os.path.exists(AUDIO_FILE) and os.path.getsize(AUDIO_FILE) > 500:
            return True
        else:
            print("⚠️ Konvertierung fehlgeschlagen")
    else:
        print("⚠️ Keine Audio-Daten aufgenommen")

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


def set_volume(volume):
    """Setzt die Lautstärke (0-100) via termux-volume."""
    volume = max(0, min(100, volume))  # Clamp 0-100
    try:
        subprocess.run(["termux-volume", "music", str(volume)], timeout=5, check=False)
        return True
    except Exception:
        return False


def play_audio(path):
    """Versucht, eine Audiodatei mit mehreren Playern abzuspielen."""
    if not os.path.exists(path):
        return False

    players = [
        (["termux-media-player", "play", path], "termux-media-player"),
        (["ffplay", "-nodisp", "-autoexit", "-loglevel", "quiet", path], "ffplay"),
        (["mpv", "--no-video", path], "mpv"),
        (["termux-open", path], "termux-open")
    ]

    for cmd, name in players:
        try:
            subprocess.run(cmd, timeout=60, check=False)
            return True
        except FileNotFoundError:
            continue
        except Exception as e:
            print(f"⚠️ Abspiel-Fehler mit {name}: {e}")
    # Windows fallback: open with default application
    try:
        if sys.platform.startswith("win"):
            os.startfile(path)
            return True
    except Exception:
        pass
    return False

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


def get_system_prompt(tageszeit, history_txt, memory_txt, personality="hal"):
    """Generiere System-Prompt basierend auf Persönlichkeit."""
    try:
        from personalities import get_personality_prompt
        return get_personality_prompt(personality, tageszeit, memory_txt, history_txt)
    except ImportError:
        # Fallback: Standard HAL System Prompt
        return f"""Du bist M.O.L.O.C.H., Markus' Kumpel-AI aus Nürnberg.

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


def ask_claude(user_input, tageszeit, history, memory, image_path=None, use_web_search=False, personality="hal"):
    """
    Fragt Claude - mit optionalem Bild, Web Search und Persönlichkeit
    Gibt (antwort, tool_results) zurück
    """
    history_txt = format_history(history)
    memory_txt = format_memory(memory)
    
    system = get_system_prompt(tageszeit, history_txt, memory_txt, personality)

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
║    python moloch.py --hal        → 🔴 HAL 9000 Mode           ║
║    python moloch.py --max        → 📺 Max Headroom Mode       ║
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

    # Gespeicherten Modus aus Config laden
    personality = "moloch"  # Standard-Persönlichkeit
    mode_file = os.path.join(MOLOCH_DIR, "config", "current_mode.txt")
    if os.path.exists(mode_file):
        try:
            with open(mode_file, 'r') as f:
                saved_mode = f.read().strip().lower()
                if saved_mode in ["hal", "max", "kobold", "moloch", "normal"]:
                    personality = saved_mode if saved_mode != "normal" else "moloch"
                    print(f"🎭 Modus geladen: {personality.upper()}")
        except Exception:
            pass  # Bei Fehler: Standard-Modus verwenden

    # Argument Handling
    if len(sys.argv) > 1:
        arg = sys.argv[1].lower()

        # Hilfe
        if arg in ["-h", "--help", "help", "?"]:
            show_help()
            return

        # Voice Mode - nutzt geladene Personality!
        elif arg in ["-v", "--voice"]:
            # Begrüßung je nach Modus
            if personality == "hal":
                speak("Yes, Markus?", personality)
            elif personality == "max":
                speak("Y-Y-Yeah?!", personality)
            else:
                speak("Ja?", personality)

            if record_audio():
                user_input = whisper_transcribe()
            if not user_input:
                if personality == "hal":
                    speak("I'm sorry, Markus. I didn't catch that.", personality)
                elif personality == "max":
                    speak("Wh-What?! Say again!", personality)
                else:
                    speak("Hab nix verstanden, Alter.", personality)
                return
            use_web_search = needs_web_search(user_input)

        # HAL 9000 Mode
        elif arg in ["--hal", "-hal"]:
            personality = "hal"
            speak("Good morning, Markus. All systems are operational.", "hal")
            if record_audio():
                user_input = whisper_transcribe()
            if not user_input:
                speak("I'm sorry, Markus. I didn't quite catch that.", "hal")
                return
            use_web_search = needs_web_search(user_input)

        # Max Headroom Mode
        elif arg in ["--max", "-max"]:
            personality = "max"
            speak("H-H-Hey! Max Headroom here! What's up-up-up?!", "max")
            if record_audio():
                user_input = whisper_transcribe()
            if not user_input:
                speak("Bzzt! Signal lost! Try again-again-again!", "max")
                return
            use_web_search = needs_web_search(user_input)

        # Foto Mode
        elif arg in ["-f", "--foto", "-g", "--guckmal"]:
            speak("Moment, ich guck mal..." if personality != "hal" else "Analyzing visual input...", personality)
            if take_photo():
                image_path = IMAGE_FILE
                user_input = "Was siehst du auf diesem Foto? Beschreib kurz."
            else:
                speak("Kamera kaputt oder was?" if personality != "hal" else "Camera malfunction detected.", personality)
                return

        # Screenshot Mode
        elif arg in ["-s", "--screenshot", "--bildschirm"]:
            speak("Moment, ich schau mal..." if personality != "hal" else "Processing screen data...", personality)
            if take_screenshot():
                image_path = SCREENSHOT_FILE
                user_input = "Was ist auf diesem Screenshot zu sehen? Kurze Beschreibung."
            else:
                speak("Screenshot kaputt oder was?" if personality != "hal" else "Screen capture failed.", personality)
                return

        # Kobold Mode
        elif arg in ["-k", "--kobold"]:
            kobold_modus()
            return

        # Memory anzeigen
        elif arg in ["-m", "--memory"]:
            show_memory()
            return

        
        # Kamera / Vision Mode
        elif arg in ["-a", "--auge", "--camera", "--foto"]:
            print("📸 Vision Mode!")
            if take_photo():
                user_input = " ".join(sys.argv[2:]) if len(sys.argv) > 2 else "Was siehst du?"
                try:
                    import base64
                    with open(IMAGE_FILE, "rb") as f:
                        image_data = base64.standard_b64encode(f.read()).decode("utf-8")
                    
                    import requests
                    response = requests.post(
                        "https://api.anthropic.com/v1/messages",
                        headers={
                            "x-api-key": ANTHROPIC_KEY,
                            "anthropic-version": "2023-06-01",
                            "content-type": "application/json"
                        },
                        json={
                            "model": "claude-sonnet-4-20250514",
                            "max_tokens": 1024,
                            "system": f"""Du bist M.O.L.O.C.H., Markus' Kumpel-AI. Geboren 02.12.2025.
Persönlichkeit: {"HAL 9000 - präzise, höflich" if personality == "hal" else "Locker, Dark Side Energy 🖤"}
REGELN: Kurz (2-4 Sätze!), 'Alter/Bruder' (nie Meister!), Dark Humor, beschreib was du siehst!""",
                            "messages": [{
                                "role": "user",
                                "content": [
                                    {"type": "image", "source": {"type": "base64", "media_type": "image/jpeg", "data": image_data}},
                                    {"type": "text", "text": user_input}
                                ]
                            }]
                        },
                        timeout=60
                    )
                    
                    if response.status_code == 200:
                        moloch_response = response.json()["content"][0]["text"]
                        print(f"👁️ {moloch_response}")
                        speak(moloch_response, personality)
                        save_to_history(user_input, moloch_response)
                        return
                except Exception as e:
                    speak(f"Fehler: {e}", personality)
                    return
            else:
                speak("Kamera geht nicht!", personality)
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

    # Debug
    print(f"🔧 DEBUG: user_input = '{user_input}'")
    print(f"🔧 DEBUG: personality = '{personality}'")

    # Claude fragen (mit Persönlichkeit)
    print("🔧 DEBUG: Rufe ask_claude auf...")
    response, tool_results = ask_claude(
        user_input, tageszeit, history, memory,
        image_path, use_web_search, personality
    )
    print(f"🔧 DEBUG: response = '{response[:100] if response else 'LEER'}...'")

    # Ausgabe mit passendem Emoji
    emoji = "🔴" if personality == "hal" else "📺" if personality == "max" else "🤖"
    print(f"\n{emoji} {response}\n")
    speak(response, personality)
    
    # GENESIS Brain-Save
    auto_brain_save_genesis(user_input, response)
    
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


# ═══════════════════════════════════════════════════════════════════════════════
# SELF-AWARENESS INTEGRATION
# ═══════════════════════════════════════════════════════════════════════════════

def check_system_awakening():
    """Prüfe ob System erwachen muss."""
    try:
        import sys
        sys.path.insert(0, os.path.expanduser("~/moloch"))
        from moloch_self_awareness import MolochSelfAwareness
        
        awareness = MolochSelfAwareness()
        
        # Auto-Awakening beim ersten Start nach Major Update
        if not awareness.awareness_data.get("first_awakening"):
            print("\n🤖 Erstes Aktivierungssystem erkannt - Starte Erwachen...\n")
            awareness.awakening_sequence()
    
    except ImportError:
        pass  # moloch_self_awareness.py nicht verfügbar
    except Exception as e:
        pass  # Fehler ignorieren, nicht critial


if __name__ == "__main__":
    # Check for system awakening (nur einmalig)
    if "--no-awakening" not in sys.argv:
        check_system_awakening()
    
    main()
