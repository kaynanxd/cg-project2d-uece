import random
from src.game.card import Card

class CardContainer:
    def __init__(self, engine):
        self.engine = engine
        self.renderer = engine.renderer
        self.filler = engine.filler
        
        self.tries = 3
        
        self.choice_1 = None
        self.choice_2 = None
        
        gap = 50
        card_w, card_h = 50, 100

        self.labels = {}
        
        professors_base = ["Everardo", "Matheus Cientista", "Ana Luiza", "Claudia Rebouças"]
        professors = []
        for i in range(0, len(professors_base)):
            professors.append(professors_base[i])
            professors.append(professors_base[i])
            
        n_cards = len(professors)
        for i in range(n_cards):
            choice = random.choice(professors)
            professors.remove(choice)
            self.labels[i] = choice

        total_w = n_cards * card_w + (n_cards - 1) * gap
        start_x = (self.renderer.width - total_w) // 2
        start_y = (self.renderer.height - card_h) // 2
        
        self.cards = [
            Card(engine, start_x + i * (card_w + gap), start_y, id=i, label=self.labels[i], set_state=self.__set_state)
            for i in range(n_cards)
        ]
    
    def __set_state(self, label):
        if not self.choice_1:
            self.choice_1 = label
        else:
            self.choice_2 = label
            
            if self.choice_1 == self.choice_2:
                matched_pair = self.choice_1
                self.cards = [card for card in self.cards if card.get_label() != matched_pair]
            else:
                print(self.tries)
                self.tries -= 1
                
            self.choice_1 = None
            self.choice_2 = None
        
    
    def update(self):
        for card in self.cards:
            card.update()
            
    def draw(self, px_array):
        for card in self.cards:
            card.draw(px_array)
    
    def draw_ui(self):
        for card in self.cards:
            card.draw_ui()
    
    def handle_event(self, event):
        for card in self.cards:
            card.handle_event(event)
            
