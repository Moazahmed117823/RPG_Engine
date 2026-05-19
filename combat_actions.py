import random

from entity import Entity


class CombatActions:
    def __init__(self, log):
        self._log = log

    def attack(self, attacker: Entity, target: Entity):
        base_damage = random.randint(5,20) + attacker.attack_power
        critical_chance = 0.15 + (attacker.level * 0.005)
        if random.random() < critical_chance:
            damage = int(base_damage * 2)
            self._log("Critical Hit !!")
        else:
            damage = base_damage
        actual_damage, blocked, dodged = target.take_damage(damage)
        if dodged:
            self._log(f"{target.name} dodged the attack!")
        else:
            if blocked:
                self._log(f"{target.name} deflect the attack!")
            self._log(
                f"[FIGHT] {attacker.name} dealt {(round(actual_damage,2))} damage to {target.name}"
            )

    def defend(self, defender: Entity):
        defender.is_defending = True
        self._log(f"{defender.name} takes a defensive stance!")

    def heal(self, entity: Entity, charges: int):
        if charges > 0:
            if entity.hp >= entity.max_hp:
                self._log(f"{entity.name} is already at full HP!")
                return charges
            heal_amount = entity.level * 10
            actual_heal = min(heal_amount, entity.max_hp - entity.hp)
            entity.heal(actual_heal)
            self._log(f"{entity.name} healed for {actual_heal} HP!")
            return charges - 1
        else:
            self._log(f"{entity.name} has no heal charges left!")
            return charges
