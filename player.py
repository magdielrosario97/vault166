class Player:
    def __init__(self):
        self.current_room = "Vacuum Room"
        self.inventory = []
        self.health = 100

    def add_item(self, item):
        self.inventory.append(item)

    def has_item(self):
        return item in self.inventory

    def has_all_items(self):
        return len(self.inventory) == 7