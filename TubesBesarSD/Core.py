import pygame
import random
from Class import DoubleLinkedList, HistoryStack, Queue
from Database import Database


class MusicCore:
    def __init__(self):
        pygame.mixer.init()
        pygame.mixer.music.set_endevent(pygame.USEREVENT)

        self.db = Database()
        self.playlist = DoubleLinkedList()
        self.history = HistoryStack()
        self.queue = Queue()
        self.CurrentSong = None
        self.isPlaylistMode = False
        self.is_paused = False
        self.LoadLibrary()


    def LoadLibrary(self):
        for song in self.db.GetAll():
            self.playlist.AddLast(song)
    def Play(self, song):
        if not song:
            return
        pygame.mixer.music.load(song.Path)
        pygame.mixer.music.play()
        self.CurrentSong = song
        self.history.Push(song)

    def PlayCurrent(self):
        self.Play(self.playlist.Current())

    def Pause(self):
        pygame.mixer.music.pause()
        self.is_paused = True

    def Resume(self):
        pygame.mixer.music.unpause()
        self.is_paused = False


    def Prev(self):
        if self.isPlaylistMode:
            return
        self.Play(self.playlist.PrevSong())



    def PlayNow(self, song):
        if not song:
            return

        self.isPlaylistMode = False
        self.queue = Queue()
        self.Play(song)


    def PlayPlaylist(self, songs):
        if not songs:
            return

        self.isPlaylistMode = True
        self.queue = Queue()

        self.Play(songs[0])
        for s in songs[1:]:
            self.queue.Enqueue(s)



    def SetQueue(self, songs):
        self.queue = Queue()
        for s in songs:
            self.queue.Enqueue(s)

    def PlayNext(self):
        # 1. Jika masih ada queue (playlist)
        if not self.queue.IsEmpty():
            self.Play(self.queue.Dequeue())
            return

        # 2. Jika Playlist jika, lanjut random genre sama
        if self.isPlaylistMode and self.CurrentSong:
            self.isPlaylistMode = False  # keluar playlist

            same = self.db.GetByGenre(self.CurrentSong.Genre)
            same = [s for s in same if s.SongID != self.CurrentSong.SongID]

            if same:
                self.Play(random.choice(same))
                return

        # 3. Mode normal random genre
        if self.CurrentSong:
            same = self.db.GetByGenre(self.CurrentSong.Genre)
            same = [s for s in same if s.SongID != self.CurrentSong.SongID]
            if same:
                self.Play(random.choice(same))
                return

        # 4. fallback (library)
        self.Play(self.playlist.NextSong())

    def TogglePlayPause(self):
        if self.is_paused:
            self.Resume()
        else:
            self.Pause()


