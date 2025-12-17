# ════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
#                           ███████╗  ██╗██╗  ██╗    ██████╗  █████╗ ███╗   ███╗███████╗
#                           ██╔═══██╗██╔╝╚██╗██╔╝   ██╔════╝ ██╔══██╗████╗ ████║██╔════╝
#                           ██║   ██║██║  ╚███╔╝    ██║  ███╗███████║██╔████╔██║█████╗  
#                           ██║▄▄ ██║██║  ██╔██╗    ██║   ██║██╔══██║██║╚██╔╝██║██╔══╝  
#                           ╚██████╔╝██║ ██╔╝ ██╗   ╚██████╔╝██║  ██║██║ ╚═╝ ██║███████╗
#                            ╚══▀▀═╝ ╚═╝ ╚═╝  ╚═╝    ╚═════╝ ╚═╝  ╚═╝╚═╝     ╚═╝╚══════╝
# ═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════
# Auteurs: DAVIOT Raphaël & RICHE Abdelrahim
# Description: Jeu QIX optimisé avec programmation orientée objet et architecture modulaire
# ═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════

# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────
# IMPORTS
# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────
from fltk import *
from time import sleep
import sys

# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────
# CONFIGURATION & CONSTANTES
# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────
from config.config import (
creer_qix, creer_sparks_manager, charger_obstacles,
charger_pommes, NIVEAUX, Joueur1, QIX as CONFIG_QIX,
configurer_joueur2
)
from config.constants import *

# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────
# GESTIONNAIRES & UI
# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────
from managers.powerup_manager import PowerupManager
from managers.polygon_manager import PolygonManager
from managers.qix_manager import QixManager
from managers.player_collision_manager import PlayerCollisionManager
from ui.victory_manager import VictoryManager
from models.player import Player
from ui.hud import creer_fenetre_jeu, creer_interface_complete, afficher_interface_2_joueurs
from ui.menu import afficher_menu_accueil, afficher_menu_variantes
from utils.game_zones import initialiser_zones_terrain

# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────
# GESTIONNAIRES CENTRALISÉS
# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────
from core.game_state import game_state
from core.player_manager import PlayerManager

def ferme_fenetre_securise():
    """Ferme la fenêtre seulement si elle existe encore."""
    try:
        ferme_fenetre()
    except:
        pass  # La fenêtre a déjà été fermée

def fenetre():
    """Crée la fenêtre de jeu et l'interface (1 ou 2 joueurs) depuis les constantes."""
    largeur_fenetre, hauteur_fenetre = creer_fenetre_jeu(game_state.config["deux"])
    creer_interface_complete(game_state.config["deux"], game_state.config["scorev"])
    return largeur_fenetre, hauteur_fenetre

# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────
# UTILITAIRES D'INIT
# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────

def initialiser_niveau():
    """Retourne (niveau_actuel, mode_menu) selon les flags de sélection de niveau."""
    niveau1 = game_state.config["niveau1"]
    niveau2 = game_state.config["niveau2"]
    niveau3 = game_state.config["niveau3"]
    
    niveau_actuel = 1
    mode_menu = False
    if niveau2:
        niveau_actuel = 2
    elif niveau3:
        niveau_actuel = 3
    elif not niveau1 and not niveau2 and not niveau3:
        mode_menu = True
        niveau_actuel = 1
    return niveau_actuel, mode_menu


def creer_entites_jeu(niveau_actuel, mode_menu):
    """Instancie QIX, Sparks, collisions joueurs et règle la vitesse du QIX pour le niveau."""
    qix_entite = creer_qix(niveau_actuel)
    sparks_manager = creer_sparks_manager(niveau_actuel, mode_menu)
    qix_manager = QixManager(qix_entite)
    player_collision_manager = PlayerCollisionManager()
    qix_manager.set_speed_for_level(niveau_actuel)
    for sparks in sparks_manager.sparks_list:
        sparks.draw()
    return qix_manager, sparks_manager, player_collision_manager


def initialiser_joueurs():
    """Crée Player 1 (et 2 si nécessaire) et renvoie les paramètres utiles du joueur."""
    taille = Joueur1["taille"]
    vitesse_deplacement = Joueur1["vitesse_deplacement"]
    player1 = Player(Joueur1["cx"], Joueur1["cy"], taille, 1, "Pacman1")
    player2 = None
    if not game_state.config["deux"]:
        player1.draw()
    return player1, player2, taille, vitesse_deplacement

