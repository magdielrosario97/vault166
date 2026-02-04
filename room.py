class Room:
    def __init__(
        self,
        name: str,
        description: str,
        hazard: str | None = None,
        locked: bool = False,
        item: str | None = None,
    ):

        self.name = name
        self.description = description
        self.hazard = hazard
        self.locked = locked
        self.item = item
        self.connections: dict[str, "Room"] = {}

    def connect(self, direction: str, room: "Room") -> None:
        self.connections[direction] = room
