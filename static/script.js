// Complete Game Logic for Tetris

// Game state variables
let humanPlayerScore = 0;
let aiPlayerScore = 0;
let humanGrid = createEmptyGrid();
let aiGrid = createEmptyGrid();
let currentPiece = null;
let nextPiece = null;
let aiCurrentPiece = null;
let gameSpeed = 1000; // ms per drop
let aiMoveDelay = 1000; // L'IA est 3x plus lente que le joueur
let lastMoveTime = 0;
let lastAiMoveTime = 0;
let gameActive = false;
let gamePaused = false;
let gameStartTime = 0;
let rainbowModeActive = false;
let pauseActive = false;

// Tetris piece definitions with authentic colors
const PIECES = {
    I: { shape: [[1, 1, 1, 1]], color: 'var(--tetris-cyan)' },
    O: { shape: [[1, 1], [1, 1]], color: 'var(--tetris-yellow)' },
    T: { shape: [[0, 1, 0], [1, 1, 1]], color: 'var(--tetris-purple)' },
    S: { shape: [[0, 1, 1], [1, 1, 0]], color: 'var(--tetris-green)' },
    Z: { shape: [[1, 1, 0], [0, 1, 1]], color: 'var(--tetris-red)' },
    J: { shape: [[1, 0, 0], [1, 1, 1]], color: 'var(--tetris-blue)' },
    L: { shape: [[0, 0, 1], [1, 1, 1]], color: 'var(--tetris-orange)' },
    HEART: { 
        shape: [[0, 1, 0, 1, 0], [1, 1, 1, 1, 1], [1, 1, 1, 1, 1], [0, 1, 1, 1, 0], [0, 0, 1, 0, 0]], 
        color: 'var(--tetris-pink)', 
        special: 'funny' 
    }
};

// Variables de l'IA
let tetrisAI = null;
let aiDifficultyLevel = 'medium'; // 'easy', 'medium', 'hard'

// Initialize the game
function initGame() {
    humanPlayerScore = 0;
    aiPlayerScore = 0;
    humanGrid = createEmptyGrid();
    aiGrid = createEmptyGrid();
    gameActive = true;
    gamePaused = false;
    gameStartTime = Date.now();
    lastMoveTime = Date.now();
    lastAiMoveTime = Date.now();
    
    // Generate first pieces
    spawnNewPiece();
    generateNextPiece();
    spawnAiPiece();
    
    updateScore();
    renderGrids();
    renderNextPiece();
    
    // Start game loop
    gameLoop();
    
    // Set up rainbow mode checker (every 2 minutes)
    clearInterval(window.rainbowInterval);
    window.rainbowInterval = setInterval(checkRainbowMode, 120000);
    
    // Update UI
    document.getElementById('pauseBtn').textContent = "Pause";

    // Initialiser l'IA
    tetrisAI = new TetrisAI();
}

// Toggle pause game
function togglePause() {
    gamePaused = !gamePaused;
    
    if (gamePaused) {
        document.getElementById('pauseBtn').textContent = "Reprendre";
        showMessage("Jeu en pause");
    } else {
        document.getElementById('pauseBtn').textContent = "Pause";
        lastMoveTime = Date.now();
        lastAiMoveTime = Date.now();
        requestAnimationFrame(gameLoop);
    }
}

// Create an empty grid for Tetris
function createEmptyGrid() {
    return Array.from({ length: 20 }, () => Array(10).fill(0));
}

// Game loop
function gameLoop() {
    if (!gameActive || gamePaused) return;
    
    const currentTime = Date.now();
    
    // Player movement
    if (currentTime - lastMoveTime > gameSpeed) {
        moveDown(currentPiece, humanGrid);
        lastMoveTime = currentTime;
    }
    
    // AI movement (ralenti)
    if (currentTime - lastAiMoveTime > aiMoveDelay) {
        aiMove();
        lastAiMoveTime = currentTime;
    }
    
    renderGrids();
    renderNextPiece();
    requestAnimationFrame(gameLoop);
}

