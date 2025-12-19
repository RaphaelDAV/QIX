"""
Module Sparks - Gestion des ennemis Sparks qui se déplacent sur les bordures
"""
from fltk import image, efface
import sys
from config.constants import GRILLE_PAS


class Sparks:
    """Classe représentant un ennemi Sparks qui se déplace le long des bordures"""
    __slots__ = (
        "x",
        "y",
        "taille",
        "sparks_id",
        "tag",
        "vitesse",
        "deplacement",
        "sprite",
        "sprite_invincible",
        "historique",
        "compteur",
    )
    def __init__(self, x, y, taille, sparks_id, vitesse, deplacement, 
                 sprite="ressources/Fantome1.png", direction_initiale="Gauche"):
        """
        Initialise un Sparks
        
        Args:
            x (int): Position x initiale
            y (int): Position y initiale
            taille (int): Taille du sprite
            sparks_id (int): Identifiant du sparks (1-6)
            vitesse (int): Vitesse de déplacement (nombre de frames entre chaque mouvement)
            deplacement (int): Distance de déplacement à chaque mouvement
            sprite (str): Chemin vers le sprite du sparks
            direction_initiale (str): Direction de départ
        """
        self.x = x
        self.y = y
        self.taille = taille
        self.sparks_id = sparks_id
        self.tag = f"sparks{sparks_id}"
        self.vitesse = vitesse
        self.deplacement = deplacement
        self.sprite = sprite
        self.sprite_invincible = "ressources/Fantome_fruit.png"
        self.historique = [direction_initiale]
        self.compteur = 0
        
    def draw(self, player_invincible=False):
        """
        Dessine le Sparks à sa position actuelle
        
        Args:
            player_invincible (bool): Si True, le joueur est invincible donc on affiche
                                      le sprite "vulnérable" (fruit) pour les Sparks
        """
        sprite_actuel = self.sprite_invincible if player_invincible else self.sprite
        image(
            self.x,
            self.y,
            sprite_actuel,
            largeur=self.taille + GRILLE_PAS,
            hauteur=self.taille + GRILLE_PAS,
            tag=self.tag
        )
    
    def move(self, zone_safe, player_invincible=False):
        """
        Déplace le Sparks le long de la zone safe
        
        Args:
            zone_safe (list): Liste des positions sur les bordures
            player_invincible (bool): Si True, le joueur est invincible donc on affiche
                                      le sprite "vulnérable" pour les Sparks
            
        Returns:
            bool: True si le Sparks s'est déplacé, False sinon
        """
        self.compteur += 1

        # Ne bouge que tous les X frames selon la vitesse
        if self.compteur % self.vitesse != 0:
            return False

        dx = 0
        dy = 0

        # Déterminer le prochain mouvement en suivant les bordures
        # Le sens de rotation dépend de la direction initiale configurée
        direction_preference = self.historique[0] if self.historique else "Gauche"
        last_dir = self.historique[-1] if self.historique else direction_preference

        # Prepare fast membership: accept set or convert when large
        zone_safe_set = zone_safe if isinstance(zone_safe, set) else None
        try:
            zone_len = len(zone_safe)
        except Exception:
            zone_len = 0
        if zone_safe_set is None and zone_len > 50:
            zone_safe_set = set((p[0], p[1]) for p in zone_safe)

        def contains(px, py):
            if zone_safe_set is not None:
                return (px, py) in zone_safe_set
            return [px, py] in zone_safe

        # Si direction preference est "Droite", on privilégie de tourner vers la droite (sens anti-horaire)
        # Si direction preference est "Gauche", on privilégie de tourner vers la gauche (sens horaire)
        if direction_preference == "Droite":
            # Sens anti-horaire : Droite -> Haut -> Gauche -> Bas
            if contains(self.x + GRILLE_PAS, self.y) and last_dir != "Gauche":
                dx = self.deplacement
                self.historique.append("Droite")
            elif contains(self.x, self.y - GRILLE_PAS) and last_dir != "Bas":
                dy = -self.deplacement
                self.historique.append("Haut")
            elif contains(self.x - GRILLE_PAS, self.y) and last_dir != "Droite":
                dx = -self.deplacement
                self.historique.append("Gauche")
            elif contains(self.x, self.y + GRILLE_PAS) and last_dir != "Haut":
                dy = self.deplacement
                self.historique.append("Bas")
        else:  # direction_preference == "Gauche"
            # Sens horaire : Gauche -> Haut -> Droite -> Bas
            if contains(self.x - GRILLE_PAS, self.y) and last_dir != "Droite":
                dx = -self.deplacement
                self.historique.append("Gauche")
            elif contains(self.x, self.y - GRILLE_PAS) and last_dir != "Bas":
                dy = -self.deplacement
                self.historique.append("Haut")
            elif contains(self.x + GRILLE_PAS, self.y) and last_dir != "Gauche":
                dx = self.deplacement
                self.historique.append("Droite")
            elif contains(self.x, self.y + GRILLE_PAS) and last_dir != "Haut":
                dy = self.deplacement
                self.historique.append("Bas")
        
        # Déplacer le Sparks si possible
        if dx != 0 or dy != 0:
            efface(self.tag)
            self.x += dx
            self.y += dy
            self.draw(player_invincible)
            return True
        
        return False
    
    def get_position(self):
        """
        Retourne la position actuelle du Sparks
        
        Returns:
            list: [x, y]
        """
        return [self.x, self.y]
    
    def collides_with(self, player_pos):
        """
        Vérifie si le Sparks est en collision avec une position
        
        Args:
            player_pos (list): Position du joueur [x, y]
            
        Returns:
            bool: True s'il y a collision
        """
        # Accept both list and tuple for player_pos
        return (self.x, self.y) == tuple(player_pos)
    
    def teleport_to(self, other_sparks):
        """
        Téléporte ce Sparks à la position d'un autre Sparks
        
        Args:
            other_sparks (Sparks): L'autre Sparks vers lequel se téléporter
        """
        self.historique.clear()
        
        # Inverser la direction de l'autre Sparks
        inverse_direction = {
            "Haut": "Bas",
            "Bas": "Haut",
            "Gauche": "Droite",
            "Droite": "Gauche"
        }
        
        derniere_direction = other_sparks.historique[-1]
        self.historique.append(inverse_direction.get(derniere_direction, "Gauche"))
        
        self.x = other_sparks.x
        self.y = other_sparks.y
    
    def is_out_of_bounds(self, zone_safe):
        """
        Vérifie si le Sparks est sorti de la zone safe
        
        Args:
            zone_safe (list): Liste des positions valides sur les bordures
            
        Returns:
            bool: True si le Sparks est hors de la zone safe
        """
        if isinstance(zone_safe, set):
            return (self.x, self.y) not in zone_safe
        try:
            zone_len = len(zone_safe)
        except Exception:
            zone_len = 0
        if zone_len > 50:
            zone_safe_set = set((p[0], p[1]) for p in zone_safe)
            return (self.x, self.y) not in zone_safe_set
        return [self.x, self.y] not in zone_safe
    
    def reset_position(self, x, y, direction="Gauche"):
        """
        Réinitialise la position du Sparks
        
        Args:
            x (int): Nouvelle position x
            y (int): Nouvelle position y
            direction (str): Nouvelle direction initiale
        """
        efface(self.tag)
        self.x = x
        self.y = y
        self.historique.clear()
        self.historique.append(direction)
        self.draw()


