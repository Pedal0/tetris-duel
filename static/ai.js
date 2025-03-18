/**
 * Intelligence Artificielle avancée pour Tetris
 * Utilise des heuristiques pour optimiser les placements
 */

// Coefficients de pondération pour les différentes heuristiques
const AI_WEIGHTS = {
    // Facteurs négatifs (à minimiser)
    heightWeight: -0.510066,      // Hauteur cumulée des colonnes
    linesWeight: 0.760666,        // Lignes complétées
    holesWeight: -0.35663,        // Trous dans la grille
    bumpinessWeight: -0.184483,   // Différences de hauteur entre colonnes adjacentes
    wellsWeight: -0.18,           // Puits profonds
    openTopColumnWeight: 0.2,     // Colonnes accessibles depuis le haut
    heightDiffWeight: -0.2        // Différence entre colonne la plus haute et plus basse
};

class TetrisAI {
    constructor() {
        this.grid = null;
        this.piece = null;
    }

    /**
     * Trouve le meilleur mouvement pour la pièce actuelle
     * @param {Object} piece - La pièce en mouvement
     * @param {Array} grid - La grille de jeu
     * @returns {Object} - Le mouvement optimal {x, rotations}
     */
    findBestMove(piece, grid) {
        this.grid = this.convertGrid(grid);
        this.piece = JSON.parse(JSON.stringify(piece));
        
        let bestScore = -Infinity;
        let bestPosition = { x: 0, rotations: 0 };
        
        // Essayer chaque rotation possible
        for (let rotations = 0; rotations < 4; rotations++) {
            let currentPiece = JSON.parse(JSON.stringify(piece));
            
            // Appliquer les rotations
            for (let r = 0; r < rotations; r++) {
                currentPiece.shape = this.rotateMatrix(currentPiece.shape);
            }
            
            // Essayer chaque position horizontale possible
            const minX = this.getMinValidX(currentPiece);
            const maxX = this.getMaxValidX(currentPiece);
            
            for (let x = minX; x <= maxX; x++) {
                const landingY = this.getLandingHeight(currentPiece, x);
                if (landingY === -1) continue; // Position impossible
                
                // Clone la grille et place la pièce
                const virtualGrid = this.cloneGrid(this.grid);
                this.placePiece(virtualGrid, currentPiece, x, landingY);
                
                // Éliminer les lignes complètes
                const linesCleared = this.clearLines(virtualGrid);
                
                // Évaluer la configuration résultante
                const score = this.evaluateGrid(virtualGrid, linesCleared);
                
                // Si meilleur score, sauvegarder la position
                if (score > bestScore) {
                    bestScore = score;
                    bestPosition = { x, rotations };
                }
            }
        }
        
        return bestPosition;
    }
    
    /**
     * Convertit la grille du format du jeu au format utilisé par l'IA
     */
    convertGrid(gameGrid) {
        const grid = Array.from({ length: 20 }, () => Array(10).fill(0));
        
        for (let y = 0; y < gameGrid.length; y++) {
            for (let x = 0; x < gameGrid[y].length; x++) {
                grid[y][x] = gameGrid[y][x] ? 1 : 0;
            }
        }
        
        return grid;
    }
    
    /**
     * Obtient la position x minimale valide pour une pièce
     */
    getMinValidX(piece) {
        const pieceWidth = piece.shape[0].length;
        return -Math.floor((pieceWidth - 1) / 2);
    }
    
    /**
     * Obtient la position x maximale valide pour une pièce
     */
    getMaxValidX(piece) {
        const pieceWidth = piece.shape[0].length;
        return 10 - Math.ceil(pieceWidth / 2);
    }
    
    /**
     * Fait tourner une matrice dans le sens horaire
     */
    rotateMatrix(matrix) {
        const N = matrix.length;
        const M = matrix[0].length;
        const result = Array.from({ length: M }, () => Array(N).fill(0));
        
        for (let y = 0; y < N; y++) {
            for (let x = 0; x < M; x++) {
                result[x][N-1-y] = matrix[y][x];
            }
        }
        
        return result;
    }
    
    /**
     * Obtient la hauteur d'atterrissage de la pièce
     */
    getLandingHeight(piece, x) {
        const pieceHeight = piece.shape.length;
        const pieceWidth = piece.shape[0].length;
        
        let y = 0;
        let isValid = false;
        
        while (y < 20) {
            if (this.isValidPosition(piece, x, y)) {
                isValid = true;
                y++;
            } else {
                break;
            }
        }
        
        return isValid ? y - 1 : -1;
    }
    
    /**
     * Vérifie si une position est valide pour la pièce
     */
    isValidPosition(piece, x, y) {
        const pieceHeight = piece.shape.length;
        const pieceWidth = piece.shape[0].length;
        
        for (let py = 0; py < pieceHeight; py++) {
            for (let px = 0; px < pieceWidth; px++) {
                if (!piece.shape[py][px]) continue;
                
                const gridY = y + py;
                const gridX = x + px;
                
                // Vérifier les limites de la grille
                if (gridY < 0 || gridY >= 20 || gridX < 0 || gridX >= 10) {
                    return false;
                }
                
                // Vérifier les collisions
                if (this.grid[gridY][gridX]) {
                    return false;
                }
            }
        }
        
        return true;
    }
    
    /**
     * Clone la grille
     */
    cloneGrid(grid) {
        return grid.map(row => [...row]);
    }
    
