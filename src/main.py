# tetris_duel/src/main.py

import tkinter as tk
import time
import random

# Import correct paths
try:
    # For direct running from main.py
    from game import TetrisGame, PIECE_COLORS
    from ai import AI
    from scoreboard import Scoreboard
    from timer import GameTimer
    from performance import PerformanceManager
except ImportError:
    # For running from project root
    from src.game import TetrisGame, PIECE_COLORS
    from src.ai import AI
    from src.scoreboard import Scoreboard
    from src.timer import GameTimer
    from src.performance import PerformanceManager

class TetrisDuel:
    def __init__(self, root: tk.Tk):
        """Initialize the Tetris Duel game."""
        self.root = root
        self.root.title("Tetris Duel")
        self.root.geometry("800x700")  # Adjusted for better visibility
        
        # Create main canvas
        self.canvas = tk.Canvas(root, width=800, height=600, bg='black')
        self.canvas.pack(pady=10)
        
        # Initialize game objects
        self.game = TetrisGame()
        self.game.initialize_game()
        self.scoreboard = Scoreboard(root)
        self.timer = GameTimer()
        self.ai = AI(self.game)
        
        # Performance optimization
        self.performance = PerformanceManager(root)
        self.performance.optimize_tkinter(self.canvas)
        
        # Game speed control
        self.game_speed = 500  # milliseconds between updates
        self.original_speed = 500
        self.gentle_pause_active = False
        self.gentle_pause_end_time = 0
        
        # AI thinking time
        self.ai_delay = 1500  # Ralentir l'IA à 1.5 secondes entre les mouvements
        
        # Task IDs for cancellation during reset
        self.ai_task_id = None
        self.game_task_id = None
        
        # Visual effects
        self.rainbow_mode = False
        self.rainbow_end_time = 0
        
        # Frame counting for smooth animation
        self.last_update_time = time.time()
        self.frame_count = 0
        self.frame_rate = 0
        
        # Color cache to improve performance
        self.color_cache = {}
        self._precalculate_colors()
        
        # Keyboard bindings
        self.setup_keyboard_bindings()
        
        # Start game timer
        self.timer.start_timer()
        self.update_ai()
        self.update_game()
    
    def _precalculate_colors(self):
        """Précalculer les couleurs pour éviter la conversion à chaque frame"""
        self.color_cache = {}
        for piece_type, rgb in PIECE_COLORS.items():
            r, g, b = rgb
            self.color_cache[piece_type] = f'#{r:02x}{g:02x}{b:02x}'
    
    def setup_keyboard_bindings(self):
        """Set up keyboard bindings for the game."""
        self.root.bind("<Left>", lambda event: self.game.handle_user_input('left'))
        self.root.bind("<Right>", lambda event: self.game.handle_user_input('right'))
        self.root.bind("<Down>", lambda event: self.game.handle_user_input('down'))
        self.root.bind("<Up>", lambda event: self.game.handle_user_input('up'))
        self.root.bind("<space>", lambda event: self.game.handle_user_input('space'))
        # Corriger les bindings pour le redémarrage
        self.root.bind("<r>", lambda event: self.reset_game())
        self.root.bind("<R>", lambda event: self.reset_game())  # Ajouter la majuscule
        
    def reset_game(self):
        """Reset the game to initial state."""
        print("Resetting game...")
        
        # Annuler les mises à jour programmées
        if hasattr(self, 'ai_task_id') and self.ai_task_id:
            self.root.after_cancel(self.ai_task_id)
        if hasattr(self, 'game_task_id') and self.game_task_id:
            self.root.after_cancel(self.game_task_id)
        
        # Réinitialiser complètement le jeu et ses composants
        self.game = TetrisGame()
        self.game.initialize_game()
        
        # Réinitialiser le score
        self.scoreboard.reset_scores()
        
        # Réinitialiser les variables de contrôle
        self.game_speed = self.original_speed
        self.gentle_pause_active = False
        self.rainbow_mode = False
        
        # Réinitialiser le timer
        self.timer = GameTimer()
        self.timer.start_timer()
        
        # Redémarrer l'IA
        self.ai = AI(self.game)
        
        # Redémarrer les tâches périodiques
        self.update_ai()
        self.update_game()
        
        # Mise à jour forcée de l'interface
        self.redraw()
    
    def update_ai(self):
        """Have the AI make a move."""
        if not self.game.game_over:
            # Get best move from AI
            move = self.ai.calculate_best_move()
            if move:
                rotation, direction = move
                
                # Apply rotation
                current_rotation = self.game.piece_rotations['ai']
                while current_rotation != rotation:
                    self.game.rotate_piece('ai')
                    current_rotation = (current_rotation + 1) % 4
                
                # Apply horizontal movement
                if direction < 0:
                    # Move left
                    for _ in range(abs(direction)):
                        self.game.move_piece('ai', 0, -1)
                elif direction > 0:
                    # Move right
                    for _ in range(direction):
                        self.game.move_piece('ai', 0, 1)
                
                # Drop the piece
                self.game.hard_drop('ai')
        
        # Schedule next AI move with longer delay
        self.ai_task_id = self.root.after(self.ai_delay, self.update_ai)
    
    def update_game(self):
        """Update the game state and redraw the canvas."""
        # Check for speed modifiers
        current_time = time.time()
        
        # Check if gentle pause should end
        if self.gentle_pause_active and current_time > self.gentle_pause_end_time:
            self.gentle_pause_active = False
            self.game_speed = self.original_speed
            print("Gentle pause ended")
            
        # Check if rainbow mode should end
        if self.rainbow_mode and current_time > self.rainbow_end_time:
            self.rainbow_mode = False
            print("Rainbow effect ended")
        
        # Check for special events based on scores
        self.check_special_events()
        
        # Update game state
        self.game.update_game_state()
        
        # Update scoreboard
        self.scoreboard.update_score(self.game.scores['human'], self.game.scores['ai'])
        
        # Redraw the game with performance monitoring
        self.performance.begin_frame()
        self.redraw()
        self.performance.end_frame()
        self.performance.limit_fps(60)  # Target 60 FPS for smoothness
        
        # Schedule next update if game is not over
        if not self.game.game_over:
            self.game_task_id = self.root.after(self.game_speed, self.update_game)
        else:
            self.game_over_display()
    
    def check_special_events(self):
        """Check for special events based on scores."""
        # Check for gentle pause (every 1000 points)
        human_score = self.game.scores['human']
        ai_score = self.game.scores['ai']
        
        if human_score // 1000 > (human_score - 50) // 1000 or ai_score // 1000 > (ai_score - 50) // 1000:
            self.activate_gentle_pause()
        
        # Rainbow effect is handled by the timer class
        if self.timer.check_rainbow_event():
            self.activate_rainbow()
    
    def activate_gentle_pause(self):
        """Activate the gentle pause - slow down the game for 10 seconds."""
        if not self.gentle_pause_active:
            self.gentle_pause_active = True
            self.game_speed = int(self.original_speed * 1.2)  # 20% slower
            self.gentle_pause_end_time = time.time() + 10  # 10 seconds
            print("Gentle pause activated!")
    
    def activate_rainbow(self):
        """Activate rainbow mode for 20 seconds."""
        self.rainbow_mode = True
        self.rainbow_end_time = time.time() + 20  # 20 seconds
        print("Rainbow effect activated!")
    
    def redraw(self):
        """Redraw the game grids and scores."""
        # Measure performance
        current_time = time.time()
        elapsed = current_time - self.last_update_time
        self.last_update_time = current_time
        
        self.frame_count += 1
        if self.frame_count % 10 == 0 and elapsed > 0:  # Update FPS every 10 frames
            self.frame_rate = 1.0 / elapsed
        
        # Clear canvas efficiently
        self.canvas.delete("all")
        
        # Draw game elements
        self.draw_grids()
        self.draw_next_pieces()
        self.draw_scores()
        
        # Display special effects indicators
        if self.gentle_pause_active:
            self.canvas.create_text(400, 30, text="GENTLE PAUSE ACTIVE!", fill="yellow", font=("Arial", 16))
        
        if self.rainbow_mode:
            self.canvas.create_text(400, 580, text="RAINBOW MODE!", fill="magenta", font=("Arial", 16))
        
        # Force update for smoother animation
        if not self.game.game_over:
            self.canvas.update_idletasks()
    
    def draw_grids(self):
        """Draw the game grids for both players."""
        # Draw borders
        self.canvas.create_rectangle(50, 50, 300, 550, outline='white', width=2)
        self.canvas.create_rectangle(500, 50, 750, 550, outline='white', width=2)
        
        # Draw grid labels
        self.canvas.create_text(175, 30, text="HUMAN PLAYER", fill="white", font=("Arial", 14))
        self.canvas.create_text(625, 30, text="AI PLAYER", fill="white", font=("Arial", 14))
        
        # Calculate cell size
        cell_width = (300 - 50) / self.game.grid_width
        cell_height = (550 - 50) / self.game.grid_height
        
        # Draw grid cells and pieces for human player
        self.draw_grid_cells('human', 50, 50, cell_width, cell_height)
        
        # Draw grid cells and pieces for AI player
        self.draw_grid_cells('ai', 500, 50, cell_width, cell_height)
    
    def draw_grid_cells(self, player, grid_x, grid_y, cell_width, cell_height):
        """Draw the grid cells for a player."""
        # Get the grid with the current piece
        grid = self.game.get_grid_with_current_piece(player)
        
        # Draw background grid first (optimization)
        for row in range(self.game.grid_height):
            for col in range(self.game.grid_width):
                x1 = grid_x + col * cell_width
                y1 = grid_y + row * cell_height
                x2 = x1 + cell_width
                y2 = y1 + cell_height
                self.canvas.create_rectangle(x1, y1, x2, y2, fill='black', outline='#222222', width=0.5)
        
        # Then only draw occupied cells
        for row in range(self.game.grid_height):
            for col in range(self.game.grid_width):
                cell_value = grid[row][col]
                if cell_value:
                    x1 = grid_x + col * cell_width
                    y1 = grid_y + row * cell_height
                    x2 = x1 + cell_width
                    y2 = y1 + cell_height
                    
                    # This is a piece cell, color it
                    if isinstance(cell_value, str):  # Regular piece
                        if self.rainbow_mode:
                            # Rainbow mode - use cached random colors for better performance
                            color_key = f'rainbow_{row}_{col}_{self.frame_count % 20}'
                            if color_key not in self.color_cache:
                                self.color_cache[color_key] = f'#{random.randint(128, 255):02x}{random.randint(128, 255):02x}{random.randint(128, 255):02x}'
                            color = self.color_cache[color_key]
                        else:
                            # Normal mode - use the cached piece color
                            color = self.color_cache.get(cell_value, '#C8C8C8')
                    else:  # Special piece like a funny piece
                        color = '#FF00FF'  # Pink for special pieces
                    
                    # Fill the cell with the appropriate color
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline='black', width=0.5)
    
    def draw_next_pieces(self):
        """Draw the next piece preview for both players."""
        # Human player next piece
        self.canvas.create_text(175, 570, text="NEXT PIECE:", fill="white", font=("Arial", 12))
        self.draw_piece_preview(self.game.next_pieces['human'], 175, 590)
        
        # AI player next piece
        self.canvas.create_text(625, 570, text="NEXT PIECE:", fill="white", font=("Arial", 12))
        self.draw_piece_preview(self.game.next_pieces['ai'], 625, 590)
    
    def draw_piece_preview(self, piece, center_x, center_y):
        """Draw a preview of a piece at the specified position."""
        if not piece:
            return
            
        shape = piece['shape']  # First rotation
        r, g, b = piece['color']
        color = f'#{r:02x}{g:02x}{b:02x}'
        
        cell_size = 15
        offset_x = -len(shape[0]) * cell_size / 2
        offset_y = -len(shape) * cell_size / 2
        
        for i in range(len(shape)):
            for j in range(len(shape[i])):
                if shape[i][j]:
                    x1 = center_x + offset_x + j * cell_size
                    y1 = center_y + offset_y + i * cell_size
                    x2 = x1 + cell_size
                    y2 = y1 + cell_size
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline='black')
    
    def draw_scores(self):
        """Display the current scores and lines for both players."""
        self.canvas.create_text(175, 620, text=f"Score: {self.game.scores['human']}", fill="white", font=("Arial", 16))
        self.canvas.create_text(175, 645, text=f"Lines: {self.game.lines_completed['human']}", fill="white", font=("Arial", 14))
        
        self.canvas.create_text(625, 620, text=f"Score: {self.game.scores['ai']}", fill="white", font=("Arial", 16))
        self.canvas.create_text(625, 645, text=f"Lines: {self.game.lines_completed['ai']}", fill="white", font=("Arial", 14))
    
    def game_over_display(self):
        """Display game over message and winner."""
        winner = "Human" if self.game.scores['human'] > self.game.scores['ai'] else "AI"
        if self.game.scores['human'] == self.game.scores['ai']:
            winner = "It's a tie!"
        else:
            winner = f"{winner} wins!"
        
        self.canvas.create_rectangle(200, 250, 600, 350, fill='black', outline='white', width=3)
        self.canvas.create_text(400, 285, text="GAME OVER", fill="red", font=("Arial", 24, "bold"))
        self.canvas.create_text(400, 315, text=winner, fill="yellow", font=("Arial", 18))
        
        # Add restart instruction
        self.canvas.create_text(400, 500, text="Press 'R' to restart", fill="white", font=("Arial", 14))

def run_game():
    """Run the Tetris Duel game."""
    root = tk.Tk()
    game = TetrisDuel(root)
    root.mainloop()

if __name__ == "__main__":
    run_game()