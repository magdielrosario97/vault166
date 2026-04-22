from vault166.player import Player
from vault166.room import Room
from vault166.rules import (
    blocked_by_darkness,
    blocked_by_lock,
    boss_room,
    has_boss_items,
    hazard_damage,
    DAMAGE,
)


def create_player(*items) -> Player:
    player = Player(create_room)
    player.inventory.update(items)
    return player


def create_room(name="Test Room", dark=False, locked=False, hazard=None) -> Room:
    return Room(name, "The testing room...", dark=dark, locked=locked, hazard=hazard)


def test_blocked_by_darkness():
    dark_room = create_room(dark=True)
    lit_room = create_room(dark=False)
    player = create_player()

    assert blocked_by_darkness(player, dark_room) == True

    player.inventory.add("flashlight")
    assert blocked_by_darkness(player, dark_room) == False

    player.inventory.remove("flashlight")
    assert blocked_by_darkness(player, lit_room) == False


def test_blocked_by_lock():
    locked_room = create_room(locked=True)
    unlocked_room = create_room(locked=False)
    armory_room = create_room(name="Armory", locked=True)
    player = create_player()

    assert blocked_by_lock(player, locked_room) == True
    player.inventory.add("keycard")
    assert blocked_by_lock(player, locked_room) == False

    assert blocked_by_lock(player, armory_room) == True
    player.inventory.add("acid")
    assert blocked_by_lock(player, armory_room) == False

    player.inventory.clear()
    assert blocked_by_lock(player, unlocked_room) == False


def test_boss_room():
    final_room = create_room(name="Research & Development")
    other_room = create_room()

    assert boss_room(final_room) == True
    assert boss_room(other_room) == False


def test_has_boss_items():
    boss_items = ("radzapper", "mask", "hazmat_suit", "fusion_core", "id_tag")
    player = create_player(*boss_items)

    assert has_boss_items(player) == True

    player.inventory.remove("mask")
    assert has_boss_items(player) == False

    player.inventory.clear()
    assert has_boss_items(player) == False


def test_hazard_damage():
    gas_room = create_room(hazard="gas")
    radiation_room = create_room(hazard="radiation")
    unknown_hazard = create_room(hazard="unknown")
    safe_room = create_room()
    player = create_player()

    assert hazard_damage(player, safe_room) == 0

    assert hazard_damage(player, gas_room) == DAMAGE
    player.inventory.add("mask")
    assert hazard_damage(player, gas_room) == 0

    assert hazard_damage(player, radiation_room) == DAMAGE
    player.inventory.add("hazmat_suit")
    assert hazard_damage(player, radiation_room) == 0

    assert hazard_damage(player, unknown_hazard) == 0
