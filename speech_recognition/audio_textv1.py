import speech_recognition as sr
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.probability import FreqDist
import nltk

# Ensure necessary NLTK data is downloaded
nltk.download('punkt')
nltk.download('stopwords')

class AudioSummarizer:
    def __init__(self, audio_path):
        self.audio_path = audio_path
        self.transcript = ""
        self.summary = ""

    def transcribe_audio(self):
        recognizer = sr.Recognizer()
        with sr.AudioFile(self.audio_path) as source:
            audio = recognizer.record(source)
        try:
            print("Transcribing audio...")
            self.transcript = recognizer.recognize_google(audio)
            print("Transcription complete.")
        except sr.UnknownValueError:
            print("Speech Recognition could not understand the audio")
        except sr.RequestError as e:
            print(f"Could not request results from Speech Recognition service; {e}")

    def summarize_text(self, ratio=0.3):
        print("Summarizing text...")
        stop_words = set(stopwords.words("english"))
        words = word_tokenize(self.transcript)
        
        # Calculate word frequencies
        freq_dist = FreqDist(word.lower() for word in words if word.lower() not in stop_words)
        
        sentences = sent_tokenize(self.transcript)
        sentence_scores = {}
        
        # Score sentences based on word frequencies
        for sentence in sentences:
            for word in word_tokenize(sentence.lower()):
                if word in freq_dist:
                    if sentence not in sentence_scores:
                        sentence_scores[sentence] = freq_dist[word]
                    else:
                        sentence_scores[sentence] += freq_dist[word]

        # Select top sentences for summary
        summary_sentences = sorted(sentence_scores, key=sentence_scores.get, reverse=True)
        summary_sentences = summary_sentences[:int(len(sentences) * ratio)]
        self.summary = ' '.join(summary_sentences)
        print("Summarization complete.")

    def process_audio(self):
        self.transcribe_audio()
        if self.transcript:
            self.summarize_text()
            print("\nTranscript:")
            print(self.transcript)
            print("\nSummary:")
            print(self.summary)
        else:
            print("No transcript available to summarize.")

if __name__ == "__main__":
    audio_path = "audio/video_audio.wav"
    summarizer = AudioSummarizer(audio_path)
    summarizer.process_audio()
