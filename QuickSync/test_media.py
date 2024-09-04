from moviepy.editor import VideoFileClip, AudioFileClip
import os

# Set the VLC plugin path
os.environ['VLC_PLUGIN_PATH'] = '/Applications/VLC.app/Contents/MacOS/plugins'

import vlc

# Rest of your VLC code
import cv2
import vlc
import time

class VideoPlayer:
    def __init__(self, video_path):
        # Initialize VLC player with the provided video path
        self.instance = vlc.Instance()
        self.player = self.instance.media_player_new()
        self.media = self.instance.media_new(video_path)
        self.player.set_media(self.media)

    def play(self):
        # Play the video
        self.player.play()
        try:
            # Keep the video window open until the video has finished playing
            while self.player.get_state() != vlc.State.Ended:
                time.sleep(1)
        except KeyboardInterrupt:
            # Allow the user to terminate the playback with Ctrl+C
            print("Playback interrupted by user.")
        finally:
            self.release()

    def release(self):
        # Stop the player and release resources
        self.player.stop()
        self.player.release()
        self.instance.release()

# Example usage
if __name__ == "__main__":
    video_path = "/Users/jamesdonkor/Documents/QuickSync/QuickSync/test_28.MOV"  # Update this path to your video file
    player = VideoPlayer(video_path)
    print("Starting video playback...")
    player.play()
    print("Video playback ended.")

