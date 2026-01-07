import os
import asyncio

try:
    import edge_tts
except Exception as e:
    print("edge-tts nicht installiert:", e)
    raise SystemExit(1)

VOICE = os.environ.get("TTS_VOICE", "en-US-AriaNeural")
OUT = "ohr_test.mp3"

async def synth(text):
    comm = edge_tts.Communicate(text, VOICE)
    await comm.save(OUT)

if __name__ == '__main__':
    text = "Hello, this is a test from M O L O C H."
    print(f"Synthetisiere mit Stimme {VOICE} -> {OUT}")
    asyncio.run(synth(text))
    if os.path.exists(OUT):
        print("Fertig:", OUT)
    else:
        print("Fehler: Datei nicht erstellt")
