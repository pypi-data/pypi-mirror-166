# random-quote.py
from random import randint


def random_quote():
    quotes = ["Don't worry, be happy", "Be yourself; everyone else is already taken.",
              "You only live once, but if you do it right, once is enough.",
              "In three words I can sum up everything I've learned about life: it goes on.",
              "To live is the rarest thing in the world. Most people exist, that is all.",
              "If you want to live a happy life, tie it to a goal, not to people or things.",
              "Not how long, but how well you have lived is the main thing.",
              "In order to write about life first you must live it.",
              "I like criticism. It makes you strong.",
              "Too many of us are not living our dreams because we are living our fears.",
              "Every moment is a fresh beginning.",
              "All life is an experiment. The more experiments you make, the better."]
    random_index = randint(0, len(quotes) - 1)
    return quotes[random_index]


def welcome_user(user_name):
    print(f"Welcome {user_name}, it's good to see you here!")
    print(f"Remember that: {random_quote()}")
