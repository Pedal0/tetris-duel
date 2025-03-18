# tetris_duel/src/game.py

import random
import copy

# Handle different import scenarios
try:
    # For direct running from game.py
    from scoreboard import Scoreboard
except ImportError:
    try:
        # For running from project root
        from src.scoreboard import Scoreboard
    except ImportError:
        # Fallback if scoreboard isn't available
        Scoreboard = None

# Définition des pièces de Tetris et leurs rotations
TETROMINOS = {
    'I': [
        [[0, 0, 0, 0],
         [1, 1, 1, 1],
         [0, 0, 0, 0],
         [0, 0, 0, 0]],
        [[0, 0, 1, 0],
         [0, 0, 1, 0],
         [0, 0, 1, 0],
         [0, 0, 1, 0]],
        [[0, 0, 0, 0],
         [0, 0, 0, 0],
         [1, 1, 1, 1],
         [0, 0, 0, 0]],
        [[0, 1, 0, 0],
         [0, 1, 0, 0],
         [0, 1, 0, 0],
         [0, 1, 0, 0]]
    ],
    'O': [
        [[0, 0, 0, 0],
         [0, 1, 1, 0],
         [0, 1, 1, 0],
         [0, 0, 0, 0]]
    ],
    'T': [
        [[0, 0, 0, 0],
         [1, 1, 1, 0],
         [0, 1, 0, 0],
         [0, 0, 0, 0]],
        [[0, 1, 0, 0],
         [1, 1, 0, 0],
         [0, 1, 0, 0],
         [0, 0, 0, 0]],
        [[0, 1, 0, 0],
         [1, 1, 1, 0],
         [0, 0, 0, 0],
         [0, 0, 0, 0]],
        [[0, 1, 0, 0],
         [0, 1, 1, 0],
         [0, 1, 0, 0],
         [0, 0, 0, 0]]
    ],
    'S': [
        [[0, 0, 0, 0],
         [0, 1, 1, 0],
         [1, 1, 0, 0],
         [0, 0, 0, 0]],
        [[0, 1, 0, 0],
         [0, 1, 1, 0],
         [0, 0, 1, 0],
         [0, 0, 0, 0]],
        [[0, 0, 0, 0],
         [0, 1, 1, 0],
         [1, 1, 0, 0],
         [0, 0, 0, 0]],
        [[1, 0, 0, 0],
         [1, 1, 0, 0],
         [0, 1, 0, 0],
         [0, 0, 0, 0]]
    ],
    'Z': [
        [[0, 0, 0, 0],
         [1, 1, 0, 0],
         [0, 1, 1, 0],
         [0, 0, 0, 0]],
        [[0, 0, 1, 0],
         [0, 1, 1, 0],
         [0, 1, 0, 0],
         [0, 0, 0, 0]],
        [[0, 0, 0, 0],
         [1, 1, 0, 0],
         [0, 1, 1, 0],
         [0, 0, 0, 0]],
        [[0, 1, 0, 0],
         [1, 1, 0, 0],
         [1, 0, 0, 0],
         [0, 0, 0, 0]]
    ],
    'J': [
        [[0, 0, 0, 0],
         [1, 1, 1, 0],
         [0, 0, 1, 0],
         [0, 0, 0, 0]],
        [[0, 1, 0, 0],
         [0, 1, 0, 0],
         [1, 1, 0, 0],
         [0, 0, 0, 0]],
        [[1, 0, 0, 0],
         [1, 1, 1, 0],
         [0, 0, 0, 0],
         [0, 0, 0, 0]],
        [[0, 1, 1, 0],
         [0, 1, 0, 0],
         [0, 1, 0, 0],
         [0, 0, 0, 0]]
    ],
    'L': [
        [[0, 0, 0, 0],
         [1, 1, 1, 0],
         [1, 0, 0, 0],
         [0, 0, 0, 0]],
        [[1, 1, 0, 0],
         [0, 1, 0, 0],
         [0, 1, 0, 0],
         [0, 0, 0, 0]],
        [[0, 0, 1, 0],
         [1, 1, 1, 0],
         [0, 0, 0, 0],
         [0, 0, 0, 0]],
        [[0, 1, 0, 0],
         [0, 1, 0, 0],
         [0, 1, 1, 0],
         [0, 0, 0, 0]]
    ]
}

