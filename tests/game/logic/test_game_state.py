import unittest
from src.game.logic.game_state import GameState, MatchResult

class TestGameState(unittest.TestCase):

    def test_first_select_returns_none(self):
        state = GameState(pairs_total=4, tries=3)
        result = state.select("A")
        self.assertIsNone(result)

    def test_matching_pair_returns_matched_true(self):
        state = GameState(pairs_total=4, tries=3)
        state.select("A")
        result = state.select("A")
        self.assertIsNotNone(result)
        self.assertTrue(result.matched)

    def test_matching_pair_result_has_correct_label(self):
        state = GameState(pairs_total=4, tries=3)
        state.select("Ana")
        result = state.select("Ana")
        self.assertEqual(result.label, "Ana")

    def test_non_matching_pair_returns_matched_false(self):
        state = GameState(pairs_total=4, tries=3)
        state.select("A")
        result = state.select("B")
        self.assertIsNotNone(result)
        self.assertFalse(result.matched)

    def test_match_increments_pairs_matched(self):
        state = GameState(pairs_total=4, tries=3)
        state.select("A")
        state.select("A")
        self.assertEqual(state.pairs_matched, 1)

    def test_no_match_decrements_tries(self):
        state = GameState(pairs_total=4, tries=3)
        state.select("A")
        state.select("B")
        self.assertEqual(state.tries, 2)

    def test_match_does_not_decrement_tries(self):
        state = GameState(pairs_total=4, tries=3)
        state.select("A")
        state.select("A")
        self.assertEqual(state.tries, 3)

    def test_no_match_does_not_increment_pairs_matched(self):
        state = GameState(pairs_total=4, tries=3)
        state.select("A")
        state.select("B")
        self.assertEqual(state.pairs_matched, 0)

    def test_state_resets_after_evaluation(self):
        state = GameState(pairs_total=4, tries=3)
        state.select("A")
        state.select("B")       # evaluated — resets internal selection
        result = state.select("C")  # new first selection
        self.assertIsNone(result)

if __name__ == "__main__":
    unittest.main()
