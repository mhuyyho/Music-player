# Các thư viện cần dùng

from lib import *
from PIL import Image, ImageTk


# Dark-mode cho app

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

# Các biến toàn cục

window = customtkinter.CTk()
current_song_btn = None # Button hiện tại của bài hát
current_file_path = None # Đường dẫn hiện tại của bài hát
after_id = None # Dùng để lưu id, quản lý hàm update_time
play_mode = True # Trạng thái đang phats nhạc
is_first_click = True
repeat_mode = False # Trạng thái đang lặp lại bài hát
song_list = []


# Khởi tạo pygame
pygame.mixer.init()

# Gọi hàm setup trong class để tạo window
setup = Setup(window)
setup.set_up()

#__________________________________________________________________FUNCTION_______________________________________________________________
# Toàn bộ function

# Cập nhật trạng thái nút pause
def image_update(img, btn):
    button_png = customtkinter.CTkImage(light_image=Image.open(os.path.join(PATH_IMAGES, img)), dark_image=Image.open(os.path.join(PATH_IMAGES, img)), size = (20,20))
    btn.configure(image = button_png)

# Chọn bài hát bằng cách click
def select_song(file_path, button):
    global current_file_path, current_song_btn, play_mode, is_first_click
    current_file_path = file_path
    # Kiểm tra xem có phải lần đầu chọn để phát nhạc hay không
    is_first_click = False 

    name_current_song_btn_label.configure(text=get_name_current_song_btn(file_path))

    # Kiểm tra button có tại hoặc đang sở hữu gía trị None hay không
    if current_song_btn is not None and current_song_btn.winfo_exists():
        current_song_btn.configure(fg_color="transparent")
    current_song_btn = button 
    # Cập nhật trạng thái nút pause
    image_update("pause.png", play_button)
    play_mode = False

# Xóa tất cả button trong Frame
def clear_songlist():
    for widget in songlist.winfo_children():
        widget.destroy()

# Cập nhật danh sách bài hát
def update_songlist():
    global song_list, current_file_path, current_song_btn
    clear_songlist()
    song_list.clear()
    for i, file_name in enumerate(os.listdir(PATH_MUSIC)):
        if file_name.endswith('.mp3'):
            file_path = os.path.join(PATH_MUSIC, file_name)
            button = customtkinter.CTkButton(
                songlist, text=file_name.split('.')[0], 
                bg_color="transparent", fg_color='transparent', width=WINDOW_WIDTH - 50
            )
            song_list.append((file_path,button))
            button.configure(command=lambda fp=file_path, btn=button: play_sound(fp, btn))
            button.grid(row=i, column=0)
            button.bind("<Button-1>", lambda e, fp=file_path, btn=button: select_song(fp, btn))
    
    # Gán bài hát hiện tại là bài hát đầu tiên
    if song_list:
        current_file_path, current_song_btn = song_list[0]


# Khai báo folder music
def import_music_folder():
    global PATH_MUSIC
    folder_selected = filedialog.askdirectory()  # Mỏư folder
    if folder_selected:  # Kiểm tra nguời dùng có chọn folder không
        PATH_MUSIC = folder_selected  # Cập nhật đường dẫn folder nhạc
        update_songlist()


# Sử dụng như một template để tạo nên nhiều frame có cấu trúc tương tự nhau
def create_frame(master, height, width, row, column, padx=0, pady=0):
    frame = customtkinter.CTkFrame(master=master, height=height, width=width, bg_color="transparent", fg_color='transparent')
    frame.grid(row=row, column=column, padx=padx, pady=pady)
    return frame

# Tìm chỉ số bài hát trong song_list theo tên
def find_song_index_by_name(song_name):
    for index, (file_path, button) in enumerate(song_list):
        if song_name.lower() in os.path.basename(file_path).lower():
            return index  # Trả về index nếu tìm thấy
    return -1  # Trả về -1 nếu không tìm thấy

