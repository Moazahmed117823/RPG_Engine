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
    def __init__(self, player: Player, enemy: Enemy):
        self.player = player
        self.enemy = enemy
        self.__round_number = 0
        self.__combat_log = []
        self.__is_active = False
        self.__player_heal_charge = 3
        self.__enemy_heal_charge = 3
        self.actions = CombatActions(self.log)
        self.__ai_client = None

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
        try:
            if choice == 1:
                self.actions.attack(self.player, self.enemy)

            elif choice == 2:
                self.actions.defend(self.player)

            elif choice == 3:
                self.__player_heal_charge = self.actions.heal(self.player, self.__player_heal_charge)
        except Exception as e:
            print(f"[ERROR] {e}")

    def EnemyTurn(self):
        self.enemy.is_defending = False
        enemy_choice = self.__ai_pick_choice()
        try:
            if enemy_choice == 1:
                self.actions.attack(self.enemy, self.player)

            elif enemy_choice == 2:
                self.actions.defend(self.enemy)

            elif enemy_choice == 3:
                self.__enemy_heal_charge = self.actions.heal(self.enemy, self.__enemy_heal_charge)

        except Exception as e:
            print(f"[ERROR] {e}")

        def __ai_pick_choice(self):
            try:
                if self.__ai_client is None:
                    api_key = os.environ.get("OPENROUTER_API_KEY")
                    if not api_key:
                        raise RuntimeError("OPENROUTER_API_KEY not set")
                    self.__ai_client = OpenAI(base_url="https://openrouter.ai/api/v1",api_key=api_key,)

                stats = {
                    "enemy_name": self.enemy.name,
                    "enemy_hp": self.enemy.hp,
                    "enemy_max_hp": self.enemy.max_hp,
                    "enemy_level": self.enemy.level,
                    "enemy_attack_power": self.enemy.attack_power,
                    "heal_charges": self.__enemy_heal_charge,
                    "player_name": self.player.name,
                    "player_hp": self.player.hp,
                    "player_max_hp": self.player.max_hp,
                    "player_level": self.player.level,
                }

                prompt = (
                    "You are an aggressive, ruthless combat AI for a turn-based RPG. "
                    "Given the current combat state, choose the enemy's next action. "
                    "Return ONLY a single digit: 1, 2, or 3. No explanation, no formatting.\n\n"
                    "RULES:\n"
                    "- You prefer to Attack (1) to crush the player.\n"
                    "- ONLY Heal (3) if your HP falls below 40% of your max HP.\n"
                    "- You may Defend (2) if your HP is getting low and you have no heals left.\n\n"
                    f"Combat state:\n{json.dumps(stats, indent=2)}\n\n"
                    "Your choice (1/2/3):"
                )

                response = self.__ai_client.chat.completions.create(
                    model="qwen/qwen-2.5-7b-instruct",
                    messages=[
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.2,
                    max_tokens=5,
                )

                text = response.choices[0].message.content.strip()
                match = re.search(r"[123]", text)
                if not match:
                    return random.randint(1, 3)

                enemy_choice = int(match.group())

                if enemy_choice == 3 and (self.__enemy_heal_charge <= 0 or self.enemy.hp >= self.enemy.max_hp):
                    enemy_choice = 1

                return enemy_choice

            except Exception as e:
                print(f"[AI Fallback] {e}")
                return random.randint(1, 3)

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
