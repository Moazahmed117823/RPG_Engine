from abc import ABC , abstractmethod
import random
class Entity(ABC):
    def __init__(self, name: str = None, hp: int = 100, level: int = 1, attack_power: int = 1):
        self.name = name
        self.hp = hp + (level * 1.5)
        self.max_hp = self.hp
        # more level = more hp and attack skills and less damage taken
        self.level = level
        self.attack_power = attack_power
        self.is_defending = False

    def heal(self, amount):
        self.hp = min(self.hp + amount, self.max_hp)

    def take_damage(self, amount: int):
        blocked = False
        if self.is_defending:
            amount = max(1, int(amount * (1 - self.level * 0.05)))
            blocked = True
        self.hp -= amount
        return amount, blocked

    def attack(self, other):
        damage = random.randint(5,20) + self.attack_power
        other.take_damage(damage)
    
    def is_alive(self):
        return self.hp > 0

