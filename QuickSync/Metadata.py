from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
#
import os
import time
from pprint import pprint
from pymediainfo import MediaInfo
import datetime
from moviepy.editor import VideoFileClip
import time
import pathlib
import cv2
import wave
import librosa
import ffmpeg
import subprocess
import json
class Metadata:

    def __init__(self, video, audio, audio_start):
        self.video = video
        self.audio = audio
        self.audio_start = audio_start
        self.video_start = None
        self.aspect_ratio = None
        self.orientation = None
        self.video_duration = None
        self.audio_duration = None
        self.video_fps = None

    def calculateDatetimeAudio(self):
        AudioUTC = os.path.getmtime(self.audio)
        self.audio_end = datetime.datetime.fromtimestamp(AudioUTC)
        print(self.audio_start)
        print(self.audio_end)


    def calculateDatetimeVideo(self):
        VideoUTC = os.path.getmtime(self.video)  # Corrected to use os.path.getmtime
        self.video_start = datetime.datetime.fromtimestamp(VideoUTC)
        print(self.video_start)

    def calculateAudioDuration(self):
        audio_data, sample_rate = librosa.load(self.audio)
        self.audio_duration = librosa.get_duration(y=audio_data, sr=sample_rate)

    def calculateVideoDuration(self):
        clip = VideoFileClip(self.video)
        self.video_duration = clip.duration
        self.video_fps = clip.fps

    def get_audioStart(self):
        return self.audio_start
    def get_audioEnd(self):
        return self.audio_end
    def get_audioDuration(self):
        return self.audio_duration
    def get_videoStart(self):
        return self.video_start
    def get_videoDuration(self):
        return self.video_duration
    # def set_video_aspect_ratio(self):
    #     media_info = MediaInfo.parse(self.video)
    #     for track in media_info.tracks:
    #         if track.track_type == "Video":
    #             self.aspect_ratio = track.display_aspect_ratio
    #             break
    def set_video_orientation(self):
        #probe = ffmpeg.probe(self.video)

        command = [
            'ffprobe',
            '-v', 'error',
            '-print_format', 'json',
            '-show_entries', 'stream=width,height',
            '-select_streams', 'v:0',
            self.video
        ]

        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        metadata = json.loads(result.stdout)


        # Parse the output to extract orientation or aspect ratio
        if metadata['streams']:
            width = metadata['streams'][0]['width']
            height = metadata['streams'][0]['height']
            print(type(width))
            print(type(height))

            self.aspect_ratio = [width, height]

        else:
            print("No video streams found")



        # video_stream = next(stream for stream in probe ['streams'] if stream['codec_type'] == 'video')
        #
        # if 'tags' in video_stream and 'rotate' in video_stream['tags']:
        #     rotation = int(video_stream['tags']['rotate'])
        #     if rotation == 90 or rotation == 270:
        #         self.orientation = "Vertical"
        #     else:
        #         self.orientation = "Horizontal"




