from player import Player
from map import build_map


class Game:
    def __init__(self):
        self.game_over = False
        self.rooms, self.room_connections, self.items = build_map()
        self.player = Player(self.rooms["Vault Entrance"])

    def process_command(self, command: str) -> None:
        current_room = self.player.current_room

        # Process player's command
        if command.startswith("go "):
            direction = command[3:]
            if direction in current_room.connections:
                self.player.current_room = current_room.connections[direction]
                current_room = self.player.current_room
                # Check if the player encounters Maradonyx
                if current_room.name == "Research & Development":
                    print(current_room.description)
                    if len(self.player.inventory) == 7:
                        print(
                            "\033[93mCongratulations! You collected all the items and defeated Maradonyx."
                        )
                        print("You win!\033[0m")
                        self.game_over = True
                    else:
                        print(
                            "\033[91mYou encountered Maradonyx before collecting all the items."
                        )
                        print("Game over!\033[0m")
                        self.game_over = True
            else:
                print("\033[91mYou can't go that way!\033[0m")
                # TODO: Temporary bridge. Rework hint logic.
                pretty = {d: r.name for d, r in current_room.connections.items()}
                print(f"HINT: {pretty}")
        elif command.startswith("get "):
            item = command[4:]
            if self.items[current_room.name] == item:
                self.player.inventory.append(item)
                print("You picked up the\033[94m", item + "\033[0m.")
                self.items[current_room.name] = None
            else:
                print("\033[91mThere is no item in the room.\033[0m")
        else:
            print("\033[91mInvalid command!\033[0m")

    def run(self):
        while not self.game_over:
            # Display current room description
            print(f"\033[92mYou moved to {self.player.current_room.name}\033[0m")
            print(self.player.current_room.description)
            # Display player's inventory
            print("Inventory:", self.player.inventory)
            # Check if the current room contains an item
            room_name = self.player.current_room.name
            if self.items[room_name] is not None:
                print(f"You see a \033[94m{self.items[room_name]}\033[0m in the room.")
            # Player input
            print("-----------------------------------------------------------------")
            command = input("Enter your command: ")
            print("-----------------------------------------------------------------")
            self.process_command(command)