# Tìm chỉ số bài hát trong song_list theo current_file_path và current_song_btn
def find_current_song_index():
    for index, (file_path, button) in enumerate(song_list):
        if file_path == current_file_path and button == current_song_btn:
            return index  # Trả về index nếu tìm thấy
    return -1  # Trả về -1 nếu không tìm thấy


# Dùng để trộn bài hát trong song_list
def shuffle_song():
    global song_list, current_file_path, current_song_btn

    # Xáo trộn danh sách bài hát
    random.shuffle(song_list)
    
    # Lấy bài hát đầu tiên trong danh sách sau khi xáo trộn
    if song_list:
        current_file_path, current_song_btn = song_list[0]
        
        # Phát bài hát đầu tiên trong danh sách đã xáo trộn
        play_sound(current_file_path, current_song_btn)
    pass

# Dùng để trở về bài hát trước đó
def prev_song():
    global song_list, current_file_path, current_song_btn

    index_prev = (find_current_song_index() - 1)% len(song_list)
    current_file_path, current_song_btn = song_list[index_prev]

    play_sound(current_file_path, current_song_btn)    
    pass

# Dùng để phát bài hát hiện tại
def play_current_song():
    global play_mode, current_song_btn, current_file_path, is_first_click, after_id
    if(play_mode):
        image_update("pause.png", play_button)
        play_mode = False
        pygame.mixer.music.unpause()
        if(is_first_click):
            play_sound(current_file_path, current_song_btn)
            is_first_click = False
        else:
            # Tiêps tục chạy thời gian của bài hát đang được phát
            if after_id is not None:
                window.after_cancel(after_id)
            update_time()
    else:
        image_update("play.png", play_button)
        play_mode = True
        pygame.mixer.music.pause()
        if after_id is not None:
            window.after_cancel(after_id)  # Dừng cập nhật thời gian
    pass

# Dùng để phát bài hát tiếp theo trong song_list
def next_song():
    
    global song_list, current_file_path, current_song_btn

    index_prev = (find_current_song_index() + 1) % len(song_list)
    current_file_path, current_song_btn = song_list[index_prev]

    play_sound(current_file_path, current_song_btn)
    pass

# Dùng để lặp lại bài hát đang được phát trong song_list
def repeat_song():
    global repeat_mode
    if( not repeat_mode):
        image_update("repeat_1.png",repeat_button_png)
        repeat_mode = True
        
    else:
        image_update("repeat.png",repeat_button_png)
        repeat_mode = False
    pass

# Dùng làm template cho các nút chức năng
def button_png(master, png_filename, func_name, row, column):
    button_png = customtkinter.CTkImage(light_image=Image.open(os.path.join(PATH_IMAGES, png_filename)), dark_image=Image.open(os.path.join(PATH_IMAGES, png_filename)), size = (20,20))
    name_button = customtkinter.CTkButton(master = master, image = button_png, command = func_name, bg_color="transparent", fg_color='transparent', text = "", width = 50, height = 50, hover = False)
    name_button.grid(row = row, column = column, padx = 0, pady = 0)
    return name_button

# Lấy thời gian hiện tại của bài hát đang được phát
def get_music_duration(file_path):
    if(file_path == None):
        return "00:00"
    audio = MP3(file_path)
    duration = int(audio.info.length) 
    minutes = duration // 60
    seconds = duration % 60
    return f"{minutes:02}:{seconds:02}"

# Lấy thời gian hiện tại của bài hát đang được phát version 2
def get_music_duration_seconds(file_path):
    audio = MP3(file_path)
    return int(audio.info.length)

# Thanh tìm kiếm 
def search_song(event=None):
    search_query = search_bar.get().lower()
    clear_songlist()

    if search_query == "":  # Nếu tìm kiếm rỗng, hiển thị lại tất cả bài hát
        update_songlist()
    else:
        for i, file_name in enumerate(os.listdir(PATH_MUSIC)):
            if file_name.endswith('.mp3') and search_query in file_name.lower():
                file_path = os.path.join(PATH_MUSIC, file_name)
                button = customtkinter.CTkButton(
                    songlist, text=file_name.split('.')[0], 
                    bg_color="transparent", fg_color='transparent', width=WINDOW_WIDTH - 50
                )
                button.configure(command=lambda fp=file_path, btn=button: play_sound(fp, btn))
                button.grid(row=i, column=0)
                button.bind("<Button-1>", lambda e, fp=file_path, btn=button: select_song(fp, btn))

    
