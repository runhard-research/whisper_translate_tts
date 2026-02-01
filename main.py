import os, json, subprocess
from dotenv import load_dotenv
from translate import translate
from diarize import diarize_audio
from tts import tts
from utils import ensure_dir

load_dotenv()

INPUT_MP3 = "input.mp3"
WORK_DIR = "work"
FINAL_MP3 = "final_japanese.mp3"

ensure_dir(WORK_DIR)

# -----------------------------
# 設定ロード
# -----------------------------
with open("config.json","r",encoding="utf-8") as f:
    config = json.load(f)

speaker_map = config["speaker_mapping"]

# -----------------------------
# WhisperX 実行
# -----------------------------
segments = diarize_audio(INPUT_MP3)

# -----------------------------
# 翻訳 + 音声生成
# -----------------------------
wav_list = []

for i, seg in enumerate(segments):
    spk = seg.get("speaker", "SPEAKER_00")
    text_en = seg["text"].strip()

    if not text_en:
        continue

    print(f"[{i}] {spk}: {text_en}")

    text_ja = translate(text_en)

    speaker_id = speaker_map.get(
        spk,
        speaker_map["SPEAKER_00"]
    )["voicevox_speaker_id"]

    out_wav = f"{WORK_DIR}/{i:04d}.wav"
    tts(text_ja, speaker_id, out_wav)

    wav_list.append(out_wav)

# -----------------------------
# ffmpeg 連結
# -----------------------------
concat_txt = f"{WORK_DIR}/concat.txt"
with open(concat_txt,"w") as f:
    for w in wav_list:
        f.write(f"file '{os.path.abspath(w)}'\n")

subprocess.run([
    "ffmpeg","-y","-f","concat","-safe","0",
    "-i",concat_txt,
    "-acodec","libmp3lame",
    FINAL_MP3
])

print("\n🎉 完了:", FINAL_MP3)
