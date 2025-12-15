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
import os



BASE = os.path.dirname(os.path.abspath(__file__)) 



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

        self.playlist_box = tk.Listbox(
            self, width=35, height=20, exportselection=False
        )
        self.playlist_box.pack(side=LEFT, padx=20, pady=20)

        self.song_box = tk.Listbox(
            self, width=40, height=20, exportselection=False
        )
        self.song_box.pack(side=LEFT, padx=20, pady=20)

        btn_frame = ttk.Frame(self)
        btn_frame.pack(side=LEFT, fill=Y, padx=10)

        ttk.Button(
            btn_frame,
            text="Create Playlist",
            bootstyle="success",
            command=self.CreatePlaylist
        ).pack(pady=5, fill=X)

        ttk.Button(
            btn_frame,
            text="Add Song to Playlist",
            bootstyle="primary",
            command=self.AddSongToPlaylist
        ).pack(pady=5, fill=X)

        ttk.Button(
            btn_frame,
            text="Refresh",
            bootstyle="secondary",
            command=self.Refresh
        ).pack(pady=20, fill=X)

        ttk.Button(
            btn_frame,
            text="Delete Playlist",
            bootstyle="danger",
            command=self.DeletePlaylist
        ).pack(pady=5, fill=X)

        ttk.Button(
            btn_frame,
            text="Delete Song",
            bootstyle="danger",
            command=self.DeleteSong
        ).pack(pady=5, fill=X)

        self.LoadSongs()
        self.LoadPlaylists()

    def DeletePlaylist(self):
        p_index = self.playlist_box.curselection()
        if not p_index:
            tk.messagebox.showerror("Error", "Select a playlist to delete.")
            return

        playlist_name = self.playlist_box.get(p_index)
        if tk.messagebox.askyesno("Confirm Delete", f"Delete playlist '{playlist_name}'?"):
            if playlist_name in self.db.playlists:
                del self.db.playlists[playlist_name]
                self.db.Save()
                self.LoadPlaylists()
                tk.messagebox.showinfo("Success", "Playlist deleted.")

    def DeleteSong(self):
        s_index = self.song_box.curselection()
        if not s_index:
            tk.messagebox.showerror("Error", "Select a song to delete.")
            return

        song_text = self.song_box.get(s_index)
        song_id = song_text.split("|")[0].strip()

        if tk.messagebox.askyesno("Confirm Delete", f"Delete song '{song_text}'?"):
            if song_id in self.db.songs:
                del self.db.songs[song_id]
                # juga hapus dari semua playlist
                for pl in self.db.playlists.values():
                    if song_id in pl:
                        pl.remove(song_id)
                self.db.Save()
                self.LoadSongs()
                self.LoadPlaylists()
                tk.messagebox.showinfo("Success", "Song deleted.")

    def LoadSongs(self):
        self.song_box.delete(0, END)
        for song in self.db.GetAll():
            self.song_box.insert(
                END, f"{song.SongID} | {song.Title} - {song.Artist}"
            )

    def LoadPlaylists(self):
        self.playlist_box.delete(0, END)
        for p in self.db.GetPlaylists():
            self.playlist_box.insert(END, p)

    def Refresh(self):
        self.LoadSongs()
        self.LoadPlaylists()

    def CreatePlaylist(self):
        name = simpledialog.askstring(
            "Create Playlist",
            "Enter playlist name:"
        )
        if not name:
            return

        self.db.CreatePlaylist(name)
        self.LoadPlaylists()
        messagebox.showinfo("Success", "Playlist created")

    def AddSongToPlaylist(self):
        p_index = self.playlist_box.curselection()
        s_index = self.song_box.curselection()

        if not p_index or not s_index:
            messagebox.showerror(
                "Error", "Select playlist and song first"
            )
            return

        playlist_name = self.playlist_box.get(p_index)

        song_text = self.song_box.get(s_index)
        song_id = song_text.split("|")[0].strip()

        self.db.AddSongToPlaylist(playlist_name, song_id)

        messagebox.showinfo(
            "Success", "Song added to playlist"
        )




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
            ("Genre", "Genre"),
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
            duration_text = self.entries["Duration"].get()
            duration = int(duration_text) if duration_text.isdigit() else 0

            path = self.entries["Path"].get().strip().replace("\\", "/")

            song = Song(
                SongID=self.entries["SongID"].get(),
                Title=self.entries["Title"].get(),
                Artist=self.entries["Artist"].get(),
                Year=int(self.entries["Year"].get()),
                Genre=self.entries["Genre"].get(),
                Path=path,
                Duration=duration
                )

            self.db.AddSong(song)
            messagebox.showinfo("Success", "Song saved to database")
            self.destroy()

        except Exception as e:
            messagebox.showerror("Error", str(e))



