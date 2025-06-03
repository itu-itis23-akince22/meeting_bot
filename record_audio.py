import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write
from pydub import AudioSegment
import os
from tempfile import NamedTemporaryFile
from dotenv import load_dotenv

load_dotenv()

class AudioRecorder:
    def __init__(self):
        self.sample_rate = int(os.getenv('SAMPLE_RATE', 44100))
        self.channels = 2
        self.recording = []
        self.stream = None

    def start_recording(self):
        print("🎙️ Recording started...")
        self.recording = []
        self.stream = sd.InputStream(
            samplerate=self.sample_rate,
            channels=self.channels,
            dtype='int16',
            callback=self.callback,
            device=int(os.getenv('AUDIO_INPUT_DEVICE_ID'))
        )
        self.stream.start()

    def callback(self, indata, frames, time, status):
        self.recording.append(indata.copy())

    def stop_and_save(self, mp3_filename="meeting_recording.mp3"):
        if self.stream:
            self.stream.stop()
            self.stream.close()

        if self.recording:
            print("🛑 Stopping recording...")

            full_recording = np.concatenate(self.recording, axis=0)

            with NamedTemporaryFile(delete=False, suffix=".wav") as tmp_wav:
                wav_path = tmp_wav.name
                write(wav_path, self.sample_rate, full_recording)
                tmp_wav.close()
                print(f"📁 Temporary WAV saved: {wav_path}")

            # Çıktıyı proje klasörüne al
            output_path = os.path.join(os.getcwd(), mp3_filename)

            audio = AudioSegment.from_wav(wav_path)
            audio.export(output_path, format="mp3")
            print(f"✅ MP3 saved to project folder: {output_path}")

            try:
                os.remove(wav_path)
            except Exception as e:
                print(f"⚠️ Could not delete temp wav file: {e}")
