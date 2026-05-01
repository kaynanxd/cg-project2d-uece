import unittest
from src.game.logic.card_layout import CardLayout

class TestCardLayout(unittest.TestCase):

    def test_positions_count_matches_n_cards(self):
        layout = CardLayout(8, 50, 100, 10, 800, 600)
        self.assertEqual(len(layout.positions), 8)

    def test_single_card_is_centered(self):
        layout = CardLayout(1, 50, 100, 10, 800, 600)
        x, y = layout.positions[0]
        self.assertEqual(x, (800 - 50) // 2)
        self.assertEqual(y, (600 - 100) // 2)

    def test_four_cards_form_2x2_grid(self):
        # cols = ceil(sqrt(4)) = 2, rows = ceil(4/2) = 2
        layout = CardLayout(4, 50, 100, 10, 800, 600)
        x0, y0 = layout.positions[0]
        x1, y1 = layout.positions[1]
        x2, y2 = layout.positions[2]
        # cards 0 and 1 share the same row
        self.assertEqual(y0, y1)
        # cards 0 and 1 are separated by card_w + gap horizontally
        self.assertEqual(x1 - x0, 50 + 10)
        # card 2 is one row below card 0
        self.assertEqual(y2 - y0, 100 + 10)

    def test_positions_are_tuples_of_two(self):
        layout = CardLayout(6, 50, 100, 10, 800, 600)
        for pos in layout.positions:
            self.assertIsInstance(pos, tuple)
            self.assertEqual(len(pos), 2)

if __name__ == "__main__":
    unittest.main()