def configurer_niveau(niveau_actuel):
    """Extrait les paramètres du niveau (QIX, Sparks, couleurs) depuis NIVEAUX."""
    xQIX, yQIX = CONFIG_QIX["x"], CONFIG_QIX["y"]
    config_niveau = NIVEAUX[niveau_actuel]
    vitesse_QIX = config_niveau["vitesse_QIX"]
    longueur_deplacement_QIX = config_niveau["longueur_QIX"]
    couleur_sparks = "green"
    vitesse_sparks = max(1, config_niveau["vitesse_sparks"])
    return xQIX, yQIX, vitesse_QIX, longueur_deplacement_QIX, couleur_sparks, vitesse_sparks


def initialiser_obstacles():
    """Charge et dessine les obstacles ; stocke les rectangles pour les collisions."""
    obstacle = game_state.config["obstacle"]
    obstacle_predefini = game_state.config["obstacle_predefini"]
    obstacle_aleatoire = game_state.config["obstacle_aleatoire"]
    
    matobstacles = charger_obstacles(obstacle_predefini, obstacle_aleatoire)
    
    # Stocker les rectangles d'obstacles au lieu de tous les pixels
    zone_obstacle = game_state.get_zone('zone_obstacle')
    zone_obstacle.clear()  # Vider la zone précédente
    
    if obstacle and matobstacles:
        for obstacles in matobstacles:
            rectangle(
                obstacles[0], obstacles[1],
                obstacles[0] + obstacles[2], obstacles[1] + obstacles[2],
                "gray", "gray", tag=("obstacle")
            )
            # Stocker seulement les coordonnées du rectangle [x, y, taille]
            zone_obstacle.append([obstacles[0], obstacles[1], obstacles[2]])
            # keep simple list of obstacles (no compact array)
            zone_obstacle.append([obstacles[0], obstacles[1], obstacles[2]])
    
    return matobstacles


def initialiser_bonus():
    """Génère les pommes/bonus si activés et retourne (positions, manager)."""
    bonus = game_state.config["bonus"]
    bonus_predefini = game_state.config["bonus_predefini"]
    zone_obstacle = game_state.get_zone('zone_obstacle')
    
    positions_pommes = None
    powerup_manager = None
    if bonus:
        positions_pommes = charger_pommes(bonus_predefini, zone_obstacle)
        powerup_manager = PowerupManager()
        powerup_manager.create_powerups_from_config(positions_pommes, SPRITES_FRUITS)
    return positions_pommes, powerup_manager

# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────
# BOUCLE DE JEU
# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────

