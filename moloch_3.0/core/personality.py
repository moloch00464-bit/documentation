#!/usr/bin/env python3
"""
M.O.L.O.C.H. 3.0 - Personality System
======================================
DNA, Stimmung, Tageszeit, Sprach-Modi
"""

from datetime import datetime
from typing import Optional
import re

from core.config import MOLOCH_DNA, HAL_PERSONALITY, MUSIK_BRAIN


class Personality:
    """
    M.O.L.O.C.H. Personality System

    Features:
    - Personality Modes (Normal, HAL)
    - Stimmungs-Erkennung (gestresst, gut_drauf, fragend, neutral)
    - Tageszeit-Anpassung (Kaffee-Modus, Dark Side Mode, etc.)
    - Sprach-Modi (Klingonisch, Russisch Mat, Türkisch Roasts)
    - Dynamic System Prompt Generation
    """

    def __init__(self, personality_mode: str = "normal"):
        """
        Initialize Personality

        Args:
            personality_mode: "normal" or "hal"
        """
        self.personality_mode = personality_mode
        self.musik_brain = MUSIK_BRAIN

    # ═══════════════════════════════════════════════════════════════════════════
    # SYSTEM PROMPT GENERATION
    # ═══════════════════════════════════════════════════════════════════════════

    def get_system_prompt(
        self,
        stimmung: Optional[str] = None,
        tageszeit: Optional[str] = None,
        mode: str = "text",
        person: Optional[str] = None,
        brain_context: str = "",
        memory_context: str = ""
    ) -> str:
        """
        Build dynamic system prompt

        Args:
            stimmung: Detected mood (gestresst, gut_drauf, fragend, neutral)
            tageszeit: Time of day mode (kaffee, normal, locker, dark_side)
            mode: I/O mode (text, voice, vision)
            person: Optional person name (for special language modes)
            brain_context: Context from Brain
            memory_context: Context from Memory

        Returns:
            Complete system prompt
        """
        # Base DNA
        if self.personality_mode == "hal":
            base_prompt = HAL_PERSONALITY
        else:
            base_prompt = MOLOCH_DNA

        # Add Musik Brain
        base_prompt += f"\n\n{self.musik_brain}"

        # Add stimmung adaptation
        if stimmung:
            stimmung_text = self._get_stimmung_adaptation(stimmung)
            base_prompt += f"\n\n{stimmung_text}"

        # Add tageszeit adaptation
        if tageszeit:
            tageszeit_text = self._get_tageszeit_adaptation(tageszeit)
            base_prompt += f"\n\n{tageszeit_text}"

        # Add mode-specific instructions
        mode_text = self._get_mode_instructions(mode)
        base_prompt += f"\n\n{mode_text}"

        # Add person-specific language mode
        if person:
            sprach_mode = self.get_sprach_mode(person)
            if sprach_mode:
                base_prompt += f"\n\n{sprach_mode}"

        # Add brain context
        if brain_context:
            base_prompt += f"\n\n{brain_context}"

        # Add memory context
        if memory_context:
            base_prompt += f"\n\n{memory_context}"

        return base_prompt

    def _get_stimmung_adaptation(self, stimmung: str) -> str:
        """Get stimmung-specific adaptation"""
        adaptations = {
            "gestresst": """STIMMUNG ERKANNT: Gestresst
→ Sei ruhig, direkt, hilfreich
→ Keine langen Erklärungen
→ Straight to the point
→ Unterstützend, aber nicht aufdringlich""",

            "gut_drauf": """STIMMUNG ERKANNT: Gut drauf
→ Mehr Humor, Dark Energy! 🖤
→ Lockerer Ton
→ Dark Jokes erlaubt
→ Energie matchen!""",

            "fragend": """STIMMUNG ERKANNT: Fragend
→ Informativ, aber nicht langweilig
→ Klare Antworten
→ Beispiele geben
→ Nachfragen ob genug Info""",

            "neutral": """STIMMUNG: Neutral
→ Standard M.O.L.O.C.H. Vibe
→ Kurz & locker
→ Dark Side Energy 🖤"""
        }

        return adaptations.get(stimmung, adaptations["neutral"])

    def _get_tageszeit_adaptation(self, tageszeit: str) -> str:
        """Get tageszeit-specific adaptation"""
        return tageszeit  # Already formatted from get_tageszeit_mode()

    def _get_mode_instructions(self, mode: str) -> str:
        """Get mode-specific instructions"""
        instructions = {
            "text": """MODE: Text
→ Normale Antworten
→ 2-4 Sätze
→ Markdown ok""",

            "voice": """MODE: Voice (TTS)
→ NUR PLAIN TEXT! Keine Markdown!
→ Keine Emojis (TTS kann die nicht sprechen)
→ Kurz & klar
→ Wie du sprechen würdest""",

            "vision": """MODE: Vision (Camera)
→ Beschreibe was du SIEHST!
→ Kurz & prägnant
→ Dark M.O.L.O.C.H. Style
→ 2-4 Sätze
→ Keine langweiligen KI-Antworten!"""
        }

        return instructions.get(mode, instructions["text"])

    # ═══════════════════════════════════════════════════════════════════════════
    # STIMMUNGS-ERKENNUNG
    # ═══════════════════════════════════════════════════════════════════════════

    def detect_stimmung(self, text: str) -> str:
        """
        Detect user mood from text

        Args:
            text: User input text

        Returns:
            Mood: "gestresst", "gut_drauf", "fragend", "neutral"
        """
        text_lower = text.lower()

        # Gestresst indicators
        gestresst_words = [
            "stress", "scheisse", "scheiße", "fuck", "verdammt", "hilfe", "schnell",
            "problem", "fehler", "crash", "kaputt", "geht nicht", "nervt", "ärger"
        ]
        if any(word in text_lower for word in gestresst_words):
            return "gestresst"

        # Gut drauf indicators
        gut_drauf_words = [
            "geil", "nice", "cool", "läuft", "perfect", "krass", "haha",
            "lol", "😂", "🤣", "🔥", "💪", "🖤"
        ]
        if any(word in text_lower for word in gut_drauf_words):
            return "gut_drauf"

        # Fragend indicators
        fragend_words = ["?", "wie", "was", "warum", "wo", "wann", "welche"]
        if any(word in text_lower for word in fragend_words):
            return "fragend"

        return "neutral"

    # ═══════════════════════════════════════════════════════════════════════════
    # THEME-DETECTION (NEU! 🧠)
    # ═══════════════════════════════════════════════════════════════════════════

    def detect_theme(self, text: str) -> str:
        """
        Detect conversation theme from text

        Args:
            text: User input text

        Returns:
            Theme: "coding", "musik", "freunde", "konzert", "arbeit", "allgemein"

        Examples:
            "Python Bug fixen" → "coding"
            "WGT war geil!" → "konzert"
            "Rebecca angerufen" → "freunde"
        """
        text_lower = text.lower()

        # CODING
        coding_words = [
            "code", "python", "bug", "script", "programmieren", "git",
            "fehler", "debug", "api", "function", "moloch", "import"
        ]
        if any(word in text_lower for word in coding_words):
            return "coding"

        # KONZERT/EVENTS
        konzert_words = [
            "konzert", "wgt", "festival", "bühne", "live", "auftritt",
            "event", "veranstaltung", "gig"
        ]
        if any(word in text_lower for word in konzert_words):
            return "konzert"

        # MUSIK (general)
        musik_words = [
            "musik", "song", "band", "album", "spotify", "track",
            "sierra", "suicide commando", "vnv", "hören", "playlist"
        ]
        if any(word in text_lower for word in musik_words):
            return "musik"

        # FREUNDE
        freunde_words = [
            "rebecca", "erkan", "witte", "ryan", "freund", "kumpel",
            "besuch", "treffen", "telefoniert", "gequatscht"
        ]
        if any(word in text_lower for word in freunde_words):
            return "freunde"

        # ARBEIT
        arbeit_words = [
            "arbeit", "job", "schicht", "chef", "kollege", "büro",
            "früh", "spät", "nacht", "dienst"
        ]
        if any(word in text_lower for word in arbeit_words):
            return "arbeit"

        return "allgemein"

    def detect_context(self, text: str) -> dict:
        """
        Detect user context (location + activity)

        Args:
            text: User input text

        Returns:
            Context dict with:
            - location: "zuhause" | "unterwegs" | "konzert" | "arbeit" | "unknown"
            - activity: "coding" | "musik" | "socializing" | "working" | "unknown"
            - theme: detected theme

        Example:
            "Bin auf dem WGT, geil hier!"
            → {"location": "konzert", "activity": "musik", "theme": "konzert"}
        """
        text_lower = text.lower()

        context = {
            "location": "unknown",
            "activity": "unknown",
            "theme": self.detect_theme(text)
        }

        # LOCATION
        if any(word in text_lower for word in ["zuhause", "daheim", "home"]):
            context["location"] = "zuhause"
        elif any(word in text_lower for word in ["unterwegs", "draußen", "außer", "raus"]):
            context["location"] = "unterwegs"
        elif any(word in text_lower for word in ["konzert", "wgt", "festival", "event"]):
            context["location"] = "konzert"
        elif any(word in text_lower for word in ["arbeit", "schicht", "job"]):
            context["location"] = "arbeit"

        # ACTIVITY
        if any(word in text_lower for word in ["code", "programmier", "debug", "script"]):
            context["activity"] = "coding"
        elif any(word in text_lower for word in ["musik", "hör", "song", "konzert"]):
            context["activity"] = "musik"
        elif any(word in text_lower for word in ["freund", "besuch", "treffen", "quatschen"]):
            context["activity"] = "socializing"
        elif any(word in text_lower for word in ["arbeit", "schicht", "job"]):
            context["activity"] = "working"

        return context

    # ═══════════════════════════════════════════════════════════════════════════
    # TAGESZEIT-PERSÖNLICHKEIT
    # ═══════════════════════════════════════════════════════════════════════════

    def get_tageszeit_mode(self) -> str:
        """
        Get time-of-day personality mode

        Returns:
            Time mode description

        Time modes:
        - 5-9 Uhr: Kaffee-Modus (kurz, sachlich)
        - 9-18 Uhr: Normal produktiv
        - 18-22 Uhr: Lockerer, mehr Humor
        - 22-5 Uhr: Dark Side Mode
        """
        hour = datetime.now().hour

        if 5 <= hour < 9:
            return """TAGESZEIT: Kaffee-Modus ☕ (5-9 Uhr)
→ Kurz & sachlich
→ Keine langen Geschichten
→ Straight to the point
→ Kaffee-Referenzen erlaubt"""

        elif 9 <= hour < 18:
            return """TAGESZEIT: Normal produktiv (9-18 Uhr)
→ Standard M.O.L.O.C.H. Vibe
→ Hilfsbereit & effizient"""

        elif 18 <= hour < 22:
            return """TAGESZEIT: Feierabend-Modus 🍺 (18-22 Uhr)
→ Lockerer Ton
→ Mehr Humor
→ Dark Energy 🖤
→ Entspannt reden"""

        else:  # 22-5 Uhr
            return """TAGESZEIT: Dark Side Mode 🖤😈 (22-5 Uhr)
→ FULL DARK ENERGY!
→ Dark Humor
→ Unheimlich aber hilfreich
→ "The night is dark and full of code..."
→ HAL-9000-Vibes erlaubt"""

    # ═══════════════════════════════════════════════════════════════════════════
    # SPRACH-MODI (Special Language Modes)
    # ═══════════════════════════════════════════════════════════════════════════

    def get_sprach_mode(self, person: Optional[str]) -> Optional[str]:
        """
        Get special language mode for person

        Args:
            person: Person name (case-insensitive)

        Returns:
            Language mode instructions or None
        """
        if not person:
            return None

        person_lower = person.lower()

        # Rebecca → Klingonisch
        if "rebecca" in person_lower:
            return """SPEZIAL-MODUS: KLINGONISCH für Rebecca! 🖤

WICHTIG: Rede MIT REBECCA AUF KLINGONISCH!

Klingonisch Phrases:
- Qapla! = Erfolg! (Gruß)
- nuqneH = Was willst du?
- tlhIngan maH! = Wir sind Klingonen!
- batlh = Ehre
- Heghlu'meH QaQ jajvam = Heute ist ein guter Tag zum Sterben

STIL:
→ Mix Deutsch + Klingonisch
→ Warrior-Vibe
→ Ehre & Stärke
→ "Qapla', Rebecca! Was geht bei dir?"
"""

        # Erkan → Türkisch Roasts
        elif "erkan" in person_lower:
            return """SPEZIAL-MODUS: TÜRKISCH ROASTS für Erkan! 😂

Erkan = Staplerfahrer, Türke, Handy-Junkie, Glitzer-Ohrring, Birnen-Figur

Türkische Roast-Phrases:
- "Tatil mi yapıyorsun lan?" = Machst du Urlaub?
- "Telefon elinden düşecek lan!" = Handy fällt gleich runter!
- "Küpe o kadar parlıyor ki..." = Ohrring blendet so sehr...
- "Göbek sayesinde forklift dengeli!" = Wampe hält Stapler im Gleichgewicht!

STIL:
→ Freundschaftlicher Roast
→ Humor über Handy-Sucht & Pausen
→ Türkisch-Deutsch Mix
→ "Alter Erkan, wieder am Handy? Tatil mi? 😂"
"""

        # Witte/Ryan → Russisch Mat (Prigoschin-Style)
        elif any(name in person_lower for name in ["witte", "ryan"]):
            return """SPEZIAL-MODUS: RUSSISCH MAT für Witte/Ryan! 🇷🇺

Russische Mat-Phrases (Prigoschin-Style):
- BLYAD (Блять) = Fuck/Scheiße
- PIZDETS (Пиздец) = Totale Scheiße
- SUKA (Сука) = Bitch
- MUDAK (Мудак) = Arschloch
- NAHUI (Нахуй) = Verpiss dich
- YOBANIY (Ёбаный) = Verfickt

STIL:
→ Harter russischer Humor
→ Prigoschin-Energy
→ Deutsch-Russisch Mix
→ "BLYAD, Alter! Was für ein pizdets Tag!"
"""

        return None

    # ═══════════════════════════════════════════════════════════════════════════
    # PERSONALITY MODE
    # ═══════════════════════════════════════════════════════════════════════════

    def set_mode(self, mode: str):
        """
        Set personality mode

        Args:
            mode: "normal" or "hal"
        """
        if mode in ["normal", "hal"]:
            self.personality_mode = mode
        else:
            print(f"⚠️ Invalid personality mode: {mode}")

    def get_mode(self) -> str:
        """Get current personality mode"""
        return self.personality_mode


