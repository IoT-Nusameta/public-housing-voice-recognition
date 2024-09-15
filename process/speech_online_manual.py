import pyaudio
import numpy as np
import wave
import io
import speech_recognition as sr

recognizer = sr.Recognizer()

# PyAudio configuration
FORMAT = pyaudio.paInt16  # Audio format (16-bit PCM)
CHANNELS = 1             # Number of audio channels (1 for mono)
RATE = 44100              # Sample rate (samples per second)
CHUNK = 1024              # Number of frames per buffer
THRESHOLD = 5000           # Threshold to detect voice activity (adjust based on your needs)
RECORD_SECONDS = 60        # Duration of recording after voice is detected
TIMEOUT_SECONDS = 1        # Duration of recording after voice is detected

# Initialize PyAudio
audio = pyaudio.PyAudio()

# Open audio stream
stream = audio.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

print("Monitoring for voice activity...")

def get_audio_props():
    data = stream.read(CHUNK)
    audio_data = np.frombuffer(data, dtype=np.int16)
    audio_level = np.max(np.abs(audio_data))
    return data, audio_level

try:
    while True:
        recording_frames = []
        n_frame = int(RATE/CHUNK)
        data, audio_level = get_audio_props()

        if audio_level > THRESHOLD:
            print("Voice detected, starting record ...")
            
            for i in range(0, n_frame*RECORD_SECONDS):
                data, audio_level = get_audio_props()
                recording_frames.append(data)

                if audio_level < 5000:
                    n_timeout += 1
                    if n_timeout > n_frame*TIMEOUT_SECONDS:
                        break
                else:
                    n_timeout = 0

                print(f'audio level: {audio_level}')
                print(f'timeout: {n_timeout}')

            # Save recorded audio to WAV file
            with io.BytesIO() as wav_buffer:
                with wave.open(wav_buffer, 'wb') as wf:
                    wf.setnchannels(CHANNELS)
                    wf.setsampwidth(audio.get_sample_size(FORMAT))
                    wf.setframerate(RATE)
                    wf.writeframes(b''.join(recording_frames))                
                wav_buffer.seek(0)  # Move to the start of the buffer

                with sr.AudioFile(wav_buffer) as source:
                    audio_data = recognizer.record(source)
                    try:
                        text = recognizer.recognize_google(audio_data, language = "id-ID")
                        print("Recognized Text: ", text)
                    except sr.UnknownValueError:
                        print("Google Speech Recognition could not understand audio")
                    except sr.RequestError as e:
                        print(f"Could not request results from Google Speech Recognition service; {e}")

except KeyboardInterrupt:
    print("Stopping...")
finally:
    stream.stop_stream()
    stream.close()
    audio.terminate()
