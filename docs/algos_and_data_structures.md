# Algorithms and Data Structures Enhancement

## Overview

This document describes the Algorithms and Data Structures enhancement for the Vault 166 project. The goal of this enhancement was to replace rigid, hardcoded gameplay logic with flexible, rule-based systems and efficient data structures that evaluate player state during movement and interaction.

The design builds on a modular architecture and focuses on scalability, clarity, and maintainability rather than raw performance.

## Implemented Data Structures

The following data structures are used throughout the project:

- **Set-based inventory**
   The player inventory is implemented as a set, enabling constant-time membership checks when evaluating hazards, locks, and boss conditions.
- **Graph-style room layout**
   Rooms are modeled as nodes in a graph, with directional connections stored in dictionaries. This structure supports clear movement logic and easy expansion of the map.
- **Dictionary-driven rule evaluation**
   Environmental hazards, locks, and special conditions are evaluated using centralized rule functions rather than scattered conditional logic.
- **Tokenized command input**
   Player input is processed into tokens and normalized before being evaluated, allowing flexible command syntax while maintaining predictable behavior.

## Algorithms Used

### Command Normalization and Resolution

Player input is normalized using the following steps:

1. Tokenization of input text
2. Alias resolution for directional commands
3. Prefix matching for commands and items
4. Ambiguity detection to prevent unintended actions

This approach allows for short and partial inputs while rejecting ambiguous commands to maintain clarity.

### Rule-Based Movement Evaluation

Movement into a room is evaluated using a sequence of rule checks:

- Darkness checks that may block movement and apply damage
- Lock checks that require specific items
- Hazard evaluation upon room entry
- Boss room condition checks based on inventory state

Each rule is implemented as a focused function that returns a clear result, keeping the game loop readable and modular.

### State Evaluation and Outcome Handling

Player state (health, inventory, location) is evaluated at key points in the game loop. Outcomes such as damage, blocked movement, or game termination are handled immediately, ensuring consistent and predictable gameplay flow.

## Benefits of This Approach

- Improved readability by separating rules from control flow
- Easier extension of game mechanics without rewriting core logic
- Clear demonstration of algorithmic thinking and data structure selection
- Reduced complexity in the main game loop
