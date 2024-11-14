from lib import *
from PIL import Image

# Use to like template for some frame
def create_frame(master, height, width, row, column, padx=0, pady=0):
    frame = customtkinter.CTkFrame(master=master, height=height, width=width, bg_color="transparent", fg_color='transparent')
    frame.grid(row=row, column=column, padx=padx, pady=pady)
    return frame



# Search song
def search_song(event):
    pass


# Use to shuffle play_list
def shuffle_song():
    pass

# Used to return to the previous song
def prev_song():
    pass

# Used to play the current song
def play_song():
    pass

# Use to return the next song
def next_song():
    pass

# Used to repeat the current song
def repeat_song():
    pass

# Used to like the template for some button 
def button_png(master, png_filename, func_name, row, column):
    button_png = customtkinter.CTkImage(light_image=Image.open(os.path.join(PATH_IMAGES, png_filename)), dark_image=Image.open(os.path.join(PATH_IMAGES, png_filename)), size = (20,20))
    name_button = customtkinter.CTkButton(master = master, image = button_png, command = func_name, bg_color="transparent", fg_color='transparent', text = "", width = 50, height = 50, hover = False)
    name_button.grid(row = row, column = column, padx = 0, pady = 0)
    return name_button


# Get the duration of the currently playing song
def get_music_duration(file_path):
    if(file_path == None):
        return "00:00"
    audio = MP3(file_path)
    duration = int(audio.info.length) 
    minutes = duration // 60
    seconds = duration % 60
    return f"{minutes:02}:{seconds:02}"

# Get the duration of the currently playing song version 2
def get_music_duration_seconds(file_path):
    audio = MP3(file_path)
    return int(audio.info.length)
