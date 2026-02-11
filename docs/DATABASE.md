# Vault 166 Database Enhancement

## Planned Enhancements

- Add SQLite persistence for game state.
- Support saving and loading from a named slot.
- Persist player state including current room, health, and inventory.
- Persist room state so picked up items do not respawn and notes do not reprint.
- Add basic validation and error handling to prevent corrupted saves from breaking gameplay.
- Document the database schema, relationships, and persistence workflow.

## Overview

This enhancement introduces SQLite-based persistence to Vault 166. The goal is to allow multiple save slots and restore full runtime state including player data, inventory, and room state while keeping static world definitions in code.

## Schema

The database consists of four related tables: SAVES, PLAYER_STATE, INVENTORY, and ROOM_STATE. The schema separates static world structure from dynamic runtime state.

![Vault 166 Database ERD](vault166_erd.png)

Note: INVENTORY and ROOM_STATE use composite primary keys (`save_id`, `item_name`) and (`save_id`, `room_name`) respectively to uniquely identify rows per save slot.
