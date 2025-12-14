import pygame
from Class import DoubleLinkedList, HistoryStack, Queue
from Database import Database

class MusicCore:
    def __init__(self):
        pygame.mixer.init()
        self.db = Database()
        self.playlist = DoubleLinkedList()
        self.history = HistoryStack()
        self.queue = Queue()

        for song in self.db.GetAll():
            self.playlist.AddLast(song)

    def Play(self, song):
        pygame.mixer.music.load(song.Path)
        pygame.mixer.music.play()
        self.history.Push(song.SongID)

    def Pause(self):
        pygame.mixer.music.pause()

    def Resume(self):
        pygame.mixer.music.unpause()

    def Next(self):
        song = self.playlist.NextSong()
        if song:
            self.Play(song)

    def Previous(self):
        song = self.playlist.PrevSong()
        if song:
            self.Play(song)
