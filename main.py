from player import Player
from enemy import Enemy 

# Test Attack
p = Player("Player001", 100, 10, 10)
e = Enemy("Villain001", 100, 5, 10)
p.attack(e)
e.attack(p)
print(e.hp)
print(p.hp)


