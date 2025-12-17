mport customtkinter as ctk
from auth import Auth
from app import TaskNovaApp

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

auth = Auth()

class Login(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("TaskNova Login")
        self.geometry("400x360")
        self.resizable(False, False)

        ctk.CTkLabel(
            self, text="TaskNova", font=("Segoe UI", 26, "bold")
        ).pack(pady=20)

        self.user = ctk.CTkEntry(self, placeholder_text="Username")
        self.user.pack(pady=10)

        self.pwd = ctk.CTkEntry(self, placeholder_text="Password", show="*")
        self.pwd.pack(pady=10)

        self.msg = ctk.CTkLabel(self, text="")
        self.msg.pack(pady=5)

        ctk.CTkButton(self, text="Login", command=self.login).pack(pady=10)
        ctk.CTkButton(self, text="Sign Up", command=self.signup).pack()

    def login(self):
        uid = auth.login(self.user.get(), self.pwd.get())
        if uid:
            self.destroy()
            TaskNovaApp(uid).mainloop()
        else:
            self.msg.configure(text="Invalid username or password", text_color="red")

    def signup(self):
        if auth.signup(self.user.get(), self.pwd.get()):
            uid = auth.login(self.user.get(), self.pwd.get())
            self.destroy()
            TaskNovaApp(uid).mainloop()
        else:
            self.msg.configure(text="Username already exists", text_color="red")

if __name__ == "__main__":
    Login().mainloop()
