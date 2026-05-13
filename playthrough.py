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
    """Runs a list of commands through the game, displaying outputs."""
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

# Scenario: Blocked Path - Locked Door
scenario("Blocked by Locked Door")
game = Game()
run_commands(game, ["go south", "go east"])

# Scenario: Blocked Path - Armory Lock
scenario("Blocked by Armory Lock")
game = Game()
game.debug = True
run_commands(game, ["tp Emergency Response", "go south"])

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

# Scenario: Win Path - Debug
scenario("Winner, Winner, Cheater Dinner")
game = Game()
game.debug = True
run_commands(game, ["godmode", "tp West Wing", "go west"])

# Scenario: Win Path - Full Playthrough
scenario("Winner, Winner, Chicken Dinner")
game = Game()
run_commands(
    game,
    [
        "go south",  # VE -> DE
        "go west",  # DE -> ST
        "get flashlight",
        "go east",  # ST -> DE
        "go south",  # DE -> AT
        "go east",  # AT -> EW
        "go east",  # EW -> LQ
        "get keycard",
        "go west",  # LQ -> EW
        "go north",  # EW -> MD
        "get mask",
        "go south",  # MD -> EW
        "go south",  # EW -> CF (cafeteria note)
        "go north",  # CF -> EW
        "go west",  # EW -> AT
        "go south",  # AT -> ER
        "get hazmat_suit",
        "go north",  # ER -> AT
        "go west",  # AT -> WW
        "go north",  # WW -> CH
        "get acid",
        "go south",  # CH -> WW
        "go south",  # WW -> EX
        "get fusion_core",
        "go north",  # EX -> WW
        "go east",  # WW -> AT
        "go north",  # AT -> DE
        "go east",  # DE -> SE
        "get id_tag",
        "go west",  # SE -> DE
        "go south",  # DE -> AT
        "go south",  # AT -> ER
        "go south",  # ER -> AR
        "get radzapper",
        "go north",  # AR -> ER
        "go north",  # ER -> AT
        "go west",  # AT -> WW
        "go west",  # WW -> RD (win!)
    ],
)
