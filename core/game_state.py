"""
Gestionnaire centralisé de l'état du jeu QIX
"""

from utils.game_zones import initialiser_zones_terrain
from config.constants import DEFAULT_GAME_STATE, DEFAULT_CONTROLS


class GameState:
    """Classe centralisée pour gérer l'état global du jeu"""
    
    def __init__(self):
        """Initialise l'état du jeu avec les valeurs par défaut"""
        # Configuration du jeu
        self.config = DEFAULT_GAME_STATE.copy()
        self.controls = DEFAULT_CONTROLS.copy()
        
        # Zones de jeu
        self.zones = initialiser_zones_terrain()
        
        # Scores
        self.score = 0
        self.score1 = 0 
        self.score2 = 0
        
        # État de jeu
        self.running = True
        self.mode_menu = False
        self.niveau_actuel = None
        
        # Invincibilité
        self.invincibilite1 = False
        self.invincibilite2 = False
        
    def get_zone(self, zone_name):
        """Retourne une zone spécifique"""
        return self.zones.get(zone_name, [])
    
    def set_config(self, **kwargs):
        """Met à jour la configuration du jeu"""
        self.config.update(kwargs)
        
    def set_controls(self, **kwargs):
        """Met à jour les contrôles du jeu"""
        self.controls.update(kwargs)
        
    def reset_zones(self):
        """Réinitialise toutes les zones de jeu"""
        self.zones = initialiser_zones_terrain()
        
    def is_two_player_mode(self):
        """Retourne True si le mode 2 joueurs est activé"""
        return self.config.get("deux", False)


# Instance globale (singleton)
game_state = GameState()