import unittest
import sys
import os
import tkinter as tk

# Add the parent directory to the path to import the src modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.scoreboard import Scoreboard

class TestScoreboard(unittest.TestCase):
    def setUp(self):
        """Set up the initial conditions for the tests."""
        self.root = tk.Tk()
        self.scoreboard = Scoreboard(self.root)
        self.scores = {
            'human': 0,
            'ai': 0
        }

    def test_update_score(self):
        """Test the update_score function for both players."""
        # Test updating human player's score
        self.scoreboard.update_score(human_score=100)
        self.assertEqual(self.scoreboard.human_score, 100, "Human player's score should be updated to 100.")

        # Test updating AI player's score
        self.scoreboard.update_score(ai_score=150)
        self.assertEqual(self.scoreboard.ai_score, 150, "AI player's score should be updated to 150.")

    def test_reset_scores(self):
        """Test the reset_scores function."""
        # First set scores to non-zero values
        self.scoreboard.update_score(human_score=100, ai_score=200)
        
        # Then reset them
        self.scoreboard.reset_scores()
        
        # Verify they're back to zero
        self.assertEqual(self.scoreboard.human_score, 0, "Human score should be reset to 0")
        self.assertEqual(self.scoreboard.ai_score, 0, "AI score should be reset to 0")

    def tearDown(self):
        """Clean up the Tkinter instance."""
        self.root.destroy()

if __name__ == '__main__':
    unittest.main()