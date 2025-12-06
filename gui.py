"""
GUI Implementation for Baduk (Go) Game using Tkinter
"""

import tkinter as tk
from tkinter import messagebox, simpledialog
from game import BadukGame
import threading
import time


class BadukGUI:
    """Main GUI class for the Baduk game."""
    
    def __init__(self, root):
        """Initialize the GUI."""
        self.root = root
        self.root.title("Baduk (Go) Game")
        self.root.resizable(False, False)
        
        self.game = None
        self.cell_size = 40
        self.board_margin = 40
        self.stone_radius = 15
        
        self.show_main_menu()
    
    def show_main_menu(self):
        """Display the main menu."""
        # Clear the window
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Center the window
        self.root.geometry("400x300")
        
        # Title
        title_label = tk.Label(
            self.root,
            text="BADUK (GO) GAME",
            font=("Arial", 24, "bold")
        )
        title_label.pack(pady=30)
        
        # Menu buttons
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=20)
        
        singleplayer_btn = tk.Button(
            button_frame,
            text="Singleplayer (vs AI)",
            font=("Arial", 14),
            width=20,
            height=2,
            command=self.start_singleplayer
        )
        singleplayer_btn.pack(pady=10)
        
        multiplayer_btn = tk.Button(
            button_frame,
            text="Multiplayer (local)",
            font=("Arial", 14),
            width=20,
            height=2,
            command=self.start_multiplayer
        )
        multiplayer_btn.pack(pady=10)
        
        quit_btn = tk.Button(
            button_frame,
            text="Quit",
            font=("Arial", 14),
            width=20,
            height=2,
            command=self.root.quit
        )
        quit_btn.pack(pady=10)
    
    def start_singleplayer(self):
        """Start a singleplayer game."""
        board_size = self.select_board_size()
        if board_size is None:
            return
        
        ai_difficulty = self.select_difficulty()
        if ai_difficulty is None:
            return
        
        self.game = BadukGame('singleplayer', board_size, ai_difficulty)
        self.show_game_board()
    
    def start_multiplayer(self):
        """Start a multiplayer game."""
        board_size = self.select_board_size()
        if board_size is None:
            return
        
        self.game = BadukGame('multiplayer', board_size)
        self.show_game_board()
    
    def select_board_size(self):
        """Show board size selection dialog."""
        dialog = tk.Toplevel(self.root)
        dialog.title("Select Board Size")
        dialog.geometry("300x200")
        dialog.transient(self.root)
        dialog.grab_set()
        
        result = {'size': None}
        
        tk.Label(
            dialog,
            text="Select Board Size:",
            font=("Arial", 14)
        ).pack(pady=20)
        
        def select_size(size):
            result['size'] = size
            dialog.destroy()
        
        tk.Button(
            dialog,
            text="9x9 (Small)",
            font=("Arial", 12),
            width=15,
            command=lambda: select_size(9)
        ).pack(pady=5)
        
        tk.Button(
            dialog,
            text="13x13 (Medium)",
            font=("Arial", 12),
            width=15,
            command=lambda: select_size(13)
        ).pack(pady=5)
        
        tk.Button(
            dialog,
            text="19x19 (Standard)",
            font=("Arial", 12),
            width=15,
            command=lambda: select_size(19)
        ).pack(pady=5)
        
        self.root.wait_window(dialog)
        return result['size']
    
    def select_difficulty(self):
        """Show AI difficulty selection dialog."""
        dialog = tk.Toplevel(self.root)
        dialog.title("Select AI Difficulty")
        dialog.geometry("300x200")
        dialog.transient(self.root)
        dialog.grab_set()
        
        result = {'difficulty': None}
        
        tk.Label(
            dialog,
            text="Select AI Difficulty:",
            font=("Arial", 14)
        ).pack(pady=20)
        
        def select_difficulty(difficulty):
            result['difficulty'] = difficulty
            dialog.destroy()
        
        tk.Button(
            dialog,
            text="Easy",
            font=("Arial", 12),
            width=15,
            command=lambda: select_difficulty('easy')
        ).pack(pady=5)
        
        tk.Button(
            dialog,
            text="Medium",
            font=("Arial", 12),
            width=15,
            command=lambda: select_difficulty('medium')
        ).pack(pady=5)
        
        tk.Button(
            dialog,
            text="Hard",
            font=("Arial", 12),
            width=15,
            command=lambda: select_difficulty('hard')
        ).pack(pady=5)
        
        self.root.wait_window(dialog)
        return result['difficulty']
    
    def show_game_board(self):
        """Display the game board."""
        # Clear the window
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Calculate window size
        board_size = self.game.board.size
        canvas_size = self.cell_size * (board_size - 1) + 2 * self.board_margin
        window_width = canvas_size + 20
        window_height = canvas_size + 150
        
        self.root.geometry(f"{window_width}x{window_height}")
        
        # Create top frame for info and controls
        top_frame = tk.Frame(self.root)
        top_frame.pack(pady=10)
        
        # Current player label
        self.player_label = tk.Label(
            top_frame,
            text=f"Current Player: {self.game.current_player.upper()}",
            font=("Arial", 14, "bold")
        )
        self.player_label.pack()
        
        # Captured stones label
        self.captured_label = tk.Label(
            top_frame,
            text=self.get_captured_text(),
            font=("Arial", 10)
        )
        self.captured_label.pack()
        
        # Canvas for the board
        self.canvas = tk.Canvas(
            self.root,
            width=canvas_size,
            height=canvas_size,
            bg='#DEB887'
        )
        self.canvas.pack(pady=10)
        
        # Bind click event
        self.canvas.bind('<Button-1>', self.on_board_click)
        
        # Draw the board
        self.draw_board()
        
        # Bottom frame for buttons
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)
        
        pass_btn = tk.Button(
            button_frame,
            text="Pass",
            font=("Arial", 12),
            width=10,
            command=self.pass_turn
        )
        pass_btn.pack(side=tk.LEFT, padx=5)
        
        menu_btn = tk.Button(
            button_frame,
            text="Main Menu",
            font=("Arial", 12),
            width=10,
            command=self.confirm_return_to_menu
        )
        menu_btn.pack(side=tk.LEFT, padx=5)
        
        # If it's AI's turn, make AI move
        if self.game.mode == 'singleplayer' and self.game.current_player == 'white':
            self.root.after(500, self.make_ai_move)
    
    def get_captured_text(self):
        """Get the captured stones text."""
        return (f"Captured - Black: {self.game.board.captured['white']}, "
                f"White: {self.game.board.captured['black']}")
    
    def draw_board(self):
        """Draw the game board."""
        self.canvas.delete('all')
        
        board_size = self.game.board.size
        
        # Draw grid lines
        for i in range(board_size):
            x = self.board_margin + i * self.cell_size
            y = self.board_margin + i * self.cell_size
            
            # Vertical line
            self.canvas.create_line(
                x, self.board_margin,
                x, self.board_margin + (board_size - 1) * self.cell_size,
                width=1
            )
            
            # Horizontal line
            self.canvas.create_line(
                self.board_margin, y,
                self.board_margin + (board_size - 1) * self.cell_size, y,
                width=1
            )
        
        # Draw star points (for 9x9, 13x13, and 19x19 boards)
        star_points = self.get_star_points(board_size)
        for row, col in star_points:
            x = self.board_margin + col * self.cell_size
            y = self.board_margin + row * self.cell_size
            self.canvas.create_oval(
                x - 3, y - 3, x + 3, y + 3,
                fill='black'
            )
        
        # Draw stones
        for row in range(board_size):
            for col in range(board_size):
                stone = self.game.board.get_stone(row, col)
                if stone:
                    self.draw_stone(row, col, stone)
        
        # Highlight last move
        last_move = self.game.board.get_last_move()
        if last_move and last_move[0] != 'pass':
            row, col = last_move[0], last_move[1]
            x = self.board_margin + col * self.cell_size
            y = self.board_margin + row * self.cell_size
            self.canvas.create_rectangle(
                x - self.stone_radius - 2, y - self.stone_radius - 2,
                x + self.stone_radius + 2, y + self.stone_radius + 2,
                outline='red', width=2
            )
    
    def get_star_points(self, board_size):
        """Get star point coordinates for the board."""
        if board_size == 9:
            return [(2, 2), (2, 6), (4, 4), (6, 2), (6, 6)]
        elif board_size == 13:
            return [(3, 3), (3, 9), (6, 6), (9, 3), (9, 9)]
        elif board_size == 19:
            return [(3, 3), (3, 9), (3, 15), (9, 3), (9, 9), 
                    (9, 15), (15, 3), (15, 9), (15, 15)]
        return []
    
    def draw_stone(self, row, col, color):
        """Draw a stone on the board."""
        x = self.board_margin + col * self.cell_size
        y = self.board_margin + row * self.cell_size
        
        fill_color = 'black' if color == 'black' else 'white'
        outline_color = 'black'
        
        self.canvas.create_oval(
            x - self.stone_radius, y - self.stone_radius,
            x + self.stone_radius, y + self.stone_radius,
            fill=fill_color,
            outline=outline_color,
            width=2
        )
    
    def on_board_click(self, event):
        """Handle board click event."""
        if self.game.is_game_over():
            return
        
        # Check if it's AI's turn
        if self.game.mode == 'singleplayer' and self.game.current_player == 'white':
            return
        
        # Convert click coordinates to board position
        x = event.x - self.board_margin
        y = event.y - self.board_margin
        
        col = round(x / self.cell_size)
        row = round(y / self.cell_size)
        
        # Check if click is close enough to an intersection
        intersection_x = self.board_margin + col * self.cell_size
        intersection_y = self.board_margin + row * self.cell_size
        
        distance = ((event.x - intersection_x) ** 2 + (event.y - intersection_y) ** 2) ** 0.5
        
        if distance > self.cell_size / 2:
            return
        
        # Try to place stone
        if self.game.board.is_valid_position(row, col):
            if self.game.make_move(row, col):
                self.update_display()
                
                # Check if game is over
                if self.game.is_game_over():
                    self.show_game_over()
                    return
                
                # If singleplayer, make AI move
                if self.game.mode == 'singleplayer' and self.game.current_player == 'white':
                    self.root.after(500, self.make_ai_move)
            else:
                messagebox.showwarning("Invalid Move", "Cannot place stone there!")
    
    def pass_turn(self):
        """Handle pass button click."""
        if self.game.is_game_over():
            return
        
        # Check if it's AI's turn
        if self.game.mode == 'singleplayer' and self.game.current_player == 'white':
            return
        
        self.game.pass_turn()
        self.update_display()
        
        # Check if game is over
        if self.game.is_game_over():
            self.show_game_over()
            return
        
        # If singleplayer, make AI move
        if self.game.mode == 'singleplayer' and self.game.current_player == 'white':
            self.root.after(500, self.make_ai_move)
    
    def make_ai_move(self):
        """Make the AI's move."""
        if self.game.is_game_over():
            return
        
        ai_move = self.game.get_ai_move()
        
        if ai_move == 'pass':
            self.game.pass_turn()
        else:
            row, col = ai_move
            self.game.make_move(row, col)
        
        self.update_display()
        
        # Check if game is over
        if self.game.is_game_over():
            self.show_game_over()
    
    def update_display(self):
        """Update the game display."""
        self.player_label.config(text=f"Current Player: {self.game.current_player.upper()}")
        self.captured_label.config(text=self.get_captured_text())
        self.draw_board()
    
    def show_game_over(self):
        """Show game over dialog."""
        result = self.game.get_winner()
        
        message = f"GAME OVER\n\n"
        message += f"Black score: {result['black_score']:.1f}\n"
        message += f"White score: {result['white_score']:.1f}\n\n"
        message += f"Winner: {result['winner'].upper()}\n"
        message += f"By {result['margin']:.1f} points"
        
        response = messagebox.askyesno(
            "Game Over",
            message + "\n\nPlay again?",
            icon='info'
        )
        
        if response:
            self.show_main_menu()
        else:
            self.root.quit()
    
    def confirm_return_to_menu(self):
        """Confirm returning to main menu."""
        if messagebox.askyesno("Return to Menu", "Are you sure you want to return to the main menu?"):
            self.show_main_menu()


def run_gui():
    """Run the GUI application."""
    root = tk.Tk()
    app = BadukGUI(root)
    root.mainloop()


if __name__ == "__main__":
    run_gui()
