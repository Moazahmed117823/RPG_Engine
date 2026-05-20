import random
import time
import json
import os
import re
from enemy import Enemy
from player import Player
from combat_actions import CombatActions
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

class CombatManager:
    def __init__(self, player: Player, enemy: Enemy, enemy_mode: str = "ai"):
        self.player = player
        self.enemy = enemy
        # Removed double underscores to make state readable by the API
        self.round_number = 0
        self.combat_log = []
        self.is_active = False
        self.player_heal_charge = 3
        self.enemy_heal_charge = 3
        self.actions = CombatActions(self.log)
        self.ai_client = None
        self.enemy_mode = enemy_mode.lower() if enemy_mode.lower() in ("ai", "player") else "ai"

    def log(self, message: str):
        self.combat_log.append(f"Round {self.round_number}: {message}")
        print(message)

    def getLog(self):
        print("\n================================= FIGHT HISTORY =================================\n")
        if not self.combat_log:
            print("No combat log available")
            return []
        else:
            for i, log in enumerate(self.combat_log):
                print(f"[Step {i+1}] {log}")
            print("\n================================= END of FIGHT ==================================\n")

    def __str__(self):
        player_hp = max(0, self.player.hp)
        enemy_hp = max(0, self.enemy.hp)
        return f"\n[ {self.player.name}: {round(player_hp,2)} HP ] - Round ({self.round_number}) - [ {self.enemy.name}: {round(enemy_hp,2)} HP ]\n"

    def __del__(self):
        print("Combat Ended!!")

    def __call__(self):
        self.start()

    def TakePlayerAction(self, actor_name: str, heal_charges: int):
        print(f"\n>>> {actor_name}'s Turn <<<")
        print("What will you do")
        print("1. Attack")
        print("2. Defend")
        print(f"3. Heal ({heal_charges} charges left)")
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
        try:
            if choice == 1:
                self.actions.attack(self.player, self.enemy)
            elif choice == 2:
                self.actions.defend(self.player)
            elif choice == 3:
                self.player_heal_charge = self.actions.heal(self.player, self.player_heal_charge)
        except Exception as e:
            print(f"[ERROR] {e}")

    def EnemyTurn(self):
        self.enemy.is_defending = False
        
        if self.enemy_mode == "player":
            enemy_choice = self.TakePlayerAction(self.enemy.name, self.enemy_heal_charge)
            if not enemy_choice:
                return  
        else:
            enemy_choice = self._ai_pick_choice()
        
        try:
            if enemy_choice == 1:
                self.actions.attack(self.enemy, self.player)
            elif enemy_choice == 2:
                self.actions.defend(self.enemy)
            elif enemy_choice == 3:
                self.enemy_heal_charge = self.actions.heal(self.enemy, self.enemy_heal_charge)
        except Exception as e:
            print(f"[ERROR] {e}")

    def _ai_pick_choice(self):
        # TEMPORARY BYPASS FOR UI TESTING
        # Reconnect your OpenAI logic here once the UI is verified!
        return random.randint(1, 3)

    def check_combat_end(self):
        if not self.player.is_alive():
            self.log(f"\n{self.player.name} has been defeated. Game Over.")
            self.is_active = False
            return True
        if not self.enemy.is_alive():
            self.log(f"\n{self.enemy.name} has been defeated. {self.player.name} is victorious!")
            self.is_active = False
            return True
        return False

    def _ask_for_combat_history(self):
        print("Do you wanna get Combat History? (Y/N)")
        try:
            choice = input("    --> ")
            if choice.upper() == "Y":
                self.getLog()
        except Exception as e:
            print(f"[ERROR] {e}")

    def start(self):
        self.is_active = True
        mode_display = "AI" if self.enemy_mode == "ai" else "PLAYER"
        self.log(f"\nCombat started between {self.player.name} and {self.enemy.name}")
        self.log(f"Enemy Mode: {mode_display}-CONTROLLED\n")

        while self.is_active:
            self.round_number += 1
            print(self)

            player_choice = self.TakePlayerAction(self.player.name, self.player_heal_charge)
            if not player_choice:
                self.EnemyTurn()
                if self.check_combat_end():
                    self._ask_for_combat_history()
                    break
                continue

            self.PlayerTurn(player_choice)
            if self.check_combat_end():
                self._ask_for_combat_history()
                break

            time.sleep(1)

            self.EnemyTurn()
            if self.check_combat_end():
                self._ask_for_combat_history()
                break