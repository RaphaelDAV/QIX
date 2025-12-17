# Profiling Report — QIX

## Objectif
Repérer et corriger les véritables problèmes de performance (temps d'exécution et mémoire), en suivant la démarche demandée : analyse statique, profiling CPU (global + ligne), profiling mémoire, optimiser une chose à la fois et re-mesurer.

## Environnement
- OS: Windows
- Python: environnement virtuel `.venv` (créé dans le workspace)
- Outils installés: `ruff`, `pylint`, `vulture`, `line_profiler`, `memory_profiler`

## Commandes utiles (exécution depuis la racine du projet)
- Créer venv et installer outils (déjà fait) :

```powershell
python -m venv .venv
.venv\Scripts\python.exe -m pip install --upgrade pip
.venv\Scripts\pip install ruff pylint vulture line_profiler memory_profiler
```

- Linter rapide (`ruff`) :

```powershell
.venv\Scripts\ruff.exe .
```

- Détecter code mort (`vulture`) :

```powershell
.venv\Scripts\vulture.exe . --min-confidence 60
```

- Pylint (exemples sur fichiers clefs) :

```powershell
.venv\Scripts\pylint.exe "managers\polygon_manager.py" "core\game_state.py" "QIX_Raphael_DAVIOT_&_Abdelrahim_RICHE.py" --score=n --exit-zero
```

- Profiling CPU (cProfile) — script fourni :

```powershell
$env:PYTHONPATH='C:\Users\riche\Desktop\Abdelrahim\QIX'
.venv\Scripts\python.exe profiling\run_cprofile_polygon.py
```

- Profiling ligne-à-ligne (`line_profiler`) — scripts fournis :

```powershell
$env:PYTHONPATH='C:\Users\riche\Desktop\Abdelrahim\QIX'
.venv\Scripts\python.exe profiling\run_line_profile_gen.py
```

- Profiling mémoire (memory_profiler) — script fourni :

```powershell
$env:PYTHONPATH='C:\Users\riche\Desktop\Abdelrahim\QIX'
.venv\Scripts\python.exe profiling\run_memory_profile_polygon.py
```

## Analyse statique (résumé)
- `vulture` a listé plusieurs fonctions/variables non utilisées; beaucoup viennent des packages installés (faux positifs attendus). Points projet :
  - `config/config.py` : fonction `ajouter_sparks_niveau` détectée inutilisée (à vérifier)
  - Plusieurs constantes dans `config/constants.py` marquées non utilisées (vérifier usages runtime)
  - Import inutilisé `configurer_joueur2` dans le fichier principal
- `pylint` signale des problèmes de style (lignes trop longues, whitespace, noms non snake_case) et structure (fonctions trop longues / trop de variables locales dans `QIX_Raphael...` et `polygon_manager`). Ce sont des améliorations de maintenance mais pas toutes critiques pour perf.

## Profiling CPU — découvertes
- Point de départ : exécution cProfile sur une version ciblée de la génération des positions intérieures d'un polygone (`PolygonManager.generer_positions_interieures`).
- Résultat initial (`cProfile` + `line_profiler`) :
  - `PolygonManager._est_point_dans_polygone` (test point-in-polygon appelé pour chaque point) était le goulot. Appels : ~10k appels, temps cumulé important (~1.4s dans test réduit, et le line_profiler initial a montré ~31s dans une exécution plus lourde).
  - Cause : algorithme naïf "test par point" qui pour chaque point du quadrillage itérait toutes les arêtes du polygone — O(N_points * N_edges).

## Optimisation appliquée (une seule modification, validée)
- Action : remplacer la méthode point-par-point par un algorithme de type "scanline fill" dans `PolygonManager.generer_positions_interieures`.
  - Pour chaque ligne `y` de la grille : calculer les intersections X entre la ligne et les arêtes du polygone, trier les intersections et remplir les intervalles par paire (alignés sur la grille). Complexité bien meilleure : O(N_edges * N_scanlines + N_fill).
- Fichier modifié : `managers/polygon_manager.py` (remplacement de la fonction `generer_positions_interieures`).

## Mesures après optimisation
- cProfile (script `profiling/run_cprofile_polygon.py`) : temps réduit de ~1.36s -> ~0.015s (sur workload d'exemple). Très nette amélioration.
- line_profiler : total time pour `generer_positions_interieures` est passé de ~24–31s à ~0.21s dans le même cas d'essai.
- memory_profiler : pic de mémoire observé ~41.6 MB (incluant overhead Python). Le scanline n'a pas augmenté significativement la mémoire peak pour la charge testée.

## Fichiers ajoutés
- `profiling/run_cprofile_polygon.py` — script de cProfile pour `generer_positions_interieures`.
- `profiling/run_line_profile_gen.py` — script line_profiler pour la méthode mise à jour.
- `profiling/run_memory_profile_polygon.py` — script memory_profiler (avec `if __name__ == '__main__'`).
- `PROFILING_README.md` — ce document.

## Commandes pour reproduire mes étapes (copier-coller)
```powershell
# créer venv & installer outils (si nécessaire)
python -m venv .venv
.venv\Scripts\python.exe -m pip install --upgrade pip
.venv\Scripts\pip install ruff pylint vulture line_profiler memory_profiler

# linting
.venv\Scripts\ruff.exe .
.venv\Scripts\vulture.exe . --min-confidence 60
.venv\Scripts\pylint.exe "managers\polygon_manager.py" --score=n --exit-zero

# CPU profiling
$env:PYTHONPATH='C:\Users\riche\Desktop\Abdelrahim\QIX'
.venv\Scripts\python.exe profiling\run_cprofile_polygon.py

# Line profiling
.venv\Scripts\python.exe profiling\run_line_profile_gen.py

# Memory profiling
.venv\Scripts\python.exe profiling\run_memory_profile_polygon.py
```