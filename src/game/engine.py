import pygame
from src.engine.renderer import Renderer
from src.engine.filler import Filler
from src.game.menu import MainMenu
from src.game.splashscreen import SplashScreen
from src.engine.clipping import Clipping
from src.game.game_screen import GameScreen

from src.engine.audio import AudioManager
 
class Engine:
    def __init__(self, width, height):
        self.clipping = Clipping(0, 0, width, height)
        pygame.init()
        self.audio = AudioManager()
        self.audio.load_sfx("click", "assets/cliquemouse.mp3")
        self.audio.load_sfx("hover", "assets/clique.mp3")
        self.audio.play_music("assets/menumusic.mp3")
        
 
        self.screen = pygame.display.set_mode((width, height))
        self.renderer = Renderer(self.screen)
        self.filler = Filler(self.renderer)
        self.clock = pygame.time.Clock()
        
        self.menu_bg_cache = pygame.Surface((width, height))
        self.bg_rendered = False
        
        self.state = "TEST"
        self.splash = SplashScreen(self)
        self.menu = MainMenu(self)
        self.game_screen = GameScreen(self)
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
                if self.state == "TEST": self.game_screen.handle_event(event)

            if self.state == "SPLASH": self.splash.update()
            if self.state != old_state: self.needs_render = True
 
            current_mouse_pos = pygame.mouse.get_pos()
            if self.state == "MENU":
                self.needs_render = True 
            elif self.state in ("TEST",) and current_mouse_pos != last_mouse_pos:
                self.needs_render = True
                last_mouse_pos = current_mouse_pos
 
            if self.needs_render:
                self.screen.fill((0, 0, 0))
 
                if self.state == "SPLASH":
                    px = pygame.PixelArray(self.screen)
                    self.splash.draw(px)
                    px.close()
 
                elif self.state == "MENU":
                    self.needs_render = True
                    if not self.menu.bg_rendered:
                        self.menu._render_background()
                    self.screen.blit(self.menu.bg_cache, (0, 0))
                    px = pygame.PixelArray(self.screen)
                    self.menu.draw(px)
                    px.close()
                elif self.state == "TEST":
                    px = pygame.PixelArray(self.screen)
                    self.game_screen.draw(px)
                    px.close()
                    self.game_screen.draw_ui()
                    
                if self.state == "MENU":
                    self.menu.draw_labels()
 
                self.needs_render = False
 
            if self.state == "SPLASH": self.splash.draw_ui()
 
            pygame.display.flip()
            delta_ms = self.clock.tick(60)
            if self.state == "TEST":
                self.game_screen.update(delta_ms)
