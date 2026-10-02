class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []
        self.books = []

    def add_cards(self, cards):
        self.hand.extend(cards)

    def remove_cards_of_rank(self, rank):
        matching = [card for card in self.hand if card.rank == rank]
        self.hand = [card for card in self.hand if card.rank != rank]
        return matching

    def legal_ranks(self):
        return sorted(set(card.rank for card in self.hand))

    def check_books(self):
        counts = {}
        for card in self.hand:
            counts[card.rank] = counts.get(card.rank, 0) + 1

        completed = []
        for rank, count in counts.items():
            if count == 4:
                self.hand = [c for c in self.hand if c.rank != rank]
                self.books.append(rank)
                completed.append(rank)

        return completed
