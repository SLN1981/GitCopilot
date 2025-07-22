# read files from audio directory
import os
# read mp3 files from audio directory
def read_mp3_files():
    audio_dir = 'audio'
    mp3_files = []
    for filename in os.listdir(audio_dir):
        if filename.endswith('.mp3'):
            mp3_files.append(os.path.join(audio_dir, filename))
    return mp3_files

import glob

def read_mp3_file_glob_approach():
    return glob.glob('audio/*.mp3')

print("MP3 files found:", read_mp3_file_glob_approach())
