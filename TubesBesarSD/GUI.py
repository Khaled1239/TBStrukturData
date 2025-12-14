import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import tkinter as tk
from PIL import Image, ImageTk


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


# ================= USER WINDOW =================
class UserWindow(ttk.Window):
    def __init__(self):
        super().__init__(themename="darkly")
        self.title("LUNA - User")
        self.geometry("1920x1080")
        self.resizable(False, False)

        self.show_user_ui()

    def show_user_ui(self):
        bg_img = Image.open(
            "C:/Users/HP/PycharmProjects/TubesBesarSD/TUBES BESAR LUNA/HALAMAN USER/background_user_update.png"
        )
        bg_img = bg_img.resize((1920, 1080))
        self.bg_photo = ImageTk.PhotoImage(bg_img)

        ttk.Label(self, image=self.bg_photo).place(
            x=0, y=0, relwidth=1, relheight=1
        )


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
