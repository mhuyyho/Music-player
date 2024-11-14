
from define import *

class Setup():
    def __init__(self, window):
        self._window = window

    def get_window(self):
        return self._window
    
    def set_window(self, window):
        self._window = window
    
    def set_up(self):
        #Size window
        self.get_window().geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{WINDOW_POSITION_LEFT}+{WINDOW_POSITION_RIGHT}")

        #Title
        self.get_window().title("Music Player")

        #Icon
        self.get_window().iconbitmap(os.path.join(PATH_IMAGES, "icon.ico"))

        #Backgrond
        # self.get_window()["background"] = BACKGROUND_COLOR

        #Not resize window    
        self.get_window().resizable(False,False)




