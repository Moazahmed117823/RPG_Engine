import random
from entity import Entity


class CombatActions:
    def __init__(self, log):
        self._log = log

    def attack(self, attacker: Entity, target: Entity):
        critical_chance = 0.15 + (attacker.level * 0.005)
        if random.random() < critical_chance:
            critical_damage = int(attacker.attack_power * 2)
            self._log("Critical Hit !!")
            target.take_damage(critical_damage)
            self._log(f"[FIGHT] {attacker.name} give {critical_damage} critical damage to {target.name}")
        else:
            attacker.attack(target)

    def defend(self, defender: Entity, attacker: Entity):
        defender.is_defending = True
        self._log(f"{defender.name} Reflect {attacker.name}'s attack")

    def heal(self, entity: Entity, charges: int):
        if charges > 0:
            heal_amount = entity.level * 10
            actual_heal = min(heal_amount, entity.max_hp - entity.hp)
            entity.heal(actual_heal)
            self._log(f"{entity.name} healed for {actual_heal} HP!")
            return charges - 1
        else:
            self._log(f"{entity.name} has no heal charges left!")
            return charges
