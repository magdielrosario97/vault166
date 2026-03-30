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
        self.parser = InputParser(valid_items, 2)
        self.conn = get_db_connection()

    def _handle_move(self, direction: str) -> None:
        """Handles player movement in the given direction, applying game rules and consequences."""
        current_room = self.player.current_room
        messages = []

        """Case 1: Check if the direction is valid from the current room."""
        if direction not in current_room.connections:
            messages.append(f"{RED}You can't go that way!{RESET}")
            return messages

        next_room = current_room.connections[direction]

        """Case 2: Check for darkness blocking the path."""
        if blocked_by_darkness(self.player, next_room):
            self.player.take_damage(DAMAGE)
            messages.append(f"{RED}It is too dark. You trip and fall.{RESET}")
            messages.append(f"{RED}-{DAMAGE} health{RESET}")

            if not self.player.is_alive():
                messages.append(f"{RED}You collapsed. Game over!{RESET}")
                self.game_over = True
            return messages

        """Case 3: Check for locks blocking the path."""
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

        """Case 4: Check for boss encounter."""
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

        """Case 5: Check for environmental hazards in the new room and apply damage if necessary."""
        if damage:
            self.player.take_damage(damage)
            messages.append(f"{RED}The environment harms you.{RESET}")
            messages.append(f"{RED}-{damage} health{RESET}")
            if not self.player.is_alive():
                messages.append(f"{RED}You collapsed. Game over!{RESET}")
                self.game_over = True
                return messages

        return messages

    def _handle_get(self, item: str) -> None:
        """Handles the player trying to get an item in the current room."""
        current_room = self.player.current_room

        if current_room.item == item:
            self.player.inventory.add(item)
            current_room.item = None
            return f"{GREEN}You picked up the {BLUE}{item}{RESET}."
        else:
            return f"{RED}There is no item in the room.{RESET}"

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
            messages = self._handle_move(value)
            for message in messages:
                print(message)

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
                self._render_room()
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

        except KeyboardInterrupt:
            print(f"\n{GREEN}Exiting game... Thanks for playing Vault 166!{RESET}")
            self.game_over = True

        finally:
            self.conn.close()
