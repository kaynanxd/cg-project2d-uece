import pygame
from src.engine.collision import is_clicked
from src.engine.math2d import Matrix3x3
from src.game.logic.timer import Timer
from src.game.logic.game_state import GameState
from src.game.game import Game

class ScoreboardHUD:
    def __init__(self, engine, game):
        self.engine = engine
        self.filler = engine.filler
        self.font = pygame.font.SysFont("Jaro", 28)
        self.container = game

        # tamanho do scoreboard 
        self.pop_rect = (10, 10, 200, 200)
    
    def update(self, delta_ms):
        self.timer.update(delta_ms)

    def draw(self, px_array):
        p_x, p_y, p_w, p_h = self.pop_rect

        verts = [
            (p_x, p_y),
            (p_x + p_w, p_y),
            (p_x + p_w, p_y + p_h),
            (p_x, p_y + p_h)
        ]
        
        # só desenha fundo
        self.filler.scanline_fill(px_array, verts, (122, 217, 207))

    def draw_ui(self):
        p_x, p_y, _, _ = self.pop_rect
        screen = self.engine.screen

        difficulty = self.container.difficulty
        timer = int(self.container.timer.elapsed_seconds())
        tries = self.container.game_state.tries
        pairs_matched = self.container.game_state.pairs_matched

        screen.blit(self.font.render(f"NIVEL {difficulty}", True, (0,0,0)), (p_x+10, p_y+10))
        screen.blit(self.font.render(f"TEMPO: {timer}", True, (0,0,0)), (p_x+10, p_y+40))
        screen.blit(self.font.render(f"PLACAR: {pairs_matched}", True, (0,0,0)), (p_x+10, p_y+70))
        screen.blit(self.font.render(f"VIDAS: {tries}", True, (0,0,0)), (p_x+10, p_y+100))