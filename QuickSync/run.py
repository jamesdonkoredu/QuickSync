import datetime
import os
import sys
import json
import subprocess

from hachoir.parser import createParser
from hachoir.metadata import extractMetadata

# Run.py
from FFT import FFT

from ClipEditor import ClipEditor
from MediaPlayer import MediaPlayer
from Metadata import Metadata
from datetime import datetime


def video_or_audio(clipEditor, video, audio):
    boolean = clipEditor.getOffestState()
    if (boolean == True):
        return boolean, audio
    else:
        return boolean, video



def performfft(video, audio):
    print("Extracting audio from video...")
    video_audio = FFT.extract_audio_from_video(video)
    print("Computing FFT for video audio...")
    y_fft_video, sr_video, n_video = FFT.compute_fft(video_audio)
    print(f"Video sample rate: {sr_video}, FFT length: {len(y_fft_video)}")

    print("Computing FFT for separate audio...")
    y_fft_audio, sr_audio, n_audio = FFT.compute_fft(audio)
    print(f"Audio sample rate: {sr_audio}, FFT length: {len(y_fft_audio)}")

    print("Finding time offset...")
    time_offset = FFT.find_time_offset(y_fft_video, y_fft_audio, sr_audio, n_audio)
    print(f"Calculated time offset: {time_offset}")

    return time_offset




def calculate(metadata):
    print("Audio start and end")
    metadata.calculateDatetimeAudio()
    print("video start is ")
    metadata.calculateDatetimeVideo()
    print("Audio duration")
    metadata.calculateAudioDuration()
    print("video duration")
    metadata.calculateVideoDuration()
    metadata.set_video_orientation()
    #metadata.set_video_aspect_ratio()

    print("Audio start time:", metadata.get_audioStart())
    print("Audio end time:", metadata.get_audioEnd())
    print("Audio duration:", metadata.get_audioDuration())
    print("Video start time:", metadata.get_videoStart())
    print("Video duration:", metadata.get_videoDuration())



def creation_date(filename):
    parser = createParser(filename)
    metadata = extractMetadata(parser)
    return metadata.get('creation_date')

if sys.platform == 'win32':
    print("pipe-test.py, running on windows")
    TONAME = '\\\\.\\pipe\\ToSrvPipe'
    FROMNAME = '\\\\.\\pipe\\FromSrvPipe'
    EOL = '\r\n\0'
else:
    print("pipe-test.py, running on linux or mac")
    TONAME = '/tmp/audacity_script_pipe.to.' + str(os.getuid())
    FROMNAME = '/tmp/audacity_script_pipe.from.' + str(os.getuid())
    EOL = '\n'

print("Write to  \"" + TONAME +"\"")
if not os.path.exists(TONAME):
    print(" ..does not exist.  Ensure Audacity is running with mod-script-pipe.")
    sys.exit()

print("Read from \"" + FROMNAME +"\"")
if not os.path.exists(FROMNAME):
    print(" ..does not exist.  Ensure Audacity is running with mod-script-pipe.")
    sys.exit()

print("-- Both pipes exist. Good.")

TOFILE = open(TONAME, 'w')
print("-- File to write to has been opened")
FROMFILE = open(FROMNAME, 'rt')
print("-- File to read from has now been opened too\r\n")


def send_command(command):
    """Send a single command."""
    print("Send: >>> \n"+command)
    TOFILE.write(command + EOL)
    TOFILE.flush()

def get_response():
    """Return the command response."""
    result = ''
    line = ''
    while True:
        result += line
        line = FROMFILE.readline()
        if line == '\n' and len(result) > 0:
            break
    return result

def do_command(command):
    """Send one command, and return the response."""

    send_command(command)
    response = get_response()
    print("Rcvd: <<< \n" + response)
    return response

def run():
    """Example list of commands."""
    #do_command('Help: Command=Help')
    #do_command('Help: Command="GetInfo"')
    do_command('Record1stChoice: Command=Record1stChoice')

    audio_start = datetime.now()

    #print statement for checks
    print("The record time is: ")
    print(datetime.now())

    stop = input("Press s to stop: ")
    if (stop == "s"):
        do_command('Transport: Command=PlayStop')
        audio_end = datetime.now()

        #print statements for checks
        print("The export time is: " )
        print(datetime.now())

        #select all tracks and export the file
        do_command('SelectAll: Command=SelectAll')
        # Specify a custom filename for export
        export_filename = "audacity_audio"
        export_path = f"/Users/jamesdonkor/Documents/{export_filename}.wav"

        do_command(f'Export2: Filename="{export_path}"')
        return audio_start, audio_end

def start():
    print("Welcome! This is the QuickSync app. This program will automatically "
          "sync video and audio recorded from a mobile device and audacity respectively")
    print("If you are ready to start, press y. This will automatically start the audacity recording ")
    response = input("Press y to begin")
    if response == "y":
        audio_start, audio_end = run()
    elif response == "t":

        # Example datetime strings
        audio_start_str = "2024-08-29 15:07:45.112314"
        audio_end_str = "2024-08-29 15:08:20.597296"
        video_start_str = "2024-08-22 00:20:54"

        # Convert string to datetime objects
        audio_start = datetime.strptime(audio_start_str, "%Y-%m-%d %H:%M:%S.%f")
        audio_end_dt = datetime.strptime(audio_end_str, "%Y-%m-%d %H:%M:%S.%f")
        video_start_dt = datetime.strptime(video_start_str, "%Y-%m-%d %H:%M:%S")

    else:
        print("Sorry this is an invalid response")



    video_directory_org = input("Please enter the directory of your videofile")
    audio_directory_org = input("Please enter the directory of your audiofile")

    metadata_1 = Metadata(video_directory_org, audio_directory_org, audio_start)
    calculate(metadata_1)

    clipEditor_init = ClipEditor(video_directory_org, audio_directory_org, metadata_1)
    print("Made it out!")


    #before you were returning the trimmed video and audio and passing thos through the performfft function
    video_directory_trim, audio_directory_trim = clipEditor_init.trimForFFT()

    print(dir(clipEditor_init))  # This will list all attributes and methods of the object

    #up until here it works as expected


    time_offset = performfft(video_directory_trim, audio_directory_trim)

    total_offset = time_offset

    print(total_offset)

    boolean, file = video_or_audio(clipEditor_init, video_directory_org, audio_directory_org)

    if (boolean == True):
        final_audio_path = clipEditor_init.trimAudio(total_offset)
        media_player = MediaPlayer(video_directory_org, final_audio_path, metadata_1)

        media_player.play_video()

    else:
        print("wait for test")


start()

#test_28 constants
#Audio start time: 2024-08-22 00:20:45.829855
#Audio end time: 2024-08-22 00:21:25.410800
#Audio duration: 39.06530612244898
#Video start time: 2024-08-22 00:20:54
#time, position, color :  15.067, (905, 614), [186 160 132]
#time, position, color :  22.733, (796, 757), [123  93  69]
