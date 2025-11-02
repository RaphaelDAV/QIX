"""Gestionnaire de collisions entre joueurs pour le jeu QIX"""

from fltk import efface, texte
from time import sleep
from config.constants import VIES_INITIALES


class PlayerCollisionManager:
    """Gestionnaire centralisé pour les collisions entre joueurs"""
    
    def __init__(self):
        """Initialise le gestionnaire de collisions"""
        self.collision_types = {
            'ENFERMEMENT': 'enfermement',
            'CROISEMENT_LIGNE': 'croisement_ligne'
        }
    
    def check_player_trapped(self, player, zone_safe, zone_terrain, zone_polygone):
        """Vérifie si un joueur est enfermé (piégé hors des zones autorisées)"""
        player_pos = player.get_position()
        
        is_trapped = (
            (player_pos not in zone_safe and player_pos not in zone_terrain) or
            player_pos in zone_polygone
        )
        
        return is_trapped
    
    def check_line_crossing(self, player, other_player_trail):
        """Vérifie si un joueur croise la ligne de l'autre joueur"""
        return player.get_position() in other_player_trail
    
    def _clear_player_traces(self, historiques_data):
        """Nettoie les traces et historiques d'un joueur"""
        historiques_data.get('historique_deplacement', []).clear()
        historiques_data.get('trait_joueur_actuel', []).clear()
        historiques_data.get('historique_positions', []).clear()
        
        if 'iteration' in historiques_data:
            historiques_data['iteration'] = 0
    
    def _update_life_display(self, player_num, vies_restantes):
        """Met à jour l'affichage des vies (cœurs)"""
        if player_num == 1:
            if vies_restantes == 2:
                efface("coeur1")
            elif vies_restantes == 1:
                efface("coeur2")
            elif vies_restantes == 0:
                efface("coeur3")
        else:
            if vies_restantes == 2:
                efface("coeur1_2")
            elif vies_restantes == 1:
                efface("coeur2_2")
            elif vies_restantes == 0:
                efface("coeur3_2")
    
    def _handle_game_over(self, winning_player_num, scorev, score1, score2):
        """Gère la fin de partie et l'affichage du gagnant"""
        elements_to_clear = [
            "coeur3", "coeur3_2", "sparks2", "sparks1", 
            "Fantome_QIX", "joueur1", "joueur2"
        ]
        for element in elements_to_clear:
            efface(element)
        
        winner_text = f"JOUEUR {winning_player_num} À GAGNÉ"
        texte(
            300, 450, winner_text,
            couleur="green", taille=30,
            police="Copperplate Gothic Bold",
            ancrage="center"
        )
        
        if scorev:
            self._display_final_scores(score1, score2)
        
        return False
    
    def _display_final_scores(self, score1, score2):
        """Affiche les scores finaux"""
        # Score joueur 1
        texte(
            170, 470, "Score joueur 1:",
            couleur="white", taille=20,
            police="Copperplate Gothic Bold"
        )
        texte(
            450, 470, int(score1),
            couleur="red", taille=20,
            police="Copperplate Gothic Bold"
        )
        
        # Score joueur 2
        texte(
            170, 500, "Score joueur 2:",
            couleur="white", taille=20,
            police="Copperplate Gothic Bold"
        )
        texte(
            450, 500, int(score2),
            couleur="red", taille=20,
            police="Copperplate Gothic Bold"
        )
    
    def handle_trapping_collision(self, player1, player2, quel_joueur, 
                                 zone_safe, zone_terrain, zone_polygone,
                                 scorev, score1, score2, historiques_data):
        """Gère les collisions d'enfermement entre joueurs"""
        if quel_joueur == 2:
            if self.check_player_trapped(player1, zone_safe, zone_terrain, zone_polygone):
                player1.reset_position(player2.x, player2.y)
                
                historiques_j1 = {
                    'historique_deplacement': historiques_data.get('historique_deplacement', []),
                    'trait_joueur_actuel': historiques_data.get('trait_joueur_actuel', []),
                    'historique_positions': historiques_data.get('historique_positions', []),
                    'iteration': 0
                }
                
                self._clear_player_traces(historiques_j1)
                
                efface("trait_joueur")
                efface("joueur1")
                
                player1.draw()
                vies_restantes = player1.lose_life()
                self._update_life_display(1, vies_restantes)
                
                if vies_restantes == 0:
                    return self._handle_game_over(2, scorev, score1, score2)
                
                sleep(0.5)
                
        elif quel_joueur == 1:
            if self.check_player_trapped(player2, zone_safe, zone_terrain, zone_polygone):
                player2.reset_position(player1.x, player1.y)
                
                historiques_j2 = {
                    'historique_deplacement': historiques_data.get('historique_deplacement2', []),
                    'trait_joueur_actuel': historiques_data.get('trait_joueur_actuel2', []),
                    'historique_positions': historiques_data.get('historique_positions2', []),
                    'iteration': 0
                }
                
                self._clear_player_traces(historiques_j2)
                
                # Effacer les éléments graphiques
                efface("trait_joueur2")
                efface("joueur2")
                
                # Redessiner et gérer les vies
                player2.draw()
                vies_restantes = player2.lose_life()
                self._update_life_display(2, vies_restantes)
                
                if vies_restantes == 0:
                    return self._handle_game_over(1, scorev, score1, score2)
                
                sleep(0.5)
        
        return True  # Le jeu continue
    
    def handle_line_crossing_collision(self, player1, player2, trait_joueur_actuel, 
                                     trait_joueur_actuel2, scorev, score1, score2,
                                     historiques_data):
        """Gère les collisions de croisement de lignes entre joueurs"""
        game_continues = True
        
        if self.check_line_crossing(player1, trait_joueur_actuel2):
            if score1 > 0:
                first_pos = historiques_data.get('historique_positions', [[550, 750]])[0]
                player1.reset_position(first_pos[0], first_pos[1])
            else:
                player1.reset_position(550, 750)
            
            historiques_j1 = {
                'historique_deplacement': historiques_data.get('historique_deplacement', []),
                'trait_joueur_actuel': historiques_data.get('trait_joueur_actuel', []),
                'historique_positions': historiques_data.get('historique_positions', []),
                'iteration': 0
            }
            
            vies_restantes = player1.lose_life()
            self._update_life_display(1, vies_restantes)
            
            if vies_restantes == 0:
                game_continues = self._handle_game_over(2, scorev, score1, score2)
            
            self._clear_player_traces(historiques_j1)
            efface("trait_joueur")
            efface("joueur1")
            player1.draw()
            sleep(0.5)
        
        # Vérifier si joueur 2 croise la ligne de joueur 1
        if self.check_line_crossing(player2, trait_joueur_actuel):
            # Repositionner joueur 2
            if score2 > 0:
                first_pos = historiques_data.get('historique_positions2', [[50, 750]])[0]
                player2.reset_position(first_pos[0], first_pos[1])
            else:
                player2.reset_position(50, 750)
            
            # Préparer les données pour joueur 2
            historiques_j2 = {
                'historique_deplacement': historiques_data.get('historique_deplacement2', []),
                'trait_joueur_actuel': historiques_data.get('trait_joueur_actuel2', []),
                'historique_positions': historiques_data.get('historique_positions2', []),
                'iteration': 0
            }
            
            # Gérer la défaite
            vies_restantes = player2.lose_life()
            self._update_life_display(2, vies_restantes)
            
            if vies_restantes == 0:
                game_continues = self._handle_game_over(1, scorev, score1, score2)
            
            self._clear_player_traces(historiques_j2)
            efface("trait_joueur2")
            efface("joueur2")
            player2.draw()
            sleep(0.5)
        
        return game_continues