#clear search bar
def clear_search(event=None):
    clear_songlist()  
    update_songlist()
    search_bar = customtkinter.CTkEntry(master=header_frame, bg_color="transparent", width=500, height=50, border_width=1, corner_radius=50, font=FONT_SEARCH_BAR, placeholder_text="What do you want to play?")
    search_bar.grid(row=0, column=0, padx=5, pady=5)
    search_bar.bind("<KeyRelease>", search_song)



# Điều chỉnh âm lượng
def custom_volume(value):
    if (value == 0):
        volume_lable.configure(image = volume_off_image)
    elif (value < 0.5):
        volume_lable.configure(image = volume_lv1_image)
    else:
        volume_lable.configure(image = volume_lv2_image)

    pygame.mixer.music.set_volume(value)



# Lấy tên của bài hát hiện tại
def get_name_current_song_btn(file_path):
    return (file_path.split('\\')[len(file_path.split('\\')) - 1]).split(".")[0]

# Câpj nhật thời gian của bài hát
def update_time():
    global after_id
    if pygame.mixer.music.get_busy():
        current_time = pygame.mixer.music.get_pos() // 1000
        current_time_label.configure(text=f"{current_time // 60:02}:{current_time % 60:02}")
        
        total_time = get_music_duration_seconds(current_file_path)
        music_time_label.configure(text=f"{total_time // 60:02}:{total_time % 60:02}")
        
        pro.set(current_time / total_time if total_time > 0 else 0)

        # Kiểm tra nếu đã đến cuối bài hát và chế độ lặp đang bật
        if current_time >= total_time:
            if repeat_mode:
                pygame.mixer.music.play()  # Lặp lại bài hát nêys repeat_mode đang được bật
            else:
                next_song()  # Phát bài hát tiếp theo

        after_id = window.after(1000, update_time)


# Phát bài hát và kiểm tra button hiện tại
def play_sound(file_path, button):
    global current_song_btn, current_file_path, after_id, scroll_position

    button.configure(fg_color=COLOR_INDIGO)
    if current_song_btn is not None and current_song_btn.winfo_exists():
        current_song_btn.configure(fg_color="transparent")

    current_song_btn = button
    current_file_path = file_path

    name_current_song_btn_label.configure(text=get_name_current_song_btn(file_path))

    music_time_label.configure(text=get_music_duration(current_file_path))

    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()

    if after_id is not None:
        window.after_cancel(after_id)
    update_time()


# Những frame chính
header_frame = create_frame(window, 60, WINDOW_WIDTH, 0, 0)
body_frame = create_frame(window, 500, WINDOW_WIDTH, 1, 0)
footer_frame = create_frame(window, 120, WINDOW_WIDTH, 2, 0) 
frame = create_frame(body_frame, 500, WINDOW_WIDTH, 0, 0)

# Thanh tìm kiếm
search_bar = customtkinter.CTkEntry(master=header_frame, bg_color="transparent", width=500, height=50, border_width=1, corner_radius=50, font=FONT_SEARCH_BAR, placeholder_text="What do you want to play?")
search_bar.grid(row=0, column=0, padx=5, pady=5)
search_bar.bind("<KeyRelease>", search_song)

# Danh sách bài hát
songlist = customtkinter.CTkScrollableFrame(frame, height=490, width=WINDOW_WIDTH - 50, scrollbar_fg_color="#212121", scrollbar_button_color="#212121")
songlist.grid(row=0, column=0, padx=5, pady=5)

