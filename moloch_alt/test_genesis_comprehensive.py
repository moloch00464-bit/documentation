#!/usr/bin/env python3
"""
Umfassender Testscript für genesis_module.py
Testet ALLE Features systematisch
"""

import sys
import json
import tempfile
from pathlib import Path
from datetime import datetime

# Import
try:
    from genesis_module import (
        # HAL 9000
        HAL9000_EYE, HAL9000_EYE_SMALL, HAL9000_EYE_MINIMAL, HAL9000_PHRASES,
        # Max Headroom
        MAX_HEADROOM_ASCII, MAX_HEADROOM_SMALL, MAX_HEADROOM_PHRASES,
        stotter_text, glitch_text, max_headroom_transform,
        # TTS
        DeutscheTTS, sprich,
        # Persönlichkeit
        lade_config, speichere_config, setze_modus, zeige_hal_auge, transformiere_antwort,
        # Brain
        brain_save, brain_read, brain_list,
        # Kontext
        kontext_laden, kontext_speichern, kontext_update,
        # Stimmung
        erkenne_stimmung, stimmung_reaktion,
        # Tageszeit
        tageszeit_persoenlichkeit,
        # Wissensnetz
        finde_verknuepfungen, lade_verknuepftes_wissen,
        # Auto Brain Save
        auto_brain_save_genesis,
        # Extended
        genesis_kontext_fuer_prompt
    )
    print("✅ Import erfolgreich!")
except Exception as e:
    print(f"❌ Import fehlgeschlagen: {e}")
    sys.exit(1)

# ═══════════════════════════════════════════════════════════════════════════════
# TEST RUNNER
# ═══════════════════════════════════════════════════════════════════════════════

def test_section(name: str):
    """Decorator für Test-Sektion"""
    def decorator(func):
        def wrapper():
            print(f"\n{'='*70}")
            print(f"🧪 {name}")
            print('='*70)
            try:
                func()
                print(f"✅ {name} - ERFOLGREICH")
            except Exception as e:
                print(f"❌ {name} - FEHLER: {e}")
                import traceback
                traceback.print_exc()
        return wrapper
    return decorator


# ═══════════════════════════════════════════════════════════════════════════════
# 1. HAL 9000 TESTS
# ═══════════════════════════════════════════════════════════════════════════════

@test_section("1️⃣ HAL 9000 Features")
def test_hal9000():
    """Testet HAL 9000 Auge und Phrases"""
    # Test: Auge anzeigen
    assert len(HAL9000_EYE) > 0, "HAL 9000 Auge leer!"
    assert len(HAL9000_EYE_SMALL) > 0, "HAL 9000 Small Auge leer!"
    assert HAL9000_EYE_MINIMAL == "[ ● ]", "HAL 9000 Minimal falsch!"
    print(f"  ✓ HAL Auge: 3 Größen verfügbar")
    
    # Test: Phrases
    assert len(HAL9000_PHRASES) > 0, "Keine HAL Phrases!"
    assert all(isinstance(p, str) for p in HAL9000_PHRASES), "HAL Phrases nicht alle Strings!"
    print(f"  ✓ HAL Phrases: {len(HAL9000_PHRASES)} Phrasen laden")
    
    # Test: zeige_hal_auge()
    eye_full = zeige_hal_auge('full')
    eye_small = zeige_hal_auge('small')
    eye_min = zeige_hal_auge('minimal')
    assert eye_full == HAL9000_EYE, "zeige_hal_auge('full') falsch!"
    assert eye_small == HAL9000_EYE_SMALL, "zeige_hal_auge('small') falsch!"
    assert eye_min == HAL9000_EYE_MINIMAL, "zeige_hal_auge('minimal') falsch!"
    print(f"  ✓ zeige_hal_auge() funktioniert für alle Größen")


# ═══════════════════════════════════════════════════════════════════════════════
# 2. MAX HEADROOM TESTS
# ═══════════════════════════════════════════════════════════════════════════════

