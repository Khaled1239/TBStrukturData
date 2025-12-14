import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import tkinter as tk
from PIL import Image, ImageTk

class App(ttk.Window):
    def __init__(self):
        super().__init__(themename="darkly")
        self.title("LUNA")
        self.geometry("1920x1080")
        self.resizable(False, False)

        self.ShowHome()

    def ShowHome(self):
        bg_img = Image.open("C:/Users/HP/PycharmProjects/TubesBesarSD/TUBES BESAR LUNA/HALAMAN LOGIN/LoginBG.png")
        bg_img = bg_img.resize((1920, 1080))
        self.bg_photo = ImageTk.PhotoImage(bg_img)

        bg_label = ttk.Label(self, image=self.bg_photo)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        admin_img = Image.open("C:/Users/HP/PycharmProjects/TubesBesarSD/TUBES BESAR LUNA/HALAMAN LOGIN/AdminB.png")
        admin_img = admin_img.resize((320, 120))   # << KONTROL SIZE
        self.admin_photo = ImageTk.PhotoImage(admin_img)

        btn_admin = tk.Button(
            self,
            image=self.admin_photo,
            borderwidth=0,
            highlightthickness=0,
            bg="#000000",
            activebackground="#000000",
            command=self.ShowAdmin
        )

        btn_admin.place(x=615, y=520, anchor="center")

        user_img = Image.open("C:/Users/HP/PycharmProjects/TubesBesarSD/TUBES BESAR LUNA/HALAMAN LOGIN/UserB.png")
        user_img = user_img.resize((320, 120))
        self.user_photo = ImageTk.PhotoImage(user_img)

        btn_user = tk.Button(
            self,
            image=self.user_photo,
            borderwidth=0,
            highlightthickness=0,
            bg="#000000",
            activebackground="#000000",
            command=self.ShowUser
        )

        btn_user.place(x=1260, y=520, anchor="center")

    def ShowAdmin(self):
        print("ADMIN")

    def ShowUser(self):
        print("USER")

if __name__ == "__main__":
    App().mainloop()
