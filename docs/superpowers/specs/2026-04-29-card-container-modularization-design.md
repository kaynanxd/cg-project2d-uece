# CardContainer Modularization Design

**Date:** 2026-04-29  
**Branch:** feat/game-screen

## Context

`CardContainer` currently accumulates too many responsibilities: defining card data, shuffling, computing layout, tracking game state, and handling match logic. This design extracts each concern into a focused class, while keeping `CardContainer` as the orchestrator that owns all game state.

## Architecture

```
src/
├── data/
│   └── professors.py          # static list of card labels
└── game/
    ├── logic/
    │   ├── __init__.py
    │   ├── deck.py            # shuffle + id→label mapping
    │   ├── card_layout.py     # dynamic grid position calculation
    │   └── game_state.py      # tries, pairs, selection and match logic
    ├── card.py                # unchanged
    ├── card_container.py      # orchestrator (owns all of the above)
    ├── engine.py              # unchanged
    └── ...
```

## Components

### `src/data/professors.py`

A plain Python list of strings. No logic — just data.

```python
PROFESSORS = ["Everardo", "Matheus Cientista", "Ana Luiza", "Claudia Rebouças"]
```

### `src/game/logic/deck.py` — `Deck`

**Responsibility:** Given a list of items, produce a shuffled `{id: label}` mapping where each item appears exactly twice.

**Interface:**
```python
class Deck:
    def __init__(self, items: list[str]):
        ...
    labels: dict[int, str]   # {0: "Ana", 1: "Everardo", ...} shuffled
    size: int                 # len(items) * 2
```

No pygame dependency. Can be unit-tested in isolation.

### `src/game/logic/card_layout.py` — `CardLayout`

**Responsibility:** Compute (x, y) positions for `n_cards` cards arranged in a balanced dynamic grid, centered on the screen.

**Interface:**
```python
class CardLayout:
    def __init__(self, n_cards: int, card_w: int, card_h: int, gap: int, screen_w: int, screen_h: int):
        ...
    positions: list[tuple[int, int]]   # [(x0, y0), (x1, y1), ...]
```

Grid shape: choose number of columns as `ceil(sqrt(n_cards))`, rows as `ceil(n_cards / cols)`. The layout centers the entire grid on screen. No pygame dependency.

### `src/game/logic/game_state.py` — `GameState` + `MatchResult`

**Responsibility:** Track `tries`, `pairs_matched`, `pairs_total`, and the two current card selections. Process each selection and return a result when a pair has been evaluated.

**Interface:**
```python
@dataclass
class MatchResult:
    matched: bool
    label: str   # label of the pair; only meaningful when matched=True

class GameState:
    def __init__(self, pairs_total: int, tries: int):
        ...
    tries: int
    pairs_matched: int
    pairs_total: int

    def select(self, label: str) -> MatchResult | None:
        # Returns None when only the first card has been selected.
        # Returns MatchResult when the second card is selected:
        #   - matched=True  → pairs_matched incremented, label set
        #   - matched=False → tries decremented, label set
        # Resets internal selection state after returning MatchResult.
```

No pygame dependency. Can be unit-tested in isolation.

### `src/game/card_container.py` — `CardContainer` (orchestrator)

**Responsibility:** Own and coordinate all game objects. React to `MatchResult` by removing matched cards from the card list. Delegate rendering and events to `Card` instances.

**`__init__` flow:**
1. Create `Deck(PROFESSORS)` → get shuffled labels and size
2. Create `CardLayout(deck.size, card_w, card_h, gap, screen_w, screen_h)` → get positions
3. Create `GameState(pairs_total=len(PROFESSORS), tries=3)`
4. Zip `deck.labels` and `layout.positions` to instantiate `Card` objects

**`__set_state(label)` flow:**
1. Call `result = self.game_state.select(label)`
2. If `result is None`: return (waiting for second card)
3. If `result.matched`: remove all cards with `card.get_label() == result.label` from `self.cards`
4. If `not result.matched`: no card removal needed (tries already decremented inside `GameState`)

`update`, `draw`, `draw_ui`, `handle_event` remain simple delegation loops over `self.cards`.

## Data Flow

```
Card clicked
    └─► CardContainer.__set_state(label)
            └─► GameState.select(label) → MatchResult | None
                    ├─ None → wait
                    ├─ matched=True  → remove cards from self.cards
                    └─ matched=False → (tries already decremented)
```

## Out of Scope

- Game over / win condition signaling to Engine (future work)
- Card flip animation (face-down / face-up state)
- Multiple difficulty levels or card sets beyond professors
