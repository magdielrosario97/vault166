class Room:
    """
    Represents a room in the vault, with its description, connections,
    and any items or hazards it contains.
    """

    def __init__(
        self,
        name: str,
        description: str,
        hazard: str | None = None,
        locked: bool = False,
        dark: bool = False,
        item: str | None = None,
        note: str | None = None,
    ):

        self.name = name
        self.description = description
        self.hazard = hazard
        self.locked = locked
        self.dark = dark
        self.item = item
        self.note = note
        self.read_note = False
        self.connections: dict[str, "Room"] = {}

    def connect(self, direction: str, room: "Room") -> None:
        """Connects this room to another room in the given direction."""
        self.connections[direction] = room
