from player import Player
from enemy import Enemy
from combat_manager import CombatManager


def main():
    try:
        player_name = input("Enter your player name: ").strip() or "Player001"
        enemy_name = input("Enter enemy name: ").strip() or "Villain001"
        game_mode = input("Choose enemy type (AI/Player): ").strip().lower()
        if game_mode not in ("ai", "player"):
            print("Invalid choice, defaulting to AI enemy.")
            game_mode = "ai"
    except Exception as e:
        print(f"Invalid input, {e}. Defaulting to AI.")
        player_name = "Player001"
        enemy_name = "Villain001"
        game_mode = "ai"

    player = Player(player_name, 100, 10, 10)
    enemy = Enemy(enemy_name, 100, 5, 5)

    combat = CombatManager(player=player, enemy=enemy, enemy_mode=game_mode)
    combat()

if __name__ == "__main__":
    main()