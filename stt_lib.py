from time import sleep
import sounddevice as sd
from vosk import Model, KaldiRecognizer
import numpy as np
import wave
import threading
import sys

model = None
recognizer = None
button_obj = None
led_obj = None

# Parameters
channels = 1  # 1 = Mono, 2 = Stereo
file_name = "input.wav"
dtype = 'int16'

# Get the mic's sample rate
device_info = sd.query_devices(None, 'input')
sample_rate = int(device_info['default_samplerate'])

# Buffer to hold recorded data
recorded_frames = []
recording = True

def init(button, led):
    global model, recognizer, button_obj, led_obj
    button_obj = button
    led_obj = led

    # 2. Load Model
    model = Model("vosk-model-en-us-0.22-lgraph")
    recognizer = KaldiRecognizer(model, sample_rate)
    print("STT Model Loaded and Ready")

# Recording functions

def callback(indata, frames, time, status):
    if status:
        print(status, file=sys.stderr)
    recorded_frames.append(indata.copy())

def wait_for_button():
    global button_obj
    button_obj.wait_for_press()
    global recording
    recording = False

def record():
    global recorded_frames, recording

    # Reset state for a fresh recording
    recorded_frames = []
    recording = True
    
    button_obj.wait_for_release()
    sleep(0.4)
    # Start enter-listening thread
    stop_thread = threading.Thread(target=wait_for_button)
    stop_thread.start()

    # Start recording stream
    with sd.InputStream(samplerate=sample_rate, 
                        channels=channels, 
                        dtype=dtype, 
                        callback=callback):
        led_obj.on()
        while recording:
            sd.sleep(100)

    # Combine and save to file
    audio_data = np.concatenate(recorded_frames)
    led_obj.off()

    with wave.open(file_name, 'wb') as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(np.dtype(dtype).itemsize)
        wf.setframerate(sample_rate)
        wf.writeframes(audio_data.tobytes())

    print(f"Saved recording as {file_name}")

# STT function

def stt():
    # 0. Record
    record()
    
    # 1. Open the file
    wf = wave.open(file_name, "rb")
    if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
        print("Audio file must be WAV format mono PCM.")
        sys.exit(1)
        
    # 2. STT the file
    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if recognizer.AcceptWaveform(data):
            # print(recognizer.Result())
            pass
        else:
            # print(recognizer.PartialResult())
            pass
            
    
    return recognizer.FinalResult()
