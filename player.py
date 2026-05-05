from entity import Entity
import random

class Player(Entity):
    def __init__(self, name: str = None, hp: int = 100, level: int = 1, attack_power: int = 1):
        super().__init__(name, hp, level, attack_power)
        self.inventory = []

    def heal(self, amount):
        self.hp += amount
        print(f"{self.name} healed for {amount} hp")
        
    def attack(self, player):
        damage = random.randint(5,20) * self.level
        player.take_damage(damage)
        print(f"{self.name} attacked {player.name} for {damage} damage")