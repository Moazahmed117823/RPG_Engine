import time
import random
from player import Player
from enemy import Enemy

class CombatManager:
    def __init__(self, player: Player , enemy: Enemy):
        self.player = player
        self.enemy = enemy
        self.__round_number = 0
        self.__combat_log = []
        self.__is_active = False
        self.__heal_charge = 3

    def log(self, message: str):
        self.__combat_log.append(message)
        print(message)

    def getLog(self):
        return self.__combat_log

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
                return False
            return choice
        except ValueError:
            print("Invalid input")
            return False
        
    def PlayerTurn(self, choice: int):
        """ Attack depend on level and attack power
            Defend more level means taken damage lose 10 %
            heal (level * 10)
            
        """
        self.player.is_defending = False
        if choice == 1:
            critical_chance = 0.15 + (self.player.level * 0.005)
            if random.random() < critical_chance:
                critical_damage = int(self.player.attack_power * 2)
                self.log("Critical Hit !!")
                self.enemy.take_damage(critical_damage)
                self.log(f"[FIGHT] {self.player.name} give {critical_damage} critical damage to {self.enemy.name}")
            else:
                self.player.attack(self.enemy)
        elif choice == 2:
            self.player.is_defending = True
            self.log(f"{self.player.name} Reflect {self.enemy.name}'s attack")
            
        elif choice == 3:
            if self.__heal_charge > 0:
                heal_amount = self.player.level * 10
                actual_heal = min(heal_amount, self.player.max_hp - self.player.hp)
                self.player.heal(actual_heal)
                self.__heal_charge -= 1
                self.log(f"{self.player.name} healed for {actual_heal} HP!")
            else:
                self.log("No heal charges left!")

    def EnemyTurn(self):
        pass
    
    def Start(self):
        pass




