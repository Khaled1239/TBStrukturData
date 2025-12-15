class Song:
    def __init__(self, SongID, Title, Artist, Year, Genre, Path, Duration=0):
        self.SongID = SongID
        self.Title = Title
        self.Artist = Artist
        self.Year = Year
        self.Genre = Genre
        self.Path = Path
        self.Duration = Duration

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
        self.CurrentNode = None

    def AddLast(self, song):
        node = DLLNode(song)
        if not self.Head:
            self.Head = self.Tail = self.CurrentNode = node
        else:
            self.Tail.Next = node
            node.Prev = self.Tail
            self.Tail = node

    def NextSong(self):
        if self.CurrentNode and self.CurrentNode.Next:
            self.CurrentNode = self.CurrentNode.Next
        return self.CurrentNode.Song if self.CurrentNode else None

    def PrevSong(self):
        if self.CurrentNode and self.CurrentNode.Prev:
            self.CurrentNode = self.CurrentNode.Prev
        return self.CurrentNode.Song if self.CurrentNode else None

    def Current(self):
        return self.CurrentNode.Song if self.CurrentNode else None


class HistoryStack:
    def __init__(self):
        self.data = []

    def Push(self, song):
        self.data.append(song)

    def Pop(self):
        return self.data.pop() if self.data else None


class Queue:
    def __init__(self):
        self.data = []

    def Enqueue(self, song):
        self.data.append(song)

    def Dequeue(self):
        return self.data.pop(0) if self.data else None

    def IsEmpty(self):
        return len(self.data) == 0
