from vault166.save_manager import SaveManager
from vault166.player import Player
from vault166.room import Room


def create_save_manager() -> SaveManager:
    return SaveManager(db_path=":memory:")  # Use in-memory database for testing


def create_player(*items) -> Player:
    player = Player(create_room())
    player.inventory.update(items)
    return player


def create_room(name="Test Room", dark=False, locked=False, hazard=None) -> Room:
    return Room(name, "The testing room...", dark=dark, locked=locked, hazard=hazard)


def create_rooms() -> dict:
    room = create_room()
    return {room.name: room}


def test_save():
    manager = create_save_manager()
    player = create_player("flashlight", "keycard")
    rooms = create_rooms()

    message = manager.save("test_slot", player, rooms)
    assert message == "Game saved to slot 'test_slot'."


def test_save_overwrite():
    manager = create_save_manager()
    player = create_player("flashlight", "keycard")
    rooms = create_rooms()

    manager.save("test_slot", player, rooms)
    message = manager.save("test_slot", player, rooms)
    assert message == "Game saved to slot 'test_slot'."


def test_load_success():
    manager = create_save_manager()
    player = create_player("flashlight", "keycard")
    rooms = create_rooms()

    manager.save("test_slot", player, rooms)
    success, message = manager.load("test_slot", player, rooms)
    assert success
    assert message == "Game loaded from slot 'test_slot'."


def test_load_not_found():
    manager = create_save_manager()
    player = create_player("flashlight", "keycard")
    rooms = create_rooms()

    success, message = manager.load("nonexistent_slot", player, rooms)
    assert not success
    assert message == "Save slot 'nonexistent_slot' not found."


def test_delete_success():
    manager = create_save_manager()
    player = create_player("flashlight", "keycard")
    rooms = create_rooms()

    manager.save("test_slot", player, rooms)
    success, message = manager.delete("test_slot")
    assert success
    assert message == "Save slot 'test_slot' deleted."


def test_delete_not_found():
    manager = create_save_manager()
    success, message = manager.delete("nonexistent_slot")
    assert not success
    assert message == "Save slot 'nonexistent_slot' not found."


def test_saves_empty():
    manager = create_save_manager()
    saves = manager.view()
    assert len(saves) == 0


def test_saves_with_data():
    manager = create_save_manager()
    player = create_player("flashlight", "keycard")
    rooms = create_rooms()

    manager.save("slot2", player, rooms)
    manager.save("slot1", player, rooms)

    saves = manager.view()
    assert len(saves) == 2
    assert {s[0] for s in saves} == {"slot1", "slot2"}
