import time
import ueberzug.lib.v0 as ueberzug
import cv2
import moviepy.editor as mp
import threading
from termcolor import colored
from slowprint.slowprint import *
import argparse
from pydub import AudioSegment
from pydub.playback import play
import os
from pynput import keyboard as pkeyboard
import keyboard
import pyautogui

parser = argparse.ArgumentParser(description='plays videos fully in the command line')
parser.add_argument('video', metavar='vid', type=str, nargs='+',help='the video to play')
args = parser.parse_args()
vid = args.video[0]

os.system('color')
#slowprint(colored("Made by Bira ❤️ ","magenta",attrs=['reverse','bold']),0.4)


def sound_thread():
    global vid
    name = vid.split('.')[0]
    song = AudioSegment.from_mp3(f'frames//{name}audio.mp3')
    play(song)

def on_activate_m():
    print('got here')



def listener():
    with pkeyboard.GlobalHotKeys({
            'f': on_activate_m}) as m:
        m.join()

def get_info(vid):
    video_capture = cv2.VideoCapture(f"{vid}")
    fps = video_capture.get(cv2.CAP_PROP_FPS)
    total = int(video_capture.get(cv2.CAP_PROP_FRAME_COUNT))
    print(f"{fps} FPS")
    return fps,total


def split_vid_to_frames(vid):
    global saved_frame_name
    name = vid.split('.')[0]
    my_clip = mp.VideoFileClip(f"{vid}")
    my_clip.audio.write_audiofile(f"frames//{name}audio.mp3")
    video_capture = cv2.VideoCapture(f"{vid}")
    total = int(video_capture.get(cv2.CAP_PROP_FRAME_COUNT))
    saved_frame_name = 0
    print(name)
    while video_capture.isOpened():
        frame_is_read, frame = video_capture.read()
        precentage = saved_frame_name / total
        print(colored(f"%{precentage*100} done..","yellow"))
        if frame_is_read:
            cv2.imwrite(f"frames//{name}frame{str(saved_frame_name)}.jpg", frame)
            saved_frame_name += 1

        else:
            print(colored("done","red",attrs=['reverse','bold']))
            break
    return fps





def play_from_frames(fps,saved_frame_name):
    global vid
    global saved_frame_nam
    i = 0
    with ueberzug.Canvas() as c:
        name = vid.split('.')[0]
        path = f"frames//{name}frame0.jpg"
        demo = c.create_placement('demo',x=0, y=0, scaler=ueberzug.ScalerOption.COVER.value)
        demo.path = path
        demo.visibility = ueberzug.Visibility.VISIBLE
        print(type(demo))

        while True:
            if i >= saved_frame_name:
                break
            i += 1
            time.sleep(1/fps)
            demo.path = f"frames//{name}frame{i}.jpg"
        os._exit(1)

fps,total = get_info(vid)

splitting_thread = threading.Thread(target=split_vid_to_frames,args=[vid])
splitting_thread.start()

time.sleep(1)

playing_thread = threading.Thread(target=play_from_frames,args=[fps,total])
playing_thread.start()

audio_thread = threading.Thread(target=sound_thread)
audio_thread.start()

playing_thread = threading.Thread(target=play_from_frames,args=[fps,total])
playing_thread.start()

shortcut_thread = threading.Thread(target=listener)
shortcut_thread.start()
