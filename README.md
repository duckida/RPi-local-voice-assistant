# RPi-local-voice-assistant
Local voice assistant running on Raspberry Pi 5 powered by VOSK STT, local LLM (llama.cpp or Ollama), and KittenTTS

## Table of Contents
* [Features](#features)
* [Setup Instructions](#setup-instructions)
* [Notes](#notes)
* [Start on boot](#start-on-boot)
* [Audio details](#audio-details)
* [AIY Voice Kit setup](#aiy-voice-kit-setup)
* [LLM tests](#llm-tests)
* [Star History](#star-history)

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
- Raspberry Pi OS (tested on Trixie 64-bit)

## Notes
If using Ollama, by default the code uses the model [`exaone3.5:2.4b`](https://ollama.com/library/exaone3.5:2.4b). This can be changed in main.py.

If using llama.cpp, by default the code uses the model [`LiquidAI/LFM2.5-1.2B-Instruct-GGUF:Q8_0`](https://huggingface.co/LiquidAI/LFM2.5-1.2B-Instruct-GGUF) This can be changed in main_llama.py. 
We also recommend `mradermacher/Youtu-LLM-2B-i1-GGUF:Q4_K_M` for reasoning-heavy tasks and `unsloth/gemma-3n-E2B-it-GGUF:Q4_K_S` for models with more RAM

By default, the code uses the VOSK model [vosk-model-en-us-0.22-lgraph]([url](https://alphacephei.com/vosk/models/vosk-model-en-us-0.22-lgraph.zip)) which you will have to download. This can be changed in main.py.

## Instructions

1. Clone this repo: `git clone https://github.com/duckida/RPi-local-voice-assistant`
2. [Install uv](https://docs.astral.sh/uv/getting-started/installation/)
3. Download the VOSK model: `wget https://alphacephei.com/vosk/models/vosk-model-en-us-0.22-lgraph.zip && unzip vosk-model-en-us-0.22-lgraph.zip`
4. If using the Ollama version, run `uv run main.py`.
   If using the llama.cpp version, run `uv run main_llama.py`

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

## Audio details
The code is designed for the latest Raspberry Pi OS Trixie, which uses PipeWire for audio. As such, the code uses `pw-play` to play audio and `python-sounddevice` for recording. It should use the default microphone and speaker connected, which can be changed thru the RPi Desktop UI.

## AIY Voice Kit setup
You will need to add `dtoverlay=googlevoicehat-soundcard` to the end of your `/boot/config/firmware.txt`

## LLM tests

We recommend using llama.cpp as it gives access to a nice web UI and more models compared to Ollama!

### Ollama models
- [Qwen3 1.7B](https://ollama.com/library/qwen3) - works as long as `/nothink` added to the prompt
- ✨ [EXAONE 3.5 2.4B](https://ollama.com/library/exaone3.5) - OK for world knowledge

### llama.cpp models
- ✨ [Gemma 3n e2B](https://huggingface.co/unsloth/gemma-3n-E2B-it-GGUF/tree/main) - great world knowledge, slightly slower
- ✨ [LFM2.5 1.5B](https://huggingface.co/LiquidAI/LFM2.5-1.2B-Instruct-GGUF) - ideal for low-latency responses, can answer basic questions

- [Youtu LLM 2B](https://huggingface.co/mradermacher/Youtu-LLM-2B-GGUF) - good for reasoning but struggles in non-reasoning mode
- [Kanana Nano 1.2B](https://huggingface.co/DevQuasar/kakaocorp.kanana-1.5-2.1b-instruct-2505-GGUF/tree/main) - very fast model, can answer basic questions
- [Qwen3 4B 2507 Instruct](https://huggingface.co/unsloth/Qwen3-4B-Instruct-2507-GGUF/tree/main?local-app=llama.cpp) - OK world knowledge, slower than Gemma3



  
## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=duckida/RPi-local-voice-assistant&type=date&legend=top-left)](https://www.star-history.com/#duckida/RPi-local-voice-assistant&type=date&legend=top-left)
