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
        
    def is_point_in_obstacle(self, x, y):
        """Vérifie rapidement si un point est dans un obstacle"""
        zone_obstacle = self.get_zone('zone_obstacle')
        for obstacle in zone_obstacle:
            # obstacle = [x_obstacle, y_obstacle, taille]
            if len(obstacle) == 3:
                ox, oy, taille = obstacle
                if ox <= x <= ox + taille and oy <= y <= oy + taille:
                    return True
        return False
        
    def is_two_player_mode(self):
        """Retourne True si le mode 2 joueurs est activé"""
        return self.config.get("deux", False)
    
    def get_player_controls(self, player_id):
        """Retourne les contrôles spécifiques pour un joueur selon le mode de jeu"""
        if player_id == 1:
            if self.is_two_player_mode():
                # Mode 2 joueurs : joueur 1 utilise les flèches et 'm' pour tracer
                return {
                    "movement": ["Left", "Right", "Up", "Down"],
                    "trace_key": "m",
                    "speed_key": "Suppr"  # Touche Suppr pour changer vitesse
                }
            else:
                # Mode 1 joueur : joueur 1 utilise les flèches et 'space' pour tracer
                return {
                    "movement": ["Left", "Right", "Up", "Down"],
                    "trace_key": "space",
                    "speed_key": "v"
                }
        elif player_id == 2 and self.is_two_player_mode():
            # Mode 2 joueurs : joueur 2 utilise QZSD et 'space' pour tracer
            return {
                "movement": ["q", "d", "z", "s"],  # gauche, droite, haut, bas
                "trace_key": "space",
                "speed_key": "v"
            }
        else:
            # Joueur 2 en mode 1 joueur (n'existe pas)
            return {
                "movement": [],
                "trace_key": None,
                "speed_key": None
            }
    
    def update_controls_for_mode(self):
        """Met à jour les contrôles selon le mode de jeu actuel"""
        if self.is_two_player_mode():
            self.controls.update({
                "touche_espace": "m",      # Joueur 1 trace avec 'm'
                "touche_espace2": "space", # Joueur 2 trace avec 'space'
                "touche_V": "Suppr",       # Joueur 1 change vitesse avec 'Suppr'
                "touche_V2": "v"           # Joueur 2 change vitesse avec 'v'
            })
        else:
            self.controls.update({
                "touche_espace": "space",  # Joueur 1 trace avec 'space'
                "touche_espace2": None,    # Pas de joueur 2
                "touche_V": "v",           # Joueur 1 change vitesse avec 'v'
                "touche_V2": None          # Pas de joueur 2
            })


# Instance globale (singleton)
game_state = GameState()