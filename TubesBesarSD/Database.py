import pickle

class Database:
    def __init__(self, filename="database.pickle"):
        self.filename = filename
        self.songs = {}
        self.playlists = {}
        self.Load()

    def Load(self):
        try:
            with open(self.filename, "rb") as f:
                data = pickle.load(f)
                self.songs = data.get("songs", {})
                self.playlists = data.get("playlists", {})
        except:
            self.songs = {}
            self.playlists = {}

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
        return [
            s for s in self.songs.values()
            if s.Genre.lower() == genre.lower()
        ]

    def CreatePlaylist(self, name):
        if name not in self.playlists:
            self.playlists[name] = []
            self.Save()

    def GetPlaylists(self):
        return list(self.playlists.keys())

    def GetPlaylistNames(self):
        return list(self.playlists.keys())

    def AddSongToPlaylist(self, playlist_name, song_id):
        if playlist_name in self.playlists:
            if song_id not in self.playlists[playlist_name]:
                self.playlists[playlist_name].append(song_id)
                self.Save()

    def GetSongsFromPlaylist(self, playlist_name):
        song_ids = self.playlists.get(playlist_name, [])
        return [
            self.songs[sid]
            for sid in song_ids
            if sid in self.songs
        ]
