from random import choice
from quotes_scraper import *


class QuotesGame:
    """
    This class implements a Guessing Game.
    We use "quotes_scraper" to scrape quotes from
    "quotes.toscrape.com" and use them for the game.
    The user have 4 attempts to guess who said the given
    quote. For every wrong guess, a hint will be given.
    """

    def __init__(self, quotes_file):
        """
        Constructor
        """
        self.quotes = read_quotes(quotes_file)  # list of all quotes
        self.quote = None  # current quote
        self.hint = None  # hint for current quote
        self.play = True  # running game flag
        self.start_game()

    def _get_quote(self):
        return self.quote['text']

    def start_game(self):
        while self.play:
            self.quote = choice(self.quotes)
            self.hint = get_author_details(self.quote['bio-link'])
            remaining_guesses = 4
            print(f"Here's a quote: \n\n{self._get_quote()}")
            while remaining_guesses:
                guess = input(
                    f"Who said this? Guesses remaining: {remaining_guesses}. ")
                if self.check_guess(guess):
                    self.finish_game(True)
                    break
                else:
                    remaining_guesses -= 1
                    if remaining_guesses:
                        print(self.get_hint(remaining_guesses))
                    else:
                        self.finish_game(False)

    def finish_game(self, correct):
        if not correct:
            message = f"Sorry, you ran out of guesses. The answer was {self.quote['author']}.\n"
        else:
            message = "Correct.\n"
        print(message)
        self.play = self.play_again()

    def check_guess(self, guess):
        return guess.lower() == self.quote['author'].lower()

    def get_hint(self, guess):
        if guess == 3:
            return f"Here's a hint: {self.hint} \n"
        elif guess == 2:
            return f"Here's another hint: The author's first name starts with '{self.quote['author'][0]}' \n"
        elif guess == 1:
            last_initial = self.quote['author'].split(" ")[1][0]
            return f"Here's another hint: The author's last name starts with '{last_initial}' \n"

    def play_again(self):
        while True:
            self.play = input("Would you like to play again (y/n)? ").lower()
            if self.play == 'n' or self.play == 'y':
                if self.play == 'n':
                    print("\nFarewell.")
                    return False
                print()
                return True