def jeu():
    """Boucle principale : entrées, tracé, polygones, collisions, QIX, score et fin de partie."""
    # Initialisation des gestionnaires
    polygon_manager = PolygonManager(COULEURS_POLYGONES.copy())
    player_manager = PlayerManager(game_state.config["deux"])
    
    # Récupération des zones via game_state
    zone_safe = game_state.get_zone('zone_safe')
    zone_terrain = game_state.get_zone('zone_terrain')
    zone_polygone = game_state.get_zone('zone_polygone')
    zone_obstacle = game_state.get_zone('zone_obstacle')
    zone_polygone_actuelle = game_state.get_zone('zone_polygone_actuelle')
    zone_safe_temp = game_state.get_zone('zone_safe_temp')
    zone_safe_apres_tri = game_state.get_zone('zone_safe_apres_tri')
    historique_positions = game_state.get_zone('historique_positions')
    historique_coin = game_state.get_zone('historique_coin')
    trait_joueur_actuel = game_state.get_zone('trait_joueur_actuel')
    historique_deplacement = game_state.get_zone('historique_deplacement')
    coin = game_state.get_zone('coin')
    coin_apres_tri = game_state.get_zone('coin_apres_tri')
    historique_zone_safe = game_state.get_zone('historique_zone_safe')
    
    niveau_actuel, mode_menu = initialiser_niveau()
    qix_manager, sparks_manager, player_collision_manager = creer_entites_jeu(niveau_actuel, mode_menu)
    player1, player2, taille, vitesse_deplacement = player_manager.initialiser_joueurs()
    xQIX, yQIX, vitesse_QIX, longueur_deplacement_QIX, couleur_sparks, vitesse_sparks = configurer_niveau(niveau_actuel)
    
    largeur = (TERRAIN_X_MAX - TERRAIN_X_MIN) // GRILLE_PAS
    hauteur = (TERRAIN_Y_MAX - TERRAIN_Y_MIN) // GRILLE_PAS
    nb_positions = int(largeur * hauteur)
    
    # État d'invincibilité
    game_state.invincibilite1 = False
    game_state.invincibilite2 = False
    
    matobstacles = initialiser_obstacles()
    positions_pommes, powerup_manager = initialiser_bonus()
    
    victory_manager = VictoryManager()
    
    # Configuration des variables de jeu depuis game_state
    vitesse = game_state.config["vitesse"]
    deux = game_state.config["deux"]
    scorev = game_state.config["scorev"]
    
    # Vitesse de tracé affichée (optionnel)
    if vitesse:
        texte(280, 170, "Vitesse traçage:", couleur="white", taille=15, police="Copperplate Gothic Bold")
        texte(475, 170, "Lente", couleur="green", taille=15, police="Copperplate Gothic Bold", tag="vitesse")
        vitesse_tracage = VITESSE_TRACAGE_LENTE
    else:
        vitesse_tracage = vitesse_deplacement  # vitesse par défaut
        
    # Initialisation vitesse traçage pour joueur 2
    vitesse_tracage2 = vitesse_tracage
        
    # Mise à jour des contrôles selon le mode de jeu
    game_state.update_controls_for_mode()
    
    # Configuration des contrôles depuis game_state
    touche_V = game_state.controls["touche_V"]
    touche_V2 = game_state.controls["touche_V2"]
    touche_espace = game_state.controls["touche_espace"]
    touche_espace2 = game_state.controls["touche_espace2"]
    
    # Initialisation des scores
    game_state.score = 0
    
    # Affichage interface deux joueurs si nécessaire
    if deux:
        afficher_interface_2_joueurs(scorev)
        game_state.score1 = 0
        game_state.score2 = 0
    else:
        game_state.score1 = game_state.score
        game_state.score2 = 0
        
    # Synchronisation des vitesses/touches avec Player
    player1.vitesse_tracage = vitesse_tracage
    player1.touche_vitesse = touche_V
    if deux and player2 is not None:
        player2.vitesse_tracage = vitesse_tracage2
        player2.touche_vitesse = touche_V2
        player2.touche_vitesse = touche_V2

    # Message de démarrage
    texte(300, 475, "CLIQUEZ POUR COMMENCER", couleur="white", taille=20, police="Copperplate Gothic Bold", ancrage="center", tag=sys.intern("commencer"))

    # État boucle
    run = True

    # Cache hot functions locally to avoid global lookups in the main loop
    _donne_ev = donne_ev
    _type_ev = type_ev
    _touche_pressee = touche_pressee

    # ═════════════════════════════════════════════════════════════════════════════════════════════════════════════
    # BOUCLE PRINCIPALE DU JEU
    # ═════════════════════════════════════════════════════════════════════════════════════════════════════════════
    while run:
        # ─────────────────────────────────────────────────────────────────────────────────────────────────────────
        # ÉVÉNEMENTS
        # ─────────────────────────────────────────────────────────────────────────────────────────────────────────
        
        ev = _donne_ev(); tev = _type_ev(ev)
        if tev == "ClicGauche":
            efface("commencer")
            sparks_manager.commencer_jeu()  # Commencer le jeu dans tous les modes
        if _touche_pressee("Escape"):
            ferme_fenetre()
            run = False
            continue
            
       # ─────────────────────────────────────────────────────────────────────────────────────────────────────────
        # DÉPLACEMENT SUR BORDURES (ZONE SAFE)
        # ─────────────────────────────────────────────────────────────────────────────────────────────────────────
        dx, dy = player1.handle_input(_touche_pressee, zone_safe, vitesse_deplacement)
        dx2, dy2 = 0, 0
        if deux and player2 is not None:
            dx2, dy2 = player2.handle_input(_touche_pressee, zone_safe, vitesse_deplacement)

        # ─────────────────────────────────────────────────────────────────────────────────────────────────────────
        # TRAÇAGE DANS LE TERRAIN (ZONE DANGEREUSE)
        # ─────────────────────────────────────────────────────────────────────────────────────────────────────────
        dx_trace, dy_trace = player1.handle_tracing(
            _touche_pressee, touche_espace, vitesse_tracage,
            zone_terrain, zone_polygone, zone_obstacle
        )
        if dx_trace or dy_trace:
            dx, dy = dx_trace, dy_trace
        historique_positions = player1.historique_positions
        trait_joueur_actuel = player1.trait_joueur_actuel
        historique_deplacement = player1.historique_deplacement

        # Initialisation des variables du joueur 2 (même en mode 1 joueur pour éviter les erreurs)
        historique_positions2 = []
        trait_joueur_actuel2 = []
        historique_deplacement2 = []
        # NE PAS réinitialiser dx2, dy2 ici - ils ont déjà été calculés plus haut !

        if deux and player2 is not None:
            dx2_trace, dy2_trace = player2.handle_tracing(
                _touche_pressee, touche_espace2, vitesse_tracage2,
                zone_terrain, zone_polygone, zone_obstacle
            )
            if dx2_trace or dy2_trace:
                dx2, dy2 = dx2_trace, dy2_trace
            historique_positions2 = player2.historique_positions
            trait_joueur_actuel2 = player2.trait_joueur_actuel
            historique_deplacement2 = player2.historique_deplacement
            
        # ─────────────────────────────────────────────────────────────────────────────────────────────────────────
        # MISE À JOUR & NETTOYAGE DES TRACES
        # ─────────────────────────────────────────────────────────────────────────────────────────────────────────
        if player1.move(dx, dy):
            pass
        # Nettoyer le tracé seulement si le joueur revient vraiment à son point de départ
        if (player1.is_in_zone(zone_safe) and len(historique_positions) > 0 and 
            player1.get_position() == historique_positions[0] and len(trait_joueur_actuel) > 0):
            historique_positions.clear(); trait_joueur_actuel.clear()

        if deux and player2 is not None:
            if player2.move(dx2, dy2):
                pass
            # Nettoyer le tracé seulement si le joueur revient vraiment à son point de départ
            if (player2.is_in_zone(zone_safe) and len(historique_positions2) > 0 and 
                player2.get_position() == historique_positions2[0] and len(trait_joueur_actuel2) > 0):
                historique_positions2.clear(); trait_joueur_actuel2.clear()
                
        # ─────────────────────────────────────────────────────────────────────────────────────────────────────────
        # POWERUPS & INVINCIBILITÉ
        # ─────────────────────────────────────────────────────────────────────────────────────────────────────────
        if powerup_manager is not None:
            powerup_results = powerup_manager.handle_player_powerups(player1, player2, deux)
            game_state.invincibilite1 = powerup_manager.is_player_invincible(1)
            if deux:
                game_state.invincibilite2 = powerup_manager.is_player_invincible(2)
            if powerup_results["player1_collected"] or (deux and powerup_results["player2_collected"]):
                pass 
        # ─────────────────────────────────────────────────────────────────────────────────────────────────────────
        # CHANGEMENT DE VITESSE
        # ─────────────────────────────────────────────────────────────────────────────────────────────────────────
        if vitesse:
            # Gestion du changement de vitesse pour le joueur 1
            if player1.handle_speed_change(_touche_pressee, zone_safe, vitesse):
                vitesse_tracage = player1.vitesse_tracage
            
            # Gestion du changement de vitesse pour le joueur 2 (si en mode deux joueurs)
            if deux and player2 is not None:
                if player2.handle_speed_change(_touche_pressee, zone_safe, vitesse):
                    vitesse_tracage2 = player2.vitesse_tracage


        # ═══════════════════════════════════════════════════════════════════════════════════════════════════
        # CRÉATION D'UN POLYGON
        # ═══════════════════════════════════════════════════════════════════════════════════════════════════
        joueur1_peut_creer = polygon_manager.peut_creer_polygone(player1, zone_safe, historique_positions)
        joueur2_peut_creer = (deux and polygon_manager.peut_creer_polygone(player2, zone_safe, historique_positions2))
        if joueur1_peut_creer or joueur2_peut_creer:
            # PHASE 1 : sélection du joueur et préparation
            zone_interieure = []
            if deux:
                if joueur1_peut_creer:
                    quel_joueur = 1; current_player = player1; current_positions = historique_positions
                    current_trait = trait_joueur_actuel; current_deplacement = historique_deplacement
                    current_vitesse = vitesse_tracage; touche_V = "Suppr"; touche_espace = None
                else:
                    quel_joueur = 2; current_player = player2; current_positions = historique_positions2
                    current_trait = trait_joueur_actuel2; current_deplacement = historique_deplacement2
                    current_vitesse = vitesse_tracage2; touche_V2 = "v"; touche_espace2 = None
            else:
                quel_joueur = 1; current_player = player1; current_positions = historique_positions
                current_trait = trait_joueur_actuel; current_deplacement = historique_deplacement
                current_vitesse = vitesse_tracage; touche_V = "v"; touche_espace = None
            current_positions.append(current_player.get_position())
            if current_vitesse == VITESSE_TRACAGE_RAPIDE and len(current_deplacement) > 1:
                direction = current_deplacement[-1]; x, y = current_player.x, current_player.y
                if direction == "Gauche":
                    current_trait.insert(-2, [x + 5, y])
                elif direction == "Droite":
                    current_trait.insert(-2, [x - 5, y])
                elif direction == "Haut":
                    current_trait.insert(-2, [x, y + 5])
                elif direction == "Bas":
                    current_trait.insert(-2, [x, y - 5])
            
             # PHASE 2 : point optimal & tri horaire
            xAutrePoint, yAutrePoint = current_positions[-1]
            point_optimal = polygon_manager.trouver_point_optimal(
                zone_safe, xQIX, yQIX, xAutrePoint, yAutrePoint
            )
            coin_apres_tri = polygon_manager.trier_zone_horaire(
                zone_safe, point_optimal, historique_coin, coin,
                zone_interieure, current_positions
            )
            coin.clear(); coin.extend(coin_apres_tri)
            zone_safe_apres_tri = polygon_manager.trier_zone_horaire(
                zone_safe, point_optimal, historique_zone_safe
            )
            
            # PHASE 3 : délimitation & mise à jour des zones
            for element in zone_safe:
                if element not in zone_safe_apres_tri:
                    zone_safe_temp.append(element)
            for element in current_trait:
                zone_safe_temp.append(element)
            if current_trait and current_positions:
                polygon_manager.mettre_a_jour_zone_safe(
                    zone_safe, zone_safe_apres_tri, current_trait,
                    current_positions[0], current_positions[-1],
                    zone_safe_temp, coin, zone_interieure
                )
            for element in current_positions:
                zone_interieure.append(element); coin.append(element)
            
            # PHASE 4 : remplissage intérieur & gestion des listes
            positions_interieures = polygon_manager.generer_positions_interieures(zone_interieure)
            for element in positions_interieures:
                if element not in zone_polygone_actuelle:
                    zone_polygone_actuelle.append(element)
            for element in zone_polygone_actuelle:
                if element in zone_terrain:
                    zone_terrain.remove(element)
            polygon_manager.determiner_zone_qix(
                zone_polygone_actuelle, zone_terrain, zone_safe,
                zone_safe_temp, coin, zone_interieure, xQIX, yQIX
            )
            polygon_manager.finaliser_polygone(zone_polygone_actuelle, zone_terrain, zone_polygone)

            # PHASE 5 : affichage & score
            obstacles_info = {
                'predefini': game_state.config["obstacle_predefini"],
                'aleatoire': game_state.config["obstacle_aleatoire"],
                'matobstacles': matobstacles if game_state.config["obstacle_predefini"] else None,
                'obstacles': []
            }
            if game_state.config["obstacle_aleatoire"]:
                obstacle_vars = ['xobstacle1', 'yobstacle1', 'taille_obstacle1',
                                 'xobstacle2', 'yobstacle2', 'taille_obstacle2',
                                 'xobstacle3', 'yobstacle3', 'taille_obstacle3']
                if all(var in globals() for var in obstacle_vars):
                    obstacles_info['obstacles'] = [
                        {'x': globals()['xobstacle1'], 'y': globals()['yobstacle1'], 'taille': globals()['taille_obstacle1']},
                        {'x': globals()['xobstacle2'], 'y': globals()['yobstacle2'], 'taille': globals()['taille_obstacle2']},
                        {'x': globals()['xobstacle3'], 'y': globals()['yobstacle3'], 'taille': globals()['taille_obstacle3']}
                    ]
                else:
                    obstacles_info['aleatoire'] = False
            polygon_manager.dessiner_polygone(zone_interieure, obstacles_info)
            surface_recouverte = polygon_manager.calculer_surface_recouverte(zone_polygone, nb_positions)
            polygon_manager.afficher_surface(surface_recouverte, deux)
            surface_polygone_actuel = len(zone_polygone_actuelle)
            score_gagne = polygon_manager.calculer_score(surface_polygone_actuel, current_vitesse)
            if deux:
                if quel_joueur == 1:
                    game_state.score1 += score_gagne
                    if scorev:
                        efface("score_joueur1"); texte(770, 250, int(game_state.score1), couleur="white", taille=16, police="Copperplate Gothic Bold", tag="score_joueur1")
                else:
                    game_state.score2 += score_gagne
                    if scorev:
                        efface("score_joueur2"); texte(770, 550, int(game_state.score2), couleur="white", taille=16, police="Copperplate Gothic Bold", tag="score_joueur2")
            else:
                game_state.score += score_gagne
                if scorev:
                    efface("score_total"); texte(420, 110, int(game_state.score), couleur="white", taille=16, police="Copperplate Gothic Bold", tag="score_total")

           # PHASE 6 : reset des états de tracé
            if deux:
                touche_espace = "m"; touche_espace2 = "space"
            else:
                touche_espace = "space"
            zones_jeu_local = {
                'zone_safe_temp': zone_safe_temp,
                'zone_safe_apres_tri': zone_safe_apres_tri,
                'historique_coin': historique_coin,
                'coin_apres_tri': coin_apres_tri,
                'zone_polygone_actuelle': zone_polygone_actuelle,
                'trait_joueur_actuel': trait_joueur_actuel,
                'historique_positions': historique_positions,
                'historique_deplacement': historique_deplacement,
                'trait_joueur_actuel2': trait_joueur_actuel2 if deux else [],
                'historique_positions2': historique_positions2 if deux else [],
                'historique_deplacement2': historique_deplacement2 if deux else []
            }
            polygon_manager.reinitialiser_historiques(zones_jeu_local, quel_joueur)

            # VICTOIRE
            if 'victory_manager' not in locals():
                victory_manager = VictoryManager()
            if victory_manager.check_victory_condition(surface_recouverte, deux, quel_joueur):
                # Effacer immédiatement le QIX et tous les éléments de jeu
                efface("Fantome_QIX")
                for i in range(1, 7):
                    efface(f"sparks{i}")
                mise_a_jour()  # Forcer la mise à jour immédiate
                
                if deux:
                    xQIX, yQIX = 150, 300
                player1_score = game_state.score1
                player2_score = game_state.score2
                single_score = game_state.score
                run = victory_manager.display_victory_screen(
                    deux, scorev, surface_recouverte, player1_score, player2_score, single_score, quel_joueur
                )
                
            # COLLISIONS D'ENFERMEMENT (post-polygone)
            if deux:
                historiques_data = {
                    'historique_deplacement': historique_deplacement,
                    'trait_joueur_actuel': trait_joueur_actuel,
                    'historique_positions': historique_positions,
                    'historique_deplacement2': historique_deplacement2,
                    'trait_joueur_actuel2': trait_joueur_actuel2,
                    'historique_positions2': historique_positions2
                }
                run = player_collision_manager.handle_trapping_collision(
                    player1, player2, quel_joueur,
                    zone_safe, zone_terrain, zone_polygone,
                    scorev, game_state.score1, game_state.score2, historiques_data
                )
                if not run:
                    break


        # COLLISIONS ENTRE JOUEURS (croisement de lignes)
        historiques_data = {
            'historique_deplacement': historique_deplacement,
            'trait_joueur_actuel': trait_joueur_actuel,
            'historique_positions': historique_positions,
            'historique_deplacement2': historique_deplacement2 if deux else [],
            'trait_joueur_actuel2': trait_joueur_actuel2 if deux else [],
            'historique_positions2': historique_positions2 if deux else []
        }
        if deux:
            historiques_data = {
                'historique_deplacement': historique_deplacement,
                'trait_joueur_actuel': trait_joueur_actuel,
                'historique_positions': historique_positions,
                'historique_deplacement2': historique_deplacement2,
                'trait_joueur_actuel2': trait_joueur_actuel2,
                'historique_positions2': historique_positions2
            }
            run = player_collision_manager.handle_line_crossing_collision(
                player1, player2, trait_joueur_actuel, trait_joueur_actuel2,
                scorev, game_state.score1, game_state.score2, historiques_data
            )

        # GESTION DU QIX (déplacement + collisions)
        qix_manager.update_and_move(
            vitesse_QIX, longueur_deplacement_QIX,
            zone_safe, zone_polygone, zone_obstacle, zone_terrain,
            game_state.invincibilite1, game_state.invincibilite2
        )
        run = qix_manager.check_all_qix_collisions(
            player1, player2, deux, zone_safe,
            trait_joueur_actuel, trait_joueur_actuel2,
            historique_positions, historique_positions2,
            historique_deplacement, historique_deplacement2,
            game_state.invincibilite1, game_state.invincibilite2, scorev,
            game_state.score, game_state.score1, game_state.score2
        )
        
        # GESTION DES SPARKS (déplacement)
        player_invincible = game_state.invincibilite1 or game_state.invincibilite2
        sparks_manager.move_all(zone_safe, vitesse_sparks, player_invincible)
        sparks_manager.check_out_of_bounds(zone_safe)
        
        # COLLISIONS AVEC LES SPARKS
        # Vérifier collision joueur 1
        sparks_collision = sparks_manager.check_collision_with_player(
            [player1.x, player1.y], game_state.invincibilite1
        )
        if sparks_collision and not game_state.invincibilite1:
            # Téléporter le Sparks vers sa paire
            sparks_manager.teleport_sparks_to_pair(sparks_collision)
            
            vies_restantes = player1.lose_life()
            # Mettre à jour l'affichage des vies
            player_collision_manager._update_life_display(1, vies_restantes)
            if vies_restantes <= 0:
                if deux:
                    # En mode 2 joueurs, l'autre joueur gagne
                    winner = 2 if player1.player_id == 1 else 1
                    run = player_collision_manager._handle_game_over(winner, scorev, game_state.score1, game_state.score2)
                else:
                    # En mode 1 joueur, game over
                    from managers.qix_manager import QixManager
                    temp_qix_manager = QixManager(None)
                    run = temp_qix_manager._handle_game_over(1, False, scorev, game_state.score1, game_state.score2)
                break
        
        # Vérifier collision joueur 2 (si en mode 2 joueurs)
        if deux and player2 is not None:
            sparks_collision2 = sparks_manager.check_collision_with_player(
                [player2.x, player2.y], game_state.invincibilite2
            )
            if sparks_collision2 and not game_state.invincibilite2:
                # Téléporter le Sparks vers sa paire
                sparks_manager.teleport_sparks_to_pair(sparks_collision2)
                
                vies_restantes2 = player2.lose_life()
                # Mettre à jour l'affichage des vies
                player_collision_manager._update_life_display(2, vies_restantes2)
                if vies_restantes2 <= 0:
                    # Joueur 1 gagne
                    run = player_collision_manager._handle_game_over(1, scorev, game_state.score1, game_state.score2)
                    break

        mise_a_jour()


