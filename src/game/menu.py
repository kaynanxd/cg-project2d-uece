import pygame
from src.engine.collision import is_clicked
from src.engine.math2d import Matrix3x3
import math
import random
 
class MainMenu:
    def __init__(self, engine):
        self.engine = engine
        self.renderer = engine.renderer
        self.filler = engine.filler
        self.screen_width = self.renderer.width
        self.screen_height = self.renderer.height
        self.cards = [FallingCard(self.screen_width, self.screen_height) for _ in range(14)]
        self.hovered_index = -1

        self.show_popup = False
        self.popup_text = ""
        
        self.pop_w, self.pop_h = 800, 550
        self.pop_x = (self.screen_width - self.pop_w) // 2
        self.pop_y = (self.screen_height - self.pop_h) // 2
        self.pop_rect = (self.pop_x, self.pop_y, self.pop_w, self.pop_h)
        
        self.close_btn_w, self.close_btn_h = 150, 50
        self.close_btn_rect = (
            self.pop_x + (self.pop_w - self.close_btn_w) // 2,
            self.pop_y + self.pop_h - 60,
            self.close_btn_w, self.close_btn_h
        )

        self.txt_tutorial = [
            "TUTORIAL",
            "",
            "- Use o mouse para clicar nas cartas",
            "- Encontre os pares iguais",
            "- A Cada Erro Se Perde Uma Vida",
            "- Se Esgotar Vidas Então GameOver",
            "- Complete o jogo no menor tempo",
        ]
        self.txt_creditos = [
            "CREDITOS",
            "",
            "Desenvolvido por:",
            "-Kaynan Santos Freitas",
            "-Ana Beatriz Oliveira Duarte",
            "-Marcello Hwang Song Lee",
            "UECE - Computacao Grafica 2026"
        ]

        self.sound_on = True
        self.mute_btn_size = 40
        self.mute_gap = 20
        self.mute_hovered = False
        self.mute_rect = (
            self.screen_width - self.mute_btn_size - self.mute_gap, self.screen_height - self.mute_btn_size - self.mute_gap,
            self.mute_btn_size, self.mute_btn_size
        )
        self.tex_sound_on, self.tw_on, self.th_on = self.filler.load_texture("assets/sound_on.png")
        self.tex_sound_off, self.tw_off, self.th_off = self.filler.load_texture("assets/sound_off.png")
        
        self.btn_w, self.btn_h = 220, 50
        self.gap = 20
        self.btn_x = (self.screen_width - self.btn_w) // 2
        
        total_menu_h = (3 * self.btn_h) + (2 * self.gap)
        self.start_y = (self.screen_height - total_menu_h) // 2
        
        self.rects = [
            (self.btn_x, self.start_y, self.btn_w, self.btn_h),
            (self.btn_x, self.start_y + self.btn_h + self.gap, self.btn_w, self.btn_h),
            (self.btn_x, self.start_y + (self.btn_h + self.gap) * 2, self.btn_w, self.btn_h),
            (self.btn_x, self.start_y + (self.btn_h + self.gap) * 3, self.btn_w, self.btn_h)
        ]
        self.labels = ["JOGAR", "TUTORIAL","CRÉDITOS", "SAIR"]
        
        self.COR_BORDA = (143, 143, 143)
        self.COR_FUNDO_BTN = (191, 191, 191)
        self.COR_HOVER = (117, 230, 216)
        self.COR_TEXTO = (0, 0, 0)
        
        self.menu_state = "MAIN"
        self.diff_labels = ["FACIL", "MEDIO", "DIFICIL", "VOLTAR"]
        self.diff_rects = [
            (self.btn_x, self.start_y + (self.btn_h + self.gap) * i, self.btn_w, self.btn_h)
            for i in range(4)
        ]

        pygame.font.init()
        self.fonte_logo = pygame.font.SysFont("Jaro", 76)
        self.fonte_btn = pygame.font.SysFont("Jaro", 36)
 
        self.bg_cache = pygame.Surface((self.screen_width, self.screen_height)).convert()
        self.bg_rendered = False
 
    def _render_background(self):
        """Desenha o gradiente de fundo uma única vez e armazena em cache."""
        px_bg = pygame.PixelArray(self.bg_cache)
        pontos = [
            (0, 0),
            (self.screen_width, 0),
            (self.screen_width, self.screen_height),
            (0, self.screen_height)
        ]
        self.filler.fill_polygon_gradient(px_bg, pontos,  (255, 255, 255),(230, 255, 254))
        px_bg.close()
        self.bg_rendered = True
 
    def draw(self, px_array):
        if not self.bg_rendered:
            self._render_background()
 
        mouse_pos = pygame.mouse.get_pos()

        for card in self.cards:
            card.update()
            verts = card.get_vertices()
            self.filler.scanline_fill(px_array, verts, card.color)
            for j in range(4):
                p1, p2 = verts[j], verts[(j+1)%4]
                aceito, nx0, ny0, nx1, ny1 = self.engine.clipping.cohen_sutherland(p1[0], p1[1], p2[0], p2[1])
                if aceito:
                    self.renderer.draw_line(px_array, nx0, ny0, nx1, ny1, card.border_color)
        
        for i in range(len(self.rects)):
            rect = self.rects[i]
            x, y, w, h = rect
            hover = is_clicked(mouse_pos, rect) if not self.show_popup else False

            if hover and self.hovered_index != i:
                self.engine.audio.play_sfx("hover")
            
            if hover:
                self.hovered_index = i

            cor_atual = self.COR_HOVER if hover else self.COR_FUNDO_BTN
            
            if hover:
                cx, cy = x + w/2, y + h/2
                m = Matrix3x3.translation(-cx, -cy)
                m = Matrix3x3.multiply(Matrix3x3.scale(1.1, 1.1), m)
                m = Matrix3x3.multiply(Matrix3x3.translation(cx, cy), m)
                vertices = [(x, y), (x+w, y), (x+w, y+h), (x, y+h)]
                pontos_btn = [Matrix3x3.apply(m, p) for p in vertices]
            else:
                pontos_btn = [(x, y), (x+w, y), (x+w, y+h), (x, y+h)]

            if not any(is_clicked(mouse_pos, r) for r in self.rects):
                self.hovered_index = -1
            
            self.filler.scanline_fill(px_array, pontos_btn, cor_atual)
            for j in range(4):
                p1, p2 = pontos_btn[j], pontos_btn[(j+1)%4]
                
                # Requisito G: Aplicando Cohen-Sutherland antes de rasterizar
                aceito, nx0, ny0, nx1, ny1 = self.engine.clipping.cohen_sutherland(
                    p1[0], p1[1], p2[0], p2[1]
                )
                if aceito:
                    self.renderer.draw_line(px_array, nx0, ny0, nx1, ny1, self.COR_BORDA)

        current_rects = self.rects if self.menu_state == "MAIN" else self.diff_rects
        
        for i in range(len(current_rects)):
            rect = current_rects[i]
            x, y, w, h = rect
            hover = is_clicked(mouse_pos, rect) if not self.show_popup else False

            if hover and self.hovered_index != i:
                self.engine.audio.play_sfx("hover")
                self.hovered_index = i

            cor_atual = self.COR_HOVER if hover else self.COR_FUNDO_BTN
            
            # Matriz de Escala (Requisito D)
            if hover:
                cx, cy = x + w/2, y + h/2
                m = Matrix3x3.translation(-cx, -cy)
                m = Matrix3x3.multiply(Matrix3x3.scale(1.1, 1.1), m)
                m = Matrix3x3.multiply(Matrix3x3.translation(cx, cy), m)
                pontos_btn = [Matrix3x3.apply(m, p) for p in [(x, y), (x+w, y), (x+w, y+h), (x, y+h)]]
            else:
                pontos_btn = [(x, y), (x+w, y), (x+w, y+h), (x, y+h)]

            self.filler.scanline_fill(px_array, pontos_btn, cor_atual)
            
            # Bordas com Clipping (Requisito G)
            for j in range(4):
                p1, p2 = pontos_btn[j], pontos_btn[(j+1)%4]
                aceito, nx0, ny0, nx1, ny1 = self.engine.clipping.cohen_sutherland(p1[0], p1[1], p2[0], p2[1])
                if aceito:
                    self.renderer.draw_line(px_array, nx0, ny0, nx1, ny1, self.COR_BORDA)

        if not any(is_clicked(mouse_pos, r) for r in current_rects):
            self.hovered_index = -1

        #Botao de volume
        mx, my = pygame.mouse.get_pos()
        x, y, w, h = self.mute_rect
        hover = is_clicked((mx, my), self.mute_rect)

        cor_bg = self.COR_HOVER if hover else (191, 191, 191)

        if hover:
            cx, cy = x + w/2, y + h/2 
            m = Matrix3x3.translation(-cx, -cy)
            m = Matrix3x3.multiply(Matrix3x3.scale(1.15, 1.15), m) 
            m = Matrix3x3.multiply(Matrix3x3.translation(cx, cy), m)
            
            vertices_base = [(x, y), (x+w, y), (x+w, y+h), (x, y+h)]
            pontos_fundo = [Matrix3x3.apply(m, p) for p in vertices_base]
        else:
            pontos_fundo = [(x, y), (x+w, y), (x+w, y+h), (x, y+h)]

        self.filler.scanline_fill(px_array, pontos_fundo, cor_bg)

        #Mapeamento de Textura(Requisito H)
        pad = 6 
        textura_atual = self.tex_sound_on if self.sound_on else self.tex_sound_off
        tw, th = (self.tw_on, self.th_on) if self.sound_on else (self.tw_off, self.th_off)

        vertices_textured = [
            (pontos_fundo[0][0] + pad, pontos_fundo[0][1] + pad, 0, 0),
            (pontos_fundo[1][0] - pad, pontos_fundo[1][1] + pad, tw, 0),
            (pontos_fundo[2][0] - pad, pontos_fundo[2][1] - pad, tw, th),
            (pontos_fundo[3][0] + pad, pontos_fundo[3][1] - pad, 0, th)
        ]

        self.filler.paint_textured_polygon(
            px_array, 
            self.screen_width, 
            self.screen_height, 
            vertices_textured, 
            textura_atual, 
            tw, 
            th
        )

        if self.show_popup:
            for ty in range(0, self.screen_height, 4): 
                for tx in range(0, self.screen_width, 4):
                    px_array[tx, ty] = (10, 10, 10)

            p_x, p_y, p_w, p_h = self.pop_rect
            verts_pop = [(p_x, p_y), (p_x + p_w, p_y), (p_x + p_w, p_y + p_h), (p_x, p_y + p_h)]
            self.filler.scanline_fill(px_array, verts_pop, (230, 230, 230)) 
            
            for j in range(4):
                p1, p2 = verts_pop[j], verts_pop[(j+1)%4]
                self.renderer.draw_line(px_array, p1[0], p1[1], p2[0], p2[1], (0, 0, 0))

            bx, by, bw, bh = self.close_btn_rect
            hover_close = is_clicked(mouse_pos, self.close_btn_rect)
            cor_c = self.COR_HOVER if hover_close else (180, 180, 180)
            v_c = [(bx, by), (bx+bw, by), (bx+bw, by+bh), (bx, by+bh)]
            self.filler.scanline_fill(px_array, v_c, cor_c)
            
            if hover_close and self.hovered_index != 100:
                self.engine.audio.play_sfx

    def draw_labels(self):

        if not self.show_popup:

            texto_logo = self.fonte_logo.render("UECE MEMORY", True, self.COR_TEXTO)
            self.engine.screen.blit(texto_logo, ((self.screen_width - texto_logo.get_width()) // 2, self.start_y - 80))

            labels_atuais = self.labels if self.menu_state == "MAIN" else self.diff_labels
            rects_atuais = self.rects if self.menu_state == "MAIN" else self.diff_rects
            
            for i in range(len(rects_atuais)):
                x, y, w, h = rects_atuais[i]
                img_texto = self.fonte_btn.render(labels_atuais[i], True, self.COR_TEXTO)
                text_x = x + (self.btn_w - img_texto.get_width()) // 2
                text_y = y + (self.btn_h - img_texto.get_height()) // 2
                self.engine.screen.blit(img_texto, (text_x, text_y))
        
        else:
            y_offset = self.pop_y + 50
            for linha in self.popup_text:
                img_linha = self.fonte_btn.render(linha, True, (0, 0, 0))
                lx = self.pop_x + (self.pop_w - img_linha.get_width()) // 2
                self.engine.screen.blit(img_linha, (lx, y_offset))
                y_offset += 45
            
            txt_close = self.fonte_btn.render("FECHAR", True, (0, 0, 0))
            cx = self.close_btn_rect[0] + (self.close_btn_w - txt_close.get_width()) // 2
            cy = self.close_btn_rect[1] + (self.close_btn_h - txt_close.get_height()) // 2
            self.engine.screen.blit(txt_close, (cx, cy))
 
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()

            if self.show_popup:
                if is_clicked(mouse_pos, self.close_btn_rect):
                    self.engine.audio.play_sfx("click")
                    self.show_popup = False
                return

            if self.menu_state == "MAIN":
                if is_clicked(mouse_pos, self.rects[0]): 
                    self.engine.audio.play_sfx("click")
                    self.menu_state = "DIFFICULTY" 
                elif is_clicked(mouse_pos, self.rects[1]):
                    self.engine.audio.play_sfx("click")
                    self.popup_text = self.txt_tutorial
                    self.show_popup = True
                elif is_clicked(mouse_pos, self.rects[2]): 
                    self.engine.audio.play_sfx("click")
                    self.popup_text = self.txt_creditos
                    self.show_popup = True
                elif is_clicked(mouse_pos, self.rects[3]): 
                    self.engine.audio.play_sfx("click")
                    pygame.time.delay(200); pygame.quit(); exit()

            elif self.menu_state == "DIFFICULTY":
                if is_clicked(mouse_pos, self.diff_rects[0]):
                    self.engine.audio.play_sfx("click")
                    self.engine.game_screen.container = None
                    self.engine.difficulty = "EASY" 
                    self.engine.state = "GAME"
                elif is_clicked(mouse_pos, self.diff_rects[1]): 
                    self.engine.audio.play_sfx("click")
                    self.engine.game_screen.container = None
                    self.engine.difficulty = "MEDIUM"
                    self.engine.state = "GAME"
                elif is_clicked(mouse_pos, self.diff_rects[2]): 
                    self.engine.audio.play_sfx("click")
                    self.engine.game_screen.container = None
                    self.engine.difficulty = "HARD"
                    self.engine.state = "GAME"
                elif is_clicked(mouse_pos, self.diff_rects[3]):
                    self.engine.audio.play_sfx("click")
                    self.menu_state = "MAIN"

            if is_clicked(mouse_pos, self.mute_rect):
                self.sound_on = not self.sound_on
                self.engine.audio.set_music_volume(0.05 if self.sound_on else 0)
                self.engine.audio.play_sfx("click")

class FallingCard:
    _colunas_disponiveis = []
    _total_colunas = 10 

    def __init__(self, screen_w, screen_h):
        self.screen_w = screen_w
        self.screen_h = screen_h

        if not FallingCard._colunas_disponiveis:
            FallingCard._colunas_disponiveis = list(range(FallingCard._total_colunas))
            random.shuffle(FallingCard._colunas_disponiveis)
        self.indice_coluna = FallingCard._colunas_disponiveis.pop() if FallingCard._colunas_disponiveis else random.randint(0, 9)
        
        self.reset(start_offscreen=True)
        self.y = random.randint(-screen_h, screen_h)

    def reset(self, start_offscreen=True):
        largura_coluna = self.screen_w // FallingCard._total_colunas
        self.x = (self.indice_coluna * largura_coluna) + (largura_coluna // 2)
        self.x += random.randint(-15, 15)

        if start_offscreen:
            self.y = random.randint(-1000, -100)
        else:
            self.y = random.randint(-screen_h, 0)

        self.speed = random.uniform(0.7, 1.5)
        self.angle = random.uniform(0, math.pi * 2)
        self.angle_speed = random.uniform(-0.01, 0.01)
        self.w = 60
        self.h = 90
        self.color = (149, 232, 215) 
        self.border_color = (200, 220, 255)

    def update(self):
        self.y += self.speed
        self.angle += self.angle_speed
        if self.y > self.screen_h + 100:
            self.reset(start_offscreen=True)

    def get_vertices(self):
        hw, hh = self.w / 2, self.h / 2
        corners = [(-hw, -hh), (hw, -hh), (hw, hh), (-hw, hh)]
        from src.engine.math2d import Matrix3x3 
        m = Matrix3x3.rotation(self.angle)
        m = Matrix3x3.multiply(Matrix3x3.translation(self.x, self.y), m)
        return [Matrix3x3.apply(m, p) for p in corners]