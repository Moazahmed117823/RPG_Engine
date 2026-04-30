from abc import ABC , abstractmethod

class Entity(ABC):
    def __init__(self, name: str = None, hp: int = 100, level: int = 1, attack_power: int = 1):
        self.name = name
        self.hp = hp + (level * 1.5)
        # more level = more hp and attack skills and less damage taken
        self.level = level
        self.attack_power = attack_power

    def take_damage(self, amount: int):
        self.hp -= amount

    def is_alive(self):
        return self.hp > 0