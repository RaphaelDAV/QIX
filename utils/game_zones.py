from config.constants import (
    TERRAIN_X_MIN, TERRAIN_Y_MIN, TERRAIN_X_MAX, TERRAIN_Y_MAX,
    ZONE_COIN_DEFAUT, GRILLE_PAS
)
from array import array

def initialiser_zones_terrain():
    """Initialise toutes les zones de jeu nécessaires au QIX"""
    zones = {
        # Zones principales
        'zone_safe': [],
        'zone_terrain': [],
        'zone_gauche': [],
        'zone_droite': [],
        'zone_haut': [],
        'zone_bas': [],
        
        # Zones de jeu
        'zone_obstacle': [],
        'zone_polygone': [],
        'zone_polygone_actuelle': [],
        'zone_safe_temp': [],
        'zone_pomme': [],
        
        # Coins et positions
        'coin': ZONE_COIN_DEFAUT.copy(),
        
        # Historiques et données temporaires
        'historique_positions': [],
        'historique_coin': [],
        'historique_virage': [],
        'historique_deplacement': [],
        'historique_zone_safe': [],
        'zone_safe_apres_tri': [],
        'coin_apres_tri': [],
        'trait_joueur_actuel': [],
        'position_qix': []
    }

    # compact storage for obstacles (kept as list of tuples)
    zones['zone_obstacle'] = zones.get('zone_obstacle', [])

    # Génération des zones safe (bordures)
    _generer_zones_bordures(zones)

    # Génération de la zone de terrain interne
    _generer_zone_terrain(zones)

    return zones

def _generer_zones_bordures(zones):
    """Génère les zones de bordures (zone safe) du terrain de jeu"""
    # Bordure gauche
    for i in range(0, TERRAIN_Y_MAX - TERRAIN_Y_MIN + GRILLE_PAS, GRILLE_PAS):
        position = [TERRAIN_X_MIN, TERRAIN_Y_MIN + i]
        zones['zone_safe'].append(position)
        zones['zone_gauche'].append(position)
    
    # Bordure droite
    for i in range(0, TERRAIN_Y_MAX - TERRAIN_Y_MIN + GRILLE_PAS, GRILLE_PAS):
        position = [TERRAIN_X_MAX, TERRAIN_Y_MIN + i]
        zones['zone_safe'].append(position)
        zones['zone_droite'].append(position)
    
    # Bordure haute
    for i in range(0, TERRAIN_X_MAX - TERRAIN_X_MIN, GRILLE_PAS):
        position = [TERRAIN_X_MIN + i, TERRAIN_Y_MIN]
        zones['zone_safe'].append(position)
        zones['zone_haut'].append(position)
    
    # Bordure basse
    for i in range(0, TERRAIN_X_MAX - TERRAIN_X_MIN + GRILLE_PAS, GRILLE_PAS):
        position = [TERRAIN_X_MIN + i, TERRAIN_Y_MAX]
        zones['zone_safe'].append(position)
        zones['zone_bas'].append(position)

def _generer_zone_terrain(zones):
    """Génère la zone de terrain interne où le joueur peut tracer"""
    for y in range(TERRAIN_Y_MIN, TERRAIN_Y_MAX, GRILLE_PAS):
        for x in range(TERRAIN_X_MIN, TERRAIN_X_MAX, GRILLE_PAS):
            zones['zone_terrain'].append([x, y])