import pygame
from src.engine.collision import is_clicked

class GamePopup:
    def __init__(self, engine, title, color_theme):
        self.engine = engine
        self.title = title
        self.color_theme = color_theme
        self.bg_cache = pygame.Surface((engine.renderer.width, engine.renderer.height))
        self.rendered_once = False
        
        self.w, self.h = 600, 450
        self.x = (engine.renderer.width - self.w) // 2
        self.y = (engine.renderer.height - self.h) // 2
        
        self.btn_retry_rect = (self.x + 50, self.y + self.h - 80, 200, 50)
        self.btn_menu_rect = (self.x + self.w - 250, self.y + self.h - 80, 200, 50)
        
        self.hover_retry = False
        self.hover_menu = False

    def update(self, mouse_pos):
        self.hover_retry = is_clicked(mouse_pos, self.btn_retry_rect)
        self.hover_menu = is_clicked(mouse_pos, self.btn_menu_rect)

    def _render_static_content(self):
        px_cache = pygame.PixelArray(self.bg_cache)
        
        verts_overlay = [(0, 0), (self.engine.renderer.width, 0), 
                         (self.engine.renderer.width, self.engine.renderer.height), 
                         (0, self.engine.renderer.height)]
        self.engine.filler.scanline_fill(px_cache, verts_overlay, (15, 15, 25))

        verts_pop = [(self.x, self.y), (self.x + self.w, self.y), 
                     (self.x + self.w, self.y + self.h), (self.x, self.y + self.h)]
        self.engine.filler.scanline_fill(px_cache, verts_pop, (240, 240, 240))
        
        px_cache.close()
        self.rendered_once = True

    # AAAAAAAAAAAAAAAAAAAAAAAAA

    def draw(self, px_array):
        if not self.rendered_once:
            self._render_static_content()

        px_cache = pygame.PixelArray(self.bg_cache)
        px_array[:] = px_cache[:]
        px_cache.close()

        self._draw_btn(px_array, self.btn_retry_rect, self.hover_retry)
        self._draw_btn(px_array, self.btn_menu_rect, self.hover_menu)
        
        verts_pop = [(self.x, self.y), (self.x + self.w, self.y), 
                     (self.x + self.w, self.y + self.h), (self.x, self.y + self.h)]
        for j in range(4):
            p1, p2 = verts_pop[j], verts_pop[(j+1)%4]
            aceito, nx0, ny0, nx1, ny1 = self.engine.clipping.cohen_sutherland(
                p1[0], p1[1], p2[0], p2[1]
            )
            if aceito:
                self.engine.renderer.draw_line(px_array, nx0, ny0, nx1, ny1, self.color_theme)

    # AAAAAAAAAAAAAAAAAAAAAAAAAA

    def _draw_btn(self, px_array, rect, is_hovered):
        x, y, w, h = rect
        cor = self.color_theme if is_hovered else (200, 200, 200)
        verts = [(x, y), (x+w, y), (x+w, y+h), (x, y+h)]
        self.engine.filler.scanline_fill(px_array, verts, cor)

        for j in range(4):
            p1, p2 = verts[j], verts[(j+1)%4]
            self.engine.renderer.draw_line(px_array, p1[0], p1[1], p2[0], p2[1], (0, 0, 0))

    def draw_labels(self, screen, font, stats):
        """
        stats: dicionário contendo {'tempo': s, 'vidas': v, 'acertos': a}
        """
        txt_title = font.render(self.title, True, self.color_theme)
        screen.blit(txt_title, (self.x + (self.w - txt_title.get_width()) // 2, self.y + 30))
        
        y_off = self.y + 120
        labels_stats = [
            f"Tempo: {stats['tempo']}s",
            f"Vidas Restantes: {stats['vidas']}",
            f"Acertos: {stats['acertos']}"
        ]
        
        for s in labels_stats:
            img = font.render(s, True, (0, 0, 0))
            screen.blit(img, (self.x + (self.w - img.get_width()) // 2, y_off))
            y_off += 50
            
        self._draw_btn_label(screen, font, self.btn_retry_rect, "REPETIR")
        self._draw_btn_label(screen, font, self.btn_menu_rect, "MENU")

    def _draw_btn_label(self, screen, font, rect, text):
        img = font.render(text, True, (0, 0, 0))
        screen.blit(img, (rect[0] + (rect[2] - img.get_width()) // 2, 
                          rect[1] + (rect[3] - img.get_height()) // 2))

class WinPopup(GamePopup):
    def __init__(self, engine):
        super().__init__(engine, "VITORIA!", (0, 180, 100))

class LosePopup(GamePopup):
    def __init__(self, engine):
        super().__init__(engine, "FIM DE JOGO", (200, 40, 40))