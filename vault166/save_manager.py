from vault166.db import (
    DB_NAME,
    get_db_connection,
    initialize_db,
    view_saves,
    save_game,
    load_game,
    delete_game,
)


class SaveManager:
    def __init__(self, db_path: str = DB_NAME):
        self.conn = get_db_connection(db_path)
        initialize_db(self.conn)

    def view(self) -> list[tuple[str, str]]:
        """Returns a list of save slots with their last save time."""
        return view_saves(self.conn)

    def save(self, slot_name, player, rooms) -> str:
        """Saves the current game state to the database."""
        save_game(self.conn, slot_name, player, rooms)
        message = f"Game saved to slot '{slot_name}'."
        return message

    def load(self, slot_name, player, rooms) -> tuple[bool, str]:
        """Loads a game state from the database."""
        success = load_game(self.conn, slot_name, player, rooms)
        if success:
            message = f"Game loaded from slot '{slot_name}'."
        else:
            message = f"Save slot '{slot_name}' not found."

        return success, message

    def delete(self, slot_name) -> tuple[bool, str]:
        """Deletes a save slot from the database."""
        success = delete_game(self.conn, slot_name)
        if success:
            message = f"Save slot '{slot_name}' deleted."
        else:
            message = f"Save slot '{slot_name}' not found."

        return success, message

    def close(self) -> None:
        """Closes the database connection."""
        self.conn.close()
