

import tkinter as tk
from hangman import HangmanLogic
from tkinter import messagebox
from MainMenu import MainMenu

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("1000x600")

        self.current_frame = None
        self.switch_frame(MainMenu)

    def switch_frame(self, frame_class, **kwargs):
        if self.current_frame:
            self.current_frame.destroy()

        self.current_frame = frame_class(self, **kwargs)
        self.current_frame.pack(expand=True, fill="both")


if __name__ == "__main__":
    app = App()
    app.mainloop()