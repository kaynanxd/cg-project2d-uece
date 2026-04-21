import pygame
from src.engine.collision import is_clicked
from src.engine.math2d import Matrix3x3 #

class MainMenu:
    def __init__(self, engine):
        self.engine = engine
        self.renderer = engine.renderer
        self.filler = engine.filler
        self.screen_width = self.renderer.width
        self.screen_height = self.renderer.height
        
        self.btn_w, self.btn_h = 220, 50
        self.gap = 20
        self.btn_x = (self.screen_width - self.btn_w) // 2
        
        total_menu_h = (3 * self.btn_h) + (2 * self.gap)
        self.start_y = (self.screen_height - total_menu_h) // 2
        
        self.rects = [
            (self.btn_x, self.start_y, self.btn_w, self.btn_h),
            (self.btn_x, self.start_y + self.btn_h + self.gap, self.btn_w, self.btn_h),
            (self.btn_x, self.start_y + (self.btn_h + self.gap) * 2, self.btn_w, self.btn_h)
        ]
        self.labels = ["JOGAR", "OPÇÕES", "SAIR"]
        
        self.COR_BORDA = (255, 255, 255)
        self.COR_FUNDO_BTN = (30, 30, 80)
        self.COR_HOVER = (60, 60, 140)
        self.COR_TEXTO = (255, 255, 255)
        
        pygame.font.init()
        self.fonte_logo = pygame.font.SysFont("Arial", 50, bold=True)
        self.fonte_btn = pygame.font.SysFont("Arial", 24)

    def draw(self, px_array): 
        mouse_pos = pygame.mouse.get_pos()
        
        for i in range(len(self.rects)):
            rect = self.rects[i]
            x, y, w, h = rect
            hover = is_clicked(mouse_pos, rect)
            cor_atual = self.COR_HOVER if hover else self.COR_FUNDO_BTN
            
            if hover:
                cx, cy = x + w/2, y + h/2
                m = Matrix3x3.translation(-cx, -cy)
                m = Matrix3x3.multiply(Matrix3x3.scale(1.1, 1.1), m)
                m = Matrix3x3.multiply(Matrix3x3.translation(cx, cy), m)
                vertices = [(x, y), (x+w, y), (x+w, y+h), (x, y+h)]
                pontos_btn = [Matrix3x3.apply(m, p) for p in vertices] #
            else:
                pontos_btn = [(x, y), (x+w, y), (x+w, y+h), (x, y+h)]
            
            self.filler.scanline_fill(px_array, pontos_btn, cor_atual) #
            for j in range(4):
                p1, p2 = pontos_btn[j], pontos_btn[(j+1)%4]
                self.renderer.draw_line(px_array, p1[0], p1[1], p2[0], p2[1], self.COR_BORDA) #

    def draw_labels(self):
        texto_logo = self.fonte_logo.render("MEU JOGO", True, self.COR_TEXTO)
        self.engine.screen.blit(texto_logo, ((self.screen_width - texto_logo.get_width()) // 2, self.start_y - 80))

        for i in range(len(self.rects)):
            x, y, w, h = self.rects[i]
            img_texto = self.fonte_btn.render(self.labels[i], True, self.COR_TEXTO)
            text_x = x + (w - img_texto.get_width()) // 2
            text_y = y + (h - img_texto.get_height()) // 2
            self.engine.screen.blit(img_texto, (text_x, text_y))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            
            if is_clicked(mouse_pos, self.rects[0]):
                if self.engine.click_sound: self.engine.click_sound.play() 
                self.engine.state = "GAME"
            # elif is_clicked(mouse_pos, self.rects[1]):
            #     if self.engine.click_sound: self.engine.click_sound.play() 
            elif is_clicked(mouse_pos, self.rects[2]):
                if self.engine.click_sound: self.engine.click_sound.play()
                pygame.time.delay(200) 
                pygame.quit()
                exit()