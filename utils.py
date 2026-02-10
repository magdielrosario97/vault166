BLUE = "\033[94m"
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
RESET = "\033[0m"

SEPARATOR = "-" * 65


def separator() -> None:
    print(SEPARATOR)


def welcome() -> None:
    """Prints the welcome message and game instructions to the player."""
    print(f"{BLUE}Welcome to Vault 166 - Text Based Game{RESET}")
    separator()
    print("Survive the vault and gather the key items needed to win.")
    print("Move: go <direction>   Example: go north, go n, go up")
    print("Get:  get <item>        Example: get flashlight, get fl")
    print("Other: map, help, quit")
    separator()
