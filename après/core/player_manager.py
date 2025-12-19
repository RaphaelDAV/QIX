"""
Gestionnaire centralisé des joueurs pour éviter la duplication de code
"""

from models.player import Player
from config.config import Joueur1, configurer_joueur2


class PlayerManager:
    """Gestionnaire centralisé pour les joueurs"""
    
    def __init__(self, deux_joueurs=False):
        """Initialise le gestionnaire de joueurs"""
        self.deux_joueurs = deux_joueurs
        self.players = []
        self.player1 = None
        self.player2 = None
        
        # Historiques pour chaque joueur
        self.historiques = {}
        
    def initialiser_joueurs(self):
        """Initialise les joueurs selon le mode de jeu"""
        from config.constants import TERRAIN_X_MIN, TERRAIN_X_MAX, TERRAIN_Y_MAX
        
        # Joueur 1
        taille = Joueur1["taille"]
        vitesse_deplacement = Joueur1["vitesse_deplacement"]
        
        # Position du joueur 1 selon le mode
        if self.deux_joueurs:
            # Mode 2 joueurs : joueur 1 en bas à gauche
            player1_x, player1_y = TERRAIN_X_MIN, TERRAIN_Y_MAX
        else:
            # Mode 1 joueur : joueur 1 au milieu du bas
            player1_x, player1_y = (TERRAIN_X_MIN + TERRAIN_X_MAX) // 2, TERRAIN_Y_MAX
        
        self.player1 = Player(player1_x, player1_y, taille, 1, "Pacman1")
        self.players.append(self.player1)
        
        # Initialisation des historiques joueur 1
        self.historiques[1] = {
            'positions': [],
            'trace': [],
            'deplacement': [],
            'vitesse_tracage': vitesse_deplacement
        }
        
        # Joueur 2 si mode deux joueurs
        if self.deux_joueurs:
            # Mode 2 joueurs : joueur 2 en bas à droite
            player2_x, player2_y = TERRAIN_X_MAX, TERRAIN_Y_MAX
            
            self.player2 = Player(
                player2_x, 
                player2_y, 
                taille, 
                2, 
                "Pacman2"
            )
            self.players.append(self.player2)
            
            # Initialisation des historiques joueur 2
            self.historiques[2] = {
                'positions': [],
                'trace': [],
                'deplacement': [],
                'vitesse_tracage': vitesse_deplacement
            }
            
        # Dessine les joueurs immédiatement pour qu'ils soient visibles au démarrage
        try:
            if self.player1:
                self.player1.draw()
            if self.deux_joueurs and self.player2:
                self.player2.draw()
        except Exception:
            # Si le contexte graphique n'est pas encore prêt, on ignore l'erreur
            pass

        return self.player1, self.player2, taille, vitesse_deplacement
    
    def handle_all_input(self, input_handler, zone_safe, vitesse_deplacement):
        """Gère les entrées pour tous les joueurs actifs"""
        movements = {}
        
        # Joueur 1
        dx, dy = self.player1.handle_input(input_handler, zone_safe, vitesse_deplacement)
        movements[1] = (dx, dy)
        
        # Joueur 2 si actif
        if self.deux_joueurs and self.player2:
            dx2, dy2 = self.player2.handle_input(input_handler, zone_safe, vitesse_deplacement)
            movements[2] = (dx2, dy2)
        else:
            movements[2] = (0, 0)
            
        return movements
    
    def handle_all_tracing(self, input_handler, zone_terrain, zone_polygone, zone_obstacle):
        """Gère le traçage pour tous les joueurs actifs"""
        traces = {}
        
        # Joueur 1
        vitesse_tracage = self.historiques[1]['vitesse_tracage']
        touche_espace = "space"
        
        dx_trace, dy_trace = self.player1.handle_tracing(
            input_handler, touche_espace, vitesse_tracage,
            zone_terrain, zone_polygone, zone_obstacle
        )
        traces[1] = (dx_trace, dy_trace)
        
        # Joueur 2 si actif
        if self.deux_joueurs and self.player2:
            vitesse_tracage2 = self.historiques[2]['vitesse_tracage']
            touche_espace2 = "m"
            
            dx2_trace, dy2_trace = self.player2.handle_tracing(
                input_handler, touche_espace2, vitesse_tracage2,
                zone_terrain, zone_polygone, zone_obstacle
            )
            traces[2] = (dx2_trace, dy2_trace)
        else:
            traces[2] = (0, 0)
            
        return traces
    
    def move_all_players(self, movements):
        """Déplace tous les joueurs selon les mouvements donnés"""
        # Mouvement joueur 1
        dx1, dy1 = movements[1]
        if self.player1:
            self.player1.move(dx1, dy1)
            
        # Mouvement joueur 2 si actif
        if self.deux_joueurs and self.player2:
            dx2, dy2 = movements[2]
            self.player2.move(dx2, dy2)
    
    def handle_all_speed_changes(self, input_handler, zone_safe, vitesse):
        """Gère les changements de vitesse pour tous les joueurs"""
        if not vitesse:
            return
            
        # Joueur 1
        if self.player1.handle_speed_change(input_handler, zone_safe, vitesse):
            self.historiques[1]['vitesse_tracage'] = self.player1.vitesse_tracage
            
        # Joueur 2 si actif
        if self.deux_joueurs and self.player2:
            if self.player2.handle_speed_change(input_handler, zone_safe, vitesse):
                self.historiques[2]['vitesse_tracage'] = self.player2.vitesse_tracage
    
    def clear_traces_in_safe_zone(self, zone_safe):
        """Nettoie les traces des joueurs quand ils sont en zone safe"""
        # Joueur 1
        if (self.player1.is_in_zone(zone_safe) and 
            (len(self.historiques[1]['trace']) == 1 or len(self.historiques[1]['positions']) == 1)):
            self.historiques[1]['positions'].clear()
            self.historiques[1]['trace'].clear()
            
        # Joueur 2 si actif
        if self.deux_joueurs and self.player2:
            if (self.player2.is_in_zone(zone_safe) and 
                (len(self.historiques[2]['trace']) == 1 or len(self.historiques[2]['positions']) == 1)):
                self.historiques[2]['positions'].clear()
                self.historiques[2]['trace'].clear()
    
    def get_historique(self, player_id):
        """Retourne l'historique d'un joueur spécifique"""
        return self.historiques.get(player_id, {})
    
    def update_historiques_from_players(self):
        """Met à jour les historiques à partir des objets Player"""
        if self.player1:
            self.historiques[1]['positions'] = self.player1.historique_positions
            self.historiques[1]['trace'] = self.player1.trait_joueur_actuel
            self.historiques[1]['deplacement'] = self.player1.historique_deplacement
            
        if self.deux_joueurs and self.player2:
            self.historiques[2]['positions'] = self.player2.historique_positions
            self.historiques[2]['trace'] = self.player2.trait_joueur_actuel
            self.historiques[2]['deplacement'] = self.player2.historique_deplacement