from player import Player
from enemy import Enemy 
from combat import CombatManager

p = Player("Player001", 100, 10, 10)
e = Enemy("Villain001", 100, 5, 10)

combat = CombatManager(p, e)
combat.start()
