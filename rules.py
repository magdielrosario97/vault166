from player import Player
from room import Room

DAMAGE = 25

FLASHLIGHT = "flashlight"
KEYCARD = "keycard"
ACID = "acid"

HAZARD_REQUIREMENTS: dict[str, set[str]] = {
    "gas": {"mask"},
    "radiation": {"mask", "hazmat_suit"},
}

BOSS_ITEMS: set[str] = {
    "radzapper",
    "mask",
    "hazmat_suit",
    "fusion_core",
    "id_tag",
}


def blocked_by_darkness(player: Player, room: Room) -> bool:
    return room.dark and FLASHLIGHT not in player.inventory


def blocked_by_lock(player: Player, room: Room) -> bool:
    if room.name == "Armory":
        return ACID not in player.inventory

    return room.locked and KEYCARD not in player.inventory


def boss_room(room: Room) -> bool:
    return room.name == "Research & Development"


def has_boss_items(player: Player) -> bool:
    missing = BOSS_ITEMS - player.inventory
    return not missing


def hazard_damage(player: Player, room: Room) -> int:
    if room.hazard is None:
        return 0

    required = HAZARD_REQUIREMENTS.get(room.hazard)
    if required is None:
        return 0

    missing = required - player.inventory
    if missing:
        return DAMAGE
    return 0
