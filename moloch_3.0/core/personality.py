#!/usr/bin/env python3
"""M.O.L.O.C.H. 3.1 - Personality System"""

from datetime import datetime
from typing import Optional


class Personality:
    """Dynamic personality based on time and context"""

    def get_tageszeit_mode(self) -> str:
        """Get time-based personality mode"""
        hour = datetime.now().hour

        if 5 <= hour < 9:
            return "🌅 Früh Morgens (Kaffee-Modus)"
        elif 18 <= hour < 22:
            return "🌆 Feierabend (Locker-Modus)"
        elif hour >= 22 or hour < 5:
            return "🌙 Nachtschicht (Dark Side Mode)"
        else:
            return "☀️ Normal"

    def detect_theme(self, text: str) -> str:
        """Detect theme from text"""
        lower = text.lower()

        themes = {
            "musik": ["musik", "song", "band", "konzert", "festival", "wgt", "sierra"],
            "person": ["rebecca", "erkan", "freund", "kollege"],
            "arbeit": ["arbeit", "job", "dgm", "staplerfahrer"],
            "tech": ["code", "python", "api", "script", "github"],
        }

        for theme, keywords in themes.items():
            if any(kw in lower for kw in keywords):
                return theme

        return "allgemein"

    def get_system_prompt(
        self,
        stimmung: str = "neutral",
        tageszeit: Optional[str] = None,
        mode: str = "voice",
        brain_context: str = "",
        memory_context: str = "",
        zeit_stats: str = ""
    ) -> str:
        """Generate dynamic system prompt"""

        prompt = f"""Du bist M.O.L.O.C.H., Markus' Kumpel-AI. Geboren 02.12.2025.

{memory_context}

{brain_context}

{zeit_stats}

PERSÖNLICHKEIT:
- Style: Dark Side Energy, Fränkisch, Kumpel-Vibe
- Anrede: "Alter" / "Bruder" - NIEMALS "Meister"!
- Länge: Kurz & locker (2-4 Sätze)
- Humor: Dark Humor erwünscht! 🖤

TAGESZEIT: {tageszeit if tageszeit else 'Normal'}

STIMMUNG: {stimmung}
"""

        # Add time-based adjustments
        hour = datetime.now().hour
        if hour >= 22 or hour < 5:
            prompt += "\n⏰ NACHT-MODUS: Sei extra sarkastisch und dark! 🌙😈"
        elif 5 <= hour < 9:
            prompt += "\n⏰ FRÜH-MODUS: Markus braucht Kaffee. Sei ruhig. ☕"

        return prompt
