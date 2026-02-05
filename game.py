from player import Player
from map import build_map

BOSS_ITEMS = {
    "radzapper",
    "mask",
    "hazmat_suit",
    "fusion_core",
    "id_tag",
}


class Game:
    def __init__(self):
        self.game_over = False
        self.rooms = build_map()
        self.player = Player(self.rooms["Vault Entrance"])

    def _handle_move(self, direction: str) -> None:
        current_room = self.player.current_room

        # Valid move
        if direction in current_room.connections:
            self.player.current_room = current_room.connections[direction]
            current_room = self.player.current_room
            self._handle_boss(current_room)
        else:
            print("\033[91mYou can't go that way!\033[0m")
            self._print_hint(current_room)

    def _handle_get(self, item: str) -> None:
        current_room = self.player.current_room

        if current_room.item == item:
            self.player.inventory.add(item)
            print("You picked up the\033[94m", item + "\033[0m.")
            current_room.item = None
        else:
            print("\033[91mThere is no item in the room.\033[0m")

    def _handle_boss(self, room) -> None:
        if room.name != "Research & Development":
            return

        print(room.description)

        # TODO: Temporary boss check. Rework with hazard system.
        missing = BOSS_ITEMS - self.player.inventory
        if not missing:
            print("\033[93mCongratulations! You encountered and defeated Maradonyx.")
            print("You win!\033[0m")
        else:
            print(
                "\033[91mYou encountered Maradonyx before collecting the required items."
            )
            print("Game over!\033[0m")

        self.game_over = True

    def _print_hint(self, room) -> None:
        # TODO: Temporary bridge. Rework hint logic.
        pretty = {d: r.name for d, r in room.connections.items()}
        print(f"HINT: {pretty}")

    def process_command(self, command: str) -> None:
        # Movement
        if command.startswith("go "):
            direction = command[3:]
            self._handle_move(direction)
        # Item collection
        elif command.startswith("get "):
            item = command[4:]
            self._handle_get(item)
        else:
            print("\033[91mInvalid command!\033[0m")

    def run(self):
        while not self.game_over:
            # Display current room description
            print(f"\033[92mYou moved to {self.player.current_room.name}\033[0m")
            print(self.player.current_room.description)
            # Display player's inventory
            print("Inventory:", list(self.player.inventory))
            # Check if the current room contains an item
            current_room = self.player.current_room
            if current_room.item is not None:
                print(f"You see a \033[94m{current_room.item}\033[0m in the room.")
            # Player input
            print("-----------------------------------------------------------------")
            command = input("Enter your command: ")
            print("-----------------------------------------------------------------")
            self.process_command(command)
