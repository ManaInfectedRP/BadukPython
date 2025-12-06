"""
AI Player for Baduk (Go)
"""

import random

class AIPlayer:
    """Simple AI player for Baduk."""
    
    def __init__(self, color, difficulty='medium'):
        """
        Initialize AI player.
        
        Args:
            color: 'black' or 'white'
            difficulty: 'easy', 'medium', or 'hard'
        """
        self.color = color
        self.difficulty = difficulty
    
    def get_move(self, board):
        """
        Get the AI's next move.
        
        Args:
            board: The game board
            
        Returns:
            Tuple (row, col) or 'pass'
        """
        legal_moves = board.get_legal_moves(self.color)
        
        if not legal_moves:
            return 'pass'
        
        if self.difficulty == 'easy':
            return self._get_random_move(legal_moves)
        elif self.difficulty == 'medium':
            return self._get_medium_move(board, legal_moves)
        else:  # hard
            return self._get_hard_move(board, legal_moves)
    
    def _get_random_move(self, legal_moves):
        """Get a random legal move."""
        return random.choice(legal_moves)
    
    def _get_medium_move(self, board, legal_moves):
        """Get a move with basic strategy."""
        # Prioritize capturing moves
        capture_moves = []
        
        for row, col in legal_moves:
            opponent_color = 'white' if self.color == 'black' else 'black'
            
            # Check if this move captures any stones - use try-finally for safety
            board.grid[row][col] = self.color
            
            try:
                captures = 0
                for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                    adj_row, adj_col = row + dr, col + dc
                    if board.is_valid_position(adj_row, adj_col):
                        if board.grid[adj_row][adj_col] == opponent_color:
                            group = board._get_group(adj_row, adj_col)
                            if board._count_liberties(group) == 0:
                                captures += len(group)
                
                if captures > 0:
                    capture_moves.append((row, col, captures))
            finally:
                board.grid[row][col] = None
        
        if capture_moves:
            # Choose the move that captures the most stones
            capture_moves.sort(key=lambda x: x[2], reverse=True)
            return (capture_moves[0][0], capture_moves[0][1])
        
        # If no captures, prioritize moves that increase our liberties
        liberty_moves = []
        
        for row, col in legal_moves:
            board.grid[row][col] = self.color
            try:
                group = board._get_group(row, col)
                liberties = board._count_liberties(group)
                liberty_moves.append((row, col, liberties))
            finally:
                board.grid[row][col] = None
        
        if liberty_moves:
            liberty_moves.sort(key=lambda x: x[2], reverse=True)
            # Choose from top 30% of moves to add some variety
            top_moves = liberty_moves[:max(1, len(liberty_moves) // 3)]
            chosen = random.choice(top_moves)
            return (chosen[0], chosen[1])
        
        return random.choice(legal_moves)
    
    def _get_hard_move(self, board, legal_moves):
        """Get a move with advanced strategy."""
        scored_moves = []
        
        for row, col in legal_moves:
            score = self._evaluate_move(board, row, col)
            scored_moves.append((row, col, score))
        
        if scored_moves:
            scored_moves.sort(key=lambda x: x[2], reverse=True)
            # Choose from top 20% of moves
            top_moves = scored_moves[:max(1, len(scored_moves) // 5)]
            chosen = random.choice(top_moves)
            return (chosen[0], chosen[1])
        
        return random.choice(legal_moves)
    
    def _evaluate_move(self, board, row, col):
        """
        Evaluate a move's strategic value.
        
        Args:
            board: The game board
            row: Row position
            col: Column position
            
        Returns:
            Score for the move (higher is better)
        """
        score = 0
        opponent_color = 'white' if self.color == 'black' else 'black'
        
        # Temporarily place stone - use try-finally to ensure state restoration
        board.grid[row][col] = self.color
        
        try:
            # Check captures
            captures = 0
            for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                adj_row, adj_col = row + dr, col + dc
                if board.is_valid_position(adj_row, adj_col):
                    if board.grid[adj_row][adj_col] == opponent_color:
                        group = board._get_group(adj_row, adj_col)
                        if board._count_liberties(group) == 0:
                            captures += len(group)
            
            score += captures * 10  # Capturing is valuable
            
            # Check our liberties
            my_group = board._get_group(row, col)
            my_liberties = board._count_liberties(my_group)
            score += my_liberties * 2
            
            # Check if we're threatening opponent groups
            threats = 0
            for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                adj_row, adj_col = row + dr, col + dc
                if board.is_valid_position(adj_row, adj_col):
                    if board.grid[adj_row][adj_col] == opponent_color:
                        group = board._get_group(adj_row, adj_col)
                        liberties = board._count_liberties(group)
                        if liberties <= 2:
                            threats += (3 - liberties) * 3
            
            score += threats
            
            # Prefer center and strategic points
            center = board.size // 2
            distance_from_center = abs(row - center) + abs(col - center)
            score += (board.size - distance_from_center) * 0.5
            
            # Prefer corner and edge points in opening
            move_count = len(board.move_history)
            if move_count < 20:
                # Corners and edges are valuable early
                if (row < 4 or row >= board.size - 4) and (col < 4 or col >= board.size - 4):
                    score += 5
        finally:
            # Always restore board state
            board.grid[row][col] = None
        
        return score
    
    def should_pass(self, board):
        """
        Decide if AI should pass.
        
        Args:
            board: The game board
            
        Returns:
            True if AI should pass, False otherwise
        """
        legal_moves = board.get_legal_moves(self.color)
        
        # Pass if no legal moves
        if not legal_moves:
            return True
        
        # For medium/hard difficulty, evaluate if passing is strategic
        if self.difficulty in ['medium', 'hard']:
            # Count empty spaces
            empty_count = sum(1 for row in range(board.size) 
                            for col in range(board.size) 
                            if board.grid[row][col] is None)
            
            # If very few empty spaces left, consider passing
            if empty_count < board.size * board.size * 0.1:
                # Evaluate if any move would improve our position significantly
                best_score = -1
                for row, col in legal_moves[:min(10, len(legal_moves))]:
                    score = self._evaluate_move(board, row, col)
                    if score > best_score:
                        best_score = score
                
                # Pass if best move doesn't add much value
                if best_score < 5:
                    return True
        
        return False
