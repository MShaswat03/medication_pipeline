**Pi instructions**

# Setup

```bash
git clone https://github.com/yourname/medication_pipeline.git
cd medication_pipeline
python3 -m venv medenv # either python3 or python
source medenv/bin/activate
For windows: ./medenv/Scripts/activate

pip install sounddevice soundfile git+https://github.com/openai/whisper.git # For pc

Download ffmpeg-release-full.zip from https://www.gyan.dev/ffmpeg/builds/ ->
Extract to C:\ffmpeg ->
setx /M PATH "$env:PATH;C:\ffmpeg\bin" or add C:\ffmpeg\bin directly into PATH and user PATH 
Verify: ffmpeg --version

Split terminal.
Get ollama AND gemma:
winget install -e --id Ollama.Ollama ->
ollama pull gemma:2b
Then add into PATH (for me it was C:\Users\Danie\AppData\Local\Programs\Ollama)

Run python local_medication_pipeline.py AND ollama serve 

If you get cannot connect to port error:
netstat -ano | findstr 11434 ->
taskkill /PID <pid> /F ->
ollama serve

# "Remind to take 500 milligrams of paracetamol at 9am"