def ferme_fenetre_securise():
    """Ferme la fenêtre seulement si elle existe encore."""
    try:
        ferme_fenetre()
    except:
        pass
    
# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────
# ENTRYPOINT
# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────
def configurer_game_state(config):
    """Configure game_state avec les paramètres du menu"""
    scorev, vitesse, obstacle, bonus, deux, niveau, start, obstacle_aleatoire, obstacle_predefini, niveau1, niveau2, niveau3, bonus_aleatoire, bonus_predefini = config
    
    game_state.set_config(
        scorev=scorev, vitesse=vitesse, obstacle=obstacle, bonus=bonus,
        deux=deux, niveau=niveau, start=start, obstacle_aleatoire=obstacle_aleatoire,
        obstacle_predefini=obstacle_predefini, niveau1=niveau1, niveau2=niveau2,
        niveau3=niveau3, bonus_aleatoire=bonus_aleatoire, bonus_predefini=bonus_predefini
    )

if __name__ == "__main__":
    # Menu principal
    menu = afficher_menu_accueil()

    # Lancement du jeu
    if menu:
        config = afficher_menu_variantes()
        # Si l'utilisateur a cliqué sur Quitter, `config` peut être False/None.
        # Ne pas tenter de l'indexer dans ce cas.
        if config and config[6]:  # start
            configurer_game_state(config)
            fenetre()
            jeu()
            ferme_fenetre_securise()
