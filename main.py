from ollama import chat, generate
from ollama import ChatResponse
from os import system
import soundfile as sf
import stt_lib
from gpiozero import Button

button = Button(23)

from kittentts import KittenTTS
m = KittenTTS("KittenML/kitten-tts-nano-0.2")

stt_lib.init(button)

response = generate(
    model='exaone3.5:2.4b',
    prompt='Hello!',
    keep_alive=-1
)

messages = []

messages.append({
    'role': 'system',
    'content': "You are a helpful voice assistant. You provide short, concise and accurate answers to the user's queries. Only reply in plain text, no markdown or emojis. Keep responses unde 15 words and only 1 sentence. Do not use *, _, \, etc.",
})

def llm(prompt):
    messages.append({
        'role': 'user',
        'content': question,
    })
    response: ChatResponse = chat(model='exaone3.5:2.4b', messages=messages, think=False)
    
    messages.append({
        'role': 'assistant',
        'content': response.message.content,
    })
    
    print(response.message.content)
    
    return response.message.content

def tts(text):
    audio = m.generate(text, voice='expr-voice-3-f')
    sf.write('output.wav', audio, 24000)
    system("pw-play output.wav")

print("Ready")
system("pw-play startup.mp3")
while True:
    button.wait_for_press()
    
    print("Listening...")
    question = stt_lib.stt()
    
    print(question)
    
    print("Thinking...")
    llm_response = llm(question)
    
    print("Speaking...")
    tts(".."+ llm_response + "..")
    
    print("Done")

