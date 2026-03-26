# Hangman in Python

Welcome to Hangman! I am sure you are familiar with this game. If not, nothing to worry about!

Here is a short explanation of the rules:

1. To start the game, just run the code. Make sure to be in the right directory, else the code won't be able to find the csv file!
2. After starting, you will see the progress in the terminal.
3. The game is simple:
   1. As initial, you get ten chances. Each chance is a part of the hanging man.
   2. Type a letter in the terminal and press enter. You can guess only one letter per turn.
   3. You are not allowed to type: multiple letters, numbers or any symbols that the alphabet doesn't contain.
   4. If you guess correct, your remaining chances stay untouched.
   5. If you guess wrong, one chance at a time will be removed and a part of the hanging man is drawn into the terminal. If you use all your chances, you lose the game and hang the man.
   6. You win the game by guessing the word correctly letter by letter
   7. Have fun!

## Customization

This game has a source of words. This source is the words.csv which you can find in this directory.
Currently, there are 999 words in this source. You can add or remove words, or even replace them within the file. Just make sure to be consistent of holding only one column; Each line representes a single word.

So, please be careful:
If two words in a line are separated by a space, the second word is included. While this doesn't cause the game to crash, it doesn't produce the desired result.