// Generate the next piece to show in the preview
function generateNextPiece() {
    // Check if we should spawn a funny piece
    if (humanPlayerScore > 0 && humanPlayerScore % 3000 < 100 && !currentPiece?.special) {
        nextPiece = {
            ...PIECES.HEART,
            position: { x: 0, y: 0 },
            special: 'funny'
        };
    } else if (nextPiece?.receivingGift) {
        // Give an easy piece (gift)
        const giftPieces = [PIECES.I, PIECES.O];
        const selectedPiece = giftPieces[Math.floor(Math.random() * giftPieces.length)];
        nextPiece = {
            ...selectedPiece,
            position: { x: 0, y: 0 },
            receivingGift: false
        };
    } else {
        const pieces = Object.values(PIECES).filter(p => !p.special);
        const randomPiece = pieces[Math.floor(Math.random() * pieces.length)];
        nextPiece = {
            ...randomPiece,
            position: { x: 0, y: 0 }
        };
    }
}

// Spawn a new piece for the human player
function spawnNewPiece() {
    // Use the next piece if available
    if (nextPiece) {
        currentPiece = { ...nextPiece, position: { x: 3, y: 0 } };
        generateNextPiece();
    } else {
        // First game piece
        const pieces = Object.values(PIECES).filter(p => !p.special);
        const randomPiece = pieces[Math.floor(Math.random() * pieces.length)];
        currentPiece = {
            ...randomPiece,
            position: { x: 3, y: 0 }
        };
        generateNextPiece();
    }
    
    // Check game over
    if (!canPlace(currentPiece, humanGrid)) {
        gameActive = false;
        showMessage(`Game Over! Votre score: ${humanPlayerScore}`);
    }
}

// Render the next piece in the preview box
function renderNextPiece() {
    if (!nextPiece) return;
    
    const container = document.getElementById('nextPieceDisplay');
    if (!container) return;
    
    container.innerHTML = '';
    
    const { shape, color } = nextPiece;
    
    // Create a mini grid for the next piece
    const pieceGrid = document.createElement('div');
    pieceGrid.className = 'next-piece-grid';
    pieceGrid.style.display = 'flex';
    pieceGrid.style.flexDirection = 'column';
    pieceGrid.style.height = '100%';
    pieceGrid.style.justifyContent = 'center';
    
    // Add rows
    for (let y = 0; y < shape.length; y++) {
        const row = document.createElement('div');
        row.style.display = 'flex';
        row.style.justifyContent = 'center';
        
        // Add cells
        for (let x = 0; x < shape[y].length; x++) {
            const cell = document.createElement('div');
            cell.style.width = '15px';
            cell.style.height = '15px';
            cell.style.border = '1px solid rgba(255,255,255,0.1)';
            
            if (shape[y][x]) {
                cell.style.backgroundColor = color;
                if (nextPiece.special) {
                    cell.style.backgroundImage = 'radial-gradient(circle, rgba(255,255,255,0.7) 0%, rgba(255,255,255,0) 70%)';
                    cell.style.animation = 'pulse 1.5s infinite alternate';
                }
            }
            
            row.appendChild(cell);
        }
        
        pieceGrid.appendChild(row);
    }
    
    container.appendChild(pieceGrid);
}

