import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import tkinter as tk
from PIL import Image, ImageTk
import threading
import pygame
from tkinter import simpledialog, messagebox
from Class import Song
from Database import Database
from Core import MusicCore
from Clap import ClapControl

class LibraryWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Library Manager")
        self.geometry("900x600")
        self.resizable(False, False)

        self.db = Database()

        ttk.Label(
            self,
            text="Library & Playlist Manager",
            font=("Segoe UI", 18, "bold")
        ).pack(pady=10)

        self.playlist_box = tk.Listbox(self, width=40, height=20)
        self.playlist_box.pack(side=LEFT, padx=20, pady=20)

        self.song_box = tk.Listbox(self, width=40, height=20)
        self.song_box.pack(side=LEFT, padx=20, pady=20)

        btn_frame = ttk.Frame(self)
        btn_frame.pack(side=LEFT, fill=Y, padx=10)

        ttk.Button(
            btn_frame,
            text="Create Playlist",
            command=self.CreatePlaylist
        ).pack(pady=5)

        ttk.Button(
            btn_frame,
            text="Add Song to Playlist",
            command=self.AddSongToPlaylist
        ).pack(pady=5)

        self.LoadSongs()

    def LoadSongs(self):
        self.song_box.delete(0, END)
        for song in self.db.GetAll():
            self.song_box.insert(END, f"{song.Title} - {song.Artist}")

    def CreatePlaylist(self):
        name = tk.simpledialog.askstring(
            "Playlist",
            "Enter playlist name:"
        )
        if name:
            self.playlist_box.insert(END, name)

    def AddSongToPlaylist(self):
        p = self.playlist_box.curselection()
        s = self.song_box.curselection()

        if not p or not s:
            ttk.ToastNotification(
                title="Error",
                message="Select playlist & song",
                duration=2000
            ).show_toast()
            return

        ttk.ToastNotification(
            title="Success",
            message="Song added to playlist",
            duration=2000
        ).show_toast()



class AddSongWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Add Song")
        self.geometry("500x500")
        self.resizable(False, False)

        self.db = Database()
        self.entries = {}

        ttk.Label(self, text="Add New Song",
                  font=("Segoe UI", 18, "bold")).pack(pady=20)

        fields = [
            ("Song ID", "SongID"),
            ("Title", "Title"),
            ("Artist", "Artist"),
            ("Year", "Year"),
            ("File Path", "Path"),
            ("Duration", "Duration")
        ]

        for label, key in fields:
            frame = ttk.Frame(self)
            frame.pack(fill=X, padx=30, pady=6)

            ttk.Label(frame, text=label, width=12).pack(side=LEFT)
            entry = ttk.Entry(frame)
            entry.pack(side=LEFT, fill=X, expand=True)

            self.entries[key] = entry

        ttk.Button(
            self,
            text="Save Song",
            bootstyle="success",
            command=self.SaveSong
        ).pack(pady=30)

    def SaveSong(self):
        try:
            song = Song(
                SongID=self.entries["SongID"].get(),
                Title=self.entries["Title"].get(),
                Artist=self.entries["Artist"].get(),
                Year=int(self.entries["Year"].get()),
                Path=self.entries["Path"].get(),
                Duration=int(self.entries["Duration"].get() or 0),
                Genre=self.entries["Genre"].get()
            )

            self.db.AddSong(song)

            ttk.ToastNotification(
                title="Success",
                message="Song saved to database",
                duration=3000
            ).show_toast()

            self.destroy()

        except Exception as e:
            ttk.ToastNotification(
                title="Error",
                message=str(e),
                duration=3000
            ).show_toast()


