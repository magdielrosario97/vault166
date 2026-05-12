import textwrap

BLUE = "\033[94m"
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
RESET = "\033[0m"

WIDTH = 80
SEPARATOR = "-" * 80


def display(messages: list[str]) -> None:
    """Utility method to display a message to the player."""
    for message in messages:
        print(wrap(message))


def wrap(message: str) -> str:
    """Wraps a message to fit within the defined WIDTH."""
    return textwrap.fill(message, width=WIDTH)


def separator() -> list[str]:
    """Returns a list containing a separator line to be used in the game output."""
    messages = []

    messages.append(f"{SEPARATOR}")
    return messages


def welcome() -> list[str]:
    """Returns a list of welcome messages to be displayed at the start of the game."""
    messages = []

    messages.extend(separator())
    messages.append(f"{BLUE}Welcome to Vault 166 - Text Based Game{RESET}")
    messages.append("Survive the vault and gather the key items needed to win.")
    messages.append("Move: go <direction>   Example: go north, go n, go up")
    messages.append("Get:  get <item>        Example: get flashlight, get fl")
    messages.append("Other: map, save [slot], load [slot], help, quit")
    messages.extend(separator())

    return messages
