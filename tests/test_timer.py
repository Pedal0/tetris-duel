import unittest
import sys
import os
import time

# Add the parent directory to the path to import the src modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.timer import GameTimer

class TestTimer(unittest.TestCase):
    def setUp(self):
        """Set up the initial conditions for the tests."""
        self.timer = GameTimer()

    def test_start_timer(self):
        """Test the start_timer function to ensure it initializes the timer correctly."""
        self.timer.start_timer()
        self.assertIsNotNone(self.timer.start_time, "Timer's start time should be set after starting.")
        
        # Allow a small delay to ensure timer is running
        time.sleep(0.1)
        self.assertGreater(self.timer.elapsed_time, 0, "Timer should be counting elapsed time.")

    def test_check_special_events(self):
        """Test the check_special_events function."""
        # Test rainbow effect at 0 points (should not trigger)
        events_before = self.timer.event_timers.copy()
        self.timer.check_special_events(0)
        self.assertEqual(self.timer.event_timers, events_before, "No events should be triggered at 0 points.")
        
        # Test gentle pause at 1000 points
        self.timer.check_special_events(1000)
        self.assertIsNotNone(self.timer.event_timers['gentle_pause'], "Gentle pause should be triggered at 1000 points.")

    def tearDown(self):
        """Clean up after tests if necessary."""
        pass

if __name__ == '__main__':
    unittest.main()