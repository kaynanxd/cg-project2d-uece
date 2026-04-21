import pygame

class SplashScreen:
    def __init__(self, engine):
        self.engine = engine
        self.timer = 0
        self.duration = 60

        self.COR_FUNDO = (10, 10, 40)
        self.COR_BORDA = (255, 255, 255)
        
        # Carrega a logo
        self.logo_original = pygame.image.load("assets/uece_logo.png").convert_alpha()
        escala = 0.5
        nova_largura = int(self.logo_original.get_width() * escala)
        nova_altura = int(self.logo_original.get_height() * escala)
        self.logo = pygame.transform.smoothscale(self.logo_original, (nova_largura, nova_altura))
        self.logo_rect = self.logo.get_rect(center=(engine.renderer.width // 2, engine.renderer.height // 2))

    def update(self):
        self.timer += 1
        if self.timer >= self.duration:
            self.engine.state = "MENU"

    def draw(self, px_array):
        """Executa o Flood Fill manual apenas uma vez."""
        w, h = self.engine.renderer.width, self.engine.renderer.height
        
        self.engine.renderer.draw_line(px_array, 0, 0, w-1, 0, self.COR_BORDA)
        self.engine.renderer.draw_line(px_array, w-1, 0, w-1, h-1, self.COR_BORDA)
        self.engine.renderer.draw_line(px_array, w-1, h-1, 0, h-1, self.COR_BORDA)
        self.engine.renderer.draw_line(px_array, 0, h-1, 0, 0, self.COR_BORDA)
        
        self.engine.filler.flood_fill(px_array, w//2, h//2, self.COR_FUNDO, self.COR_BORDA)

    def draw_ui(self):
        self.engine.screen.blit(self.logo, self.logo_rect)