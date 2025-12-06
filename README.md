# BadukPython
Baduk (Go) Singleplayer / Multiplayer Game in Python

## Overview
A complete implementation of the Baduk (Go) board game with both singleplayer (vs AI) and multiplayer (local) modes, featuring a graphical user interface for an intuitive playing experience.

## Features
- **Graphical User Interface**: Click on the board to place stones instead of typing coordinates
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
- **Visual Elements**: Traditional Go board appearance with star points, clear stone rendering, and move highlighting

## Installation

### Prerequisites
- Python 3.11.* is required
- Tkinter (usually included with Python, but may need separate installation on some Linux systems)
- This game uses only Python's standard library

```bash
# Verify Python version
python3 --version  # Should show Python 3.11.x

# Clone the repository
git clone https://github.com/ManaInfectedRP/BadukPython.git
cd BadukPython
```

If you don't have Python 3.11, you can install it using:
- **Ubuntu/Debian**: `sudo apt-get install python3.11 python3-tk`
- **macOS** (with Homebrew): `brew install python@3.11 python-tk@3.11`
- **Windows**: Download from [python.org](https://www.python.org/downloads/) (includes tkinter by default)

## Usage

### GUI Mode (Default)
Run the game with the graphical interface:

```bash
python3 main.py
# or if you have multiple Python versions
python3.11 main.py
```

### Terminal Mode (Optional)
If you prefer the original terminal-based interface:

```bash
python3 main.py --terminal
```

## How to Play

### GUI Mode
1. Click on a game mode button (Singleplayer or Multiplayer)
2. Select board size from the dialog (9x9, 13x13, or 19x19)
3. If playing singleplayer, choose AI difficulty
4. Click on intersections on the board to place your stones
5. Click "Pass" button to skip your turn
6. Click "Main Menu" to return to the main menu
7. Game ends when both players pass consecutively, showing final scores

### Terminal Mode
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
- `main.py` - Main entry point (launches GUI by default, terminal mode with --terminal flag)
- `gui.py` - Graphical user interface implementation using Tkinter
- `game.py` - Game controller and state management
- `board.py` - Board logic, move validation, and scoring
- `ai_player.py` - AI opponent with strategic move evaluation

## Requirements
- Python 3.11.*
- Tkinter (for GUI mode)

**Note:** The code is compatible with Python 3.11 and uses only standard library features. Tkinter is included with most Python installations, but may need to be installed separately on some Linux distributions.
