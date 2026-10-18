import textwrap

STAR = "\u2605"
HEART = "\u2764"

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


def separator(symbol: str = "─") -> list[str]:
    """Returns a list containing a separator line made of the specified symbol, spanning the defined WIDTH."""
    messages = []

    messages.append(f"{symbol * WIDTH}")

    return messages


def help_commands():
    """Returns a list of help messages to be displayed when the player types 'help'."""
    messages = []

    messages.extend(
        [
            f"Commands",
            *separator(),
            f"  Move:      go <direction>      Example: go north, go n, go up",
            f"  Get:       get <item>          Example: get flashlight, get fl",
            f"  Save:      save [slot]         Example: save, save test",
            f"  Load:      load [slot]         Example: load, load test",
            f"  Delete:    delete [slot]       Example: delete test",
            f"  Other:     map, saves, help, quit",
            *separator(),
            *empty_line(2),
        ]
    )

    return messages


def welcome() -> list[str]:
    """Returns a list of welcome messages to be displayed at the start of the game."""
    messages = []

    messages.extend(
        [
            *separator("═"),
            f"{f'{STAR} Welcome to Vault 166 {STAR}'.center(WIDTH)}",
            *separator("═"),
            *empty_line(),
            f"{f'Survive the vault and gather the key items needed to win!'.center(WIDTH)}",
            *empty_line(),
            *help_commands(),
        ]
    )

    return messages


def farewell() -> list[str]:
    """Returns a list of farewell messages to be displayed at the end of the game."""
    messages = []

    messages.extend(
        [
            *empty_line(5),
            *separator("═"),
            f"{f'{STAR} {STAR} Exiting game... Thanks for playing Vault 166! {STAR} {STAR}'.center(WIDTH)}",
            f"{f'{HEART} {HEART} {HEART}'.center(WIDTH)}",
            *separator("═"),
        ]
    )

    return messages
