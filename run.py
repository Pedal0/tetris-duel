#!/usr/bin/env python
# run.py - Script principal pour lancer le jeu Tetris Duel

import sys
import os

# Ajouter le répertoire du projet au path Python
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Importer le jeu
from src.main import run_game

if __name__ == "__main__":
    print("Démarrage de Tetris Duel...")
    print("Commandes : flèches (gauche, droite, bas), haut pour rotation, espace pour descente rapide")
    print("Appuyez sur 'R' pour redémarrer le jeu")
    run_game()
