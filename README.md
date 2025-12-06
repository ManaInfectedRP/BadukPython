# BadukPython
Baduk (Go) Singleplayer / Multiplayer Game in Python

## Overview
A complete implementation of the Baduk (Go) board game with both singleplayer (vs AI) and multiplayer (local) modes.

## Features
- **Singleplayer Mode**: Play against an AI opponent with three difficulty levels (Easy, Medium, Hard)
- **Multiplayer Mode**: Play locally against another human player
- **Multiple Board Sizes**: Choose from 9x9, 13x13, or 19x19 boards
- **Full Game Rules**: 
  - Stone placement and capture mechanics
  - Liberty counting
  - Ko rule enforcement
  - Suicide prevention
  - Area scoring with komi
- **Strategic AI**: The AI uses multiple heuristics including capture detection, liberty counting, and positional evaluation

## Installation
This game uses only Python's standard library, so no external dependencies are required.

```bash
# Clone the repository
git clone https://github.com/ManaInfectedRP/BadukPython.git
cd BadukPython
```

## Usage
Run the game with:

```bash
python main.py
```

## How to Play
1. Choose game mode (Singleplayer or Multiplayer)
2. Select board size (9x9, 13x13, or 19x19)
3. If playing singleplayer, choose AI difficulty
4. Take turns placing stones on the board
5. Enter moves as "row column" (e.g., "3 4")
6. Type "pass" to skip your turn
7. Game ends when both players pass consecutively

## Game Rules
- Black plays first
- Capture opponent stones by surrounding them (removing all liberties)
- Suicide moves (placing a stone with no liberties) are not allowed
- Ko rule: You cannot immediately recapture a single stone that was just captured
- Score is calculated using area scoring + captured stones + 6.5 komi for white

## File Structure
- `main.py` - Main entry point and game loop
- `game.py` - Game controller and state management
- `board.py` - Board logic, move validation, and scoring
- `ai_player.py` - AI opponent with strategic move evaluation

## Requirements
- Python 3.6 or higher
