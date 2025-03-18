import time
import threading

class GameTimer:
    """
    A class to manage the game timer and special events for Tetris Duel.
    """

    def __init__(self):
        self.start_time = None
        self.elapsed_time = 0
        self.special_events = {
            'rainbow_effect': 120,  # every 2 minutes (120 seconds)
            'gentle_pause': 1000,   # every 1000 points
            'funny_pieces': 3000    # every 3000 points
        }
        self.event_timers = {
            'rainbow_effect': None,
            'gentle_pause': None,
            'funny_pieces': None
        }
        self.lock = threading.Lock()
        self.last_rainbow_check = 0
        self.rainbow_activated = False

    def start_timer(self):
        """
        Start the game timer in a separate thread.
        """
        self.start_time = time.time()
        threading.Thread(target=self._run_timer, daemon=True).start()

    def _run_timer(self):
        """
        Internal method to run the timer and check for special events.
        """
        while True:
            with self.lock:
                self.elapsed_time = time.time() - self.start_time
            time.sleep(0.1)  # Check more frequently for smoother updates

    def check_special_events(self, score=0):
        """
        Check for special events based on the elapsed time and score.

        Args:
            score (int): The current score of the player.
        """
        # Check for rainbow effect every 2 minutes
        if self.elapsed_time // 120 > self.last_rainbow_check // 120:
            self.trigger_event('rainbow_effect')
            self.last_rainbow_check = self.elapsed_time

        # Check for gentle pause every 1000 points
        if score // 1000 > (score - 1) // 1000 and score > 0:
            self.trigger_event('gentle_pause')

        # Check for funny pieces every 3000 points
        if score // 3000 > (score - 1) // 3000 and score > 0:
            self.trigger_event('funny_pieces')

    def check_rainbow_event(self):
        """
        Check if it's time to trigger the rainbow effect.
        
        Returns:
            bool: True if rainbow effect should be activated, False otherwise.
        """
        # Check if 2 minutes have passed since the last rainbow event
        current_period = int(self.elapsed_time // 120)
        last_period = int(self.last_rainbow_check // 120)
        
        if current_period > last_period:
            self.last_rainbow_check = self.elapsed_time
            self.rainbow_activated = True
            return True
            
        return False

    def trigger_event(self, event_name):
        """
        Trigger a special event.

        Args:
            event_name (str): The name of the event to trigger.
        """
        if event_name in self.event_timers and self.event_timers[event_name] is None:
            print(f"Triggering event: {event_name}")
            # Reset the timer for this event
            self.event_timers[event_name] = time.time()
            
            # Special handling for rainbow effect
            if event_name == 'rainbow_effect':
                self.rainbow_activated = True

    def reset_event(self, event_name):
        """
        Reset the timer for a specific event.

        Args:
            event_name (str): The name of the event to reset.
        """
        if event_name in self.event_timers:
            self.event_timers[event_name] = None
            
            # Special handling for rainbow effect
            if event_name == 'rainbow_effect':
                self.rainbow_activated = False

    def get_elapsed_time_formatted(self):
        """
        Get the elapsed time in a human-readable format.
        
        Returns:
            str: Time in format MM:SS
        """
        minutes = int(self.elapsed_time // 60)
        seconds = int(self.elapsed_time % 60)
        return f"{minutes:02d}:{seconds:02d}"

# Example usage
if __name__ == "__main__":
    timer = GameTimer()
    timer.start_timer()
    while True:
        time.sleep(1)  # Simulate game running
        print(f"Elapsed time: {timer.get_elapsed_time_formatted()}")