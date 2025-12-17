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
        # helper cache (not persistent between calls) can be used by methods
        
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
        """Trouve le point optimal dans la zone safe (loin du QIX, proche du joueur)
        on utilise les distances au carré pour éviter les opérations sqrt inutiles"""
        w = weight_proximite
        def score(point):
            d_qix = (point[0] - xQIX) ** 2 + (point[1] - yQIX) ** 2
            d_autre = (point[0] - xAutrePoint) ** 2 + (point[1] - yAutrePoint) ** 2
            """intention originale : maximiser la distance par rapport au QIX et minimiser la distance par rapport à l'autre point"""
            return (1 - w) * d_qix - w * d_autre

        return min(zone_safe, key=score)
    
    def trier_zone_horaire(self, zone_safe, point_depart, historique, coin=None, 
                          zone_interieure=None, historique_positions=None):
        """Trie une zone dans le sens horaire à partir d'un point de départ"""
        zone_triee = []
        historique.clear()
        historique.append("Gauche")
        
        x, y = point_depart
        """on utilise un ensemble de tuples pour des tests d'appartenance rapides (garde la liste zone_safe originale intacte)"""
        zone_safe_set = set((p[0], p[1]) for p in zone_safe)
        coin_set = set((p[0], p[1]) for p in coin) if coin is not None else None
        zone_interieure_set = set((p[0], p[1]) for p in zone_interieure) if zone_interieure is not None else None
        historique_positions_set = set((p[0], p[1]) for p in historique_positions) if historique_positions is not None else None

        for _ in range(len(zone_safe)):
            dx, dy = 0, 0
            pt = (x, y)
            if coin_set is not None and zone_interieure_set is not None and historique_positions_set is not None:
                if pt in coin_set or pt in historique_positions_set or pt in zone_interieure_set:
                    if [x, y] not in zone_triee:
                        zone_triee.append([x, y])
            else:
                if [x, y] not in zone_triee:
                    zone_triee.append([x, y])
            """Tests d'appartenance rapides en utilisant un ensemble de tuples"""
            if (x - GRILLE_PAS, y) in zone_safe_set and historique[-1] != "Droite":
                dx = -GRILLE_PAS
                historique.append("Gauche")
            elif (x, y + GRILLE_PAS) in zone_safe_set and historique[-1] != "Haut":
                dy = GRILLE_PAS
                historique.append("Bas")
            elif (x + GRILLE_PAS, y) in zone_safe_set and historique[-1] != "Gauche":
                dx = GRILLE_PAS
                historique.append("Droite")
            elif (x, y - GRILLE_PAS) in zone_safe_set and historique[-1] != "Bas":
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
        
        # Remplacer la zone safe par la version triée (plus efficace via extend)
        zone_safe.clear()
        zone_safe.extend(zone_safe_triee)

        # Prepare fast membership and index lookup
        zone_safe_set = set((p[0], p[1]) for p in zone_safe)
        index_map = { (p[0], p[1]) : idx for idx, p in enumerate(zone_safe) }
        
        # Vérifier que les points existent dans la zone safe avant de les chercher
        # Pour une ligne droite entre deux bords, on doit chercher les points les plus proches
        point_debut = premier_point
        point_fin = dernier_point
        
        # Si les points exacts ne sont pas dans zone_safe, chercher les plus proches
        if tuple(premier_point) not in zone_safe_set:
            point_debut = self._trouver_point_le_plus_proche(premier_point, zone_safe)
        if tuple(dernier_point) not in zone_safe_set:
            point_fin = self._trouver_point_le_plus_proche(dernier_point, zone_safe)
        
        # Si on ne trouve toujours pas les points, essayer avec les premiers et derniers éléments du trait
        if tuple(point_debut) not in zone_safe_set and len(trait_joueur) > 0:
            point_debut = self._trouver_point_le_plus_proche(trait_joueur[0], zone_safe)
        if tuple(point_fin) not in zone_safe_set and len(trait_joueur) > 0:
            point_fin = self._trouver_point_le_plus_proche(trait_joueur[-1], zone_safe)
            
        # Dernière vérification - si on ne trouve toujours rien, abandonner
        if tuple(point_debut) not in zone_safe_set or tuple(point_fin) not in zone_safe_set:
            return
        
        # Trouver les indices des points de début et fin via index_map
        coin1_poly = index_map.get((point_debut[0], point_debut[1]))
        coin2_poly = index_map.get((point_fin[0], point_fin[1]))
        if coin1_poly is None or coin2_poly is None:
            return
        
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
    
    def _trouver_point_le_plus_proche(self, point_cherche, zone_safe):
        """
        Trouve le point le plus proche dans la zone safe
        
        Args:
            point_cherche (list): Point à rechercher [x, y]
            zone_safe (list): Liste des points de la zone safe
            
        Returns:
            list: Point le plus proche dans zone_safe
        """
        if not zone_safe:
            return point_cherche

        # Use squared distance to avoid sqrt and reduce allocations
        def sqdist(p):
            return (p[0] - point_cherche[0]) ** 2 + (p[1] - point_cherche[1]) ** 2

        return min(zone_safe, key=sqdist)
    
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
        
        est = self._est_point_dans_polygone
        positions = []
        for x in range(xmin, xmax + 1, GRILLE_PAS):
            for y in range(ymin, ymax + 1, GRILLE_PAS):
                if est(x, y, polygone):
                    positions.append([x, y])
        return positions
    
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
            for mat in matobstacles:
                x0, y0, taille = mat[0], mat[1], mat[2]
                rectangle(x0, y0, x0 + taille, y0 + taille, "gray", "gray", tag="obstacle")
        
        # Obstacles aléatoires
        if obstacles_info.get('aleatoire', False):
            obstacles = obstacles_info.get('obstacles', [])
            for idx, obs in enumerate(obstacles, 1):
                efface(f"obstacle{idx}")
                x0, y0, t = obs['x'], obs['y'], obs['taille']
                rectangle(x0, y0, x0 + t, y0 + t, "gray", "gray", tag=f"obstacle{idx}")
    
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
