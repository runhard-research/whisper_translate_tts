# WhisperX + VOICEVOX Multispeaker Translation & TTS Pipeline

This project provides a **fully pipeline** for:

1. English speech → transcription + speaker diarization (WhisperX)
2. English → Japanese translation
3. Japanese → multi‑speaker TTS (VOICEVOX)

It supports **multi‑speaker voice mapping**, fully automated batch processing, and **Docker-based VOICEVOX Engine setup**.

---

## Features

- 🎙️ **Automatic Speech Recognition (ASR)** using WhisperX
- 🧠 **Speaker Diarization** (multi-speaker separation)
- 🌍 **English → Japanese translation**
- 🗣️ **Multi‑speaker Japanese TTS** via VOICEVOX
- 🐳 **Docker Compose based VOICEVOX Engine deployment**


---

## System Overview

```
Audio (English)
   ↓
WhisperX (transcription + diarization)
   ↓
Segmented English Text + Speaker IDs
   ↓
Translation (EN → JA)
   ↓
VOICEVOX TTS (per-speaker voice mapping)
   ↓
Final Japanese multi-speaker audio
```

---

## Requirements

### OS

- Ubuntu 20.04 / 22.04 (recommended)
- Windows + WSL2 (tested)

### Python

- Python **3.9 – 3.11** recommended

### Hardware

- CPU only → supported (slower)
- GPU → CUDA 11.8+ recommended

---

## Install VOICEVOX Engine (Docker Compose)

### 1. Install Docker & Docker Compose

```bash
sudo apt update
sudo apt install -y docker.io docker-compose-plugin
sudo usermod -aG docker $USER
```

Logout & login again.

---

### 2. docker-compose.yml

Create the following file:

```yaml
version: "3.9"

services:
  voicevox:
    image: voicevox/voicevox_engine:latest
    container_name: voicevox_engine
    restart: unless-stopped
    ports:
      - "50021:50021"
```

---

### 3. Start VOICEVOX Engine

```bash
docker compose up -d
```

Check API:

```bash
curl http://localhost:50021/version
```

---

## Python Environment Setup

### 1. Create venv

```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

### 2. Install Dependencies

```bash
pip install --upgrade pip
```

CPU only:
```bash
pip install torch==2.1.2 torchaudio==2.1.2 \
  --index-url https://download.pytorch.org/whl/cpu
```

```bash
pip install "numpy<2"
```

```bash
pip install -r requirements.txt
```
### requirements.txt↑
```
whisperx==3.2.0
faster-whisper==1.0.0
numpy<2
requests
ffmpeg-python
python-dotenv
```

---

## Configuration

### config.json

```json
{
  "voicevox_url": "http://localhost:50021",
  "speaker_mapping": {
    "SPEAKER_00": {"voicevox_speaker_id": 2},
    "SPEAKER_01": {"voicevox_speaker_id": 3},
    "SPEAKER_02": {"voicevox_speaker_id": 8}
  },
  "default_speaker": {"voicevox_speaker_id": 2}
}
```

Speaker IDs can be checked by:

```bash
curl http://localhost:50021/speakers
```

---

## Usage

### 1. Input audio

Place your English audio file:

```
input.wav
```

---

### 2. Run pipeline

```bash
python main.py
```

---

### 3. Output

```
work/
 ├─ 0000.wav
 ├─ 0001.wav
 ├─ 0002.wav
 ・・・
 ├─ concat.txt
final_japanese.mp3

```

---

## Multi-Speaker Mapping

Example mapping:

| Whisper Speaker | Character | VOICEVOX ID |
|-----------------|-----------|-------------|
| SPEAKER_00 | Shikoku Metan | 2 |
| SPEAKER_01 | Zundamon | 3 |
| SPEAKER_02 | Kasukabe Tsumugi | 8 |

---

## Known Issues

- Some VOICEVOX voices sound similar → confirm speaker IDs
- Long audio → memory usage high → split audio recommended

---

## License Notes

This project **does not bundle any model weights or voice models**.

You must comply with:

- WhisperX license
- Faster-Whisper license
- VOICEVOX Engine license
- Each VOICEVOX voice character license

Commercial usage may require **separate permission** from VOICEVOX.

---

## Credits

- WhisperX: https://github.com/m-bain/whisperX
- faster-whisper: https://github.com/SYSTRAN/faster-whisper
- VOICEVOX Engine: https://github.com/VOICEVOX/voicevox_engine

---

## Future Work

- GUI frontend
- Streaming mode
- Realtime multi-speaker translation

---


