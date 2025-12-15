import pickle

class Database:
    def __init__(self, filename="database.pickle"):
        self.filename = filename
        self.songs = {}
        self.playlists = []
        self.Load()

    def Load(self):
        try:
            with open(self.filename, "rb") as f:
                data = pickle.load(f)
                self.songs = data.get("songs", {})
                self.playlists = data.get("playlists", [])
        except:
            self.songs = {}
            self.playlists = []

    def Save(self):
        with open(self.filename, "wb") as f:
            pickle.dump({
                "songs": self.songs,
                "playlists": self.playlists
            }, f)

    def AddSong(self, song):
        self.songs[song.SongID] = song
        self.Save()

    def GetAll(self):
        return list(self.songs.values())

    def Search(self, keyword):
        keyword = keyword.lower()
        return [
            s for s in self.songs.values()
            if keyword in s.Title.lower()
            or keyword in s.Artist.lower()
            or keyword in s.Genre.lower()
        ]

    def GetByGenre(self, genre):
        return [s for s in self.songs.values()
                if s.Genre.lower() == genre.lower()]

    # ===== PLAYLIST (MINIMAL) =====
    def CreatePlaylist(self, name):
        self.playlists.append(name)
        self.Save()

    def GetPlaylists(self):
        return self.playlists
