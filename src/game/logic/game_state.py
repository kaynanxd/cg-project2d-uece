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
