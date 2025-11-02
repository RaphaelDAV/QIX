"""Gestionnaire de polygones pour le jeu QIX"""

from random import randint
from fltk import polygone, efface, rectangle, texte
from config.constants import (
    GRILLE_PAS, 
    VITESSE_TRACAGE_LENTE, 
    VITESSE_TRACAGE_RAPIDE
)

def echanger_listes(liste1, liste2):
    """Échange le contenu de deux listes"""
    temp = liste1.copy()
    liste1[:] = liste2
    liste2[:] = temp
    
class PolygonManager:
    """Gestionnaire centralisé pour la création et la gestion des polygones"""
    
    def __init__(self, lst_couleur):
        """Initialise le gestionnaire de polygones"""
        self.lst_couleur = lst_couleur
        self.nb_polygone = 0
        self.surface_polygone = 0.0
        
    def peut_creer_polygone(self, player, zone_safe, historique_positions):
        """Vérifie si un joueur peut créer un polygone"""
        if not player.is_in_zone(zone_safe):
            return False
            
        if len(historique_positions) < 1:
            return False
            
        if len(historique_positions) == 1:
            return player.get_position() != historique_positions[0]
            
        return True
    
    def trouver_point_optimal(self, zone_safe, xQIX, yQIX, xAutrePoint, yAutrePoint, 
                             weight_proximite=0.3):
        """Trouve le point optimal dans la zone safe (loin du QIX, proche du joueur)"""
        point_optimal = min(
            zone_safe,
            key=lambda point: (1 - weight_proximite)
            * ((point[0] - xQIX) ** 2 + (point[1] - yQIX) ** 2)
            + weight_proximite
            * -((point[0] - xAutrePoint) ** 2 + (point[1] - yAutrePoint) ** 2),
        )
        return point_optimal
    
    def trier_zone_horaire(self, zone_safe, point_depart, historique, coin=None, 
                          zone_interieure=None, historique_positions=None):
        """Trie une zone dans le sens horaire à partir d'un point de départ"""
        zone_triee = []
        historique.clear()
        historique.append("Gauche")
        
        x, y = point_depart
        
        for _ in range(len(zone_safe)):
            dx, dy = 0, 0
            
            if coin is not None and zone_interieure is not None and historique_positions is not None:
                if ([x, y] in coin or [x, y] in historique_positions or 
                    [x, y] in zone_interieure):
                    if [x, y] not in zone_triee:
                        zone_triee.append([x, y])
            else:
                if [x, y] not in zone_triee:
                    zone_triee.append([x, y])
            
            if [x - GRILLE_PAS, y] in zone_safe and historique[-1] != "Droite":
                dx = -GRILLE_PAS
                historique.append("Gauche")
            elif [x, y + GRILLE_PAS] in zone_safe and historique[-1] != "Haut":
                dy = GRILLE_PAS
                historique.append("Bas")
            elif [x + GRILLE_PAS, y] in zone_safe and historique[-1] != "Gauche":
                dx = GRILLE_PAS
                historique.append("Droite")
            elif [x, y - GRILLE_PAS] in zone_safe and historique[-1] != "Bas":
                dy = -GRILLE_PAS
                historique.append("Haut")
            
            # Déplacer vers le point suivant
            if dx != 0 or dy != 0:
                x += dx
                y += dy
        
        return zone_triee
    
    def mettre_a_jour_zone_safe(self, zone_safe, zone_safe_triee, trait_joueur, 
                                premier_point, dernier_point, zone_safe_temp, coin, 
                                zone_interieure):
        """
        Met à jour la zone safe après création d'un polygone
        
        Args:
            zone_safe (list): Zone safe à mettre à jour (modifiée en place)
            zone_safe_triee (list): Zone safe triée
            trait_joueur (list): Trait tracé par le joueur
            premier_point (list): Premier point du trait
            dernier_point (list): Dernier point du trait
            zone_safe_temp (list): Zone safe temporaire
            coin (list): Liste des coins
            zone_interieure (list): Zone intérieure du polygone
        """
        # Vérifier que les données sont valides avant de continuer
        if not trait_joueur or not premier_point or not dernier_point:
            # Les données ont été effacées (probablement après une collision)
            return
        
        # Remplacer la zone safe par la version triée
        zone_safe.clear()
        for element in zone_safe_triee:
            zone_safe.append(element)
        
        # Vérifier que les points existent dans la zone safe avant de les chercher
        if premier_point not in zone_safe or dernier_point not in zone_safe:
            # Les points ne sont pas dans la zone safe, abandon de l'opération
            return
        
        # Trouver les indices des points de début et fin
        coin1_poly = zone_safe.index(premier_point)
        coin2_poly = zone_safe.index(dernier_point)
        
        # Supprimer la partie de zone safe entre les deux points et ajouter le trait
        if coin2_poly > coin1_poly:
            # Retirer les éléments entre les deux points
            for element in reversed(zone_safe[coin1_poly + 1:coin2_poly]):
                zone_safe.remove(element)
                zone_safe_temp.append(element)
                if element in coin:
                    coin.remove(element)
                    zone_interieure.append(element)
            
            # Insérer le trait du joueur
            for i in range(len(trait_joueur)):
                if trait_joueur[i] not in zone_safe:
                    zone_safe.insert(coin1_poly + i, trait_joueur[i])
        else:
            # Retirer les éléments entre les deux points (dans l'autre sens)
            for element in zone_safe[coin2_poly + 1:coin1_poly]:
                zone_safe.remove(element)
                zone_safe_temp.append(element)
                if element in coin:
                    coin.remove(element)
                    zone_interieure.append(element)
            
            # Insérer le trait du joueur
            for i in range(len(trait_joueur)):
                if trait_joueur[i] not in zone_safe:
                    zone_safe.insert(coin2_poly + i, trait_joueur[i])
    
    def generer_positions_interieures(self, polygone):
        """
        Génère toutes les positions à l'intérieur d'un polygone
        
        Args:
            polygone (list): Liste des points du polygone
            
        Returns:
            list: Liste des positions intérieures
        """
        # Trouver les limites du polygone
        xmin = int(min(p[0] for p in polygone))
        ymin = int(min(p[1] for p in polygone))
        xmax = int(max(p[0] for p in polygone))
        ymax = int(max(p[1] for p in polygone))
        
        positions_interieures = []
        
        # Parcourir toutes les positions possibles
        for x in range(xmin, xmax + 1, GRILLE_PAS):
            for y in range(ymin, ymax + 1, GRILLE_PAS):
                if self._est_point_dans_polygone(x, y, polygone):
                    positions_interieures.append([x, y])
        
        return positions_interieures
    
    def _est_point_dans_polygone(self, x, y, polygone):
        """
        Vérifie si un point est à l'intérieur d'un polygone (algorithme ray-casting)
        
        Args:
            x (float): Coordonnée X du point
            y (float): Coordonnée Y du point
            polygone (list): Liste des sommets du polygone
            
        Returns:
            bool: True si le point est dans le polygone
        """
        n = len(polygone)
        est_a_l_interieur = False
        
        for i in range(n):
            xi, yi = polygone[i]
            xj, yj = polygone[(i + 1) % n]
            
            # Vérifier si le point est entre les deux sommets verticalement
            condition1 = (yi <= y <= yj) or (yj <= y <= yi)
            
            # Vérifier si le point est sur le bord
            sur_le_bord = (
                (y == yi and min(xi, xj) <= x <= max(xi, xj)) or
                (y == yj and min(xi, xj) <= x <= max(xi, xj)) or
                (x == xi and min(yi, yj) <= y <= max(yi, yj)) or
                (x == xj and min(yi, yj) <= y <= max(yi, yj))
            )
            
            if condition1 or sur_le_bord:
                if yi != yj:
                    # Vérifier si le rayon horizontal croise le segment
                    condition2 = x > (xj - xi) * (y - yi) / (yj - yi) + xi
                else:
                    condition2 = False
                
                if condition2:
                    est_a_l_interieur = not est_a_l_interieur
        
        return est_a_l_interieur
    
    def determiner_zone_qix(self, zone_polygone_actuelle, zone_terrain, zone_safe, 
                           zone_safe_temp, coin, zone_interieure, xQIX, yQIX):
        """
        Détermine dans quelle zone se trouve le QIX et inverse les zones si nécessaire
        
        Args:
            zone_polygone_actuelle (list): Polygone en cours de création
            zone_terrain (list): Zone de terrain
            zone_safe (list): Zone safe
            zone_safe_temp (list): Zone safe temporaire
            coin (list): Liste des coins
            zone_interieure (list): Zone intérieure
            xQIX (float): Position X du QIX
            yQIX (float): Position Y du QIX
        """
        # Si le QIX est dans le polygone créé, échanger les zones
        if [xQIX, yQIX] in zone_polygone_actuelle:
            echanger_listes(zone_terrain, zone_polygone_actuelle)
            echanger_listes(zone_safe, zone_safe_temp)
            echanger_listes(coin, zone_interieure)
    
    def finaliser_polygone(self, zone_polygone_actuelle, zone_terrain, zone_polygone):
        """
        Finalise la création du polygone en mettant à jour les zones
        
        Args:
            zone_polygone_actuelle (list): Polygone actuel
            zone_terrain (list): Zone de terrain (modifiée)
            zone_polygone (list): Liste de tous les polygones (modifiée)
        """
        # Retirer les positions du polygone de la zone terrain
        for element in zone_polygone_actuelle:
            if element in zone_terrain:
                zone_terrain.remove(element)
            if element not in zone_polygone:
                zone_polygone.append(element)
    
    def dessiner_polygone(self, zone_interieure, obstacles_info=None):
        """
        Dessine le polygone avec une couleur aléatoire
        
        Args:
            zone_interieure (list): Points du polygone à dessiner
            obstacles_info (dict, optional): Informations sur les obstacles à redessiner
        """
        # Choisir une couleur aléatoire
        if len(self.lst_couleur) > 0:
            couleur_choisie = randint(0, len(self.lst_couleur) - 1)
            couleur = self.lst_couleur[couleur_choisie]
            self.lst_couleur.remove(couleur)
        else:
            couleur = "lightblue"  # Couleur par défaut si plus de couleurs
        
        # Dessiner le polygone
        polygone(
            zone_interieure,
            "midnightblue",
            remplissage=couleur,
            epaisseur=GRILLE_PAS,
        )
        
        # Redessiner les obstacles si nécessaire
        if obstacles_info:
            self._redessiner_obstacles(obstacles_info)
        
        self.nb_polygone += 1
    
    def _redessiner_obstacles(self, obstacles_info):
        """
        Redessine les obstacles après la création d'un polygone
        
        Args:
            obstacles_info (dict): Informations sur les obstacles
        """
        # Obstacles prédéfinis
        if obstacles_info.get('predefini', False):
            matobstacles = obstacles_info.get('matobstacles', [])
            for i in range(len(matobstacles)):
                rectangle(
                    matobstacles[i][0],
                    matobstacles[i][1],
                    matobstacles[i][0] + matobstacles[i][2],
                    matobstacles[i][1] + matobstacles[i][2],
                    "gray",
                    "gray",
                    tag="obstacle",
                )
        
        # Obstacles aléatoires
        if obstacles_info.get('aleatoire', False):
            obstacles = obstacles_info.get('obstacles', [])
            for idx, obs in enumerate(obstacles, 1):
                efface(f"obstacle{idx}")
                rectangle(
                    obs['x'],
                    obs['y'],
                    obs['x'] + obs['taille'],
                    obs['y'] + obs['taille'],
                    "gray",
                    "gray",
                    tag=f"obstacle{idx}",
                )
    
    def calculer_surface_recouverte(self, zone_polygone, nb_positions_totales):
        """
        Calcule le pourcentage de surface recouverte
        
        Args:
            zone_polygone (list): Liste de toutes les positions des polygones
            nb_positions_totales (int): Nombre total de positions possibles
            
        Returns:
            float: Pourcentage de surface recouverte
        """
        surface_polygone = len(zone_polygone)
        return (surface_polygone * 100) / nb_positions_totales
    
    def afficher_surface(self, surface_recouverte, deux_joueurs, x_position=235):
        """
        Affiche le pourcentage de surface recouverte
        
        Args:
            surface_recouverte (float): Pourcentage de surface
            deux_joueurs (bool): Mode 2 joueurs actif
            x_position (int): Position X pour l'affichage solo (défaut 235)
        """
        efface("score_pourcentage")
        x = 700 if deux_joueurs else x_position
        texte(
            x,
            110,
            int(surface_recouverte),
            couleur="white",
            taille=16,
            police="Copperplate Gothic Bold",
            tag="score_pourcentage",
        )
    
    def calculer_score(self, surface_polygone_actuel, vitesse_tracage, score_max=20000):
        """
        Calcule le score gagné pour un polygone
        
        Args:
            surface_polygone_actuel (int): Taille du polygone créé
            vitesse_tracage (int): Vitesse de tracé (VITESSE_TRACAGE_LENTE ou VITESSE_TRACAGE_RAPIDE)
            score_max (int): Score maximum (défaut 20000)
            
        Returns:
            float: Score gagné
        """
        surface_totale = 100 * 110
        
        if vitesse_tracage == VITESSE_TRACAGE_LENTE:
            return surface_polygone_actuel * score_max / surface_totale
        elif vitesse_tracage == VITESSE_TRACAGE_RAPIDE:
            return (surface_polygone_actuel / 2) * score_max / surface_totale
        else:
            return 0
    
    def reinitialiser_historiques(self, zones_jeu, quel_joueur):
        """
        Réinitialise les historiques après création d'un polygone
        
        Args:
            zones_jeu (dict): Dictionnaire contenant toutes les zones
            quel_joueur (int): Numéro du joueur (1 ou 2)
        """
        # Réinitialiser les zones communes
        zones_jeu['zone_safe_temp'].clear()
        zones_jeu['zone_safe_apres_tri'].clear()
        zones_jeu['historique_coin'].clear()
        zones_jeu['coin_apres_tri'].clear()
        zones_jeu['zone_polygone_actuelle'].clear()
        
        # Réinitialiser les historiques du joueur concerné
        if quel_joueur == 1:
            zones_jeu['trait_joueur_actuel'].clear()
            zones_jeu['historique_positions'].clear()
            zones_jeu['historique_deplacement'].clear()
        elif quel_joueur == 2:
            zones_jeu.get('trait_joueur_actuel2', []).clear()
            zones_jeu.get('historique_positions2', []).clear()
            zones_jeu.get('historique_deplacement2', []).clear()
