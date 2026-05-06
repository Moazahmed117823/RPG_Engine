from entity import Entity

class Player(Entity):
    def __init__(self, name: str = None, hp: int = 100, level: int = 1, attack_power: int = 1):
        super().__init__(name, hp, level, attack_power)
        self.inventory = []

    def heal(self, amount):
        self.hp += amount