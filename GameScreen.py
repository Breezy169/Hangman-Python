import tkinter as tk
from tkinter import messagebox
from hangman import HangmanLogic

class GameScreen(tk.Frame):
    def __init__(self, master, mode, max_rounds, players):
        super().__init__(master)

        self.mode = mode
        self.max_rounds = max_rounds
        self.players = players
        self.initial_hangman_state = ""

        if mode == "multiplayer":
            self.game = HangmanLogic(mode="multiplayer", players=players, max_rounds=max_rounds)
        else:
            self.game = HangmanLogic(mode="singleplayer", players=None, max_rounds=max_rounds)

        self.hangman_state = self.initial_hangman_state if len(self.game.letterFalseGuessed) == 0 else self.game.get_hangman()
        self.game_info = self.game.get_status()
        state_text = "\n".join([f"{key}: {value}" for key, value in self.game_info.items()])
        self.word = self.game.display_word()

        self.columnconfigure((0, 1), weight=1)
        self.rowconfigure((0, 1), weight=1)

        self.frame_tl = tk.Frame(self, bg="#f0f0f0", bd=2, relief="groove")
        self.frame_tr = tk.Frame(self, bg="#f9f9f9", bd=2, relief="groove")
        self.frame_bl = tk.Frame(self, bg="#e0e0e0", bd=2, relief="groove")
        self.frame_br = tk.Frame(self, bg="#d0d0d0", bd=2, relief="groove")

        self.frame_tl.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.frame_tr.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        self.frame_bl.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        self.frame_br.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)

        if self.mode == "multiplayer":
            tk.Label(self.frame_bl, text=f"{self.game.current_player}'s turn!", font=("Courier", 14), bg="#e0e0e0").pack(pady=5)
        else:
            tk.Label(self.frame_br, text=state_text, bg="#d0d0d0").pack(pady=60)
            tk.Label(self.frame_bl, text="Your turn!", font=("Courier", 14), bg="#e0e0e0").pack(pady=5)

        tk.Label(self.frame_tl, text="Guess the word:", font=("Arial", 20), bg="#f0f0f0").pack(pady=10)
        self.word_label = tk.Label(self.frame_tl, text=self.word, font=("Arial", 20))
        self.word_label.pack(pady=10)

        tk.Label(self.frame_bl, text="Guess a letter:", font=("Courier", 14), bg="#e0e0e0").pack()

        self.guess_entry = tk.Entry(self.frame_bl)
        self.guess_entry.pack(pady=20)
        self.guess_entry.focus_set()
        self.guess_entry.bind("<Return>", self.on_enter_pressed)

        self.hangman_label = tk.Label(
            self.frame_tr,
            text=self.hangman_state,
            bg="#f9f9f9",
            font=("Courier", 14)
        )
        self.hangman_label.pack(pady=10)
        tk.Label(self.frame_tl, text=f"Mode: {mode} \n Max Rounds: {max_rounds}").pack(pady=10)

    def on_enter_pressed(self, event=None):
        guessed_letter = self.guess_entry.get().strip()

        try:
            correct = self.game.check_guess(guessed_letter)
            if self.game.game_over:
                self.word_label.config(text=self.game.word.upper())
            else:
                self.word_label.config(text=self.game.display_word())
            
            self.hangman_label.config(text=self.game.get_hangman())

            if not correct:
                messagebox.showinfo("Wrong guess", "Wrong guess!")

        except Exception as e:
            messagebox.showerror("Error", str(e))

        finally:
            self.guess_entry.delete(0, tk.END)