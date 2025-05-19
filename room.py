# Create a Room class to store each room's info
class Room:
    def __init__(self, name, description="", required_item=None, hazard_item=None, item=None, is_locked=False):
        self.name = name  # Name of the room
        self.description = description  # Description of the room
        self.required_item = required_item if required_item else []  # Item needed to enter this room (optional)
        self.hazard_item = hazard_item if hazard_item else [] # Item needed to avoid consequences
        self.item = item  # Item found in this room (optional)
        self.is_locked = is_locked  # True if the room is locked
        self.connections = {}  # Dictionary to hold connected rooms 

    # Connect this room to another in a specific direction
    def connect(self, direction, room):
        # Store a reference to the other room in the given direction
        self.connections[direction] = room
