# Instructions pour jouer à Tetris Duel

## Comment lancer le jeu
1. Assurez-vous que Python 3.6 ou plus récent est installé sur votre ordinateur
2. Exécutez la commande: `python run.py` depuis le répertoire du projet

## Règles du jeu
Tetris Duel est une version spéciale de Tetris où un joueur humain affronte une intelligence artificielle.

### Règles classiques
- Des pièces de différentes formes tombent du haut de la grille
- Le joueur peut déplacer et faire tourner ces pièces avant qu'elles ne se placent
- Lorsqu'une ligne horizontale est complète, elle disparaît et rapporte des points
- Le jeu se termine quand les pièces atteignent le haut de la grille

### Règles spéciales
1. **Cadeau surprise**: Quand un joueur complète 2 lignes d'un coup, l'adversaire reçoit une pièce facile (carré ou ligne)
2. **Pause douceur**: Tous les 1000 points, les pièces tombent 20% plus lentement pendant 10 secondes
3. **Pièce rigolote**: Tous les 3000 points, une pièce spéciale en forme de cœur ou d'étoile apparaît et vaut 100 points bonus
4. **Arc-en-ciel**: Toutes les 2 minutes, les pièces changent de couleur pendant 20 secondes

### Tableau des scores
- 50 points par ligne complétée
- Bonus: +100 pour 2 lignes, +200 pour 3 lignes, +300 pour 4 lignes
- +100 points pour placer correctement une pièce rigolote

## Contrôles
- **Flèche gauche**: Déplacer la pièce vers la gauche
- **Flèche droite**: Déplacer la pièce vers la droite
- **Flèche bas**: Accélérer la descente de la pièce
- **Flèche haut**: Faire pivoter la pièce
- **Espace**: Faire tomber la pièce instantanément
- **R**: Redémarrer la partie

## Astuces
- Gardez la pile de pièces aussi basse que possible
- Préparez-vous à recevoir des Tetris (4 lignes d'un coup) pour maximiser votre score
- Utilisez les pièces rigolotes pour remplir les trous difficiles
- Profitez des périodes de pause douceur pour mieux organiser votre grille
