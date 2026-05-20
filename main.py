# IMPORT FASTAPI AND DATA VALIDATION
from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel
import uvicorn

# IMPORT YOUR EXISTING GAME LOGIC
from player import Player
from enemy import Enemy
from combat_manager import CombatManager

# INITIALIZE THE FASTAPI APPLICATION
app = FastAPI(title="RPG Combat Engine API")

# INITIALIZE THE GAME STATE IN MEMORY
current_player = Player("Player001", 100, 10, 10)
current_enemy = Enemy("Villain001", 100, 5, 5)
game_session = CombatManager(current_player, current_enemy, "ai")

# DEFENSIVE HELPER: BYPASS PYTHON NAME MANGLING
# This searches the object for a variable regardless of whether it is public or private
def get_var(obj, var_name, default_value):
    class_name = obj.__class__.__name__
    possible_names = [var_name, f"_{var_name}", f"_{class_name}__{var_name}"]
    
    for name in possible_names:
        if hasattr(obj, name):
            return getattr(obj, name)
    return default_value

# MANUALLY ACTIVATE THE SESSION SAFELY
if hasattr(game_session, '_CombatManager__is_active'):
    game_session._CombatManager__is_active = True
elif hasattr(game_session, 'is_active'):
    game_session.is_active = True

# DEFINE THE EXPECTED JSON PAYLOAD
class ActionModel(BaseModel):
    choice: int

@app.get("/")
async def serve_frontend():
    return FileResponse("frontend/index.html")

@app.post("/action")
async def process_turn(action: ActionModel):
    
    # 1. SAFELY GET PREVIOUS LOG LENGTH
    combat_log = get_var(game_session, "combat_log", [])
    previous_log_count = len(combat_log)

    # 2. EXECUTE PLAYER ACTION
    game_session.PlayerTurn(action.choice)
    
    # 3. CHECK DEATH & ENEMY TURN
    if not game_session.check_combat_end():
        game_session.EnemyTurn()
        game_session.check_combat_end()
    
    # 4. EXTRACT ONLY THE NEW LOGS
    combat_log = get_var(game_session, "combat_log", [])
    new_logs = combat_log[previous_log_count:]

    # 5. SAFELY GET UI STATS
    heal_charges = get_var(game_session, "player_heal_charge", 3)
    is_active = get_var(game_session, "is_active", True)

    # 6. RETURN STATE TO JAVASCRIPT
    return {
        "player": {
            "hp": game_session.player.hp,
            "max_hp": game_session.player.max_hp,
            "heal_charges": heal_charges
        },
        "enemy": {
            "hp": game_session.enemy.hp,
            "max_hp": game_session.enemy.max_hp
        },
        "logs": new_logs,
        "game_over": not is_active
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)