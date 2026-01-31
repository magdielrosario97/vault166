'''
Vault 166 - A survival text-based python game
Created by Magdiel Rosario Orta
21 June 2023
'''

from map import build_map
from utils import welcome

# Game function
def vault166():

    # Game Initialization
    current_room = "Vacuum Room"
    inventory = []
    game_over = False
    rooms, room_connections, items = build_map()

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


def main():
    welcome()
    vault166()
    
if __name__ == "__main__":
    main()
