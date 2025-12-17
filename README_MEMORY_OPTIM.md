**Optimisation mémoire — projet QIX**

**Objectif :** Réduire la consommation mémoire là où c'est pertinent, sans dégrader les performances.

**Modifications appliquées**
- Ajout de `__slots__` aux classes modèles (réduction mémoire par instance) :
  - `models/player.py` — `Player`
  - `models/powerup.py` — `Powerup`
  - `models/qix.py` — `Qix`
  - `models/sparks.py` — `Sparks`
- Remplacement paresseux de la génération complète de la `zone_terrain` par un objet `ZoneGrid` (dans `utils/game_zones.py`).
  - `ZoneGrid` implémente l'API d'une liste (mutable) mais n'alloue la grille complète que si des opérations mutantes/accès aléatoires le nécessitent. Les tests d'appartenance (`in`) sont rapides et sans allocation.

**Pourquoi ces changements ?**
- `__slots__` empêche la création d'un `__dict__` par instance, économisant de la mémoire quand on crée beaucoup d'objets.
- `ZoneGrid` permet d'éviter d'allouer l'intégralité de la grille interne (`zone_terrain`) tant que le code ne demande pas la liste complète — utile pour les checks d'appartenance fréquents.

**Commandes pour reproduire les mesures (PowerShell)**
1. Activez l'environnement virtuel :

```powershell
& .\.venv\Scripts\Activate.ps1
```

2. Exécuter la comparaison automatisée (script qui exécute before/after et écrit les résultats dans ce README) :

```powershell
python .\profiling\compare_memory_profiles.py
```

3. (Optionnel) Exécuter manuellement le profil unique :

```powershell
# Baseline (clone HEAD)
git clone . profiling_before
& .\.venv\Scripts\python.exe .\profiling_before\profiling\run_memory_profile_qix.py

# Après optimisation (workspace courant)
& .\.venv\Scripts\python.exe .\profiling\run_memory_profile_qix.py
```

**Résultats mesurés localement**
- Baseline (HEAD clone) :
  - Current memory (MB): 1.152
  - Peak memory (MB): 1.155

- Après optimisation (`__slots__` + `ZoneGrid`) :
  - Current memory (MB): 1.144
  - Peak memory (MB): 1.146

**Fichiers ajoutés / modifiés importants**
- `utils/game_zones.py` : ajout de `ZoneGrid`, `zone_terrain` initialisé paresseusement.
- `models/*.py` : ajout de `__slots__` pour `Player`, `Powerup`, `Qix`, `Sparks`.
- `profiling/compare_memory_profiles.py` : script d'automatisation before/after.

---

Si vous voulez que j'exécute un benchmark plus lourd (par ex. `run_memory_profile_polygon.py`) ou que j'intègre d'autres optimisations, dites laquelle et je m'en occupe.
Optimisation mémoire — projet QIX

Objectif

- Réduire la consommation mémoire par instance là où c'est pertinent, sans dégrader les performances.

Modifications appliquées

- Ajout de `__slots__` aux classes modèles pour réduire l'empreinte mémoire par instance :
  - `models/player.py` — `Player`
  - `models/powerup.py` — `Powerup`
  - `models/qix.py` — `Qix`
  - `models/sparks.py` — `Sparks`

Pourquoi `__slots__` ?

- Empêche la création d'un `__dict__` par instance et donc réduit l'utilisation mémoire quand on instancie beaucoup d'objets.
- Changement sûr tant qu'on n'a pas besoin d'ajouter dynamiquement des attributs non déclarés.

Comment reproduire les mesures

1. Activez l'environnement virtuel (PowerShell) :

```powershell
& .\.venv\Scripts\Activate.ps1
```

2. Cloner la version HEAD actuelle (baseline "before") et exécuter le script de profiling mémoire :

```powershell
git clone . profiling_before
& .\.venv\Scripts\python.exe .\profiling_before\profiling\run_memory_profile_qix.py
```

3. Exécuter le script de profiling mémoire dans l'arbre courant (état "after") :

```powershell
& .\.venv\Scripts\python.exe .\profiling\run_memory_profile_qix.py
```

Résultats (exécutés localement)

- Baseline (HEAD clone) :
  - Current memory (MB): 1.152
  - Peak memory (MB): 1.155

- Après optimisation (`__slots__`) :
  - Current memory (MB): 1.144
  - Peak memory (MB): 1.146

---
Memory profile comparison (2025-12-17T16:24:57.193167):
Baseline - Current: 1.153 MB, Peak: 1.155 MB
Optimized - Current: 0.372 MB, Peak: 0.835 MB
Delta Current: 0.781000 MB, Delta Peak: 0.320000 MB

---
Memory profile comparison (2025-12-17T16:25:04.820030):
Baseline - Current: 1.144 MB, Peak: 1.146 MB
Optimized - Current: 0.105 MB, Peak: 0.107 MB
Delta Current: 1.039000 MB, Delta Peak: 1.039000 MB
