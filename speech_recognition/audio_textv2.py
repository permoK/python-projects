import speech_recognition as sr
from pydub import AudioSegment

# Convert the audio to a WAV format (if it's not already in WAV format)
def convert_to_wav(audio_path, wav_output_path):
    audio = AudioSegment.from_file(audio_path)
    audio.export(wav_output_path, format="wav")

# Convert audio to text
def audio_to_text(wav_path):
    recognizer = sr.Recognizer()
    with sr.AudioFile(wav_path) as source:
        audio_data = recognizer.record(source)
        text = recognizer.recognize_google(audio_data)
    return text

# Example usage:
audio_path = "output/2 mins to understand.mp3"  # Update with the path to your audio file
wav_output_path = "output/2 mins to understand.txt"  # This will be the converted WAV file

# Convert the MP3 audio to WAV
convert_to_wav(audio_path, wav_output_path)

# Convert the WAV audio to text
text = audio_to_text(wav_output_path)

# Output the recognized text
print(text)

