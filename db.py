import sqlite3
from datetime import datetime

DB_NAME = "vault166.db"


def get_db_connection() -> sqlite3.Connection:
    """Establishes and returns a database connection with foreign key support."""
    conn = sqlite3.connect(DB_NAME)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def initialize_db(conn) -> None:
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


def save_game(conn, slot_name, player, rooms) -> None:
    """Saves the current game state to the database."""
    now = datetime.now().isoformat(timespec="seconds")

    row = conn.execute(
        "SELECT save_id FROM saves WHERE slot_name = ?;",
        (slot_name,),
    ).fetchone()

    if row is None:
        conn.execute(
            "INSERT INTO saves (slot_name, last_save) VALUES (?, ?);",
            (slot_name, now),
        )
        save_id = conn.execute(
            "SELECT save_id FROM saves WHERE slot_name = ?;",
            (slot_name,),
        ).fetchone()[0]
    else:
        save_id = row[0]
        conn.execute(
            "UPDATE saves SET last_save = ? WHERE save_id = ?;",
            (now, save_id),
        )

    conn.execute(
        """
        INSERT INTO player_state (save_id, current_room, health)
        VALUES (?, ?, ?)
        ON CONFLICT(save_id) DO UPDATE SET
            current_room = excluded.current_room,
            health = excluded.health;
        """,
        (save_id, player.current_room.name, player.health),
    )

    conn.execute("DELETE FROM inventory WHERE save_id = ?;", (save_id,))
    for item_name in sorted(player.inventory):
        conn.execute(
            "INSERT INTO inventory (save_id, item_name) VALUES (?, ?);",
            (save_id, item_name),
        )

    conn.execute("DELETE FROM room_state WHERE save_id = ?;", (save_id,))
    for room in rooms.values():
        conn.execute(
            "INSERT INTO room_state (save_id, room_name, item, read_note) VALUES (?, ?, ?, ?);",
            (save_id, room.name, room.item, 1 if room.read_note else 0),
        )

    conn.commit()


def load_game(conn, slot_name, rooms, player) -> bool:
    """Loads a save slot into the current game objects.
    Returns True if loaded, False if slot not found."""
    row = conn.execute(
        "SELECT save_id FROM saves WHERE slot_name = ?;",
        (slot_name,),
    ).fetchone()

    if row is None:
        return False

    save_id = row[0]

    player_row = conn.execute(
        "SELECT current_room, health FROM player_state WHERE save_id = ?;",
        (save_id,),
    ).fetchone()

    if player_row is None:
        return False

    current_room_name = player_row[0]
    health = player_row[1]

    if current_room_name not in rooms:
        return False

    player.current_room = rooms[current_room_name]
    player.health = int(health)

    inventory_rows = conn.execute(
        "SELECT item_name FROM inventory WHERE save_id = ?;",
        (save_id,),
    ).fetchall()

    player.inventory.clear()
    for inventory_row in inventory_rows:
        player.inventory.add(inventory_row[0])

    room_rows = conn.execute(
        "SELECT room_name, item, read_note FROM room_state WHERE save_id = ?;",
        (save_id,),
    ).fetchall()

    for room_state in room_rows:
        room_name = room_state[0]
        if room_name in rooms:
            rooms[room_name].item = room_state[1]
            rooms[room_name].read_note = bool(room_state[2])

    return True