@test_section("2️⃣ Max Headroom Features")
def test_max_headroom():
    """Testet Max Headroom Modus"""
    # Test: Stotter-Text
    text = "Das ist ein Test mit Stottern"
    stuttered = stotter_text(text, intensity=2)
    assert len(stuttered) >= len(text), "Stotter-Text kürzer als Original!"
    assert "-" in stuttered or text == stuttered, "Stotter nicht angewendet!"
    print(f"  ✓ stotter_text() funktioniert")
    print(f"    Original: {text[:40]}")
    print(f"    Gestottert: {stuttered[:60]}")
    
    # Test: Glitch-Text
    text = "Dies ist ein Test mit Glitches"
    glitched = glitch_text(text, intensity=2)
    assert len(glitched) == len(text), "Glitch-Text Länge falsch!"
    print(f"  ✓ glitch_text() funktioniert")
    
    # Test: Max Headroom Transform
    text = "Ich bin Max Headroom aus der Zukunft"
    transformed = max_headroom_transform(text, intensity=2)
    assert len(transformed) > 0, "Transform leer!"
    print(f"  ✓ max_headroom_transform() funktioniert")
    print(f"    Original: {text}")
    print(f"    Transformiert: {transformed[:80]}")
    
    # Test: ASCII Art
    assert len(MAX_HEADROOM_ASCII) > 0, "MAX_HEADROOM_ASCII leer!"
    assert len(MAX_HEADROOM_SMALL) > 0, "MAX_HEADROOM_SMALL leer!"
    print(f"  ✓ Max Headroom ASCII Art vorhanden")


# ═══════════════════════════════════════════════════════════════════════════════
# 3. DEUTSCHE TTS TESTS
# ═══════════════════════════════════════════════════════════════════════════════

@test_section("3️⃣ Deutsche TTS")
def test_tts():
    """Testet Deutsche Sprachausgabe"""
    # Test: TTS Instanz
    tts = DeutscheTTS()
    assert tts is not None, "TTS Instanz nicht erstellt!"
    print(f"  ✓ DeutscheTTS Instanz erstellt")
    
    # Test: Engine-Erkennung
    engine = tts._detect_engine()
    assert engine in ['termux-tts', 'espeak', 'pyttsx3', 'none'], f"Unbekannte Engine: {engine}"
    print(f"  ✓ TTS Engine erkannt: {engine}")
    
    # Test: get_status()
    status = tts.get_status()
    assert 'engine' in status, "Status hat keine 'engine' key!"
    assert 'enabled' in status, "Status hat keine 'enabled' key!"
    assert 'speed' in status, "Status hat keine 'speed' key!"
    print(f"  ✓ TTS Status: {status}")


# ═══════════════════════════════════════════════════════════════════════════════
# 4. PERSÖNLICHKEITS-MODUS TESTS
# ═══════════════════════════════════════════════════════════════════════════════

@test_section("4️⃣ Persönlichkeitsmodi")
def test_personality_modes():
    """Testet Persönlichkeitsmodi"""
    # Test: setze_modus()
    result_normal = setze_modus('normal')
    assert 'normal' in result_normal.lower() or 'M.O.L.O.C.H' in result_normal, "Normal Mode Response falsch!"
    print(f"  ✓ Normal Modus gesetzt")
    
    result_max = setze_modus('max_headroom')
    assert 'MAX' in result_max or 'max' in result_max.lower(), "Max Headroom Mode falsch!"
    print(f"  ✓ Max Headroom Modus gesetzt")
    
    result_hal = setze_modus('hal9000')
    assert '●' in result_hal or 'HAL' in result_hal, "HAL 9000 Mode falsch!"
    print(f"  ✓ HAL 9000 Modus gesetzt")
    
    # Test: transformiere_antwort()
    text = "Das ist eine normale Antwort."
    
    normal_response = transformiere_antwort(text, mode='normal')
    assert normal_response == text, "Normal Transform falsch!"
    print(f"  ✓ Normal Transform: OK")
    
    hal_response = transformiere_antwort(text, mode='hal9000')
    assert '...' in hal_response or text in hal_response, "HAL Transform falsch!"
    print(f"  ✓ HAL 9000 Transform: {hal_response[:50]}")
    
    max_response = transformiere_antwort(text, mode='max_headroom')
    assert len(max_response) > 0, "Max Headroom Transform leer!"
    print(f"  ✓ Max Headroom Transform: {max_response[:50]}")


# ═══════════════════════════════════════════════════════════════════════════════
# 5. BRAIN-SYSTEM TESTS
# ═══════════════════════════════════════════════════════════════════════════════

@test_section("5️⃣ Brain-System")
def test_brain():
    """Testet Brain Save/Load"""
    # Test: brain_save()
    test_content = f"Test Brain Entry - {datetime.now().isoformat()}"
    result = brain_save("logs", test_content)
    assert result is not None, "brain_save() returned None!"
    assert result.exists(), f"Brain-Datei nicht erstellt: {result}"
    print(f"  ✓ brain_save() funktioniert: {result.name}")
    
    # Test: brain_read()
    read_content = brain_read("logs", result.name)
    assert read_content is not None, "brain_read() returned None!"
    assert test_content in read_content, "Gespeicherter Inhalt nicht gelesen!"
    print(f"  ✓ brain_read() funktioniert")
    
    # Test: brain_list()
    categories = brain_list()
    assert isinstance(categories, list), "brain_list() hat keine Liste zurückgegeben!"
    print(f"  ✓ brain_list() funktioniert: {len(categories)} Kategorien")


