# tetris_duel/src/ai.py

import random
import copy

class AI:
    """
    AI class for automatic piece placement in Tetris Duel.
    """

    def __init__(self, game):
        """
        Initializes the AI with a reference to the game instance.

        :param game: An instance of the TetrisGame class.
        """
        self.game = game
        # Weights for different evaluation metrics
        self.weights = {
            'height': -0.510066,
            'lines': 0.760666,
            'holes': -0.35663,
            'bumpiness': -0.184483,
            'random': 0.1  # Ajouter un facteur aléatoire pour plus de variété
        }
        # Garder une trace des derniers mouvements pour éviter les répétitions
        self.last_moves = []
        self.max_history = 5

    def calculate_best_move(self):
        """
        Calculates the best move for the AI player based on the current game state.

        :return: A tuple containing the best move (rotation, direction).
        """
        if not self.game.current_pieces.get('ai'):
            return None
            
        best_moves = []
        best_score = float('-inf')
        
        piece_type = self.game.current_pieces['ai'].get('type')
        
        # Skip if it's a funny piece that can't rotate
        if piece_type == 'funny':
            # For funny pieces, try different horizontal positions
            for col_offset in range(-5, 6):
                # Simulate moving the piece
                score = self.evaluate_move(0, col_offset)
                # Ajouter un bruit aléatoire pour éviter de toujours choisir la même action
                score += random.uniform(-0.1, 0.1)
                
                if score > best_score:
                    best_score = score
                    best_moves = [(0, col_offset)]  # Reset list with this move
                elif abs(score - best_score) < 0.1:  # If scores are very close
                    best_moves.append((0, col_offset))  # Add as an alternative
        else:
            # Pour les pièces normales
            max_rotations = 1 if piece_type == 'O' else 4  # O piece doesn't need rotation
            
            for rotation in range(max_rotations):
                for col_offset in range(-5, 6):  # Try different horizontal positions
                    # Simulate moving the piece
                    score = self.evaluate_move(rotation, col_offset)
                    # Ajouter un bruit aléatoire pour éviter de toujours choisir la même action
                    score += random.uniform(-0.1, 0.1)
                    
                    # Pénaliser légèrement les mouvements récemment effectués
                    if (rotation, col_offset) in self.last_moves:
                        score -= 0.05 * (self.max_history - self.last_moves.index((rotation, col_offset)))
                    
                    if score > best_score:
                        best_score = score
                        best_moves = [(rotation, col_offset)]  # Reset list with this move
                    elif abs(score - best_score) < 0.1:  # If scores are very close
                        best_moves.append((rotation, col_offset))  # Add as an alternative
        
        # Si plusieurs mouvements ont des scores similaires, en choisir un au hasard
        best_move = random.choice(best_moves) if best_moves else None
        
        # Remember this move
        if best_move:
            self.last_moves.append(best_move)
            if len(self.last_moves) > self.max_history:
                self.last_moves.pop(0)
                
        return best_move

    def evaluate_move(self, rotation, col_offset):
        """
        Evaluates a potential move by simulating it and scoring the resulting board.
        
        :param rotation: The rotation to apply to the piece
        :param col_offset: The horizontal offset to apply
        :return: A score for this move
        """
        # Make a copy of the game state
        game_copy = self.get_game_copy()
        
        # Apply rotation
        original_rotation = game_copy.piece_rotations['ai']
        game_copy.piece_rotations['ai'] = rotation
        
        # Apply horizontal movement
        original_position = game_copy.piece_positions['ai'][:]
        game_copy.piece_positions['ai'][1] += col_offset
        
        # Check if this position is valid
        if game_copy.check_collision('ai'):
            return float('-inf')  # Invalid move
            
        # Simulate dropping the piece
        self.simulate_drop(game_copy, 'ai')
        
        # Evaluate the board state
        return self.evaluate_board(game_copy)

    def get_game_copy(self):
        """
        Creates a copy of the game state for simulation.
        
        :return: A copy of the game object
        """
        game_copy = copy.deepcopy(self.game)
        return game_copy

    def simulate_drop(self, game, player):
        """
        Simulates dropping a piece to its final position.
        
        :param game: The game object
        :param player: The player ('human' or 'ai')
        """
        while True:
            old_position = game.piece_positions[player][:]
            game.piece_positions[player][0] += 1
            
            if game.check_collision(player):
                game.piece_positions[player] = old_position
                game.lock_piece(player)
                break

    def evaluate_board(self, game, player='ai'):
        """
        Evaluates the board state and returns a score.
        Uses multiple heuristics to determine how good the position is.

        :param game: The game state to evaluate
        :param player: The player whose board to evaluate
        :return: A score representing how favorable the board state is
        """
        # Get the grid
        grid = game.grids[player]
        
        # Calculate various metrics
        height_sum = 0
        holes = 0
        completed_lines = 0
        bumpiness = 0
        
        # Calculate column heights and holes
        heights = [0] * game.grid_width
        for col in range(game.grid_width):
            found_block = False
            for row in range(game.grid_height):
                if grid[row][col]:
                    found_block = True
                    if heights[col] == 0:  # First block in column
                        heights[col] = game.grid_height - row
                elif found_block:
                    # This is a hole
                    holes += 1
        
        # Calculate sum of heights
        height_sum = sum(heights)
        
        # Calculate bumpiness (sum of height differences between adjacent columns)
        for i in range(game.grid_width - 1):
            bumpiness += abs(heights[i] - heights[i+1])
        
        # Check for completed lines
        completed_lines = 0
        for row in range(game.grid_height):
            if all(cell for cell in grid[row]):
                completed_lines += 1
        
        # Facteur aléatoire pour diversité
        random_factor = random.random() * self.weights['random']
        
        # Calculate score based on weights
        score = (
            self.weights['height'] * height_sum +
            self.weights['lines'] * completed_lines +
            self.weights['holes'] * holes +
            self.weights['bumpiness'] * bumpiness +
            random_factor
        )
        
        return score

    def get_possible_moves(self, piece):
        """
        Generates a list of possible moves for the given piece.
        Note: This method is kept for compatibility with tests.

        :param piece: The current Tetris piece.
        :return: A list of possible moves (rotation, direction).
        """
        moves = []
        # Add all possible rotations and directions
        if piece.get('type') == 'funny':
            # Funny pieces can't rotate, just different horizontal positions
            for direction in range(-5, 6):
                moves.append((0, direction))
        else:
            max_rotations = 1 if piece.get('type') == 'O' else 4
            for rotation in range(max_rotations):
                for direction in range(-5, 6):
                    moves.append((rotation, direction))
                    
        return moves