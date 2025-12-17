import customtkinter as ctk
from tkcalendar import DateEntry
from datetime import date
from auth import Auth
from task import TaskNovaManager

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

auth = Auth()

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("TaskNova ✨")
        self.state("zoomed")

        self.user_id = None
        self.login_frame = LoginFrame(self)
        self.task_frame = None

        self.login_frame.pack(fill="both", expand=True)

    def show_tasks(self, user_id):
        self.user_id = user_id
        self.login_frame.pack_forget()
        self.task_frame = TaskFrame(self, user_id)
        self.task_frame.pack(fill="both", expand=True)

    def logout(self):
        self.task_frame.pack_forget()
        self.login_frame = LoginFrame(self)
        self.login_frame.pack(fill="both", expand=True)


class LoginFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        ctk.CTkLabel(
            self, text="TaskNova Login",
            font=("Segoe UI", 28, "bold")
        ).pack(pady=30)

        self.user = ctk.CTkEntry(self, placeholder_text="Username")
        self.user.pack(pady=10)

        self.pwd = ctk.CTkEntry(self, placeholder_text="Password", show="*")
        self.pwd.pack(pady=10)

        self.msg = ctk.CTkLabel(self, text="")
        self.msg.pack()

        ctk.CTkButton(self, text="Login", command=self.login).pack(pady=10)
        ctk.CTkButton(self, text="Sign Up", command=self.signup).pack()

    def login(self):
        uid = auth.login(self.user.get(), self.pwd.get())
        if uid:
            self.master.show_tasks(uid)
        else:
            self.msg.configure(text="Invalid login", text_color="red")

    def signup(self):
        if auth.signup(self.user.get(), self.pwd.get()):
            uid = auth.login(self.user.get(), self.pwd.get())
            self.master.show_tasks(uid)
        else:
            
            self.msg.configure(text="User already exists", text_color="red")


class TaskFrame(ctk.CTkFrame):
    def __init__(self, master, user_id):
        super().__init__(master)
        self.user_id = user_id
        self.manager = TaskNovaManager()

        ctk.CTkLabel(
            self, text="TaskNova",
            font=("Segoe UI", 32, "bold")
        ).pack(pady=10)

        ctk.CTkButton(
            self, text="🔒 Logout",
            fg_color="red", hover_color="#aa0000",
            command=self.master.logout
        ).pack(pady=10)

        # Input section
        input_frame = ctk.CTkFrame(self)
        input_frame.pack(pady=10)

        self.task_entry = ctk.CTkEntry(
            input_frame, width=300, placeholder_text="Enter task"
        )
        self.task_entry.grid(row=0, column=0, padx=8)

        self.date = DateEntry(input_frame, date_pattern="yyyy-mm-dd")
        self.date.grid(row=0, column=1, padx=8)

        self.priority = ctk.CTkOptionMenu(
            input_frame, values=["High", "Medium", "Low"]
        )
        self.priority.set("Medium")
        self.priority.grid(row=0, column=2, padx=8)

        ctk.CTkButton(
            input_frame, text="➕ Add Task",
            command=self.add_task
        ).grid(row=0, column=3, padx=8)

        # Task ID entry
        self.id_entry = ctk.CTkEntry(
            self, width=200, placeholder_text="Enter Task ID"
        )
        self.id_entry.pack(pady=5)

        # Action buttons
        action = ctk.CTkFrame(self)
        action.pack(pady=5)

        ctk.CTkButton(
            action, text="✅ Complete",
            command=self.complete_task
        ).grid(row=0, column=0, padx=15)

        ctk.CTkButton(
            action, text="❌ Delete",
            fg_color="red", hover_color="#aa0000",
            command=self.delete_task
        ).grid(row=0, column=1, padx=15)

        # Task list
        self.task_list = ctk.CTkScrollableFrame(
            self, width=1100, height=420
        )
        self.task_list.pack(pady=15)

        self.load_tasks()

    def load_tasks(self):
        for w in self.task_list.winfo_children():
            w.destroy()

        today = date.today()

        for t in self.manager.get_tasks(self.user_id):
            task_id, task, status, due_date, priority = t

            # COLOR LOGIC
            if status == "Completed":
                color = "green"
                icon = "🟢"
            else:
                if priority == "High":
                    color = "red"
                    icon = "🔴"
                elif priority == "Medium":
                    color = "yellow"
                    icon = "🟡"
                else:
                    color = "lightgreen"
                    icon = "🟢"

            overdue = " ⚠ OVERDUE" if due_date < today and status == "Pending" else ""

            text = f"{icon} ID:{task_id} | {task} | {status} | Due:{due_date} | {priority}{overdue}"

            ctk.CTkLabel(
                self.task_list,
                text=text,
                text_color=color,
                font=("Segoe UI", 16)
            ).pack(anchor="w", pady=4, padx=10)

    def add_task(self):
        if self.task_entry.get():
            self.manager.add_task(
                self.task_entry.get(),
                self.date.get_date(),
                self.priority.get(),
                self.user_id
            )
            self.task_entry.delete(0, "end")
            self.load_tasks()

    def complete_task(self):
        if self.id_entry.get():
            self.manager.complete_task(int(self.id_entry.get()), self.user_id)
            self.load_tasks()

    def delete_task(self):
        if self.id_entry.get():
            self.manager.delete_task(int(self.id_entry.get()), self.user_id)
            self.load_tasks()


if __name__ == "__main__":
    App().mainloop()
