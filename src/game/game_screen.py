import pygame
from src.game.game import Game
from src.game.scoreboardhud import ScoreboardHUD

class GameScreen:
    def __init__(self, engine):
        self.engine = engine
        self.container = Game(engine, engine.difficulty)
        self.last_difficulty = None
        self.scoreboard = ScoreboardHUD(engine, self.container)

    def update(self, delta_ms: int) -> None:
        if self.last_difficulty != self.engine.difficulty:
            self.container = Game(self.engine, self.engine.difficulty)
            self.last_difficulty = self.engine.difficulty
            
            # atualizar referência
            self.scoreboard.container = self.container

        self.container.update(delta_ms)

    def handle_event(self, event):
        if self.container:
            self.container.handle_event(event)

    def draw(self, px_array):
        if self.container:
            self.container.draw(px_array)

    def draw_ui(self, screen):
        if self.container:
            self.container.draw_ui()

        if self.scoreboard:
            px_array = pygame.PixelArray(screen)
            self.scoreboard.draw(px_array)
            
            px_array.close()
            
            self.scoreboard.draw_ui()