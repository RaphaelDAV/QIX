"""Module Player - Gestion du joueur dans le jeu QIX"""
from fltk import image, efface, texte, ligne
import time
from config.constants import (
    VIES_INITIALES,
    VITESSE_TRACAGE_LENTE,
    VITESSE_TRACAGE_RAPIDE,
    GRILLE_PAS,
    TERRAIN_X_MIN,
    TERRAIN_X_MAX,
    TERRAIN_Y_MIN,
    TERRAIN_Y_MAX,
)


class Player:
    """Classe représentant un joueur dans le jeu QIX"""
    __slots__ = (
        "x",
        "y",
        "taille",
        "player_id",
        "sprite_base",
        "tag",
        "direction",
        "vie",
        "invincible",
        "vitesse_tracage",
        "touche_vitesse",
        "last_speed_change",
        "historique_positions",
        "trait_joueur_actuel",
        "historique_deplacement",
        "historique_virage",
        "iteration",
        "_sprite_paths",
        "_controls_move",
        "_controls_trace",
        "_directions_opposees",
    )
    def __init__(self, x, y, taille, player_id=1, sprite_base="Pacman1"):
        self.x = x
        self.y = y
        self.taille = taille
        self.player_id = player_id
        self.sprite_base = sprite_base
        self.tag = f"joueur{player_id}"
        self.direction = "haut"
        self.vie = VIES_INITIALES
        self.invincible = False
        
        # Gestion vitesse
        self.vitesse_tracage = VITESSE_TRACAGE_LENTE
        self.touche_vitesse = "v" if player_id == 1 else "v"
        self.last_speed_change = 0
        
        # Historiques traçage
        self.historique_positions = []
        self.trait_joueur_actuel = []
        self.historique_deplacement = []
        self.historique_virage = []
        self.iteration = 0
        # Precompute frequently used mappings to avoid rebuilding inside loops
        base = f"ressources/{self.sprite_base}_{{}}.png"
        self._sprite_paths = {
            "haut": base.format("haut"),
            "bas": base.format("bas"),
            "gauche": base.format("gauche"),
            "droite": base.format("droite"),
        }

        # Controls caches for move and tracing to avoid rebuilding dicts each frame
        if self.player_id == 1:
            self._controls_move = {
                "Left": (-1, 0, "gauche"),
                "Right": (1, 0, "droite"),
                "Down": (0, 1, "bas"),
                "Up": (0, -1, "haut"),
            }
            self._controls_trace = {
                "Left": (-1, 0, "Gauche"),
                "Right": (1, 0, "Droite"),
                "Down": (0, 1, "Bas"),
                "Up": (0, -1, "Haut"),
            }
        else:
            self._controls_move = {
                "q": (-1, 0, "gauche"),
                "d": (1, 0, "droite"),
                "s": (0, 1, "bas"),
                "z": (0, -1, "haut"),
            }
            self._controls_trace = {
                "q": (-1, 0, "Gauche"),
                "d": (1, 0, "Droite"),
                "s": (0, 1, "Bas"),
                "z": (0, -1, "Haut"),
            }

        self._directions_opposees = {
            "Gauche": "Droite",
            "Droite": "Gauche",
            "Haut": "Bas",
            "Bas": "Haut",
        }
        
    def draw(self, direction=None):
        """Dessine le joueur à sa position actuelle"""
        if direction:
            self.direction = direction
        sprite = self._sprite_paths.get(self.direction, self._sprite_paths["haut"])

        image(
            self.x,
            self.y,
            sprite,
            largeur=self.taille + GRILLE_PAS,
            hauteur=self.taille + GRILLE_PAS,
            tag=self.tag,
        )
    
    def move(self, dx, dy):
        """Déplace le joueur et retourne True si mouvement effectué"""
        if dx != 0 or dy != 0:
            efface(self.tag)
            self.x += dx
            self.y += dy
            
            if dx < 0:
                self.direction = "gauche"
            elif dx > 0:
                self.direction = "droite"
            elif dy < 0:
                self.direction = "haut"
            elif dy > 0:
                self.direction = "bas"
            
            self.draw()
            return True
        return False
    
    def get_position(self):
        """Retourne la position actuelle [x, y]"""
        return [self.x, self.y]
    
    def is_in_zone(self, zone):
        """Vérifie si le joueur est dans une zone donnée"""
        # zone may be a name (str) or a list of [x,y]
        if isinstance(zone, str):
            try:
                from core.game_state import game_state
                z = game_state.get_zone(zone)
            except Exception:
                return False
            return [self.x, self.y] in z
        return [self.x, self.y] in zone
    
    def lose_life(self):
        """Fait perdre une vie au joueur"""
        self.vie -= 1
        return self.vie
    
    def set_invincible(self, invincible):
        """Active ou désactive l'invincibilité"""
        self.invincible = invincible
    
    def reset_position(self, x, y):
        """Réinitialise la position du joueur"""
        efface(self.tag)
        self.x = x
        self.y = y
        self.draw()
    
    def handle_input(self, input_handler, zone_safe, vitesse_deplacement):
        """Gère les entrées du joueur et calcule le déplacement"""
        dx, dy = 0, 0

        for key, (dir_x, dir_y, direction) in self._controls_move.items():
            if input_handler(key):
                step_x = GRILLE_PAS if dir_x > 0 else -GRILLE_PAS if dir_x < 0 else 0
                step_y = GRILLE_PAS if dir_y > 0 else -GRILLE_PAS if dir_y < 0 else 0
                new_x = self.x + step_x
                new_y = self.y + step_y

                # simple list membership test against provided zone_safe
                if [new_x, new_y] in zone_safe:
                    dx, dy = step_x, step_y
                    self.direction = direction
                break

        return dx, dy
    
    def handle_tracing(self, input_handler, space_key, vitesse_tracage, zone_terrain, zone_polygone, zone_obstacle):
        """Gère le traçage de formes quand la touche espace est maintenue"""
        dx, dy = 0, 0
        
        if self.player_id == 1:
            controls = {
                "Left": (-vitesse_tracage, 0, "Gauche"),
                "Right": (vitesse_tracage, 0, "Droite"),
                "Down": (0, vitesse_tracage, "Bas"),
                "Up": (0, -vitesse_tracage, "Haut")
            }
        else:
            controls = {
                "q": (-vitesse_tracage, 0, "Gauche"),
                "d": (vitesse_tracage, 0, "Droite"),
                "s": (0, vitesse_tracage, "Bas"),
                "z": (0, -vitesse_tracage, "Haut")
            }
        
        # Définition des directions opposées pour empêcher le demi-tour
        directions_opposees = {
            "Gauche": "Droite",
            "Droite": "Gauche", 
            "Haut": "Bas",
            "Bas": "Haut"
        }
        
        if input_handler(space_key) and any(input_handler(k) for k in self._controls_trace.keys()):

            if self.iteration == 0:
                self.historique_positions.append([self.x, self.y])
                self.iteration += 1

            step = GRILLE_PAS * (int(vitesse_tracage / GRILLE_PAS))

            for key, (dir_x, dir_y, direction) in self._controls_trace.items():
                if input_handler(key):
                    # Anti demi-tour
                    if (
                        self.historique_deplacement
                        and self.historique_deplacement[-1] in self._directions_opposees
                        and direction == self._directions_opposees[self.historique_deplacement[-1]]
                    ):
                        continue

                    proposed_x = self.x + (step if dir_x > 0 else -step if dir_x < 0 else 0)
                    proposed_y = self.y + (step if dir_y > 0 else -step if dir_y < 0 else 0)

                    new_x = proposed_x
                    new_y = proposed_y

                    # Clamp to terrain bounds
                    if dir_x > 0 and proposed_x > TERRAIN_X_MAX:
                        new_x = TERRAIN_X_MAX
                    elif dir_x < 0 and proposed_x < TERRAIN_X_MIN:
                        new_x = TERRAIN_X_MIN

                    if dir_y > 0 and proposed_y > TERRAIN_Y_MAX:
                        new_y = TERRAIN_Y_MAX
                    elif dir_y < 0 and proposed_y < TERRAIN_Y_MIN:
                        new_y = TERRAIN_Y_MIN

                    check_pos = [new_x, new_y]
                    # membership checks against passed-in zone lists
                    from core.game_state import game_state
                    if (
                        check_pos in zone_terrain
                        and check_pos not in zone_polygone
                        and not game_state.is_point_in_obstacle(new_x, new_y)
                        and check_pos not in self.trait_joueur_actuel
                    ):
                        dx, dy = dir_x * vitesse_tracage, dir_y * vitesse_tracage

                        tag = f"trait_joueur{self.player_id if self.player_id != 1 else ''}"
                        if direction == "Haut":
                            ligne(self.x, self.y - step, self.x, self.y, "white", 2, tag=tag)
                        else:
                            ligne(self.x, self.y, new_x, new_y, "white", 2, tag=tag)

                        self.historique_virage.append([direction, [self.x, self.y]])
                        self.historique_deplacement.append(direction)

                        if (
                            len(self.historique_virage) >= 2
                            and self.historique_virage[-1][0] != self.historique_virage[-2][0]
                        ):
                            self.historique_positions.append([self.x, self.y])

                        break

            if [self.x, self.y] not in self.trait_joueur_actuel:
                self.trait_joueur_actuel.append([self.x, self.y])
        
        return dx, dy
    
    def handle_speed_change(self, touche_pressee, zone_safe, vitesse_enabled=True):
        """Gère le changement de vitesse de traçage du joueur"""
        if not vitesse_enabled:
            return False

        current_time = time.time()
        if current_time - self.last_speed_change < 1.0:
            return False

        if touche_pressee(self.touche_vitesse) and [self.x, self.y] in zone_safe:
            self.last_speed_change = current_time

            speed_tag = f"vitesse{self.player_id if self.player_id > 1 else ''}"
            efface(speed_tag)

            display_positions = {1: 475, 2: 600}
            x_pos = display_positions.get(self.player_id, 475)

            if self.vitesse_tracage == 5:
                self.vitesse_tracage = 10
                texte(
                    x_pos,
                    170,
                    "Rapide",
                    couleur="red",
                    taille=15,
                    police="Copperplate Gothic Bold",
                    tag=speed_tag,
                )
            elif self.vitesse_tracage == 10:
                self.vitesse_tracage = 5
                texte(
                    x_pos,
                    170,
                    "Lente",
                    couleur="green",
                    taille=15,
                    police="Copperplate Gothic Bold",
                    tag=speed_tag,
                )

            return True

        return False
