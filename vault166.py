"""
Vault 166 - A survival text-based python game
Created by Magdiel Rosario Orta
21 June 2023

Revised by Magdiel Rosario Orta
8 February 2026
"""

from game import Game
from utils import welcome
from db import get_db_connection, initialize_db


def vault166():
    conn = get_db_connection()
    initialize_db(conn)
    conn.close()

    game = Game()
    game.run()


def main():
    welcome()
    vault166()


if __name__ == "__main__":
    main()
