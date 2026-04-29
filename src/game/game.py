from src.data.professors import PROFESSORS
from src.game.card import Card
from src.game.logic.deck import Deck
from src.game.logic.card_layout import CardLayout
from src.game.logic.game_state import GameState
from src.game.logic.timer import Timer

class Game:
    def __init__(self, engine):
        self.engine = engine
        self.renderer = engine.renderer
        self.filler = engine.filler

        card_w, card_h, gap = 50, 100, 50

        deck = Deck(PROFESSORS)
        layout = CardLayout(deck.size, card_w, card_h, gap, self.renderer.width, self.renderer.height)
        self.game_state = GameState(pairs_total=len(PROFESSORS), tries=3)
        self.timer = Timer()
        self._first_card_id: int | None = None

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

    def __set_state(self, card_id: int, label: str):
        if self._first_card_id == card_id:
            return
        result = self.game_state.select(label)
        if result is None:
            self._first_card_id = card_id
            return
        self._first_card_id = None
        if result.matched:
            self.cards = [card for card in self.cards if card.get_label() != result.label]

        print(self.game_state.tries)
        print(f"{self.game_state.pairs_matched}/{self.game_state.pairs_total}")
        print(f"tempo: {self.timer.elapsed_seconds():.1f}s")

    def update(self, delta_ms: int) -> None:
        self.timer.update(delta_ms)
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
