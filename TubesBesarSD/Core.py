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

    def Resume(self):
        pygame.mixer.music.unpause()

    def Prev(self):
        self.Play(self.playlist.PrevSong())

    def SetQueue(self, songs):
        self.queue = Queue()
        for s in songs:
            self.queue.Enqueue(s)

    def PlayNext(self):
        if not self.queue.IsEmpty():
            self.Play(self.queue.Dequeue())
            return

        if self.CurrentSong:
            same = self.db.GetByGenre(self.CurrentSong.Genre)
            same = [s for s in same if s.SongID != self.CurrentSong.SongID]
            if same:
                self.Play(random.choice(same))
                return

        self.Play(self.playlist.NextSong())
