"""
Main entry point for Baduk (Go) game
"""

from game import BadukGame

def display_menu():
    """Display the main menu."""
    print("\n" + "="*50)
    print("BADUK (GO) GAME")
    print("="*50)
    print("1. Singleplayer (vs AI)")
    print("2. Multiplayer (local)")
    print("3. Quit")
    print("="*50)

def select_board_size():
    """Let user select board size."""
    print("\nSelect board size:")
    print("1. 9x9 (Small)")
    print("2. 13x13 (Medium)")
    print("3. 19x19 (Standard)")
    
    while True:
        choice = input("Enter choice (1-3): ").strip()
        if choice == '1':
            return 9
        elif choice == '2':
            return 13
        elif choice == '3':
            return 19
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

def select_difficulty():
    """Let user select AI difficulty."""
    print("\nSelect AI difficulty:")
    print("1. Easy")
    print("2. Medium")
    print("3. Hard")
    
    while True:
        choice = input("Enter choice (1-3): ").strip()
        if choice == '1':
            return 'easy'
        elif choice == '2':
            return 'medium'
        elif choice == '3':
            return 'hard'
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

def get_player_move(game):
    """Get move input from human player."""
    print("\nEnter your move:")
    print("- Enter row and column (e.g., '3 4')")
    print("- Enter 'pass' to pass your turn")
    print("- Enter 'quit' to end the game")
    
    while True:
        move_input = input(f"{game.current_player.upper()} move: ").strip().lower()
        
        if move_input == 'quit':
            return 'quit'
        
        if move_input == 'pass':
            return 'pass'
        
        try:
            parts = move_input.split()
            if len(parts) != 2:
                print("Invalid input. Enter row and column separated by space (e.g., '3 4')")
                continue
            
            row, col = int(parts[0]), int(parts[1])
            
            if not game.board.is_valid_position(row, col):
                print(f"Invalid position. Must be between 0 and {game.board.size - 1}")
                continue
            
            return (row, col)
        
        except ValueError:
            print("Invalid input. Enter numbers for row and column.")

def play_game(mode, board_size, ai_difficulty=None):
    """
    Play a game of Baduk.
    
    Args:
        mode: 'singleplayer' or 'multiplayer'
        board_size: Size of the board
        ai_difficulty: AI difficulty level (for singleplayer)
    """
    game = BadukGame(mode, board_size, ai_difficulty)
    
    print(f"\n{'='*50}")
    print(f"Starting {mode.upper()} game on {board_size}x{board_size} board")
    if mode == 'singleplayer':
        print(f"AI difficulty: {ai_difficulty.upper()}")
    print(f"{'='*50}\n")
    
    print("Game Rules:")
    print("- Black plays first")
    print("- Capture opponent stones by surrounding them")
    print("- No suicide moves (placing a stone with no liberties)")
    print("- Ko rule: Cannot immediately recapture a single stone")
    print("- Game ends when both players pass consecutively")
    print(f"{'='*50}\n")
    
    # Main game loop
    while not game.is_game_over():
        game.display_board()
        
        # Check if it's AI's turn
        if mode == 'singleplayer' and game.current_player == 'white':
            print("\nAI is thinking...")
            ai_move = game.get_ai_move()
            
            if ai_move == 'pass':
                print("AI passes.")
                game.pass_turn()
            else:
                row, col = ai_move
                if game.make_move(row, col):
                    print(f"AI plays at ({row}, {col})")
                else:
                    print("AI made an invalid move (this shouldn't happen)")
            
            input("\nPress Enter to continue...")
        else:
            # Human player's turn
            move = get_player_move(game)
            
            if move == 'quit':
                print("\nGame ended by player.")
                return
            
            if move == 'pass':
                game.pass_turn()
                print(f"{game.current_player.upper()} passed.")
            else:
                row, col = move
                if game.make_move(row, col):
                    print(f"Move placed at ({row}, {col})")
                else:
                    print("Invalid move. Try again.")
                    continue
    
    # Game over - display final results
    game.display_board()
    
    play_again = input("\nPlay again? (y/n): ").strip().lower()
    if play_again == 'y':
        main()

def main():
    """Main function."""
    while True:
        display_menu()
        choice = input("Enter choice (1-3): ").strip()
        
        if choice == '1':
            # Singleplayer mode
            board_size = select_board_size()
            ai_difficulty = select_difficulty()
            play_game('singleplayer', board_size, ai_difficulty)
            break
        
        elif choice == '2':
            # Multiplayer mode
            board_size = select_board_size()
            play_game('multiplayer', board_size)
            break
        
        elif choice == '3':
            print("\nThanks for playing!")
            break
        
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

if __name__ == "__main__":
    main()
