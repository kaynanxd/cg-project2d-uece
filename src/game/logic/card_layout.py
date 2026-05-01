from math import ceil, sqrt

class CardLayout:
    def __init__(self, n_cards: int, card_w: int, card_h: int, gap: int, screen_w: int, screen_h: int, cols: int, rows: int):

        self.cols = cols
        self.rows = rows

        total_w = self.cols * card_w + (self.cols - 1) * gap
        total_h = self.rows * card_h + (self.rows - 1) * gap
        start_x = (screen_w - total_w) // 2
        start_y = (screen_h - total_h) // 2

        self.positions: list[tuple[int, int]] = [
            (
                start_x + (i % cols) * (card_w + gap),
                start_y + (i // cols) * (card_h + gap),
            )
            for i in range(n_cards)
        ]
