from fltk import efface, rectangle, texte
from config.constants import (TERRAIN_X_MIN, TERRAIN_Y_MIN, TERRAIN_X_MAX, TERRAIN_Y_MAX, SURFACE_VICTOIRE)


class VictoryManager:
    """Classe centralisant la gestion des écrans de victoire"""
    
    POLICE_STANDARD = "Copperplate Gothic Bold"
    ZONE_VICTOIRE = (TERRAIN_X_MIN, TERRAIN_Y_MIN, TERRAIN_X_MAX, TERRAIN_Y_MAX)
    COULEUR_FOND = "white"
    COULEUR_BORDURE = "black"
    EPAISSEUR_BORDURE = 3
    
    COULEUR_TITRE = "green"
    COULEUR_TEXTE = "white"
    COULEUR_SCORE = "red"
    COULEUR_SURFACE = "blue"
    
    def __init__(self):
        self.elements_a_effacer = [
            "coeur3", "sparks1", "sparks2", "sparks3", 
            "sparks4", "sparks5", "sparks6", "Fantome_QIX", "joueur1", "joueur2"
        ]
    
    def check_victory_condition(self, surface_recouverte, deux, quel_joueur):
        """Vérifie si les conditions de victoire sont remplies"""
        if deux and (quel_joueur == 1 or quel_joueur == 2):
            return surface_recouverte >= SURFACE_VICTOIRE
        elif not deux:
            return surface_recouverte >= SURFACE_VICTOIRE
        return False
    
    def display_victory_screen(self, deux, scorev, surface_recouverte, 
                              score1=0, score2=0, score=0, winner_player=None):
        """Affiche l'écran de victoire selon le mode de jeu"""
        self._clear_game_elements()
        self._create_victory_background()
        
        if deux:
            self._display_multiplayer_victory(scorev, surface_recouverte, score1, score2, winner_player)
        else:
            self._display_singleplayer_victory(scorev, surface_recouverte, score)
        
        return False
    
    def _clear_game_elements(self):
        from fltk import mise_a_jour
        for element in self.elements_a_effacer:
            efface(element)
        # Forcer la mise à jour pour que les éléments soient effectivement effacés
        mise_a_jour()
    
    def _create_victory_background(self):
        rectangle(
            self.ZONE_VICTOIRE[0], self.ZONE_VICTOIRE[1],
            self.ZONE_VICTOIRE[2], self.ZONE_VICTOIRE[3],
            self.COULEUR_FOND, self.COULEUR_BORDURE, self.EPAISSEUR_BORDURE
        )
    
    def _display_multiplayer_victory(self, scorev, surface_recouverte, score1, score2):
        self._display_surface_info(surface_recouverte, y_position=TERRAIN_Y_MAX-200)
        
        # Toujours afficher le gagnant en mode deux joueurs
        self._display_multiplayer_scores_and_winner(score1, score2, show_scores=scorev)
    
    def _display_singleplayer_victory(self, scorev, surface_recouverte, score):
        self._display_simple_victory_message()
        
        if scorev:
            self._display_single_score(score)
        
        self._display_surface_info(surface_recouverte, y_position=500)
    
    def _display_multiplayer_scores_and_winner(self, score1, score2, show_scores=True):
        if score1 > score2:
            self._display_winner_announcement("JOUEUR 1 À GAGNÉ")
            if show_scores:
                self._display_player_scores(score1, score2, joueur1_gagne=True)
        elif score2 > score1:
            self._display_winner_announcement("JOUEUR 2 À GAGNÉ")
            if show_scores:
                self._display_player_scores(score1, score2, joueur1_gagne=False)
        else:
            self._display_simple_victory_message()
    
    def _display_winner_announcement(self, message_gagnant):
        texte(
            300, 450, message_gagnant,
            couleur=self.COULEUR_TITRE, taille=30,
            police=self.POLICE_STANDARD, ancrage="center"
        )
    
    def _display_player_scores(self, score1, score2, joueur1_gagne=True):
        if joueur1_gagne:
            self._display_score_line("Score joueur 1:", score1, 470)
            self._display_score_line("Score joueur 2:", score2, 500)
        else:
            self._display_score_line("Score joueur 2:", score2, 500)
            self._display_score_line("Score joueur 1:", score1, 470)
    
    def _display_score_line(self, label, score, y_position):
        texte(
            170, y_position, label,
            couleur=self.COULEUR_TEXTE, taille=20, police=self.POLICE_STANDARD
        )
        texte(
            450, y_position, int(score),
            couleur=self.COULEUR_SCORE, taille=20, police=self.POLICE_STANDARD
        )
    
    def _display_single_score(self, score):
        texte(
            170, 470, "Votre score:",
            couleur=self.COULEUR_TEXTE, taille=20, police=self.POLICE_STANDARD
        )
        texte(
            370, 470, int(score),
            couleur=self.COULEUR_SCORE, taille=20, police=self.POLICE_STANDARD
        )
    
    def _display_surface_info(self, surface_recouverte, y_position):
        texte(
            130, y_position, "Surface conquise:",
            couleur=self.COULEUR_TEXTE, taille=20, police=self.POLICE_STANDARD
        )
        texte(
            420, y_position, int(surface_recouverte),
            couleur=self.COULEUR_SURFACE, taille=20, police=self.POLICE_STANDARD
        )
        texte(
            460, y_position, "%",
            couleur=self.COULEUR_SURFACE, taille=20, police=self.POLICE_STANDARD
        )
    
    def _display_simple_victory_message(self):
        texte(
            300, 450, "GAGNÉ",
            couleur=self.COULEUR_TITRE, taille=40,
            police=self.POLICE_STANDARD, ancrage="center"
        )