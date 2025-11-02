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
        
        # Vérification joueur 1
        collected_id = self.check_player_collisions(player1)
        if collected_id:
            results["player1_collected"] = collected_id
            player1.set_invincible(True)
        
        # Vérification joueur 2 (si mode multijoueur)
        if mode_deux and player2:
            collected_id = self.check_player_collisions(player2)
            if collected_id:
                results["player2_collected"] = collected_id
                player2.set_invincible(True)
                results["color_effects"] = self.color_effects[2].copy()
        
        # Mise à jour des statuts d'invincibilité
        player1.set_invincible(self.is_player_invincible(1))
        if player2:
            player2.set_invincible(self.is_player_invincible(2))
        
        # Mise à jour de l'affichage
        self.update_invincibility_display(1, mode_deux)
        if mode_deux:
            self.update_invincibility_display(2, mode_deux)
        
        if not mode_deux and not self.is_player_invincible(1):
            results["color_effects"] = self.color_effects[1].copy()
        
        return results
    
    def update_invincibility_display(self, player_id, mode_deux=False):
        """Met à jour l'affichage de l'invincibilité"""
        tag = f"Invincibilite{player_id}"
        
        if self.is_player_invincible(player_id):
            if mode_deux:
                positions = {
                    1: (680, 400),
                    2: (680, 710)
                }
            else:
                positions = {1: (50, 170)}
            
            if player_id in positions:
                x, y = positions[player_id]
                texte(
                    x, y, "Invincibilite",
                    couleur="yellow", taille=16,
                    police="Copperplate Gothic Bold",
                    tag=tag
                )
        else:
            efface(tag)
    
    def create_powerups_from_config(self, positions_pommes, sprites_fruits):
        """Crée les powerups à partir de la configuration existante"""
        from fltk import image
        
        for i, (pomme_x, pomme_y) in enumerate(positions_pommes):
            if i < len(sprites_fruits):
                image(
                    pomme_x, pomme_y, sprites_fruits[i],
                    largeur=20, hauteur=20, tag=f"pomme{i+1}"
                )
                
                from models.powerup import Powerup
                powerup = Powerup(pomme_x, pomme_y, i + 1, sprites_fruits[i])
                self.add_powerup(powerup)
