import random

class Deck:
    def __init__(self, items: list[str]):
        doubled = items + items
        random.shuffle(doubled)
        self.labels = {i: label for i, label in enumerate(doubled)}
        self.size = len(doubled)
