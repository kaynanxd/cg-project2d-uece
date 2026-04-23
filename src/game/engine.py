import pygame
from src.engine.renderer import Renderer
from src.engine.filler import Filler
from src.game.menu import MainMenu 
from src.game.splashscreen import SplashScreen
from src.engine.clipping import Clipping

class Engine:
    def __init__(self, width, height):
        self.clipping = Clipping(0, 0, width, height)
        pygame.init()
        pygame.mixer.init()
        # Música de fundo
        try:
            pygame.mixer.music.load("assets/menumusic.mp3")
            pygame.mixer.music.set_volume(0.05)
            pygame.mixer.music.play(-1)
        except:
            print("Erro: assets/musica_fundo.mp3 não encontrado")

        try:
            self.click_sound = pygame.mixer.Sound("assets/cliquemouse.mp3")
        except:
            self.click_sound = None

        self.screen = pygame.display.set_mode((width, height))
        self.renderer = Renderer(self.screen)
        self.filler = Filler(self.renderer)
        self.clock = pygame.time.Clock()
        
        self.menu_bg_cache = pygame.Surface((width, height))
        self.bg_rendered = False
        
        self.state = "SPLASH"
        self.splash = SplashScreen(self)
        self.menu = MainMenu(self)
        self.needs_render = True 
        self.running = True

    def run(self):
        last_mouse_pos = (0, 0)
        while self.running:
            old_state = self.state
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT: self.running = False
                if self.state == "MENU": self.menu.handle_event(event)

            if self.state == "SPLASH": self.splash.update()
            if self.state != old_state: self.needs_render = True

            if self.state == "MENU":
                current_mouse_pos = pygame.mouse.get_pos()
                if current_mouse_pos != last_mouse_pos:
                    self.needs_render = True
                    last_mouse_pos = current_mouse_pos

            if self.needs_render:
                if self.state == "MENU" and not self.bg_rendered:
                    px_bg = pygame.PixelArray(self.menu_bg_cache)
                    pontos_fundo = [(0, 0), (self.renderer.width, 0), (self.renderer.width, self.renderer.height), (0, self.renderer.height)]
                    self.filler.fill_polygon_gradient(px_bg, pontos_fundo, (0, 0, 150), (100, 150, 255))
                    px_bg.close()
                    self.bg_rendered = True

                self.screen.fill((0, 0, 0))
                
                if self.state == "SPLASH":
                    px = pygame.PixelArray(self.screen)
                    self.splash.draw(px)
                    px.close()
                elif self.state == "MENU":
                    self.screen.blit(self.menu_bg_cache, (0, 0))
                    px = pygame.PixelArray(self.screen)
                    self.menu.draw(px)
                    px.close()
                    
                if self.state == "MENU":
                    self.menu.draw_labels()
                
                self.needs_render = False

            if self.state == "SPLASH": self.splash.draw_ui()


            pygame.display.flip()
            self.clock.tick(60)