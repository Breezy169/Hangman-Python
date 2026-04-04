import tkinter as tk
from hangman import HangmanLogic

class GameScreen(tk.Frame):
    def __init__(self, master, mode, max_rounds, players):
        super().__init__(master)

        self.mode = mode
        self.max_rounds = max_rounds
        self.players = players
        self.initial_hangman_state = ""

        # Hangman-Instance
        if mode == "multiplayer":
            self.game = HangmanLogic(mode="multiplayer", players=players, max_rounds=max_rounds)
        else:
            self.game = HangmanLogic(mode="singleplayer", players=None, max_rounds=max_rounds)

       
        self.hangman_state = self.initial_hangman_state if len(self.game.letterFalseGuessed) == 0 else self.game.get_hangman()
        self.game_info = self.game.get_status()
        state_text = "\n".join([f"{key}: {value}" for key, value in self.game_info.items()]) 
        self.word = self.game.display_word()
        

        # Grid Prep: 2x2
        self.columnconfigure((0,1), weight=1)
        self.rowconfigure((0,1), weight=1)

        # 4 Frames Grid
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

            # Assuming that `self.game.players` is the list of players
            players = self.game.players
            
            # All attributes to be displayed (rows)
            attributes = ["Player", "Letter Guessed", "Correct Guesses", "False Guesses", "Points"]
            
            # Dynamic label generation
            for row_index, attr in enumerate(attributes):
                for col_index, player in enumerate(players):
                    # Retrieve player information
                    if self.game.mode == "singleplayer":
                        info = self.game.player_info()  # returns a dictionary
                    else:
                        # Multiplayer: Player-specific information
                        guessed_letters = list(self.game.player_guesses[player])
                        correct_guess = sum(1 for l in guessed_letters if l in self.game.letterCorrectGuessed)
                        false_guess = len(guessed_letters) - correct_guess
                        info = {
                            "Player": player,
                            "Letter Guessed": f"{len(guessed_letters)} - {guessed_letters}",
                            "Correct Guesses": f"{correct_guess} - {''.join([l for l in guessed_letters if l in self.game.letterCorrectGuessed])}",
                            "False Guesses": f"{false_guess}",
                            "Points": self.game.player_points[player]
                        }
            
                    tk.Label(self.frame_br, text=info[attr], font=("Arial", 12), borderwidth=1, relief="solid", padx=5, pady=5)\
                      .grid(row=row_index, column=col_index, sticky="nsew")
            
            # Position columns equally 
            for col_index in range(len(players)):
                self.frame_br.columnconfigure(col_index, weight=1)
        else: 
            tk.Label(self.frame_br, text=state_text, bg="#d0d0d0").pack(pady=60)
            tk.Label(self.frame_bl, text="Your turn!", font=("Courier", 14), bg="#e0e0e0").pack(pady=5)
     
        tk.Label(self.frame_tl, text="Guess the word:", font=("Arial", 20), bg="#f0f0f0").pack(pady=60)
        tk.Label(self.frame_tl, text=self.word, font=("Arial", 20)).pack(pady=30)
        
        tk.Label(self.frame_tr, text=self.hangman_state,  bg="#f9f9f9", font=("Courier", 14)).pack(pady=120)
        
        tk.Label(self.frame_bl, text="Guess a letter:", font=("Courier", 14), bg="#e0e0e0").pack()
        tk.Entry(self.frame_bl).pack(pady=60)

        # Mode + Round info
        tk.Label(self.frame_tl, text=f"Mode: {mode} \n Max Rounds: {max_rounds}").pack(pady=10)

