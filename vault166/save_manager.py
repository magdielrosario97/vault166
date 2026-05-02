from db import get_db_connection, initialize_db, save_game, load_game


class SaveManager:
    def __init__(self):
        self.conn = get_db_connection()
        initialize_db(self.conn)
