import pygame

from src.engine.collision import is_clicked

class Card:
    def __init__(self, engine, x, y, id, label, set_state):
        self.engine = engine
        self.renderer = engine.renderer
        self.filler = engine.filler
        
        self.id = id
        self.label = label
        self.x, self.y = x, y 
        self.w, self.h = 50, 100
        
        self.card_container = (self.x, self.y, self.w, self.h)
        self.set_state = set_state
        
        self.COR_FUNDO = (20, 20, 60)
        self.COR_BORDA = (100, 180, 255)
        self.fonte = pygame.font.SysFont("Arial", 18,)
    
    def get_label(self):
        return self.label
    
    def update(self):
        pass
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse = pygame.mouse.get_pos()
            if is_clicked(mouse, self.card_container):
                self.set_state(self.label)
    
    def draw(self, px_array):
        x, y, w, h = self.x, self.y, self.w, self.h
        pontos = [(x, y), (x+w, y), (x+w, y+h), (x, y+h)]
        
        self.filler.scanline_fill(px_array, pontos, self.COR_FUNDO)
        
        lados = list(zip(pontos, pontos[1:] + [pontos[0]]))
        for p1, p2, in lados:
            ok, nx0, ny0, nx1, ny1 = self.engine.clipping.cohen_sutherland(                                                                                                                                           
                p1[0], p1[1], p2[0], p2[1]                                                                                                                                                                            
            )                                                                                                                                                                                                         
            if ok:                                                                                                                                                                                                    
                self.renderer.draw_line(px_array, nx0, ny0, nx1, ny1, self.COR_BORDA)
    
    def draw_ui(self):
        t = self.fonte.render(str(self.label), True, (255, 255, 255))
        self.engine.screen.blit(t, (
            self.x + (self.w - t.get_width()) // 2,
            self.y + (self.h - t.get_height()) // 2
        ))
    