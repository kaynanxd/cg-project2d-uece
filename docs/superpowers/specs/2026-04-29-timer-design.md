# Timer Design

**Date:** 2026-04-29  
**Branch:** feat/game-screen

## Context

The memory game needs to track how long the player has been playing. The `Timer` class is the sole responsibility of `test_screen`/`card_container` — the engine passes `delta_ms` but has no knowledge of the Timer itself.

## Architecture

```
src/game/logic/timer.py              # new: Timer class
tests/game/logic/test_timer.py       # new: unit tests
src/game/card_container.py           # modified: owns Timer, calls timer.update(delta_ms)
src/game/test_screen.py              # modified: update(delta_ms) signature
src/game/engine.py                   # minimal change: capture clock.tick() return value
```

## Component

### `src/game/logic/timer.py` — `Timer`

**Responsibility:** Accumulate elapsed time in milliseconds via `update(delta_ms)` calls. No pygame dependency.

**Interface:**

```python
class Timer:
    def __init__(self):
        ...
    
    def update(self, delta_ms: int) -> None:
        # Accumulates delta_ms into internal counter.
        # No-op when paused (future implementation).

    def elapsed_seconds(self) -> float:
        # Returns total elapsed time in seconds.

    def pause(self) -> None:
        # Stub — body is `pass` until pause/resume is in scope.

    def resume(self) -> None:
        # Stub — body is `pass` until pause/resume is in scope.
```

**Internal state:** `_elapsed_ms: int = 0`

No pygame dependency. Fully testable by passing controlled `delta_ms` values.

## Data Flow

```
Engine.run()
  └─ delta_ms = self.clock.tick(60)      # was already called; return value was discarded
  └─ if state == "TEST": test_screen.update(delta_ms)

TestScreen.update(delta_ms: int)
  └─ self.container.update(delta_ms)

CardContainer.update(delta_ms: int)
  └─ self.timer.update(delta_ms)
  └─ card.update() for each card
```

## Engine Change

One line only — capture `delta_ms` from the already-existing `clock.tick(60)` call and pass it to `test_screen` for the TEST state. The engine does not import or reference `Timer` in any way.

## Out of Scope

- `pause()` and `resume()` implementation (interface is defined, behavior is stubbed)
- Displaying the timer on screen (HUD)
- Using the timer value for scoring
