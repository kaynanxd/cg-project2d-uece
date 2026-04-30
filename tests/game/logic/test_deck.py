import unittest
from src.game.logic.deck import Deck

class TestDeck(unittest.TestCase):

    def test_size_is_double_items(self):
        deck = Deck(["A", "B", "C"])
        self.assertEqual(deck.size, 6)

    def test_labels_keys_are_sequential(self):
        deck = Deck(["A", "B"])
        self.assertEqual(set(deck.labels.keys()), {0, 1, 2, 3})

    def test_each_item_appears_exactly_twice(self):
        items = ["A", "B", "C"]
        deck = Deck(items)
        values = list(deck.labels.values())
        for item in items:
            self.assertEqual(values.count(item), 2)

    def test_empty_items_gives_empty_deck(self):
        deck = Deck([])
        self.assertEqual(deck.size, 0)
        self.assertEqual(deck.labels, {})

if __name__ == "__main__":
    unittest.main()
