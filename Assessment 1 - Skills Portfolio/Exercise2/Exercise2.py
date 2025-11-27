import tkinter as tk
from tkinter import messagebox
import random
import os

class JokeApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Alexa Joke Assistant")
        self.master.geometry("550x400")
        self.master.config(bg="#FFF8DC")  # Cornsilk background

        # Load jokes from the same directory as script
        self.jokes = self.load_jokes()
        self.current_setup = None
        self.current_punchline = None

        # Title label
        self.title_label = tk.Label(
            master,
            text=" Alexa Joke Assistant ",
            font=("Comic Sans MS", 26, "bold"),
            bg="#FFF8DC",
            fg="#FF6347"  # Tomato color
        )
        self.title_label.pack(pady=(20, 10))

        # Setup text
        self.setup_label = tk.Label(
            master,
            text="",
            font=("Arial", 18, "bold"),
            wraplength=500,
            bg="#FFF8DC",
            fg="#4682B4"  # Steel blue
        )
        self.setup_label.pack(pady=(10, 5))

        # Punchline text
        self.punchline_label = tk.Label(
            master,
            text="",
            font=("Arial", 16, "italic"),
            fg="#32CD32",  # Lime green
            wraplength=500,
            bg="#FFF8DC",
        )
        self.punchline_label.pack(pady=(5, 20))

        # Buttons frame
        btn_frame = tk.Frame(master, bg="#FFF8DC")
        btn_frame.pack(pady=(10, 25))

        button_style = {
            "font": ("Arial", 12, "bold"),
            "bg": "#FFB74D",  # Light orange
            "fg": "black",
            "activebackground": "#FFA726",  # Darker orange
            "activeforeground": "white",
            "relief": "raised",
            "bd": 2,
            "padx": 10,
            "pady": 5
        }

        self.joke_btn = tk.Button(
            btn_frame, text="Tell me a Joke", command=self.show_joke, width=15, **button_style
        )
        self.joke_btn.grid(row=0, column=0, padx=8, pady=5)

        self.punchline_btn = tk.Button(
            btn_frame, text="Show Punchline", command=self.show_punchline, width=15, **button_style
        )
        self.punchline_btn.grid(row=0, column=1, padx=8, pady=5)

        self.next_btn = tk.Button(
            btn_frame, text="Next Joke", command=self.show_joke, width=15, **button_style
        )
        self.next_btn.grid(row=0, column=2, padx=8, pady=5)

        # Quit button
        self.quit_btn = tk.Button(
            master, text="Quit", command=self.master.quit, width=12,
            font=("Arial", 12, "bold"),
            bg="#FF5733",  # Bright red
            fg="white",
            activebackground="#FA0202",  # Darker red
            activeforeground="white",
            relief="raised",
            bd=2,
            padx=10,
            pady=5
        )
        self.quit_btn.pack(pady=(10, 15))

    def load_jokes(self):
        """Load jokes from the randomJokes.txt file."""
        try:
            base_path = os.path.dirname(os.path.abspath(__file__))
            file_path = os.path.join(base_path, "randomJokes.txt")

            with open(file_path, "r", encoding="utf-8") as f:
                jokes = f.read().splitlines()

            return jokes
        except FileNotFoundError:
            messagebox.showerror(
                "Error", "randomJokes.txt not found in the same folder as this script."
            )
            return []

    def show_joke(self):
        """Display a random joke."""
        if not self.jokes:
            return

        joke = random.choice(self.jokes)

        if "?" in joke:
            setup, punchline = joke.split("?", 1)
            self.current_setup = setup.strip() + "?"
            self.current_punchline = punchline.strip()
        else:
            self.current_setup = joke
            self.current_punchline = "(No punchline found)"

        self.setup_label.config(text=self.current_setup)
        self.punchline_label.config(text="")

    def show_punchline(self):
        """Display the punchline of the current joke."""
        if self.current_punchline:
            self.punchline_label.config(text=self.current_punchline)
        else:
            self.punchline_label.config(text="No punchline available.")


if __name__ == "__main__":
    root = tk.Tk()
    app = JokeApp(root)
    root.mainloop()