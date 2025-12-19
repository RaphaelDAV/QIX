import os
from random import randint

# Import des classes du jeu
from models.player import Player
from models.qix import Qix
from models.sparks import Sparks, SparksManager

# Import des constantes
from config.constants import (
    TERRAIN_X_MIN, TERRAIN_Y_MIN, TERRAIN_X_MAX, TERRAIN_Y_MAX,
    VITESSE_DEPLACEMENT_BASE, VITESSE_TRACAGE_LENTE, VITESSE_TRACAGE_RAPIDE,
    VIES_INITIALES, SPRITES_SPARKS, GRILLE_PAS, DIRECTIONS_SPARKS_DEFAUT
)

# ------------------ Joueur 1 ------------------
Joueur1 = {
    "cx": TERRAIN_X_MIN,  # Position X de départ (bordure gauche)
    "cy": TERRAIN_Y_MAX,  # Position Y de départ (bordure bas)
    "taille": 10,         # Taille du joueur
    "iteration": 0,       # Compteur d'itérations
    "vitesse_deplacement": VITESSE_DEPLACEMENT_BASE,
    "surface_polygone": 0,
}

# ------------------ QIX ------------------
QIX = {
    "couleur": "blue",
    "x": (TERRAIN_X_MIN + TERRAIN_X_MAX) // 2,  # Centre du terrain en X
    "y": (TERRAIN_Y_MIN + TERRAIN_Y_MAX) // 2,  # Centre du terrain en Y
    "vitesse": 10,
}

# ------------------ Sparks ------------------
SPARKS = [
    {"x": TERRAIN_X_MIN, "y": TERRAIN_Y_MIN, "taille": 20, "img": "Fantome1", "tag": "sparks1"},
    {"x": TERRAIN_X_MIN, "y": TERRAIN_Y_MIN, "taille": 20, "img": "Fantome2", "tag": "sparks2"},
]

# Ajout des Sparks selon le niveau
def ajouter_sparks_niveau(niveau):
    if niveau in [2, 3]:
        SPARKS.extend([
            {"x": 50, "y": 205, "taille": 20, "img": "Fantome3", "tag": "sparks3"},
            {"x": 550, "y": 205, "taille": 20, "img": "Fantome4", "tag": "sparks4"},
        ])
    if niveau == 3:
        SPARKS.extend([
            {"x": 175, "y": 200, "taille": 20, "img": "Fantome5", "tag": "sparks5"},
            {"x": 425, "y": 200, "taille": 20, "img": "Fantome1", "tag": "sparks6"},
        ])

# ------------------ Obstacles ------------------
def charger_obstacles(predefini=True, aleatoire=False):
    mat = []
    if predefini and os.path.isfile("ressources/obstacles.txt"):
        with open("ressources/obstacles.txt") as f:
            lignes = [l.strip() for l in f.readlines()]
        temp2 = lignes[10].split(",")
        mat = [list(map(int, c.split())) for c in temp2]

    if aleatoire:
        for _ in range(3):
            x, y, taille = randint(100, 300), randint(380, 580), randint(50, 120)
            mat.append([x, y, taille])
    return mat

# ------------------ Pommes ------------------
def placer_pomme(zone_obstacle):
    #Génère une position aléatoire pour placer une pomme/bonus
    from core.game_state import game_state
    x, y = randint(100, 500), randint(250, 700)
    while (x % GRILLE_PAS != 0 or y % GRILLE_PAS != 0 or 
           game_state.is_point_in_obstacle(x, y)):
        x, y = randint(100, 500), randint(250, 700)
    return x, y

def charger_pommes(predefini=True, zone_obstacle=None):
    positions = []
    if zone_obstacle is None:
        zone_obstacle = []
    
    if predefini:
        # Import de la fonction du module utils
        for _ in range(5):
            positions.append(placer_pomme(zone_obstacle))
    else:
        if os.path.isfile("ressources/obstacles.txt"):
            with open("ressources/obstacles.txt") as f:
                lignes = [l.strip() for l in f.readlines()]
            positions = [
                (int(lignes[27]), int(lignes[28])),
                (int(lignes[32]), int(lignes[33])),
                (int(lignes[37]), int(lignes[38])),
                (int(lignes[42]), int(lignes[43])),
                (int(lignes[47]), int(lignes[48])),
            ]
    return positions

# ------------------ Vitesse ------------------
VITESSE_TRACAGE = {
    True: VITESSE_TRACAGE_RAPIDE,   # mode rapide
    False: VITESSE_TRACAGE_LENTE,   # vitesse par défaut
}

# ------------------ Niveaux ------------------
NIVEAUX = {
    1: {"longueur_QIX": 6, "vitesse_QIX": 10, "vitesse_sparks": 1},
    2: {"longueur_QIX": 9, "vitesse_QIX": 20, "vitesse_sparks": 1},
    3: {"longueur_QIX": 12, "vitesse_QIX": 30, "vitesse_sparks": 1},
}





# ------------------ Fonctions d'initialisation des classes ------------------

