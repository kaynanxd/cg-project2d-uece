import pygame
from src.engine.math2d import Matrix3x3

class SplashScreen:
    def __init__(self, engine):
        self.engine = engine
        self.renderer = engine.renderer
        self.filler = engine.filler
        self.timer = 0
        self.duration = 180 

        self.COR_FUNDO = (10, 10, 40)
        self.COR_BORDA = (255, 255, 255)
        self.COR_DETALHE = (0, 200, 255)
        
        #Carrega a logo para uma matriz numerica e scala ela
        full_matrix, w, h = self.filler.load_texture("assets/uece_logo.png")
        self.logo_matriz, self.logo_w, self.logo_h = Matrix3x3.scale_image_matrix(full_matrix, w, h, 0.5)
        self.pos_x = (self.renderer.width - self.logo_w) // 2
        self.pos_y = (self.renderer.height - self.logo_h) // 2

    def update(self):
        self.timer += 1
        if self.timer >= self.duration:
            self.engine.state = "MENU"

    def draw(self, px_array):
        """Desenha a abertura usando APENAS algoritmos manuais."""
        w, h = self.renderer.width, self.renderer.height
        
        #Borda para o Flood Fill
        self.renderer.draw_line(px_array, 0, 0, w-1, 0, self.COR_BORDA)
        self.renderer.draw_line(px_array, w-1, 0, w-1, h-1, self.COR_BORDA)
        self.renderer.draw_line(px_array, w-1, h-1, 0, h-1, self.COR_BORDA)
        self.renderer.draw_line(px_array, 0, h-1, 0, 0, self.COR_BORDA)
        
        self.filler.flood_fill(px_array, w//2, h//2, self.COR_FUNDO, self.COR_BORDA)

        #Requisito B: Desenhar Circunferência e Elipse 
        self.renderer.draw_circle(px_array, w//2, h//2, 350, self.COR_DETALHE)
        self.renderer.draw_ellipse(px_array, w//2, h//2, 400, 250, self.COR_DETALHE)

        #Desenho Manual da Logo
        for x in range(self.logo_w):
            for y in range(self.logo_h):
                cor_pixel = self.logo_matriz[x][y]
                if cor_pixel[3] > 10:
                    self.renderer.set_pixel(px_array, self.pos_x + x, self.pos_y + y, cor_pixel)

    def draw_ui(self):
        fonte = pygame.font.SysFont("Arial", 18)
        texto = fonte.render("UECE - Computação Gráfica 2026", True, (200, 200, 200))
        self.engine.screen.blit(texto, (20, self.renderer.height - 40))