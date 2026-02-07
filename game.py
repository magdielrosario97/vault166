from player import Player
from map import build_map, print_map
from input_parser import InputParser
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

        valid_items = {room.item for room in self.rooms.values() if room.item}
        self.parser = InputParser(valid_items, 2)

    def _handle_move(self, direction: str) -> None:
        current_room = self.player.current_room

        # Invalid move
        if direction not in current_room.connections:
            print("\033[91mYou can't go that way!\033[0m")
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
            if next_room.name == "Armory":
                print(
                    "\033[91mThe Armory lock is seized. Maybe something can melt it.\033[0m"
                )
            else:
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
                    "\033[93mCongratulations! You encountered and defeated Maradonyx."
                )
                print(
                    "With the threat neutralized, you recover the schematics and make your way out of Vault 166."
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

    def process_command(self, command: str) -> None:
        action, value = self.parser.parse(command)

        if action == "move":
            self._handle_move(value)
        elif action == "get":
            self._handle_get(value)
        elif action == "map":
            print_map()
        elif action == "help":
            print("Commands: go <direction>, get <item>, map, help, exit/quit")
        elif action == "exit":
            print("Exiting game... Thanks for playing Vault 166!")
            self.game_over = True
        else:
            print(f"\033[91m{value}\033[0m")

    def run(self):
        while not self.game_over:
            current_room = self.player.current_room
            # Display current room description
            print(f"\033[92mYou moved to {current_room.name}\033[0m")
            print(current_room.description)
            if current_room.note and not current_room.read_note:
                print(current_room.note)
                current_room.read_note = True
            # Display player's inventory
            print("Inventory:", list(self.player.inventory))
            print("Health:", self.player.health)
            # Check if the current room contains an item
            if current_room.item is not None:
                print(f"You see a \033[94m{current_room.item}\033[0m in the room.")
            # Player input
            print("-----------------------------------------------------------------")
            command = input("Enter your command: ")
            print("-----------------------------------------------------------------")
            self.process_command(command)
