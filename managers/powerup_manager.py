"""Module PowerupManager - Gestionnaire powerups pour le jeu QIX"""
from models.powerup import PowerupManager as BasePowerupManager
from fltk import texte, efface


class PowerupManager(BasePowerupManager):
    """Gestionnaire de powerups étendu pour le jeu QIX"""
    
    def __init__(self, zone_pomme=None, deux_joueurs=False):
        super().__init__()
        self.color_effects = {
            1: {"sparks": "green", "qix": "blue"},
            2: {"sparks": "purple", "qix": "purple"}
        }
        self.deux_joueurs = deux_joueurs
    
    def handle_player_powerups(self, player1, player2=None, mode_deux=False):
        """Gère les powerups pour un ou deux joueurs"""
        results = {
            "player1_collected": None,
            "player2_collected": None,
            "color_effects": self.color_effects[1].copy()
        }

        """on collecte les collisions (effectuer les importations/interactions une seule fois par joueur)"""
        collected1 = self.check_player_collisions(player1)
        if collected1:
            results["player1_collected"] = collected1

        collected2 = None
        if mode_deux and player2:
            collected2 = self.check_player_collisions(player2)
            if collected2:
                results["player2_collected"] = collected2

        # Mise à jour des états d'invincibilité en fonction de timers/state 
        player1.set_invincible(self.is_player_invincible(1))
        if player2:
            player2.set_invincible(self.is_player_invincible(2))

        # Mise à jour de l'affichage
        self.update_invincibility_display(1, mode_deux)
        if mode_deux:
            self.update_invincibility_display(2, mode_deux)

       # on détermine les effets de couleur : priorité au joueur 2 en mode multijoueur
        if mode_deux and self.is_player_invincible(2):
            results["color_effects"] = self.color_effects[2].copy()
        elif self.is_player_invincible(1):
            results["color_effects"] = self.color_effects[1].copy()
        else:
            results["color_effects"] = self.color_effects[1].copy()

        return results
    
    def update_invincibility_display(self, player_id, mode_deux=False):
        """Met à jour l'affichage de l'invincibilité"""
        tag = f"Invincibilite{player_id}"
        inv = self.is_player_invincible(player_id)

        # Efface le tag précédent pour éviter les textes superposés en double
        if not inv:
            efface(tag)
            return

        # Positions pour l'affichage
        if mode_deux:
            positions = {1: (680, 400), 2: (680, 710)}
        else:
            positions = {1: (50, 170)}

        pos = positions.get(player_id)
        if not pos:
            return

        x, y = pos
        efface(tag)
        texte(x, y, "Invincibilite", couleur="yellow", taille=16,
              police="Copperplate Gothic Bold", tag=tag)
    
    def create_powerups_from_config(self, positions_pommes, sprites_fruits):
        """Crée les powerups à partir de la configuration existante"""
        from fltk import image
        from models.powerup import Powerup

        # Associe les positions avec les sprites disponibles (s'arrête au plus court)
        for i, (pos, sprite) in enumerate(zip(positions_pommes, sprites_fruits), start=1):
            pomme_x, pomme_y = pos
            image(pomme_x, pomme_y, sprite, largeur=20, hauteur=20, tag=f"pomme{i}")
            powerup = Powerup(pomme_x, pomme_y, i, sprite)
            self.add_powerup(powerup)
