'''
Vault 166 - A survival text-based python game
Created by Magdiel Rosario Orta
21 June 2023
'''

from game import Game
from utils import welcome

# Game function
def vault166():
    # Game Initialization
    game = Game()
    # Game Loop
    game.run()

def main():
    welcome()
    vault166()
    
if __name__ == "__main__":
    main()