class SparksManager:
    """Gestionnaire pour gérer plusieurs Sparks ensemble"""
    
    def __init__(self):
        """Initialise le gestionnaire de Sparks"""
        self.sparks_list = []
        self.temps_sparks = 0
        self.mode_menu = False
        self.jeu_commence = True  # Le jeu commence immédiatement par défaut
    
    def add_sparks(self, sparks):
        """
        Ajoute un Sparks à la liste
        
        Args:
            sparks (Sparks): Instance de Sparks à ajouter
        """
        self.sparks_list.append(sparks)
    
    def move_all(self, zone_safe, vitesse, player_invincible=False):
        """
        Déplace tous les Sparks
        
        Args:
            zone_safe (list): Zone safe actuelle
            vitesse (int): Vitesse de déplacement
            player_invincible (bool): Si True, le joueur est invincible, les Sparks
                                      affichent leur sprite "vulnérable"
        """
        # Les sparks ne bougent que si le jeu a commencé (après le clic)
        if not self.jeu_commence:
            return  # Pas de mouvement avant le clic

        # Prepare a set for zone_safe once when large to avoid repeated conversions
        zone_safe_set = zone_safe if isinstance(zone_safe, set) else None
        try:
            zone_len = len(zone_safe)
        except Exception:
            zone_len = 0
        if zone_safe_set is None and zone_len > 50:
            zone_safe_set = set((p[0], p[1]) for p in zone_safe)

        if self.temps_sparks % vitesse == 0:
            for sparks in self.sparks_list:
                # pass set when available; Sparks.move accepts either
                sparks.move(zone_safe_set if zone_safe_set is not None else zone_safe, player_invincible)

        self.temps_sparks += 1
    
    def commencer_jeu(self):
        """
        Démarre le jeu (les sparks arrêtent de tourner et commencent à avancer)
        """
        self.jeu_commence = True
    
    def check_out_of_bounds(self, zone_safe):
        """
        Vérifie et téléporte les Sparks qui sont sortis de la zone safe
        
        Args:
            zone_safe (list): Zone safe actuelle
        """
        # Pré-calculer une version en `set` de `zone_safe` si la zone est grande
        zone_safe_set = zone_safe if isinstance(zone_safe, set) else None
        try:
            zone_len = len(zone_safe)
        except Exception:
            zone_len = 0
        if zone_safe_set is None and zone_len > 50:
            zone_safe_set = set((p[0], p[1]) for p in zone_safe)

        for i, sparks in enumerate(self.sparks_list):
            # Passer la version set si disponible pour éviter des reconversions coûteuses
            check_zone = zone_safe_set if zone_safe_set is not None else zone_safe
            if sparks.is_out_of_bounds(check_zone):
                # En mode menu avec 2 sparks, ils se téléportent l'un vers l'autre
                if self.mode_menu and len(self.sparks_list) == 2:
                    other_index = 1 - i  # Avec 2 sparks : 0->1, 1->0
                    sparks.teleport_to(self.sparks_list[other_index])
                else:
                    # Téléporter vers un autre Sparks
                    other_index = (i + 1) % len(self.sparks_list)
                    if other_index != i:
                        sparks.teleport_to(self.sparks_list[other_index])
    
    def check_collision_with_player(self, player_pos, player_invincible=False):
        """
        Vérifie si un Sparks touche le joueur
        
        Args:
            player_pos (list): Position du joueur [x, y]
            player_invincible (bool): Si True, le joueur est invincible donc pas de collision
            
        Returns:
            Sparks or None: Le Sparks en collision, ou None (si joueur invincible)
        """
        if player_invincible:
            return None
        
        for sparks in self.sparks_list:
            if sparks.collides_with(player_pos):
                return sparks
        
        return None
    
    def teleport_sparks_to_pair(self, sparks_to_teleport):
        """
        Téléporte un Sparks vers sa paire
        
        Args:
            sparks_to_teleport (Sparks): Le Sparks à téléporter
        """
        try:
            sparks_index = self.sparks_list.index(sparks_to_teleport)
            
            # Logique de paire selon le nombre de Sparks
            if len(self.sparks_list) == 2:
                # Avec 2 Sparks : 0<->1
                pair_index = 1 - sparks_index
            elif len(self.sparks_list) == 4:
                # Avec 4 Sparks : 0<->1, 2<->3
                pair_index = sparks_index + 1 if sparks_index % 2 == 0 else sparks_index - 1
            elif len(self.sparks_list) == 6:
                # Avec 6 Sparks : 0<->1, 2<->3, 4<->5
                pair_index = sparks_index + 1 if sparks_index % 2 == 0 else sparks_index - 1
            else:
                # Cas par défaut : téléporter vers le Sparks suivant
                pair_index = (sparks_index + 1) % len(self.sparks_list)
            
            if 0 <= pair_index < len(self.sparks_list) and pair_index != sparks_index:
                sparks_to_teleport.teleport_to(self.sparks_list[pair_index])
        
        except (ValueError, IndexError):
            # En cas d'erreur, ne rien faire
            pass

    def get_all_positions(self):
        """Retourne toutes les positions des Sparks"""
        positions = []
        for sparks in self.sparks_list:
            positions.append(sparks.get_position())
        return positions
