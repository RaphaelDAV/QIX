"""Gestionnaire QIX pour le jeu QIX"""

from fltk import efface, texte, image
from time import sleep
from random import choice
from config.constants import (
    TERRAIN_X_MIN, TERRAIN_X_MAX, TERRAIN_Y_MIN, TERRAIN_Y_MAX,
    SPRITE_QIX, SPRITE_SPARKS_VULNERABLE, GRILLE_PAS
)


class QixManager:
    """Gestionnaire centralisé pour toutes les opérations liées au QIX"""
    
    QIX_SIZE = 40
    QIX_RADIUS = QIX_SIZE // 2
    
    TERRAIN_MIN_X = TERRAIN_X_MIN + QIX_RADIUS
    TERRAIN_MAX_X = TERRAIN_X_MAX - QIX_RADIUS
    TERRAIN_MIN_Y = TERRAIN_Y_MIN + QIX_RADIUS
    TERRAIN_MAX_Y = TERRAIN_Y_MAX - QIX_RADIUS
    
    DIAGONAL_DIRECTIONS = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
    
    def __init__(self, qix_instance):
        """Initialise le gestionnaire QIX"""
        self.qix = qix_instance
        self.position_qix = []
        self.sprite_normal = SPRITE_QIX
        self.sprite_invincible = SPRITE_SPARKS_VULNERABLE
        
        self.velocity_x = 1
        self.velocity_y = 1
        self.speed_multiplier = 1
        
        self.randomize_initial_direction()
        
    def randomize_initial_direction(self):
        """Randomise la direction initiale du QIX"""
        self.velocity_x, self.velocity_y = choice(self.DIAGONAL_DIRECTIONS)
    
    def set_speed_for_level(self, niveau):
        """Ajuste la vitesse du QIX selon le niveau de difficulté"""
        base_speed = 1
        level_multipliers = {1: 1.0, 2: 1.3, 3: 1.6}
        
        speed = int(base_speed * level_multipliers.get(niveau, 1.0))
        
        direction_x = 1 if self.velocity_x > 0 else -1
        direction_y = 1 if self.velocity_y > 0 else -1
        
        self.velocity_x = speed * direction_x
        self.velocity_y = speed * direction_y
        
    def update_and_move(self, vitesse_QIX, longueur_deplacement_QIX, zone_safe, 
                       zone_polygone, zone_obstacle, zone_terrain, 
                       invincibilite1=False, invincibilite2=False):
        """Met à jour et déplace le QIX en diagonal avec rebonds sur les murs"""
        self.speed_multiplier = max(1, longueur_deplacement_QIX)
        
        nouveau_x, nouveau_y = self._calculate_new_position_with_boundaries()
        
        self._handle_collisions_and_bounces(nouveau_x, nouveau_y, zone_safe, zone_polygone, zone_obstacle)
        
        self._draw_qix(invincibilite1 or invincibilite2)
        self._update_collision_positions()
        
        return True
    
    def _handle_collisions_and_bounces(self, nouveau_x, nouveau_y, zone_safe, zone_polygone, zone_obstacle):
        """Gère les collisions avec les zones interdites et effectue les rebonds"""
        if self._is_valid_qix_position(nouveau_x, nouveau_y, zone_safe, zone_polygone, zone_obstacle):
            self.qix.x, self.qix.y = nouveau_x, nouveau_y
        else:
            self._bounce_off_obstacles(nouveau_x, nouveau_y, zone_safe, zone_polygone, zone_obstacle)
    
    def _bounce_off_obstacles(self, nouveau_x, nouveau_y, zone_safe, zone_polygone, zone_obstacle):
        """Effectue le rebond en fonction de la direction d'arrivée du QIX"""
        if not self._is_valid_qix_position(nouveau_x, self.qix.y, zone_safe, zone_polygone, zone_obstacle) and self.velocity_x != 0:
            self.velocity_x = -self.velocity_x
        elif self._is_valid_qix_position(nouveau_x, self.qix.y, zone_safe, zone_polygone, zone_obstacle):
                self.qix.x = nouveau_x
        
        if not self._is_valid_qix_position(self.qix.x, nouveau_y, zone_safe, zone_polygone, zone_obstacle) and self.velocity_y != 0:
            self.velocity_y = -self.velocity_y
        elif self._is_valid_qix_position(self.qix.x, nouveau_y, zone_safe, zone_polygone, zone_obstacle):
                self.qix.y = nouveau_y
    
    def _calculate_new_position_with_boundaries(self):
        """Calcule la nouvelle position en gérant les rebonds sur les limites du terrain"""
        nouveau_x = self.qix.x + (self.velocity_x * self.speed_multiplier)
        nouveau_y = self.qix.y + (self.velocity_y * self.speed_multiplier)
        
        if nouveau_x <= self.TERRAIN_MIN_X and self.velocity_x < 0:
            self.velocity_x = -self.velocity_x
        elif nouveau_x >= self.TERRAIN_MAX_X and self.velocity_x > 0:
            self.velocity_x = -self.velocity_x
        
        if nouveau_y <= self.TERRAIN_MIN_Y and self.velocity_y < 0:
            self.velocity_y = -self.velocity_y
        elif nouveau_y >= self.TERRAIN_MAX_Y and self.velocity_y > 0:
            self.velocity_y = -self.velocity_y
        
        return (
            self.qix.x + (self.velocity_x * self.speed_multiplier),
            self.qix.y + (self.velocity_y * self.speed_multiplier)
        )
    
    def _is_valid_qix_position(self, x, y, zone_safe, zone_polygone, zone_obstacle):
        """Vérifie si une position est valide pour le QIX"""
        check_points = set()
        
        for dx in range(-self.QIX_RADIUS, self.QIX_RADIUS + 1, GRILLE_PAS):
            for dy in range(-self.QIX_RADIUS, self.QIX_RADIUS + 1, GRILLE_PAS):
                check_points.add((x + dx, y + dy))
        
        for edge_x in [x - self.QIX_RADIUS, x + self.QIX_RADIUS]:
            for edge_y in range(int(y - self.QIX_RADIUS), int(y + self.QIX_RADIUS + 1)):
                check_points.add((edge_x, edge_y))
        
        for edge_y in [y - self.QIX_RADIUS, y + self.QIX_RADIUS]:
            for edge_x in range(int(x - self.QIX_RADIUS), int(x + self.QIX_RADIUS + 1)):
                check_points.add((edge_x, edge_y))
        
        # Vérification optimisée avec conversion directe
        for point in check_points:
            point_list = [point[0], point[1]]
            if (point_list in zone_safe or point_list in zone_polygone or point_list in zone_obstacle):
                return False
        
        return True
    
    def _draw_qix(self, player_invincible=False):
        """
        Dessine le QIX avec le sprite approprié
        
        Args:
            player_invincible (bool): True si un joueur est invincible
        """
        efface("Fantome_QIX")
        
        sprite_actuel = self.sprite_invincible if player_invincible else self.sprite_normal
        
        image(
            self.qix.x,
            self.qix.y,
            sprite_actuel,
            largeur=self.QIX_SIZE,
            hauteur=self.QIX_SIZE,
            tag="Fantome_QIX"
        )
    
    def _update_collision_positions(self):
        """
        Met à jour la liste des positions occupées par le QIX pour les collisions
        Optimisé pour éviter les répétitions
        """
        self.position_qix.clear()
        
        # Générer le périmètre du QIX de manière optimisée
        x_min, x_max = int(self.qix.x - self.QIX_RADIUS), int(self.qix.x + self.QIX_RADIUS)
        y_min, y_max = int(self.qix.y - self.QIX_RADIUS), int(self.qix.y + self.QIX_RADIUS)
        
        # Bords horizontaux (haut et bas)
        for i in range(x_min, x_max):
            self.position_qix.extend([[i, y_min], [i, y_max]])
            
        # Bords verticaux (gauche et droite)
        for i in range(y_min, y_max):
            self.position_qix.extend([[x_min, i], [x_max, i]])
    
    def check_collision_with_trail(self, trail, player_invincible=False):
        """Vérifie si le QIX touche le trait d'un joueur"""
        if player_invincible:
            return False
            
        for element in trail:
            if element in self.position_qix:
                return True
        return False
    
    def check_collision_with_player(self, player_position, player_in_safe_zone=False, 
                                   player_invincible=False):
        """Vérifie si le QIX touche directement un joueur"""
        if player_in_safe_zone or player_invincible:
            return False
            
        return player_position in self.position_qix
    
    def handle_player_collision(self, player, player_num, historique_positions, 
                               trait_joueur_actuel, historique_deplacement,
                               score, deux_joueurs=False, scorev=False, 
                               score1=0, score2=0):
        """
        Gère une collision entre le QIX et un joueur
        """
        # Réinitialiser la position du joueur
        if score > 0 and len(historique_positions) > 0:
            player.reset_position(historique_positions[0][0], historique_positions[0][1])
        else:
            if deux_joueurs:
                reset_x = TERRAIN_X_MAX if player_num == 1 else TERRAIN_X_MIN
                player.reset_position(reset_x, TERRAIN_Y_MAX)
            else:
                player.reset_position(300, TERRAIN_Y_MAX)
        
        # Nettoyer les historiques
        self._clear_player_data(historique_deplacement, trait_joueur_actuel, historique_positions)
        
        # Effacer les éléments graphiques
        player_tag = f"joueur{player_num}"
        trail_tag = f"trait_joueur{player_num if player_num == 2 else ''}"
        
        efface(trail_tag)
        efface(player_tag)
        
        # Redessiner le joueur et gérer les vies
        player.draw()
        vies_restantes = player.lose_life()
        
        # Mettre à jour l'affichage des vies
        self._update_life_display(player_num, vies_restantes)
        
        # Vérifier game over
        if vies_restantes == 0:
            return self._handle_game_over(player_num, deux_joueurs, scorev, score1, score2)
        
        sleep(0.5)
        return True
    
    def _clear_player_data(self, historique_deplacement, trait_joueur_actuel, historique_positions):
        """
        Nettoie les données d'un joueur après collision
        """
        historique_deplacement.clear()
        trait_joueur_actuel.clear()
        historique_positions.clear()
    
    def _update_life_display(self, player_num, vies_restantes):
        """
        Met à jour l'affichage des cœurs selon les vies restantes
        """
        if player_num == 1:
            if vies_restantes == 2:
                efface("coeur1")
            elif vies_restantes == 1:
                efface("coeur2")
            elif vies_restantes == 0:
                efface("coeur3")
        else:  # player_num == 2
            if vies_restantes == 2:
                efface("coeur1_2")
            elif vies_restantes == 1:
                efface("coeur2_2")
            elif vies_restantes == 0:
                efface("coeur3_2")
    
    def _handle_game_over(self, defeated_player, deux_joueurs, scorev, score1, score2):
        """
        Gère la fin de partie
        """
        # Effacer tous les éléments
        elements_to_clear = [
            "coeur3", "coeur3_2", "sparks2", "sparks1", 
            "Fantome_QIX", "joueur1", "joueur2"
        ]
        for element in elements_to_clear:
            efface(element)
        
        # Afficher le message approprié
        if deux_joueurs:
            winner = 2 if defeated_player == 1 else 1
            message = f"JOUEUR {winner} À GAGNÉ"
            couleur = "green"
        else:
            message = "GAME OVER"
            couleur = "red"
        
        texte(
            300, 450, message,
            couleur=couleur, taille=40 if not deux_joueurs else 30,
            police="Copperplate Gothic Bold",
            ancrage="center"
        )
        
        # Afficher les scores en mode 2 joueurs
        if deux_joueurs and scorev:
            self._display_final_scores(score1, score2)
        
        return False
    
    def _display_final_scores(self, score1, score2):
        """
        Affiche les scores finaux
        """
        texte(170, 470, "Score joueur 1:", couleur="white", taille=20,
              police="Copperplate Gothic Bold")
        texte(450, 470, int(score1), couleur="red", taille=20,
              police="Copperplate Gothic Bold")
        texte(170, 500, "Score joueur 2:", couleur="white", taille=20,
              police="Copperplate Gothic Bold")
        texte(450, 500, int(score2), couleur="red", taille=20,
              police="Copperplate Gothic Bold")
    
    def check_all_qix_collisions(self, player1, player2, deux_joueurs, zone_safe,
                                trait_joueur_actuel, trait_joueur_actuel2,
                                historique_positions, historique_positions2,
                                historique_deplacement, historique_deplacement2,
                                invincibilite1, invincibilite2, scorev,
                                score, score1, score2):
        """
        Vérifie toutes les collisions du QIX avec les joueurs (méthode principale)
        """
        # Vérifier collisions avec les traits
        if deux_joueurs:
            # Mode 2 joueurs
            # Collision QIX avec trait joueur 1
            if self.check_collision_with_trail(trait_joueur_actuel, invincibilite1):
                if not self.handle_player_collision(
                    player1, 1, historique_positions, trait_joueur_actuel,
                    historique_deplacement, score1, deux_joueurs, scorev, score1, score2
                ):
                    return False
            
            # Collision QIX avec trait joueur 2
            if self.check_collision_with_trail(trait_joueur_actuel2, invincibilite2):
                if not self.handle_player_collision(
                    player2, 2, historique_positions2, trait_joueur_actuel2,
                    historique_deplacement2, score2, deux_joueurs, scorev, score1, score2
                ):
                    return False
        else:
            # Mode solo
            if self.check_collision_with_trail(trait_joueur_actuel, invincibilite1):
                if not self.handle_player_collision(
                    player1, 1, historique_positions, trait_joueur_actuel,
                    historique_deplacement, score, deux_joueurs, scorev, 0, 0
                ):
                    return False
        
        # Vérifier collisions directes avec les joueurs
        # Joueur 1
        if self.check_collision_with_player(
            player1.get_position(), 
            player1.is_in_zone(zone_safe),
            invincibilite1
        ):
            score_ref = score1 if deux_joueurs else score
            if not self.handle_player_collision(
                player1, 1, historique_positions, trait_joueur_actuel,
                historique_deplacement, score_ref, deux_joueurs, scorev, score1, score2
            ):
                return False
        
        # Joueur 2 (mode 2 joueurs seulement)
        if deux_joueurs and player2 is not None:
            if self.check_collision_with_player(
                player2.get_position(),
                player2.is_in_zone(zone_safe),
                invincibilite2
            ):
                if not self.handle_player_collision(
                    player2, 2, historique_positions2, trait_joueur_actuel2,
                    historique_deplacement2, score2, deux_joueurs, scorev, score1, score2
                ):
                    return False
        
        return True
    
    def get_position(self):
        """Retourne la position actuelle du QIX"""
        return (self.qix.x, self.qix.y)
    
    def reset_position(self, x, y):
        """Réinitialise la position du QIX"""
        self.qix.reset_position(x, y)
        self._update_collision_positions()