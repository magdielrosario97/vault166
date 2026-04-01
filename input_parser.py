import string

VALID_DIRECTIONS = ["north", "south", "east", "west"]
DIRECTION_ALIASES = {
    "u": "north",
    "up": "north",
    "d": "south",
    "down": "south",
    "l": "west",
    "left": "west",
    "r": "east",
    "right": "east",
    "n": "north",
    "s": "south",
    "e": "east",
    "w": "west",
}


class InputParser:
    """Parses player input into game commands and arguments."""

    def __init__(
        self, valid_items: set[str], valid_rooms: set[str], min_item_chars: int = 2
    ):
        self.valid_items = valid_items
        self.valid_rooms = valid_rooms
        self.min_item_chars = min_item_chars

    def parse(self, raw: str) -> tuple[str, str | None]:
        """
        Parses raw input and returns a tuple of (action, argument) or (action, None).
        """
        tokens = self.tokenize(raw)

        if not tokens:
            return "invalid", "Please enter a command."

        verb = tokens[0]

        # Handle movement commands - "go <direction>"
        if verb == "go":
            if len(tokens) < 2:
                return "invalid", "Specify a direction to go."
            direction = self.normalize_direction(tokens[1])
            if direction is None:
                return "invalid", "Unknown direction."
            return "move", direction

        # Handle item pickup - "get <item>"
        if verb == "get":
            if len(tokens) < 2:
                return "invalid", "Specify an item to get."
            item = self.normalize_item(tokens[1])
            if item is None:
                return "invalid", "Item not found or ambiguous."
            return "get", item

        # Handle save game - "save [slot_name]"
        if verb == "save":
            if len(tokens) < 2:
                return "save", "main"
            slot_name = tokens[1]
            return "save", slot_name

        # Handle load game - "load [slot_name]"
        if verb == "load":
            if len(tokens) < 2:
                return "load", "main"
            slot_name = tokens[1]
            return "load", slot_name

        # Handle map command - "map"
        if verb == "map":
            return "map", None

        # Handle help command - "help"
        if verb == "help":
            return "help", None

        # Handle exit commands - "exit" or "quit"
        if verb in {"exit", "quit"}:
            return "exit", None

        # Debug commands (only if debug mode is enabled in the game)
        # Teleport debug command - tp <room name>
        if verb == "tp":
            if len(tokens) < 2:
                return "invalid", "Specify a room to teleport to."

            room_name = self.normalize_room(" ".join(tokens[1:]))

            if room_name is None:
                return "invalid", "Room not found or ambiguous."

            return "tp", room_name

        # Add item debug command - add <item name>
        if verb == "add":
            if len(tokens) < 2:
                return "invalid", "Specify an item to add."

            item = self.normalize_item(tokens[1])

            if item is None:
                return "invalid", "Item not found or ambiguous."

            return "add", item

        # Remove item debug command - remove <item name>
        if verb == "remove":
            if len(tokens) < 2:
                return "invalid", "Specify an item to remove."

            item = self.normalize_item(tokens[1])

            if item is None:
                return "invalid", "Item not found or ambiguous."

            return "remove", item

        # Clear inventory debug command - clearinv
        if verb == "clearinv":
            return "clearinv", None

        # God mode debug command - godmode
        if verb == "godmode":
            return "godmode", None

        return "invalid", "Unknown command. Type 'help' to see available commands."

    def tokenize(self, raw: str) -> list[str]:
        """Converts raw input into a list of cleaned tokens."""
        raw = raw.lower().strip()
        if not raw:
            return []
        parts = raw.split()
        tokens = []
        for part in parts:
            part = part.strip(string.punctuation)
            if part:
                tokens.append(part)
        return tokens

    def normalize_direction(self, in_direction: str) -> str | None:
        """Converts input direction to a valid direction or returns None if invalid."""
        if in_direction in DIRECTION_ALIASES:
            return DIRECTION_ALIASES[in_direction]

        match_direction = [
            direction
            for direction in VALID_DIRECTIONS
            if direction.startswith(in_direction)
        ]
        if len(match_direction) == 1:
            return match_direction[0]

        return None

    def normalize_item(self, in_item: str) -> str | None:
        """Converts input item to a valid item or returns None if invalid or ambiguous."""
        if in_item in self.valid_items:
            return in_item

        if len(in_item) < self.min_item_chars:
            return None

        match_items = [item for item in self.valid_items if item.startswith(in_item)]
        if len(match_items) == 1:
            return match_items[0]

        return None

    def normalize_room(self, in_room: str) -> str | None:
        """Converts input room name to a valid room name or returns None if invalid or ambiguous."""
        if len(in_room) < self.min_item_chars:
            return None

        match_rooms = [
            room for room in self.valid_rooms if room.lower().startswith(in_room)
        ]
        if len(match_rooms) == 1:
            return match_rooms[0]

        return None
