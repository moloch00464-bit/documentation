#!/usr/bin/env python3
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
    (r'\b([BCDFGHJKLMNPQRSTVWXYZ])([aeiouäöü])', r'\1-\1-\1\2'),  # Konsonant + Vokal
    (r'\b(sch|ch|st|sp)', r'\1-\1-\1'),  # Deutsche Kombinationen
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

    # Glitch-Effekte nur ersetzen, nicht hinzufügen (um Länge zu behalten)
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
        phrase = random.choice(MAX_HEADROOM_PHRASES)
        response = MAX_HEADROOM_SMALL + "\n" + phrase + "\nMax Headroom Modus aktiviert!"
        return response

    elif mode == 'hal9000':
        config['personality_mode'] = 'hal9000'
        speichere_config(config)
        phrase = random.choice(HAL9000_PHRASES)
        response = HAL9000_EYE_SMALL + "\n" + phrase + "\nHAL 9000 Modus aktiviert!"
        return response

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
            text = text + "\n" + random.choice(HAL9000_PHRASES)
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
            f.write(f"[{timestamp}] {inhalt}\n")

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
                ergebnis.append(f"=== {f.name} ===\n{file.read()}")

        return "\n".join(ergebnis) if ergebnis else None
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
        log_entry = f"USER: {user_input}\nMOLOCH: {response[:200] if response else 'N/A'}"
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

    return "\n".join(teile)