// Spawn a new piece for the AI player
function spawnAiPiece() {
    // Similar logic to spawnNewPiece but for AI
    if (aiPlayerScore > 0 && aiPlayerScore % 3000 < 100 && !aiCurrentPiece?.special) {
        aiCurrentPiece = {
            ...PIECES.HEART,
            position: { x: 3, y: 0 },
            special: 'funny'
        };
    } else if (aiCurrentPiece?.receivingGift) {
        const giftPieces = [PIECES.I, PIECES.O];
        const selectedPiece = giftPieces[Math.floor(Math.random() * giftPieces.length)];
        aiCurrentPiece = {
            ...selectedPiece,
            position: { x: 3, y: 0 },
            receivingGift: false
        };
    } else {
        const pieces = Object.values(PIECES).filter(p => !p.special);
        const randomPiece = pieces[Math.floor(Math.random() * pieces.length)];
        aiCurrentPiece = {
            ...randomPiece,
            position: { x: 3, y: 0 }
        };
    }
    
    if (!canPlace(aiCurrentPiece, aiGrid)) {
        gameActive = false;
        showMessage(`Game Over! Score IA: ${aiPlayerScore}`);
    }
}

// Handle user input for moving and rotating pieces
function handleInput(event) {
    if (!gameActive || gamePaused) return;
    
    switch (event.key) {
        case 'ArrowLeft':
            movePiece(-1);
            break;
        case 'ArrowRight':
            movePiece(1);
            break;
        case 'ArrowDown':
            dropPiece();
            break;
        case 'ArrowUp':
            rotatePiece();
            break;
        case ' ': // Space bar for hard drop
            hardDrop();
            break;
        case 'p': // P key for pause
        case 'P':
            togglePause();
            break;
    }
    renderGrids();
    
    // Prevent default action (page scrolling)
    event.preventDefault();
}

// Move the current piece left or right
function movePiece(direction) {
    if (canMove(currentPiece, humanGrid, direction, 0)) {
        currentPiece.position.x += direction;
        return true;
    }
    return false;
}

// Check if piece can move in a direction
function canMove(piece, grid, xOffset, yOffset) {
    const { shape, position } = piece;
    
    for (let y = 0; y < shape.length; y++) {
        for (let x = 0; x < shape[y].length; x++) {
            if (shape[y][x]) {
                const newX = position.x + x + xOffset;
                const newY = position.y + y + yOffset;
                
                if (newX < 0 || newX >= 10 || newY >= 20 || 
                   (newY >= 0 && grid[newY][newX])) {
                    return false;
                }
            }
        }
    }
    return true;
}

// Move the piece down one row
function moveDown(piece, grid) {
    if (piece && canMove(piece, grid, 0, 1)) {
        piece.position.y++;
        return true;
    }
    
    if (piece === currentPiece) {
        placePiece(currentPiece, humanGrid);
        const linesCleared = checkForLines(humanGrid);
        updateScore(linesCleared, 'human');
        spawnNewPiece();
    } else if (piece === aiCurrentPiece) {
        placePiece(aiCurrentPiece, aiGrid);
        const linesCleared = checkForLines(aiGrid);
        updateScore(linesCleared, 'ai');
        spawnAiPiece();
    }
    
    return false;
}

// Drop the current piece one row
function dropPiece() {
    moveDown(currentPiece, humanGrid);
}

// Hard drop - drop the piece all the way down
function hardDrop() {
    while (moveDown(currentPiece, humanGrid)) {}
}

// Rotate the current piece
function rotatePiece() {
    const rotatedShape = rotateMatrix(currentPiece.shape);
    const originalShape = currentPiece.shape;
    
    currentPiece.shape = rotatedShape;
    
    if (!canPlace(currentPiece, humanGrid)) {
        // Try wall kicks
        const originalX = currentPiece.position.x;
        
        // Try moving right
        currentPiece.position.x += 1;
        if (canPlace(currentPiece, humanGrid)) {
            return;
        }
        
        // Try moving left
        currentPiece.position.x = originalX - 1;
        if (canPlace(currentPiece, humanGrid)) {
            return;
        }
        
        // If all fails, revert rotation
        currentPiece.position.x = originalX;
        currentPiece.shape = originalShape;
    }
}

