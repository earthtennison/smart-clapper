import sounddevice as sd
import soundfile as sf

save_path = "../audio/test3.wav"
fs = 44100
duration = 5  # seconds

print("start recording for {} second...".format(duration))
myrecording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
sd.wait()
sf.write(save_path,myrecording, samplerate=fs)
print("finish recording...")