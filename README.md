Ce dépôt contient deux versions du jeu QIX (dossier `avant` et `après`) et des scripts/ressources
pour comparer performance et mémoire.

**But**
- Optimiser l'ancienne version du jeu Qix
- Reproduire les profils mémoire et linéaires (line profiler) pour les versions `avant` et `après`.

Prérequis
- Python 3.8+ (ou l'interpréteur utilisé par votre venv)
- venv recommandé : activez votre environnement avant d'exécuter les commandes
- Outils utiles : `memory_profiler` (mprof), `line_profiler` (kernprof + line_profiler)

Installation rapide
```powershell
python -m pip install --user pip
pip install virtualenv
python -m virtualenv .venv
. .venv\Scripts\Activate.ps1   # PowerShell
pip install -r requirements.txt
pip install memory_profiler line_profiler
```

Profilage mémoire (mprof)
- Avant (dossier `avant`) :
```powershell
cd ./avant
mprof run -o "..\stats\avant\mprofile.dat" --include-children python .\QIX_Raphael_DAVIOT_Nael_AIT_AISSI.py
```
Ensuite, pour extraire quelques statistiques depuis la donnée enregistrée :
```powershell
cd ..
python - <<'PY'
from pathlib import Path
import statistics
p = Path('stats\avant\mprofile.dat')
s = p.read_text()
vals = [float(l.split()[1]) for l in s.splitlines() if l.startswith('MEM')]
print('samples', len(vals))
print('max', max(vals))
print('mean', statistics.mean(vals))
print('last', vals[-1])
PY
```

- Après (dossier `après`) :
```powershell
cd ./après
mprof run -o "..\stats\après\mprofile_apres.dat" --include-children python .\QIX_Raphael_DAVIOT_Abdelrahim_RICHE.py
```
Puis analyser de la même façon en adaptant le chemin vers `stats\après\mprofile_apres.dat`.

Profilage linéaire (line_profiler)
Remarque : `line_profiler` ne collecte des métriques que pour les fonctions décorées par `@profile`.

- Avant :
```powershell
cd ./avant
python -m kernprof -l -v .\QIX_Raphael_DAVIOT_Nael_AIT_AISSI.py
python -m line_profiler .\QIX_Raphael_DAVIOT_Nael_AIT_AISSI.py.lprof > stats\avant\line_profile.txt
```

- Après :
```powershell
cd ./après
python -m kernprof -l -v .\QIX_Raphael_DAVIOT_Abdelrahim_RICHE.py
python -m line_profiler .\QIX_Raphael_DAVIOT_Abdelrahim_RICHE.py.lprof > stats\après\line_profile.txt
```

Conseils pratiques
- Si votre rapport line_profiler contient seulement "Timer unit..." et rien d'autre, cela signifie
	que `@profile` n'a pas été appliqué aux fonctions exécutées — ajoutez `@profile` aux fonctions ciblées
	ou utilisez le shim already présent pour exécuter sans erreur.
- Utilisez `Get-ChildItem -Path . -Filter *.lprof -Recurse` (PowerShell) pour retrouver rapidement le `.lprof` généré.
- Pour exécuter les commandes depuis la racine du dépôt, ajustez les chemins (`avant\...` ou `après\...`).

Ressources
- memory_profiler: https://pypi.org/project/memory-profiler/
- line_profiler (kernprof): https://pypi.org/project/line-profiler/

Si vous voulez, je peux :
- lancer les commandes `kernprof` + `line_profiler` pour l'une des versions et sauvegarder le rapport dans `stats` (indiquez `avant` ou `après`),
- ou générer une version PDF/HTML du rapport.
