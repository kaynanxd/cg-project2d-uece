# CardContainer Modularization Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Split `CardContainer` into focused classes (`Deck`, `CardLayout`, `GameState`) and move card data to `src/data/`, while keeping `CardContainer` as the orchestrator that owns all game state.

**Architecture:** Three new classes under `src/game/logic/` each handle a single concern (shuffling, layout, state/match logic). `CardContainer` creates and owns all of them, delegating to each. All logic classes are free of pygame and can be tested without a display.

**Tech Stack:** Python 3.12, pygame 2.6.1, `unittest` (stdlib)

---

## File Map

| Action | Path | Responsibility |
|--------|------|----------------|
| Create | `src/data/__init__.py` | package marker |
| Create | `src/data/professors.py` | static list of card labels |
| Create | `src/game/logic/__init__.py` | package marker |
| Create | `src/game/logic/deck.py` | shuffle items into `{id: label}` mapping |
| Create | `src/game/logic/card_layout.py` | dynamic grid position calculation |
| Create | `src/game/logic/game_state.py` | tries, pairs, selection and match logic |
| Modify | `src/game/card_container.py` | refactored orchestrator |
| Create | `tests/__init__.py` | package marker |
| Create | `tests/game/__init__.py` | package marker |
| Create | `tests/game/logic/__init__.py` | package marker |
| Create | `tests/game/logic/test_deck.py` | unit tests for Deck |
| Create | `tests/game/logic/test_card_layout.py` | unit tests for CardLayout |
| Create | `tests/game/logic/test_game_state.py` | unit tests for GameState |

---

## Task 1: Create data file and package scaffolding

**Files:**
- Create: `src/data/__init__.py`
- Create: `src/data/professors.py`
- Create: `src/game/logic/__init__.py`
- Create: `tests/__init__.py`
- Create: `tests/game/__init__.py`
- Create: `tests/game/logic/__init__.py`

- [ ] **Step 1: Create all package markers and the data file**

```python
# src/data/__init__.py
# (empty)
```

```python
# src/data/professors.py
PROFESSORS = ["Everardo", "Matheus Cientista", "Ana Luiza", "Claudia Rebouças"]
```

```python
# src/game/logic/__init__.py
# (empty)
```

```python
# tests/__init__.py
# (empty)
```

```python
# tests/game/__init__.py
# (empty)
```

```python
# tests/game/logic/__init__.py
# (empty)
```

- [ ] **Step 2: Verify the data import works**

Run from the project root:
```bash
python -c "from src.data.professors import PROFESSORS; print(PROFESSORS)"
```
Expected output:
```
['Everardo', 'Matheus Cientista', 'Ana Luiza', 'Claudia Rebouças']
```

- [ ] **Step 3: Commit**

```bash
git add src/data/ src/game/logic/__init__.py tests/
git commit -m "chore: scaffold data/, game/logic/, and tests/ packages"
```

---

## Task 2: Implement `Deck` with TDD

**Files:**
- Create: `src/game/logic/deck.py`
- Create: `tests/game/logic/test_deck.py`

- [ ] **Step 1: Write the failing tests**

```python
# tests/game/logic/test_deck.py
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
```

- [ ] **Step 2: Run the tests to verify they fail**

```bash
python -m unittest tests.game.logic.test_deck -v
```
Expected: `ModuleNotFoundError: No module named 'src.game.logic.deck'`

- [ ] **Step 3: Implement `Deck`**

```python
# src/game/logic/deck.py
import random

class Deck:
    def __init__(self, items: list[str]):
        doubled = items + items
        random.shuffle(doubled)
        self.labels = {i: label for i, label in enumerate(doubled)}
        self.size = len(doubled)
```

- [ ] **Step 4: Run the tests to verify they pass**

```bash
python -m unittest tests.game.logic.test_deck -v
```
Expected: 4 tests, all PASS.

- [ ] **Step 5: Commit**

```bash
git add src/game/logic/deck.py tests/game/logic/test_deck.py
git commit -m "feat(logic): add Deck class with shuffle and label mapping"
```

---

## Task 3: Implement `CardLayout` with TDD

**Files:**
- Create: `src/game/logic/card_layout.py`
- Create: `tests/game/logic/test_card_layout.py`

- [ ] **Step 1: Write the failing tests**

```python
# tests/game/logic/test_card_layout.py
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
```

- [ ] **Step 2: Run the tests to verify they fail**

```bash
python -m unittest tests.game.logic.test_card_layout -v
```
Expected: `ModuleNotFoundError: No module named 'src.game.logic.card_layout'`

- [ ] **Step 3: Implement `CardLayout`**

