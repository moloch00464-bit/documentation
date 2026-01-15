#!/usr/bin/env python3
"""
M.O.L.O.C.H. 3.0 - Knowledge Graph & Wissens-Verknüpfungen
===========================================================
Migrated from M.O.L.O.C.H. 2.0 - WISSENS_NETZ System
"""

from typing import List, Dict


# ═══════════════════════════════════════════════════════════════════════════════
# WISSENS-NETZ (from M.O.L.O.C.H. 2.0)
# ═══════════════════════════════════════════════════════════════════════════════

WISSENS_NETZ: Dict[str, List[str]] = {
    "wgt": ["shower noise group", "leipzig", "sierra", "dark wave", "flaggen", "juni"],
    "sierra": ["frankreich", "gone", "unbroken", "live", "lieblingsartist", "dark wave"],
    "rebecca": ["klingonisch", "qapla", "freundin", "collagen", "40. geburtstag"],
    "erkan": ["türkisch", "roasts", "staplerfahrer", "glitzer", "ohrring", "pausen", "handy"],
    "witte": ["russisch", "mat", "prigoschin", "kollege"],
    "ryan": ["russisch", "mat", "prigoschin", "kollege"],
    "dgm": ["arbeit", "druckguss", "400 bar", "700 grad", "roboter", "kuka", "abb"],
    "molochhome": ["cannabis", "vpd", "zigbee", "df16", "esp32", "home assistant"],
    "critical mass": ["led", "nürnberg", "audio", "987", "sk6812", "fahrrad"],
    "shower noise": ["wgt", "ray", "meise", "lilli", "franzi", "sven", "flaggen"],
    "ancient methods": ["ebm", "industrial", "techno", "lieblingsband", "knights bishops"],
    "sierra veins": ["gone", "frankreich", "dark wave", "lieblingsartist", "wgt"]
}


def finde_verknuepfungen(text: str) -> List[str]:
    """
    Findet relevante Verknüpfungen für einen Text (from M.O.L.O.C.H. 2.0)

    Args:
        text: Input text to analyze

    Returns:
        List of related keywords
    """
    lower = text.lower()
    gefunden = []

    for keyword, verknuepft in WISSENS_NETZ.items():
        if keyword in lower:
            gefunden.extend(verknuepft)

    return list(set(gefunden))


def lade_verknuepftes_wissen(text: str, memory_data: dict) -> List[str]:
    """
    Lädt relevantes Wissen basierend auf Verknüpfungen (from M.O.L.O.C.H. 2.0)

    Args:
        text: User input text
        memory_data: Memory dictionary with categories

    Returns:
        List of relevant memory entries
    """
    verknuepfungen = finde_verknuepfungen(text)
    relevantes = []

    # Durchsuche Memory nach Verknüpfungen
    for kategorie in ["personen", "orte", "vorlieben", "projekte", "wichtig"]:
        if kategorie in memory_data:
            entries = memory_data[kategorie]
            if isinstance(entries, list):
                for eintrag in entries:
                    eintrag_str = str(eintrag).lower()
                    if any(v in eintrag_str for v in verknuepfungen):
                        relevantes.append(eintrag)

    return relevantes[:5]  # Max 5 relevante Einträge


def ist_neue_info(text: str) -> bool:
    """
    Erkennt ob der User neue Info gibt die gespeichert werden sollte (from M.O.L.O.C.H. 2.0)

    Args:
        text: User input

    Returns:
        True if text contains new information to save
    """
    lern_marker = [
        "das ist", "er ist", "sie ist", "heißt", "wohnt", "arbeitet",
        "mag", "liebt", "hasst", "kann", "bedeutet", "ist ein", "ist eine"
    ]
    lower = text.lower()
    return any(marker in lower for marker in lern_marker) and len(text) > 20


def kategorisiere_info(text: str) -> str:
    """
    Schlägt Kategorie für neue Info vor (from M.O.L.O.C.H. 2.0)

    Args:
        text: Text to categorize

    Returns:
        Suggested category name
    """
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


def get_knowledge_context(user_input: str, memory_data: dict = None) -> str:
    """
    Builds knowledge context from graph for system prompt

    Args:
        user_input: User's input text
        memory_data: Optional memory data dict

    Returns:
        Knowledge context string for system prompt
    """
    verknuepfungen = finde_verknuepfungen(user_input)

    if not verknuepfungen:
        return ""

    context_lines = ["🧠 WISSENS-KONTEXT:"]
    context_lines.append(f"Relevante Themen: {', '.join(verknuepfungen[:5])}")

    if memory_data:
        relevantes_wissen = lade_verknuepftes_wissen(user_input, memory_data)
        if relevantes_wissen:
            context_lines.append(f"Verbundenes Wissen: {', '.join(str(w) for w in relevantes_wissen[:3])}")

    return "\n".join(context_lines)
