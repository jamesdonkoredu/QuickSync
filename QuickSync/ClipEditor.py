import os
from moviepy.editor import VideoFileClip, AudioFileClip

class ClipEditor:
    output_directory_audio = "/Users/jamesdonkor/Documents/QuickSync/QuickSyncStorage/Audio"
    output_directory_video = "/Users/jamesdonkor/Documents/QuickSync/QuickSyncStorage/Video"

    correctOrder = False

    def __init__(self, video=None, audio=None, metadata=None):
        self.video = video
        self.audio = audio
        self.metadata = metadata

        if video and audio:
            print("Initialized with both video and audio.")
        elif video:
            print("Initialized with video only.")
        elif audio:
            print("Initialized with audio only.")
        else:
            raise ValueError("At least one of video or audio must be provided.")

    def from_video(cls, video, metadata=None):
        return cls(video=video, metadata=metadata)

    @classmethod
    def from_audio(cls, audio, metadata=None):
        return cls(audio=audio, metadata=metadata)

    def getOffestState(self):
        return self.correctOrder

    def trimForFFT(self):
        # Load video and audio
        video = VideoFileClip(self.video)
        audio = AudioFileClip(self.audio)

        print("here are the metadata times")
        print(self.metadata.audio_start)
        print(self.metadata.video_start)



    # Calculate time difference in seconds
        time_diff = (self.metadata.audio_start - self.metadata.video_start).total_seconds()

        print("time difference before summation")
        print(time_diff)


    # Calculate audio start and end times based on time_diff and video's duration
        if time_diff < 0:
            audio_start = -time_diff  # Start after the negative offset (when the video starts)
            audio_end = audio_start + video.duration  # End at video duration
        else:
            audio_start = time_diff  # Start at the beginning of the audio
            audio_end = video.duration  # End at video duration

    # Ensure the audio_end does not exceed the audio's duration
        audio_end = min(audio_end, audio.duration)


        print("The audio start is at")
        print(audio_start)

        print("The audio end is")
        print(audio_end)

        # Trim the audio


        trimmed_audio = audio.subclip(audio_start, audio_end)

    # Define output filenames
        video_output_filename = "trimmed_video.mp4"
        audio_output_filename = "trimmed_audio.wav"

    # Define output paths
        video_output_path = os.path.join(self.output_directory_video, video_output_filename)
        audio_output_path = os.path.join(self.output_directory_audio, audio_output_filename)

    # Save the trimmed video and audio files
        video.write_videofile(video_output_path, codec="libx264", audio_codec="aac")
        trimmed_audio.write_audiofile(audio_output_path)

        return video_output_path, audio_output_path


    def trimAudio(self, total_offset):
        """
        Trim the audio by the given total_offset.
        :param total_offset: Time in seconds to trim from the start of the audio.
        :return: Trimmed AudioFileClip
        """
        if not self.audio:
            raise ValueError("No audio file is loaded.")

        # Load the audio if it's a filepath
        if isinstance(self.audio, str):
            self.audio = AudioFileClip(self.audio)

        # Check if total_offset is within the audio duration
        if total_offset > self.audio.duration:
            raise ValueError("Total offset is longer than the audio duration.")

        # Trim the audio
        trimmed_audio = self.audio.subclip(total_offset)

        # Save the trimmed audio
        trimmed_audio_filename = "trimmed_audio.wav"
        trimmed_audio_path = os.path.join(self.output_directory_audio, trimmed_audio_filename)
        trimmed_audio.write_audiofile(trimmed_audio_path)

        # Return the path to the trimmed audio
        return trimmed_audio_path