# Couleurs des pièces
PIECE_COLORS = {
    'I': (0, 255, 255),  # Cyan
    'O': (255, 255, 0),  # Jaune
    'T': (128, 0, 128),  # Violet
    'S': (0, 255, 0),    # Vert
    'Z': (255, 0, 0),    # Rouge
    'J': (0, 0, 255),    # Bleu
    'L': (255, 165, 0)   # Orange
}

# Définition de la pièce spéciale rigolote (en forme de cœur)
FUNNY_PIECE = {
    'heart': [
        [[0, 1, 0, 1, 0],
         [1, 1, 1, 1, 1],
         [1, 1, 1, 1, 1],
         [0, 1, 1, 1, 0],
         [0, 0, 1, 0, 0]]
    ],
    'star': [
        [[0, 0, 1, 0, 0],
         [0, 1, 1, 1, 0],
         [1, 1, 1, 1, 1],
         [0, 1, 1, 1, 0],
         [0, 1, 0, 1, 0]]
    ]
}

FUNNY_PIECE_COLOR = (255, 105, 180)  # Rose vif

class TetrisGame:
    def __init__(self):
        """Initialize the Tetris game with default settings."""
        self.grid_width, self.grid_height = 10, 20  # Dimensions standards de la grille Tetris
        self.grids = {
            'human': [[0 for _ in range(self.grid_width)] for _ in range(self.grid_height)],
            'ai': [[0 for _ in range(self.grid_width)] for _ in range(self.grid_height)]
        }
        self.current_pieces = {'human': None, 'ai': None}
        self.next_pieces = {'human': None, 'ai': None}
        self.piece_positions = {'human': [0, 3], 'ai': [0, 3]}  # [row, col] for each player
        self.piece_rotations = {'human': 0, 'ai': 0}
        self.lines_completed = {'human': 0, 'ai': 0}
        self.scores = {'human': 0, 'ai': 0}
        self.game_over = False
        self.special_events_timer = 0
        
        # Special rules tracking
        self.funny_piece_thresholds = {'human': 3000, 'ai': 3000}
        self.surprise_gift_pending = {'human': False, 'ai': False}
        self.last_cleared_lines = {'human': 0, 'ai': 0}
        
    def initialize_game(self):
        """Set up the game state for a new game."""
        # Réinitialiser les grilles
        self.grids = {
            'human': [[0 for _ in range(self.grid_width)] for _ in range(self.grid_height)],
            'ai': [[0 for _ in range(self.grid_width)] for _ in range(self.grid_height)]
        }
        
        # Générer les pièces initiales et suivantes
        self.next_pieces = {'human': self.generate_piece('human'), 'ai': self.generate_piece('ai')}
        self.spawn_new_pieces()
        
        self.lines_completed = {'human': 0, 'ai': 0}
        self.scores = {'human': 0, 'ai': 0}
        self.game_over = False
        self.special_events_timer = 0
        
        # Reset special rules tracking
        self.funny_piece_thresholds = {'human': 3000, 'ai': 3000}
        self.surprise_gift_pending = {'human': False, 'ai': False}
        self.last_cleared_lines = {'human': 0, 'ai': 0}

    def generate_piece(self, player):
        """Générer une nouvelle pièce avec son type."""
        # Check if we should generate a funny piece (every 3000 points)
        if self.scores[player] >= self.funny_piece_thresholds[player]:
            self.funny_piece_thresholds[player] += 3000  # Set next threshold
            print(f"Funny piece for {player}!")
            # Choisir une pièce rigolote (cœur ou étoile)
            funny_shape = random.choice(list(FUNNY_PIECE.keys()))
            return {
                'type': 'funny',
                'shape': FUNNY_PIECE[funny_shape][0],
                'color': FUNNY_PIECE_COLOR,
                'funny_shape': funny_shape
            }
        
        # Check if we should generate an easy piece as a gift (when opponent completed 2 lines)
        if self.surprise_gift_pending[player]:
            self.surprise_gift_pending[player] = False
            # Give an easy piece (I or O)
            easy_piece = random.choice(['I', 'O'])
            print(f"Surprise gift for {player}: {easy_piece}!")
            return {
                'type': easy_piece,
                'shape': TETROMINOS[easy_piece][0],
                'color': PIECE_COLORS[easy_piece]
            }
        
        # Generate a regular piece
        piece_type = random.choice(list(TETROMINOS.keys()))
        return {
            'type': piece_type,
            'shape': TETROMINOS[piece_type][0],
            'color': PIECE_COLORS[piece_type]
        }

    def spawn_piece(self):
        """Méthode maintenue pour la compatibilité, 
        mais utilise désormais generate_piece."""
        return self.generate_piece('human')['type']
        
    def spawn_new_pieces(self):
        """Place de nouvelles pièces pour les deux joueurs."""
        for player in ['human', 'ai']:
            self.current_pieces[player] = self.next_pieces[player]
            self.next_pieces[player] = self.generate_piece(player)
            self.piece_positions[player] = [0, self.grid_width // 2 - 2]
            self.piece_rotations[player] = 0
            
            # Vérifier si le jeu est terminé
            if self.check_collision(player):
                self.game_over = True
                print(f"Game over! {player.capitalize()} player lost.")

    def update_game_state(self):
        """Update the game state, including piece positions and scoring."""
        if self.game_over:
            return

        # Update human player state
        self.update_player_state('human')
        # Update AI player state
        self.update_player_state('ai')

        # Check for special events
        self.check_special_events()

    def update_player_state(self, player):
        """Update the state of the specified player."""
        # Déplacer automatiquement la pièce vers le bas
        old_position = self.piece_positions[player][:]
        self.piece_positions[player][0] += 1
        
        # Vérifier collision
        if self.check_collision(player):
            # Restaurer l'ancienne position
            self.piece_positions[player] = old_position
            # Fixer la pièce dans la grille
            self.lock_piece(player)
            # Vérifier les lignes complètes
            completed_lines = self.check_for_completed_lines(player)
            self.last_cleared_lines[player] = completed_lines
            
            if completed_lines:
                self.lines_completed[player] += completed_lines
                
                # Règle du cadeau surprise: Si un joueur complète 2 lignes, 
                # l'adversaire reçoit une pièce facile
                if completed_lines == 2:
                    opponent = 'ai' if player == 'human' else 'human'
                    self.surprise_gift_pending[opponent] = True
                    print(f"Surprise gift pending for {opponent}")
                
                # Calculer le score selon les règles demandées
                base_points = 50 * completed_lines
                
                # Apply bonuses
                if completed_lines == 2:
                    bonus = 100
                elif completed_lines == 3:
                    bonus = 200
                elif completed_lines == 4:
                    bonus = 300
                else:
                    bonus = 0
                
                total_points = base_points + bonus
                self.scores[player] += total_points
                
                # Bonus pour les pièces rigolotes bien placées
                if self.current_pieces[player].get('type') == 'funny':
                    self.scores[player] += 100
                    print(f"Bonus de 100 points pour pièce rigolote bien placée!")
            
            # Engendrer une nouvelle pièce
            self.current_pieces[player] = self.next_pieces[player]
            self.next_pieces[player] = self.generate_piece(player)
            self.piece_positions[player] = [0, self.grid_width // 2 - 2]
            self.piece_rotations[player] = 0
            
            # Vérifier si le jeu est terminé
            if self.check_collision(player):
                self.game_over = True
                print(f"Game over! {player.capitalize()} player lost.")

    def lock_piece(self, player):
        """Fixer la pièce courante dans la grille."""
        piece = self.current_pieces[player]
        
        # Handle special case for funny piece
        if piece.get('type') == 'funny':
            shape = piece['shape']
        else:
            # Regular tetromino
            shape = TETROMINOS[piece['type']][self.piece_rotations[player]]
            
        row_offset, col_offset = self.piece_positions[player]
        
        for i in range(len(shape)):
            for j in range(len(shape[i])):
                if shape[i][j]:
                    new_row, new_col = row_offset + i, col_offset + j
                    if 0 <= new_row < self.grid_height and 0 <= new_col < self.grid_width:
                        self.grids[player][new_row][new_col] = piece['type']

    def check_for_completed_lines(self, player):
        """Vérifier et supprimer les lignes complétées."""
        completed_lines = 0
        # Check from bottom to top
        row = self.grid_height - 1
        while row >= 0:
            if all(cell for cell in self.grids[player][row]):
                completed_lines += 1
                # Supprimer la ligne complétée
                for r in range(row, 0, -1):
                    self.grids[player][r] = self.grids[player][r-1][:]
                self.grids[player][0] = [0 for _ in range(self.grid_width)]
                # Ne pas incrémenter row car la nouvelle ligne déplacée doit être vérifiée
            else:
                row -= 1
        
        return completed_lines

    def handle_user_input(self, input_command):
        """Handle user input for controlling the human player."""
        if self.game_over:
            return
            
        # Mapper les commandes clavier aux actions
        commands = {
            'left': lambda: self.move_piece('human', 0, -1),
            'right': lambda: self.move_piece('human', 0, 1),
            'down': lambda: self.move_piece('human', 1, 0),
            'up': lambda: self.rotate_piece('human'),
            'space': lambda: self.hard_drop('human')
        }
        
        if input_command in commands:
            commands[input_command]()

    def move_piece(self, player, delta_row, delta_col):
        """Move the current piece of the specified player."""
        old_position = self.piece_positions[player][:]
        
        # Mettre à jour la position
        self.piece_positions[player][0] += delta_row
        self.piece_positions[player][1] += delta_col
        
        # Vérifier collision
        if self.check_collision(player):
            # Restaurer l'ancienne position
            self.piece_positions[player] = old_position
            
            # Si le mouvement vers le bas est bloqué, fixer la pièce
            if delta_row > 0:
                self.lock_piece(player)
                
                # Vérifier les lignes complètes
                completed_lines = self.check_for_completed_lines(player)
                self.last_cleared_lines[player] = completed_lines
                
                if completed_lines:
                    self.lines_completed[player] += completed_lines
                    
                    # Règle du cadeau surprise
                    if completed_lines == 2:
                        opponent = 'ai' if player == 'human' else 'human'
                        self.surprise_gift_pending[opponent] = True
                        print(f"Surprise gift pending for {opponent}")
                    
                    # Calculer le score selon les règles demandées
                    base_points = 50 * completed_lines
                    
                    # Apply bonuses
                    if completed_lines == 2:
                        bonus = 100
                    elif completed_lines == 3:
                        bonus = 200
                    elif completed_lines == 4:
                        bonus = 300
                    else:
                        bonus = 0
                    
                    total_points = base_points + bonus
                    self.scores[player] += total_points
                    print(f"{player} got {total_points} points ({base_points} base + {bonus} bonus)")
                    
                    # Bonus pour les pièces rigolotes bien placées
                    if self.current_pieces[player].get('type') == 'funny':
                        self.scores[player] += 100
                        print(f"Bonus de 100 points pour pièce rigolote bien placée!")
                
                # Engendrer une nouvelle pièce
                self.current_pieces[player] = self.next_pieces[player]
                self.next_pieces[player] = self.generate_piece(player)
                self.piece_positions[player] = [0, self.grid_width // 2 - 2]
                self.piece_rotations[player] = 0
                
                # Vérifier si le jeu est terminé
                if self.check_collision(player):
                    self.game_over = True
                    print(f"Game over! {player.capitalize()} player lost.")
                    
            return False
        return True

    def rotate_piece(self, player):
        """Faire pivoter la pièce du joueur spécifié."""
        piece = self.current_pieces[player]
        
        # Funny pieces can't rotate
        if piece.get('type') == 'funny':
            return
            
        old_rotation = self.piece_rotations[player]
        piece_type = piece['type']
        
        # Calculer la nouvelle rotation
        self.piece_rotations[player] = (self.piece_rotations[player] + 1) % len(TETROMINOS[piece_type])
        
        # Vérifier collision
        if self.check_collision(player):
            # Restaurer l'ancienne rotation
            self.piece_rotations[player] = old_rotation

    def hard_drop(self, player):
        """Faire tomber la pièce jusqu'à ce qu'elle entre en collision."""
        while self.move_piece(player, 1, 0):
            pass  # Continuer à déplacer la pièce vers le bas jusqu'à ce qu'elle ne puisse plus

    def check_collision(self, player):
        """Vérifier si la pièce actuelle est en collision avec les murs ou d'autres pièces."""
        piece = self.current_pieces[player]
        
        # Handle special case for funny piece
        if piece.get('type') == 'funny':
            shape = piece['shape']
        else:
            # Regular tetromino
            shape = TETROMINOS[piece['type']][self.piece_rotations[player]]
            
        row_offset, col_offset = self.piece_positions[player]
        
        for i in range(len(shape)):
            for j in range(len(shape[i])):
                if shape[i][j]:
                    new_row, new_col = row_offset + i, col_offset + j
                    
                    # Vérifier les limites de la grille
                    if new_row < 0 or new_row >= self.grid_height or new_col < 0 or new_col >= self.grid_width:
                        return True
                    
                    # Vérifier la collision avec d'autres pièces
                    if self.grids[player][new_row][new_col]:
                        return True
        
        return False

    def get_current_piece_cells(self, player):
        """Obtenir les cellules occupées par la pièce actuelle du joueur."""
        piece = self.current_pieces[player]
        
        # Handle special case for funny piece
        if piece.get('type') == 'funny':
            shape = piece['shape']
        else:
            # Regular tetromino
            shape = TETROMINOS[piece['type']][self.piece_rotations[player]]
            
        row_offset, col_offset = self.piece_positions[player]
        cells = []
        
        for i in range(len(shape)):
            for j in range(len(shape[i])):
                if shape[i][j]:
                    new_row, new_col = row_offset + i, col_offset + j
                    if 0 <= new_row < self.grid_height and 0 <= new_col < self.grid_width:
                        cells.append((new_row, new_col))
        
        return cells

    def check_special_events(self):
        """Check and trigger special events based on game state."""
        self.special_events_timer += 1
        if self.special_events_timer >= 120:  # Example: every 2 minutes
            self.trigger_rainbow_effect()
            self.special_events_timer = 0

    def trigger_rainbow_effect(self):
        """Trigger a rainbow effect in the game."""
        # Cette méthode est maintenant gérée par la classe TetrisDuel
        print("Rainbow effect triggered!")
        
    def get_grid_with_current_piece(self, player):
        """Obtenir une copie de la grille incluant la pièce actuelle."""
        grid_copy = copy.deepcopy(self.grids[player])
        
        if not self.current_pieces[player]:
            return grid_copy
        
        piece = self.current_pieces[player]
        
        # Handle special case for funny piece
        if piece.get('type') == 'funny':
            shape = piece['shape']
        else:
            # Regular tetromino
            shape = TETROMINOS[piece['type']][self.piece_rotations[player]]
            
        row_offset, col_offset = self.piece_positions[player]
        
        for i in range(len(shape)):
            for j in range(len(shape[i])):
                if shape[i][j]:
                    new_row, new_col = row_offset + i, col_offset + j
                    if 0 <= new_row < self.grid_height and 0 <= new_col < self.grid_width:
                        grid_copy[new_row][new_col] = piece['type']
        
        return grid_copy

# Example usage
if __name__ == "__main__":
    game = TetrisGame()
    game.initialize_game()
    while not game.game_over:
        game.update_game_state()
        # Simulate user input
        game.handle_user_input(random.choice(['left', 'right', 'up', 'down', 'space']))