#local_medication_pipeline.py
import tempfile
import sounddevice as sd
import soundfile as sf
import whisper
import requests 
import json

sd.default.device = 0 # set to your microphone device index

def record_audio_to_tempfile(duration=5, samplerate=16000):
     print(f"\n[Record] Recording for {duration} seconds...")

     audio = sd.rec(
          int(duration * samplerate),
          samplerate=samplerate, 
          channels=1, 
          dtype="float32",
     )

     sd.wait()  #wait until recording is finished

     tmp_file = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
     sf.write(tmp_file.name, audio, samplerate)

     print("[Record] Saved:", tmp_file.name)
     return tmp_file.name

_whisper_model_cache = {} # simple cache so we load model only once

def transcribe_with_whisper(audio_path):
     
     print("\n[Whisper] Loading Tiny model..")

     if "model" not in _whisper_model_cache:
          _whisper_model_cache["model"] = whisper.load_model("tiny")
     model = _whisper_model_cache["model"]

     print(f"[Whisper] Transcribing: {audio_path}")
     result = model.transcribe(audio_path)
     text = result["text"].strip()
     print(f"[Whisper] Text: {text!r}")
     return text 

def call_gemma_for_medication(user_text):
     
     print("\n[Gemma] Sending text to LLM...")

     
     system_prompt = (
        "You are a medication reminder parser.\n"
        "The user will describe what medicine to take and when.\n"
        "Your job is to extract structured information and output ONLY valid JSON.\n"
        "No explanations, no extra text, no markdown.\n"
        "JSON format:\n"
        "{\n"
        '  \"medication_name\": string,\n'
        '  \"dose_mg\": number | null,\n'
        '  \"times\": [\"HH:MM\", ...],\n'
        '  \"date\": string,\n'
        '  \"notes\": string\n'
        "}\n"
    )

     full_prompt = (
        f"{system_prompt}\n\n"
        f"User: {user_text}\n"
        f"Assistant:"
    )
     
     payload = {
          "model": "gemma:2b",
          "prompt": full_prompt, 
          "stream": False,
     }

     resp = requests.post("http://localhost:11434/api/generate", json=payload)
     resp.raise_for_status()
     data = resp.json()

     raw = data.get("response", "").strip()
     print("[Gemma] Raw response:", raw)

     #try to parse JSON
     try:
         parsed = json.loads(raw)
     except json.JSONDecodeError:
          print("[Gemma] WARNING: Could not parse JSON, returning raw text.")
          parsed = {"raw_responese": raw}
    
     print("[Gemma] Parsed:", parsed)
     return parsed 

    #  answer = data.get("response", "").strip()
    #  print("[Gemma] Response:")
    #  print(answer)
    #  return answer 


def run_medication_pipeline_once():
    # 1) Record from mic
    audio_path = record_audio_to_tempfile(duration=5)


    # 2) STT with Whisper
    text = transcribe_with_whisper(audio_path)
    if not text:
        print("[Pipeline] No text detected, try again.")
        return

    # 3) LLM interpretation with Gemma
    response = call_gemma_for_medication(text)

    print("\n[Pipeline] ----- SUMMARY -----")
    print("Heard:", text)
    print("Gemma interpretation:", response)
    print("[Pipeline] --------------------\n")


if __name__ == "__main__":
    print("=== Local Medication Workflow Demo ===")
    print("Flow: Mic -> Whisper Tiny -> Gemma (gemma:2b)\n")

    while True:
        cmd = input("Press ENTER to record (or type 'q' to quit): ").strip().lower()
        if cmd == "q":
            print("Bye.")
            break

        run_medication_pipeline_once()
