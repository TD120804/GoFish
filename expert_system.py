from collections import Counter

class GoFishExpertSystem:
    """
    Rule-based expert system for the AI player.

    Knowledge base:
      - AI's current hand
      - ranks previously requested by the human
      - ranks the AI has evidence the human may hold
      - observed cards collected during play

    Inference:
      Explicit rules assign a priority score to every legal rank.
      The highest-priority rank becomes the AI's question.
    """

    def __init__(self):
        self.human_request_history = []
        self.known_human_ranks = set()
        self.observed_human_cards = []
        self.turn_log = []

    def record_human_request(self, rank):
        self.human_request_history.append(rank)

    def record_human_cards_received(self, cards):
        self.observed_human_cards.extend(cards)
        for card in cards:
            self.known_human_ranks.add(card.rank)

    def record_ai_observation(self, message):
        self.turn_log.append(message)

    def choose_rank(self, ai_hand, legal_ranks):
        if not legal_ranks:
            return None

        counts = Counter(card.rank for card in ai_hand)
        scores = {rank: 0 for rank in legal_ranks}
        reasons = {rank: [] for rank in legal_ranks}

        # RULE 1:
        # If AI has 3 cards of a rank, prioritize completing the book.
        for rank in legal_ranks:
            if counts[rank] == 3:
                scores[rank] += 100
                reasons[rank].append("3-card completion")

        # RULE 2:
        # If AI has 2 cards of a rank, prioritize it.
        for rank in legal_ranks:
            if counts[rank] == 2:
                scores[rank] += 50
                reasons[rank].append("pair")

        # RULE 3:
        # If human previously asked for a rank, infer that the human
        # may have interest in / possession of that rank.
        for rank in legal_ranks:
            if rank in self.human_request_history:
                scores[rank] += 25
                reasons[rank].append("human previously requested")

        # RULE 4:
        # If direct evidence says the human holds a rank, strongly prefer it.
        for rank in legal_ranks:
            if rank in self.known_human_ranks:
                scores[rank] += 80
                reasons[rank].append("known human rank")

        # RULE 5:
        # Slightly prefer ranks with more AI cards.
        for rank in legal_ranks:
            scores[rank] += counts[rank] * 5

        # Deterministic tie-break: highest score, then rank order.
        chosen = max(
            legal_ranks,
            key=lambda r: (scores[r], r)
        )

        explanation = reasons[chosen] or ["fallback legal choice"]

        return {
            "rank": chosen,
            "score": scores[chosen],
            "reasons": explanation,
            "all_scores": scores
        }
