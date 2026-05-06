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
            heal (level * 25)
            
        """
        pass

    def EnemyTurn(self):
        pass


    def Start(self):
        pass











