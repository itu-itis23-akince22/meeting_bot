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
        print("Recording started...")
        self.recording = []
        self.stream = sd.InputStream(
            samplerate=self.sample_rate,
            channels=self.channels,
            dtype='int16',
            callback=self.callback,
            device=int(os.getenv('AUDIO_INPUT_DEVICE_ID', 1))  # default fallback
        )
        self.stream.start()

    def callback(self, indata, frames, time, status):
        """Callback to collect chunks of audio data."""
        if status:
            print(f"Stream status: {status}")
        self.recording.append(indata.copy())

    def stop_and_save(self, mp3_filename="meeting_recording.mp3"):
        """Stops the audio stream and saves the output as an MP3 file."""
        if self.stream:
            self.stream.stop()
            self.stream.close()

        if self.recording:
            print("Stopping recording...")

            full_recording = np.concatenate(self.recording, axis=0)

            # Save to temporary WAV file
            with NamedTemporaryFile(delete=False, suffix=".wav") as tmp_wav:
                wav_path = tmp_wav.name
                write(wav_path, self.sample_rate, full_recording)
                tmp_wav.close()
                print(f"Temporary WAV saved: {wav_path}")

            # Convert WAV to MP3
            output_path = os.path.join(os.getcwd(), mp3_filename)
            audio = AudioSegment.from_wav(wav_path)
            audio.export(output_path, format="mp3")
            print(f"MP3 saved to: {output_path}")

            # Delete temporary WAV file
            try:
                os.remove(wav_path)
            except Exception as e:
                print(f"Could not delete temporary WAV file: {e}")
