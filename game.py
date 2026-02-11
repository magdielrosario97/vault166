from utils import separator, GREEN, BLUE, RED, YELLOW, RESET
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
    """Main game class that manages the game state, player, and game loop."""

    def __init__(self):
        self.game_over = False
        self.rooms = build_map()
        self.player = Player(self.rooms["Vault Entrance"])

        valid_items = {room.item for room in self.rooms.values() if room.item}
        self.parser = InputParser(valid_items, 2)

    def _handle_move(self, direction: str) -> None:
        """Handles player movement in the given direction, applying game rules and consequences."""
        current_room = self.player.current_room

        if direction not in current_room.connections:
            print(f"{RED}You can't go that way!{RESET}")
            return

        next_room = current_room.connections[direction]

        if blocked_by_darkness(self.player, next_room):
            self.player.take_damage(DAMAGE)
            print(f"{RED}It is too dark. You trip and fall.{RESET}")
            print(f"{RED}-{DAMAGE} health{RESET}")
            if not self.player.is_alive():
                print(f"{RED}You collapsed. Game over!{RESET}")
                self.game_over = True
            return

        if blocked_by_lock(self.player, next_room):
            if next_room.name == "Armory":
                print(
                    f"{YELLOW}The Armory lock is seized. Maybe something can melt it.{RESET}"
                )
            else:
                print(f"{RED}The door is locked. You need a keycard.{RESET}")
            return

        self.player.current_room = next_room
        current_room = self.player.current_room

        if boss_room(current_room):
            print(current_room.description)
            if has_boss_items(self.player):
                print(
                    f"{GREEN}Congratulations! You encountered and defeated Maradonyx.{RESET}"
                )
                print(
                    f"{GREEN}With the threat neutralized, you recover the schematics and make your way out of Vault 166.{RESET}"
                )
                print(f"{GREEN}You win!{RESET}")
            else:
                print(f"{RED}You encountered Maradonyx unprepared. Game over!{RESET}")
            self.game_over = True
            return

        damage = hazard_damage(self.player, current_room)

        if damage:
            self.player.take_damage(damage)
            print(f"{RED}The environment harms you.{RESET}")
            print(f"{RED}-{damage} health{RESET}")
            if not self.player.is_alive():
                print(f"{RED}You collapsed. Game over!{RESET}")
                self.game_over = True
                return

    def _handle_get(self, item: str) -> None:
        """Handles the player trying to get an item in the current room."""
        current_room = self.player.current_room

        if current_room.item == item:
            self.player.inventory.add(item)
            print(f"{GREEN}You picked up the {BLUE}{item}{RESET}.")
            current_room.item = None
        else:
            print(f"{RED}There is no item in the room.{RESET}")

    def _render_room(self) -> None:
        """Renders the current room's description, any notes, and visible items."""
        room = self.player.current_room
        print(room.description)

        if room.note and not room.read_note:
            print(room.note)
            room.read_note = True

        if room.item is not None:
            print(f"You see a {BLUE}{room.item}{RESET} in the room.")

    def _render_status(self) -> None:
        """Renders the player's current status, including room name, health, and inventory."""
        room = self.player.current_room

        print(f"{YELLOW}Current Room:{RESET} {room.name}")
        print(f"{YELLOW}Health:{RESET} {self.player.health}")
        print(f"{YELLOW}Inventory:{RESET} {sorted(self.player.inventory)}")

    def process_command(self, command: str) -> str:
        """Processes the player's input command and executes the corresponding action."""
        action, value = self.parser.parse(command)

        if action == "move":
            self._handle_move(value)
        elif action == "get":
            self._handle_get(value)
        elif action == "map":
            print_map()
        elif action == "save":
            print(f"{YELLOW}Save request received for slot: {value}{RESET}")
        elif action == "load":
            print(f"{YELLOW}Load request received for slot: {value}{RESET}")
        elif action == "help":
            print(
                f"{BLUE}Commands:{RESET} go <direction>, get <item>, map, save [slot], load [slot], help, exit/quit"
            )
        elif action == "exit":
            print(f"{GREEN}Exiting game... Thanks for playing Vault 166!{RESET}")
            self.game_over = True
        else:
            print(f"{RED}{value}{RESET}")

        return action

    def run(self):
        """Starts the main game loop, rendering the initial room and processing player commands until the game is over."""
        self._render_room()

        while not self.game_over:
            separator()
            self._render_status()
            separator()

            command = input("Enter your command: ")
            separator()

            action = self.process_command(command)
            if self.game_over:
                break

            if action in {"move", "get"}:
                self._render_room()
