import random
import time
from enemy import Enemy
from player import Player
from combat_actions import CombatActions


class CombatManager:
    def __init__(self, player: Player, enemy: Enemy):
        self.player = player
        self.enemy = enemy
        self.__round_number = 0
        self.__combat_log = []
        self.__is_active = False
        self.__player_heal_charge = 3
        self.__enemy_heal_charge = 3
        self.actions = CombatActions(self.log)

    def log(self, message: str):
        self.__combat_log.append(f"Round {self.__round_number}: {message}")
        print(message)

    def getLog(self):
        print("\n================================= FIGHT HISTORY =================================\n")
        if not self.__combat_log:
            print("No combat log available")
            return []
        else:
            for i,log in enumerate(self.__combat_log):
                print(f"[Step {i+1}] {log}")
            print("\n================================= END of FIGHT ==================================\n")


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
            self.actions.attack(self.player, self.enemy)

        elif choice == 2:
            self.actions.defend(self.player, self.enemy)

        elif choice == 3:
            self.__player_heal_charge = self.actions.heal(self.player, self.__player_heal_charge)

    def EnemyTurn(self):
        choice = random.randint(1,3)
        
        if choice == 1:
            self.actions.attack(self.enemy, self.player)

        elif choice == 2:
            self.actions.defend(self.enemy, self.player)

        elif choice == 3:
            self.__enemy_heal_charge = self.actions.heal(self.enemy, self.__enemy_heal_charge)

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
        self.log(f"\nCombat started between {self.player.name} and {self.enemy.name}\n")

        while self.__is_active:
            self.__round_number += 1
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