class AdminWindow(ttk.Window):
    def __init__(self):
        super().__init__(themename="darkly")
        self.title("LUNA - Admin")
        self.geometry("1920x1080")
        self.resizable(False, False)

        self.SetupBackground()
        self.LoadButtonImages()
        self.CreateButtons()

    def SetupBackground(self):
        self.canvas = tk.Canvas(self, width=1920, height=1080, highlightthickness=0)
        self.canvas.place(x=0, y=0)

        bg = Image.open(
            "C:/Users/HP/PycharmProjects/TubesBesarSD/TUBES BESAR LUNA/HALAMAN ADMIN/Background.png"
        ).resize((1920, 1080))

        self.bg_photo = ImageTk.PhotoImage(bg)
        self.canvas.create_image(0, 0, anchor="nw", image=self.bg_photo)

    def LoadButtonImages(self):
        self.addsong_img = ImageTk.PhotoImage(
            Image.open(
                "C:/Users/HP/PycharmProjects/TubesBesarSD/TUBES BESAR LUNA/HALAMAN ADMIN/BUTTON/BAddMusic.png"
            ).resize((750, 280))
        )

        self.library_img = ImageTk.PhotoImage(
            Image.open(
                "C:/Users/HP/PycharmProjects/TubesBesarSD/TUBES BESAR LUNA/HALAMAN ADMIN//BUTTON/BLibrary.png"
            ).resize((750, 280))
        )

    def CreateButtons(self):
        self.btn_addsong = self.canvas.create_image(
            600, 755,
            image=self.addsong_img,
            anchor="center"
        )

        self.btn_library = self.canvas.create_image(
            1375, 755,
            image=self.library_img,
            anchor="center"
        )

        self.canvas.tag_bind(
            self.btn_addsong,
            "<Button-1>",
            lambda e: self.OpenAddSong()
        )

        self.canvas.tag_bind(
            self.btn_library,
            "<Button-1>",
            lambda e: self.OpenLibrary()
        )

    def OpenAddSong(self):
        AddSongWindow(self)

    def OpenLibrary(self):
        LibraryWindow(self)





class UserWindow(ttk.Window):
    def __init__(self):
        super().__init__(themename="darkly")

        self.title("LUNA - User")
        self.geometry("1920x1080")
        self.resizable(False, False)

        pygame.init()

        self.core = MusicCore()
        self.db = Database()

        self.SetupCanvas()
        self.LoadImages()
        self.CreateButtons()

        self.after(500, self.CheckEnd)

    def SetupCanvas(self):
        self.canvas = tk.Canvas(
            self,
            width=1920,
            height=1080,
            highlightthickness=0
        )
        self.canvas.pack(fill="both", expand=True)

        bg = Image.open(
            "C:/Users/HP/PycharmProjects/TubesBesarSD/"
            "TUBES BESAR LUNA/HALAMAN USER/background_user_update.png"
        ).resize((1920, 1080))

        self.bg_img = ImageTk.PhotoImage(bg)

        # ⬇️ SIMPAN ID BACKGROUND
        self.bg_id = self.canvas.create_image(
            0, 0, anchor="nw", image=self.bg_img
        )
    def LoadImages(self):
        base = "C:/Users/HP/PycharmProjects/TubesBesarSD/TUBES BESAR LUNA/HALAMAN USER/"

        BTN = (70, 70)
        PLAY = (110, 110)
        MENU = (260, 70)

        self.img_search = ImageTk.PhotoImage(
            Image.open(base + "BUTTON_Search(1).png").resize(MENU)
        )
        self.img_create = ImageTk.PhotoImage(
            Image.open(base + "BUTTON_CreatePlaylist.png").resize(MENU)
        )
        self.img_library = ImageTk.PhotoImage(
            Image.open(base + "BUTTON_Library.png").resize(MENU)
        )

        self.img_prev = ImageTk.PhotoImage(
            Image.open(base + "PREV.png").resize(BTN)
        )
        self.img_play = ImageTk.PhotoImage(
            Image.open(base + "Play.png").resize(PLAY)
        )
        self.img_pause = ImageTk.PhotoImage(
            Image.open(base + "PAUSE.png").resize(BTN)
        )
        self.img_next = ImageTk.PhotoImage(
            Image.open(base + "NEXT.png").resize(BTN)
        )

    def CreateButtons(self):
        # ===== TOP MENU =====
        self.btn_create = self.canvas.create_image(
            350, 140, image=self.img_create, anchor="center"
        )
        self.btn_library = self.canvas.create_image(
            650, 140, image=self.img_library, anchor="center"
        )
        self.btn_search = self.canvas.create_image(
            950, 140, image=self.img_search, anchor="center"
        )

        y = 930
        self.btn_prev = self.canvas.create_image(760, y, image=self.img_prev)
        self.btn_play = self.canvas.create_image(900, y, image=self.img_play)
        self.btn_pause = self.canvas.create_image(1040, y, image=self.img_pause)
        self.btn_next = self.canvas.create_image(1180, y, image=self.img_next)

        self.canvas.tag_raise(self.btn_create)
        self.canvas.tag_raise(self.btn_library)
        self.canvas.tag_raise(self.btn_search)
        self.canvas.tag_raise(self.btn_prev)
        self.canvas.tag_raise(self.btn_play)
        self.canvas.tag_raise(self.btn_pause)
        self.canvas.tag_raise(self.btn_next)

        self.canvas.tag_bind(self.btn_create, "<Button-1>",
                             lambda e: self.CreatePlaylist())
        self.canvas.tag_bind(self.btn_library, "<Button-1>",
                             lambda e: self.OpenLibrary())
        self.canvas.tag_bind(self.btn_search, "<Button-1>",
                             lambda e: self.SearchSong())

        self.canvas.tag_bind(self.btn_prev, "<Button-1>",
                             lambda e: self.core.Prev())
        self.canvas.tag_bind(self.btn_play, "<Button-1>",
                             lambda e: self.core.PlayCurrent())
        self.canvas.tag_bind(self.btn_pause, "<Button-1>",
                             lambda e: self.core.Pause())
        self.canvas.tag_bind(self.btn_next, "<Button-1>",
                             lambda e: self.core.PlayNext())

    def CreatePlaylist(self):
        name = tk.simpledialog.askstring(
            "Create Playlist",
            "Enter playlist name:"
        )
        if name:
            self.db.CreatePlaylist(name)

    def OpenLibrary(self):
        playlists = self.db.GetPlaylists()
        msg = "\n".join(playlists) if playlists else "No playlist"
        tk.messagebox.showinfo("Library", msg)

    def SearchSong(self):
        keyword = tk.simpledialog.askstring(
            "Search",
            "Title / Artist / Genre:"
        )
        if not keyword:
            return

        songs = self.db.Search(keyword)
        if songs:
            self.core.SetQueue(songs)
            self.core.PlayCurrent()

    def CheckEnd(self):
        for event in pygame.event.get():
            if event.type == pygame.USEREVENT:
                self.core.PlayNext()

        self.after(200, self.CheckEnd)


