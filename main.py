import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import pygame
import random
import os
from mutagen.mp3 import MP3

# Initialize pygame
pygame.mixer.init()

# Global variables
window = tk.Tk()
current_song = None
current_file_path = None
after_id = None
scroll_position = 0
paused = False
songlist = []
PATH_IMAGES = "images"  # Replace with your path
PATH_MUSIC = "music"    # Replace with your music folder path
WINDOW_WIDTH = 800
FONT_SEARCH_BAR = ("Arial", 14)
FONT_TIME = ("Arial", 10)
COLOR_WHITE = "#FFFFFF"
COLOR_INDIGO = "#4B0082"

# Functions
def create_frame(master, height, width, row, column, padx=0, pady=0):
    frame = tk.Frame(master, height=height, width=width, bg="transparent")
    frame.grid(row=row, column=column, padx=padx, pady=pady)
    return frame

def shuffle_song():
    global songlist, current_song, current_file_path
    
    if not songlist:
        return
    
    random.shuffle(songlist)
    play_sound(songlist[0], None)

def prev_song():
    global current_song, songlist, current_file_path
    
    if not songlist or current_song is None:
        return

    current_index = songlist.index(current_song)
    
    if current_index > 0:
        prev_song_button = songlist[current_index - 1]
        play_sound(prev_song_button, None)
    else:
        play_sound(songlist[-1], None)

def play_song():
    global current_song, paused, current_file_path

    if current_song is None:
        return
    
    if paused:
        pygame.mixer.music.unpause()
        paused = False
    else:
        pygame.mixer.music.load(current_file_path)
        pygame.mixer.music.play(loops=0)
    
    update_time()

def next_song():
    global current_song, songlist, current_file_path

    if not songlist or current_song is None:
        return

    current_index = songlist.index(current_song)
    
    if current_index < len(songlist) - 1:
        next_song_button = songlist[current_index + 1]
        play_sound(next_song_button, None)
    else:
        play_sound(songlist[0], None)

def repeat_song():
    global current_song, current_file_path

    if current_song is None:
        return

    pygame.mixer.music.load(current_file_path)
    pygame.mixer.music.play(loops=0)
    update_time()

def button_png(master, png_filename, func_name, row, column):
    img = Image.open(os.path.join(PATH_IMAGES, png_filename))
    img = img.resize((20, 20), Image.ANTIALIAS)
    photo = ImageTk.PhotoImage(img)
    button = tk.Button(master, image=photo, command=func_name, bg="transparent", fg="transparent")
    button.image = photo  # Keep a reference to the image
    button.grid(row=row, column=column, padx=0, pady=0)
    return button

def get_music_duration(file_path):
    if(file_path is None):
        return "00:00"
    audio = MP3(file_path)
    duration = int(audio.info.length) 
    minutes = duration // 60
    seconds = duration % 60
    return f"{minutes:02}:{seconds:02}"

def get_music_duration_seconds(file_path):
    audio = MP3(file_path)
    return int(audio.info.length)

def search_song(event=None):
    search_query = search_bar.get().lower()
    clear_songlist()

    for i, file_name in enumerate(os.listdir(PATH_MUSIC)):
        if file_name.endswith('.mp3') and search_query in file_name.lower():
            file_path = os.path.join(PATH_MUSIC, file_name)
            button = tk.Button(songlist, text=file_name.split('.')[0], command=lambda fp=file_path, btn=button: play_sound(fp, btn))
            button.grid(row=i, column=0)

def custom_volume(value):
    if value == 0:
        volume_label.configure(image=volume_off_image)
    elif value < 0.5:
        volume_label.configure(image=volume_lv1_image)
    else:
        volume_label.configure(image=volume_lv2_image)

    pygame.mixer.music.set_volume(value)

def get_name_current_song(file_path):
    return file_path.split('\\')[-1].split(".")[0]

# Main window setup
window.geometry(f"{WINDOW_WIDTH}x600")
window.title("Music Player")

