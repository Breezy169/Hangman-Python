import random
from collections import Counter

class HangmanLogic:

    def __init__(self, mode="singleplayer", players=None, round_count= 0, max_rounds = 0, teams_enabled=False):
        self.word_pool = self._load_words()
        self.word = self._get_random_word().lower()
        self.mode = mode      
        self.letterCorrectGuessed = set()
        self.letterFalseGuessed = set()
        self.stages = 10
        self.game_over = False
        self.game_win = False
        self.hangman_stages = [
            """
            ========
            """,
            """
            |
            |
            |
            |
            ========
            """,
            """
            +---+
            |
            |
            |
            |
            ========
            """,
            """
            +---+
            |   |
            |
            |
            |
            ========
            """,
            """
            +---+
            |   |
            |   O
            |
            |
            ========
            """,
            """
            +---+
            |   |
            |   O
            |   |
            |
            ========
            """,
            """
            +---+
            |   |
            |   O
            |  /|
            |
            ========
            """,
            """
            +---+
            |   |
            |   O
            |  /|\\
            |
            ========
            """,
            """
            +---+
            |   |
            |   O
            |  /|\\
            |  /
            ========
            """,
            """
            +---+
            |   |
            |   O
            |  /|\\
            |  / \\
            ========
            """
        ]

        if mode == "multiplayer":
            if players is None:
                players = ["Player 1", "Player 2"]
            self.players = players
            self.teams_enabled = teams_enabled  
            self.round_count = round_count
            self.current_player_index = 0
            self.max_rounds = max_rounds
            self.player_points = {}
            self.player_guesses = {}
            for player in players:
                self.player_points[player] = 0
            for player in players:
                self.player_guesses[player] = set()

    def _load_words(self):
        try:
            with open("words.csv", "r", encoding="utf-8") as file:
                # split words when encountering commas or new lines
                content = file.read().replace(',', '\n')
                words = [w.strip().upper() for w in content.splitlines() if w.strip()]
                return words if words else ["PYTHON", "TERMINAL", "GUESS"]
        except FileNotFoundError:
            return ["PYTHON", "TERMINAL", "GUESS"]

    def _get_random_word(self):
        if not self.word_pool:
            self.word_pool = self._load_words() # Pool neu füllen wenn leer
        word = random.choice(self.word_pool)
        self.word_pool.remove(word)
        return word
    
    # This function resets variables and is only needed for multiplayer mode
    def reset_round(self, next_word):
        self.word = next_word.lower()
        self.letterCorrectGuessed = set()
        self.letterFalseGuessed = set()
        self.stages = 10
        self.game_over = False
        self.game_win = False

    @property
    def current_player(self):
        return self.players[self.current_player_index]
    
    def next_turn(self):
        self.current_player_index = (self.current_player_index + 1) % len(self.players)
        # processing round counts

            
    def process_turn(self, guessed_letter):
        correct_guess = self.check_guess(guessed_letter)
        # turn passed on to the next player upon guessing wrong letter
        if not correct_guess:
            self.next_turn()   
        return correct_guess
    
    def get_status(self):
        return {
            "word": self.display_word(),
            "lives": self.stages,
            "game_over": self.game_over,
            "won": self.game_win
        }
    
    def player_info(self):
        player_guessed = list(self.player_guesses[self.current_player])
        correct_guess = 0
        correct_guesses = ""
        false_guess = 0
        false_guesses = ""
        for letter in player_guessed:
            if letter in self.letterCorrectGuessed:
                correct_guess += 1
                correct_guesses += letter
            else:
                false_guess += 1
                false_guesses += letter
        return {
            "Player": self.current_player,
            "Letter Guessed": f"{len(player_guessed)} -  {player_guessed}",
            "Correct Guesses": f"{correct_guess} - {correct_guesses}",
            "False Guesses": f"{false_guess} - {false_guesses}",
            "Points": self.player_points[self.current_player]
        }
    
    def get_hangman(self):
        return self.hangman_stages[min(9, 10-self.stages)]
    
    def check_guess(self, guessed_letter):
        guessed_letter = guessed_letter.lower()

        # 3 validations of the input
        if not guessed_letter.isalpha():
            raise ValueError("You must guess a letter!")

        if len(guessed_letter) > 1:
            raise Exception("You can guess only one letter per turn!")

        if guessed_letter in self.letterCorrectGuessed:
            raise Exception("You already guessed this letter!")
        
        # make guessed letter to lower and sort it as either correct guessed or false guessed + check if win conditions are met
        if guessed_letter in self.word:
            self.letterCorrectGuessed.add(guessed_letter)
            self.player_guesses[self.current_player] += guessed_letter
            if self.mode == "multiplayer":
                self.player_points[self.current_player] += 1
            if all(c in self.letterCorrectGuessed for c in self.word):
                self.win()
            return True
        else:
            self.letterFalseGuessed.add(guessed_letter)
            self.stages -= 1
            if self.stages <= 0: 
                self.lose()
            return False

    def display_word(self):
        return " ".join([c if c in self.letterCorrectGuessed else "_" for c in self.word])

    def win(self):
        self.game_over = True
        self.game_win = True
        self.round_count += 1
        # multiplayer point calculation
        if self.mode == "multiplayer":
            self.player_points[self.current_player]  += self.stages
        
    def lose(self):
        self.game_over = True
        self.game_win = False
        return True if self.stages <= 0 else False