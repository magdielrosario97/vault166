''' python
Pseudocode for Vault 166
================================================================================

Define rooms into a dictionary holding the room name
and description as room_name: description.

rooms = {
    Vacuum Room: You are in sealed vacuum room.
    Mechanical Room: You entered a room with a tool box.
    Decon Room: You step in a room full of decon equipment.
    Foyer: You encounter the check in desk in an open wide room.
    Security: You come across a room full of security camera feed.
    Experimental Room: You walk into a bright white room full of prototypes.
    Emergency Room: You walk into an emergency room with electronic medical equipment.
    Laboratory: You come into an extremely clean room.
    Chemical Room: You opened the door holding Maradonyx.
}

================================================================================

Define the connection of the rooms into a dictionary holding
to hold possible movement options.
room_conn = {
    Vacuum Room: {west: Mechanical Room, south: Decon Room}
    Mechanical Room: {east: Vacuum Room}
    Decon Room: {north: Vacuum Room, south: Foyer}
    Foyer: {north: Decon Room, south: Laboratory, east: Security, west: Experimental Room}
    Security: {east: Foyer}
    Experimental Room: {west: Foyer, south: Emergency Room}
    Emergency Room: {west: Laboratory, north: Experimental Room}
    Laboratory: {east: Chemical Room, north: Foyer, west: Emergency Room}
    Chemical Room: {east: Laboratory}
}

================================================================================

Define items into a dictionary with room_name: item
items = {
    Vacuum Room: None # Entrance
    Mechanical Room: Wrench
    Decon Room: Boots
    Foyer: Flashlight
    Security: Master Key
    Experimental Room: Icy Goo Blaster
    Emergency Room: Fuse
    Laboratory: Radzapper Schematics
    Chemical Room: None # Maradonyx's Room
}

================================================================================

Define current_room as the entrance room
Define an empty list to hold the users inventory
Define an empty list holding the collected items

While true
    Print [current room]
    Print [item in room]

    If current_room is in items
    and items at current room
    and items at current room not in inventory
        Print You see [item]

    Prompt User for a go direction and get item command
    Define a variable holding the command string split

    If the split part of the string equals 2
        Define action, target = split part of string

        If action is equal to go
            If target is in room conn at current room
                Define current room as room conn at current room at target
                Print You moved to [current room]

            Else
                Print You cannot go in that direction

        Else If action is equal to get
            If target equals item at current room and target is not in inventory
                Append target to inventory
                Print You obtained [item]
                Append item to collected items list

                If the length of items collected is equal to 7
                and current room equals Vacuum Room
                    Print Winning Message
                    Break

            Else
                Print You cannot get item

    Else
        Print Invalid Command
'''