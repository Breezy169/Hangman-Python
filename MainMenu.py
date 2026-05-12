import tkinter as tk
from hangman import HangmanLogic
from GameScreen import GameScreen

class MainMenu(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        tk.Label(self, text="Wähle deinen Modus", font=("Arial", 16)).pack(pady=20)

        button_frame = tk.Frame(self)
        button_frame.pack()

        
        self.selected_mode = tk.StringVar(value="singleplayer")  # default
        
        tk.Label(self, text="Number of rounds:", font=("Calibri", 12)).pack(pady=(20,5))
        self.max_rounds_entry = tk.Entry(self, font=("Calibri", 12))
        self.max_rounds_entry.pack(pady=(5,15))
        
        
        tk.Label(self, text="Number of players:", font=("Calibri", 12)).pack()
        self.player_count_entry = tk.Entry(self, font=("Calibri", 12))
        self.player_count_entry.pack(pady=10)
        # Toggle-Funktion
        def toggle_mode(mode):
            self.selected_mode.set(mode)
            # Optisches Feedback
            if mode == "singleplayer":
                btn_single.config(relief="sunken", bg="lightblue")
                btn_multi.config(relief="raised", bg="SystemButtonFace")
                self.player_count_entry.config(state="disabled")
            else:
                btn_multi.config(relief="sunken", bg="lightblue")
                btn_single.config(relief="raised", bg="SystemButtonFace")
                self.player_count_entry.config(state="normal")


        # Button Singleplayer
        btn_single = tk.Button(button_frame, text="Singleplayer",
                               command=lambda: toggle_mode("singleplayer"))
        btn_single.pack(side="left", padx=5)

        # Button Multiplayer
        btn_multi = tk.Button(button_frame, text="Multiplayer",
                              command=lambda: toggle_mode("multiplayer"))
        btn_multi.pack(side="left", padx=5)

        # Start-Button
        tk.Button(button_frame, text="Start",
                  command=lambda: self.start_game_from_menu(self.selected_mode.get())
        ).pack(side="left", padx=5)

        # Initial optisches Feedback
        toggle_mode("singleplayer")


    def start_game_from_menu(self, mode):
        # Input aus Entry lesen
        try:
            

            max_rounds = int(self.max_rounds_entry.get())
            if max_rounds < 1:
                max_rounds = 1
                from tkinter import messagebox
                messagebox.showerror("Adaptive Change", "You entered a number that is less than 1! \n Number of maximum rounds is set as 1.")
        except ValueError:
            import tkinter.messagebox as messagebox
            messagebox.showerror("Invalid input", "Please enter only numbers!")
            return 
        
        #default for singleplayer
        players = None
        if self.player_count_entry.cget("state") != "disabled":
            try:
                player_count = int(self.player_count_entry.get())
                if player_count < 2:
                    player_count = 2
                    from tkinter import messagebox
                    messagebox.showerror("Adaptive Change", "You entered a number that is less than 2! \n Number of maximum rounds is set as 2.")
                players = [f"P{i+1}" for i in range(player_count)]
            except ValueError:
                import tkinter.messagebox as messagebox
                messagebox.showerror("Invalid input", "Please enter only numbers!")
                return 
        
        # Frame wechseln + max_rounds weitergeben
        self.master.switch_frame(GameScreen, mode=mode, max_rounds=max_rounds, players=players)
