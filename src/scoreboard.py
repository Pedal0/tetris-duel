# scoreboard.py

import tkinter as tk

class Scoreboard:
    """
    A class to manage and display the scores for both players in the Tetris Duel game.
    """

    def __init__(self, master: tk.Tk):
        """
        Initializes the Scoreboard with a Tkinter frame and labels for both players' scores.

        Args:
            master (tk.Tk): The parent Tkinter window.
        """
        self.master = master
        self.frame = tk.Frame(master)
        self.frame.pack()

        self.human_score = 0
        self.ai_score = 0

        self.human_score_label = tk.Label(self.frame, text=f"Human Score: {self.human_score}", font=("Helvetica", 16))
        self.human_score_label.pack(side=tk.LEFT, padx=10)

        self.ai_score_label = tk.Label(self.frame, text=f"AI Score: {self.ai_score}", font=("Helvetica", 16))
        self.ai_score_label.pack(side=tk.LEFT, padx=10)

    def update_score(self, human_score=None, ai_score=None) -> None:
        """
        Updates the scores for both players.

        Args:
            human_score (int, optional): The new score for the human player.
            ai_score (int, optional): The new score for the AI player.
        """
        if human_score is not None:
            self.human_score = human_score
        if ai_score is not None:
            self.ai_score = ai_score
        self.display_scores()

    def display_scores(self) -> None:
        """
        Updates the displayed scores on the scoreboard.
        """
        self.human_score_label.config(text=f"Human Score: {self.human_score}")
        self.ai_score_label.config(text=f"AI Score: {self.ai_score}")

    def reset_scores(self) -> None:
        """
        Resets the scores for both players to zero.
        """
        self.human_score = 0
        self.ai_score = 0
        self.display_scores()

# Example usage:
if __name__ == "__main__":
    root = tk.Tk()
    scoreboard = Scoreboard(root)
    scoreboard.update_score(10, 5)  # Example score update
    root.mainloop()