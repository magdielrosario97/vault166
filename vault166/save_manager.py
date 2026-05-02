from db import get_db_connection, initialize_db, save_game, load_game


class SaveManager:
    def __init__(self):
        self.conn = get_db_connection()
        initialize_db(self.conn)

    def save(self, slot_name, player, rooms) -> str:
        save_game(self.conn, slot_name, player, rooms)
        message = f"Game saved to slot '{slot_name}'."
        return message
