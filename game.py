from cards import create_deck, shuffle_deck
from player import Player
from expert_system import GoFishExpertSystem


class GoFishGame:
    def __init__(self):
        self.reset()

    def reset(self):
        self.deck = create_deck()
        shuffle_deck(self.deck)

        self.human = Player("Player")
        self.ai = Player("Expert AI")
        self.expert = GoFishExpertSystem()

        self.message = ""
        self.ai_explanation = ""

        self.turn = "human"
        self.game_over = False
        self.winner = None

        self.last_draw = None
        self.last_ai_rank = None

        # Deal 7 cards to each player.
        self.deal_cards(7)

        self.check_all_books()

        self.message = "Your turn — click a card to choose a rank."

    def deal_cards(self, amount):
        for _ in range(amount):
            if self.deck:
                self.human.add_cards([self.deck.pop()])

            if self.deck:
                self.ai.add_cards([self.deck.pop()])

    def draw_card(self, player):
        if not self.deck:
            return None

        card = self.deck.pop()
        player.add_cards([card])
        return card

    def request_rank(self, rank):
        if self.game_over:
            return

        if self.turn != "human":
            return

        if rank not in self.human.legal_ranks():
            self.message = "You can only ask for a rank you currently have."
            return

        self.message = f'You asked: "Do you have any {rank}s?"'

        cards = self.ai.remove_cards_of_rank(rank)

        # AI HAS the requested rank.
        if cards:
            self.human.add_cards(cards)

            self.message = (
                f'AI gave you {len(cards)} {rank}'
                f'{"s" if len(cards) != 1 else ""}! '
                f"You get another turn."
            )

            self.check_all_books()

            if not self.game_over:
                self.turn = "human"

            return

        # AI DOES NOT have the requested rank.
        self.expert.record_human_request(rank)

        self.message = f'AI says: "Go Fish!"'

        drawn = self.draw_card(self.human)

        if drawn:
            self.last_draw = drawn

            if drawn.rank == rank:
                self.message = (
                    f"Go Fish! You drew a {drawn.rank}. "
                    f"You get another turn!"
                )

                self.check_all_books()

                if not self.game_over:
                    self.turn = "human"

                return

            self.message = (
                f"Go Fish! You drew "
                f"{drawn.rank} of {drawn.suit}. "
                f"Your turn ends."
            )

        else:
            self.message = "Go Fish! The deck is empty."

        self.check_all_books()

        if not self.game_over:
            self.turn = "ai"
            self.ai_turn()

    def ai_turn(self):
        if self.game_over:
            return

        legal = self.ai.legal_ranks()

        if not legal:
            self.turn = "human"
            self.check_game_over()
            return

        decision = self.expert.choose_rank(
            self.ai.hand,
            legal
        )

        rank = decision["rank"]
        self.last_ai_rank = rank

        self.ai_explanation = (
            f"Rule fired: {', '.join(decision['reasons'])}. "
            f"Priority = {decision['score']}."
        )

        cards = self.human.remove_cards_of_rank(rank)

        # HUMAN HAS THE REQUESTED RANK.
        if cards:
            self.ai.add_cards(cards)

            self.expert.record_ai_observation(
                f"AI requested {rank} and received "
                f"{len(cards)} card(s)."
            )

            self.message = (
                f'AI asked: "Do you have any {rank}s?" '
                f"You gave the AI {len(cards)} card(s)."
            )

            self.check_all_books()

            if not self.game_over:
                # Successful request = AI continues.
                self.turn = "ai"
                self.ai_turn()

            return

        # HUMAN DOES NOT HAVE THE RANK.
        self.expert.record_ai_observation(
            f"AI requested {rank} and had to Go Fish."
        )

        drawn = self.draw_card(self.ai)

        if drawn:
            self.last_draw = drawn

            if drawn.rank == rank:
                self.message = (
                    f'AI asked for {rank}s, got none, '
                    f'and drew the requested rank. AI goes again.'
                )

                self.check_all_books()

                if not self.game_over:
                    self.turn = "ai"
                    self.ai_turn()

                return

            self.message = (
                f'AI asked for {rank}s, got none, '
                f'and went fishing. Your turn.'
            )

        else:
            self.message = (
                f'AI asked for {rank}s, but the deck is empty. '
                f"Your turn."
            )

        self.check_all_books()

        if not self.game_over:
            self.turn = "human"

    def check_all_books(self):
        human_books = self.human.check_books()
        ai_books = self.ai.check_books()

        if human_books:
            self.message += (
                f" You completed: {', '.join(human_books)}!"
            )

        if ai_books:
            self.message += (
                f" AI completed: {', '.join(ai_books)}!"
            )

        self.check_game_over()

    def check_game_over(self):
        # If both hands are empty and there is nothing left to draw.
        if (
            not self.deck
            and not self.human.hand
            and not self.ai.hand
        ):
            self.finish_game()
            return

        # If a player has no cards but cards remain,
        # give them one card so the game can continue.
        if not self.human.hand and self.deck:
            self.draw_card(self.human)

        if not self.ai.hand and self.deck:
            self.draw_card(self.ai)

        # If there are no cards left and somebody has no hand,
        # the game is over.
        if (
            not self.deck
            and (
                not self.human.hand
                or not self.ai.hand
            )
        ):
            self.finish_game()

    def finish_game(self):
        self.game_over = True

        human_score = len(self.human.books)
        ai_score = len(self.ai.books)

        if human_score > ai_score:
            self.winner = "Player"
        elif ai_score > human_score:
            self.winner = "Expert AI"
        else:
            self.winner = "Draw"

        if self.winner == "Draw":
            self.message = "Game over — it's a draw!"
        else:
            self.message = (
                f"Game over — {self.winner} wins!"
            )

    def available_human_ranks(self):
        return self.human.legal_ranks()