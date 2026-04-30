import unittest
from src.game.logic.timer import Timer


class TestTimer(unittest.TestCase):

    def test_elapsed_seconds_starts_at_zero(self):
        timer = Timer()
        self.assertEqual(timer.elapsed_seconds(), 0.0)

    def test_update_converts_ms_to_seconds(self):
        timer = Timer()
        timer.update(2000)
        self.assertEqual(timer.elapsed_seconds(), 2.0)

    def test_multiple_updates_accumulate(self):
        timer = Timer()
        timer.update(100)
        timer.update(200)
        timer.update(700)
        self.assertEqual(timer.elapsed_seconds(), 1.0)

    def test_pause_is_callable(self):
        timer = Timer()
        timer.update(1000)
        timer.pause()  # must not raise

    def test_resume_is_callable(self):
        timer = Timer()
        timer.update(1000)
        timer.resume()  # must not raise


if __name__ == "__main__":
    unittest.main()
