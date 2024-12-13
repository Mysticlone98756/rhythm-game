import pygame
import os
import glob
import random
import math
import sys
import 



WIDTH = 400
HEIGHT = 650

Scroll_Speed = 1
Upscroll = True
Downscroll = False
title_image_number = 0
title_image_folder = "C:\\Users\\Mysticlone98756\\Desktop\\codin\\rhythm game(full-setup)\\client\\img"

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption("a generic rhythm game")

font_n = "handdrawnuniquenessregular"
font_s = 24
font = pygame.font.SysFont(font_n, font_s)

text_surface = font.render("A generic Rhythm Game", True, (255, 255, 255))

supported_audio_formats = (".mp3")
supported_chart_formats = (".sm") #for the time being

songs_folder = "C:\\Users\\Mysticlone98756\\Desktop\\codin\\rhythm game(full-setup)\\client\\songs"

def load_songs(folder):
    return [f for f in os.listdir(folder) if f.endswith(supported_audio_formats)]

def play_songs(folder):
    songs = load_songs(folder)
    if not songs:
        print("No songs? How come??")
        return
    
    print("songs found?? woohoo!! Here are the songs:", songs)
    
    for song in songs:
        song_path = os.path.join(folder, song)
        print(f"now playing: {song}")
        pygame.mixer.music.load(song_path)
        pygame.mixer.music.play()
        
        while pygame.mixer.get_busy():
            pygame.time.Clock().tick(10)
            
play_songs(songs_folder)

#load images (keys and other things)
noteskins_folder = "C:\\Users\\Mysticlone98756\\Desktop\\codin\\rhythm game(full-setup)\\client\\img\\noteskins\\default_4k"
notes = {}

for i in range(1, 5):
    file_name = f"receptor_{i}.png"
    file_path = os.path.join(noteskins_folder, file_name)
    if os.path.exists(file_path):
        notes[f"note_{i}"] = pygame.image.load(file_path)
    else:
        print("files not found: {file_path}")

note_left = notes.get("note_1")
note_down = notes.get("note_2")
note_up = notes.get("note_3")
note_right = notes.get("note_4")

if note_left is None or note_down is None or note_up is None or note_right is None:
    print("Some notes are missing!")
    


#auto load charts/songs from where? 
chart_folder= "C:\\Users\\Mysticlone98756\\Desktop\\codin\\rhythm game(full-setup)\\client\\charts"
chart_files = os.path.join(chart_folder, ".sm")
charts = glob.glob(chart_files)
title_image_path = os.path.join(title_image_folder, "title-image.png")

print(f"Loading image from: {title_image_path}")
if not os.path.exists(title_image_path):
    raise FileNotFoundError(f"Title image not found: {title_image_path}")

title_image = pygame.image.load(title_image_path)


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    if Upscroll == False:
        Downscroll = True
    elif Downscroll == False:
        Upscroll = True
            
    screen.fill("white")
    #screen.blit(text_surface, (75, 25))

    screen.blit(title_image, (100, 25))
    if note_left:
        scaled_note_left = pygame.transform.scale(note_left, (75, 50))
        screen.blit(scaled_note_left, (100, 300))
    if note_down:
        scaled_note_down = pygame.transform.scale(note_down, (50, 50))
        screen.blit(scaled_note_down, (200, 300))
    if note_up:
        scaled_note_up = pygame.transform.scale(note_up, (50, 50))
        screen.blit(scaled_note_up, (300, 300))
    if note_right:
        scaled_note_right = pygame.transform.scale(note_right, (50, 50))
        screen.blit(scaled_note_right, (400, 300))
        
    
    
    pygame.display.flip()
    pygame.time.Clock().tick(60)