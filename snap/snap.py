import sys
from abc import ABC, abstractmethod
from enum import Enum, auto
import random

CARDS_IN_PACK = 52


class Suite(Enum):
    SPADES = auto()
    CLUBS = auto()
    HEARTS = auto()
    DIAMONDS = auto()


class Value(Enum):
    ONE = auto()
    TWO = auto()
    THREE = auto()
    FOUR = auto()
    FIVE = auto()
    SIX = auto()
    SEVEN = auto()
    EIGHT = auto()
    NINE = auto()
    TEN = auto()
    JACK = auto()
    QUEEN = auto()
    KING = auto()


class Card:
    def __init__(self, suite, value):
        self.suite = suite
        self.value = value

    def __eq__(self, other):
        return self.suite == other.suite and self.value == other.value

    def __hash__(self):
        return hash((self.suite, self.value))


class Deck:
    def __init__(self, num_packs_):
        self.cards = num_packs_ * CARDS_IN_PACK * [None]
        inx = 0
        for i in range(num_packs_):
            for card_val in Value:
                for suite in Suite:
                    inx += 1
                    self.cards[i * CARDS_IN_PACK + ((card_val.value - 1) * len(Suite)) + suite.value - 1] \
                        = Card(suite, card_val)

    def shuffle(self):
        random.shuffle(self.cards)

    def __iter__(self):
        def deck_iterator(deck_):
            for card in deck_.cards:
                yield card

        return deck_iterator(self)


class MatchFunction(Enum):
    SUITE = auto()
    VALUE = auto()
    EXACT = auto()


class Matcher(ABC):
    @abstractmethod
    def match(self, card_a, card_b):
        pass


class ExactMatcher(Matcher):
    def match(self, card_a, card_b):
        return card_a == card_b


class SuiteMatcher(Matcher):
    def match(self, card_a, card_b):
        return card_a.suite == card_b.suite


class ValueMatcher(Matcher):
    def match(self, card_a, card_b):
        return card_a.value == card_b.value


def play_cards(deck_, matcher_):
    player_scores = [0, 0]
    curr_card = None
    cards_in_play = 0
    for card in deck_:
        cards_in_play += 1
        if not curr_card:
            # First iteration, or starting a new round
            curr_card = card
            continue

        if matcher_.match(curr_card, card):
            player_scores[random.randint(0, 1)] += cards_in_play
            cards_in_play = 0
            curr_card = None
        else:
            curr_card = card

    return player_scores


def get_user_setup():
    try:
        input_str = input("How many packs? (1) > ")
        if input_str:
            num_packs = int(input_str)
        else:
            num_packs = 1
        input_str = input("How would you like to match cards: exact, suite or value? (suite) > ").upper()

        if not input_str:
            input_str = "SUITE"
        match_function = MatchFunction[input_str]

        return num_packs, match_function

    except (KeyError, ValueError) as e:
        print("Specify an integer for the number of packs, and one of \"exact\", \"suite\" or \"value\" for matching.",
              file=sys.stderr)
        print(e)
        raise SystemExit()


if __name__ == "__main__":
    num_packs, match_function = get_user_setup()

    matcher = {
        MatchFunction.SUITE: SuiteMatcher,
        MatchFunction.VALUE: ValueMatcher,
        MatchFunction.EXACT: ExactMatcher
    }[match_function]()
    deck = Deck(num_packs)
    deck.shuffle()

    score1, score2 = play_cards(deck, matcher)
    if score1 == score2:
        print(f"It was a draw, with both players scoring {score1}.")
    elif score1 > score2:
        print(f"Player 1 won with a score of {score1} to {score2}")
    else:
        print(f"Player 2 won with a score of {score2} to {score1}")
