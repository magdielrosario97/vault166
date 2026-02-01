from player import Player
from map import build_map

class Game:
    def __init__(self):
        self.game_over = False
        self.player = Player("Vacuum Room")
        self.rooms, self.room_connections, self.items = build_map()

    def run(self):
            while not self.game_over:
                # Display current room description
                print(f'\033[92mYou moved to {self.player.current_room}\033[0m')
                print(self.rooms[self.player.current_room])
                # Display player's inventory
                print("Inventory:", self.player.inventory)

                # Check if the current room contains an item
                if self.items[self.player.current_room] is not None:
                    print(f"You see a \033[94m{self.items[self.player.current_room]}\033[0m in the room.")

                # Player input
                print('-----------------------------------------------------------------')
                command = input("Enter your command: ")
                print('-----------------------------------------------------------------')
                # Process player's command
                if command.startswith("go "):
                    direction = command[3:]
                    if direction in self.room_connections[self.player.current_room]:
                        self.player.current_room = self.room_connections[self.player.current_room][direction]
                        # Check if the player encounters Maradonyx
                        if self.player.current_room == "Chemical Room":
                            print(self.rooms[self.player.current_room])
                            if len(self.player.inventory) == 7 and self.player.current_room == 'Chemical Room':
                                print("\033[93mCongratulations! You collected all the items and defeated Maradonyx.")
                                print("You win!\033[0m")
                                self.game_over = True
                            else:
                                print("\033[91mYou encountered Maradonyx before collecting all the items.")
                                print("Game over!\033[0m")
                                self.game_over = True
                    else:
                        print("\033[91mYou can't go that way!\033[0m")
                        print(f'HINT: {self.room_connections[self.player.current_room]}')
                elif command.startswith("get "):
                    item = command[4:]
                    if self.items[self.player.current_room] == item:
                        self.player.inventory.append(item)
                        print("You picked up the\033[94m", item + "\033[0m.")
                        self.items[self.player.current_room] = None
                    else:
                        print("\033[91mThere is no item in the room.\033[0m")
                else:
                    print("\033[91mInvalid command!\033[0m")
            