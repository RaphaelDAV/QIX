"""
Constantes du jeu QIX
"""

# ------------------ Fenêtre ------------------
FENETRE_LARGEUR_BASE = 600
FENETRE_HAUTEUR_BASE = 800
FENETRE_LARGEUR_DEUX_JOUEURS = 900

# Configuration de fenêtre (remplace parametres.txt)
FENETRE_CONFIG = {
    "largeur": 600,
    "hauteur": 800,
    "aire_x": 50,
    "aire_y": 200, 
    "aire_xb": 550,
    "aire_yb": 750
}

# ------------------ Zones de jeu ------------------
TERRAIN_X_MIN = 50
TERRAIN_Y_MIN = 200
TERRAIN_X_MAX = 550
TERRAIN_Y_MAX = 750

# ------------------ Gameplay ------------------
VITESSE_DEPLACEMENT_BASE = 5
VITESSE_TRACAGE_LENTE = 5
VITESSE_TRACAGE_RAPIDE = 10

VIES_INITIALES = 3
SURFACE_VICTOIRE = 75  # Pourcentage de surface à conquérir

TEMPS_INVINCIBILITE = 3  # Secondes d'invincibilité après bonus

# ------------------ Score ------------------
SCORE_MAX = 20000
MULTIPLICATEUR_VITESSE_LENTE = 1.0
MULTIPLICATEUR_VITESSE_RAPIDE = 0.5

# ------------------ Sprites ------------------
SPRITES_JOUEUR1 = {
    "haut": "ressources/Pacman1_haut.png",
    "bas": "ressources/Pacman1_bas.png",
    "gauche": "ressources/Pacman1_gauche.png",
    "droite": "ressources/Pacman1_droite.png"
}

SPRITES_JOUEUR2 = {
    "haut": "ressources/Pacman2_haut.png",
    "bas": "ressources/Pacman2_bas.png",
    "gauche": "ressources/Pacman2_gauche.png",
    "droite": "ressources/Pacman2_droite.png"
}

SPRITES_SPARKS = [
    "ressources/Fantome1.png",
    "ressources/Fantome2.png",
    "ressources/Fantome3.png",
    "ressources/Fantome4.png",
    "ressources/Fantome5.png"
]

SPRITE_QIX = "ressources/Fantome_qix.png"
SPRITE_SPARKS_VULNERABLE = "ressources/Fantome_fruit.png"

SPRITES_FRUITS = [
    "ressources/Fruit1.png",
    "ressources/Fruit2.png",
    "ressources/Fruit3.png",
    "ressources/Fruit4.png",
    "ressources/Fruit5.png"
]

# ------------------ Couleurs ------------------
COULEURS_POLYGONES = [
    "red", "green", "blue", "cyan", "magenta", "yellow", "brown", "orange",
    "pink", "purple", "burlywood", "cadetblue", "chartreuse", "chocolate",
    "coral", "cornflowerblue", "cornsilk", "darkorange", "darkseagreen",
    "darkturquoise", "deepskyblue", "dodgerblue", "goldenrod", "hotpink",
    "khaki", "lightcoral", "lightpink", "lightsalmon", "lightseagreen"
]

# ------------------ Contrôles ------------------
TOUCHES_JOUEUR1 = {
    "haut": "Up",
    "bas": "Down", 
    "gauche": "Left",
    "droite": "Right",
    "trace": "space",
    "vitesse": "v"
}

TOUCHES_JOUEUR2 = {
    "haut": "z",
    "bas": "s",
    "gauche": "q", 
    "droite": "d",
    "trace": "m",
    "vitesse": "v"
}

# ------------------ Directions par défaut des Sparks ------------------
DIRECTIONS_SPARKS_DEFAUT = {
    "sparks1": ["Droite"],    # Paire 1 : va vers la droite
    "sparks2": ["Gauche"],    # Paire 1 : va vers la gauche (opposé)
    "sparks3": ["Droite"],    # Paire 2 : va vers la droite
    "sparks4": ["Gauche"],    # Paire 2 : va vers la gauche (opposé)
    "sparks5": ["Droite"],    # Paire 3 : va vers la droite
    "sparks6": ["Gauche"]     # Paire 3 : va vers la gauche (opposé)
}

# ------------------ Zones de terrain ------------------
ZONE_COIN_DEFAUT = [[50, 200], [550, 200], [550, 750], [50, 750]]

# Pas de déplacement pour la grille
GRILLE_PAS = 5

# ------------------ Messages ------------------
MESSAGES = {
    "victoire": "GAGNÉ",
    "victoire_joueur1": "JOUEUR 1 À GAGNÉ", 
    "victoire_joueur2": "JOUEUR 2 À GAGNÉ",
    "game_over": "GAME OVER",
    "surface_conquise": "Surface conquise:",
    "votre_score": "Votre score:",
    "score_joueur1": "Score joueur 1:",
    "score_joueur2": "Score joueur 2:",
    "invincibilite": "Invincibilite",
    "commencer": "CLIQUEZ POUR COMMENCER",
    "quitter": "Appuyez sur ECHAP pour quitter"
}

# ------------------ Variables de jeu globales ------------------
# Valeurs par défaut pour variables de jeu
DEFAULT_GAME_STATE = {
    "scorev": False,
    "vitesse": False, 
    "obstacle": False,
    "bonus": False,
    "deux": False,
    "niveau": False,
    "start": False,
    "obstacle_aleatoire": False,
    "obstacle_predefini": False,
    "niveau1": False,
    "niveau2": False, 
    "niveau3": False,
    "bonus_aleatoire": False,
    "bonus_predefini": False
}

# Variables de contrôle par défaut
DEFAULT_CONTROLS = {
    "touche_V": "v",
    "touche_V2": "v",
    "touche_espace": "space",
    "touche_espace2": "m"
}

# Variables de fichiers de ressources
FICHIERS_RESSOURCES = {
    "obstacles": "ressources/obstacles.txt"
}
