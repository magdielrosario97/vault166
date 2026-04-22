from vault166.input_parser import InputParser


def create_parser() -> InputParser:
    parser = InputParser(
        valid_items={"flashlight", "fan"},
        valid_rooms={"Storage", "Study"},
    )

    return parser


def test_tokenize():
    parser = create_parser()

    assert parser.tokenize("") == []
    assert parser.tokenize("   ") == []
    assert parser.tokenize("go north.") == ["go", "north"]
    assert parser.tokenize("go NORTH") == ["go", "north"]
    assert parser.tokenize("go  north") == ["go", "north"]


def test_parse_go():
    parser = create_parser()

    assert parser.parse("go north") == ("move", "north")
    assert parser.parse("go nor") == ("move", "north")
    assert parser.parse("go n") == ("move", "north")
    assert parser.parse("go") == ("invalid", "Specify a direction to go.")
    assert parser.parse("go xyz") == ("invalid", "Unknown direction.")


def test_parse_get():
    parser = create_parser()

    assert parser.parse("get flashlight") == ("get", "flashlight")
    assert parser.parse("get flash") == ("get", "flashlight")
    assert parser.parse("get f") == ("invalid", "Item not found or ambiguous.")
    assert parser.parse("get") == ("invalid", "Specify an item to get.")
    assert parser.parse("get xyz") == ("invalid", "Item not found or ambiguous.")


def test_parse_save_load():
    parser = create_parser()

    assert parser.parse("save") == ("save", "main")
    assert parser.parse("save slot1") == ("save", "slot1")

    assert parser.parse("load") == ("load", "main")
    assert parser.parse("load slot1") == ("load", "slot1")


def test_parse_other_commands():
    parser = create_parser()

    assert parser.parse("map") == ("map", None)
    assert parser.parse("help") == ("help", None)
    assert parser.parse("exit") == ("exit", None)
    assert parser.parse("quit") == ("exit", None)
    assert parser.parse("") == ("invalid", "Please enter a command.")
    assert parser.parse("unknown") == (
        "invalid",
        "Unknown command. Type 'help' to see available commands.",
    )


def test_parse_debug():
    parser = create_parser()

    assert parser.parse("tp Storage") == ("tp", "Storage")
    assert parser.parse("tp stor") == ("tp", "Storage")
    assert parser.parse("tp") == ("invalid", "Specify a room to teleport to.")
    assert parser.parse("add flashlight") == ("add", "flashlight")
    assert parser.parse("remove flashlight") == ("remove", "flashlight")
    assert parser.parse("clearinv") == ("clearinv", None)
    assert parser.parse("godmode") == ("godmode", None)
