import unittest
import sys
import os

# Add the parent directory to the path to import the src modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.game import TetrisGame

class TestGameLogic(unittest.TestCase):
    def setUp(self):
        """Set up the initial game state before each test."""
        self.game = TetrisGame()
        self.game.initialize_game()

    def test_initialize_game(self):
        """Test the initialization of the game state."""
        self.assertIsNotNone(self.game, "Game state should not be None after initialization.")
        self.assertIn('human', self.game.current_pieces, "Game should have human player pieces.")
        self.assertIn('ai', self.game.current_pieces, "Game should have AI player pieces.")
        self.assertEqual(self.game.lines_completed, {'human': 0, 'ai': 0}, "Initial lines completed should be 0.")
        self.assertEqual(self.game.scores, {'human': 0, 'ai': 0}, "Initial scores should be zero for both players.")

    def test_update_game_state(self):
        """Test updating the game state."""
        initial_score = self.game.scores['human']
        # Force a line completion for testing
        self.game.lines_completed['human'] = 1
        self.game.update_game_state()
        self.assertGreaterEqual(self.game.scores['human'], initial_score, "Human score should not decrease after update.")

if __name__ == '__main__':
    unittest.main()