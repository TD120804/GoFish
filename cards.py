import random


SUITS = [
    "Hearts",
    "Diamonds",
    "Clubs",
    "Spades"
]


SUIT_SYMBOLS = {
    "Hearts": "♥",
    "Diamonds": "♦",
    "Clubs": "♣",
    "Spades": "♠"
}


RANKS = [
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    "10",
    "J",
    "Q",
    "K",
    "A"
]


RANK_VALUES = {
    rank: i
    for i, rank in enumerate(RANKS)
}


class Card:

    def __init__(
        self,
        rank,
        suit
    ):
        self.rank = rank
        self.suit = suit

    def __repr__(self):
        return (
            f"{self.rank} of {self.suit}"
        )

    def short_name(self):

        return (
            f"{self.rank}"
            f"{SUIT_SYMBOLS[self.suit]}"
        )


def create_deck():

    return [
        Card(rank, suit)
        for suit in SUITS
        for rank in RANKS
    ]


def shuffle_deck(deck):

    random.shuffle(deck)