def build_map():
    # Define rooms into a dictionary holding the room name
    rooms = {
        "Vacuum Room": "You are in sealed vacuum room.",
        "Mechanical Room": "You entered a room with a tool box.",
        "Decon Room": "You step in a room full of decon equipment.",
        "Foyer": "You encounter the check in desk in an open wide room.",
        "Security": "You come across a room full of security camera feed.",
        "Experimental Room": "You walk into a bright white room full of prototypes.",
        "Emergency Room": "You walk into an emergency room with electronic medical equipment.",
        "Laboratory": "You come into an extremely clean room.",
        "Chemical Room": "You opened the door holding Maradonyx."
    }

    # Define the connection of the rooms into a dictionary
    room_connections = {
        "Vacuum Room": {"west": "Mechanical Room", "south": "Decon Room"},
        "Mechanical Room": {"east": "Vacuum Room"},
        "Decon Room": {"north": "Vacuum Room", "south": "Foyer"},
        "Foyer": {"north": "Decon Room", "south": "Laboratory", "west": "Security", "east": "Experimental Room"},
        "Security": {"east": "Foyer"},
        "Experimental Room": {"west": "Foyer", "south": "Emergency Room"},
        "Emergency Room": {"west": "Laboratory", "north": "Experimental Room"},
        "Laboratory": {"west": "Chemical Room", "north": "Foyer", "east": "Emergency Room"},
        "Chemical Room": {"east": "Laboratory"}
    }

    # Define items into a dictionary with room_name: item
    items = {
        "Vacuum Room": None,  # Entrance
        "Mechanical Room": "wrench",
        "Decon Room": "mask",
        "Foyer": "flashlight",
        "Security": "key",
        "Experimental Room": "ice-blaster",
        "Emergency Room": "battery",
        "Laboratory": "schematics",
        "Chemical Room": None  # Maradonyx's Room
    }
    
    return rooms, room_connections, items