// Rotate a matrix (for piece rotation)
function rotateMatrix(matrix) {
    const N = matrix.length;
    const M = matrix[0].length;
    let result = Array.from({ length: M }, () => Array(N).fill(0));
    
    for (let y = 0; y < N; y++) {
        for (let x = 0; x < M; x++) {
            result[x][N-1-y] = matrix[y][x];
        }
    }
    
    return result;
}

// Check if a piece can be placed on the grid
function canPlace(piece, grid) {
    return canMove(piece, grid, 0, 0);
}

// Place the current piece on the grid
function placePiece(piece, grid) {
    const { shape, position, color, special } = piece;
    
    for (let y = 0; y < shape.length; y++) {
        for (let x = 0; x < shape[y].length; x++) {
            if (shape[y][x]) {
                const gridY = position.y + y;
                const gridX = position.x + x;
                
                if (gridY >= 0) {
                    grid[gridY][gridX] = {
                        color: rainbowModeActive ? getRandomColor() : color,
                        special: special || false
                    };
                }
            }
        }
    }
}

// Check for completed lines and remove them
function checkForLines(grid) {
    let linesCleared = 0;
    
    for (let y = 0; y < grid.length; y++) {
        if (grid[y].every(cell => cell !== 0)) {
            // Remove the line
            grid.splice(y, 1);
            // Add empty line at top
            grid.unshift(Array(10).fill(0));
            linesCleared++;
        }
    }
    
    return linesCleared;
}

// Update the score based on lines cleared
function updateScore(linesCleared, player) {
    if (!linesCleared) return;
    
    let points = 0;
    
    // Base points
    if (linesCleared === 1) {
        points = 50;
    } 
    // Bonuses for multiple lines
    else if (linesCleared === 2) {
        points = 100 + (50 * 2); // 50 per line + 100 bonus
        
        // Surprise gift for opponent
        if (player === 'human') {
            aiCurrentPiece.receivingGift = true;
        } else {
            currentPiece.receivingGift = true;
        }
    } 
    else if (linesCleared === 3) {
        points = 200 + (50 * 3); // 50 per line + 200 bonus
    } 
    else if (linesCleared === 4) {
        points = 300 + (50 * 4); // 50 per line + 300 bonus (Tetris)
    }
    
    // Add funny piece bonus
    const specialCells = checkForSpecialPieces(player === 'human' ? humanGrid : aiGrid);
    if (specialCells > 0) {
        points += 100;
    }
    
    if (player === 'human') {
        humanPlayerScore += points;
        // Check for pause douceur
        checkPauseDouceur(humanPlayerScore);
    } else {
        aiPlayerScore += points;
        checkPauseDouceur(aiPlayerScore);
    }
    
    // Update the display
    document.getElementById('humanScore').innerText = humanPlayerScore;
    document.getElementById('aiScore').innerText = aiPlayerScore;
}

// Check for special pieces in the grid
function checkForSpecialPieces(grid) {
    let count = 0;
    
    for (let y = 0; y < grid.length; y++) {
        for (let x = 0; x < grid[y].length; x++) {
            if (grid[y][x] && grid[y][x].special) {
                count++;
            }
        }
    }
    
    return count;
}

// Check for "pause douceur" (slow down after hitting score milestones)
function checkPauseDouceur(score) {
    if (score > 0 && score % 1000 < 100 && !pauseActive) {
        pauseActive = true;
        const originalSpeed = gameSpeed;
        gameSpeed *= 1.2; // 20% slower
        
        setTimeout(() => {
            gameSpeed = originalSpeed;
            pauseActive = false;
        }, 10000); // 10 seconds of slower gameplay
        
        // Show feedback to the player
        showMessage("Pause douceur! Game slowed by 20% for 10 seconds.");
    }
}

// Toggle rainbow mode every 2 minutes
function checkRainbowMode() {
    rainbowModeActive = true;
    showMessage("Rainbow Mode Activated! 🌈");
    
    setTimeout(() => {
        rainbowModeActive = false;
    }, 20000); // Rainbow mode lasts 20 seconds
}

