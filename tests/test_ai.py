import unittest
import sys
import os

# Add the parent directory to the path to import the src modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.ai import AI
from src.game import TetrisGame

class TestAI(unittest.TestCase):
    """Unit tests for AI logic in Tetris Duel."""

    def setUp(self):
        """Set up the necessary environment for the tests."""
        self.game = TetrisGame()
        self.game.initialize_game()
        self.ai = AI(self.game)

    def test_calculate_best_move(self):
        """Test the calculate_best_move function."""
        best_move = self.ai.calculate_best_move()
        self.assertIsNotNone(best_move, "AI should return a valid move.")
        self.assertTrue(isinstance(best_move, tuple), "Move should be a tuple of (rotation, direction).")
        self.assertEqual(len(best_move), 2, "Move tuple should have 2 elements.")

    def test_get_possible_moves(self):
        """Test the get_possible_moves function."""
        piece = self.game.current_pieces['ai']
        moves = self.ai.get_possible_moves(piece)
        self.assertGreater(len(moves), 0, "There should be at least one possible move.")

    def tearDown(self):
        """Clean up after tests if necessary."""
        pass

if __name__ == '__main__':
    unittest.main()