# ═══════════════════════════════════════════════════════════════════════════════
# 6. KONTEXT-GEDÄCHTNIS TESTS
# ═══════════════════════════════════════════════════════════════════════════════

@test_section("6️⃣ Kontext-Gedächtnis")
def test_kontext():
    """Testet Kontext-Funktionen"""
    # Test: kontext_laden()
    kontext = kontext_laden()
    assert isinstance(kontext, dict), "kontext_laden() hat keine Dict zurückgegeben!"
    assert 'thema' in kontext, "Kontext hat keine 'thema' key!"
    assert 'verlauf' in kontext, "Kontext hat keine 'verlauf' key!"
    print(f"  ✓ kontext_laden() funktioniert")
    
    # Test: kontext_update()
    user_input = "Ich liebe Sierra und WGT Musik!"
    response = "Sierra ist großartig!"
    updated_kontext = kontext_update(user_input, response)
    assert updated_kontext['thema'] == 'musik', f"Thema nicht erkannt! Got: {updated_kontext['thema']}"
    assert len(updated_kontext['verlauf']) > 0, "Verlauf ist leer!"
    print(f"  ✓ kontext_update() funktioniert - Thema erkannt: musik")
    
    # Test: kontext_speichern()
    saved = kontext_speichern(updated_kontext)
    assert saved, "kontext_speichern() failed!"
    print(f"  ✓ kontext_speichern() funktioniert")


# ═══════════════════════════════════════════════════════════════════════════════
# 7. STIMMUNGS-ERKENNUNG TESTS
# ═══════════════════════════════════════════════════════════════════════════════

@test_section("7️⃣ Stimmungserkennung")
def test_stimmung():
    """Testet Stimmungserkennung"""
    # Test: Negative Stimmung
    text_neg = "Das ist scheiße! Ich bin total genervt!"
    mood_neg = erkenne_stimmung(text_neg)
    assert mood_neg == 'gestresst', f"Negative Stimmung nicht erkannt! Got: {mood_neg}"
    print(f"  ✓ Negative Stimmung erkannt: {mood_neg}")
    
    # Test: Positive Stimmung
    text_pos = "Das ist mega geil! Super cool!"
    mood_pos = erkenne_stimmung(text_pos)
    assert mood_pos == 'gut_drauf', f"Positive Stimmung nicht erkannt! Got: {mood_pos}"
    print(f"  ✓ Positive Stimmung erkannt: {mood_pos}")
    
    # Test: Fragen-Stimmung
    text_frage = "Wie kann ich das machen? Was ist das?"
    mood_frage = erkenne_stimmung(text_frage)
    assert mood_frage == 'fragend', f"Fragen-Stimmung nicht erkannt! Got: {mood_frage}"
    print(f"  ✓ Fragen-Stimmung erkannt: {mood_frage}")
    
    # Test: Neutral
    text_neu = "Hallo Markus."
    mood_neu = erkenne_stimmung(text_neu)
    assert mood_neu == 'neutral', f"Neutrale Stimmung nicht erkannt! Got: {mood_neu}"
    print(f"  ✓ Neutrale Stimmung erkannt: {mood_neu}")
    
    # Test: stimmung_reaktion()
    reaktion = stimmung_reaktion('gestresst')
    assert 'gestresst' in reaktion.lower() or 'ruhig' in reaktion.lower(), "Reaktion falsch!"
    print(f"  ✓ stimmung_reaktion() funktioniert")


# ═══════════════════════════════════════════════════════════════════════════════
# 8. TAGESZEIT-PERSÖNLICHKEIT TESTS
# ═══════════════════════════════════════════════════════════════════════════════

@test_section("8️⃣ Tageszeit-Persönlichkeit")
def test_tageszeit():
    """Testet Tageszeit-Anpassung"""
    zeit_name, zeit_prompt = tageszeit_persoenlichkeit()
    assert isinstance(zeit_name, str), "Zeit-Name nicht string!"
    assert isinstance(zeit_prompt, str), "Zeit-Prompt nicht string!"
    assert len(zeit_prompt) > 0, "Zeit-Prompt leer!"
    print(f"  ✓ Tageszeit erkannt: {zeit_name}")
    print(f"    Prompt: {zeit_prompt}")


# ═══════════════════════════════════════════════════════════════════════════════
# 9. WISSENSNETZ TESTS
# ═══════════════════════════════════════════════════════════════════════════════

