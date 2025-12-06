# BadukPython
Baduk (Go) Singleplayer / Multiplayer Game in Python

## Overview
A complete implementation of the Baduk (Go) board game with singleplayer (vs AI), local multiplayer, and network multiplayer modes, featuring a graphical user interface for an intuitive playing experience.

## Features
- **Graphical User Interface**: Click on the board to place stones instead of typing coordinates
- **Singleplayer Mode**: Play against an AI opponent with three difficulty levels (Easy, Medium, Hard)
- **Local Multiplayer Mode**: Play on the same computer against another human player
- **Network Multiplayer Mode**: Play over the network with another player
  - Host a game and share your IP:Port with another player
  - Join a game by entering the host's IP:Port
  - Real-time move synchronization
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

#### Singleplayer (vs AI)
1. Click "Singleplayer (vs AI)"
2. Select board size from the dialog (9x9, 13x13, or 19x19)
3. Choose AI difficulty (Easy, Medium, or Hard)
4. Click on intersections on the board to place your stones
5. Click "Pass" button to skip your turn
6. Click "Main Menu" to return to the main menu
7. Game ends when both players pass consecutively, showing final scores

#### Local Multiplayer
1. Click "Multiplayer (local)"
2. Select board size from the dialog
3. Take turns clicking on the board to place stones
4. Click "Pass" button to skip your turn

#### Network Multiplayer
**To Host a Game:**
1. Click "Network Multiplayer"
2. Click "Host Game"
3. Select board size from the dialog
4. Enter a port number (default: 5555)
5. The game will display your IP address and port (e.g., `192.168.1.100:5555`)
6. Click "Copy to Clipboard" to copy the connection information
7. Share this information with the other player
8. Wait for the other player to connect
9. Once connected, you play as Black and go first

**To Join a Game:**
1. Click "Network Multiplayer"
2. Click "Join Game"
3. Select board size from the dialog (must match the host's selection)
4. Enter the host's IP:Port (e.g., `192.168.1.100:5555`)
5. Wait for connection to establish
6. Once connected, you play as White and go second

### Terminal Mode
1. Choose game mode (Singleplayer or Local Multiplayer)
2. Select board size (9x9, 13x13, or 19x19)
3. If playing singleplayer, choose AI difficulty
4. Take turns placing stones on the board
5. Enter moves as "row column" (e.g., "3 4")
6. Type "pass" to skip your turn
7. Game ends when both players pass consecutively

**Note:** Network multiplayer is only available in GUI mode.

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
- `network.py` - Network multiplayer server and client implementation

## Requirements
- Python 3.11.*
- Tkinter (for GUI mode)
- Network connectivity (for network multiplayer mode)

**Note:** The code uses only Python standard library features. Tkinter is included with most Python installations, but may need to be installed separately on some Linux distributions.

## Network Multiplayer Setup

### Firewall Configuration
For network multiplayer to work, the host must ensure that:
- The selected port (default: 5555) is open in the firewall
- The port is not blocked by antivirus software or security settings

**Windows:**
```powershell
# Allow port 5555 through Windows Firewall
netsh advfirewall firewall add rule name="Baduk Game" dir=in action=allow protocol=TCP localport=5555
```

**Linux (ufw):**
```bash
# Allow port 5555 through firewall
sudo ufw allow 5555/tcp
```

**macOS:**
- Go to System Preferences > Security & Privacy > Firewall > Firewall Options
- Add Python or the specific application to the allowed list

### Network Configuration
- **Local Network (LAN):** Players should be on the same local network for best performance
- **Internet Play:** The host may need to configure port forwarding on their router to play over the internet
- **IP Address:** The displayed IP address is your local network IP. For internet play, share your public IP address (findable at whatismyip.com)

### Troubleshooting
- **Cannot connect:** Verify the IP address and port are correct
- **Connection refused:** Check that the host's firewall allows incoming connections on the specified port
- **Disconnected during game:** Ensure stable network connection between both players
- **Wrong IP displayed:** If the displayed IP is incorrect, the host can manually check their IP address using `ipconfig` (Windows) or `ifconfig`/`ip addr` (Linux/macOS)