// Get a random color for rainbow mode
function getRandomColor() {
    const colors = ['#FF0000', '#FF7F00', '#FFFF00', '#00FF00', '#0000FF', '#4B0082', '#9400D3'];
    return colors[Math.floor(Math.random() * colors.length)];
}

// AI logic - mise à jour pour utiliser la nouvelle IA
function aiMove() {
    if (!aiCurrentPiece) return;
    
    // Décision de l'IA basée sur la difficulté
    let decisions;
    
    if (aiDifficultyLevel === 'easy') {
        // Mode facile: IA simplifiée et aléatoire
        decisions = tetrisAI.makeEasyMove(aiCurrentPiece, aiGrid);
    } else {
        // Mode medium et hard: IA avancée
        decisions = tetrisAI.findBestMove(aiCurrentPiece, aiGrid);
        
        // En mode medium, parfois faire une erreur intentionnelle
        if (aiDifficultyLevel === 'medium' && Math.random() < 0.3) {
            // 30% de chance de faire une erreur en mode medium
            let randomOffset = Math.floor(Math.random() * 3) - 1; // -1, 0, ou 1
            decisions.x += randomOffset;
        }
    }
    
    // Appliquer les décisions
    aiCurrentPiece.position.x = decisions.x;
    
    // Tourner la pièce selon la rotation optimale
    for (let i = 0; i < decisions.rotations; i++) {
        const rotatedShape = rotateMatrix(aiCurrentPiece.shape);
        aiCurrentPiece.shape = rotatedShape;
    }
    
    // Faire descendre la pièce d'une ligne
    moveDown(aiCurrentPiece, aiGrid);
    renderGrids();
}

// Calculate the best move for the AI
function calculateBestMove(piece, grid) {
    // Simple algorithm: prefer positions that result in the most contacts
    let bestScore = -1;
    let bestX = 0;
    let bestRotations = 0;
    
    // Try each rotation
    for (let rotations = 0; rotations < 4; rotations++) {
        let testPiece = JSON.parse(JSON.stringify(piece));
        
        // Apply rotations
        for (let i = 0; i < rotations; i++) {
            testPiece.shape = rotateMatrix(testPiece.shape);
        }
        
        // Try each horizontal position
        for (let x = -2; x < 10; x++) {
            testPiece.position = { x, y: 0 };
            
            if (!canPlace(testPiece, grid)) continue;
            
            // Drop the piece
            while (canMove(testPiece, grid, 0, 1)) {
                testPiece.position.y++;
            }
            
            // Calculate score based on height and contacts
            const score = calculateScore(testPiece, grid);
            
            if (score > bestScore) {
                bestScore = score;
                bestX = x;
                bestRotations = rotations;
            }
        }
    }
    
    return { x: bestX, rotations: bestRotations };
}

// Calculate a score for an AI move
function calculateScore(piece, grid) {
    // Implement a simple scoring strategy
    let score = 0;
    const maxHeight = getHighestPoint(piece);
    
    // Prefer lower placements
    score -= maxHeight * 2;
    
    // Prefer positions with more contacts
    score += countContacts(piece, grid) * 3;
    
    return score;
}

// Get highest point of a piece
function getHighestPoint(piece) {
    return piece.position.y;
}

// Count contacts between piece and existing blocks/floor
function countContacts(piece, grid) {
    let contacts = 0;
    const { shape, position } = piece;
    
    for (let y = 0; y < shape.length; y++) {
        for (let x = 0; x < shape[y].length; x++) {
            if (shape[y][x]) {
                const gridY = position.y + y;
                const gridX = position.x + x;
                
                // Check below
                if (gridY + 1 >= 20 || (gridY + 1 < 20 && gridY + 1 >= 0 && grid[gridY + 1][gridX])) {
                    contacts++;
                }
                
                // Check left
                if (gridX - 1 < 0 || (gridX - 1 >= 0 && grid[gridY][gridX - 1])) {
                    contacts++;
                }
                
                // Check right
                if (gridX + 1 >= 10 || (gridX + 1 < 10 && grid[gridY][gridX + 1])) {
                    contacts++;
                }
            }
        }
    }
    
    return contacts;
}

