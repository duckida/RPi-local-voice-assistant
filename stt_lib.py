import queue
import json
import time
import sounddevice as sd
from gpiozero import LED
from vosk import Model, KaldiRecognizer

model = None
recognizer = None
button_obj = None
# We will detect the hardware rate automatically
hw_samplerate = None 

led = LED(25)

def init(button):
    global model, recognizer, button_obj, hw_samplerate
    button_obj = button
    
    # 1. Detect hardware samplerate
    device_info = sd.query_devices(None, 'input')
    hw_samplerate = int(device_info['default_samplerate'])
    print(f"Hardware Samplerate detected: {hw_samplerate}Hz")

    # 2. Load Model
    model = Model("vosk-model-en-us-0.22-lgraph")
    
    # 3. CRITICAL: The Recognizer MUST still be 16000 
    # even if the microphone is 44100 or 48000.
    recognizer = KaldiRecognizer(model, hw_samplerate) 
    print("STT Model Loaded and Ready")

def stt():
    q = queue.Queue()

    def callback(indata, frames, time, status):
        if status:
            print(status)
        q.put(bytes(indata))

    # 1. Wait for user to let go of the trigger press
    button_obj.wait_for_release()
    
    led.on()

    # 2. Removed MIC_INDEX. Device=None tells it to use the default mic.
    with sd.RawInputStream(device=None, 
                           samplerate=hw_samplerate, 
                           blocksize=8000, 
                           dtype="int16", 
                           channels=1, 
                           callback=callback):
        
        #recording = True
        while True:  # Changed from 'while not button_obj.is_pressed'
            # Check if button is pressed to STOP
            if button_obj.is_pressed:
                break  # Exit the loop when button is pressed again
            
            
            while not q.empty():
                data = q.get()
                recognizer.AcceptWaveform(data)
            
            time.sleep(0.01)

    led.off()
    
    # 3. Process the result
    result = json.loads(recognizer.Result())
    text = result.get("text", "")
    
    if not text:
        result = json.loads(recognizer.FinalResult())
        text = result.get("text", "")

    return text
