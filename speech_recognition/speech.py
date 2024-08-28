import cv2
import speech_recognition as sr
from moviepy.editor import VideoFileClip
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.probability import FreqDist
import nltk

# Ensure necessary NLTK data is downloaded
nltk.download('punkt')
nltk.download('stopwords')

class VideoSummarizer:
    def __init__(self, video_path):
        self.video_path = video_path
        self.video = None
        self.audio = None
        self.transcript = ""
        self.summary = ""

    def extract_audio(self):
        video = VideoFileClip(self.video_path)
        audio = video.audio
        audio.write_audiofile("temp_audio.wav")
        self.audio = "temp_audio.wav"

    def transcribe_audio(self):
        recognizer = sr.Recognizer()
        with sr.AudioFile(self.audio) as source:
            audio = recognizer.record(source)
        try:
            self.transcript = recognizer.recognize_google(audio)
        except sr.UnknownValueError:
            print("Speech Recognition could not understand the audio")
        except sr.RequestError as e:
            print(f"Could not request results from Speech Recognition service; {e}")

    def summarize_text(self, ratio=0.3):
        stop_words = set(stopwords.words("english"))
        words = word_tokenize(self.transcript)
        freq_dist = FreqDist(word.lower() for word in words if word.lower() not in stop_words)
        
        sentences = sent_tokenize(self.transcript)
        sentence_scores = {}
        for sentence in sentences:
            for word in word_tokenize(sentence.lower()):
                if word in freq_dist:
                    if sentence not in sentence_scores:
                        sentence_scores[sentence] = freq_dist[word]
                    else:
                        sentence_scores[sentence] += freq_dist[word]

        summary_sentences = sorted(sentence_scores, key=sentence_scores.get, reverse=True)
        summary_sentences = summary_sentences[:int(len(sentences) * ratio)]
        self.summary = ' '.join(summary_sentences)

    def extract_keyframes(self, interval=1):
        cap = cv2.VideoCapture(self.video_path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_count = 0
        keyframes = []

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            if frame_count % (fps * interval) == 0:
                keyframes.append(frame)
            frame_count += 1

        cap.release()
        return keyframes

    def process_video(self):
        print("Extracting audio...")
        self.extract_audio()
        
        print("Transcribing audio...")
        self.transcribe_audio()
        
        print("Summarizing content...")
        self.summarize_text()
        
        print("Extracting keyframes...")
        keyframes = self.extract_keyframes()
        
        print("Summary:")
        print(self.summary)
        
        print(f"Number of keyframes extracted: {len(keyframes)}")

if __name__ == "__main__":
    video_path = "audio/v1.mp4"
    summarizer = VideoSummarizer(video_path)
    summarizer.process_video()
