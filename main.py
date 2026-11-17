import sounddevice as sd
import threading
import soundfile as sf
import queue
import numpy as np
import tkinter as tk
from tkinter import ttk
from scipy.io.wavfile import write

class AudioRecorder:

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("MusicHelper")
        self.root.geometry('800x600')
        
        self.record_button = ttk.Button(self.root, text="Record", command=self.thread_for_rec)
        self.record_button.pack()
        self.stop_record_button = ttk.Button(self.root, text="Stop", command=self.stop_record)
        self.stop_record_button.pack()
        self.note_button = ttk.Button(self.root, text="Note", command=self.play_a_note)
        self.note_button.pack()
        self.quit_button = ttk.Button(self.root, text="Quit", command=self.root.destroy)
        self.quit_button.pack()
        self.recording = False
        self.q = queue.Queue()
        
        self.root.mainloop()

    def callback(self, indata, frames, time, status):
        self.q.put(indata.copy())

    def thread_for_rec(self):
        self.recording = True
        threading.Thread(target=self.record).start()

    def record(self):
        with sf.SoundFile("singing.wav", mode="x", samplerate=44100, channels=1, subtype="PCM_24") as f:
            with sd.InputStream(samplerate=44100, channels=1, callback=self.callback):
                while self.recording:
                    f.write(self.q.get())

    def stop_record(self):
        self.recording = False

    def play_a_note(self):
        frequency = 400
        duration = 2.0
        sample_rate = 44100

        t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
        wave = 0.3 * np.sin(2 * np.pi * frequency * t)

        sd.play(wave, sample_rate)
        sd.wait()

if __name__ == "__main__":
    AudioRecorder()