**Pi instructions**

# Setup

```bash
git clone https://github.com/yourname/medication_pipeline.git
cd medication_pipeline
python3 -m venv medenv # either python3 or python
source medenv/bin/activate
# For windows: ./medenv/Scripts/activate
pip install -r requirements.txt # For raspberry pi 
pip install sounddevice soundfile git+https://github.com/openai/whisper.git # For pc
python local_medication_pipeline.py 

# "Remind to take 500 milligrams of paracetamol at 9am"
# Download ffmpeg-release-full.zip from https://www.gyan.dev/ffmpeg/builds/
# Extract to C:\ffmpeg
# setx /M PATH "$env:PATH;C:\ffmpeg\bin"
# Verify: ffmpeg --version