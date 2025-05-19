'''
Vault 166 - A survival text-based python game
Created by Magdiel Rosario Orta
'''

# Imports
from player import Player
from map import starting_room
from utils import welcome

# Game function
def vault166():
    # Create player instance
    player = Player(starting_room)
    game_over = False

    # Game Loop
    while not game_over:
        # Display current room description
        print(f'\033[92mYou are in {player.current_room.name}\033[0m')
        print("Inventory:", player.inventory)

        # # Check if there's an item
        # if items[player.current_room] is not None:
        #     print(f"You see a \033[94m{items[player.current_room]}\033[0m in the room.")

        print('-----------------------------------------------------------------')
        command = input("Enter your command: ").strip().lower()
        print('-----------------------------------------------------------------')

        if command.startswith("go "):
            direction = command[3:]
            player.move(direction)
        
        # elif command.startswith("get "):
        #     item = command[4:]
        #     if items[player.current_room] == item:
        #         player.add_item(item)
        #         print("You picked up the\033[94m", item + "\033[0m.")
        #         items[player.current_room] = None
        #     else:
        #         print("\033[91mThere is no item in the room.\033[0m")
        elif command.startswith("exit"):
            exit()

        else:
            print("\033[91mInvalid command!\033[0m")


# Run the game
welcome()
vault166()
