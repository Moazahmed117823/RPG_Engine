from entity import Entity
import random 


class Enemy(Entity):
    def __init__(self, name: str = None, hp: int = 100, level: int = 1, attack_power: int = 1):
        super().__init__(name, hp, level, attack_power)
    
    def attack(self, player):
        damage = random.randint(5,20) * self.level
        player.take_damage(damage)



