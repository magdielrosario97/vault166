"""
Vault 166 - Playthrough Script
Runs through major game scenarios verbosely to validate output and formatting.
Each scenario creates a fresh Game instance to ensure isolated state.
"""

from vault166.game import Game
from vault166.utils import display

SCENARIO_WIDTH = 60


def scenario(title: str) -> None:
    """Prints a labeled scenario header."""
    print(f"\n{'=' * SCENARIO_WIDTH}")
    print(f"  SCENARIO: {title}")
    print(f"{'=' * SCENARIO_WIDTH}\n")


def run_commands(game: Game, commands: list[str]) -> None:
    for command in commands:
        print(f"> {command}")
        action, messages = game.process_command(command)
        display(messages)
        if action in {"move", "get"}:
            display(game._render_room())
        print()
        if game.game_over:
            break


# Scenario: Player Movement
scenario("Player Movement")
game = Game()
run_commands(game, ["go south", "go west", "go east", "go north", "go south"])

# Scenario: Item Interaction
scenario("Item Interaction")
game = Game()
run_commands(game, ["go south", "go west", "get flashlight", "get key", "get f"])

# Scenario: Game Save Management
scenario("Game Save Management")
game = Game()
run_commands(
    game,
    [
        "save test",
        "saves",
        "go south",
        "load test",
        "saves",
        "delete test",
        "saves",
        "save",
        "load",
        "delete",
        "saves",
        "load nonexistent",
        "delete nonexistent",
    ],
)

# Scenario: Death - Darkness
scenario("Death by Darkness")
game = Game()
run_commands(game, ["go south", "go south", "go south", "go south", "go south"])

# Scenario: Death - Gas
scenario("Death by Gas")
game = Game()
game.debug = True  # Enable debug mode to bypass death and continue testing
run_commands(
    game,
    [
        "add flashlight",
        "tp Atrium",
        "go west",
        "go east",
        "go west",
        "go east",
        "go west",
        "go east",
        "go west",
    ],
)

# Scenario: Death - Radiation
scenario("Death by Radiation")
game = Game()
game.debug = True  # Enable debug mode to bypass death and continue testing
run_commands(
    game,
    [
        "add mask",
        "tp West Wing",
        "go north",
        "go south",
        "go north",
        "go south",
        "go north",
        "go south",
        "go north",
    ],
)

# Scenario: Death - Boss
scenario("Death by Boss")
game = Game()
game.debug = True
run_commands(
    game,
    [
        "add keycard",
        "tp West Wing",
        "go west",
    ],
)

# Scenario: Map and Help Commands
scenario("Map and Help Commands")
game = Game()
run_commands(game, ["map", "help"])

# Scenario: Invalid Commands
scenario("Invalid Commands")
game = Game()
run_commands(game, ["", "unknown", "go", "go xyz", "get", "get xyz"])
