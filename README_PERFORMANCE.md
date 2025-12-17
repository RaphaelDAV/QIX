# README — Performance / Profilage

But: Ce document rassemble les constats, commandes et recommandations pour profiler et améliorer les performances du projet QIX.

**But**: réduire le temps CPU de l'exécution en se basant sur des mesures, pas des micro-optimisations.

**Emplacement du profil**: `profiling/project.prof`

**Résumé rapide des constats**
- **Hotspots identifiés**: `Sparks.is_out_of_bounds` (conversions répétées), `QixManager._is_valid_qix_position` (tests d'appartenance répétés), `game_state.is_point_in_obstacle` (many repeated checks).
- **Cause fréquente**: tests d'appartenance réalisés sur des listes (`[x,y] in zone`) entraînant O(n) coûteux, et reconversions de listes en `set` répétées pour chaque appel.
- **Action immédiate appliquée**: optimisation sûre et localisée dans `models/sparks.py` — pré-calcul d'une version `set` de `zone_safe` dans `SparksManager.check_out_of_bounds` et passage de cette `set` à `Sparks.is_out_of_bounds` pour éviter de reconstruire la `set` par spark.
- **Impact mesuré**: dans un run headless de 400 frames, le temps total observé est passé d'environ `0.223s` → `0.175s` et le nombre d'appels totaux a diminué (ex. ~557k → ~387k) — gains significatifs pour une modification à faible risque.

**Comment reproduire le profil (PowerShell)**

- Positionnez-vous à la racine du projet (ex: `chemin_du_projet\QIX`).

```powershell
$env:PYTHONPATH = 'chemin_du_projet/QIX'
.venv\Scripts\python.exe profiling/run_cprofile_project.py
```

Le script va exécuter une version "headless" du jeu pendant `N_FRAMES` (défini dans `profiling/run_cprofile_project.py`) et produire `profiling/project.prof` ainsi qu'un résumé imprimé.

Pour afficher manuellement les 20 fonctions principales (cumulative time):

```powershell
.venv\Scripts\python.exe -c "from pstats import Stats; Stats('profiling/project.prof').strip_dirs().sort_stats('cumtime').print_stats(20)"
```

Pour trier par `tottime` (temps interne) :

```powershell
.venv\Scripts\python.exe -c "from pstats import Stats; s=Stats('profiling/project.prof'); s.strip_dirs().sort_stats('tottime').print_stats(20)"
```

Pour une inspection interactive plus riche, installez `snakeviz` et lancez :

```powershell
.venv\Scripts\python.exe -m pip install --user snakeviz
.venv\Scripts\python.exe -m snakeviz profiling/project.prof
```

**Commandes alternatives (tester PyPy)**
- Si vous avez `pypy3` installé, testez le même script pour voir le gain JIT minimal sans changer le code :

```powershell
# Exemple si pypy3 est dans le PATH
pypy3 profiling/run_cprofile_project.py
```

ou (chemin absolu) :

```powershell
& 'C:\chemin\vers\pypy3.exe' profiling/run_cprofile_project.py
```

Notes: PyPy peut améliorer sensiblement certaines portions (boucles, code Python pur) mais certains modules C-extension ou comportements spécifiques peuvent être incompatibles.

**Résumé des modifications apportées**
- `models/sparks.py` : `SparksManager.check_out_of_bounds` — pré-calcul d'une `set` pour `zone_safe` si la zone est suffisamment grande et passage de cette `set` en entrée à `Sparks.is_out_of_bounds`.
  - But: éviter la reconstruction répétée de la `set` pour chaque spark.
  - Risque: nul/minime (changement local, comportement inchangé).

**Recommandations priorisées (coût / bénéfice)**
- **(1) Convertir les tests fréquents en membership O(1)**: remplacer les occurrences ` [x,y] in zone ` par `tuple(x,y) in zone_set` quand possible.
  - Implémentation: maintenir pour chaque zone une version `set(map(tuple, zone))` mise à jour quand la zone change.
- **(2) Uniformiser la conversion set**: utiliser `set(map(tuple, zone))` (plus clair et légèrement plus rapide que `set((p[0], p[1]) for p in zone)`).
- **(3) Optimiser `is_point_in_obstacle`**: actuellement itère sur tous les obstacles; si beaucoup d'obstacles, utiliser une grille spatiale (buckets) pour réduire le nombre de tests.
- **(4) Réduire la résolution des tests**: si la logique de collision le permet, tester moins de points (ex: pas chaque pixel, mais par `GRILLE_PAS`).
- **(5) Tester PyPy**: faible coût d'essai, potentiels gains JIT sans modifier le code.
- **(6) Mesure continue**: intégrer un petit script `profiling/run_cprofile_project.py` (existant) dans votre workflow pour tester l'impact de chaque changement.

**Prochaines étapes suggérées**
- Option rapide (je peux appliquer): convertir les autres reconversions répétées en `set(map(tuple, zone))` et propager l'utilisation de `zone_set` aux autres managers.
- Option moyenne: ajouter une structure `ZoneCache` dans `core/game_state.py` qui expose `get_zone_set(name)` et s'assure que les sets sont invalidés quand la zone est modifiée.
- Option avancée: prototype d'un index spatial pour obstacles et tests de collision (benchmark avant/après).

**Notes pratiques / pièges**
- Les caches basés sur `id(obj), len(obj)` (comme dans `QixManager`) sont une bonne approche simple mais fragile si la zone est modifiée in-place sans changement de longueur; il faut invalider le cache dans ces cas.
- Attention à l'utilisation de `lru_cache` sur des fonctions qui reçoivent des structures mutables (list/dict) — il faut s'assurer que les clés sont immuables ou utiliser des décorateurs personnalisés.

**Fichiers pertinents**
- `profiling/run_cprofile_project.py` : script headless pour générer `profiling/project.prof`.
- `profiling/project.prof` : dernier profil enregistré (binaire pstats).
- `models/sparks.py` : optimisation appliquée.
- `managers/qix_manager.py` & `core/game_state.py` : zones de priorité pour prochaines optimisations.
