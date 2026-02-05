from player import Player
from map import build_map
from rules import (
    blocked_by_darkness,
    blocked_by_lock,
    boss_room,
    has_boss_items,
    hazard_damage,
    DAMAGE,
)


class Game:
    def __init__(self):
        self.game_over = False
        self.rooms = build_map()
        self.player = Player(self.rooms["Vault Entrance"])

    def _handle_move(self, direction: str) -> None:
        current_room = self.player.current_room

        # Invalid move
        if direction not in current_room.connections:
            print("\033[91mYou can't go that way!\033[0m")
            self._print_hint(current_room)
            return

        next_room = current_room.connections[direction]

        # Darkness blocks and also hurts
        if blocked_by_darkness(self.player, next_room):
            self.player.take_damage(DAMAGE)
            print("\033[91mIt is too dark. You trip and fall.\033[0m")
            print(f"\033[91m-{DAMAGE} health\033[0m")
            if not self.player.is_alive():
                print("\033[91mYou collapsed. Game over!\033[0m")
                self.game_over = True
            return

        # Locks block entry
        if blocked_by_lock(self.player, next_room):
            print("\033[91mThe door is locked. You need a keycard.\033[0m")
            return

        # Move into the room
        self.player.current_room = next_room
        current_room = self.player.current_room

        # Boss room check
        if boss_room(current_room):
            print(current_room.description)
            if has_boss_items(self.player):
                print(
                    "\033[93mCongratulations! You encountered and defeated Maradonyx.\033[0m"
                )
                print("You win!\033[0m")
            else:
                print("\033[91mYou encountered Maradonyx unprepared. Game over!\033[0m")
            self.game_over = True
            return

        # Environmental hazards
        damage = hazard_damage(self.player, current_room)
        if damage:
            self.player.take_damage(damage)
            print("\033[91mThe environment harms you.\033[0m")
            print(f"\033[91m-{damage} health\033[0m")
            if not self.player.is_alive():
                print("\033[91mYou collapsed. Game over!\033[0m")
                self.game_over = True
                return

    def _handle_get(self, item: str) -> None:
        current_room = self.player.current_room

        if current_room.item == item:
            self.player.inventory.add(item)
            print("You picked up the\033[94m", item + "\033[0m.")
            current_room.item = None
        else:
            print("\033[91mThere is no item in the room.\033[0m")

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
            print("Health:", self.player.health)
            # Check if the current room contains an item
            current_room = self.player.current_room
            if current_room.item is not None:
                print(f"You see a \033[94m{current_room.item}\033[0m in the room.")
            # Player input
            print("-----------------------------------------------------------------")
            command = input("Enter your command: ")
            print("-----------------------------------------------------------------")
            self.process_command(command)
