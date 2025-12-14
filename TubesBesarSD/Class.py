class Song:
    def __init__(self, SongID, Title, Artist, Year, Path, Duration=0):
        self.SongID = SongID
        self.Title = Title
        self.Artist = Artist
        self.Year = Year
        self.Path = Path
        self.Duration = Duration
        self.Metadata = {}

    def __repr__(self):
        return f"{self.Title} - {self.Artist}"


class DLLNode:
    def __init__(self, song):
        self.Song = song
        self.Next = None
        self.Prev = None


class DoubleLinkedList:
    def __init__(self):
        self.Head = None
        self.Tail = None
        self.Curr = None

    def AddLast(self, song):
        node = DLLNode(song)
        if self.Head is None:
            self.Head = self.Tail = self.Curr = node
        else:
            self.Tail.Next = node
            node.Prev = self.Tail
            self.Tail = node

    def NextSong(self):
        if self.Curr and self.Curr.Next:
            self.Curr = self.Curr.Next
        return self.Curr.Song if self.Curr else None

    def PrevSong(self):
        if self.Curr and self.Curr.Prev:
            self.Curr = self.Curr.Prev
        return self.Curr.Song if self.Curr else None

    def Current(self):
        return self.Curr.Song if self.Curr else None


class HistoryStack:
    def __init__(self):
        self.data = []

    def Push(self, song_id):
        self.data.append(song_id)

    def Pop(self):
        return self.data.pop() if self.data else None


class Queue:
    def __init__(self):
        self.data = []

    def Enqueue(self, song_id):
        self.data.append(song_id)

    def Dequeue(self):
        return self.data.pop(0) if self.data else None