# Footer
f1_footer = create_frame(footer_frame, 120, int(WINDOW_WIDTH//4), 0, 0)
f2_footer = create_frame(footer_frame, 120, 2*int(WINDOW_WIDTH//4), 0, 1)
f3_footer = create_frame(footer_frame, 120, int(WINDOW_WIDTH//4), 0, 2)

f21_footer = create_frame(f2_footer, 60, 2*int(WINDOW_WIDTH//4), 0, 0)
f22_footer = create_frame(f2_footer, 54, 2*int(WINDOW_WIDTH//4), 1, 0)
f22_footer.grid_propagate(False)
f1_footer.grid_propagate(False)
f2_footer.grid_propagate(False)
f3_footer.grid_propagate(False)


# Frame 1 footer: Tên bài hát
f1_footer.grid_rowconfigure(0, weight=1)
f1_footer.grid_columnconfigure(0, weight=1)
name_current_song_btn_label = customtkinter.CTkLabel(
    f1_footer,text="",font=FONT_TIME,bg_color="transparent",fg_color="transparent",text_color="white", corner_radius=10,pady=10,padx=20,width=100, anchor="center", wraplength=180  )
name_current_song_btn_label.grid(row=0, column=0, sticky="nsew")
f1_footer.grid_propagate(False) 

#Frame 2 footer : Các nút shuffle, next, prev, play, progress, timestamp
shuffle_button = button_png(f21_footer,'shuffle.png', shuffle_song, row = 0, column = 0)

prev_button = button_png(f21_footer,'previous.png', prev_song, row = 0, column = 1)

play_button = button_png(f21_footer,'play.png', play_current_song, row = 0, column = 2)

next_button = button_png(f21_footer,'next.png', next_song, row = 0, column = 3)

repeat_button_png = button_png(f21_footer,'repeat.png', repeat_song, row = 0, column = 4)


current_time_label = customtkinter.CTkLabel(f22_footer,text = "00:00", font=FONT_TIME)
current_time_label.grid(row = 0, column = 0, padx = 3, pady = 15)
pro = customtkinter.CTkProgressBar(f22_footer, width = 300, progress_color=COLOR_WHITE, height = None)
pro.grid(row = 0, column = 1, padx = 0, pady = 0)
music_time_label = customtkinter.CTkLabel(f22_footer,text = "00:00", font=FONT_TIME)
music_time_label.grid(row = 0, column = 3, padx = 3, pady = 15)



#Frame 3 footer: volume
volume_off_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(PATH_IMAGES, "volume_off.png")),                                      dark_image=Image.open(os.path.join(PATH_IMAGES, "volume_off.png")),
                                         size = (15,15))
volume_lv1_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(PATH_IMAGES, "volume_lv1.png")), 
                                         dark_image=Image.open(os.path.join(PATH_IMAGES, "volume_lv1.png")),
                                         size = (15,15))
volume_lv2_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(PATH_IMAGES, "volume_lv2.png")), 
                                         dark_image=Image.open(os.path.join(PATH_IMAGES, "volume_lv2.png")),
                                         size = (15,15))

# Center 
f3_footer.grid_rowconfigure(0, weight=1)
f3_footer.grid_columnconfigure(0, weight=1)
f3_footer.grid_columnconfigure(1, weight=1)

volume_lable = customtkinter.CTkLabel(f3_footer, image=volume_lv2_image, text = '')
volume_lable.grid(row=0, column=0, padx=5, sticky="e")

volume_slider = customtkinter.CTkSlider(f3_footer, from_=0, to = 1, command = custom_volume, width = 100)
volume_slider.grid(row=0, column=1, padx=5, sticky="w")
volume_slider.grid_propagate(False)
        
#Import button
download_button = customtkinter.CTkImage(light_image=Image.open(os.path.join(PATH_IMAGES, 'downloads.png')), 
                                         dark_image=Image.open(os.path.join(PATH_IMAGES, 'downloads.png')),
                                         size = (20,20))
import_button = customtkinter.CTkButton(
    master=window, image = download_button, command=import_music_folder,bg_color="transparent", fg_color='transparent', text = "",
    height = 20, width = 20
)
import_button.place(anchor = NW) 

# Pausing using spacebar key 
window.bind("<space>", lambda event: play_current_song())
# escape from searching
window.bind("<Escape>", lambda event: clear_search() )

update_songlist()

window.mainloop()