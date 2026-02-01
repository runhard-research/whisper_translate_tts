import os, torch, whisperx

HF_TOKEN = os.getenv("HUGGINGFACE_TOKEN")

def diarize_audio(audio_path: str):
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print("device:", device)

    model = whisperx.load_model(
        "medium",
        device="cpu",
        compute_type="int8"
    )

    result = model.transcribe(audio_path, batch_size=16)

    model_a, metadata = whisperx.load_align_model(language_code="en", device=device)
    result = whisperx.align(result["segments"], model_a, metadata, audio_path, device)

    diarize_model = whisperx.DiarizationPipeline(
        use_auth_token=HF_TOKEN,
        device=device
    )

    diarize_segments = diarize_model(audio_path)

    result = whisperx.assign_word_speakers(diarize_segments, result)

    return result["segments"]
