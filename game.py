'''
Vault 166 - A survival text-based python game
Created by Magdiel Rosario Orta
'''

# Imports
from player import Player
from room import rooms, room_connections
from items import items
from utils import welcome

# Game function
def vault166():
    # Create player instance
    player = Player()
    game_over = False

    # Game Loop
    while not game_over:
        # Display current room description
        print(f'\033[92mYou moved to {player.current_room}\033[0m')
        print(rooms[player.current_room])
        print("Inventory:", player.inventory)

        # Check if there's an item
        if items[player.current_room] is not None:
            print(f"You see a \033[94m{items[player.current_room]}\033[0m in the room.")

        print('-----------------------------------------------------------------')
        command = input("Enter your command: ").strip().lower()
        print('-----------------------------------------------------------------')

        if command.startswith("go "):
            direction = command[3:]
            if direction in room_connections[player.current_room]:
                player.current_room = room_connections[player.current_room][direction]

                # Check for Maradonyx encounter
                if player.current_room == "Chemical Room":
                    print(rooms[player.current_room])
                    if player.has_all_items():
                        print("\033[93mCongratulations! You collected all the items and defeated Maradonyx.")
                        print("You win!\033[0m")
                    else:
                        print("\033[91mYou encountered Maradonyx before collecting all the items.")
                        print("Game over!\033[0m")
                    game_over = True
            else:
                print("\033[91mYou can't go that way!\033[0m")
                print(f"HINT: {room_connections[player.current_room]}")
        
        elif command.startswith("get "):
            item = command[4:]
            if items[player.current_room] == item:
                player.add_item(item)
                print("You picked up the\033[94m", item + "\033[0m.")
                items[player.current_room] = None
            else:
                print("\033[91mThere is no item in the room.\033[0m")

        else:
            print("\033[91mInvalid command!\033[0m")


# Run the game
welcome()
vault166()
