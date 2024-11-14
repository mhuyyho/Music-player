class Music():
    def __init__(self, name, dir ) :
        self._name = name
        self._dir = dir

    def get_name(self):
        return self._name
    
    def get_dir(self):
        return self._dir
    
    def set_name(self, name : str):
        self._name = name

    def set_dir(self, dir : str):
        self._dir = dir


class PlayList(Music):
    def __init__(self, name):
        self._name = name
        self._playlist = []
    
    def get_playlist(self):
        return (self._name, self._playlist)

    def add_music(self, music:Music):   
        self._playlist.append(music)


class ListPlayList(PlayList):
    def __init__(self):
        self._listplaylist = []

    def add_play_list(self):
        self._listplaylist.append(super().get_playlist())