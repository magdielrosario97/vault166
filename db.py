import sqlite3

DB_NAME = "vault166.db"


def get_db_connection():
    """Establishes and returns a database connection with foreign key support."""
    conn = sqlite3.connect(DB_NAME)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def initialize_db(conn):
    """Initializes the database with required tables."""
    # SAVES table
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS saves (
            save_id INTEGER PRIMARY KEY AUTOINCREMENT,
            slot_name TEXT NOT NULL UNIQUE,
            last_save TEXT NOT NULL
        );
    """
    )

    # PLAYER_STATE table
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS player_state (
            save_id INTEGER PRIMARY KEY,
            current_room TEXT NOT NULL,
            health INTEGER NOT NULL,
            FOREIGN KEY (save_id) REFERENCES saves(save_id) ON DELETE CASCADE
        );
    """
    )

    # INVENTORY table
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS inventory (
            save_id INTEGER NOT NULL,
            item_name TEXT NOT NULL,
            PRIMARY KEY (save_id, item_name),
            FOREIGN KEY (save_id) REFERENCES saves(save_id) ON DELETE CASCADE
        );
    """
    )

    # ROOM_STATE table
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS room_state (
            save_id INTEGER NOT NULL,
            room_name TEXT NOT NULL,
            item TEXT,
            read_note INTEGER NOT NULL DEFAULT 0,
            PRIMARY KEY (save_id, room_name),
            FOREIGN KEY (save_id) REFERENCES saves(save_id) ON DELETE CASCADE
        );
    """
    )

    conn.commit()
