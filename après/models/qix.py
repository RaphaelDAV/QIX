"""
Module Qix - Gestion de l'ennemi principal Qix
"""
from fltk import image, efface
from config.constants import GRILLE_PAS


class Qix:
    """Classe représentant l'ennemi Qix qui se déplace dans le terrain"""
    __slots__ = (
        "x",
        "y",
        "vitesse",
        "longueur_deplacement",
        "sprite",
        "tag",
        "compteur",
        "direction_actuelle",
        "distance_parcourue",
    )
    def __init__(self, x, y, vitesse, longueur_deplacement=6, sprite="ressources/Fantome_qix.png"):
        """Initialise le Qix"""
        self.x = x
        self.y = y
        self.vitesse = vitesse
        self.longueur_deplacement = longueur_deplacement
        self.sprite = sprite
        self.tag = "Fantome_QIX"
        self.compteur = 0
        self.direction_actuelle = None
        self.distance_parcourue = 0
        
    def reset_position(self, x, y):
        """Réinitialise la position du Qix"""
        efface(self.tag)
        self.x = x
        self.y = y
        self.direction_actuelle = None
        self.distance_parcourue = 0
