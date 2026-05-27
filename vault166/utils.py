import textwrap

BLUE = "\033[94m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
AMBER = "\033[38;5;214m"
AMBER_DIM = "\033[38;5;136m"
LIME = "\033[38;5;154m"
OLIVE = "\033[38;5;100m"
RED = "\033[91m"
ORANGE = "\033[38;5;208m"
TEAL = "\033[38;5;37m"
RESET = "\033[0m"

STAR = "\u2605"
HEART = "\u2764"

BLINK = "\033[5m"

WIDTH = 80


def display(messages: list[str], wrap_text: bool = False) -> None:
    """Utility function to display messages to the player, with optional text wrapping."""
    for message in messages:
        if wrap_text:
            print(wrap(message))
        else:
            print(message)


def wrap(message: str) -> str:
    """Wraps a message to fit within the defined WIDTH."""
    return textwrap.fill(message, width=WIDTH)


def empty_line(lines: int = 1) -> list[str]:
    """Returns a list of empty strings to create blank lines in the game output."""
    return [""] * lines


def separator(symbol: str = "-", color: str = GREEN) -> list[str]:
    """Returns a list containing a separator line made of the specified symbol and color, spanning the defined WIDTH."""
    messages = []

    messages.append(f"{color}{symbol * WIDTH}{RESET}")

    return messages


def welcome() -> list[str]:
    """Returns a list of welcome messages to be displayed at the start of the game."""
    messages = []

def farewell() -> list[str]:
    """Returns a list of farewell messages to be displayed at the end of the game."""
    messages = []

    messages.extend(
        [
            *empty_line(5),
            *separator("\u2593"),
            f"{TEAL}{BLINK}{f'{STAR} {STAR} Exiting game... Thanks for playing Vault 166! {STAR} {STAR}'.center(WIDTH)}{RESET}",
            f"{TEAL}{f'{HEART} {HEART} {HEART}'.center(WIDTH)}{RESET}",
            *separator("\u2593"),
        ]
    )

    return messages
