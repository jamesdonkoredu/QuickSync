import numpy as np
import scipy.signal
from moviepy.editor import VideoFileClip
import librosa

class FFT:

    def __init__(self, video, audio):
        self.video = video
        self.audio = audio

    # Extract audio from video
    @staticmethod
    def extract_audio_from_video(video_path):
        video = VideoFileClip(video_path)
        audio_path = "video_audio.wav"
        video.audio.write_audiofile(audio_path, codec='pcm_s16le')
        return audio_path

    # Compute FFT
    @staticmethod
    def compute_fft(audio_path):
        y, sr = librosa.load(audio_path, sr=None)
        n = len(y)
        y_fft = np.fft.fft(y)
        return y_fft, sr, n

    # Find time offset using cross-correlation
    @staticmethod
    def find_time_offset(y_fft_video, y_fft_audio, sr, n):
        correlation = scipy.signal.correlate(y_fft_audio, y_fft_video, mode='full')
        lag = np.argmax(correlation) - (len(y_fft_video) - 1)
        time_offset = lag / sr
        return time_offset


