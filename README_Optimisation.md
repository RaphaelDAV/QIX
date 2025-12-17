# README — Optimisation, Profilage & Mémoire

## But

- Centraliser le compte-rendu des travaux d'optimisation réalisés sur le projet QIX (performance CPU et consommation mémoire).
- Documenter la méthodologie, les modifications appliquées, les fichiers affectés, les tests exécutés et les résultats mesurés.

## Environnement

- OS : Windows
- Python : environnement virtuel `.venv` (prévu à la racine du projet)
- Outils utilisés : `cProfile`, `line_profiler`, `memory_profiler`, `pstats`, `snakeviz`, `ruff`, `pylint`, `vulture`.

## Méthodologie

1. Mesurer avant d'optimiser : produire des profils CPU et mémoire (cProfile + line_profiler + memory_profiler).
2. Appliquer une optimisation ciblée (une chose à la fois).
3. Mesurer l'impact après modification.
4. Documenter les changements et les gains observés.

## Synthèse des optimisations réalisées

### 1) Optimisations de performance (CPU)

- Objectif : réduire le temps CPU sur les fonctions identifiées comme hotspots.
- Diagnostic principal : appels coûteux dus à des tests d'appartenance sur des listes (`[x,y] in zone`) et algorithmes quadratiques pour le remplissage interne des polygones.
- Modifications appliquées :
  - `managers/polygon_manager.py` : remplacement de l'approche naïve « test par point » par une méthode de type *scanline fill* dans `generer_positions_interieures`. Pour chaque ligne Y, on calcule les intersections avec les arêtes, on trie les X et on remplit les intervalles par paire (alignés sur la grille) — complexité grandement améliorée.
  - `models/sparks.py` : optimisation de `SparksManager.check_out_of_bounds` en pré-calculant une version `set` de `zone_safe` (lorsque pertinent) et en la passant aux instances `Sparks` pour éviter la reconstruction répétée d'une `set` par spark.

### 2) Optimisations mémoire

- Objectif : réduire l'empreinte mémoire sans dégrader les performances.
- Modifications appliquées :
  - Ajout de `__slots__` sur les classes modèles pour réduire la mémoire par instance :
    - `models/player.py` — `Player`
    - `models/powerup.py` — `Powerup`
    - `models/qix.py` — `Qix`
    - `models/sparks.py` — `Sparks`
  - Implémentation paresseuse de `zone_terrain` via `ZoneGrid` dans `utils/game_zones.py` : `ZoneGrid` implémente l'API d'une liste mutable mais n'alloue la grille complète que si des opérations mutantes/accès aléatoires sont nécessaires; les vérifications `in` restent rapides et sans allocation inutile.

## Fichiers modifiés (liste consolidée)

- `managers/polygon_manager.py` — nouvelle implémentation de `generer_positions_interieures` (scanline fill).
- `models/sparks.py` — optimisation `check_out_of_bounds` / passage d'un `set` pré-calculé.
- `utils/game_zones.py` — ajout / mise à jour de `ZoneGrid` (implémentation paresseuse).
- `models/player.py`, `models/powerup.py`, `models/qix.py`, `models/sparks.py` — ajout de `__slots__` sur les classes concernées.
- Scripts de profiling ajoutés / utilisés :
  - `profiling/run_cprofile_project.py`
  - `profiling/run_cprofile_polygon.py`
  - `profiling/run_line_profile_gen.py`
  - `profiling/run_line_profile_polygon.py`
  - `profiling/run_memory_profile_polygon.py`
  - `profiling/run_memory_profile_qix.py`
- Scripts d'automatisation :
  - `profiling/compare_memory_profiles.py` (comparaison before/after et écriture dans `README_MEMORY_OPTIM.md`).

## Tests exécutés et résultats mesurés

### Performance (exemples)

- Cas test (scanline vs naïf) : temps réduit significativement pour la génération des positions intérieures d'un polygone.
  - Exemple (workload d'exemple, run headless) : `generer_positions_interieures` — temps ramené de ~1.36s à ~0.015s sur le cas testé.
- Hotspots identifiés avant optimisation : `Sparks.is_out_of_bounds`, `QixManager._is_valid_qix_position`, `game_state.is_point_in_obstacle`.
- Impact mesuré (exemple de run headless 400 frames) après optimisation de `Sparks` : temps total observé réduit (ex. 0.223s → 0.175s dans un cas rapporté).

### Mémoire (exemples)

- Profils mémoire mesurés localement :
  - Baseline (avant optimisations) : Current ≈ 1.152 MB, Peak ≈ 1.155 MB
  - Après `__slots__` + `ZoneGrid` : Current ≈ 1.144 MB, Peak ≈ 1.146 MB
  - Des comparaisons supplémentaires figurent dans `README_MEMORY_OPTIM.md`.

## Reproduction (commandes PowerShell)

Activer l'environnement virtuel :

```powershell
& .\.venv\Scripts\Activate.ps1
```

Exécuter le profil CPU global (ex : polygon) :

```powershell
$env:PYTHONPATH = 'C:\chemin\vers\QIX'  # adapter si nécessaire
.venv\Scripts\python.exe profiling/run_cprofile_polygon.py
```

Exécuter le line profiler pour la génération des positions intérieures :

```powershell
.venv\Scripts\python.exe profiling/run_line_profile_gen.py
```

Exécuter le profiling mémoire pour le polygon ou le QIX :

```powershell
.venv\Scripts\python.exe profiling/run_memory_profile_polygon.py
.venv\Scripts\python.exe profiling/run_memory_profile_qix.py
```

Exécuter la comparaison automatique before/after (si `profiling_before` absent, il sera cloné) :

```powershell
.venv\Scripts\python.exe profiling/compare_memory_profiles.py
```

## Analyse détaillée et explications

- Cause principale des coûts CPU : tests d'appartenance sur des listes et algorithmes O(N_points * N_edges) pour le remplissage intérieur des polygones. Les structures de données inappropriées (listes pour des tests fréquents) entraînent des parcours O(n) coûteux.

- Remèdes appliqués :
  - Remplacer des tests répétitifs sur listes par des tests en O(1) via `set` lorsque possible (ex. : convertir `zone_safe` une seule fois et transmettre la `set` aux fonctions appelantes).
  - Remplacer le test point-à-point par une méthode scanline pour le remplissage des polygones.
  - Réduire l'empreinte mémoire par instance avec `__slots__` là où de nombreuses instances sont créées.
  - Éviter la matérialisation complète d'une grande grille (`zone_terrain`) tant que ce n'est pas nécessaire (implémentation paresseuse `ZoneGrid`).

## Limitations et remarques

- Les gains dépendent du workload de test : certains gains sont plus visibles en exécution headless ou sur scénarios fortement chargés.
- `__slots__` empêche l'ajout dynamique d'attributs non déclarés — vérifier les extensions dynamiques éventuelles avant d'ajouter `__slots__` sur d'autres classes.
- Certains outils de lint (`vulture`, `pylint`) ont fourni des pistes utiles mais peuvent générer des faux positifs; vérifier manuellement.

## Emplacement des documents de profiling et des résultats

- `profiling/project.prof` — fichier pstats (cProfile) pour le projet.
- `profiling/*` — scripts de profiling et résultats.