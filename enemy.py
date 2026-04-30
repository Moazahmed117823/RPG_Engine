from entity import Entity
import random 


class Enemy(Entity):
    def __init__(self, name, hp, attack,level):
        super().__init__(name, hp, attack,level)
    
    def attack_player(self, player):
        damage = random.randint(5,20) * self.level
        player.take_damage(damage)



