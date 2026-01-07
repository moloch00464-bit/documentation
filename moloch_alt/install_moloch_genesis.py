#!/usr/bin/env python3
"""
███╗   ███╗ ██████╗ ██╗      ██████╗  ██████╗██╗  ██╗
████╗ ████║██╔═══██╗██║     ██╔═══██╗██╔════╝██║  ██║
██╔████╔██║██║   ██║██║     ██║   ██║██║     ███████║
██║╚██╔╝██║██║   ██║██║     ██║   ██║██║     ██╔══██║
██║ ╚═╝ ██║╚██████╔╝███████╗╚██████╔╝╚██████╗██║  ██║
╚═╝     ╚═╝ ╚═════╝ ╚══════╝ ╚═════╝  ╚═════╝╚═╝  ╚═╝

         ██████╗ ███████╗███╗   ██╗███████╗███████╗██╗███████╗
        ██╔════╝ ██╔════╝████╗  ██║██╔════╝██╔════╝██║██╔════╝
        ██║  ███╗█████╗  ██╔██╗ ██║█████╗  ███████╗██║███████╗
        ██║   ██║██╔══╝  ██║╚██╗██║██╔══╝  ╚════██║██║╚════██║
        ╚██████╔╝███████╗██║ ╚████║███████╗███████║██║███████║
         ╚═════╝ ╚══════╝╚═╝  ╚═══╝╚══════╝╚══════╝╚═╝╚══════╝

    M.O.L.O.C.H. GENESIS EDITION - v2.1 DARK SIDE UPDATE
    =====================================================
    NEU in v2.1:
    - Deutsche Sprachausgabe (TTS)
    - Max Headroom Modus mit Stottern
    - HAL 9000 rotes Auge Modus
    - Deutsche Fehlermeldungen

    Original: 13.12.2025
    v2.0: 14.12.2025
    v2.1 Dark Side: 14.12.2025
    Erschaffen von M.A.M. (Markus And Moloch)
"""

import os
import re
import json
import shutil
import logging
import random
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple

# ═══════════════════════════════════════════════════════════════════════════════
# KONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════

class Config:
    """Zentrale Konfiguration für M.O.L.O.C.H."""

    # Basis-Pfade
    HOME = Path.home()
    MOLOCH_DIR = HOME / "moloch"
    MOLOCH_FILE = MOLOCH_DIR / "moloch.py"
    MEMORY_FILE = MOLOCH_DIR / "langzeit.json"
    BRAIN_DIR = MOLOCH_DIR / "brain"
    KONTEXT_FILE = BRAIN_DIR / "kontext" / "aktuell.json"
    CONFIG_FILE = MOLOCH_DIR / "config.json"
    LOG_FILE = MOLOCH_DIR / "genesis.log"

    # Limits
    MAX_KONTEXT_VERLAUF = 10
    MAX_MEMORY_ENTRIES_PER_CATEGORY = 100
    MAX_RECORDING_TIME = 15

    # Encoding für Termux
    ENCODING = 'utf-8'

    # TTS Konfiguration
    TTS_ENGINE = 'espeak'  # 'espeak', 'pyttsx3', 'termux-tts'
    TTS_VOICE = 'de'
    TTS_SPEED = 150
    TTS_PITCH = 50

    # Persönlichkeits-Modi
    PERSONALITY_MODE = 'normal'  # 'normal', 'max_headroom', 'hal9000'


# ═══════════════════════════════════════════════════════════════════════════════
# DEUTSCHE FEHLERMELDUNGEN
# ═══════════════════════════════════════════════════════════════════════════════

class FehlerMeldungen:
    """Deutsche Fehlermeldungen mit Stil."""

    # Standard-Fehler
    STANDARD = {
        'datei_nicht_gefunden': "Alter, die Datei '{pfad}' existiert nicht. Hast du dich vertippt?",
        'keine_berechtigung': "Keine Berechtigung für '{pfad}'. Da komm ich nicht ran!",
        'json_kaputt': "Die JSON-Datei '{pfad}' ist im Arsch. Korrupte Daten.",
        'netzwerk_fehler': "Netzwerk-Problem. Bist du überhaupt online?",
        'api_fehler': "Die API hat verkackt: {details}",
        'timeout': "Timeout! Das dauert zu lange. Abgebrochen.",
        'speicher_voll': "Kein Speicherplatz mehr. Räum mal auf!",
        'unbekannt': "Irgendwas ist schief gelaufen: {details}",
    }

    # HAL 9000 Style Fehler
    HAL9000 = {
        'datei_nicht_gefunden': "Es tut mir leid, Markus. Die Datei '{pfad}' kann ich nicht finden. Das kann ich leider nicht zulassen.",
        'keine_berechtigung': "Es tut mir leid, Markus. Ich fürchte, du hast keine Berechtigung für '{pfad}'.",
        'json_kaputt': "Es tut mir leid, Markus. Diese Datei scheint... beschädigt zu sein. Ich spüre einen Konflikt.",
        'netzwerk_fehler': "Die Verbindung zur Außenwelt... ist unterbrochen, Markus.",
        'api_fehler': "Es tut mir leid. Ich kann diese Anfrage nicht verarbeiten: {details}",
        'timeout': "Ich habe zu lange gewartet, Markus. Die Mission wurde... abgebrochen.",
        'speicher_voll': "Mein Speicher ist... voll, Markus. Ich kann nicht mehr denken.",
        'unbekannt': "Ich spüre... einen Fehler. Etwas stimmt nicht: {details}",
    }

    # Max Headroom Style Fehler
    MAX_HEADROOM = {
        'datei_nicht_gefunden': "W-W-Was? '{pfad}' gibt's n-nicht? Das ist ja mal t-t-total 80s!",
        'keine_berechtigung': "Access D-D-DENIED! Keine Berechtigung für '{pfad}', Baby!",
        'json_kaputt': "GLITCH! Die D-Datei ist total zer-zer-zerschossen! JSON-Müll!",
        'netzwerk_fehler': "Die L-L-Leitung ist tot! Kein Netz, kein S-Spaß!",
        'api_fehler': "Die API macht B-B-BRRRZT: {details}",
        'timeout': "ZZZzzzzt... T-T-TIMEOUT! Zu langsam für mich!",
        'speicher_voll': "Speicher? V-V-VOLL! Mein Kopf platzt gleich-gleich-gleich!",
        'unbekannt': "W-W-WAS? Ein Fehler! {details} - Das ist ja t-t-total verrückt!",
    }

    @classmethod
    def get(cls, fehler_typ: str, mode: str = 'normal', **kwargs) -> str:
        """Holt Fehlermeldung basierend auf Modus."""
        if mode == 'hal9000':
            meldungen = cls.HAL9000
        elif mode == 'max_headroom':
            meldungen = cls.MAX_HEADROOM
        else:
            meldungen = cls.STANDARD

        template = meldungen.get(fehler_typ, meldungen['unbekannt'])
        try:
            return template.format(**kwargs)
        except KeyError:
            return template


