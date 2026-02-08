# Vault 166 Architecture

This document describes the current architecture of Vault 166 following the Software Engineering and Design enhancement.

The goal of this enhancement was to improve code organization, separation of concerns, and maintainability while preserving the core gameplay experience.

## Architectural Focus

The project has been refactored from an earlier single-script implementation into a modular structure with clearly defined responsibilities.

The refactor focuses on:

- separating the main game loop from supporting logic
- centralizing player state and inventory management
- isolating gameplay rules from control flow
- improving input handling and command normalization

## Modules

- Entry file (`vault166.py`)  
  Acts as the program entry point and starts the game loop.

- `game.py`  
  Owns the main game loop, command dispatch, and output flow.

- `input_parser.py`  
  Handles command parsing, normalization, alias resolution, and ambiguity detection.

- `player.py`  
  Stores player-related state such as current room, inventory, and health.

- `room.py`  
  Defines room state and properties, including connections, hazards, and items.

- `rules.py`  
  Encapsulates gameplay rules such as environmental hazards, locked areas, and boss conditions.

- `map.py`  
  Defines the vault layout and provides a static minimap reference.

- `utils.py`  
  Contains shared output helpers and formatting utilities.

## Scope

This architecture reflects the current implemented design. Gameplay mechanics were not fundamentally altered, but usability, input handling, and internal structure were improved to support clarity, extensibility, and maintainability.
