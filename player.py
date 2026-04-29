from entity import Entity


class Player(Entity):
    def __init__(self, name):
        super().__init__(name, hp=100, level=0, attack=1)
        self.inventory = []

    def heal(self, amount):
        self.hp += amount
