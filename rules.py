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
    """Determines if the player is blocked by darkness when trying to enter a room."""
    return room.dark and FLASHLIGHT not in player.inventory


def blocked_by_lock(player: Player, room: Room) -> bool:
    """Determines if the player is blocked by a locked door when trying to enter a room."""
    if room.name == "Armory":
        return ACID not in player.inventory

    return room.locked and KEYCARD not in player.inventory


def boss_room(room: Room) -> bool:
    """Determines if the given room is the boss room."""
    return room.name == "Research & Development"


def has_boss_items(player: Player) -> bool:
    """Checks if the player has all the required items to defeat the boss."""
    missing = BOSS_ITEMS - player.inventory
    return not missing


def hazard_damage(player: Player, room: Room) -> int:
    """Calculates the damage the player takes from hazards in the room, if any."""
    if room.hazard is None:
        return 0

    required = HAZARD_REQUIREMENTS.get(room.hazard)
    if required is None:
        return 0

    missing = required - player.inventory
    if missing:
        return DAMAGE
    return 0
