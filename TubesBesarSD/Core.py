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

        # Load playlist dari database
        for song in self.db.GetAll():
            self.playlist.AddLast(song)

    def play_song(self, song):
        pygame.mixer.music.load(song.Path)
        pygame.mixer.music.play()
        self.history.Push(song.SongID)

    def play_current(self):
        song = self.playlist.Current()
        if song:
            self.play_song(song)

    def pause(self):
        pygame.mixer.music.pause()

    def resume(self):
        pygame.mixer.music.unpause()

    def next_song(self):
        # Prioritas queue
        if self.queue.data:
            song_id = self.queue.Dequeue()
            song = self.db.songs.get(song_id)
            if song:
                self.play_song(song)
                return

        # Fallback ke playlist
        song = self.playlist.NextSong()
        if song:
            self.play_song(song)

    def prev_song(self):
        song = self.playlist.PrevSong()
        if song:
            self.play_song(song)
