import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import tkinter as tk
from PIL import Image, ImageTk

from Class import Song
from Database import Database


# ================= ADD SONG CHILD WINDOW =================
class AddSongWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Add Song")
        self.geometry("500x500")
        self.resizable(False, False)

        self.db = Database()

        self.create_form()

    def create_form(self):
        ttk.Label(self, text="Add New Song", font=("Segoe UI", 18, "bold")).pack(pady=20)

        self.entries = {}

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
            frame.pack(fill=X, padx=30, pady=5)

            ttk.Label(frame, text=label, width=12).pack(side=LEFT)
            entry = ttk.Entry(frame)
            entry.pack(side=LEFT, fill=X, expand=True)

            self.entries[key] = entry

        ttk.Button(
            self,
            text="Save Song",
            bootstyle="success",
            command=self.save_song
        ).pack(pady=25)

    def save_song(self):
        try:
            song = Song(
                SongID=self.entries["SongID"].get(),
                Title=self.entries["Title"].get(),
                Artist=self.entries["Artist"].get(),
                Year=int(self.entries["Year"].get()),
                Path=self.entries["Path"].get(),
                Duration=int(self.entries["Duration"].get() or 0)
            )

            self.db.AddSong(song)
            ttk.ToastNotification(
                title="Success",
                message="Song added successfully",
                duration=3000
            ).show_toast()

            self.destroy()

        except Exception as e:
            ttk.ToastNotification(
                title="Error",
                message=str(e),
                duration=3000
            ).show_toast()

# ================= ADMIN WINDOW =================
class AdminWindow(ttk.Window):
    def __init__(self):
        super().__init__(themename="darkly")
        self.title("LUNA - Admin")
        self.geometry("1920x1080")
        self.resizable(False, False)

        self.show_admin_ui()

    def show_admin_ui(self):
        bg_img = Image.open(
            "C:/Users/HP/PycharmProjects/TubesBesarSD/TUBES BESAR LUNA/HALAMAN ADMIN/Background.png"
        )
        bg_img = bg_img.resize((1920, 1080))
        self.bg_photo = ImageTk.PhotoImage(bg_img)

        ttk.Label(self, image=self.bg_photo).place(
            x=0, y=0, relwidth=1, relheight=1
        )
        ttk.Button(
            self,
            text="Add Song",
            bootstyle="info",
            width=20,
            command=self.AddSongW
        ).pack(anchor=W, padx=40, pady=20)

    def AddSongW(self):
        AddSongWindow(self)
# ================= USER WINDOW =================
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import threading
from PIL import Image, ImageTk

from Core import MusicCore
from Clap import ClapControl


class UserWindow(ttk.Window):
    def __init__(self):
        super().__init__(themename="darkly")
        self.title("LUNA - User")
        self.geometry("1920x1080")
        self.resizable(False, False)

        # Core Music Player
        self.core = MusicCore()

        self.show_user_ui()
        self.create_player_controls()
        self.start_clap_control()

    def show_user_ui(self):
        bg_img = Image.open(
            "C:/Users/HP/PycharmProjects/TubesBesarSD/TUBES BESAR LUNA/HALAMAN USER/background_user_update.png"
        )
        bg_img = bg_img.resize((1920, 1080))
        self.bg_photo = ImageTk.PhotoImage(bg_img)

        ttk.Label(self, image=self.bg_photo).place(
            x=0, y=0, relwidth=1, relheight=1
        )

    # ================= PLAYER BUTTONS =================
    def create_player_controls(self):
        btn_y = 900   # posisi Y tombol (sesuaikan kalau perlu)

        ttk.Button(
            self,
            text="Play",
            width=10,
            bootstyle="success",
            command=self.core.play_current
        ).place(x=650, y=btn_y)

        ttk.Button(
            self,
            text="Pause",
            width=10,
            bootstyle="warning",
            command=self.core.pause
        ).place(x=760, y=btn_y)

        ttk.Button(
            self,
            text="Resume",
            width=10,
            bootstyle="info",
            command=self.core.resume
        ).place(x=870, y=btn_y)

        ttk.Button(
            self,
            text="Prev",
            width=10,
            bootstyle="secondary",
            command=self.core.prev_song
        ).place(x=980, y=btn_y)

        ttk.Button(
            self,
            text="Next",
            width=10,
            bootstyle="primary",
            command=self.core.next_song
        ).place(x=1090, y=btn_y)

    # ================= CLAP CONTROL =================
    def start_clap_control(self):
        clap = ClapControl(self.core)
        threading.Thread(
            target=clap.listen,
            daemon=True
        ).start()

# ================= LOGIN WINDOW =================
class App(ttk.Window):
    def __init__(self):
        super().__init__(themename="darkly")
        self.title("LUNA")
        self.geometry("1920x1080")
        self.resizable(False, False)

        self.ShowHome()

    def ShowHome(self):
        bg_img = Image.open(
            "C:/Users/HP/PycharmProjects/TubesBesarSD/TUBES BESAR LUNA/HALAMAN LOGIN/LoginBG.png"
        )
        bg_img = bg_img.resize((1920, 1080))
        self.bg_photo = ImageTk.PhotoImage(bg_img)

        ttk.Label(self, image=self.bg_photo).place(
            x=0, y=0, relwidth=1, relheight=1
        )

        # ===== ADMIN BUTTON =====
        admin_img = Image.open(
            "C:/Users/HP/PycharmProjects/TubesBesarSD/TUBES BESAR LUNA/HALAMAN LOGIN/AdminB.png"
        )
        admin_img = admin_img.resize((320, 120))
        self.admin_photo = ImageTk.PhotoImage(admin_img)

        tk.Button(
            self,
            image=self.admin_photo,
            borderwidth=0,
            bg="#000000",
            activebackground="#000000",
            command=self.open_admin_window
        ).place(x=615, y=520, anchor="center")

        # ===== USER BUTTON =====
        user_img = Image.open(
            "C:/Users/HP/PycharmProjects/TubesBesarSD/TUBES BESAR LUNA/HALAMAN LOGIN/UserB.png"
        )
        user_img = user_img.resize((320, 120))
        self.user_photo = ImageTk.PhotoImage(user_img)

        tk.Button(
            self,
            image=self.user_photo,
            borderwidth=0,
            bg="#000000",
            activebackground="#000000",
            command=self.open_user_window
        ).place(x=1260, y=520, anchor="center")

    def open_admin_window(self):
        self.destroy()
        AdminWindow().mainloop()

    def open_user_window(self):
        self.destroy()
        UserWindow().mainloop()


# ================= RUN =================
if __name__ == "__main__":
    App().mainloop()