class App(ttk.Window):
    def __init__(self):
        super().__init__(themename="darkly")
        self.title("LUNA")
        self.geometry("1920x1080")
        self.resizable(False, False)

        bg = Image.open(
            "C:/Users/HP/PycharmProjects/TubesBesarSD/TUBES BESAR LUNA/HALAMAN LOGIN/LoginBG.png"
        ).resize((1920, 1080))
        self.bg_photo = ImageTk.PhotoImage(bg)

        ttk.Label(self, image=self.bg_photo).place(
            x=0, y=0, relwidth=1, relheight=1
        )

        self.LoadButtons()

    def LoadButtons(self):
        self.admin_img = ImageTk.PhotoImage(Image.open(
            "C:/Users/HP/PycharmProjects/TubesBesarSD/TUBES BESAR LUNA/HALAMAN LOGIN/AdminB.png"
        ).resize((320, 120)))

        self.user_img = ImageTk.PhotoImage(Image.open(
            "C:/Users/HP/PycharmProjects/TubesBesarSD/TUBES BESAR LUNA/HALAMAN LOGIN/UserB.png"
        ).resize((320, 120)))

        tk.Button(
            self, image=self.admin_img,
            borderwidth=0,
            command=self.OpenAdmin
        ).place(x=615, y=520, anchor="center")

        tk.Button(
            self, image=self.user_img,
            borderwidth=0,
            command=self.OpenUser
        ).place(x=1260, y=520, anchor="center")

    def OpenAdmin(self):
        self.destroy()
        AdminWindow().mainloop()

    def OpenUser(self):
        self.destroy()
        UserWindow().mainloop()


if __name__ == "__main__":
    App().mainloop()