Grid algorithm: `cols = ceil(sqrt(n_cards))`, `rows = ceil(n_cards / cols)`. The full grid is centered on screen.

```python
# src/game/logic/card_layout.py
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
```

- [ ] **Step 4: Run the tests to verify they pass**

```bash
python -m unittest tests.game.logic.test_card_layout -v
```
Expected: 4 tests, all PASS.

- [ ] **Step 5: Commit**

```bash
git add src/game/logic/card_layout.py tests/game/logic/test_card_layout.py
git commit -m "feat(logic): add CardLayout with dynamic grid centering"
```

---

## Task 4: Implement `GameState` with TDD

**Files:**
- Create: `src/game/logic/game_state.py`
- Create: `tests/game/logic/test_game_state.py`

- [ ] **Step 1: Write the failing tests**

```python
# tests/game/logic/test_game_state.py
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
```

- [ ] **Step 2: Run the tests to verify they fail**

```bash
python -m unittest tests.game.logic.test_game_state -v
```
Expected: `ModuleNotFoundError: No module named 'src.game.logic.game_state'`

- [ ] **Step 3: Implement `GameState` and `MatchResult`**

```python
# src/game/logic/game_state.py
from dataclasses import dataclass

@dataclass
class MatchResult:
    matched: bool
    label: str  # only meaningful when matched=True

class GameState:
    def __init__(self, pairs_total: int, tries: int):
        self.tries = tries
        self.pairs_matched = 0
        self.pairs_total = pairs_total
        self._choice: str | None = None

    def select(self, label: str) -> MatchResult | None:
        if self._choice is None:
            self._choice = label
            return None

        first, self._choice = self._choice, None

        if first == label:
            self.pairs_matched += 1
            return MatchResult(matched=True, label=label)

        self.tries -= 1
        return MatchResult(matched=False, label=label)
```

- [ ] **Step 4: Run the tests to verify they pass**

```bash
python -m unittest tests.game.logic.test_game_state -v
```
Expected: 9 tests, all PASS.

- [ ] **Step 5: Run the full test suite to catch any regressions**

```bash
python -m unittest discover -s tests -v
```
Expected: all tests PASS.

- [ ] **Step 6: Commit**

```bash
git add src/game/logic/game_state.py tests/game/logic/test_game_state.py
git commit -m "feat(logic): add GameState and MatchResult with selection and match logic"
```

---

## Task 5: Refactor `CardContainer` as orchestrator

**Files:**
- Modify: `src/game/card_container.py`

- [ ] **Step 1: Replace the contents of `card_container.py`**

```python
# src/game/card_container.py
from src.data.professors import PROFESSORS
from src.game.card import Card
from src.game.logic.deck import Deck
from src.game.logic.card_layout import CardLayout
from src.game.logic.game_state import GameState

class CardContainer:
    def __init__(self, engine):
        self.engine = engine
        self.renderer = engine.renderer
        self.filler = engine.filler

        card_w, card_h, gap = 50, 100, 50

        deck = Deck(PROFESSORS)
        layout = CardLayout(deck.size, card_w, card_h, gap, self.renderer.width, self.renderer.height)
        self.game_state = GameState(pairs_total=len(PROFESSORS), tries=3)

        self.cards = [
            Card(
                engine,
                layout.positions[i][0],
                layout.positions[i][1],
                id=i,
                label=deck.labels[i],
                set_state=self.__set_state,
            )
            for i in range(deck.size)
        ]

    def __set_state(self, label: str):
        result = self.game_state.select(label)
        if result is None:
            return
        if result.matched:
            self.cards = [card for card in self.cards if card.get_label() != result.label]

        print(self.game_state.tries)
        print(f"{self.game_state.pairs_matched}/{self.game_state.pairs_total}")

    def update(self):
        for card in self.cards:
            card.update()

    def draw(self, px_array):
        for card in self.cards:
            card.draw(px_array)

    def draw_ui(self):
        for card in self.cards:
            card.draw_ui()

    def handle_event(self, event):
        for card in self.cards:
            card.handle_event(event)
```

- [ ] **Step 2: Run the full test suite to confirm nothing is broken**

```bash
python -m unittest discover -s tests -v
```
Expected: all tests PASS.

- [ ] **Step 3: Smoke-test the game manually**

```bash
python main.py
```
Expected: game opens, cards appear in a grid layout, clicking two matching cards removes them, clicking two non-matching cards decrements the try counter printed in the terminal.

- [ ] **Step 4: Commit**

```bash
git add src/game/card_container.py
git commit -m "refactor(game): CardContainer delegates to Deck, CardLayout, and GameState"
```
