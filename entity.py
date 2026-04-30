from abc import ABS , abstractmethod

class Entity():
    def __init__(self, name: str, hp: int, level: int, attack: int):
        self.name = name
        self.hp = hp
        # more level = more hp and attack skills and less damage taken
        self.level = level
        self.attack = attack

    def take_damage(self, amount):
        self.hp -= amount

    def is_alive(self):
        return self.hp > 0
