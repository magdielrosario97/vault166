class Player:
    def __init__(self, starting_room):
        self.current_room = starting_room
        self.inventory: set[str] = set()
        self.health = 100

    def take_damage(self, amount: int) -> None:
        self.health -= amount
        if self.health < 0:
            self.health = 0

    def is_alive(self) -> bool:
        return self.health > 0
