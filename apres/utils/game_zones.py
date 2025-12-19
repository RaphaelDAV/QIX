from config.constants import (
    TERRAIN_X_MIN, TERRAIN_Y_MIN, TERRAIN_X_MAX, TERRAIN_Y_MAX,
    ZONE_COIN_DEFAUT, GRILLE_PAS
)
from collections.abc import MutableSequence
from typing import Iterable, List, Tuple, Optional


class ZoneGrid(MutableSequence):
    """Séquence paresseuse basée sur une grille de points alignés.

    Se comporte comme une liste de points `[x, y]` alignés sur une
    grille régulière entre xmin..xmax et ymin..ymax avec un pas `pas`.
    La liste complète n'est *pas* générée tant que des opérations
    nécessitant un accès aléatoire ou une mutation ne sont pas utilisées.
    Les vérifications d'appartenance (`in`) sont implémentées de façon
    efficace sans allouer la grille entière.
    """

    def __init__(self, xmin: int, xmax: int, ymin: int, ymax: int, pas: int):
        self.xmin = xmin
        self.xmax = xmax
        self.ymin = ymin
        self.ymax = ymax
        self.pas = pas

        # caches transitoires / tampons de mutation
        self._removed: set[Tuple[int, int]] = set()
        self._added: List[List[int]] = []
        self._cache: Optional[List[List[int]]] = None

    # --- fonctions paresseuses ---
    def _aligned(self, x: int, y: int) -> bool:
        return (
            self.xmin <= x <= self.xmax
            and self.ymin <= y <= self.ymax
            and ((x - self.xmin) % self.pas) == 0
            and ((y - self.ymin) % self.pas) == 0
        )

    def _generate(self) -> List[List[int]]:
        """Matérialise la liste complète de points (en tenant compte des suppressions et ajouts)."""
        pts: List[List[int]] = []
        for y in range(self.ymin, self.ymax + 1, self.pas):
            for x in range(self.xmin, self.xmax + 1, self.pas):
                if (x, y) in self._removed:
                    continue
                pts.append([x, y])
        # incorporer les points ajoutés (préserver l'ordre d'ajout)
        if self._added:
            pts.extend(self._added)
        return pts

    def _ensure_cache(self):
        if self._cache is None:
            self._cache = self._generate()

    # --- API MutableSequence ---
    def __len__(self) -> int:
        if self._cache is not None:
            return len(self._cache)
        # calculer la taille sans matérialiser la liste complète
        nx = ((self.xmax - self.xmin) // self.pas) + 1
        ny = ((self.ymax - self.ymin) // self.pas) + 1
        return nx * ny - len(self._removed) + len(self._added)

    def __getitem__(self, index):
        self._ensure_cache()
        return self._cache[index]

    def __setitem__(self, index, value):
        self._ensure_cache()
        self._cache[index] = value

    def __delitem__(self, index):
        self._ensure_cache()
        del self._cache[index]

    def insert(self, index: int, value):
        self._ensure_cache()
        self._cache.insert(index, value)

    def __iter__(self):
        if self._cache is not None:
            yield from self._cache
            return
        # itérer paresseusement sans allouer la liste complète
        for y in range(self.ymin, self.ymax + 1, self.pas):
            for x in range(self.xmin, self.xmax + 1, self.pas):
                if (x, y) in self._removed:
                    continue
                yield [x, y]
        for p in self._added:
            yield p

    def __contains__(self, item) -> bool:
        # accepter liste/tuple [x,y] ou (x,y)
        try:
            x, y = (item[0], item[1])
        except Exception:
            return False
        if [x, y] in self._added:
            return True
        if (x, y) in self._removed:
            return False
        return self._aligned(x, y)

    # méthodes utilitaires qui modifient
    def remove(self, value):
        # préférer marquer la suppression plutôt que de matérialiser
        try:
            x, y = (value[0], value[1])
        except Exception:
            raise ValueError("value not in ZoneGrid")
        if [x, y] in self._added:
            # retirer des ajouts si présent
            self._added.remove([x, y])
            if self._cache is not None:
                try:
                    self._cache.remove([x, y])
                except ValueError:
                    pass
            return
        if not self._aligned(x, y):
            raise ValueError("value not in ZoneGrid")
        self._removed.add((x, y))
        if self._cache is not None:
            try:
                self._cache.remove([x, y])
            except ValueError:
                pass

    def append(self, value):
        self._added.append([value[0], value[1]])
        if self._cache is not None:
            self._cache.append([value[0], value[1]])

    def clear(self):
        # réinitialiser à vide matérialise la sémantique
        self._cache = []
        self._removed.clear()
        self._added.clear()

    def extend(self, iterable: Iterable[List[int]]):
        for v in iterable:
            self.append(v)

    def copy(self) -> List[List[int]]:
        return list(self)


def initialiser_zones_terrain():
    """Initialise toutes les zones de jeu nécessaires au QIX"""
    zones = {
        # Zones principales
        'zone_safe': [],
        'zone_terrain': [],
        'zone_gauche': [],
        'zone_droite': [],
        'zone_haut': [],
        'zone_bas': [],
        
        # Zones de jeu
        'zone_obstacle': [],
        'zone_polygone': [],
        'zone_polygone_actuelle': [],
        'zone_safe_temp': [],
        'zone_pomme': [],
        
        # Coins et positions
        'coin': ZONE_COIN_DEFAUT.copy(),
        
        # Historiques et données temporaires
        'historique_positions': [],
        'historique_coin': [],
        'historique_virage': [],
        'historique_deplacement': [],
        'historique_zone_safe': [],
        'zone_safe_apres_tri': [],
        'coin_apres_tri': [],
        'trait_joueur_actuel': [],
        'position_qix': []
    }

    # stockage compact pour obstacles (conservé comme liste de tuples)
    zones['zone_obstacle'] = zones.get('zone_obstacle', [])

    # Génération des zones safe (bordures)
    _generer_zones_bordures(zones)

    # Pour la zone de terrain interne, utiliser un objet lazy `ZoneGrid`
    # qui implémente l'API d'une liste, mais n'alloue pas tout en mémoire
    # tant que des opérations aléatoires / mutantes ne sont pas requises.
    zones['zone_terrain'] = ZoneGrid(
        TERRAIN_X_MIN, TERRAIN_X_MAX, TERRAIN_Y_MIN, TERRAIN_Y_MAX, GRILLE_PAS
    )

    return zones


def _generer_zones_bordures(zones):
    """Génère les zones de bordures (zone safe) du terrain de jeu"""
    # Bordure gauche
    for i in range(0, TERRAIN_Y_MAX - TERRAIN_Y_MIN + GRILLE_PAS, GRILLE_PAS):
        position = [TERRAIN_X_MIN, TERRAIN_Y_MIN + i]
        zones['zone_safe'].append(position)
        zones['zone_gauche'].append(position)
    
    # Bordure droite
    for i in range(0, TERRAIN_Y_MAX - TERRAIN_Y_MIN + GRILLE_PAS, GRILLE_PAS):
        position = [TERRAIN_X_MAX, TERRAIN_Y_MIN + i]
        zones['zone_safe'].append(position)
        zones['zone_droite'].append(position)
    
    # Bordure haute
    for i in range(0, TERRAIN_X_MAX - TERRAIN_X_MIN, GRILLE_PAS):
        position = [TERRAIN_X_MIN + i, TERRAIN_Y_MIN]
        zones['zone_safe'].append(position)
        zones['zone_haut'].append(position)
    
    # Bordure basse
    for i in range(0, TERRAIN_X_MAX - TERRAIN_X_MIN + GRILLE_PAS, GRILLE_PAS):
        position = [TERRAIN_X_MIN + i, TERRAIN_Y_MAX]
        zones['zone_safe'].append(position)
        zones['zone_bas'].append(position)


def _generer_zone_terrain(zones):
    """Génère la zone de terrain interne où le joueur peut tracer
    (deprecated — kept for compatibility if code expects a concrete list).
    """
    for y in range(TERRAIN_Y_MIN, TERRAIN_Y_MAX, GRILLE_PAS):
        for x in range(TERRAIN_X_MIN, TERRAIN_X_MAX, GRILLE_PAS):
            zones['zone_terrain'].append([x, y])
