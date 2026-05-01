from src.data.professors import PROFESSORS
from src.game.card import Card
from src.game.logic.deck import Deck
from src.game.logic.card_layout import CardLayout
from src.game.logic.game_state import GameState
from src.game.logic.timer import Timer
from src.game.popup import WinPopup, LosePopup
from src.engine.collision import is_clicked
import pygame
import random

class Game:
    def __init__(self, engine, difficulty="EASY"):
        self.engine = engine
        self.renderer = engine.renderer
        self.filler = engine.filler
        self.difficulty = difficulty

        # AAAAAAAAAAAAAAAAAAAAAAAAAA

        self.tex_bg, self.bg_w, self.bg_h = self.filler.load_texture("assets/bg_partida.png")

        self.bg_cache = pygame.Surface((self.renderer.width, self.renderer.height)).convert()
        self.bg_rendered = False

        # AAAAAAAAAAAAAAAAAAAAAAAAAA

        self.btn_size = 40
        self.gap = 15
        self.back_rect = (
            self.renderer.width - (self.btn_size * 2) - (self.gap * 2), 
            self.gap, 
            self.btn_size, 
            self.btn_size
        )

        self.mute_rect = (
            self.renderer.width - self.btn_size - self.gap, 
            self.gap, 
            self.btn_size, 
            self.btn_size
        )

        self.tex_back, self.bw, self.bh = self.filler.load_texture("assets/back_icon.png")
        self.tex_on, self.onw, self.onh = self.filler.load_texture("assets/sound_on.png")
        self.tex_off, self.offw, self.offh = self.filler.load_texture("assets/sound_off.png")
        self.mute_hover = False
        self.back_hover = False

        self.win_popup = WinPopup(engine)
        self.lose_popup = LosePopup(engine)
        self.show_popup = None 

        if difficulty == "EASY":
            n_professors = 4
            self.max_tries = 5
            cols = 4
            rows = 2
        elif difficulty == "MEDIUM":
            n_professors = 6
            self.max_tries = 4
            cols = 4
            rows = 3
        else:
            n_professors = 8
            self.max_tries = 3
            cols = 4
            rows = 4
        all_profs = list(PROFESSORS)
        random.shuffle(all_profs)
        selected_professors = all_profs[:n_professors]

        card_w = 80  
        card_h = 120  
        gap = 30      

        deck = Deck(selected_professors)
        layout = CardLayout(deck.size, card_w, card_h, gap, self.renderer.width, self.renderer.height,cols=cols,rows=rows)
        self.game_state = GameState(pairs_total=n_professors, tries=self.max_tries)
        self.timer = Timer()
        self._first_card_id: int | None = None

        self.cards = [
            Card(
                engine,
                layout.positions[i][0],
                layout.positions[i][1],
                card_w,
                card_h, 
                id=i,
                label=deck.labels[i],
                set_state=self.__set_state,
            )
            for i in range(deck.size)
        ]

    def __set_state(self, card_id: int, label: str):
        if self._first_card_id == card_id:
            return
        result = self.game_state.select(label)
        if result is None:
            self._first_card_id = card_id
            return
        self._first_card_id = None
        if result.matched:
            self.cards = [card for card in self.cards if card.get_label() != result.label]

        if self.game_state.pairs_matched == self.game_state.pairs_total:
            self.show_popup = "WIN"
        elif self.game_state.tries <= 0:
            self.show_popup = "LOSE"

        print(self.game_state.tries)
        print(f"{self.game_state.pairs_matched}/{self.game_state.pairs_total}")
        print(f"tempo: {self.timer.elapsed_seconds():.1f}s")

    def update(self, delta_ms: int) -> None:
        if self.show_popup:
            mouse_pos = pygame.mouse.get_pos()
            popup = self.win_popup if self.show_popup == "WIN" else self.lose_popup
            popup.update(mouse_pos)
            return 
        mouse_pos = pygame.mouse.get_pos()
        self.back_hover = is_clicked(mouse_pos, self.back_rect)
        self.mute_hover = is_clicked(mouse_pos, self.mute_rect)

        self.timer.update(delta_ms)
        for card in self.cards:
            card.update()

    def _render_background(self):
        px_bg = pygame.PixelArray(self.bg_cache)
        
        vertices_fundo = [
            (0, 0, 0, 0),
            (self.renderer.width, 0, self.bg_w, 0),
            (self.renderer.width, self.renderer.height, self.bg_w, self.bg_h),
            (0, self.renderer.height, 0, self.bg_h)
        ]
        
        self.filler.paint_textured_polygon(
            px_bg, 
            self.renderer.width, 
            self.renderer.height, 
            vertices_fundo, 
            self.tex_bg, 
            self.bg_w, 
            self.bg_h
        )
        
        px_bg.close()
        self.bg_rendered = True

    def draw(self, px_array):

        # AAAAAAAAAAAAAAAAAAAAAAAAA

        if not self.bg_rendered:
            self._render_background()
            
        px_cache = pygame.PixelArray(self.bg_cache)
        px_array[:] = px_cache[:] 
        px_cache.close()

        # AAAAAAAAAAAAAAAAAAAAAAAAA

        for card in self.cards:
            card.draw(px_array)
            for rect, hover, tex, tw, th in [
                (self.back_rect, self.back_hover, self.tex_back, self.bw, self.bh),
                (self.mute_rect, self.mute_hover, 
                (self.tex_on if self.engine.menu.sound_on else self.tex_off), 
                self.onw, self.onh)
            ]:
                x, y, w, h = rect
                cor = (117, 230, 216) if hover else (191, 191, 191)
                
                verts = [(x, y), (x+w, y), (x+w, y+h), (x, y+h)]
                self.filler.scanline_fill(px_array, verts, cor)
                
                pad = 5
                verts_tex = [
                    (x + pad, y + pad, 0, 0),
                    (x + w - pad, y + pad, tw, 0),
                    (x + w - pad, y + h - pad, tw, th),
                    (x + pad, y + h - pad, 0, th)
                ]
                self.filler.paint_textured_polygon(
                    px_array, self.renderer.width, self.renderer.height, 
                    verts_tex, tex, tw, th
                )
        if self.show_popup:
            popup = self.win_popup if self.show_popup == "WIN" else self.lose_popup
            popup.draw(px_array)


    def draw_ui(self):
        if self.show_popup:
            popup = self.win_popup if self.show_popup == "WIN" else self.lose_popup
            stats = {
                'tempo': int(self.timer.elapsed_seconds()),
                'vidas': self.game_state.tries,
                'acertos': self.game_state.pairs_matched
            }
            font = pygame.font.SysFont("Jaro", 30)
            popup.draw_labels(self.engine.screen, font, stats)
        else:
            for card in self.cards:
                card.draw_ui()

    def handle_event(self, event):
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                if is_clicked(mouse_pos, self.back_rect):
                    self.engine.audio.play_sfx("click")
                    self.engine.state = "MENU"
                    return 
            
                if is_clicked(mouse_pos, self.mute_rect):
                    self.engine.audio.play_sfx("click")
                    self.engine.menu.sound_on = not self.engine.menu.sound_on
                    self.engine.audio.set_music_volume(0.05 if self.engine.menu.sound_on else 0)
                    return

            if self.show_popup:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    popup = self.win_popup if self.show_popup == "WIN" else self.lose_popup
                    
                    if is_clicked(mouse_pos, popup.btn_retry_rect):
                        self.engine.audio.play_sfx("click")
                        self.engine.game_screen.container = None 
                    elif is_clicked(mouse_pos, popup.btn_menu_rect):
                        self.engine.state = "MENU"
                return 

            for card in self.cards:
                card.handle_event(event)