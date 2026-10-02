import pygame

from cards import SUIT_SYMBOLS


# ============================================================
# COLORS
# ============================================================

BG = (15, 17, 32)
PANEL = (27, 30, 52)
PANEL_LIGHT = (36, 40, 66)

CARD = (248, 246, 239)
CARD_BORDER = (210, 208, 200)

TEXT = (240, 240, 246)
MUTED = (165, 170, 190)

ACCENT = (145, 105, 245)
ACCENT_HOVER = (170, 135, 255)

GREEN = (85, 200, 130)
RED = (215, 75, 90)
GOLD = (235, 190, 75)

DARK_CARD = (42, 48, 85)
DARK_CARD_BORDER = (75, 82, 125)


SUIT_COLORS = {
    "Hearts": RED,
    "Diamonds": RED,
    "Clubs": (30, 30, 35),
    "Spades": (30, 30, 35),
}


class GoFishUI:

    def __init__(self, screen, game):

        self.screen = screen
        self.game = game

        self.show_help = False

        self.selected_card = None

        self.card_rects = []

        self.title_font = pygame.font.SysFont(
            "arial",
            34,
            bold=True
        )

        self.heading_font = pygame.font.SysFont(
            "arial",
            24,
            bold=True
        )

        self.body_font = pygame.font.SysFont(
            "arial",
            18
        )

        self.small_font = pygame.font.SysFont(
            "arial",
            14
        )

        self.card_rank_font = pygame.font.SysFont(
            "arial",
            22,
            bold=True
        )

        self.card_suit_font = pygame.font.SysFont(
            "arial",
            32,
            bold=True
        )

        self.button_font = pygame.font.SysFont(
            "arial",
            16,
            bold=True
        )

        self.restart_rect = pygame.Rect(
            925,
            22,
            145,
            40
        )

        self.help_rect = pygame.Rect(
            760,
            22,
            145,
            40
        )

    # ========================================================
    # TEXT
    # ========================================================

    def text(
        self,
        value,
        font,
        color,
        pos,
        center=False
    ):

        surface = font.render(
            str(value),
            True,
            color
        )

        rect = surface.get_rect()

        if center:
            rect.center = pos
        else:
            rect.topleft = pos

        self.screen.blit(surface, rect)

    # ========================================================
    # BUTTON
    # ========================================================

    def button(
        self,
        rect,
        label,
        enabled=True
    ):

        mouse_pos = pygame.mouse.get_pos()

        if not enabled:
            color = (65, 67, 85)

        elif rect.collidepoint(mouse_pos):
            color = ACCENT_HOVER

        else:
            color = ACCENT

        pygame.draw.rect(
            self.screen,
            color,
            rect,
            border_radius=8
        )

        self.text(
            label,
            self.button_font,
            TEXT,
            rect.center,
            True
        )

    # ========================================================
    # CARD
    # ========================================================

    def draw_card(
        self,
        card,
        x,
        y,
        width=82,
        height=112,
        selected=False
    ):

        rect = pygame.Rect(
            x,
            y,
            width,
            height
        )

        # Selection highlight
        if selected:
            pygame.draw.rect(
                self.screen,
                GOLD,
                (
                    x - 4,
                    y - 4,
                    width + 8,
                    height + 8
                ),
                border_radius=12
            )

        # Card body
        pygame.draw.rect(
            self.screen,
            CARD,
            rect,
            border_radius=9
        )

        pygame.draw.rect(
            self.screen,
            CARD_BORDER,
            rect,
            2,
            border_radius=9
        )

        color = SUIT_COLORS[card.suit]
        symbol = SUIT_SYMBOLS[card.suit]

        # Top-left rank
        self.text(
            card.rank,
            self.card_rank_font,
            color,
            (x + 8, y + 6)
        )

        self.text(
            symbol,
            self.card_suit_font,
            color,
            (
                x + width // 2,
                y + height // 2
            ),
            True
        )

        # Bottom-right small rank/suit
        bottom_text = f"{card.rank}{symbol}"

        self.text(
            bottom_text,
            self.small_font,
            color,
            (
                x + width - 8,
                y + height - 20
            )
        )

        return rect

    # ========================================================
    # CARD BACK
    # ========================================================

    def draw_card_back(
        self,
        x,
        y,
        width=62,
        height=88
    ):

        rect = pygame.Rect(
            x,
            y,
            width,
            height
        )

        pygame.draw.rect(
            self.screen,
            DARK_CARD,
            rect,
            border_radius=8
        )

        pygame.draw.rect(
            self.screen,
            DARK_CARD_BORDER,
            rect,
            2,
            border_radius=8
        )

        inner = pygame.Rect(
            x + 7,
            y + 7,
            width - 14,
            height - 14
        )

        pygame.draw.rect(
            self.screen,
            (58, 66, 112),
            inner,
            2,
            border_radius=5
        )

        self.text(
            "★",
            self.heading_font,
            GOLD,
            rect.center,
            True
        )

        return rect

    # ========================================================
    # EVENT HANDLING
    # ========================================================

    def handle_event(self, event):

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:

                if self.show_help:
                    self.show_help = False
                else:
                    pygame.event.post(
                        pygame.event.Event(
                            pygame.QUIT
                        )
                    )

                return

            if event.key == pygame.K_r:

                self.game.reset()
                self.selected_card = None
                return

            if event.key == pygame.K_h:

                self.show_help = not self.show_help
                return

        if event.type != pygame.MOUSEBUTTONDOWN:
            return

        if event.button != 1:
            return

        # Help button
        if self.help_rect.collidepoint(event.pos):

            self.show_help = True
            return

        # Restart
        if self.restart_rect.collidepoint(event.pos):

            self.game.reset()
            self.selected_card = None
            return

        # Help screen blocks the game
        if self.show_help:

            close_rect = pygame.Rect(
                450,
                610,
                200,
                45
            )

            if close_rect.collidepoint(event.pos):
                self.show_help = False

            return

        # Game over
        if self.game.game_over:
            return

        # Only human can act
        if self.game.turn != "human":
            return

        # Check if player clicked one of their cards
        for index, rect in self.card_rects:

            if rect.collidepoint(event.pos):

                card = self.game.human.hand[index]

                self.selected_card = card.rank

                # Ask immediately
                self.game.request_rank(
                    card.rank
                )

                self.selected_card = None

                return

    # ========================================================
    # DRAW TOP BAR
    # ========================================================

    def draw_top_bar(self):

        self.text(
            "GO FISH",
            self.title_font,
            TEXT,
            (28, 18)
        )

        self.text(
            "Rule-Based Expert System",
            self.small_font,
            MUTED,
            (31, 58)
        )

        self.button(
            self.help_rect,
            "HOW TO PLAY"
        )

        self.button(
            self.restart_rect,
            "NEW GAME"
        )

    # ========================================================
    # DRAW AI AREA
    # ========================================================

    def draw_ai_area(self):

        pygame.draw.rect(
            self.screen,
            PANEL,
            (25, 82, 1050, 145),
            border_radius=14
        )

        self.text(
            "EXPERT AI",
            self.heading_font,
            TEXT,
            (45, 98)
        )

        self.text(
            f"Books: {len(self.game.ai.books)}",
            self.body_font,
            GOLD,
            (45, 135)
        )

        self.text(
            f"Cards: {len(self.game.ai.hand)}",
            self.body_font,
            MUTED,
            (45, 164)
        )

        # Draw AI cards face-down
        x = 190

        for _ in range(
            min(len(self.game.ai.hand), 14)
        ):

            self.draw_card_back(
                x,
                105
            )

            x += 54

        # Deck
        self.draw_card_back(
            925,
            105,
            70,
            100
        )

        self.text(
            str(len(self.game.deck)),
            self.body_font,
            TEXT,
            (960, 216),
            True
        )

        self.text(
            "DECK",
            self.small_font,
            MUTED,
            (960, 224),
            True
        )

    # ========================================================
    # STATUS
    # ========================================================

    def draw_status(self):

        pygame.draw.rect(
            self.screen,
            PANEL,
            (25, 240, 1050, 115),
            border_radius=14
        )

        self.text(
            "GAME STATUS",
            self.heading_font,
            TEXT,
            (45, 255)
        )

        self.text(
            self.game.message,
            self.body_font,
            TEXT,
            (45, 292)
        )

        if self.game.turn == "human":

            self.text(
                "YOUR TURN — CLICK A CARD TO ASK FOR ITS RANK",
                self.small_font,
                GREEN,
                (45, 325)
            )

        else:

            self.text(
                "AI TURN — EXPERT SYSTEM IS REASONING...",
                self.small_font,
                GOLD,
                (45, 325)
            )

    # ========================================================
    # EXPERT SYSTEM
    # ========================================================

    def draw_expert_panel(self):

        pygame.draw.rect(
            self.screen,
            PANEL,
            (25, 370, 1050, 110),
            border_radius=14
        )

        self.text(
            "🧠 EXPERT SYSTEM",
            self.heading_font,
            TEXT,
            (45, 383)
        )

        explanation = (
            self.game.ai_explanation
            or "Waiting for the AI's first decision."
        )

        self.text(
            explanation,
            self.small_font,
            MUTED,
            (45, 420)
        )

        known = sorted(
            self.game.expert.known_human_ranks
        )

        known_text = (
            ", ".join(known)
            if known
            else "None"
        )

        self.text(
            f"Known opponent ranks: {known_text}",
            self.small_font,
            MUTED,
            (45, 447)
        )

    # ========================================================
    # HUMAN HAND
    # ========================================================

    def draw_human_area(self):

        pygame.draw.rect(
            self.screen,
            PANEL,
            (25, 495, 1050, 200),
            border_radius=14
        )

        self.text(
            "YOUR HAND",
            self.heading_font,
            TEXT,
            (45, 510)
        )

        self.text(
            "Click any card to ask the AI for that rank.",
            self.small_font,
            MUTED,
            (45, 540)
        )

        self.text(
            f"Books: {len(self.game.human.books)}",
            self.body_font,
            GOLD,
            (900, 515)
        )

        self.card_rects = []

        cards = self.game.human.hand

        card_width = 82
        card_height = 112

        gap = 8

        total_width = (
            len(cards) * card_width
            + max(0, len(cards) - 1) * gap
        )

        start_x = max(
            45,
            (1100 - total_width) // 2
        )

        y = 570

        for index, card in enumerate(cards):

            x = start_x + index * (
                card_width + gap
            )

            selected = (
                self.selected_card == card.rank
            )

            rect = self.draw_card(
                card,
                x,
                y,
                card_width,
                card_height,
                selected
            )

            self.card_rects.append(
                (index, rect)
            )

    # ========================================================
    # HELP SCREEN
    # ========================================================

    def draw_help(self):

        overlay = pygame.Surface(
            self.screen.get_size(),
            pygame.SRCALPHA
        )

        overlay.fill(
            (0, 0, 0, 190)
        )

        self.screen.blit(
            overlay,
            (0, 0)
        )

        panel = pygame.Rect(
            180,
            55,
            740,
            600
        )

        pygame.draw.rect(
            self.screen,
            PANEL,
            panel,
            border_radius=18
        )

        pygame.draw.rect(
            self.screen,
            ACCENT,
            panel,
            2,
            border_radius=18
        )

        self.text(
            "HOW TO PLAY GO FISH",
            self.title_font,
            TEXT,
            (550, 90),
            True
        )

        rules = [
            (
                "1.",
                "You and the AI start with 7 cards."
            ),
            (
                "2.",
                "Your goal is to collect books of four cards"
            ),
            (
                "",
                "with the same rank."
            ),
            (
                "3.",
                "On your turn, click a card in your hand."
            ),
            (
                "",
                "This asks the AI for that card's rank."
            ),
            (
                "4.",
                "If the AI has that rank, it gives you ALL"
            ),
            (
                "",
                "cards of that rank."
            ),
            (
                "5.",
                "If the AI does not have it, you hear:"
            ),
            (
                "",
                "\"Go Fish!\" and draw from the deck."
            ),
            (
                "6.",
                "If you draw the rank you asked for, you"
            ),
            (
                "",
                "get another turn."
            ),
            (
                "7.",
                "Four cards of the same rank make a BOOK."
            ),
            (
                "8.",
                "The player with the most books wins."
            ),
        ]

        y = 145

        for number, line in rules:

            if number:

                self.text(
                    number,
                    self.body_font,
                    GOLD,
                    (225, y)
                )

                x = 260

            else:

                x = 260

            self.text(
                line,
                self.small_font,
                TEXT,
                (x, y)
            )

            y += 35

        # Expert system explanation
        pygame.draw.rect(
            self.screen,
            PANEL_LIGHT,
            (220, 470, 660, 110),
            border_radius=12
        )

        self.text(
            "WHY IS THE AI AN EXPERT SYSTEM?",
            self.body_font,
            GOLD,
            (245, 485)
        )

        self.text(
            "The AI stores facts about the game and",
            self.small_font,
            TEXT,
            (245, 515)
        )

        self.text(
            "uses explicit IF/THEN rules to decide",
            self.small_font,
            TEXT,
            (245, 537)
        )

        self.text(
            "which rank it should request.",
            self.small_font,
            TEXT,
            (245, 559)
        )

        close_rect = pygame.Rect(
            450,
            610,
            200,
            45
        )

        self.button(
            close_rect,
            "BACK TO GAME"
        )

    # ========================================================
    # GAME OVER
    # ========================================================

    def draw_game_over(self):

        overlay = pygame.Surface(
            self.screen.get_size(),
            pygame.SRCALPHA
        )

        overlay.fill(
            (0, 0, 0, 160)
        )

        self.screen.blit(
            overlay,
            (0, 0)
        )

        panel = pygame.Rect(
            300,
            230,
            500,
            260
        )

        pygame.draw.rect(
            self.screen,
            PANEL,
            panel,
            border_radius=18
        )

        pygame.draw.rect(
            self.screen,
            ACCENT,
            panel,
            2,
            border_radius=18
        )

        self.text(
            "GAME OVER",
            self.title_font,
            TEXT,
            (550, 265),
            True
        )

        winner_text = self.game.message

        self.text(
            winner_text,
            self.body_font,
            TEXT,
            (550, 315),
            True
        )

        self.text(
            (
                f"Player: {len(self.game.human.books)} books"
                f"     |     "
                f"AI: {len(self.game.ai.books)} books"
            ),
            self.body_font,
            GOLD,
            (550, 355),
            True
        )

        self.text(
            "Press R or click NEW GAME",
            self.small_font,
            MUTED,
            (550, 410),
            True
        )

    # ========================================================
    # MAIN DRAW
    # ========================================================

    def update(self):
        pass

    def draw(self):

        self.screen.fill(BG)

        self.draw_top_bar()

        self.draw_ai_area()

        self.draw_status()

        self.draw_expert_panel()

        self.draw_human_area()

        if self.show_help:

            self.draw_help()

        elif self.game.game_over:

            self.draw_game_over()