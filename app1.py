import tkinter as tk
from tkinter import messagebox
import subprocess

# ====== MAIN APPLICATION CLASS ======
class OfflineGenieApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Offline Genie")
        self.attributes('-fullscreen', True)  # Fullscreen

        container = tk.Frame(self)
        container.pack(fill="both", expand=True)

        self.frames = {}
        for F in (HomePage, TravelAssistantPage, NavigationPage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(HomePage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

# ====== HOMEPAGE ======
class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = tk.Label(self, text="Offline Genie", font=("Arial", 24, "bold"))
        label.pack(pady=40)

        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=20)

        genie_btn = tk.Button(
            btn_frame, text="Start Travel Assistant",
            command=lambda: controller.show_frame(TravelAssistantPage),
            width=25, height=2, bg="lightblue", font=("Arial", 12)
        )
        genie_btn.grid(row=0, column=0, padx=20)

        nav_btn = tk.Button(
            btn_frame, text="Start Navigation Module",
            command=lambda: controller.show_frame(NavigationPage),
            width=25, height=2, bg="lightgreen", font=("Arial", 12)
        )
        nav_btn.grid(row=0, column=1, padx=20)

        exit_btn = tk.Button(
            self, text="Exit",
            command=controller.quit,
            width=20, height=2, bg="pink", font=("Arial", 12)
        )
        exit_btn.pack(pady=30)

# ====== TRAVEL ASSISTANT PAGE ======
class TravelAssistantPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = tk.Label(self, text="Travel Assistant Running...", font=("Arial", 20, "bold"))
        label.pack(pady=40)

        # Run offline_genie.py as subprocess
        run_btn = tk.Button(
            self, text="Launch Travel Assistant",
            command=self.launch_genie,
            width=30, height=2, bg="lightblue", font=("Arial", 12)
        )
        run_btn.pack(pady=20)

        back_btn = tk.Button(
            self, text="Back to Home",
            command=lambda: controller.show_frame(HomePage),
            width=20, height=2, bg="orange", font=("Arial", 12)
        )
        back_btn.pack(pady=30)

    def launch_genie(self):
        try:
            subprocess.Popen(["python", "offline_genie.py"])
        except Exception as e:
            messagebox.showerror("Error", f"Failed to launch Travel Assistant.\n{e}")

# ====== NAVIGATION PAGE ======
class NavigationPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = tk.Label(self, text="Navigation Module Running...", font=("Arial", 20, "bold"))
        label.pack(pady=40)

        # Run navigation.py as subprocess
        run_btn = tk.Button(
            self, text="Launch Navigation",
            command=self.launch_navigation,
            width=30, height=2, bg="lightgreen", font=("Arial", 12)
        )
        run_btn.pack(pady=20)

        back_btn = tk.Button(
            self, text="Back to Home",
            command=lambda: controller.show_frame(HomePage),
            width=20, height=2, bg="orange", font=("Arial", 12)
        )
        back_btn.pack(pady=30)

    def launch_navigation(self):
        try:
            subprocess.Popen(["python", "navigation.py"])
        except Exception as e:
            messagebox.showerror("Error", f"Failed to launch Navigation Module.\n{e}")

# ====== RUN APP ======
if __name__ == "__main__":
    app = OfflineGenieApp()
    app.mainloop()
