class Entity:
    def __init__(self, name, hp, level, attack):
        self.name = name
        self.hp = hp
        # more level = more hp and attack skills and less damage taken
        self.level = level
        self.attack = attack

    def take_damage(self, amount):
        self.hp -= amount

    def is_alive(self):
        return self.hp > 0


class Player(Entity):
    def __init__(self, name):
        super().__init__(name, hp=100, level=0, attack=1)
        self.inventory = []

    def heal(self, amount):
        self.hp += amount
