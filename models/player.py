"""Module Player - Gestion du joueur dans le jeu QIX"""
from fltk import image, efface
from config.constants import (
    VIES_INITIALES, 
    VITESSE_TRACAGE_LENTE, 
    VITESSE_TRACAGE_RAPIDE,
    GRILLE_PAS
)


class Player:
    """Classe représentant un joueur dans le jeu QIX"""
    
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
        
    def draw(self, direction=None):
        """Dessine le joueur à sa position actuelle"""
        if direction:
            self.direction = direction
            
        sprite_map = {
            "haut": f"ressources/{self.sprite_base}_haut.png",
            "bas": f"ressources/{self.sprite_base}_bas.png",
            "gauche": f"ressources/{self.sprite_base}_gauche.png",
            "droite": f"ressources/{self.sprite_base}_droite.png"
        }
        
        sprite = sprite_map.get(self.direction, sprite_map["haut"])
        
        image(
            self.x, self.y, sprite, 
            largeur=self.taille + GRILLE_PAS, 
            hauteur=self.taille + GRILLE_PAS, 
            tag=self.tag
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
        
        if self.player_id == 1:
            controls = {
                "Left": (-vitesse_deplacement, 0, "gauche"),
                "Right": (vitesse_deplacement, 0, "droite"),
                "Down": (0, vitesse_deplacement, "bas"),
                "Up": (0, -vitesse_deplacement, "haut")
            }
        else:
            controls = {
                "q": (-vitesse_deplacement, 0, "gauche"),
                "d": (vitesse_deplacement, 0, "droite"),
                "s": (0, vitesse_deplacement, "bas"),
                "z": (0, -vitesse_deplacement, "haut")
            }
        
        for key, (vel_x, vel_y, direction) in controls.items():
            if input_handler(key):
                new_x = self.x + (GRILLE_PAS if vel_x > 0 else -GRILLE_PAS if vel_x < 0 else 0)
                new_y = self.y + (GRILLE_PAS if vel_y > 0 else -GRILLE_PAS if vel_y < 0 else 0)
                
                if [new_x, new_y] in zone_safe:
                    dx, dy = vel_x, vel_y
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
        
        if input_handler(space_key) and any(input_handler(key) for key in controls.keys()):
            
            if self.iteration == 0:
                self.historique_positions.append([self.x, self.y])
                self.iteration += 1
            
            for key, (vel_x, vel_y, direction) in controls.items():
                if input_handler(key):
                    step = GRILLE_PAS * (int(vitesse_tracage / GRILLE_PAS))
                    new_x = self.x + (step if vel_x > 0 else -step if vel_x < 0 else 0)
                    new_y = self.y + (step if vel_y > 0 else -step if vel_y < 0 else 0)
                    
                    check_pos = [new_x, new_y]
                    if (check_pos in zone_terrain and 
                        check_pos not in zone_polygone and 
                        check_pos not in zone_obstacle):
                        dx, dy = vel_x, vel_y
                        
                        from fltk import ligne
                        if direction == "Haut":
                            ligne(self.x, self.y - step, self.x, self.y, "white", 2, tag=f"trait_joueur{self.player_id if self.player_id != 1 else ''}")
                        else:
                            ligne(self.x, self.y, new_x, new_y, "white", 2, tag=f"trait_joueur{self.player_id if self.player_id != 1 else ''}")
                        
                        self.historique_virage.append([direction, [self.x, self.y]])
                        self.historique_deplacement.append(direction)
                        
                        if (len(self.historique_virage) >= 2 and 
                            self.historique_virage[-1][0] != self.historique_virage[-2][0]):
                            self.historique_positions.append([self.x, self.y])
                        
                        break
            
            if [self.x, self.y] not in self.trait_joueur_actuel:
                self.trait_joueur_actuel.append([self.x, self.y])
        
        return dx, dy
    
    def handle_speed_change(self, touche_pressee, zone_safe, vitesse_enabled=True):
        """Gère le changement de vitesse de traçage du joueur"""
        from fltk import texte, efface
        import time
        
        if not vitesse_enabled:
            return False
            
        current_time = time.time()
        if current_time - self.last_speed_change < 1.0:
            return False
            
        if touche_pressee(self.touche_vitesse) and [self.x, self.y] in zone_safe:
            self.last_speed_change = current_time
            self.touche_vitesse = None
            
            speed_tag = f"vitesse{self.player_id if self.player_id > 1 else ''}"
            efface(speed_tag)
            
            display_positions = {1: 475, 2: 600}
            x_pos = display_positions.get(self.player_id, 475)
            
            if self.vitesse_tracage == 5:
                self.vitesse_tracage = 10
                texte(x_pos, 170, "Rapide", couleur="red", taille=15,
                      police="Copperplate Gothic Bold", tag=speed_tag)
            elif self.vitesse_tracage == 10:
                self.vitesse_tracage = 5
                texte(x_pos, 170, "Lente", couleur="green", taille=15,
                      police="Copperplate Gothic Bold", tag=speed_tag)
            
            self.touche_vitesse = "v"
            return True
            
        return False