// Mise à jour de la vitesse de l'IA en fonction du niveau de difficulté
function updateAIDifficulty(level) {
    aiDifficultyLevel = level;
    
    switch(level) {
        case 'easy':
            aiMoveDelay = 2000; // 2 secondes pour niveau facile
            break;
        case 'medium':
            aiMoveDelay = 1000; // 1 seconde pour niveau moyen
            break;
        case 'hard':
            aiMoveDelay = 500; // 0.5 secondes pour niveau difficile
            break;
    }
}

// Ajout d'une fonction pour changer la difficulté
function changeDifficulty(level) {
    updateAIDifficulty(level);
    showMessage(`Difficulté IA: ${level.toUpperCase()}`);
}

// Render the game grids
function renderGrids() {
    const humanGridEl = document.getElementById('humanGrid');
    const aiGridEl = document.getElementById('aiGrid');
    
    if (!humanGridEl || !aiGridEl) return;
    
    // Clear grids
    humanGridEl.innerHTML = '';
    aiGridEl.innerHTML = '';
    
    // Create a temporary grid with the active piece
    const tempHumanGrid = JSON.parse(JSON.stringify(humanGrid));
    const tempAiGrid = JSON.parse(JSON.stringify(aiGrid));
    
    // Add the current pieces to the temporary grids
    if (currentPiece) {
        addPieceToTempGrid(currentPiece, tempHumanGrid);
    }
    
    if (aiCurrentPiece) {
        addPieceToTempGrid(aiCurrentPiece, tempAiGrid);
    }
    
    // Render human grid
    renderGrid(tempHumanGrid, humanGridEl);
    
    // Render AI grid
    renderGrid(tempAiGrid, aiGridEl);
}

// Add a piece to a temporary grid for rendering
function addPieceToTempGrid(piece, tempGrid) {
    const { shape, position, color } = piece;
    
    for (let y = 0; y < shape.length; y++) {
        for (let x = 0; x < shape[y].length; x++) {
            if (shape[y][x]) {
                const gridY = position.y + y;
                const gridX = position.x + x;
                
                if (gridY >= 0 && gridY < 20 && gridX >= 0 && gridX < 10) {
                    tempGrid[gridY][gridX] = {
                        color: rainbowModeActive ? getRandomColor() : color,
                        active: true,
                        special: piece.special || false
                    };
                }
            }
        }
    }
}

// Render a grid
function renderGrid(grid, element) {
    for (let y = 0; y < grid.length; y++) {
        const row = document.createElement('div');
        row.className = 'grid-row';
        
        for (let x = 0; x < grid[y].length; x++) {
            const cell = document.createElement('div');
            cell.className = 'grid-cell';
            
            if (grid[y][x]) {
                cell.style.backgroundColor = grid[y][x].color;
                
                if (grid[y][x].active) {
                    cell.classList.add('active');
                }
                
                if (grid[y][x].special) {
                    cell.classList.add('special');
                }
            }
            
            row.appendChild(cell);
        }
        
        element.appendChild(row);
    }
}

// Show a message to the player
function showMessage(message) {
    const messageEl = document.createElement('div');
    messageEl.className = 'game-message';
    messageEl.textContent = message;
    
    document.querySelector('main').appendChild(messageEl);
    
    setTimeout(() => {
        messageEl.classList.add('fade-out');
        setTimeout(() => {
            messageEl.remove();
        }, 500);
    }, 2000);
}

// Start the game on page load
window.onload = initGame;
// Event listener for keyboard input
document.addEventListener('keydown', handleInput);