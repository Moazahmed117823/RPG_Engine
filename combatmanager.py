import random
import time
from enemy import Enemy
from player import Player

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
        print("\n================================= FIGHT HISTORY =================================")
        for log in self.__combat_log:
            print(f" {log}\n")
        print("\n================================= END of FIGHT ==================================")

 
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
            if choice not in (1, 2, 3, None):
                print("Invalid choice")
                return False
            return choice
        except Exception as e:
            print(f"[ERROR] {e}")
            return False

    def PlayerTurn(self, choice: int):
        self.player.is_defending = False
        if choice == 1:
            critical_chance = 0.15 + (self.player.level * 0.005)
            if random.random() < critical_chance:
                critical_damage = int(self.player.attack_power * 2)
                self.log("Critical Hit !!")
                self.enemy.take_damage(critical_damage)
                self.log(
                    f"[FIGHT] {self.player.name} give {critical_damage} critical damage to {self.enemy.name}"
                )
            else:
                self.player.attack(self.enemy)

        elif choice == 2:
            self.player.is_defending = True
            self.log(f"{self.player.name} Reflect {self.enemy.name}'s attack")

        elif choice == 3:
            if self.__player_heal_charge > 0:
                heal_amount = self.player.level * 10
                actual_heal = min(heal_amount, self.player.max_hp - self.player.hp)
                self.player.heal(actual_heal)
                self.__player_heal_charge -= 1
                self.log(f"{self.player.name} healed for {actual_heal} HP!")
            else:
                self.log("No heal charges left!")

    def EnemyTurn(self):
        self.enemy.is_defending = False
        choice = random.randint(1, 3)
        if choice == 1:
            critical_chance = 0.15 + (self.enemy.level * 0.005)
            if random.random() < critical_chance:
                critical_damage = int(self.enemy.attack_power * 2)
                self.log("Critical Hit !!")
                self.player.take_damage(critical_damage)
                self.log(
                    f"[FIGHT] {self.enemy.name} gives {critical_damage} critical damage to {self.player.name}"
                )
            else:
                self.enemy.attack(self.player)

        elif choice == 2:
            self.enemy.is_defending = True
            self.log(f"{self.enemy.name} Reflect {self.player.name}'s attack")

        elif choice == 3:
            if self.__enemy_heal_charge > 0:
                heal_amount = self.enemy.level * 10
                actual_heal = min(heal_amount, self.enemy.max_hp - self.enemy.hp)
                self.enemy.heal(actual_heal)
                self.__enemy_heal_charge -= 1
                self.log(f"{self.enemy.name} healed for {actual_heal} HP!")
            else:
                self.log(f"{self.enemy.name} has no heal charges left!")

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