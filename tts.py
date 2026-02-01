import requests

VOICEVOX_URL = "http://localhost:50021"

def tts(text: str, speaker: int, out: str):
    query = requests.post(
        f"{VOICEVOX_URL}/audio_query",
        params={"text": text, "speaker": speaker}
    ).json()

    audio = requests.post(
        f"{VOICEVOX_URL}/synthesis",
        params={"speaker": speaker},
        json=query
    ).content

    with open(out,"wb") as f:
        f.write(audio)
