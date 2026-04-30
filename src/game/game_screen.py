from src.game.game import Game

class GameScreen:
    def __init__(self, engine):
        self.engine = engine
        self.container = Game(engine)

    def handle_event(self, event):
        self.container.handle_event(event)

    def draw(self, px_array):
        self.container.draw(px_array)

    def draw_ui(self):
        self.container.draw_ui()

    def update(self, delta_ms: int) -> None:
        self.container.update(delta_ms)
