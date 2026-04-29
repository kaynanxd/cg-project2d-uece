from math import ceil, sqrt

class CardLayout:
    def __init__(self, n_cards: int, card_w: int, card_h: int, gap: int, screen_w: int, screen_h: int):
        cols = ceil(sqrt(n_cards)) if n_cards > 0 else 1
        rows = ceil(n_cards / cols) if n_cards > 0 else 0

        total_w = cols * card_w + (cols - 1) * gap
        total_h = rows * card_h + (rows - 1) * gap
        start_x = (screen_w - total_w) // 2
        start_y = (screen_h - total_h) // 2

        self.positions: list[tuple[int, int]] = [
            (
                start_x + (i % cols) * (card_w + gap),
                start_y + (i // cols) * (card_h + gap),
            )
            for i in range(n_cards)
        ]
