from utils import separator, GREEN, BLUE, RED, YELLOW, RESET
from player import Player
from map import build_map, print_map
from input_parser import InputParser
from db import get_db_connection, save_game, load_game
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
        valid_rooms = set(self.rooms.keys())
        self.parser = InputParser(valid_items, valid_rooms, 2)
        self.conn = get_db_connection()

        self.debug = False  # Set to True to enable debug mode with extra commands.

    def _display_messages(self, messages: list[str]) -> None:
        """Utility method to display a message to the player."""
        for message in messages:
            print(message)

    def _handle_move(self, direction: str) -> list[str]:
        """Handles player movement in the given direction, applying game rules and consequences."""
        current_room = self.player.current_room
        messages = []

        if direction not in current_room.connections:
            messages.append(f"{RED}You can't go that way!{RESET}")
            return messages

        next_room = current_room.connections[direction]

        if blocked_by_darkness(self.player, next_room):
            self.player.take_damage(DAMAGE)
            messages.append(f"{RED}It is too dark. You trip and fall.{RESET}")
            messages.append(f"{RED}-{DAMAGE} health{RESET}")

            if not self.player.is_alive():
                messages.append(f"{RED}You collapsed. Game over!{RESET}")
                self.game_over = True
            return messages

        if blocked_by_lock(self.player, next_room):
            if next_room.name == "Armory":
                messages.append(
                    f"{YELLOW}The Armory lock is seized. Maybe something can melt it.{RESET}"
                )
            else:
                messages.append(f"{RED}The door is locked. You need a keycard.{RESET}")
            return messages

        self.player.current_room = next_room
        current_room = self.player.current_room

        if boss_room(current_room):
            messages.append(current_room.description)
            if has_boss_items(self.player):
                messages.append(
                    f"{GREEN}Congratulations! You encountered and defeated Maradonyx.{RESET}"
                )
                messages.append(
                    f"{GREEN}With the threat neutralized, you recover the schematics and make your way out of Vault 166.{RESET}"
                )
                messages.append(f"{GREEN}You win!{RESET}")
            else:
                messages.append(
                    f"{RED}You encountered Maradonyx unprepared. Game over!{RESET}"
                )
            self.game_over = True
            return messages

        damage = hazard_damage(self.player, current_room)

        if damage:
            self.player.take_damage(damage)
            messages.append(f"{RED}The environment harms you.{RESET}")
            messages.append(f"{RED}-{damage} health{RESET}")
            if not self.player.is_alive():
                messages.append(f"{RED}You collapsed. Game over!{RESET}")
                self.game_over = True
                return messages

        return messages

    def _handle_get(self, item: str) -> str:
        """Handles the player trying to get an item in the current room."""
        current_room = self.player.current_room

        if current_room.item == item:
            self.player.inventory.add(item)
            current_room.item = None
            return f"{GREEN}You picked up the {BLUE}{item}{RESET}."
        else:
            return f"{RED}There is no item in the room.{RESET}"

    def _render_room(self) -> list[str]:
        """Renders the current room's description, any notes, and visible items."""
        messages = []

        room = self.player.current_room
        messages.append(room.description)

        if room.note and not room.read_note:
            messages.append(room.note)
            room.read_note = True

        if room.item is not None:
            messages.append(f"You see a {BLUE}{room.item}{RESET} in the room.")

        return messages

    def _handle_debug(self, action: str, value: str | None) -> str:
        """Handles debug commands when debug mode is enabled."""
        if action == "tp":
            self.player.current_room = self.rooms[value]
            print(f"{GREEN}Teleported to {value}{RESET}")

            self._display_messages(self._render_room())

            return "debug"

        if action == "add":
            if value in self.player.inventory:
                print(f"{YELLOW}{value} is already in inventory{RESET}")
            else:
                self.player.inventory.add(value)
                print(f"{GREEN}Added {value} to inventory{RESET}")
            return "debug"

        if action == "remove":
            if value in self.player.inventory:
                self.player.inventory.remove(value)
                print(f"{GREEN}Removed {value} from inventory{RESET}")
            else:
                print(f"{RED}{value} is not in inventory{RESET}")
            return "debug"

        if action == "clearinv":
            if not self.player.inventory:
                print(f"{YELLOW}Inventory is already empty{RESET}")
            else:
                self.player.inventory.clear()
                print(f"{GREEN}Cleared inventory{RESET}")
            return "debug"

        if action == "godmode":
            self.player.health = 999
            self.player.inventory.update(
                {
                    "flashlight",
                    "keycard",
                    "mask",
                    "hazmat_suit",
                    "acid",
                    "fusion_core",
                    "id_tag",
                    "radzapper",
                }
            )
            print(f"{GREEN}Maxed health and added all items to inventory{RESET}")

        return "debug"

    def _render_status(self) -> list[str]:
        """Renders the player's current status, including room name, health, and inventory."""
        room = self.player.current_room
        messages = []

        messages.append(f"{YELLOW}Current Room:{RESET} {room.name}")
        messages.append(f"{YELLOW}Health:{RESET} {self.player.health}")
        messages.append(f"{YELLOW}Inventory:{RESET} {sorted(self.player.inventory)}")

        return messages

    def process_command(self, command: str) -> str:
        """Processes the player's input command and executes the corresponding action."""

        # Toggle debug mode with "debug" command
        if command.strip() == "debug":
            self.debug = not self.debug
            state = "enabled" if self.debug else "disabled"
            print(f"{YELLOW}Debug mode {state}{RESET}")
            return "debug"

        action, value = self.parser.parse(command)

        # Debug command - only execute if debug mode is enabled
        if self.debug and action in {"tp", "add", "remove", "clearinv", "godmode"}:
            return self._handle_debug(action, value)

        # Gameplay commands - move, get, map, save, load, help, exit
        if action == "move":
            self._display_messages(self._handle_move(value))

        elif action == "get":
            message = self._handle_get(value)
            print(message)

        elif action == "map":
            print_map()

        elif action == "save":
            save_game(self.conn, value, self.player, self.rooms)
            print(f"{GREEN}Game saved to slot {value}.{RESET}")

        elif action == "load":
            loaded = load_game(self.conn, value, self.rooms, self.player)
            if loaded:
                print(f"{GREEN}Game loaded from slot {value}.{RESET}")

                self._display_messages(self._render_room())
            else:
                print(f"{RED}Save slot not found: {value}{RESET}")

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
        try:
            self._display_messages(self._render_room())

            while not self.game_over:
                separator()
                self._display_messages(self._render_status())
                separator()

                command = input("Enter your command: ")
                separator()

                action = self.process_command(command)
                if self.game_over:
                    break

                if action in {"move", "get"}:
                    self._display_messages(self._render_room())

        except KeyboardInterrupt:
            print(f"\n{GREEN}Exiting game... Thanks for playing Vault 166!{RESET}")
            self.game_over = True

        finally:
            self.conn.close()
