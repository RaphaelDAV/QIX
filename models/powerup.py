"""
Module Powerup - Gestion des bonus et powerups dans le jeu QIX
"""
from fltk import efface, texte
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
        self.sprite_path = sprite_path
        self.effect_duration = effect_duration
    
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
            
        # Use squared-distance check for small performance win
        if not self.is_active:
            return False

        dx = player_x - self.x
        dy = player_y - self.y
        # collision radius 20 -> squared radius 400
        return (dx * dx + dy * dy) <= 400
    
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
        # invincibility_timers holds end timestamps: {player_id: end_time}
        self.invincibility_timers = {}
        self.default_invincibility_duration = 3.0
    
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

        # iterate over a snapshot of items to allow removal
        for powerup_id, powerup in list(self.powerups.items()):
            if not powerup.is_active:
                # Clean up inactive powerups to keep dict small
                del self.powerups[powerup_id]
                continue

            if powerup.check_collision(player_pos[0], player_pos[1]):
                consumption_time = powerup.consume()
                if consumption_time:
                    # Remove the consumed powerup from manager
                    if powerup_id in self.powerups:
                        del self.powerups[powerup_id]
                    # Activate invincibility using powerup-specific duration
                    duration = getattr(powerup, "effect_duration", self.default_invincibility_duration)
                    self._activate_invincibility(player.player_id, consumption_time, duration)
                    return powerup_id

        return None
    
    def _activate_invincibility(self, player_id, start_time, duration=None):
        """
        Active l'invincibilité pour un joueur
        
        Args:
            player_id (int): ID du joueur
            start_time (float): Timestamp de début d'invincibilité
        """
        if duration is None:
            duration = self.default_invincibility_duration
        # store end timestamp for simpler checks later
        self.invincibility_timers[player_id] = start_time + duration
    
    def is_player_invincible(self, player_id):
        """
        Vérifie si un joueur est invincible
        
        Args:
            player_id (int): ID du joueur à vérifier
            
        Returns:
            bool: True si le joueur est invincible
        """
        end_time = self.invincibility_timers.get(player_id)
        if end_time is None:
            return False

        if time() >= end_time:
            # expired
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
        tag = f"Invincibilite{player_id}"

        inv = self.is_player_invincible(player_id)
        if not inv:
            efface(tag)
            return

        # Positions for display
        if mode_deux:
            positions = {1: (680, 400), 2: (680, 710)}
        else:
            positions = {1: (50, 170)}

        pos = positions.get(player_id)
        if not pos:
            return

        x, y = pos
        efface(tag)
        texte(x, y, "Invincibilite", couleur="yellow", taille=16,
              police="Copperplate Gothic Bold", tag=tag)
