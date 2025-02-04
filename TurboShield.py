import pyaudio
import wave
import os

class TurboShield:
    def __init__(self):
        self.chunk = 1024  # Record in chunks of 1024 samples
        self.sample_format = pyaudio.paInt16  # 16 bits per sample
        self.channels = 2
        self.fs = 44100  # Record at 44100 samples per second
        self.filename = "output.wav"
        self.frames = []  # Initialize array to store frames
    
    def record_audio(self, record_seconds=5):
        p = pyaudio.PyAudio()
        
        print("Recording...")
        stream = p.open(format=self.sample_format,
                        channels=self.channels,
                        rate=self.fs,
                        frames_per_buffer=self.chunk,
                        input=True)
        
        for _ in range(0, int(self.fs / self.chunk * record_seconds)):
            data = stream.read(self.chunk)
            self.frames.append(data)
        
        stream.stop_stream()
        stream.close()
        p.terminate()
        print("Recording complete.")
    
    def save_audio(self, filename=None):
        if filename:
            self.filename = filename
        
        wf = wave.open(self.filename, 'wb')
        wf.setnchannels(self.channels)
        wf.setsampwidth(pyaudio.PyAudio().get_sample_size(self.sample_format))
        wf.setframerate(self.fs)
        wf.writeframes(b''.join(self.frames))
        wf.close()
        print(f"Audio saved as {self.filename}")
    
    def play_audio(self):
        if not os.path.exists(self.filename):
            print(f"No audio file found with the name {self.filename}")
            return
        
        wf = wave.open(self.filename, 'rb')
        p = pyaudio.PyAudio()
        
        stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                        channels=wf.getnchannels(),
                        rate=wf.getframerate(),
                        output=True)
        
        data = wf.readframes(self.chunk)
        
        print("Playing audio...")
        while data:
            stream.write(data)
            data = wf.readframes(self.chunk)
        
        stream.stop_stream()
        stream.close()
        p.terminate()
        print("Playback finished.")
    
    def edit_audio(self):
        print("Edit functionality is currently not implemented.")
        # Future implementations: trimming, cutting, volume adjustments, etc.

if __name__ == "__main__":
    turbo_shield = TurboShield()
    turbo_shield.record_audio()
    turbo_shield.save_audio()
    turbo_shield.play_audio()