class AdminWindow(ttk.Window):
    def __init__(self):
        super().__init__(themename="darkly")
        self.title("LUNA - Admin")
        self.geometry("1920x1080")
        self.resizable(False, False)

        self.SetupBackground()
        self.LoadButtonImages()
        self.CreateButtons()

    
    def Logout(self):
        self.destroy()
        App().mainloop()


    def SetupBackground(self):
        self.canvas = tk.Canvas(self, width=1920, height=1080, highlightthickness=0)
        self.canvas.place(x=0, y=0)

        bg = Image.open(
            BASE + "/TUBES BESAR LUNA/HALAMAN ADMIN/Background.png"
        ).resize((1920, 1080))

        self.bg_photo = ImageTk.PhotoImage(bg)
        self.canvas.create_image(0, 0, anchor="nw", image=self.bg_photo)

    def LoadButtonImages(self):
        self.addsong_img = ImageTk.PhotoImage(
            Image.open(
                BASE + "/TUBES BESAR LUNA/HALAMAN ADMIN/BUTTON/BAddMusic.png"
            ).resize((750, 280))
        )

        self.logout_img = ImageTk.PhotoImage(
            Image.open(BASE + "/TUBES BESAR LUNA/BLogout.png").resize((140, 70))
        )

        self.library_img = ImageTk.PhotoImage(
            Image.open(
                BASE + "/TUBES BESAR LUNA/HALAMAN ADMIN/BUTTON/BLibrary.png"
            ).resize((750, 280))
        )

    def CreateButtons(self):
        self.btn_addsong = self.canvas.create_image(
            600, 755,
            image=self.addsong_img,
            anchor="center"
        )

        self.btn_logout = self.canvas.create_image(
            985, 940,
            image=self.logout_img,
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

        self.canvas.tag_bind(
            self.btn_logout,
            "<Button-1>",
            lambda e: self.Logout()
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

        # ===== CLAP CONTROL =====
        self.clap = ClapControl(self.core)

        import threading
        threading.Thread(
            target=self.clap.Listen,
            daemon=True
        ).start()

        self.SetupCanvas()
        self.LoadImages()
        self.CreateButtons()

        self.bind("<ButtonPress-3>", self.StartPTT)
        self.bind("<ButtonRelease-3>", self.StopPTT)

        self.after(500, self.CheckEnd)

    def ShowCurrentSong(self):
        song = self.core.CurrentSong
        if not song:
            tk.messagebox.showinfo("Current Song", "No song is currently playing.")
            return

        info = f"""
                Title  : {song.Title}
                Artist : {song.Artist}
                Genre  : {song.Genre}
                Year   : {song.Year}
                Duration: {song.Duration}
                """
        tk.messagebox.showinfo("Current Song Info", info)


    def ShowHistory(self):
        win = tk.Toplevel(self)
        win.title("History Pemutaran")
        win.geometry("400x300")

        listbox = tk.Listbox(win, width=50, height=15)
        listbox.pack(padx=10, pady=10, fill="both", expand=True)

        temp = []
        while self.core.history.data:
            song = self.core.history.Pop()
            temp.append(song)
        for song in temp:
            listbox.insert(
                tk.END,
                f"{song.Title} - {song.Artist} ({song.Genre})"
            )

        for song in reversed(temp):
            self.core.history.Push(song)

    # PTT
    def StartPTT(self, event=None):
        self.clap.StartPTT()
        print("PTT ON")

    def StopPTT(self, event=None):
        self.clap.StopPTT()
        print("PTT OFF")

    def Logout(self):
        self.destroy()
        App().mainloop()

    def SetupCanvas(self):
        self.canvas = tk.Canvas(
            self,
            width=1920,
            height=1080,
            highlightthickness=0
        )
        self.canvas.pack(fill="both", expand=True)

        bg = Image.open(
            BASE + "/TUBES BESAR LUNA/HALAMAN USER/background_user_update.png"
        ).resize((1920, 1080))

        self.bg_img = ImageTk.PhotoImage(bg)
        self.canvas.create_image(0, 0, anchor="nw", image=self.bg_img)


    def LoadImages(self):
        base = BASE + "/TUBES BESAR LUNA/HALAMAN USER/"

        BTN = (70, 70)
        MENU = (380, 260)

        self.img_search = ImageTk.PhotoImage(
            Image.open(base + "BUTTON_Search(1).png").resize(MENU)
        )
        self.img_history = ImageTk.PhotoImage(
            Image.open(base + "RecentlyPLayedB.png").resize((247,65))
        )
        self.img_create = ImageTk.PhotoImage(
            Image.open(base + "BUTTON_CreatePlaylist.png").resize(MENU)
        )
        self.img_library = ImageTk.PhotoImage(
            Image.open(base + "BUTTON_Library.png").resize(MENU)
        )

        self.img_songinfo = ImageTk.PhotoImage(
            Image.open(base + "SongInfo.png").resize((394,70))
        )

        self.img_prev = ImageTk.PhotoImage(
            Image.open(base + "PREV.png").resize(BTN)
        )
        self.img_play = ImageTk.PhotoImage(
            Image.open(base + "Play.png").resize(BTN)
        )
        self.img_pause = ImageTk.PhotoImage(
            Image.open(base + "PAUSE.png").resize(BTN)
        )
        self.img_next = ImageTk.PhotoImage(
            Image.open(base + "NEXT.png").resize(BTN)
        )

        self.logout_img = ImageTk.PhotoImage(
            Image.open(BASE + "/TUBES BESAR LUNA/BLogout.png").resize((140, 70))
        )

    def CreateButtons(self):
        self.btn_create = self.canvas.create_image(
            480, 700, image=self.img_create, anchor="center"
        )
        self.btn_library = self.canvas.create_image(
            960, 700, image=self.img_library, anchor="center"
        )
        self.btn_search = self.canvas.create_image(
            1440, 700, image=self.img_search, anchor="center"
        )

        self.btn_logout = self.canvas.create_image(
            1665, 965, image=self.logout_img, anchor="center"
        )
        
        self.btn_history = self.canvas.create_image(
            1590, 237, image=self.img_history, anchor="center"
        )

        self.btn_songinfo = self.canvas.create_image(
            380, 965, image=self.img_songinfo, anchor="center"
        )

        y = 965
        self.btn_prev = self.canvas.create_image(720, y, image=self.img_prev)
        self.btn_play = self.canvas.create_image(880, y, image=self.img_play)
        self.btn_pause = self.canvas.create_image(1040, y, image=self.img_pause)
        self.btn_next = self.canvas.create_image(1200, y, image=self.img_next)

        self.canvas.tag_bind(self.btn_logout, "<Button-1>",
                             lambda e: self.Logout())
        self.canvas.tag_bind(self.btn_create, "<Button-1>",
                             lambda e: self.CreatePlaylist())
        self.canvas.tag_bind(self.btn_library, "<Button-1>",
                             lambda e: self.OpenLibrary())
        self.canvas.tag_bind(self.btn_search, "<Button-1>",
                             lambda e: self.SearchSong())
        self.canvas.tag_bind(self.btn_history, "<Button-1>",
                             lambda e: self.ShowHistory())
        self.canvas.tag_bind(self.btn_songinfo, "<Button-1>",
                             lambda e: self.ShowCurrentSong())
        self.canvas.tag_bind(self.btn_prev, "<Button-1>",
                             lambda e: self.core.Prev())
        self.canvas.tag_bind(self.btn_play, "<Button-1>",
                             lambda e: self.core.Resume())
        self.canvas.tag_bind(self.btn_pause, "<Button-1>",
                             lambda e: self.core.Pause())
        self.canvas.tag_bind(self.btn_next, "<Button-1>",
                             lambda e: self.core.PlayNext())

    def CreatePlaylist(self):
        name = tk.simpledialog.askstring(
            "Create Playlist", "Enter playlist name:"
        )
        if name:
            self.db.CreatePlaylist(name)

    def OpenLibrary(self):
        PlaylistSelectWindow(self)

    def SearchSong(self):
        keyword = tk.simpledialog.askstring(
            "Search", "Title / Artist / Genre:"
        )
        if keyword:
            songs = self.db.Search(keyword)
            if songs:
                self.core.PlayPlaylist(songs)

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
            BASE + "/TUBES BESAR LUNA/HALAMAN LOGIN/LoginBG.png"
        ).resize((1920, 1080))
        self.bg_photo = ImageTk.PhotoImage(bg)

        ttk.Label(self, image=self.bg_photo).place(
            x=0, y=0, relwidth=1, relheight=1
        )

        self.LoadButtons()

    def LoadButtons(self):
        self.admin_img = ImageTk.PhotoImage(Image.open(
            BASE + "/TUBES BESAR LUNA/HALAMAN LOGIN/AdminB.png"
        ).resize((320, 120)))

        self.user_img = ImageTk.PhotoImage(Image.open(
            BASE + "/TUBES BESAR LUNA/HALAMAN LOGIN/UserB.png"
        ).resize((320, 120)))

        tk.Button(
            self, image=self.admin_img,
            borderwidth=0,
            command=self.OpenAdmin
        ).place(x=619, y=519, anchor="center")

        tk.Button(
            self, image=self.user_img,
            borderwidth=0,
            command=self.OpenUser
        ).place(x=1259, y=519, anchor="center")

    def OpenAdmin(self):
        self.destroy()
        AdminWindow().mainloop()

    def OpenUser(self):
        self.destroy()
        UserWindow().mainloop()

class PlaylistSelectWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Your Playlists")
        self.geometry("400x600")

        self.parent = parent
        self.db = Database()

        ttk.Label(
            self, text="Select Playlist",
            font=("Segoe UI", 14, "bold")
        ).pack(pady=10)

        self.listbox = tk.Listbox(self, height=15)
        self.listbox.pack(fill=BOTH, expand=True, padx=20)

        for name in self.db.GetPlaylistNames():
            self.listbox.insert(END, name)

        ttk.Button(
            self, text="Open Playlist",
            command=self.OpenPlaylist
        ).pack(pady=10)

    def OpenPlaylist(self):
        sel = self.listbox.curselection()
        if not sel:
            return

        name = self.listbox.get(sel)
        PlaylistPlayerWindow(self.parent, name)
        self.destroy()


class PlaylistPlayerWindow(tk.Toplevel):
    def __init__(self, parent, playlist_name):
        super().__init__(parent)
        self.title(playlist_name)
        self.geometry("500x500")

        self.db = Database()
        self.core = parent.core

        ttk.Label(
            self, text=playlist_name,
            font=("Segoe UI", 16, "bold")
        ).pack(pady=10)

        self.song_box = tk.Listbox(self)
        self.song_box.pack(fill=BOTH, expand=True, padx=20)

        self.songs = self.db.GetSongsFromPlaylist(playlist_name)

        for s in self.songs:
            self.song_box.insert(END, f"{s.Title} - {s.Artist}")

        ttk.Button(
            self, text="Play Playlist",
            command=self.PlayPlaylist
        ).pack(pady=10)

    def PlayPlaylist(self):
        if self.songs:
            self.core.PlayPlaylist(self.songs)


if __name__ == "__main__":
    App().mainloop()
