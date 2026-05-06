from entity import Entity



class Enemy(Entity):
    def __init__(self, name: str = None, hp: int = 100, level: int = 1, attack_power: int = 1):
        super().__init__(name, hp, level, attack_power)

    def heal(self, amount):
        self.hp += amount