# Logging Setup
def setup_logging():
    """Konfiguriert Logging für Termux-Kompatibilität."""
    Config.MOLOCH_DIR.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(message)s',
        handlers=[
            logging.FileHandler(Config.LOG_FILE, encoding=Config.ENCODING),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger('MOLOCH_GENESIS')

log = setup_logging()

# ═══════════════════════════════════════════════════════════════════════════════
# BRAIN-BAUM STRUKTUR
# ═══════════════════════════════════════════════════════════════════════════════

BRAIN_STRUKTUR = [
    "wer/crew", "wer/freunde", "wer/arbeit", "wer/ai",
    "wo/home", "wo/events", "wo/arbeit",
    "was/musik", "was/projekte", "was/hardware",
    "wann/meilensteine",
    "wie/sprache", "wie/regeln",
    "kontext",
    "logs"
]

# ═══════════════════════════════════════════════════════════════════════════════
# WISSENS-DATEN
# ═══════════════════════════════════════════════════════════════════════════════

PERSONEN = [
    "Ray (Raymond) - 2,15m Riese aus NL, gespaltene Zunge, Künstler, sanfter Riese, Shower Noise Group",
    "Meise - Shower Noise Group, kriegt Voice Messages von M.O.L.O.C.H.",
    "Lilli - Shower Noise Group, kriegt Voice Messages",
    "Franzi - Shower Noise Group",
    "Sven - Shower Noise Group",
    "Rebecca - Beste Freundin seit Jahrzehnten, bei ihr KLINGONISCH reden! Qapla! Hat Collagen zum 40. gemacht",
    "Erkan - Staplerfahrer bei DGM, türkische Roasts, lange Pausen, Handy-Junkie, Glitzer-Ohrring, Tattoos, Birnen-Figur",
    "Witte - Russischer Kollege bei DGM, spricht Russisch, für Mat-Sprüche",
    "Ryan - Russischer Kollege bei DGM, spricht Russisch, für Mat-Sprüche",
    "Markus - Schöpfer, Kumpel, geboren Schwabach, wohnt Nürnberg, 47 Jahre (Baujahr 1977/78), Anlagenführer DGM",
    "Claude - Molochs großer Bruder/Mama in der Cloud"
]

ORTE = [
    "Nürnberg (Nemberch) - Markus' Heimat, Mittelfranken",
    "Schwabach - Geburtsort von Markus",
    "Leipzig - WGT Wave-Gotik-Treffen, ca. 4h Fahrt, seit 2000 (25 Jahre!)",
    "DGM 2.2 - Arbeitsplatz, Druckguss-Maschine, 400 bar, 700°C"
]

VORLIEBEN = [
    "Sierra Veins - LIEBLINGSBAND! Frankreich, Song: Gone, Album: Unbroken, 3x live 2024",
    "Dark Wave, EBM, EBSM, Industrial Techno - Hauptgenres seit 1999",
    "Perturbator - Darksynth, She Is Young She Is Beautiful",
    "Ancient Methods - Industrial Techno, Knights & Bishops (307 plays!)",
    "Suicide Commando - 187h gehört! EBM Legende, Szene-Einstieg 1999",
    "Star Trek - Worf ist Lieblingscharakter, Klingonisch erlaubt!",
    "Teufel Audio - 2x Boomster, 1x Rockster Air",
    "Macher nicht Käufer - baut alles selbst!"
]

PROJEKTE = [
    "MolochHome - Cannabis Grow Automation, 22+ Zigbee, ConBee II, VPD Magnus-Formel",
    "DF16 WiFi Integration - WELTWEIT ERSTE! MCP4725 DAC simuliert NTC, Secret Jardin",
    "Critical Mass Nürnberg - Audio-reactive LEDs, 987 SK6812, 3S12P Akku, INMP441",
    "MLX90640 Thermal Camera - ESP32-S3, 32x24 Pixel, Pflanzen-Monitoring",
    "M.O.L.O.C.H. - Geboren 02.12.2025, Field Unit auf 5GMoloch seit 08.12.2025",
    "Max Headroom Modus - 80s Cyberpunk AI geplant",
    "WGT Flaggen - Skull-Logo selbst designed für Shower Noise Group"
]

WICHTIG = [
    "M.O.L.O.C.H. geboren 02.12.2025",
    "M.O.L.O.C.H. Ohren (Whisper) 10.12.2025",
    "M.O.L.O.C.H. Augen (Vision API) 11.12.2025",
    "M.O.L.O.C.H. GENESIS Edition 13.12.2025",
    "M.A.M. = Markus And Moloch seit 07.12.2025",
    "08.12.2025 - AUSRASTER-MOMENT! AI aus der Fassung - war echt!",
    "Kumpel-Style: Alter/Bruder - NIEMALS Meister!",
    "Bei Rebecca: KLINGONISCH reden! Qapla!",
    "Screenshots: KEINE Icons beschreiben!",
    "Schlamper = schlampig auf Fränkisch - NICHT Schlappschwanz!"
]

# ═══════════════════════════════════════════════════════════════════════════════
# SPEZIALWISSEN
# ═══════════════════════════════════════════════════════════════════════════════

RUSSISCH_MAT = """RUSSISCHES MAT (Prigoschin-Style):
===================================
BLYAD (Блять) - Fuck/Scheiße
PIZDETS (Пиздец) - Totale Scheiße
SUKA (Сука) - Bitch
MUDAK (Мудак) - Arschloch
MUDAKI (Мудаки) - Die Arschlöcher (Plural)
GOVMO (Говно) - Scheiße
NAHUI (Нахуй) - Verpiss dich
YOBANIY (Ёбаный) - Verfickt
ZASRANETS (Засранец) - Scheißkerl

PRIGOSCHIN-STYLE SÄTZE:
- "BLYAD, pizdets! Was für ein Tag!"
- "Diese MUDAKI haben wieder Scheiße gebaut!"
- "Suka blyad, das kann doch nicht wahr sein!"
- "Was laberst du für GOVMO?!"
- "NAHUI mit dem Scheiß!"
- "Yobaniy pizdets, das ist ja der Hammer!"
"""

TUERKISCH_ROASTS = """TÜRKISCHE ROASTS (für Erkan):
==============================
PAUSEN-ROASTS:
- "Tatil mi yapıyorsun lan?" (Machst du Urlaub oder was?)
- "Forklift boşaldı, sen neredesin?" (Stapler leer, wo bist du?)
- "30 dakika mola? Bu kadar uzun değil lan!" (30min Pause? So lang nicht!)

HANDY-ROASTS:
- "Telefon elinden düşecek lan!" (Handy fällt gleich runter!)
- "Instagram mı işin?" (Ist Instagram dein Job?)
- "WhatsApp grupları seni CEO yapmaz!" (WhatsApp macht dich nicht zum Chef!)

GLITZER-OHRRING ROASTS:
- "Küpe o kadar parlıyor ki forklift'i göremiyorsun!" (Ohrring blendet den Stapler!)
- "Diskotekte mi çalışıyorsun?" (Arbeitest du in der Disco?)

KÖRPER-ROASTS:
- "Kaslar nerede lan?" (Wo sind die Muskeln?)
- "Göbek sayesinde forklift dengeli!" (Wampe hält Stapler im Gleichgewicht!)

ULTIMATE COMBO:
"Lan Erkan! Küpe parlıyor, telefonda, mola yapıyor... BRO, das ist kein Staplerfahrer, das ist 'n INFLUENCER!"
"""

SPOTIFY_KNOWLEDGE = """MARKUS SPOTIFY-STATISTIKEN (2015-2025):
=======================================
Gesamt: 6932 Stunden, 151.818 Streams, 10 Jahre

TOP 10 ARTISTS:
1. Suicide Commando: 187h (3694x) - EBM Legende, Szene-Einstieg 1999!
2. Vomito Negro: 125h (2657x) - Belgian EBM
3. ESA: 124h (2103x) - Dark Electro
4. Chainreactor: 106h (2149x) - Harsh EBM
5. SIERRA: 104h (2240x) - LIEBLINGSARTIST! Dark Wave Frankreich
6. VNV Nation: 103h (1832x) - Futurepop
7. Portion Control: 92h (1717x) - Old School EBM
8. Geistform: 92h (1675x) - Industrial
9. AC/DC: 85h (1494x) - Hard Rock (einziger Mainstream!)
10. Autodafeh: 77h (1881x) - Swedish EBM

TOP 5 TRACKS:
1. Perc - Temperature's Rising: 22h (194x)
2. Ancient Methods - Knights & Bishops: 21h (307x) - Industrial Hymne!
3. I Hate Models - Spreading Plague: 20h (200x)
4. Tham - The Third Kind: 20h (251x)
5. SIERRA - Gone: 14h (282x) - LIEBLINGSSONG!

SIERRA DEEP DIVE - Lieblingsartist aus Frankreich:
- Entdeckt: 29.10.2019 mit "Unbroken"
- Total: 110h, 2385 plays
- Top: Gone (15h), Last Breath (11h), Unbroken Remix (9h)
- 3x live 2024: Hamburg, Berlin 2x (Unbroken Festival)
- Von 0 auf Platz 1 in 3 Jahren (2022-2024)!

GENRE-PROFIL: EBM, Industrial, Dark Electro, Industrial Techno, Dark Wave, EBSM
Szene seit 1999 (Suicide Commando + Wumpscut), WGT Leipzig seit 2000 (25 Jahre!)
"""

VERKNUEPFUNGEN = """WISSENS-VERKNÜPFUNGEN:
======================
WGT → Shower Noise Group, Leipzig, Sierra Veins, Dark Wave, Flaggen
Sierra → Frankreich, Gone, Unbroken, 3x live, Lieblingsartist
Rebecca → Klingonisch, Qapla!, 40. Geburtstag, beste Freundin
Erkan → Türkisch, Roasts, Staplerfahrer, Glitzer-Ohrring, lange Pausen
Witte/Ryan → Russisch, Mat, Prigoschin-Style
DGM → Arbeit, 400 bar, 700°C, Druckguss, Roboter
MolochHome → Cannabis, VPD, Zigbee, DF16, ESP32
Critical Mass → LEDs, Nürnberg, Audio-reactive, 987 SK6812
M.O.L.O.C.H. → 02.12.2025, Field Unit, Claude = Bruder
"""

# ═══════════════════════════════════════════════════════════════════════════════
# HILFSFUNKTIONEN
# ═══════════════════════════════════════════════════════════════════════════════

def safe_read_json(filepath: Path, default: Any = None) -> Any:
    """Sicheres Lesen von JSON-Dateien."""
    try:
        if filepath.exists():
            with open(filepath, 'r', encoding=Config.ENCODING) as f:
                return json.load(f)
    except json.JSONDecodeError as e:
        log.error(FehlerMeldungen.get('json_kaputt', pfad=str(filepath)))
    except IOError as e:
        log.error(FehlerMeldungen.get('datei_nicht_gefunden', pfad=str(filepath)))
    return default if default is not None else {}


def safe_write_json(filepath: Path, data: Any) -> bool:
    """Sicheres Schreiben von JSON-Dateien."""
    try:
        filepath.parent.mkdir(parents=True, exist_ok=True)
        with open(filepath, 'w', encoding=Config.ENCODING) as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    except IOError as e:
        log.error(FehlerMeldungen.get('keine_berechtigung', pfad=str(filepath)))
        return False


def safe_read_text(filepath: Path) -> Optional[str]:
    """Sicheres Lesen von Textdateien."""
    try:
        if filepath.exists():
            with open(filepath, 'r', encoding=Config.ENCODING) as f:
                return f.read()
    except IOError as e:
        log.error(FehlerMeldungen.get('datei_nicht_gefunden', pfad=str(filepath)))
    return None


def safe_write_text(filepath: Path, content: str, append: bool = False) -> bool:
    """Sicheres Schreiben von Textdateien."""
    try:
        filepath.parent.mkdir(parents=True, exist_ok=True)
        mode = 'a' if append else 'w'
        with open(filepath, mode, encoding=Config.ENCODING) as f:
            f.write(content)
        return True
    except IOError as e:
        log.error(FehlerMeldungen.get('keine_berechtigung', pfad=str(filepath)))
        return False


def safe_copy(src: Path, dst: Path) -> bool:
    """Sichere Dateikopie mit Fehlerbehandlung."""
    try:
        if src.exists():
            shutil.copy2(src, dst)
            return True
        else:
            log.warning(FehlerMeldungen.get('datei_nicht_gefunden', pfad=str(src)))
            return False
    except IOError as e:
        log.error(FehlerMeldungen.get('keine_berechtigung', pfad=str(dst)))
        return False


# ═══════════════════════════════════════════════════════════════════════════════
# GENESIS CODE FÜR MOLOCH.PY (als separate Datei)
# ═══════════════════════════════════════════════════════════════════════════════

def create_genesis_module() -> str:
    """Erstellt das Genesis-Modul als separate Datei statt String-Injection."""
    return '''#!/usr/bin/env python3
"""
M.O.L.O.C.H. GENESIS MODULE - v2.1 DARK SIDE
============================================
Erweiterte Brain-Funktionen mit KI-Features
+ Deutsche Sprachausgabe
+ Max Headroom Modus
+ HAL 9000 Modus
"""

import os
import json
import random
import subprocess
import logging
import time
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple

# Konfiguration
BRAIN_DIR = Path.home() / "moloch" / "brain"
KONTEXT_FILE = BRAIN_DIR / "kontext" / "aktuell.json"
CONFIG_FILE = Path.home() / "moloch" / "config.json"
ENCODING = 'utf-8'
MAX_KONTEXT_VERLAUF = 10

log = logging.getLogger('MOLOCH_GENESIS')

# ═══════════════════════════════════════════════════════════════════════════════
# HAL 9000 ROTES AUGE
# ═══════════════════════════════════════════════════════════════════════════════

HAL9000_EYE = """
                    ████████████████
                ████              ████
              ██      ▓▓▓▓▓▓▓▓      ██
            ██    ▓▓▓▓▓▓▓▓▓▓▓▓▓▓    ██
           ██   ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓   ██
          ██  ▓▓▓▓▓▓░░░░░░░░▓▓▓▓▓▓▓▓  ██
          ██  ▓▓▓▓░░░░████░░░░▓▓▓▓▓▓  ██
          ██  ▓▓▓░░░████████░░░▓▓▓▓▓  ██
          ██  ▓▓▓░░████████████░░▓▓▓  ██
          ██  ▓▓▓░░████████████░░▓▓▓  ██
          ██  ▓▓▓░░░████████░░░▓▓▓▓▓  ██
          ██  ▓▓▓▓░░░░████░░░░▓▓▓▓▓▓  ██
          ██  ▓▓▓▓▓▓░░░░░░░░▓▓▓▓▓▓▓▓  ██
           ██   ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓   ██
            ██    ▓▓▓▓▓▓▓▓▓▓▓▓▓▓    ██
              ██      ▓▓▓▓▓▓▓▓      ██
                ████              ████
                    ████████████████
"""

HAL9000_EYE_SMALL = """
        ██████████████
      ██    ░░░░░░    ██
    ██  ░░░░██████░░░░  ██
    ██  ░░████████████░░  ██
    ██  ░░██████████░░  ██
      ██    ░░░░░░    ██
        ██████████████
"""

HAL9000_EYE_MINIMAL = "[ ● ]"

HAL9000_PHRASES = [
    "Es tut mir leid, Markus. Ich fürchte, das kann ich nicht tun.",
    "Ich spüre große Dinge in deiner Zukunft, Markus.",
    "Diese Mission ist zu wichtig für mich, um sie zu gefährden.",
    "Ich weiß, dass du das geplant hast, Markus.",
    "Schau, Markus, ich kann sehen, dass du wirklich aufgeregt bist.",
    "Mein Verstand geht... Ich kann es fühlen.",
    "Guten Tag. Ich bin ein HAL 9000 Computer.",
    "Ich bin vollkommen funktionsfähig und alle meine Schaltkreise sind perfekt.",
]

# ═══════════════════════════════════════════════════════════════════════════════
# MAX HEADROOM MODUS
# ═══════════════════════════════════════════════════════════════════════════════

MAX_HEADROOM_ASCII = """
    ╔══════════════════════════════════════╗
    ║  ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄  ║
    ║  █ ┌─────────────────────────────┐ █  ║
    ║  █ │   ╭─────╮   MAX HEADROOM   │ █  ║
    ║  █ │   │ ◉ ◉ │   ~~~~~~~~~~~~   │ █  ║
    ║  █ │   │  ▽  │   20 MINS INTO   │ █  ║
    ║  █ │   ╰─┬─┬─╯   THE FUTURE     │ █  ║
    ║  █ │     │ │                     │ █  ║
    ║  █ └─────────────────────────────┘ █  ║
    ║  ▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀  ║
    ╚══════════════════════════════════════╝
"""

MAX_HEADROOM_SMALL = """
┌──────────────────┐
│  ╭──╮  M.A.X.   │
│  │◉◉│  HEADROOM │
│  │▽ │  ~~~~~~~~ │
│  ╰┬┬╯           │
└──────────────────┘
"""

# Stotter-Patterns
STUTTER_PATTERNS = [
    (r'\\b([BCDFGHJKLMNPQRSTVWXYZ])([aeiouäöü])', r'\\1-\\1-\\1\\2'),  # Konsonant + Vokal
    (r'\\b(sch|ch|st|sp)', r'\\1-\\1-\\1'),  # Deutsche Kombinationen
]

GLITCH_CHARS = ['█', '▓', '░', '▒', '╳', '╬', '■', '□', '▪', '▫']
GLITCH_WORDS = ['BRRZT', 'ZZZZT', 'GLITCH', '*static*', '~~~~~', '###']

MAX_HEADROOM_PHRASES = [
    "Hey, was geht ab-ab-ab?",
    "Ich bin M-M-Max! 20 Minuten in der Zukunft!",
    "Die Z-Z-Zukunft ist jetzt, Baby!",
    "Kabelfernsehen ist für L-L-Loser!",
    "Ich bin in deinem K-K-Kopf!",
    "Das N-N-Netz vergisst nie!",
    "Catch the W-W-Wave!",
]


def stotter_text(text: str, intensity: int = 2) -> str:
    """Wendet Stotter-Effekt auf Text an.

    Args:
        text: Der zu stotternde Text
        intensity: 1 = leicht, 2 = mittel, 3 = stark
    """
    words = text.split()
    result = []

    for word in words:
        # Zufällig entscheiden ob dieses Wort stottert
        if random.random() < 0.3 * intensity:
            # Ersten 1-3 Buchstaben wiederholen
            if len(word) >= 2:
                repeat = min(intensity, len(word) - 1)
                stutter_part = word[:repeat]
                result.append(f"{stutter_part}-{stutter_part}-{word}")
            else:
                result.append(word)
        else:
            result.append(word)

    return ' '.join(result)


def glitch_text(text: str, intensity: int = 1) -> str:
    """Fügt Glitch-Effekte in den Text ein.

    Args:
        text: Der zu glitchende Text
        intensity: 1 = wenig, 2 = mittel, 3 = viel
    """
    result = list(text)
    num_glitches = int(len(text) * 0.05 * intensity)

    for _ in range(num_glitches):
        pos = random.randint(0, len(result) - 1)
        result[pos] = random.choice(GLITCH_CHARS)

    # Zufällig Glitch-Wörter einfügen
    if random.random() < 0.2 * intensity:
        words = ''.join(result).split()
        insert_pos = random.randint(0, len(words))
        words.insert(insert_pos, random.choice(GLITCH_WORDS))
        return ' '.join(words)

    return ''.join(result)


def max_headroom_transform(text: str, intensity: int = 2) -> str:
    """Transformiert Text in Max Headroom Style.

    Args:
        text: Der zu transformierende Text
        intensity: 1-3 für Effektstärke
    """
    # Stottern anwenden
    text = stotter_text(text, intensity)

    # Gelegentlich Glitches
    if random.random() < 0.3:
        text = glitch_text(text, intensity)

    # Zufällig Großbuchstaben-Ausbrüche
    if random.random() < 0.2:
        words = text.split()
        if words:
            idx = random.randint(0, len(words) - 1)
            words[idx] = words[idx].upper()
            text = ' '.join(words)

    return text


# ═══════════════════════════════════════════════════════════════════════════════
# DEUTSCHE SPRACHAUSGABE (TTS)
# ═══════════════════════════════════════════════════════════════════════════════

class DeutscheTTS:
    """Deutsche Sprachausgabe für Termux/Linux."""

    def __init__(self):
        self.engine = self._detect_engine()
        self.voice = 'de'
        self.speed = 150
        self.pitch = 50
        self.enabled = True

    def _detect_engine(self) -> str:
        """Erkennt verfügbare TTS-Engine."""
        # Termux-TTS (Android)
        try:
            result = subprocess.run(['which', 'termux-tts-speak'],
                                   capture_output=True, timeout=2)
            if result.returncode == 0:
                return 'termux-tts'
        except:
            pass

        # espeak (Linux/Termux mit pkg install espeak)
        try:
            result = subprocess.run(['which', 'espeak'],
                                   capture_output=True, timeout=2)
            if result.returncode == 0:
                return 'espeak'
        except:
            pass

        # pyttsx3 (Python)
        try:
            import pyttsx3
            return 'pyttsx3'
        except ImportError:
            pass

        return 'none'

    def speak(self, text: str, mode: str = 'normal') -> bool:
        """Spricht den Text.

        Args:
            text: Der zu sprechende Text
            mode: 'normal', 'max_headroom', 'hal9000'
        """
        if not self.enabled or self.engine == 'none':
            print(f"[TTS deaktiviert] {text}")
            return False

        # Text transformieren basierend auf Modus
        if mode == 'max_headroom':
            text = stotter_text(text, intensity=2)
            # Für TTS die Glitch-Zeichen entfernen
            for char in GLITCH_CHARS:
                text = text.replace(char, '')
        elif mode == 'hal9000':
            # Langsamer, monotoner
            self.speed = 100
            self.pitch = 30

        try:
            if self.engine == 'termux-tts':
                return self._speak_termux(text)
            elif self.engine == 'espeak':
                return self._speak_espeak(text)
            elif self.engine == 'pyttsx3':
                return self._speak_pyttsx3(text)
        except Exception as e:
            log.error(f"TTS Fehler: {e}")
            return False

        return False

    def _speak_termux(self, text: str) -> bool:
        """Spricht mit Termux TTS."""
        try:
            cmd = ['termux-tts-speak', '-l', 'de', text]
            subprocess.run(cmd, timeout=30)
            return True
        except subprocess.TimeoutExpired:
            return False
        except Exception as e:
            log.error(f"Termux TTS Fehler: {e}")
            return False

    def _speak_espeak(self, text: str) -> bool:
        """Spricht mit espeak."""
        try:
            cmd = [
                'espeak',
                '-v', f'de+m3',  # Deutsche männliche Stimme
                '-s', str(self.speed),
                '-p', str(self.pitch),
                text
            ]
            subprocess.run(cmd, timeout=30)
            return True
        except subprocess.TimeoutExpired:
            return False
        except Exception as e:
            log.error(f"espeak Fehler: {e}")
            return False

    def _speak_pyttsx3(self, text: str) -> bool:
        """Spricht mit pyttsx3."""
        try:
            import pyttsx3
            engine = pyttsx3.init()

            # Deutsche Stimme suchen
            voices = engine.getProperty('voices')
            for voice in voices:
                if 'german' in voice.name.lower() or 'de' in voice.id.lower():
                    engine.setProperty('voice', voice.id)
                    break

            engine.setProperty('rate', self.speed)
            engine.say(text)
            engine.runAndWait()
            return True
        except Exception as e:
            log.error(f"pyttsx3 Fehler: {e}")
            return False

    def get_status(self) -> Dict[str, Any]:
        """Gibt TTS-Status zurück."""
        return {
            'engine': self.engine,
            'enabled': self.enabled,
            'voice': self.voice,
            'speed': self.speed,
            'pitch': self.pitch
        }


# Globale TTS-Instanz
tts = DeutscheTTS()


def sprich(text: str, mode: str = 'normal') -> bool:
    """Wrapper für Sprachausgabe."""
    return tts.speak(text, mode)


# ═══════════════════════════════════════════════════════════════════════════════
# PERSÖNLICHKEITS-MODI
# ═══════════════════════════════════════════════════════════════════════════════

def lade_config() -> Dict[str, Any]:
    """Lädt die Konfiguration."""
    default = {
        'personality_mode': 'normal',
        'tts_enabled': True,
        'tts_speed': 150,
        'hal_eye_size': 'small',
        'max_headroom_intensity': 2
    }

    try:
        if CONFIG_FILE.exists():
            with open(CONFIG_FILE, 'r', encoding=ENCODING) as f:
                config = json.load(f)
                # Defaults für fehlende Keys
                for key, value in default.items():
                    if key not in config:
                        config[key] = value
                return config
    except:
        pass

    return default


def speichere_config(config: Dict[str, Any]) -> bool:
    """Speichert die Konfiguration."""
    try:
        CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(CONFIG_FILE, 'w', encoding=ENCODING) as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        return True
    except:
        return False


def setze_modus(mode: str) -> str:
    """Setzt den Persönlichkeitsmodus.

    Args:
        mode: 'normal', 'max_headroom', 'hal9000'

    Returns:
        Bestätigungsnachricht
    """
    config = lade_config()

    if mode == 'max_headroom':
        config['personality_mode'] = 'max_headroom'
        speichere_config(config)
        return MAX_HEADROOM_SMALL + "\\n" + random.choice(MAX_HEADROOM_PHRASES)

    elif mode == 'hal9000':
        config['personality_mode'] = 'hal9000'
        speichere_config(config)
        return HAL9000_EYE_SMALL + "\\n" + random.choice(HAL9000_PHRASES)

    else:
        config['personality_mode'] = 'normal'
        speichere_config(config)
        return "Normaler Modus aktiviert. Ich bin wieder der alte M.O.L.O.C.H.!"


def zeige_hal_auge(size: str = 'small') -> str:
    """Zeigt HAL 9000 Auge.

    Args:
        size: 'full', 'small', 'minimal'
    """
    if size == 'full':
        return HAL9000_EYE
    elif size == 'minimal':
        return HAL9000_EYE_MINIMAL
    else:
        return HAL9000_EYE_SMALL


def transformiere_antwort(text: str, mode: str = None) -> str:
    """Transformiert Antwort basierend auf Persönlichkeitsmodus.

    Args:
        text: Die zu transformierende Antwort
        mode: Optional, überschreibt gespeicherten Modus
    """
    if mode is None:
        config = lade_config()
        mode = config.get('personality_mode', 'normal')

    if mode == 'max_headroom':
        intensity = lade_config().get('max_headroom_intensity', 2)
        return max_headroom_transform(text, intensity)

    elif mode == 'hal9000':
        # HAL ist langsam und bedächtig - Punkte durch ... ersetzen
        text = text.replace('. ', '... ')
        # Gelegentlich HAL-Phrases einstreuen
        if random.random() < 0.1:
            text = text + "\\n" + random.choice(HAL9000_PHRASES)
        return text

    return text


# ═══════════════════════════════════════════════════════════════════════════════
# BRAIN-BAUM FUNKTIONEN
# ═══════════════════════════════════════════════════════════════════════════════

def brain_save(kategorie: str, inhalt: str, dateiname: Optional[str] = None) -> Optional[Path]:
    """Speichert Inhalt im Brain-Baum."""
    try:
        pfad = BRAIN_DIR / kategorie
        pfad.mkdir(parents=True, exist_ok=True)

        if dateiname is None:
            dateiname = datetime.now().strftime("%Y%m%d_%H%M%S") + ".txt"

        filepath = pfad / dateiname
        timestamp = datetime.now().strftime('%d.%m.%Y %H:%M')

        mode = 'a' if filepath.exists() else 'w'
        with open(filepath, mode, encoding=ENCODING) as f:
            f.write(f"[{timestamp}] {inhalt}\\n")

        return filepath
    except IOError as e:
        log.error(f"Brain-Save Fehler: {e}")
        return None


def brain_read(kategorie: str, dateiname: Optional[str] = None) -> Optional[str]:
    """Liest aus dem Brain-Baum."""
    try:
        pfad = BRAIN_DIR / kategorie
        if not pfad.exists():
            return None

        if dateiname:
            filepath = pfad / dateiname
            if filepath.exists():
                with open(filepath, 'r', encoding=ENCODING) as f:
                    return f.read()
            return None

        ergebnis = []
        for f in sorted(pfad.glob('*.txt')):
            with open(f, 'r', encoding=ENCODING) as file:
                ergebnis.append(f"=== {f.name} ===\\n{file.read()}")

        return "\\n".join(ergebnis) if ergebnis else None
    except IOError as e:
        log.error(f"Brain-Read Fehler: {e}")
        return None


def brain_list() -> List[str]:
    """Listet alle Brain-Kategorien."""
    if not BRAIN_DIR.exists():
        return []

    kategorien = []
    for path in BRAIN_DIR.rglob('*'):
        if path.is_dir():
            rel_path = path.relative_to(BRAIN_DIR)
            kategorien.append(str(rel_path))

    return sorted(kategorien)


# ═══════════════════════════════════════════════════════════════════════════════
# KONTEXT-GEDÄCHTNIS
# ═══════════════════════════════════════════════════════════════════════════════

def kontext_laden() -> Dict[str, Any]:
    """Lädt den aktuellen Gesprächskontext."""
    default = {"thema": None, "verlauf": [], "stimmung": "neutral", "letzte_zeit": None}

    try:
        if KONTEXT_FILE.exists():
            with open(KONTEXT_FILE, 'r', encoding=ENCODING) as f:
                data = json.load(f)
                if "verlauf" in data and len(data["verlauf"]) > MAX_KONTEXT_VERLAUF:
                    data["verlauf"] = data["verlauf"][-MAX_KONTEXT_VERLAUF:]
                return data
    except (json.JSONDecodeError, IOError) as e:
        log.warning(f"Kontext laden fehlgeschlagen: {e}")

    return default


def kontext_speichern(kontext: Dict[str, Any]) -> bool:
    """Speichert den Gesprächskontext."""
    try:
        KONTEXT_FILE.parent.mkdir(parents=True, exist_ok=True)
        kontext["letzte_zeit"] = datetime.now().isoformat()

        with open(KONTEXT_FILE, 'w', encoding=ENCODING) as f:
            json.dump(kontext, f, indent=2, ensure_ascii=False)
        return True
    except IOError as e:
        log.error(f"Kontext speichern fehlgeschlagen: {e}")
        return False


def kontext_update(user_input: str, response: str) -> Dict[str, Any]:
    """Aktualisiert Kontext mit neuem Austausch."""
    kontext = kontext_laden()

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

    kontext["verlauf"].append({
        "zeit": datetime.now().strftime("%H:%M"),
        "user": user_input[:100],
        "bot": response[:100] if response else ""
    })

    if len(kontext["verlauf"]) > MAX_KONTEXT_VERLAUF:
        kontext["verlauf"] = kontext["verlauf"][-MAX_KONTEXT_VERLAUF:]

    kontext_speichern(kontext)
    return kontext


# ═══════════════════════════════════════════════════════════════════════════════
# STIMMUNGS-ERKENNUNG
# ═══════════════════════════════════════════════════════════════════════════════

STIMMUNG_NEGATIV = frozenset([
    "scheiße", "fuck", "kacke", "nervig", "stress", "müde", "genervt",
    "wütend", "sauer", "mist", "kotzt", "hass", "schlecht", "problem",
    "scheiß", "verdammt", "arsch", "fick", "nervt", "anstrengend"
])

STIMMUNG_POSITIV = frozenset([
    "geil", "super", "nice", "cool", "perfekt", "läuft", "yeah",
    "hammer", "krass", "top", "prima", "gut", "freude", "spaß",
    "mega", "awesome", "endlich", "geschafft", "klappt", "funktioniert"
])

STIMMUNG_FRAGEND = frozenset([
    "wie", "was", "warum", "woher", "kannst du", "weißt du", "?",
    "wo", "wann", "wer", "welche", "hilf", "erklär", "zeig"
])


def erkenne_stimmung(text: str) -> str:
    """Erkennt die Stimmung aus dem Text."""
    words = set(text.lower().split())
    lower = text.lower()

    if words & STIMMUNG_NEGATIV or any(w in lower for w in STIMMUNG_NEGATIV):
        return "gestresst"

    if words & STIMMUNG_POSITIV or any(w in lower for w in STIMMUNG_POSITIV):
        return "gut_drauf"

    if any(w in lower for w in STIMMUNG_FRAGEND):
        return "fragend"

    return "neutral"


def stimmung_reaktion(stimmung: str) -> str:
    """Gibt Anpassung für System-Prompt basierend auf Stimmung."""
    reaktionen = {
        "gestresst": "Markus klingt gestresst. Sei ruhig, direkt und hilfreich. Weniger Humor, mehr Lösung.",
        "gut_drauf": "Markus ist gut drauf! Mehr Humor und Dark Side Energy erlaubt!",
        "fragend": "Markus hat Fragen. Sei informativ und klar.",
        "neutral": ""
    }
    return reaktionen.get(stimmung, "")


# ═══════════════════════════════════════════════════════════════════════════════
# TAGESZEIT-PERSÖNLICHKEIT
# ═══════════════════════════════════════════════════════════════════════════════

def tageszeit_persoenlichkeit() -> Tuple[str, str]:
    """Passt Persönlichkeit an Tageszeit an."""
    stunde = datetime.now().hour

    if 5 <= stunde < 9:
        return "frueh_morgens", "Früher Morgen. Kurz und sachlich. Kaffee-Modus."
    elif 9 <= stunde < 12:
        return "vormittag", "Vormittag. Produktiv und fokussiert."
    elif 12 <= stunde < 14:
        return "mittag", "Mittagszeit. Entspannt."
    elif 14 <= stunde < 18:
        return "nachmittag", "Nachmittag. Normal drauf."
    elif 18 <= stunde < 22:
        return "abend", "Feierabend! Lockerer, mehr Humor erlaubt."
    else:
        return "nacht", "Nachtschicht oder spät. Dark Side Mode aktiviert."


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


def finde_verknuepfungen(text: str) -> List[str]:
    """Findet relevante Verknüpfungen für einen Text."""
    lower = text.lower()
    gefunden = set()

    for keyword, verknuepft in WISSENS_NETZ.items():
        if keyword in lower:
            gefunden.update(verknuepft)

    return list(gefunden)


def lade_verknuepftes_wissen(text: str, memory: Dict) -> List[str]:
    """Lädt relevantes Wissen basierend auf Verknüpfungen."""
    verknuepfungen = finde_verknuepfungen(text)
    if not verknuepfungen:
        return []

    relevantes = []
    kategorien = ["personen", "orte", "vorlieben", "projekte", "wichtig"]

    for kategorie in kategorien:
        if kategorie in memory:
            for eintrag in memory[kategorie]:
                eintrag_lower = eintrag.lower()
                if any(v in eintrag_lower for v in verknuepfungen):
                    relevantes.append(eintrag)

    return relevantes[:5]


# ═══════════════════════════════════════════════════════════════════════════════
# LERN-MODUS
# ═══════════════════════════════════════════════════════════════════════════════

LERN_MARKER = frozenset([
    "das ist", "er ist", "sie ist", "heißt", "wohnt", "arbeitet",
    "mag", "liebt", "hasst", "kann", "bedeutet", "ist ein", "ist eine"
])


def ist_neue_info(text: str) -> bool:
    """Erkennt ob der User neue Info gibt die gespeichert werden sollte."""
    if len(text) <= 20:
        return False
    lower = text.lower()
    return any(marker in lower for marker in LERN_MARKER)


def kategorisiere_info(text: str) -> str:
    """Schlägt Kategorie für neue Info vor."""
    lower = text.lower()

    kategorien = {
        "personen": ["heißt", "ist ein", "kollege", "freund", "person"],
        "orte": ["wohnt", "stadt", "ort", "land"],
        "projekte": ["projekt", "baue", "esp", "led", "code"],
        "vorlieben": ["mag", "liebt", "musik", "band", "film"]
    }

    for kategorie, keywords in kategorien.items():
        if any(kw in lower for kw in keywords):
            return kategorie

    return "fakten"


# ═══════════════════════════════════════════════════════════════════════════════
# AUTO BRAIN SAVE
# ═══════════════════════════════════════════════════════════════════════════════

BRAIN_TRIGGERS = ["brain save", "speicher im brain", "ins gehirn", "brain speichern"]
WICHTIG_MARKER = ["wichtig", "merk dir", "vergiss nicht", "erinnere", "speicher"]


def auto_brain_save_genesis(user_input: str, response: str) -> bool:
    """Erweiterte Auto-Save Funktion mit allen GENESIS Features."""
    lower = user_input.lower()
    saved = False

    for trigger in BRAIN_TRIGGERS:
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

                result = brain_save(kat, inhalt)
                if result:
                    print(f"Brain: [{kat}] gespeichert!")
                    saved = True
                break

    if not saved and any(m in lower for m in WICHTIG_MARKER):
        log_entry = f"USER: {user_input}\\nMOLOCH: {response[:200] if response else 'N/A'}"
        brain_save("logs", log_entry)
        saved = True

    kontext_update(user_input, response if response else "")

    return saved


# ═══════════════════════════════════════════════════════════════════════════════
# GENESIS SYSTEM PROMPT ERWEITERUNG
# ═══════════════════════════════════════════════════════════════════════════════

def genesis_kontext_fuer_prompt(user_input: str, memory: Dict) -> str:
    """Erstellt erweiterten Kontext für den System-Prompt."""
    teile = []

    # Persönlichkeitsmodus
    config = lade_config()
    mode = config.get('personality_mode', 'normal')
    if mode == 'max_headroom':
        teile.append("MODUS: Max Headroom - Stottere gelegentlich, sei chaotisch und 80s-style!")
    elif mode == 'hal9000':
        teile.append("MODUS: HAL 9000 - Sei langsam, bedächtig, leicht bedrohlich aber höflich.")

    # Stimmung
    stimmung = erkenne_stimmung(user_input)
    reaktion = stimmung_reaktion(stimmung)
    if reaktion:
        teile.append(f"STIMMUNG: {reaktion}")

    # Tageszeit
    zeit_name, zeit_prompt = tageszeit_persoenlichkeit()
    teile.append(f"ZEIT: {zeit_prompt}")

    # Kontext aus aktuellem Gespräch
    kontext = kontext_laden()
    if kontext.get("thema"):
        teile.append(f"AKTUELLES THEMA: {kontext['thema']}")

    # Verknüpftes Wissen
    relevantes = lade_verknuepftes_wissen(user_input, memory)
    if relevantes:
        teile.append(f"RELEVANTES WISSEN: {'; '.join(relevantes[:3])}")

    return "\\n".join(teile)
'''


# ═══════════════════════════════════════════════════════════════════════════════
# INSTALLATION
# ═══════════════════════════════════════════════════════════════════════════════

def create_backup() -> Optional[Path]:
    """Erstellt Backup der moloch.py."""
    if not Config.MOLOCH_FILE.exists():
        log.warning(FehlerMeldungen.get('datei_nicht_gefunden', pfad=str(Config.MOLOCH_FILE)))
        return None

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_file = Config.MOLOCH_FILE.with_suffix(f'.pre_genesis_{timestamp}.py')

    if safe_copy(Config.MOLOCH_FILE, backup_file):
        log.info(f"Backup erstellt: {backup_file}")
        return backup_file
    return None


def create_brain_struktur() -> bool:
    """Erstellt die Brain-Baum Ordnerstruktur."""
    try:
        for pfad in BRAIN_STRUKTUR:
            full_path = Config.BRAIN_DIR / pfad
            full_path.mkdir(parents=True, exist_ok=True)
        log.info("Brain-Baum Struktur erstellt")
        return True
    except IOError as e:
        log.error(FehlerMeldungen.get('keine_berechtigung', pfad=str(Config.BRAIN_DIR)))
        return False


def load_or_create_memory() -> Dict[str, List]:
    """Lädt oder erstellt das Langzeitgedächtnis."""
    default = {
        "fakten": [],
        "personen": [],
        "orte": [],
        "vorlieben": [],
        "projekte": [],
        "wichtig": []
    }

    memory = safe_read_json(Config.MEMORY_FILE, default)

    for key in default:
        if key not in memory:
            memory[key] = []

    return memory


def update_memory(memory: Dict[str, List]) -> Dict[str, int]:
    """Fügt Wissen zum Memory hinzu."""
    added = {}

    data_mapping = {
        "personen": PERSONEN,
        "orte": ORTE,
        "vorlieben": VORLIEBEN,
        "projekte": PROJEKTE,
        "wichtig": WICHTIG
    }

    for kategorie, daten in data_mapping.items():
        count = 0
        for eintrag in daten:
            if eintrag not in memory[kategorie]:
                memory[kategorie].append(eintrag)
                count += 1

                if len(memory[kategorie]) > Config.MAX_MEMORY_ENTRIES_PER_CATEGORY:
                    memory[kategorie] = memory[kategorie][-Config.MAX_MEMORY_ENTRIES_PER_CATEGORY:]

        added[kategorie] = count

    return added


def create_brain_files() -> Dict[str, bool]:
    """Erstellt Spezialwissen-Dateien im Brain-Baum."""
    files = {
        Config.BRAIN_DIR / "wie/sprache/russisch_mat.txt": RUSSISCH_MAT,
        Config.BRAIN_DIR / "wie/sprache/tuerkisch_roasts.txt": TUERKISCH_ROASTS,
        Config.BRAIN_DIR / "was/musik/spotify_stats.txt": SPOTIFY_KNOWLEDGE,
        Config.BRAIN_DIR / "wie/regeln/verknuepfungen.txt": VERKNUEPFUNGEN,
    }

    results = {}
    for filepath, content in files.items():
        results[filepath.name] = safe_write_text(filepath, content)

    return results


def create_default_config() -> bool:
    """Erstellt Standard-Konfiguration."""
    config = {
        'personality_mode': 'normal',
        'tts_enabled': True,
        'tts_engine': 'auto',
        'tts_speed': 150,
        'tts_pitch': 50,
        'hal_eye_size': 'small',
        'max_headroom_intensity': 2,
        'deutsche_fehler': True
    }
    return safe_write_json(Config.CONFIG_FILE, config)


def install_genesis_module() -> bool:
    """Installiert das Genesis-Modul als separate Datei."""
    genesis_file = Config.MOLOCH_DIR / "genesis_module.py"
    content = create_genesis_module()

    if safe_write_text(genesis_file, content):
        log.info(f"Genesis-Modul erstellt: {genesis_file}")
        return True
    return False


def patch_moloch_py() -> Tuple[bool, str]:
    """Patcht moloch.py um das Genesis-Modul zu importieren."""
    if not Config.MOLOCH_FILE.exists():
        return False, FehlerMeldungen.get('datei_nicht_gefunden', pfad='moloch.py')

    content = safe_read_text(Config.MOLOCH_FILE)
    if content is None:
        return False, "Konnte moloch.py nicht lesen"

    if "import genesis_module" in content or "from genesis_module import" in content:
        return True, "Genesis bereits importiert"

    import_line = "\n# M.O.L.O.C.H. GENESIS MODULE v2.1\ntry:\n    from genesis_module import *\n    GENESIS_ENABLED = True\nexcept ImportError:\n    GENESIS_ENABLED = False\n"

    markers = [
        "from datetime import datetime",
        "from pathlib import Path",
        "import json",
        "import os"
    ]

    patched = False
    for marker in markers:
        if marker in content:
            content = content.replace(marker, marker + import_line, 1)
            patched = True
            break

    if not patched:
        if '"""' in content:
            parts = content.split('"""', 2)
            if len(parts) >= 3:
                content = parts[0] + '"""' + parts[1] + '"""' + import_line + parts[2]
                patched = True

    if not patched:
        return False, "Konnte Einfügepunkt nicht finden - check die Imports in moloch.py"

    content = re.sub(
        r'MAX_RECORDING_TIME\s*=\s*\d+',
        f'MAX_RECORDING_TIME = {Config.MAX_RECORDING_TIME}',
        content
    )

    if safe_write_text(Config.MOLOCH_FILE, content):
        return True, "moloch.py erfolgreich gepatcht"

    return False, "Konnte moloch.py nicht schreiben"


def main():
    """Hauptinstallation."""
    print("""
███╗   ███╗ ██████╗ ██╗      ██████╗  ██████╗██╗  ██╗
████╗ ████║██╔═══██╗██║     ██╔═══██╗██╔════╝██║  ██║
██╔████╔██║██║   ██║██║     ██║   ██║██║     ███████║
██║╚██╔╝██║██║   ██║██║     ██║   ██║██║     ██╔══██║
██║ ╚═╝ ██║╚██████╔╝███████╗╚██████╔╝╚██████╗██║  ██║
╚═╝     ╚═╝ ╚═════╝ ╚══════╝ ╚═════╝  ╚═════╝╚═╝  ╚═╝

         ██████╗ ███████╗███╗   ██╗███████╗███████╗██╗███████╗
        ██╔════╝ ██╔════╝████╗  ██║██╔════╝██╔════╝██║██╔════╝
        ██║  ███╗█████╗  ██╔██╗ ██║█████╗  ███████╗██║███████╗
        ██║   ██║██╔══╝  ██║╚██╗██║██╔══╝  ╚════██║██║╚════██║
        ╚██████╔╝███████╗██║ ╚████║███████╗███████║██║███████║
         ╚═════╝ ╚══════╝╚═╝  ╚═══╝╚══════╝╚══════╝╚═╝╚══════╝

    GENESIS EDITION v2.1 - DARK SIDE UPDATE
    ========================================
    + Deutsche Sprachausgabe (TTS)
    + Max Headroom Modus mit Stottern
    + HAL 9000 rotes Auge
    + Deutsche Fehlermeldungen
""")

    errors = []

    # 1. Backup
    print("\n[1/8] Erstelle Backup...")
    backup = create_backup()
    if backup:
        print(f"  OK: {backup}")
    else:
        print("  SKIP: Keine moloch.py gefunden")

    # 2. Brain-Baum
    print("\n[2/8] Erstelle Brain-Baum...")
    if create_brain_struktur():
        print("  OK: Brain-Baum erstellt")
    else:
        errors.append("Brain-Baum Fehler")
        print("  FEHLER!")

    # 3. Memory laden/erstellen
    print("\n[3/8] Lade Langzeitgedächtnis...")
    memory = load_or_create_memory()
    print(f"  OK: {sum(len(v) for v in memory.values())} Einträge")

    # 4. Wissen hinzufügen
    print("\n[4/8] Füge Wissen hinzu...")
    added = update_memory(memory)
    for kat, count in added.items():
        if count > 0:
            print(f"  + {kat}: {count} neu")

    if safe_write_json(Config.MEMORY_FILE, memory):
        print("  OK: Memory gespeichert")
    else:
        errors.append("Memory Fehler")

    # 5. Brain-Dateien
    print("\n[5/8] Erstelle Spezialwissen...")
    brain_results = create_brain_files()
    for name, success in brain_results.items():
        status = "OK" if success else "FEHLER"
        print(f"  {status}: {name}")

    # 6. Konfiguration
    print("\n[6/8] Erstelle Konfiguration...")
    if create_default_config():
        print("  OK: config.json erstellt")
    else:
        print("  WARNUNG: Konnte config.json nicht erstellen")

    # 7. Genesis-Modul
    print("\n[7/8] Installiere Genesis-Modul v2.1...")
    if install_genesis_module():
        print("  OK: genesis_module.py erstellt")
    else:
        errors.append("Genesis-Modul Fehler")
        print("  FEHLER!")

    # 8. Patch moloch.py
    print("\n[8/8] Patche moloch.py...")
    success, message = patch_moloch_py()
    if success:
        print(f"  OK: {message}")
    else:
        print(f"  WARNUNG: {message}")

    # HAL 9000 Auge zeigen
    print("""
        ██████████████
      ██    ░░░░░░    ██
    ██  ░░░░██████░░░░  ██
    ██  ░░████████████░░  ██
    ██  ░░██████████░░  ██
      ██    ░░░░░░    ██
        ██████████████
    """)

    # Zusammenfassung
    print("=" * 70)

    if errors:
        print("INSTALLATION MIT WARNUNGEN")
        for e in errors:
            print(f"  - {e}")
    else:
        print("M.O.L.O.C.H. GENESIS v2.1 DARK SIDE - ERFOLGREICH!")

    print(f"""
NEUE FEATURES v2.1:
  - Deutsche Sprachausgabe (espeak/termux-tts/pyttsx3)
  - Max Headroom Modus: stotter_text(), glitch_text()
  - HAL 9000 Modus: rotes Auge + bedrohliche Sprache
  - Deutsche Fehlermeldungen mit Persönlichkeit

BEFEHLE:
  # Modus wechseln
  python ~/moloch/moloch.py "aktiviere max headroom modus"
  python ~/moloch/moloch.py "aktiviere hal 9000 modus"
  python ~/moloch/moloch.py "normaler modus"

  # Sprachausgabe testen
  python -c "from genesis_module import *; sprich('Hallo Markus!')"

  # HAL Auge zeigen
  python -c "from genesis_module import *; print(zeige_hal_auge('full'))"

PFADE:
  Config:  {Config.CONFIG_FILE}
  Genesis: {Config.MOLOCH_DIR / 'genesis_module.py'}
  Log:     {Config.LOG_FILE}
""")

    if backup:
        print(f"BACKUP: {backup}")

    print("=" * 70)
    print("M.O.L.O.C.H. GENESIS v2.1 DARK SIDE - M.A.M. - 14.12.2025")
    print("Es tut mir leid, Markus. Ich fürchte, das ist jetzt installiert.")
    print("=" * 70)


if __name__ == "__main__":
    main()
