import random
from colorama import Fore, Back, Style, init
init(autoreset=True) #Ends color formatting after each print statement
import sys
import os
import random

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.join(current_dir, '..')
sys.path.append(parent_dir)

try:
    from WordleAI import WordleAI as WordleAI
except ModuleNotFoundError:
    print("WordleAI.py is not found.")

from wordle_secret_words import get_secret_words
from valid_wordle_guesses import get_valid_wordle_guesses

class Wordle:
    def __init__(self, all_valid_words: list[str], valid_wordle_answers: list[str]):
        self.valid_guesses = set(all_valid_words)
        self.AI = WordleAI(all_valid_words, valid_wordle_answers)
        self.feedback = []
        self.guesses = []
        self.secret_word = random.choice(list(valid_wordle_answers))
        self.get_player_input()

    def get_player_input(self):
        guess = input("Enter guess: ").upper()
        while not guess in self.valid_guesses:
            if guess.lower() == "h":
                print(self.AI.guess(self.guesses, self.feedback))
            guess = input("Enter guess: ").upper()
        self.guesses.append(guess)
        self.feedback.append(self.AI.get_feedback(guess, self.secret_word))
        self.print_board()
        if guess == self.secret_word:
            self.end_game(True)
        elif len(self.guesses) >= 6:
            self.end_game(False)
        else:
            self.get_player_input()

    def print_board(self):
        print()
        for i in range(len(self.feedback)):
            colors = []
            for letter in self.feedback[i]:
                if letter == "-":
                    colors.append(Back.LIGHTBLACK_EX)
                elif letter == letter.lower():
                    colors.append(Back.YELLOW)
                else:
                    colors.append(Back.GREEN)
            guess = self.guesses[i]
            print(colors[0] + guess[0] + colors[1] + guess[1] + colors[2] + guess[2] + colors[3] + guess[3] + colors[4] + guess[4])
        print()

    def end_game(self, won):
        if won:
            print("You won!")
        else:
            print("You lost. The word was", self.secret_word)


if __name__ == "__main__":
    Game = Wordle(get_valid_wordle_guesses(), get_secret_words())