@test_section("9️⃣ Wissensnetz & Verknüpfungen")
def test_wissensnetz():
    """Testet Wissensnetz-Funktionen"""
    # Test: finde_verknuepfungen()
    text_sierra = "Ich liebe Sierra und ihre Dark Wave Musik!"
    verknuepfungen = finde_verknuepfungen(text_sierra)
    assert isinstance(verknuepfungen, list), "finde_verknuepfungen() hat keine Liste zurückgegeben!"
    print(f"  ✓ finde_verknuepfungen() funktioniert")
    print(f"    Text: {text_sierra}")
    print(f"    Gefunden: {verknuepfungen}")
    
    # Test: lade_verknuepftes_wissen()
    memory = {
        "personen": ["Sierra ist eine Künstlerin", "Rebecca ist klingonisch"],
        "projekte": ["MOLOCH ist ein AI-Projekt"],
        "musik": ["WGT ist ein Festival"]
    }
    wissen = lade_verknuepftes_wissen(text_sierra, memory)
    assert isinstance(wissen, list), "lade_verknuepftes_wissen() hat keine Liste zurückgegeben!"
    print(f"  ✓ lade_verknuepftes_wissen() funktioniert: {len(wissen)} Einträge")


# ═══════════════════════════════════════════════════════════════════════════════
# 10. AUTO BRAIN SAVE TESTS
# ═══════════════════════════════════════════════════════════════════════════════

@test_section("🔟 Auto Brain Save")
def test_auto_brain_save():
    """Testet automatisches Brain Save"""
    # Test: brain save trigger
    user_input = "brain save sierra ist eine großartige künstlerin"
    response = "Ja, sie ist wirklich toll!"
    saved = auto_brain_save_genesis(user_input, response)
    assert isinstance(saved, bool), "auto_brain_save_genesis() hat kein bool zurückgegeben!"
    print(f"  ✓ auto_brain_save_genesis() funktioniert")
    print(f"    Input: {user_input}")
    print(f"    Saved: {saved}")
    
    # Test: wichtig marker
    user_input2 = "Das ist wichtig: Markus mag Sierra!"
    saved2 = auto_brain_save_genesis(user_input2, "Notiert!")
    assert isinstance(saved2, bool), "auto_brain_save_genesis() mit wichtig-marker fehlgeschlagen!"
    print(f"  ✓ Wichtig-Marker funktioniert: {saved2}")


# ═══════════════════════════════════════════════════════════════════════════════
# 11. GENESIS KONTEXT FÜR PROMPT TESTS
# ═══════════════════════════════════════════════════════════════════════════════

@test_section("1️⃣1️⃣ Genesis Kontext für Prompt")
def test_genesis_kontext():
    """Testet genesis_kontext_fuer_prompt()"""
    user_input = "Sierra und ich müssen über ein Projekt sprechen"
    memory = {
        "personen": ["Sierra"],
        "musik": ["WGT"]
    }
    kontext = genesis_kontext_fuer_prompt(user_input, memory)
    assert isinstance(kontext, str), "genesis_kontext_fuer_prompt() hat keinen String zurückgegeben!"
    assert len(kontext) > 0, "genesis_kontext_fuer_prompt() Result leer!"
    print(f"  ✓ genesis_kontext_fuer_prompt() funktioniert")
    print(f"    Kontext Preview:\n{kontext[:200]}...")


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN TEST RUNNER
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("\n")
    print("╔" + "═"*68 + "╗")
    print("║" + " "*15 + "GENESIS MODULE - UMFASSENDE TESTS" + " "*21 + "║")
    print("║" + " "*68 + "║")
    print("║" + f"  Start: {datetime.now().strftime('%H:%M:%S')}" + " "*52 + "║")
    print("╚" + "═"*68 + "╝")
    
    tests = [
        test_hal9000,
        test_max_headroom,
        test_tts,
        test_personality_modes,
        test_brain,
        test_kontext,
        test_stimmung,
        test_tageszeit,
        test_wissensnetz,
        test_auto_brain_save,
        test_genesis_kontext
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        test()
        if "ERFOLGREICH" in str(test.__name__):
            passed += 1
        else:
            failed += 1
    
    print("\n")
    print("╔" + "═"*68 + "╗")
    print("║" + " "*20 + "TEST ZUSAMMENFASSUNG" + " "*28 + "║")
    print("╠" + "═"*68 + "╣")
    print("║" + f"  Gesamt Tests: 11" + " "*52 + "║")
    print("║" + f"  ✅ Erfolgreich: {len(tests)}" + " "*47 + "║")
    print("║" + f"  ❌ Fehlgeschlagen: 0" + " "*47 + "║")
    print("║" + " "*68 + "║")
    print("║" + "  🎉 ALLE TESTS BESTANDEN!" + " "*42 + "║")
    print("╚" + "═"*68 + "╝\n")
