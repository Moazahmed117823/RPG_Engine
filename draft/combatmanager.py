import random
import time
from enemy import Enemy
from player import Player
from entity import Entity

class CombatManager:
    def __init__(self, player: Player, enemy: Enemy):
        self.player = player
        self.enemy = enemy
        self.__round_number = 0
        self.__combat_log = []
        self.__is_active = False
        self.__player_heal_charge = 3
        self.__enemy_heal_charge = 3

    def log(self, message: str):
        self.__combat_log.append(message)
        print(message)

    def getLog(self):
        header = "\n================================= FIGHT HISTORY ================================="
        footer = "================================= END of FIGHT =================================="
        f_logs = "\n".join(self.__combat_log)
        logs_output = f"{header}\n{f_logs}\n{footer}"
        print(logs_output)
        return self.__combat_log

 
    def __str__(self):
        player_hp = max(0, self.player.hp)
        enemy_hp = max(0, self.enemy.hp)
        return f"\n[ {self.player.name}: {player_hp} HP ] - Round ({self.__round_number}) - [ {self.enemy.name}: {enemy_hp} HP ]\n"

    def __del__(self):
        print("Combat Ended!!")

    def __call__(self):
        self.start()
        
    def TakePlayerAction(self):
        print("What will you do")
        print("1. Attack")
        print("2. Defend")
        print(f"3. Heal ({self.__player_heal_charge} charges left)")
        try:
            print("Enter choice (1-3): ")
            choice = int(input("    --> "))
            if not choice:
                print("Miss your chance!")
                return False
            if choice not in (1, 2, 3):
                print("Invalid choice")
                return False
            return choice
        except Exception as e:
            print(f"[ERROR] {e}")
            return False

    def PlayerTurn(self, choice: int):
        self.player.is_defending = False
        if choice == 1:
            self.attack(self.player, self.enemy)

        elif choice == 2:
            self.defend(self.player, self.enemy)

        elif choice == 3:
            self.heal(self.player)

    def EnemyTurn(self):
        choice = random.randint(1,3)
        
        if choice == 1:
            self.attack(self.enemy, self.player)

        elif choice == 2:
            self.defend(self.enemy, self.player)

        elif choice == 3:
            self.heal(self.enemy)

    def check_combat_end(self):
        if not self.player.is_alive():
            self.log(f"\n{self.player.name} has been defeated. Game Over.")
            self.__is_active = False
            return True
        if not self.enemy.is_alive():
            self.log(f"\n{self.player.name} is victorious!")
            self.__is_active = False
            return True
        return False

    def start(self):
        self.__is_active = True
        self.log(f"\nCombat started between {self.player.name} and {self.enemy.name}")
        #self.log(f"{self.player.hp} HP  ---  {self.enemy.hp} HP\n")

        while self.__is_active:
            self.__round_number += 1
            #self.log(f"\n--- Round {self.__round_number} ---")
            print(self)

            player_choice = self.TakePlayerAction()
            if not player_choice:
                self.EnemyTurn()
                continue

            self.PlayerTurn(player_choice)
            if self.check_combat_end():
                print("Do you wanna get Combat History? (Y/N)")
                try:
                    choice = input("    --> ")
                    if choice.upper() == "Y":
                        self.getLog()
                    else:
                        break
                except Exception as e:
                    print(f"[ERROR] {e}")
                break

            time.sleep(1)

            self.EnemyTurn()
            if self.check_combat_end():
                print("Do you wanna get Combat History? (Y/N)")
                try:
                    choice = input("    --> ")
                    if choice.upper() == "Y":
                        self.getLog()
                    else:
                        break
                except Exception as e:
                    print(f"[ERROR] {e}")
                break