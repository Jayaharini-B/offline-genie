import vosk
import sounddevice as sd
import queue

# Use full model folder path
model = vosk.Model(r"E:\AI OFFLINE GENIE\vosk-model-small-en-us-0.15")
q = queue.Queue()

def callback(indata, frames, time, status):
    q.put(bytes(indata))

with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype="int16",
                       channels=1, callback=callback):
    rec = vosk.KaldiRecognizer(model, 16000)
    print("🎤 Speak now...")
    while True:
        data = q.get()
        if rec.AcceptWaveform(data):
            result = rec.Result()
            print(result)
            break
