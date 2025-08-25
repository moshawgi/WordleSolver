import sys
import os
from copy import deepcopy

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.join(current_dir, '..')
sys.path.append(parent_dir)

from wordle_secret_words import get_secret_words
from valid_wordle_guesses import get_valid_wordle_guesses

class WordleAI:
    def __init__(self, all_valid_words: list[str], valid_wordle_answers: list[str]):
        self.valid_guesses = all_valid_words
        self.possible_answers = valid_wordle_answers
        self.current_valid = valid_wordle_answers.copy()
        # Add additional data attributes as needed

    def get_feedback(self, guess: str, secret_word: str) -> str:
        '''Generates a feedback string based on comparing a 5-letter guess with the secret word.
            The feedback string uses the following schema:
                - Correct letter, correct spot: uppercase letter ('A'-'Z')
                - Correct letter, wrong spot: lowercase letter ('a'-'z')
                - Letter not in the word: '-'

            Args:
                guess (str): The guessed word
                secret_word (str): The secret word

            Returns:
                str: Feedback string, based on comparing guess with the secret word

            Examples
            >>> AI = WordleAI(get_valid_wordle_guesses(), get_secret_words())
            >>> AI.get_feedback("lever", "EATEN") == "-e-E-"
            True
            >>> AI.get_feedback("LEVER", "LOWER") == "L--ER"
            True
            >>> AI.get_feedback("MOMMY", "MADAM") == "M-m--"
            True
            >>> AI.get_feedback("ARGUE", "MOTTO") == "-----"
            True
            >>> AI.get_feedback("PIECE", "SLATE") == "----E"
            True
            >>> AI.get_feedback("TROUT", "FRUIT") == "-R-uT"
            True
        '''
        if not guess:
            return "-----"
        word = list(secret_word.lower())
        guess = guess.lower()
        result = list("-----")
        for i in range(len(word)):
            if guess[i] == word[i]:
                result[i] = word[i].upper()
                word[i] = 0
        for i in range(len(word)):
            if result[i] != "-":
                continue
            if guess[i] in word:
                result[i] = guess[i]
                word[word.index(guess[i])] = 0
        return "".join(result)

    def is_valid(self, word1, guesses, feedback):
        for j in range(len(feedback)):
            word = list(word1.lower())
            feed = feedback[j]
            for i in range(len(feed)):
                letter = feed[i]
                if letter != "-" and letter.upper() == letter:
                    if word[i].upper() != letter:
                        return False
                    else:
                        word[i] = 0
            for i in range(len(feed)):
                letter = feed[i]
                if letter != "-" and letter.lower() == letter:
                    if letter not in word or word[i] == letter:
                        return False
                    else:
                        word[word.index(letter)] = 0
            for i in range(len(feed)):
                letter = feed[i]
                if letter == "-" and guesses[j][i].lower() in word:
                    return False
        return True

    def guess(self, guesses: list[str], feedback: list[str]) -> str:
        '''Analyzes feedback from previous guesses/feedback (if any) to make a new guess

        Args:
            guesses (list): A list of string guesses, which could be empty
            feedback (list): A list of feedback strings, which could be empty

        Returns:
            str: a valid guess that is exactly 5 uppercase letters
        '''

        if len(guesses) == 0 and len(feedback) == 0:
            self.current_valid = self.possible_answers.copy()
            return "FLAME"
        if len(guesses) == 1 and len(feedback) == 1:
            new_valid = self.current_valid.copy()
            for word1 in new_valid:
                if not self.is_valid(word1, guesses, feedback):
                    self.current_valid.remove(word1)
            return "POUCH"
        if len(guesses) == 2 and len(feedback) == 2:
            new_valid = self.current_valid.copy()
            for word1 in new_valid:
                if not self.is_valid(word1, [guesses[1]], [feedback[1]]):
                    self.current_valid.remove(word1)
            return "TRINS"
        # if len(guesses) == 0:
        #     self.current_valid = self.possible_answers.copy()
        if len(self.current_valid) == len(self.possible_answers):
            new_valid = self.current_valid.copy()
            for word1 in new_valid:
                if not self.is_valid(word1, guesses, feedback):
                    self.current_valid.remove(word1)
        else:
            new_valid = self.current_valid.copy()
            for word1 in new_valid:
                if not self.is_valid(word1, [guesses[len(guesses) - 1]], [feedback[len(feedback) - 1]]):
                    self.current_valid.remove(word1)
        if len(self.current_valid) > 3:
            in_common = set("abcdefghijklmnopqrstuvwxyz".upper())
            for word in self.current_valid:
                in_common = in_common.intersection(set(word))
            not_in_common = set()
            for word in self.current_valid:
                not_in_common.update(set(word) - in_common)
            best_word = ""
            longest_set = 0
            gray_letters = set()
            for j in range(len(feedback)):
                for i in range(len(feedback[j])):
                    if feedback[j][i] == "-":
                        gray_letters.add(guesses[j][i])
            for word1 in self.possible_answers:
                if len(set(word1).intersection(not_in_common)) > longest_set: #.intersection(set("abcdefghijklmnopqrstuvwxyz") - gray_letters)
                    longest_set = len(set(word1).intersection(not_in_common))
                    best_word = word1
            return best_word
        return list(self.current_valid)[0]

if __name__ == "__main__":
    AI = WordleAI(get_valid_wordle_guesses(), get_secret_words())
    print(AI.get_feedback("LEVER", "LOWER")) #"L--ER"
    guesses = ["CRANE", "CATER"]
    feedback = ["cra-e", "cater"]
    print(AI.guess(guesses, feedback)) #REACT