# Create frames
header_frame = create_frame(window, 60, WINDOW_WIDTH, 0, 0)
body_frame = create_frame(window, 500, WINDOW_WIDTH, 1, 0)
footer_frame = create_frame(window, 120, WINDOW_WIDTH, 2, 0)
frame = create_frame(body_frame, 500, WINDOW_WIDTH, 0, 0)

# Song search bar
search_bar = tk.Entry(master=header_frame, width=60, font=FONT_SEARCH_BAR)
search_bar.grid(row=0, column=0, padx=5, pady=5)
search_bar.bind("<KeyRelease>", search_song)

# List Song
songlist = tk.Frame(frame)
songlist.grid(row=0, column=0, padx=5, pady=5)

# Footer
f1_footer = create_frame(footer_frame, 120, int(WINDOW_WIDTH // 4), 0, 0)
f2_footer = create_frame(footer_frame, 120, 2 * int(WINDOW_WIDTH // 4), 0, 1)
f3_footer = create_frame(footer_frame, 120, int(WINDOW_WIDTH // 4), 0, 2)

# Footer frame 1: current song name
name_current_song_label = tk.Label(f1_footer, text="", font=FONT_TIME, fg="white")
name_current_song_label.grid(row=0, column=0, sticky="nsew")

# Footer frame 2: controls (shuffle, prev, play, next, repeat)
shuffle_button = button_png(f2_footer, 'shuffle.png', shuffle_song, 0, 0)
prev_button = button_png(f2_footer, 'previous.png', prev_song, 0, 1)
play_button = button_png(f2_footer, 'play.png', play_song, 0, 2)
next_button = button_png(f2_footer, 'next.png', next_song, 0, 3)
repeat_button_png = button_png(f2_footer, 'repeat.png', repeat_song, 0, 4)

# Footer frame 3: volume control
volume_label = tk.Label(f3_footer, text="Volume", fg="white")
volume_label.grid(row=0, column=0, padx=5)

volume_slider = tk.Scale(f3_footer, from_=0, to=1, orient="horizontal", command=custom_volume)
volume_slider.grid(row=0, column=1, padx=5)

def update_time():
    global after_id
    if pygame.mixer.music.get_busy():
        current_time = pygame.mixer.music.get_pos() // 1000
        current_time_label.configure(text=f"{current_time // 60:02}:{current_time % 60:02}")
        
        total_time = get_music_duration_seconds(current_file_path)
        music_time_label.configure(text=f"{total_time // 60:02}:{total_time % 60:02}")
        
        pro.set(current_time / total_time if total_time > 0 else 0)
        after_id = window.after(1000, update_time)

def play_sound(file_path, button):
    global current_song, current_file_path, after_id, scroll_position

    if current_song is not None:
        current_song.configure(fg="transparent")
    
    button.configure(fg=COLOR_INDIGO)
    current_song = button
    current_file_path = file_path

    music_time_label.configure(text=get_music_duration(current_file_path))

    name_current_song_label.configure(text=get_name_current_song(current_file_path))
    scroll_position = 0
    scroll_text()

    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()

    if after_id is not None:
        window.after_cancel(after_id)
    update_time()

# Clear song list
def clear_songlist():
    for widget in songlist.winfo_children():
        widget.destroy()

def update_songlist():
    clear_songlist()
    for i, file_name in enumerate(os.listdir(PATH_MUSIC)):
        if file_name.endswith('.mp3'):
            file_path = os.path.join(PATH_MUSIC, file_name)
            button = tk.Button(songlist, text=file_name.split('.')[0], command=lambda fp=file_path, btn=button: play_sound(fp, btn))
            button.grid(row=i, column=0)

update_songlist()

# Import music folder
def import_music_folder():
    global PATH_MUSIC
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        PATH_MUSIC = folder_selected
        update_songlist()

# File menu
file_menu = tk.Menu(window)
window.config(menu=file_menu)
file_menu.add_command(label="Import music folder", command=import_music_folder)

window.mainloop()
