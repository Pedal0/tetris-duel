# tetris_duel/config/config.py

"""
Configuration file for Tetris Duel game settings.

This module contains all the configurable parameters for the game,
including grid sizes, scoring rules, and special event timings.
"""

# Game settings
GRID_WIDTH = 10  # Width of the Tetris grid
GRID_HEIGHT = 20  # Height of the Tetris grid
HUMAN_PLAYER_COLOR = "#00FF00"  # Color for the human player's pieces
AI_PLAYER_COLOR = "#FF0000"  # Color for the AI player's pieces

# Scoring settings
LINE_COMPLETION_SCORE = 100  # Score for completing a single line
BONUS_FOR_TWO_LINES = 300  # Bonus score for completing two lines at once
FUNNY_PIECE_SCORE_THRESHOLD = 3000  # Score threshold for introducing funny pieces
RAINBOW_EFFECT_INTERVAL = 120  # Interval in seconds for the rainbow effect
GENTLE_PAUSE_THRESHOLD = 1000  # Score threshold for gentle pause

# Game controls
HUMAN_PLAYER_CONTROLS = {
    "left": "Left Arrow",
    "right": "Right Arrow",
    "down": "Down Arrow",
    "rotate": "Up Arrow"
}

# AI settings
AI_MOVE_DELAY = 500  # Delay in milliseconds for AI moves

# Miscellaneous settings
ENABLE_SOUND = True  # Enable sound effects
ENABLE_MUSIC = True  # Enable background music

def get_game_settings():
    """
    Returns a dictionary of game settings for easy access.
    """
    return {
        "grid_width": GRID_WIDTH,
        "grid_height": GRID_HEIGHT,
        "human_player_color": HUMAN_PLAYER_COLOR,
        "ai_player_color": AI_PLAYER_COLOR,
        "line_completion_score": LINE_COMPLETION_SCORE,
        "bonus_for_two_lines": BONUS_FOR_TWO_LINES,
        "funny_piece_score_threshold": FUNNY_PIECE_SCORE_THRESHOLD,
        "rainbow_effect_interval": RAINBOW_EFFECT_INTERVAL,
        "gentle_pause_threshold": GENTLE_PAUSE_THRESHOLD,
        "human_player_controls": HUMAN_PLAYER_CONTROLS,
        "ai_move_delay": AI_MOVE_DELAY,
        "enable_sound": ENABLE_SOUND,
        "enable_music": ENABLE_MUSIC
    }