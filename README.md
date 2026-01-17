# RPi-local-voice-assistant
Local voice assistant running on Raspberry Pi 5 powered by VOSK STT, local LLM, and KittenTTS

## Features
- STT powered by VOSK 
- Ollama or llama.cpp local LLM processes queries
- TTS powered by [KittenTTS](https://github.com/KittenML/KittenTTS)
- Trigger with button on GPIO 23
- Status LED on GPIO 25

The project has been tested on the Raspberry Pi 5 (4GB RAM) and is designed for the AIY Voice Kit, though it works with any mic and speaker!

## Setup Instructions
Requirements: 
- Mic
- Speaker
- Ollama or llama.cpp installed with a model downloaded

> If using Ollama, by default the code uses the model [`exaone3.5:2.4b`](https://ollama.com/library/exaone3.5:2.4b). This can be changed in main.py.
> If using llama.cpp, by default the code uses the model [LiquidAI/LFM2.5-1.2B-Instruct-GGUF:Q8_0](https://huggingface.co/LiquidAI/LFM2.5-1.2B-Instruct-GGUF) This can be changed in main_llama.py.
> By default, the code uses the VOSK model [vosk-model-en-us-0.22-lgraph]([url](https://alphacephei.com/vosk/models/vosk-model-en-us-0.22-lgraph.zip)). This can be changed in main.py.

1. Clone this repo: `git clone https://github.com/duckida/RPi-local-voice-assistant`
2. [Install uv](https://docs.astral.sh/uv/getting-started/installation/)
3. Download the VOSK model: `wget https://alphacephei.com/vosk/models/vosk-model-en-us-0.22-lgraph.zip && unzip vosk-model-en-us-0.22-lgraph.zip`
4. If using the Ollama version, run `uv run main.py `. If using the llama.cpp version, run `uv run main_llama.py`

## Start on boot
1. Create a service: `sudo systemctl edit --force --full local-ai-assistant.service`
2. Paste the following into the service:
```
[Unit]
Description=Local AI Assistant
After=multi-user.target

[Service]
Type=idle
ExecStart=/home/pi/.local/bin/uv run /home/pi/local-ai-assistant/main.py
Environment=XDG_RUNTIME_DIR=/run/user/1000
WorkingDirectory=/home/pi/local-ai-assistant
User=pi

[Install]
WantedBy=multi-user.target
```
3. Reload the systemd daemon: `sudo systemctl daemon-reload`
4. Enable the service: `sudo systemctl enable local-ai-assistant.service`
5. Reboot your Pi and it should start!

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=duckida/RPi-local-voice-assistant&type=date&legend=top-left)](https://www.star-history.com/#duckida/RPi-local-voice-assistant&type=date&legend=top-left)
