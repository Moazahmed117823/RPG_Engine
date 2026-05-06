import time
import random
from player import Player
from enemy import Enemy


class CombatManager:
    def __init__(self, player: Player , enemy: Enemy):
        self.player = player
        self.enemy = enemy
        self.round_number = 0
        self.combat_log = []
        self.is_active = False


    def log(self, message: str):
        self.combat_log.append(message)
        print(message)


    def TakePlayerAction(self):
        print("What will you do")
        print("1. Attack")
        print("2. Defend")
        print("3. Heal")
        try:
            print("Enter choice (1-3): ")
            choice = int(input("    -->"))
            if choice not in (1,2,3):
                print("Invalid choice")
                return -1
            return choice
        except ValueError:
            print("Invalid input")
            return -1


    def PlayerTurn(self, choice: int):
        pass


    