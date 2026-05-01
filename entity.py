from abc import ABC , abstractmethod

class Entity(ABC):
    def __init__(self, name: str = None, hp: int = 100, level: int = 1, attack_power: int = 1):
        self.name = name
        self.hp = hp + (level * 1.5)
        # more level = more hp and attack skills and less damage taken
        self.level = level
        self.attack_power = attack_power
        self.is_defending = False

    def take_damage(self, amount: int):
        if self.is_defending:
            amount //= 2
            print(f"{self.name} blocks the attack!")
        self.hp -= amount

    def attack(self, victum):
        victum.take_damage(self.attack_power)
        print(f"{self.name} attacked {victum.name} for {self.attack_power} damage")
    
    def is_alive(self):
        return self.hp > 0
    
    