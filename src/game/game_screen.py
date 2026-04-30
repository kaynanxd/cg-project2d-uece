from src.game.game import Game

class GameScreen:
    def __init__(self, engine):
        self.engine = engine
        self.container = None
        self.last_difficulty = None

    def update(self, delta_ms: int) -> None:
            if self.container is None or self.last_difficulty != self.engine.difficulty:
                self.container = Game(self.engine, self.engine.difficulty)
                self.last_difficulty = self.engine.difficulty
                
            self.container.update(delta_ms)

    def handle_event(self, event):
        if self.container:
            self.container.handle_event(event)

    def draw(self, px_array):
        if self.container:
            self.container.draw(px_array)

    def draw_ui(self):
        if self.container:
            self.container.draw_ui()