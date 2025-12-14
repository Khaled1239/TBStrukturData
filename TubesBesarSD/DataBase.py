import pickle
from typing import Dict
from Class import Song

class Database:
    def __init__(self, filename='DataBase.pickle'):
        self.filename = filename
        self.Songs: Dict[str, Song] = {}

    def Load(self):
        try:
            with open(self.filename, 'rb') as f:
                self.Songs = pickle.load(f)
        except FileNotFoundError:
            self.Songs = {}

    def Save(self):
        with open(self.filename, 'wb') as f:
            pickle.dump(self.Songs, f)

    def AddS(self, song: Song):
        self.Songs[song.SongID] = song
        self.Save()

    def UpdateS(self, SongID: str, **kwargs):
        if SongID in self.Songs:
            for k,v in kwargs.items():
                setattr(self.Songs[SongID], k, v)
            self.Save()
            return True
        return False

    def DeleteS(self, SongID: str):
        if SongID in self.Songs:
            del self.Songs[SongID]
            self.Save()
            return True
        return False

    def AllS(self):
        return list(self.Songs.values())
