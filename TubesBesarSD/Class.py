class Song:
    def __init__(self, SongID, Tittle, Artist, Year, Path, Duration=0):
        self.SongID = SongID
        self.Tittle = Tittle
        self.Artist = Artist
        self.Year = Year
        self.Path = Path
        self.Duration = Duration
        self.Metadata = {}

    def __repr__(self):
        return f"Song({self.SongID}, {self.Tittle}, {self.Artist})"

#########################################################################
class DLLNode:
    def __init__(self,Song):
        self.Song = Song
        self.Next = None
        self.Prev = None

class DoubleLinkedList:
    def __init__(self):
        self.Head = None
        self.Tail = None
        self.Curr = None
        self.Size = 0

    # tambah ke akhir playlist
    def AddLast(self, Song):
        Node = DLLNode(Song)

        if self.Head is None:
            self.Head = self.Tail = Node
            self.Curr = Node
        else:
            self.Tail.next = Node
            Node.Prev = self.Tail
            self.Tail = Node

        self.Size += 1

    # hapus berdasarkan SongID
    def RemID(self, SongID):
        Pointer = self.Head

        while Pointer is not None:
            if Pointer.Song.SongID == SongID:

                # update Head
                if Pointer.Prev is None:
                    self.Head = Pointer.Next
                    if self.Head:
                        self.Head.Prev = None

                # update Tail
                elif Pointer.Next is None:
                    self.Tail = Pointer.Prev
                    if self.Tail:
                        self.Tail.Next = None

                # Node tengah
                else:
                    Pointer.Prev.Next = Pointer.Next
                    Pointer.Next.Prev = Pointer.Prev

                # update Curr jika Node dihapus adalah yang sedang diputar
                if self.Curr == Pointer:
                    if Pointer.Next:
                        self.Curr = Pointer.Next
                    else:
                        self.Curr = Pointer.Prev

                self.Size -= 1
                return True

            Pointer = Pointer.Next

        return False

    # pindah ke lagu berikutnya
    def Next(self):
        if self.Curr is not None and self.Curr.Next is not None:
            self.Curr = self.Curr.Next
            return self.Curr.Song
        return None

    # pindah ke lagu sebelumnya
    def Previous(self):
        if self.Curr is not None and self.Curr.Prev is not None:
            self.Curr = self.Curr.Prev
            return self.Curr.Song
        return None

    # ambil lagu yang sedang diputar
    def Current(self):
        if self.Curr is None:
            return None
        return self.Curr.Song

    # ubah Curr berdasarkan ID
    def SetCurrID(self, SongID):
        Pointer = self.Head
        while Pointer is not None:
            if Pointer.Song.SongID == SongID:
                self.Curr = Pointer
                return True
            Pointer = Pointer.Next
        return False

    # debug print
    def Debug(self):
        Pointer = self.Head
        while Pointer is not None:
            print(Pointer.Song)
            Pointer = Pointer.Next



#########################################################################

class HistoryStack:
    def __init__(self):
        self.Data = []

    def Push(self, SongID):
        self.Data.append(SongID)

    def Pop(self):
        if len(self.Data) == 0:
            return None
        return self.Data.pop()

    def Peek(self):
        if len(self.Data) == 0:
            return None
        return self.Data[-1]

    def Empty(self):
        return len(self.Data) == 0

    def Show(self):
        return self.Data[:]



#########################################################################

class Queue:
    def __init__(self):
        self.Data = []

    def Enqueue(self, song_id):
        self.Data.append(song_id)

    def Dequeue(self):
        if len(self.Data) == 0:
            return None
        return self.Data.pop(0)

    def Empty(self):
        return len(self.Data) == 0

    def Size(self):
        return len(self.Data)

    def Show(self):
        return self.Data[:]