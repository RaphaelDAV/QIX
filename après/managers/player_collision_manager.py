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
        """ Pour les listes de zones importantes, les vérifications d'adhésion peuvent s'avérer
        coûteuses; on privilégie donc un système par défaut lorsque cela est avantageux."""
        try:
            len_safe = len(zone_safe)
        except Exception:
            len_safe = 0
        try:
            len_terrain = len(zone_terrain)
        except Exception:
            len_terrain = 0
        try:
            len_polygone = len(zone_polygone)
        except Exception:
            len_polygone = 0

        """On convertissez en ensembles uniquement lorsqu'il ne s'agit pas déjà d'ensembles et qu'ils sont de taille raisonnable."""
        if not isinstance(zone_safe, set) and len_safe > 50:
            zone_safe = set(zone_safe)
        if not isinstance(zone_terrain, set) and len_terrain > 50:
            zone_terrain = set(zone_terrain)
        if not isinstance(zone_polygone, set) and len_polygone > 50:
            zone_polygone = set(zone_polygone)

        is_trapped = ((player_pos not in zone_safe and player_pos not in zone_terrain)
                      or player_pos in zone_polygone)

        return is_trapped
    
    def check_line_crossing(self, player, other_player_trail):
        """Vérifie si un joueur croise la ligne de l'autre joueur"""
        return player.get_position() in other_player_trail
    
    def _clear_player_traces(self, historiques_data):
        """Nettoie les traces et historiques d'un joueur
        on s'assurer que les clés attendues existent et qu'elles 
        sont effacées directement lorsque cela est possible."""
        if 'historique_deplacement' in historiques_data and isinstance(historiques_data['historique_deplacement'], list):
            historiques_data['historique_deplacement'].clear()
        else:
            historiques_data['historique_deplacement'] = []

        if 'trait_joueur_actuel' in historiques_data and isinstance(historiques_data['trait_joueur_actuel'], list):
            historiques_data['trait_joueur_actuel'].clear()
        else:
            historiques_data['trait_joueur_actuel'] = []

        if 'historique_positions' in historiques_data and isinstance(historiques_data['historique_positions'], list):
            historiques_data['historique_positions'].clear()
        else:
            historiques_data['historique_positions'] = []

        historiques_data['iteration'] = 0
    
    def _update_life_display(self, player_num, vies_restantes):
        """Met à jour l'affichage des vies (cœurs)
        on associe les vies restantes au nom de base de l'élément cœur"""
        mapping = {2: 'coeur1', 1: 'coeur2', 0: 'coeur3'}
        base = mapping.get(vies_restantes)
        if base is None:
            return

        suffix = '' if player_num == 1 else '_2'
        efface(f"{base}{suffix}")

        return None

    def _process_post_collision(self, player, historiques_subset, efface_trait_tag,
                                efface_player_tag, player_num, scorev, score1, score2):
        """Opérations communes après une collision: vider historiques, effacer éléments,
        redessiner, décrémenter vie et gérer fin de partie.
        Retourne True si le jeu continue, False sinon.
        """
        self._clear_player_traces(historiques_subset)

        # Effacer éléments graphiques
        if efface_trait_tag:
            efface(efface_trait_tag)
        if efface_player_tag:
            efface(efface_player_tag)

        # Redessiner et gérer les vies
        try:
            player.draw()
        except Exception:
            pass

        vies_restantes = player.lose_life()
        self._update_life_display(player_num, vies_restantes)

        if vies_restantes == 0:
            winning = 2 if player_num == 1 else 1
            return self._handle_game_over(winning, scorev, score1, score2)

        sleep(0.5)
        return True
    
    def _handle_game_over(self, winning_player_num, scorev, score1, score2):
        """Gère la fin de partie et l'affichage du gagnant"""
        from fltk import mise_a_jour
        
        elements_to_clear = [
            "coeur3", "coeur3_2", "sparks1", "sparks2", "sparks3",
            "sparks4", "sparks5", "sparks6", "Fantome_QIX", "joueur1", "joueur2"
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
        
        mise_a_jour()       
        sleep(5)
        
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

                return self._process_post_collision(player1, historiques_j1, "trait_joueur", "joueur1",
                                                    1, scorev, score1, score2)

        elif quel_joueur == 1:
            if self.check_player_trapped(player2, zone_safe, zone_terrain, zone_polygone):
                player2.reset_position(player1.x, player1.y)

                historiques_j2 = {
                    'historique_deplacement': historiques_data.get('historique_deplacement2', []),
                    'trait_joueur_actuel': historiques_data.get('trait_joueur_actuel2', []),
                    'historique_positions': historiques_data.get('historique_positions2', []),
                    'iteration': 0
                }

                return self._process_post_collision(player2, historiques_j2, "trait_joueur2", "joueur2",
                                                    2, scorev, score1, score2)

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

            game_continues = self._process_post_collision(player1, historiques_j1, "trait_joueur", "joueur1",
                                                         1, scorev, score1, score2)
        
        # Vérifier si joueur 2 croise la ligne de joueur 1
        if self.check_line_crossing(player2, trait_joueur_actuel):
            # Repositionner joueur 2
            if score2 > 0:
                first_pos = historiques_data.get('historique_positions2', [[50, 750]])[0]
                player2.reset_position(first_pos[0], first_pos[1])
            else:
                player2.reset_position(50, 750)
            historiques_j2 = {
                'historique_deplacement': historiques_data.get('historique_deplacement2', []),
                'trait_joueur_actuel': historiques_data.get('trait_joueur_actuel2', []),
                'historique_positions': historiques_data.get('historique_positions2', []),
                'iteration': 0
            }

            game_continues = self._process_post_collision(player2, historiques_j2, "trait_joueur2", "joueur2",
                                                         2, scorev, score1, score2)
        
        return game_continues