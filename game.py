"""
Baduk (Go) Game Controller
"""

from board import Board
from ai_player import AIPlayer

class BadukGame:
    """Main game controller for Baduk."""
    
    def __init__(self, mode='multiplayer', board_size=19, ai_difficulty='medium', network_role=None, network_connection=None):
        """
        Initialize a Baduk game.
        
        Args:
            mode: 'singleplayer', 'multiplayer', or 'network'
            board_size: Size of the board (9, 13, or 19)
            ai_difficulty: 'easy', 'medium', or 'hard' (for singleplayer)
            network_role: 'host' or 'client' (for network mode)
            network_connection: GameServer or GameClient instance (for network mode)
        """
        self.mode = mode
        self.board = Board(board_size)
        self.current_player = 'black'
        self.consecutive_passes = 0
        self.game_over = False
        
        # Initialize AI if singleplayer
        self.ai = None
        if mode == 'singleplayer':
            self.ai = AIPlayer('white', ai_difficulty)
        
        # Network multiplayer support
        self.network_role = network_role
        self.network_connection = network_connection
    
    def switch_player(self):
        """Switch to the other player."""
        self.current_player = 'white' if self.current_player == 'black' else 'black'
    
    def make_move(self, row, col):
        """
        Make a move at the specified position.
        
        Args:
            row: Row position
            col: Column position
            
        Returns:
            True if move was successful, False otherwise
        """
        if self.game_over:
            return False
        
        if self.board.place_stone(row, col, self.current_player):
            self.consecutive_passes = 0
            self.switch_player()
            return True
        
        return False
    
    def pass_turn(self):
        """Current player passes their turn."""
        if self.game_over:
            return
        
        self.board.pass_turn()
        self.consecutive_passes += 1
        
        if self.consecutive_passes >= 2:
            self.game_over = True
        
        self.switch_player()
    
    def get_ai_move(self):
        """
        Get the AI's move (for singleplayer mode).
        
        Returns:
            Tuple (row, col) or 'pass'
        """
        if self.ai and self.current_player == self.ai.color:
            if self.ai.should_pass(self.board):
                return 'pass'
            return self.ai.get_move(self.board)
        
        return None
    
    def is_game_over(self):
        """Check if the game is over."""
        return self.game_over
    
    def get_winner(self):
        """
        Get the winner of the game.
        
        Returns:
            Dictionary with scores and winner
        """
        if not self.game_over:
            return None
        
        scores = self.board.calculate_score()
        
        # Add komi (compensation for white)
        komi = 6.5
        scores['white'] += komi
        
        result = {
            'black_score': scores['black'],
            'white_score': scores['white'],
            'winner': 'black' if scores['black'] > scores['white'] else 'white',
            'margin': abs(scores['black'] - scores['white'])
        }
        
        return result
    
    def display_board(self):
        """Display the current board state."""
        self.board.display()
        print(f"\nCurrent player: {self.current_player.upper()}")
        
        if self.game_over:
            result = self.get_winner()
            print("\n" + "="*50)
            print("GAME OVER")
            print("="*50)
            print(f"Black score: {result['black_score']:.1f}")
            print(f"White score: {result['white_score']:.1f}")
            print(f"Winner: {result['winner'].upper()} by {result['margin']:.1f} points")
            print("="*50)
    
    def get_legal_moves(self):
        """Get all legal moves for the current player."""
        return self.board.get_legal_moves(self.current_player)
    
    def undo_last_move(self):
        """Undo the last move (basic implementation)."""
        # This is a simplified version - full implementation would need more complex state management
        if not self.board.move_history:
            return False
        
        # For now, we'll just indicate it's not fully implemented
        return False
