"""
Baduk (Go) Board Implementation
"""

class Board:
    """Represents a Baduk board with stone placement and capture logic."""
    
    def __init__(self, size=19):
        """
        Initialize a Baduk board.
        
        Args:
            size: Board size (default 19x19, can be 9x9 or 13x13)
        """
        self.size = size
        self.grid = [[None for _ in range(size)] for _ in range(size)]
        self.captured = {'black': 0, 'white': 0}
        self.move_history = []
        self.ko_point = None  # For ko rule enforcement
        
    def is_valid_position(self, row, col):
        """Check if position is within board bounds."""
        return 0 <= row < self.size and 0 <= col < self.size
    
    def get_stone(self, row, col):
        """Get the stone color at a position."""
        if not self.is_valid_position(row, col):
            return None
        return self.grid[row][col]
    
    def place_stone(self, row, col, color):
        """
        Place a stone on the board.
        
        Args:
            row: Row position
            col: Column position
            color: 'black' or 'white'
            
        Returns:
            True if placement was successful, False otherwise
        """
        if not self.is_valid_position(row, col):
            return False
        
        if self.grid[row][col] is not None:
            return False
        
        # Check ko rule
        if self.ko_point == (row, col):
            return False
        
        # Temporarily place stone
        self.grid[row][col] = color
        
        # Check for captures
        opponent_color = 'white' if color == 'black' else 'black'
        captured_stones = []
        
        # Check all adjacent opponent groups
        for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            adj_row, adj_col = row + dr, col + dc
            if self.is_valid_position(adj_row, adj_col):
                if self.grid[adj_row][adj_col] == opponent_color:
                    group = self._get_group(adj_row, adj_col)
                    if self._count_liberties(group) == 0:
                        captured_stones.extend(group)
        
        # Remove captured stones
        for stone_row, stone_col in captured_stones:
            self.grid[stone_row][stone_col] = None
            self.captured[opponent_color] += 1
        
        # Check if move is suicide (no liberties and no captures)
        if not captured_stones:
            my_group = self._get_group(row, col)
            if self._count_liberties(my_group) == 0:
                self.grid[row][col] = None
                return False
        
        # Update ko point
        if len(captured_stones) == 1:
            self.ko_point = captured_stones[0]
        else:
            self.ko_point = None
        
        # Record move
        self.move_history.append((row, col, color, len(captured_stones)))
        
        return True
    
    def _get_group(self, row, col):
        """Get all stones in the connected group."""
        color = self.grid[row][col]
        if color is None:
            return []
        
        group = []
        visited = set()
        stack = [(row, col)]
        
        while stack:
            r, c = stack.pop()
            if (r, c) in visited:
                continue
            visited.add((r, c))
            
            if not self.is_valid_position(r, c):
                continue
            if self.grid[r][c] != color:
                continue
            
            group.append((r, c))
            
            for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                stack.append((r + dr, c + dc))
        
        return group
    
    def _count_liberties(self, group):
        """Count the number of liberties for a group."""
        liberties = set()
        
        for row, col in group:
            for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                adj_row, adj_col = row + dr, col + dc
                if self.is_valid_position(adj_row, adj_col):
                    if self.grid[adj_row][adj_col] is None:
                        liberties.add((adj_row, adj_col))
        
        return len(liberties)
    
    def get_legal_moves(self, color):
        """Get all legal moves for a color."""
        legal_moves = []
        
        for row in range(self.size):
            for col in range(self.size):
                if self._is_legal_move(row, col, color):
                    legal_moves.append((row, col))
        
        return legal_moves
    
    def _is_legal_move(self, row, col, color):
        """Check if a move is legal."""
        if not self.is_valid_position(row, col):
            return False
        
        if self.grid[row][col] is not None:
            return False
        
        if self.ko_point == (row, col):
            return False
        
        # Create a temporary copy to test the move
        original_grid = [row[:] for row in self.grid]
        original_ko = self.ko_point
        
        self.grid[row][col] = color
        
        # Check for captures
        opponent_color = 'white' if color == 'black' else 'black'
        has_captures = False
        
        for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            adj_row, adj_col = row + dr, col + dc
            if self.is_valid_position(adj_row, adj_col):
                if self.grid[adj_row][adj_col] == opponent_color:
                    group = self._get_group(adj_row, adj_col)
                    if self._count_liberties(group) == 0:
                        has_captures = True
                        break
        
        # Check if move is suicide
        is_legal = True
        if not has_captures:
            my_group = self._get_group(row, col)
            if self._count_liberties(my_group) == 0:
                is_legal = False
        
        # Restore original state
        self.grid = original_grid
        self.ko_point = original_ko
        
        return is_legal
    
    def calculate_score(self):
        """
        Calculate the score using area scoring.
        
        Note: This implementation uses visited set to track processed regions,
        making it O(n^2) where n is board size, which is efficient for standard
        board sizes (9x9, 13x13, 19x19).
        
        Returns:
            Dictionary with 'black' and 'white' scores
        """
        territory = {'black': 0, 'white': 0, 'neutral': 0}
        visited = set()
        
        for row in range(self.size):
            for col in range(self.size):
                if self.grid[row][col] is None and (row, col) not in visited:
                    empty_region, borders = self._get_empty_region(row, col)
                    visited.update(empty_region)
                    
                    if len(borders) == 1:
                        color = list(borders)[0]
                        territory[color] += len(empty_region)
                    else:
                        territory['neutral'] += len(empty_region)
        
        # Count stones on board
        for row in range(self.size):
            for col in range(self.size):
                if self.grid[row][col] == 'black':
                    territory['black'] += 1
                elif self.grid[row][col] == 'white':
                    territory['white'] += 1
        
        # Add captured stones
        territory['black'] += self.captured['white']
        territory['white'] += self.captured['black']
        
        return territory
    
    def _get_empty_region(self, row, col):
        """Get all empty points in a connected region and their bordering colors."""
        region = []
        borders = set()
        visited = set()
        stack = [(row, col)]
        
        while stack:
            r, c = stack.pop()
            if (r, c) in visited:
                continue
            visited.add((r, c))
            
            if not self.is_valid_position(r, c):
                continue
            
            if self.grid[r][c] is None:
                region.append((r, c))
                for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                    stack.append((r + dr, c + dc))
            else:
                borders.add(self.grid[r][c])
        
        return region, borders
    
    def display(self):
        """Display the board in text format."""
        print("\n  ", end="")
        for col in range(self.size):
            print(f"{col:2}", end=" ")
        print()
        
        for row in range(self.size):
            print(f"{row:2} ", end="")
            for col in range(self.size):
                stone = self.grid[row][col]
                if stone == 'black':
                    print(" ●", end=" ")
                elif stone == 'white':
                    print(" ○", end=" ")
                else:
                    print(" ·", end=" ")
            print()
        
        print(f"\nCaptured - Black: {self.captured['white']}, White: {self.captured['black']}")
    
    def pass_turn(self):
        """Record a pass."""
        self.move_history.append(('pass', None, None, 0))
    
    def get_last_move(self):
        """Get the last move played."""
        if self.move_history:
            return self.move_history[-1]
        return None