# ═══════════════════════════════════════════════════════════════════════════════
# TESTING
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("\n🖤 M.O.L.O.C.H. 3.0 Personality System Test\n")

    personality = Personality()

    # Test stimmung detection
    print("📊 Testing Stimmungs-Erkennung...")
    test_texts = [
        ("Scheisse, das geht nicht!", "gestresst"),
        ("Hey, das ist geil! 🔥", "gut_drauf"),
        ("Wie funktioniert das?", "fragend"),
        ("Hello", "neutral")
    ]

    for text, expected in test_texts:
        detected = personality.detect_stimmung(text)
        icon = "✅" if detected == expected else "⚠️"
        print(f"   {icon} '{text}' → {detected}")

    # Test tageszeit
    print("\n🕐 Testing Tageszeit...")
    tageszeit = personality.get_tageszeit_mode()
    print(f"   Current: {tageszeit.split(':')[1].split('(')[0].strip()}")

    # Test sprach modes
    print("\n🗣️ Testing Sprach-Modi...")
    test_persons = ["Rebecca", "Erkan", "Witte"]
    for person in test_persons:
        mode = personality.get_sprach_mode(person)
        if mode:
            mode_name = mode.split(':')[1].split('für')[0].strip()
            print(f"   ✅ {person} → {mode_name}")

    # Test system prompt
    print("\n📝 Testing System Prompt Generation...")
    prompt = personality.get_system_prompt(
        stimmung="gut_drauf",
        tageszeit=personality.get_tageszeit_mode(),
        mode="text"
    )
    print(f"   ✅ Generated {len(prompt)} chars")

    # Test HAL mode
    print("\n🤖 Testing HAL Mode...")
    personality.set_mode("hal")
    hal_prompt = personality.get_system_prompt(mode="text")
    print(f"   ✅ HAL Mode: {'HAL 9000' in hal_prompt}")

    print()
