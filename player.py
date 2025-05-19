# create a Player class to keep track of player position and information
class Player:
    def __init__(self, starting_room):
        self.current_room = starting_room
        self.inventory = []

    # try to move in a direction
    def move(self, direction):
        # if room exists in direction
        if direction in self.current_room.connections:
            # set room to check connections
            next_room = self.current_room.connections[direction]
            
            # if next room is locked
            if next_room.is_locked:
                # prevent movement
                print("This room is locked.")
                return
            
            # Check hazard protection (optional danger logic)
            if next_room.hazard_item:
                missing_protection = [item for item in next_room.hazard_item if item not in self.inventory]
                if missing_protection:
                    print(f"You enter {next_room.name}... but you’re not fully protected!")
                    print(f"You are missing: {', '.join(missing_protection)}")
                    print("\033[91mYou were exposed to radiation and died.\033[0m")
                    # End game
                    exit()
            
            # Move player to next room
            self.current_room = next_room
            print(f"You have moved to {self.current_room.name}")
        else:
            # Alert player
            print("\033[91mYou can't go that way!\033[0m")

    # # adds item to player inventory
    # def add_item(self, item):
    #     self.inventory.append(item)

    # # checks if player has item
    # def has_item(self):
    #     return item in self.inventory

    # # check if player has all items
    # def has_all_items(self):
    #     return len(self.inventory) == 7