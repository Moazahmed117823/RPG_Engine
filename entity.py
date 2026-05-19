import random
from abc import ABC, abstractmethod

class Entity(ABC):
    def __init__(self, name: str = None, hp: int = 100, level: int = 1, attack_power: int = 1, dodge_rate: float = 0.1):
        self.name = name
        self.hp = int(hp + (level * 1.5))
        self.max_hp = self.hp
        # More level = more HP, attack skills, and less damage taken
        self.level = level
        self.attack_power = attack_power
        self.is_defending = False
        self.dodge_rate = dodge_rate

    def heal(self, amount: int):
        self.hp = min(self.hp + amount, self.max_hp)

    def take_damage(self, amount: int):
        dodged = False
        blocked = False
        if random.random() < self.dodge_rate:
            dodged = True
            amount = 0
            print(f"{self.name} dodged the attack!")
        else:
            if self.is_defending:
                damage_reduction = 0.50 + (self.level * 0.02)
                damage_reduction = min(0.90, damage_reduction) 
                amount = max(1, int(amount * (1 - damage_reduction)))
                blocked = True
                print(f"{self.name} blocks the attack!")

        self.hp -= amount
        return amount, blocked, dodged
    
    def attack(self, other):
        damage = random.randint(5, 20) + self.attack_power
        actual_damage, blocked, dodged = other.take_damage(damage)
        if not dodged:
            print(f"{self.name} attacked {other.name} for {round(actual_damage,2)} damage")

    def is_alive(self):
        return self.hp > 0