from moviepy.editor import VideoFileClip

# Path to the uploaded video file
video_path = "/home/peekay/Downloads/y2mate.com - 2 mins to understand How the collaborative contact centre boosts the customer experience_720pFH.mp4"
audio_output_path = "output/2 mins to understand.mp3"

# Load the video file
video_clip = VideoFileClip(video_path)

# Extract the audio
audio_clip = video_clip.audio

# Save the audio to a file
audio_clip.write_audiofile(audio_output_path)

# Close the video and audio clips to free resources
video_clip.close()
audio_clip.close()

audio_output_path

