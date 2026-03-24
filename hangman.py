import random
from collections import Counter

with open('words.csv', "r", encoding="utf-8") as csvfile:
    words = csvfile.read()

words = f"""{words}"""
words = words.split()
word = random.choice(words)

hangman = [
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

if __name__ == '__main__':
    print("Welcome to Hangman Python!")
    print("Guess the word!")

    for _ in word:
        print("_", end=" ")
    print()

    letterCorrectGuessed = ''
    letterFalseGuessed = ''
    chances = len(hangman)
    flag = 0
    stage = 0
    try:
        while chances > 0 and flag == 0:
            print()
            chances -= 1
            try:
                guess = input('Enter a letter: ').lower()
            except:
                print("You must enter letters!")
                continue

            if not guess.isalpha():
                print("You must enter only letters!")
                continue
            elif len(guess) > 1:
                print("You must enter only one letter at a time!")
                continue
            elif guess in letterCorrectGuessed:
                print("You already guessed this letter!")
                continue

            if guess not in word:
                letterFalseGuessed += guess
                print(hangman[stage])
                stage += 1
                print("The letter", guess, "is not included in the word! Try again.")
            else:
                chances += 1
                letterCorrectGuessed += guess * word.count(guess)
            
            for char in word:
                if char in letterCorrectGuessed:
                    print(char, end=' ')
                   
                else:
                    print('_', end=' ')

                
            print("\n Remaining chances: ", chances)

            if Counter(letterCorrectGuessed) == Counter(word):
                print("\nCongratulations! You guessed the word!:", word)
                flag = 1
                break

        if chances <= 0  and Counter(letterCorrectGuessed) != Counter(word):
            print("You've run out of chances.")
            print("You lost. The word was:", word)

    except:
        print("\nThe game was interrupted.")
        exit()