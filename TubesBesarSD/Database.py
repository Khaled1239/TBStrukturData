import pickle
from Class import Song

class Database:
    def __init__(self, filename="database.pickle"):
        self.filename = filename
        self.songs = {}
        self.Load()

    def Load(self):
        try:
            with open(self.filename, "rb") as f:
                self.songs = pickle.load(f)
        except:
            self.songs = {}

    def Save(self):
        with open(self.filename, "wb") as f:
            pickle.dump(self.songs, f)

    def AddSong(self, song):
        self.songs[song.SongID] = song
        self.Save()

    def DeleteSong(self, song_id):
        if song_id in self.songs:
            del self.songs[song_id]
            self.Save()

    def GetAll(self):
        return list(self.songs.values())
