from moviepy.editor import VideoFileClip, AudioFileClip
import simpleaudio as sa

class MediaPlayer:
    def __init__(self, video_path, audio_path=None, metadata=None):
        self.video_path = video_path
        self.audio_path = audio_path
        self.metadata = metadata
        self.aspect_ratio = metadata.aspect_ratio

    def play_video(self):
        target_height = 1920
        width_ratio = self.aspect_ratio[0]
        height_ratio = self.aspect_ratio[1]

        target_width = float((width_ratio/height_ratio) * target_height)

        # Load and play the video with audio (if available)
        clip = VideoFileClip(self.video_path)
        resized_clip = clip.resize(height=target_height, width=target_width)




        if self.audio_path:
            print(self.audio_path)
            # If a separate audio file is provided, use it
            audio_clip = AudioFileClip(self.audio_path)
            resized_clip = resized_clip.set_audio(audio_clip)

        resized_clip.preview()

    def play_audio(self):
        if self.audio_path:
            # Load and play the audio only
            wave_obj = sa.WaveObject.from_wave_file(self.audio_path)
            play_obj = wave_obj.play()
            play_obj.wait_done()
        else:
            print("No audio file provided to play.")
    # def get_aspect_ratio_dimensions(self):
    #     aspect_ratio_parts = self.aspect_ratio.split(":")
    #     width_ratio = int(aspect_ratio_parts[0])
    #     height_ratio = int(aspect_ratio_parts[1])
    #     return width_ratio, height_ratio

    def calculate_width(self, height, width_ratio, height_ratio):
        return int((width_ratio/height_ratio) * height)



# Example usage:
# media_player = MediaPlayer('synchronized_video.mp4', 'trimmed_audio.wav')
# media_player.play_video()
