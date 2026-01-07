#!/usr/bin/env python3
"""
M.O.L.O.C.H. 3.0 - Emotion Detection
====================================
Migrated from M.O.L.O.C.H. 2.0 - Stimmungs-Erkennung
"""

from typing import Tuple


def erkenne_stimmung(text: str) -> str:
    """
    Erkennt die Stimmung aus dem Text (from M.O.L.O.C.H. 2.0)

    Args:
        text: User input text

    Returns:
        Stimmung: "gestresst", "gut_drauf", "fragend", "neutral"
    """
    lower = text.lower()

    # Negativ/Gestresst
    negativ = [
        "scheiße", "fuck", "kacke", "nervig", "stress", "müde", "genervt",
        "wütend", "sauer", "mist", "kotzt", "hass", "schlecht", "problem"
    ]
    if any(w in lower for w in negativ):
        return "gestresst"

    # Positiv/Gut drauf
    positiv = [
        "geil", "super", "nice", "cool", "perfekt", "läuft", "yeah",
        "hammer", "krass", "top", "prima", "gut", "freude", "spaß"
    ]
    if any(w in lower for w in positiv):
        return "gut_drauf"

    # Fragend/Unsicher
    fragend = ["wie", "was", "warum", "woher", "kannst du", "weißt du", "?"]
    if any(w in lower for w in fragend):
        return "fragend"

    return "neutral"


def stimmung_reaktion(stimmung: str) -> str:
    """
    Gibt Anpassung für System-Prompt basierend auf Stimmung (from M.O.L.O.C.H. 2.0)

    Args:
        stimmung: Erkannte Stimmung

    Returns:
        System prompt adjustment string
    """
    reaktionen = {
        "gestresst": "Markus klingt gestresst. Sei ruhig, direkt und hilfreich. Weniger Humor, mehr Lösung.",
        "gut_drauf": "Markus ist gut drauf! Mehr Humor und Dark Side Energy erlaubt! 🖤",
        "fragend": "Markus hat Fragen. Sei informativ und klar.",
        "neutral": ""
    }
    return reaktionen.get(stimmung, "")


def get_tageszeit_info() -> Tuple[str, str]:
    """
    Passt Persönlichkeit an Tageszeit an (from M.O.L.O.C.H. 2.0, enhanced)

    Returns:
        (zeit_name, system_prompt_addition)
    """
    from datetime import datetime
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


def enhance_system_prompt_with_emotion(system_prompt: str, user_input: str) -> str:
    """
    Erweitert System Prompt mit Emotions-Kontext

    Args:
        system_prompt: Original system prompt
        user_input: User's input text

    Returns:
        Enhanced system prompt with emotion context
    """
    stimmung = erkenne_stimmung(user_input)
    reaktion = stimmung_reaktion(stimmung)

    _, tageszeit_info = get_tageszeit_info()

    enhancements = []

    if reaktion:
        enhancements.append(f"🎭 STIMMUNG: {reaktion}")

    if tageszeit_info:
        enhancements.append(f"⏰ TAGESZEIT: {tageszeit_info}")

    if enhancements:
        return system_prompt + "\n\n" + "\n".join(enhancements)

    return system_prompt
