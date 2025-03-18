# tetris_duel/src/performance.py

"""
Module d'optimisation des performances pour le jeu Tetris Duel.
"""

import time
import platform
import tkinter as tk
import gc

class PerformanceManager:
    def __init__(self, root=None):
        """
        Initialise le gestionnaire de performances.
        
        Args:
            root: Fenêtre principale de l'application Tkinter
        """
        self.root = root
        self.last_gc_time = time.time()
        self.gc_interval = 10  # Garbage collection interval in seconds
        self.frame_time = 0
        self.last_frame_time = time.time()
        self.frame_count = 0
        self.fps = 0
        
        # Paramètres de lissage FPS
        self.frame_times = []
        self.frame_time_window = 20  # Nombre de frames pour le calcul de moyenne
        
        # Paramètres de limitation de FPS
        self.target_fps = 60
        self.frame_time_deficit = 0
        self.vsync_enabled = False
        
        # Détection du système
        self.system = platform.system()
        
    def optimize_tkinter(self, canvas=None):
        """
        Optimise les paramètres Tkinter pour de meilleures performances.
        
        Args:
            canvas: Canvas Tkinter à optimiser
        """
        if not self.root:
            return
            
        # Désactiver la mise à jour en temps réel
        if canvas:
            canvas.config(takefocus=0)
            
        # Optimisations spécifiques à chaque système
        if self.system == "Windows":
            try:
                # Optimisations Windows
                self.root.call('tk', 'scaling', 1.0)
                self.root.option_add('*Font', 'TkDefaultFont 9')
            except:
                pass
        elif self.system == "Darwin":  # macOS
            try:
                # Optimisations macOS
                self.root.option_add('*Font', 'TkDefaultFont 12')
            except:
                pass
        
        # Désactiver le redimensionnement pour éviter les recalculs
        self.root.resizable(False, False)
        
    def begin_frame(self):
        """
        Marque le début d'une nouvelle frame.
        """
        # Exécuter le garbage collector périodiquement
        current_time = time.time()
        if current_time - self.last_gc_time > self.gc_interval:
            gc.collect()
            self.last_gc_time = current_time
            
        self.last_frame_time = current_time
        
    def end_frame(self):
        """
        Marque la fin d'une frame et calcule le temps écoulé.
        
        Returns:
            float: Temps écoulé pour cette frame en secondes
        """
        current_time = time.time()
        self.frame_time = current_time - self.last_frame_time
        self.frame_count += 1
        
        # Mettre à jour la fenêtre glissante des temps de frame
        self.frame_times.append(self.frame_time)
        if len(self.frame_times) > self.frame_time_window:
            self.frame_times.pop(0)
        
        # Calculer le FPS moyen sur la fenêtre de temps
        if self.frame_times:
            avg_frame_time = sum(self.frame_times) / len(self.frame_times)
            if avg_frame_time > 0:
                self.fps = 1.0 / avg_frame_time
                
        return self.frame_time
    
    def get_fps(self):
        """
        Retourne le FPS actuel.
        
        Returns:
            int: Frames par seconde
        """
        return int(self.fps)
    
    def set_fps_mode(self, mode):
        """
        Configure un mode FPS prédéfini.
        
        Args:
            mode: String représentant le mode ('30', '60', 'unlimited')
        """
        if mode == '30':
            self.target_fps = 30
            self.frame_time_window = 15
            self.vsync_enabled = False
        elif mode == '60':
            self.target_fps = 60
            self.frame_time_window = 20
            self.vsync_enabled = False
        elif mode == 'vsync':
            self.vsync_enabled = True
        else:  # unlimited
            self.target_fps = 0  # pas de limite
            self.vsync_enabled = False
    
    def limit_fps(self, target_fps=None):
        """
        Limite le FPS en attendant si nécessaire, avec compensation.
        
        Args:
            target_fps: FPS cible (optionnel, utilise self.target_fps par défaut)
        """
        if target_fps is not None:
            self.target_fps = target_fps
            
        # Si le mode vsync est activé ou aucune limite n'est définie
        if self.vsync_enabled or self.target_fps <= 0:
            return
            
        target_frame_time = 1.0 / self.target_fps
        
        # Calculer le temps d'attente nécessaire (avec compensation)
        wait_time = target_frame_time - self.frame_time - self.frame_time_deficit
        
        if wait_time > 0:
            # Technique de sleep de précision pour minimiser le jitter
            end_wait = time.time() + wait_time
            
            # Sleep grossier jusqu'à ~1ms avant la fin
            coarse_wait = wait_time - 0.001
            if coarse_wait > 0:
                time.sleep(coarse_wait)
                
            # Attente active pour la précision finale
            while time.time() < end_wait:
                pass
                
            # Calculer le temps réel d'attente
            actual_wait = time.time() - (self.last_frame_time + self.frame_time)
            # Calculer le déficit pour la prochaine frame
            self.frame_time_deficit = actual_wait - wait_time
        else:
            # Si nous sommes en retard, limiter l'accumulation du déficit
            self.frame_time_deficit = max(-target_frame_time/2, wait_time)
            
    def synchronize_with_display(self):
        """
        Synchronise avec le taux de rafraîchissement de l'affichage si vsync est activé.
        À appeler juste avant l'affichage d'une nouvelle frame.
        """
        if self.vsync_enabled and self.root:
            self.root.update_idletasks()  # Force le traitement des événements graphiques
