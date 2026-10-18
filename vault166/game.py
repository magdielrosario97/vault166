from vault166.utils import (
    welcome,
    farewell,
    empty_line,
    separator,
    display,
    help_commands
)
from vault166.player import Player
from vault166.map import build_map, render_map
from vault166.input_parser import InputParser
from vault166.save_manager import SaveManager
from vault166.rules import (
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
        self.save_manager = SaveManager()

        self.debug = False  # Set to True to enable debug mode with extra commands.

    def _handle_move(self, direction: str) -> list[str]:
        """Handles player movement in the given direction, applying game rules and consequences."""
        current_room = self.player.current_room
        messages = []

        if direction not in current_room.connections:
            messages.append(f"You can't go that way!")
            return messages

        next_room = current_room.connections[direction]

        if blocked_by_darkness(self.player, next_room):
            self.player.take_damage(DAMAGE)
            messages.append(
                f"It is too dark. You trip and fall. | -{DAMAGE} health"
            )

            if not self.player.is_alive():
                messages.extend(empty_line())
                messages.append(f"You collapsed. Game over!")
                self.game_over = True
            return messages

        if blocked_by_lock(self.player, next_room):
            if next_room.name == "Armory":
                messages.append(
                    f"The Armory lock is seized. Maybe something can melt it.   "
                )
            else:
                messages.append(f"The door is locked. You need a keycard.")
            return messages

        self.player.current_room = next_room
        current_room = self.player.current_room

        if boss_room(current_room):
            if has_boss_items(self.player):
                messages.append(f"{current_room.description}")
                messages.extend(empty_line())
                messages.append(
                    f"Congratulations! You encountered and defeated Maradonyx."
                )
                messages.extend(empty_line())
                messages.append(
                    f"With the threat neutralized, you recover the schematics and make your way out of Vault 166."
                )
                messages.extend(empty_line())
                messages.append(f"You win!")
            else:
                messages.append(f"{current_room.description}")
                messages.extend(empty_line())
                messages.append(
                    f"You encountered Maradonyx unprepared. Game over!"
                )
            self.game_over = True
            return messages

        damage = hazard_damage(self.player, current_room)

        if damage:
            self.player.take_damage(damage)
            messages.append(
                f"The environment harms you. | -{damage} health"
            )
            if not self.player.is_alive():
                messages.extend(empty_line())
                messages.append(f"You collapsed. Game over!")
                self.game_over = True
                return messages

        return messages

    def _handle_get(self, item: str) -> list[str]:
        """Handles the player trying to get an item in the current room."""
        current_room = self.player.current_room
        messages = []

        if current_room.item == item:
            self.player.inventory.add(item)
            current_room.item = None
            messages.append(f"You picked up the {item}.")
        else:
            messages.append(f"There is no item in the room.")

        return messages

    def _render_room(self) -> list[str]:
        """Renders the current room's description, any notes, and visible items."""
        messages = []

        room = self.player.current_room
        messages.append(room.description)

        if room.note and not room.read_note:
            messages.extend(empty_line())
            messages.extend(room.note)

            room.read_note = True

        if room.item is not None:
            messages.extend(empty_line())
            messages.append(
                f"\u269e You see a {room.item} in the room \u269f"
            )

        return messages

    def _handle_debug(self, action: str, value: str | None) -> list[str]:
        """Handles debug commands when debug mode is enabled."""
        messages = []

        if action == "tp":
            self.player.current_room = self.rooms[value]
            messages.append(f"Teleported to {value}")
            return messages

        if action == "add":
            if value in self.player.inventory:
                messages.append(f"{value} is already in inventory")
            else:
                self.player.inventory.add(value)
                messages.append(f"Added {value} to inventory")
            return messages

        if action == "remove":
            if value in self.player.inventory:
                self.player.inventory.remove(value)
                messages.append(f"Removed {value} from inventory")
            else:
                messages.append(f"{value} is not in inventory")
            return messages

        if action == "clearinv":
            if not self.player.inventory:
                messages.append(f"Inventory is already empty")
            else:
                self.player.inventory.clear()
                messages.append(f"Cleared inventory")
            return messages

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
            messages.append(
                f"Maxed health and added all items to inventory"
            )

        return messages

    def _render_status(self) -> list[str]:
        """Renders the player's current status, including room name, health, and inventory."""
        room = self.player.current_room
        item_bag = ", ".join(sorted(self.player.inventory)) if self.player.inventory else "Empty"
        messages = []

        messages.append(f"Current Room: {room.name}")
        messages.append(f"Health: {self.player.health}")
        messages.append(f"Bag: {item_bag}")

        return messages

    def process_command(self, command: str) -> tuple[str, list[str]]:
        """Processes the player's input command and executes the corresponding action."""
        messages = []

        # Toggle debug mode with "debug" command
        if command.strip() == "debug":
            self.debug = not self.debug
            state = "enabled" if self.debug else "disabled"
            messages.append(f"Debug mode {state}")
            return "debug", messages

        action, value = self.parser.parse(command)

        # Debug command - only execute if debug mode is enabled
        if self.debug and action in {"tp", "add", "remove", "clearinv", "godmode"}:
            return "debug", self._handle_debug(action, value)

        # Gameplay commands - move, get, map, save, load, help, exit
        if action == "move":
            messages.extend(self._handle_move(value))

        elif action == "get":
            messages.extend(self._handle_get(value))

        elif action == "map":
            messages.extend(render_map())

        elif action == "save":
            message = self.save_manager.save(value, self.player, self.rooms)
            messages.append(f"{message}")

        elif action == "load":
            success, message = self.save_manager.load(value, self.player, self.rooms)

            if success:
                messages.append(f"{message}")
            else:
                messages.append(f"{message}")

        elif action == "saves":
            saves = self.save_manager.view()
            if saves:
                messages.append(f"Save Slots:")
                for slot_name, last_save in saves:
                    messages.append(f" - {slot_name} (Last saved: {last_save})")
            else:
                messages.append(f"No save slots found.")

        elif action == "delete":
            success, message = self.save_manager.delete(value)

            if success:
                messages.append(f"{message}")
            else:
                messages.append(f"{message}")

        elif action == "help":
            messages.extend(help_commands())

        elif action == "exit":
            messages.extend(farewell())
            self.game_over = True

        else:
            messages.append(f"{value}")

        return action, messages

    # BUG: saves with default slot name are deleted on game exit - need to ensure default saves are preserved
    def run(self):
        """Starts the main game loop, rendering the initial room and processing player commands until the game is over."""
        try:
            display(welcome())
            while not self.game_over:

                display(separator())
                display(self._render_status())
                display(separator())
                display(self._render_room(), True)
                display(empty_line())

                command = input(f"> Enter your command: ")

                messages = self.process_command(command)[1]

                if messages:
                    display(empty_line())
                    display(messages)

                if self.game_over:
                    break

                display(empty_line(4))

        except KeyboardInterrupt:
            display(farewell())
            self.game_over = True

        finally:
            self.save_manager.close()
