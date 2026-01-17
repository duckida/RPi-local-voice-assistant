import os
from openai import OpenAI
from os import system, environ
import soundfile as sf
import stt_lib
from gpiozero import Button, PWMLED
from kittentts import KittenTTS
import subprocess
from time import sleep

# Hardware Setup
button = Button(23)
led = PWMLED(25)

# Environment and TTS Setup
environ["HF_HUB_OFFLINE"] = "1"
m = KittenTTS("KittenML/kitten-tts-nano-0.2")
stt_lib.init(button, led)

server_process = subprocess.Popen([
    "/home/pi/llama.cpp/build/bin/llama-server", 
    "-hf", "LiquidAI/LFM2.5-1.2B-Instruct-GGUF:Q8_0", 
    "--port", "8080", "-c", "8192"
])

# Give the model about 10 seconds to load into memory
print("Loading llama.cpp...")
sleep(30)

# Initialize OpenAI client to point to your local llama-server
# llama-server defaults to port 8080
client = OpenAI(base_url="http://localhost:8080/v1", api_key="required-but-not-used")

messages = [
    {
        'role': 'system',
        'content': "You are a helpful voice assistant. Provide short, concise and accurate answers. "
                   "Only reply in plain text, no markdown or emojis. Keep responses under 15 words "
                   "and only 1 sentence. Do not use *, _, \, etc.",
    }
]

def llm(user_input):
    messages.append({'role': 'user', 'content': user_input})
    
    # Call the llama-server API
    completion = client.chat.completions.create(
        model="local-model", # llama-server ignores this and uses the loaded model
        messages=messages,
        max_tokens=50
    )
    
    response_text = completion.choices[0].message.content
    
    messages.append({'role': 'assistant', 'content': response_text})
    print(f"AI: {response_text}")
    
    return response_text

def tts(text):
    # Generating audio and playing via PipeWire
    audio = m.generate(text, voice='expr-voice-3-f')
    sf.write('output.wav', audio, 24000)
    system("pw-play output.wav")

print("Ready")
system("pw-play startup.mp3")

while True:
    button.wait_for_press()
    
    print("Listening...")
    question = stt_lib.stt()
    print(f"User: {question}")
    
    if question:
        print("Thinking...")
        led.pulse()
        llm_response = llm(question)
        led.off()
        
        print("Speaking...")
        # Adding dots as a small buffer for the TTS engine
        tts(".. " + llm_response + " ..")
    
    print("Done")
