'''
Vault 166 - A survival text-based python game
Created by Magdiel Rosario Orta
21 June 2023
'''

# Function to show player welcome message and instructions
def welcome():
    print('\033[94mWelcome to Vault 166 - Text Based Game\033[0m')
    print('-----------------------------------------------------------------')
    print('Collect all 7 items and escape!')
    print('To move: go north | go south | go east | go west')
    print('To collect item: get item')
    print('-----------------------------------------------------------------')


# Game function
def vault166():
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

    # Game Initialization
    current_room = "Vacuum Room"
    inventory = []
    game_over = False

    # Game Loop
    while not game_over:
        # Display current room description
        print(f'\033[92mYou moved to {current_room}\033[0m')
        print(rooms[current_room])
        # Display player's inventory
        print("Inventory:", inventory)

        # Check if the current room contains an item
        if items[current_room] is not None:
            print(f"You see a \033[94m{items[current_room]}\033[0m in the room.")

        # Player input
        print('-----------------------------------------------------------------')
        command = input("Enter your command: ")
        print('-----------------------------------------------------------------')
        # Process player's command
        if command.startswith("go "):
            direction = command[3:]
            if direction in room_connections[current_room]:
                current_room = room_connections[current_room][direction]
                # Check if the player encounters Maradonyx
                if current_room == "Chemical Room":
                    print(rooms[current_room])
                    if len(inventory) == 7 and current_room == 'Chemical Room':
                        print("\033[93mCongratulations! You collected all the items and defeated Maradonyx.")
                        print("You win!\033[0m")
                        game_over = True
                    else:
                        print("\033[91mYou encountered Maradonyx before collecting all the items.")
                        print("Game over!\033[0m")
                        game_over = True
            else:
                print("\033[91mYou can't go that way!\033[0m")
                print(f'HINT: {room_connections[current_room]}')
        elif command.startswith("get "):
            item = command[4:]
            if items[current_room] == item:
                inventory.append(item)
                print("You picked up the\033[94m", item + "\033[0m.")
                items[current_room] = None
            else:
                print("\033[91mThere is no item in the room.\033[0m")
        else:
            print("\033[91mInvalid command!\033[0m")


welcome()
vault166()
