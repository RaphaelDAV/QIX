            README - Jeu QIX
----------------------------------------

**Auteur :** [Raphael Daviot et Nael AIT AISSI]

**Date de création :** [06/01/2024]

----------------------------------------

**Description du jeu :**

QIX est un jeu classique d'arcade où le joueur contrôle un carré qui doit remplir 75%de l'aire de jeu en dessinant des formes et par la même occasion evité l'objet nommer QIX qui ce deplace aléatoirement sur l'aire de jeu.

**Instructions :**

1. Utilisez les touches fléchées pour déplacer le carré.
2. Dessinez des formes à l'intérieur de l'aire de jeu en appuyant sur la barre espace lorsque vous êtes prêt à relier les bords.
3. Évitez de toucher le QIX en mouvement et les bordures de l'aire de jeu.
4. Votre objectif est de remplir 75% de l'aire de jeu sans vous faire toucher par le QIX
5. Il est possible d'activer et désactiver différentes fonctionnalités pour que chaque parties soient unique tel qu'un mode 2 joueurs, des obstacles, des bonus etc...

**Fonctionnalités du jeu :**

- Affichage du pourcentage de surface révélée.
- Affichage du "Game over" quand la partie est perdu.
- Affichage de "Gagné" avec votre score et la surface lorsque la partie est gagnée
- Système de vie.
- Système de score basé sur la surface révélée.
- Compteur de vies pour le joueur.
- Déplacement aléatoire du QIX pour créer un défi supplémentaire.
- Déplacement du joueur avec les fèches.
- Déplacement des sparks sur les ligne externes ainsi que les lignes internes
- dessin de polygone en fonction des lignes de déplacement du joueur
- Mise en place d'obstacle infranchissable pour le joueur
- Mise en place de bonus rendant invincible le joueur pendant 3 secondes
- Écran de démarrage permettant de lancer de jeu ou de le quitter
- Réappartition des sparks lorsque ces derniers se retrouvent bloqués
- Mise en place de l'activation et la désactivation des variantes suivantes à travers un menu juste avant de rentrer dans le jeu: scores, vitesses, obstacles, bonus, deux joueurs, sparks internes et niveaux
- 3 niveau de difficultés possibles, facile, moyen et difficle augmentant la vitesse du QIX et le nombre de sparks
- Mode 2 joueurs permettant à deux personnes de jouer en simultané l'un contre l'autre avec tout les variantes possiblement
- Les bonus offrent quelques secondes d'invincibilité au joueur qui l'a récupéré
- Si le mode 2 joueurs est activé, une interface différente est ouverte permettant de visualiser le score et le nombre de vie de chaque joueur
- Il est possible d'importer à l'aide d'un fichier texte les obstacles que vous souhaitez ainsi que la position des bonus
- Vous pouvez aussi changer les paramètres du QIX, du joueur et des sparks ainsi que de l'interface dans un autre fichier parametre.txt
- Possibilité d'enlever une vie à l'adversaire en l'enfermant
- Perte d'une vie si on croise le trait de l'adversaire 

**Installation :**

1. Assurez-vous d'avoir Python installé sur votre système.
2. Installez la bibliothèque FLTK pour Python si ce n'est pas déjà fait.
3. Exécutez le fichier du jeu pour lancer ce dernier ou executez le à travers le terminal
4. Veillez d'avoir toute les images du jeu dans le meme dossier que le fichier QIX.py


**Probèmes rencontrés:**

- Création des polygone a l'aide du chemin du joueur et former un polygone dans un angle.
- Aucuns problèmes pour la création d'un polygones mais impossibilité d'en créer un deuxième dans de bonnes conditions
- Limiter la zone de deplacement du QIX en fonction des zone(polygone) créé par le joueur.
- Pouvoir faire entrer les sparks dans les bordures des polygones crées par le joueur
- Faire en sorte que chaque fonction marche en simultanées.
- Faire en sorte que les sparks suivent les lignes sans bug
- Création du timer difficile pour le bonus
- Changement de groupe au cours du projet
- Imposibilité d'être invincible pendant 3 secondes



