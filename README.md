# Tetris Duel

## Project Overview
Tetris Duel is a two-player Tetris game that pits a human player against an AI. The human player controls Tetris pieces using keyboard arrow keys, while the AI automatically places pieces according to its logic. The game features a real-time scoreboard that tracks the scores of both players, along with various special events and effects that enhance the gameplay experience.

## Features
- Display two separate grids for the human and AI players.
- Human player controls Tetris pieces using keyboard arrow keys.
- AI logic for automatic piece placement.
- Real-time scoreboard displaying scores for both players.
- Scoring rules for line completions and bonuses.
- Introduce surprise gifts for completing 2 lines.
- Gentle pause implemented for every 1,000 points scored.
- Funny pieces introduced every 3,000 points.
- Rainbow effect activated every 2 minutes.

## Prerequisites
- Python >= 3.6
- Tkinter (included with standard Python installations)

## Installation
1. Clone the repository:
   ```bash
   $ git clone https://github.com/yourusername/tetris_duel.git
   $ cd tetris_duel
   ```
2. (Optional) Create a virtual environment:
   ```bash
   $ python -m venv venv
   $ source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
3. Install dependencies:
   ```bash
   $ pip install -r requirements.txt
   ```

## Configuration
Edit the `config.py` file located in the `tetris_duel/config` directory to customize game settings, such as initial scores or game duration.

## Deployment
To deploy the game:
1. Ensure all prerequisites are met and dependencies installed.
2. Run the main application:
   ```bash
   $ python run.py
   ```
3. For production deployment, consider using platforms like Heroku or AWS by containerizing the application and using Docker (if applicable).

## Usage
- Launch the game by running the main script:
  ```bash
  $ python run.py
  ```
- Player controls:
  - Move left: Arrow Left
  - Move right: Arrow Right
  - Rotate: Arrow Up
  - Drop: Arrow Down

## Project Structure
```
tetris_duel/
├── .gitignore               # Specify files and directories to ignore in version control
├── README.md                # Project description and setup instructions
├── assets/
│   └── style.css            # Styles for the game interface
├── config/
│   └── config.py           # Configuration file for game settings
├── src/
│   ├── ai.py               # AI logic for automatic piece placement
│   ├── game.py             # Game logic and mechanics implementation
│   ├── main.py             # Main entry point for the Tetris Duel game
│   ├── scoreboard.py        # Score tracking and display
│   └── timer.py            # Manage game timer and special events
└── tests/
    ├── test_ai.py          # Unit tests for AI logic
    ├── test_game.py        # Unit tests for game logic
    ├── test_scoreboard.py   # Unit tests for scoreboard functionality
    └── test_timer.py        # Unit tests for timer functionality
```

## API Documentation
N/A

## Troubleshooting
- **Game does not start:** Ensure you have installed all dependencies and are using the correct Python version.
- **Controls not responding:** Check if the window is active and that you are using the correct keys.
- **Unexpected behavior from AI:** Review the AI logic in `ai.py` for any logical errors.

## Development
To set up a development environment:
1. Follow the installation steps above.
2. Use an IDE or text editor of your choice to modify the source code.
3. Run tests to ensure functionality:
   ```bash
   $ python -m unittest discover -s tests
   ```