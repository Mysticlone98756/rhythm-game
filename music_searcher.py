import time
import requests
import json
import os
import sys
import random
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler



W = 700
H = 800
folder = 'C:/Users/Mysticlone98756/Desktop/codin/rhythm game(full-setup)'
audio_formats = ('.mp3', '.m4a', '.wav', '.ogg', '.flac')  # Add more formats as needed
previous_files = set()

music_check = os.listdir(os.path.join(folder, "client", "songs"))
print(music_check)

class Watcher(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return
        if event.src_path.endswith(audio_formats):
            print(f"New audio file detected: {os.path.basename(event.src_path)}")

folder = 'C:/Users/Mysticlone98756/Desktop/codin/rhythm game(full-setup)/client/songs'
observer = Observer()
event_handler = Watcher()
observer.schedule(event_handler, folder, recursive=False)

try:
    observer.start()
    print(f"Watching folder: {folder}")
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Secret huh?")
    print("You think you can do this?")
    print("Too bad")
    quit()