    /**
     * Place une pièce sur la grille virtuelle
     */
    placePiece(grid, piece, x, y) {
        const pieceHeight = piece.shape.length;
        const pieceWidth = piece.shape[0].length;
        
        for (let py = 0; py < pieceHeight; py++) {
            for (let px = 0; px < pieceWidth; px++) {
                if (piece.shape[py][px]) {
                    const gridY = y + py;
                    const gridX = x + px;
                    
                    if (gridY >= 0 && gridY < 20 && gridX >= 0 && gridX < 10) {
                        grid[gridY][gridX] = 1;
                    }
                }
            }
        }
    }
    
    /**
     * Élimine les lignes complètes et retourne le nombre éliminé
     */
    clearLines(grid) {
        let linesCleared = 0;
        
        for (let y = 0; y < grid.length; y++) {
            if (grid[y].every(cell => cell === 1)) {
                // Supprimer la ligne
                grid.splice(y, 1);
                // Ajouter une ligne vide en haut
                grid.unshift(Array(10).fill(0));
                linesCleared++;
            }
        }
        
        return linesCleared;
    }
    
    /**
     * Évalue une configuration de grille en utilisant plusieurs heuristiques
     */
    evaluateGrid(grid, linesCleared) {
        const heights = this.getColumnHeights(grid);
        const totalHeight = heights.reduce((sum, h) => sum + h, 0);
        const holes = this.countHoles(grid, heights);
        const bumpiness = this.calculateBumpiness(heights);
        const wells = this.calculateWells(heights);
        const openTopColumns = this.countOpenTopColumns(heights);
        const heightDiff = Math.max(...heights) - Math.min(...heights);
        
        // Calculer le score basé sur les coefficients de pondération
        return (
            AI_WEIGHTS.heightWeight * totalHeight +
            AI_WEIGHTS.linesWeight * linesCleared +
            AI_WEIGHTS.holesWeight * holes +
            AI_WEIGHTS.bumpinessWeight * bumpiness +
            AI_WEIGHTS.wellsWeight * wells +
            AI_WEIGHTS.openTopColumnWeight * openTopColumns +
            AI_WEIGHTS.heightDiffWeight * heightDiff
        );
    }
    
    /**
     * Calcule la hauteur de chaque colonne
     */
    getColumnHeights(grid) {
        const heights = Array(10).fill(0);
        
        for (let x = 0; x < 10; x++) {
            for (let y = 0; y < 20; y++) {
                if (grid[y][x]) {
                    heights[x] = 20 - y;
                    break;
                }
            }
        }
        
        return heights;
    }
    
    /**
     * Compte le nombre de trous dans la grille
     * Un trou est une cellule vide avec au moins un bloc au-dessus
     */
    countHoles(grid, heights) {
        let holes = 0;
        
        for (let x = 0; x < 10; x++) {
            let blockFound = false;
            
            for (let y = 0; y < 20; y++) {
                if (grid[y][x]) {
                    blockFound = true;
                } else if (blockFound) {
                    // Si on trouve une cellule vide sous un bloc, c'est un trou
                    holes++;
                }
            }
        }
        
        return holes;
    }
    
    /**
     * Calcule les irrégularités entre colonnes adjacentes
     */
    calculateBumpiness(heights) {
        let bumpiness = 0;
        
        for (let x = 0; x < 9; x++) {
            bumpiness += Math.abs(heights[x] - heights[x+1]);
        }
        
        return bumpiness;
    }
    
    /**
     * Calcule la profondeur des puits
     * Un puits est une colonne avec des colonnes plus hautes de chaque côté
     */
    calculateWells(heights) {
        let wells = 0;
        
        // Première colonne
        if (heights[0] < heights[1]) {
            wells += heights[1] - heights[0];
        }
        
        // Colonnes du milieu
        for (let x = 1; x < 9; x++) {
            const wellDepth = Math.min(heights[x-1], heights[x+1]) - heights[x];
            if (wellDepth > 0) {
                wells += wellDepth;
            }
        }
        
        // Dernière colonne
        if (heights[9] < heights[8]) {
            wells += heights[8] - heights[9];
        }
        
        return wells;
    }
    
    /**
     * Compte le nombre de colonnes facilement accessibles depuis le haut
     */
    countOpenTopColumns(heights) {
        const avgHeight = heights.reduce((sum, h) => sum + h, 0) / heights.length;
        return heights.filter(h => h <= avgHeight - 2).length;
    }
    
    /**
     * Décision simplifiée pour les niveaux faciles
     */
    makeEasyMove(piece, grid) {
        // Version simplifiée qui privilégie les placements équilibrés sans trop réfléchir
        const positions = [];
        
        // Essayer chaque rotation et position horizontale
        for (let rotations = 0; rotations < 4; rotations++) {
            let testPiece = JSON.parse(JSON.stringify(piece));
            
            // Appliquer les rotations
            for (let r = 0; r < rotations; r++) {
                testPiece.shape = this.rotateMatrix(testPiece.shape);
            }
            
            // Essayer plusieurs positions horizontales aléatoires
            for (let i = 0; i < 3; i++) {
                const x = Math.floor(Math.random() * 7);
                positions.push({x, rotations, score: Math.random()});
            }
        }
        
        // Trier par score aléatoire et retourner le meilleur
        positions.sort((a, b) => b.score - a.score);
        return positions[0];
    }
}

// Exporter la classe d'IA
window.TetrisAI = TetrisAI;
