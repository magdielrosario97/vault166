# Vault 166 Architecture

This document describes the current structure of Vault 166 during the Software Engineering and Design enhancement.

The goal of this enhancement is to improve code organization and separation of concerns while keeping gameplay behavior the same.

## Current focus

At this stage, the project is being refactored from a single-script implementation into a modular structure.

The refactor focuses on:

- separating the game loop from supporting logic
- centralizing player state
- isolating world data from gameplay rules

## Modules

- Entry file  
  Starts the game and invokes the main loop.

- game.py  
  Will own the main game loop and command processing.

- player.py  
  Will store player-related state such as current room and inventory.

- map.py  
  Will store world data including rooms, connections, and items.

- utils.py  
  Will contain shared output helpers.

## Scope

This document reflects the current refactor work only. Gameplay systems and features are not being changed as part of this enhancement.