def creer_qix(niveau=1):
    """Crée le Qix avec la configuration du niveau"""
    config_niveau = NIVEAUX.get(niveau, NIVEAUX[1])
    return Qix(
        QIX["x"], 
        QIX["y"], 
        config_niveau["vitesse_QIX"],
        config_niveau["longueur_QIX"]
    )

def creer_sparks_manager(niveau=1, mode_menu=False):
    """Crée le gestionnaire de Sparks selon le niveau"""
    manager = SparksManager()
    config_niveau = NIVEAUX.get(niveau, NIVEAUX[1])
    vitesse_sparks = max(1, config_niveau["vitesse_sparks"])  # Éviter vitesse 0
    
    # Mode menu : 2 sparks aux positions opposées sur la ligne du haut
    if mode_menu:
        sparks_configs = [
            {"x": 50, "y": 200, "sprite": "ressources/Fantome1.png", "direction": "Droite"},
            {"x": 550, "y": 200, "sprite": "ressources/Fantome2.png", "direction": "Gauche"},
        ]
    else:
        # Sparks de base (niveau 1+) - positionnés aux extrémités de la bordure du haut
        sparks_configs = [
            {"x": TERRAIN_X_MIN, "y": TERRAIN_Y_MIN, "sprite": SPRITES_SPARKS[0]},
            {"x": TERRAIN_X_MAX, "y": TERRAIN_Y_MIN, "sprite": SPRITES_SPARKS[1]},
        ]
    
    # Sparks supplémentaires niveau 2+ (seulement si pas en mode menu)
    if not mode_menu and niveau >= 2:
        # Répartition sur la bordure du haut : 1/3 et 2/3 de la largeur
        sparks_configs.extend([
            # Sparks3 : 1/3 de la bordure du haut
            {"x": TERRAIN_X_MIN + (TERRAIN_X_MAX - TERRAIN_X_MIN) // 3, "y": TERRAIN_Y_MIN, "sprite": SPRITES_SPARKS[2]},
            # Sparks4 : 2/3 de la bordure du haut
            {"x": TERRAIN_X_MIN + 2 * (TERRAIN_X_MAX - TERRAIN_X_MIN) // 3, "y": TERRAIN_Y_MIN, "sprite": SPRITES_SPARKS[3]},
        ])
    
    # Sparks supplémentaires niveau 3 (seulement si pas en mode menu)
    if not mode_menu and niveau >= 3:
        # Répartition sur la bordure du haut : positions intermédiaires
        sparks_configs.extend([
            # Sparks5 : 1/6 de la bordure du haut
            {"x": TERRAIN_X_MIN + (TERRAIN_X_MAX - TERRAIN_X_MIN) // 6, "y": TERRAIN_Y_MIN, "sprite": SPRITES_SPARKS[4]},
            # Sparks6 : 5/6 de la bordure du haut
            {"x": TERRAIN_X_MIN + 5 * (TERRAIN_X_MAX - TERRAIN_X_MIN) // 6, "y": TERRAIN_Y_MIN, "sprite": SPRITES_SPARKS[0]},
        ])
    
    # Créer les Sparks
    for i, config in enumerate(sparks_configs, 1):
        # Utiliser les directions prédéfinies ou direction par défaut
        sparks_tag = f"sparks{i}"
        direction_initiale = config.get("direction", DIRECTIONS_SPARKS_DEFAUT.get(sparks_tag, ["Gauche"])[0])
        
        sparks = Sparks(
            config["x"], 
            config["y"], 
            10,  # taille fixe
            i,  # sparks_id
            vitesse_sparks,  # vitesse
            GRILLE_PAS,  # deplacement basé sur le pas de grille
            config["sprite"],
            direction_initiale
        )
        manager.add_sparks(sparks)
    
    # Marquer le mode menu
    manager.mode_menu = mode_menu
    manager.jeu_commence = False  # Le jeu n'a pas encore commencé, attendre le clic
    
    return manager


# ------------------ Configuration du mode 2 joueurs ------------------

def configurer_joueur2(deux_joueurs=True):
    """Configure les variables spécifiques au joueur 2"""
    if not deux_joueurs:
        return {"touche_espace": "space"}
    
    return {
        "cx": TERRAIN_X_MIN,   
        "cy": TERRAIN_Y_MAX,   
        "cx2": TERRAIN_X_MAX,  
        "cy2": TERRAIN_Y_MAX,  
        "historique_positions2": [],
        "trait_joueur_actuel2": [],
        "iteration2": 0,
        "touche_espace": "m",
        "touche_espace2": "space",
        "historique_deplacement2": [],
        "historique_virage2": [],
        "vitesse_tracage2": VITESSE_TRACAGE_LENTE,
        "surface_polygone_joueur1": 0,
        "surface_polygone_joueur2": 0,
        "touche_V2": "v",
        "score1": 0,
        "score2": 0,
        "Nombre_vie2": VIES_INITIALES,
        "Invincibilite2": False
    }

