"""
Module Powerup - Gestion des bonus et powerups dans le jeu QIX
"""
from fltk import efface
from time import time


class Powerup:
    """Classe représentant un powerup/bonus dans le jeu"""
    
    def __init__(self, x, y, powerup_id, sprite_path, effect_duration=3):
        """
        Initialise un powerup
        
        Args:
            x (int): Position x du powerup
            y (int): Position y du powerup  
            powerup_id (int): Identifiant unique du powerup (1-5)
            sprite_path (str): Chemin vers l'image du powerup
            effect_duration (int): Durée de l'effet en secondes
        """
        self.x = x
        self.y = y
        self.powerup_id = powerup_id
        self.is_active = True
        self.tag = f"pomme{powerup_id}"
    
    def check_collision(self, player_x, player_y):
        """
        Vérifie si un joueur entre en collision avec ce powerup
        
        Args:
            player_x (int): Position x du joueur
            player_y (int): Position y du joueur
            
        Returns:
            bool: True si collision détectée
        """
        if not self.is_active:
            return False
            
        # Utiliser une détection par proximité plus flexible
        # Zone de collision de 20x20 pixels autour du powerup
        distance_x = abs(player_x - self.x)
        distance_y = abs(player_y - self.y)
        
        # Debug détaillé pour voir les distances
        
        collision = distance_x <= 20 and distance_y <= 20
        
        return collision
    
    def consume(self):
        """
        Consomme le powerup (le désactive et efface son sprite)
        
        Returns:
            float: Timestamp de consommation
        """
        if self.is_active:
            self.is_active = False
            efface(self.tag)
            return time()
        return None


class PowerupManager:
    """Gestionnaire centralisé pour tous les powerups du jeu"""
    
    def __init__(self):
        """Initialise le gestionnaire de powerups"""
        self.powerups = {}
        self.invincibility_timers = {}  # {player_id: start_time}
        self.invincibility_duration = 3.0  # Durée d'invincibilité en secondes
    
    def add_powerup(self, powerup):
        """
        Ajoute un powerup au gestionnaire
        
        Args:
            powerup (Powerup): Instance de powerup à ajouter
        """ 
        self.powerups[powerup.powerup_id] = powerup
    
    def check_player_collisions(self, player):
        """
        Vérifie les collisions entre un joueur et tous les powerups actifs
        
        Args:
            player (Player): Instance du joueur à vérifier
            
        Returns:
            int or None: ID du powerup collecté, None si aucune collision
        """
        player_pos = player.get_position()
        
        for powerup_id, powerup in self.powerups.items():
            if powerup.check_collision(player_pos[0], player_pos[1]):
                consumption_time = powerup.consume()
                if consumption_time:
                    self._activate_invincibility(player.player_id, consumption_time)
                    return powerup_id
        return None
    
    def _activate_invincibility(self, player_id, start_time):
        """
        Active l'invincibilité pour un joueur
        
        Args:
            player_id (int): ID du joueur
            start_time (float): Timestamp de début d'invincibilité
        """
        self.invincibility_timers[player_id] = start_time
    
    def is_player_invincible(self, player_id):
        """
        Vérifie si un joueur est invincible
        
        Args:
            player_id (int): ID du joueur à vérifier
            
        Returns:
            bool: True si le joueur est invincible
        """
        if player_id not in self.invincibility_timers:
            return False
        
        elapsed_time = time() - self.invincibility_timers[player_id]
        if elapsed_time >= self.invincibility_duration:
            # Invincibilité expirée
            del self.invincibility_timers[player_id]
            return False
        
        return True
    
    def update_invincibility_display(self, player_id, mode_deux=False):
        """
        Met à jour l'affichage de l'invincibilité pour un joueur
        
        Args:
            player_id (int): ID du joueur
            mode_deux (bool): True si mode 2 joueurs
        """
        from fltk import texte, efface
        
        tag = f"Invincibilite{player_id}"
        
        if self.is_player_invincible(player_id):
            # Positions selon le mode et le joueur
            if mode_deux:
                positions = {
                    1: (680, 400),
                    2: (680, 710)
                }
            else:
                positions = {1: (50, 170)}
            
            if player_id in positions:
                x, y = positions[player_id]
                texte(
                    x, y, "Invincibilite",
                    couleur="yellow", taille=16,
                    police="Copperplate Gothic Bold",
                    tag=tag
                )
        else:
            efface(tag)
