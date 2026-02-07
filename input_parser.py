import string

VALID_COMMANDS = ["go", "get", "map", "help"]
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
    def __init__(self, valid_items: set[str], min_item_chars: int):
        self.valid_items = valid_items
        self.min_item_chars = min_item_chars

    def parse(self, raw: str):
        tokens = self.tokenize(raw)

        if not tokens:
            return "invalid", "Please enter a command."

        verb = tokens[0]

        if verb == "go":
            if len(tokens) < 2:
                return "invalid", "Specify a direction to go."
            direction = self.normalize_direction(tokens[1])
            if direction is None:
                return "invalid", "Unknown direction."
            return "move", direction

        if verb == "get":
            if len(tokens) < 2:
                return "invalid", "Specify an item to get."
            item = self.normalize_item(tokens[1])
            if item is None:
                return "invalid", "Item not found or ambiguous."
            return "get", item

        if verb == "map":
            return "map", None

        if verb == "help":
            return "help", None

        if verb in {"exit", "quit"}:
            return "exit", None

        return "invalid", "Unknown command. Type 'help' to see available commands."

    def tokenize(self, raw: str) -> list[str]:
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
        if in_item in self.valid_items:
            return in_item

        if len(in_item) < self.min_item_chars:
            return None

        match_items = [item for item in self.valid_items if item.startswith(in_item)]
        if len(match_items) == 1:
            return match_items[0]

        return None
