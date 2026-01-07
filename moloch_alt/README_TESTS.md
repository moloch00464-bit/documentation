GENESIS MODULE — Testanleitung

Dieses README beschreibt, wie du die umfassenden Tests für `genesis_module.py` ausführst.

Voraussetzungen
- Python 3.8+ installiert
- Git-Repository im Projektordner
- Optional: `espeak` oder `pyttsx3` für TTS-Tests (wenn verfügbar)

Dateien
- `test_genesis_comprehensive.py`: Umfassende Tests für `genesis_module.py`.

Schnellstart
1. Wechsle in das Projektverzeichnis:

```bash
cd "c:\Users\49179\Desktop\Kleine Moloch\Smartphon moloch\moloch"
```

2. Test ausführen:

```bash
python test_genesis_comprehensive.py
```

Was die Tests tun
- Prüfen HAL 9000 ASCII und Phrasen
- Prüfen Max Headroom (Stottern, Glitches, ASCII)
- Prüfen Deutsche TTS Erkennung (keine Audio-Ausgabe wenn Engine fehlt)
- Prüfen Persönlichkeitsmodi, `setze_modus()` und `transformiere_antwort()`
- Prüfen `brain_save`, `brain_read`, `brain_list`
- Prüfen Kontext-Funktionen (`kontext_laden`, `kontext_update`, `kontext_speichern`)
- Prüfen Stimmungserkennung
- Prüfen Wissensnetz-Funktionen
- Prüfen Auto Brain Save
- Prüfen `genesis_kontext_fuer_prompt()`

Hinweise
- Tests schreiben Dateien in `~/.moloch/brain/...` (standardmäßig `C:\Users\<User>\moloch\brain` unter Windows). Du kannst diese Dateien danach prüfen oder löschen.
- Wenn `pyttsx3` nicht installiert ist, meldet der Test `engine: none` — das ist in Ordnung.

Fehlerbehebung
- Falls ein Test fehlschlägt: Fehlermeldung im Terminal lesen, das betroffene Modul in `genesis_module.py` prüfen und erneut testen.

Kontakt
- Wenn du willst, committe ich die Änderungen und zeige den finalen Git-Status.
