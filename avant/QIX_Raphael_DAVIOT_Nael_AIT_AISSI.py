# -----------------------------------------Définition des libraries-----------------------------------------------sparks31

from fltk import *
from time import *
from random import *
from math import *
import os.path


# ----------------------------------------Paramètres des personnages et des sparks-------------------------------------------------
def joueur1(x, y, cote, sprite):
    image(x + 5, y + 5, sprite, largeur=cote + 5, hauteur=cote + 5, tag="joueur1")


def joueur2(x, y, cote, sprite):
    image(x + 5, y + 5, sprite, largeur=cote + 5, hauteur=cote + 5, tag="joueur2")


def sparks1(cxsparks1, cysparks1, taille, sprite):
    image(
        cxsparks1,
        cysparks1,
        sprite,
        largeur=taille + 5,
        hauteur=taille + 5,
        tag="sparks1",
    )


def sparks2(cxsparks2, cysparks2, taille, sprite):
    image(
        cxsparks2,
        cysparks2,
        sprite,
        largeur=taille + 5,
        hauteur=taille + 5,
        tag="sparks2",
    )


def sparks3(cxsparks3, cysparks3, taille, sprite):
    image(
        cxsparks3,
        cysparks3,
        sprite,
        largeur=taille + 5,
        hauteur=taille + 5,
        tag="sparks3",
    )


def sparks4(cxsparks4, cysparks4, taille, sprite):
    image(
        cxsparks4,
        cysparks4,
        sprite,
        largeur=taille + 5,
        hauteur=taille + 5,
        tag="sparks4",
    )


def sparks5(cxsparks5, cysparks5, taille, sprite):
    image(
        cxsparks5,
        cysparks5,
        sprite,
        largeur=taille + 5,
        hauteur=taille + 5,
        tag="sparks5",
    )


def sparks6(cxsparks6, cysparks6, taille, sprite):
    image(
        cxsparks6,
        cysparks6,
        sprite,
        largeur=taille + 5,
        hauteur=taille + 5,
        tag="sparks6",
    )


# ---------------------------------------Paramètres de la fenêtre---------------------------------------------------
def fenetre():
    with open("ressources/parametres.txt", "r") as fichier:
        # Lire toutes les lignes dans une liste
        lignes = fichier.readlines()

        # Utiliser une comprehension de liste pour appliquer strip() a chaque �l�ment
        lignes = [element.strip() for element in lignes]
    # on configure la taille de la fenetre et l'aire de jeu avec le fichier paramatres.txt
    largeurFenetre = int(lignes[2])
    hauteurFenetre = int(lignes[3])

    if deux == True:
        largeurFenetre = int(lignes[2]) * 1.5
    # Aire
    x, y, xb, yb = int(lignes[7]), int(lignes[8]), int(lignes[9]), int(lignes[10])

    cree_fenetre(largeurFenetre, hauteurFenetre)
    rectangle(0, 0, largeurFenetre, hauteurFenetre, "white", "black", 10)
    image(
        300,
        400,
        "ressources/background3.png",
        largeur=largeurFenetre,
        hauteur=hauteurFenetre,
    )
    rectangle(x, y, xb, yb, "midnightblue", "black", 3)

    if deux == False:
        texte(
            230,
            80,
            "CLAIMED",
            couleur="white",
            taille=20,
            police="Copperplate Gothic Bold",
        )
        texte(
            315,
            110,
            "75 %",
            couleur="white",
            taille=16,
            police="Copperplate Gothic Bold",
        )
        texte(
            270, 110, "%", couleur="white", taille=16, police="Copperplate Gothic Bold"
        )
        texte(
            235,
            110,
            "0",
            couleur="white",
            taille=16,
            police="Copperplate Gothic Bold",
            tag="score_pourcentage",
        )

    if deux == False:
        texte(
            60, 75, "QIX", couleur="white", taille=45, police="Copperplate Gothic Bold"
        )
        texte(
            420,
            80,
            "SCORE",
            couleur="white",
            taille=20,
            police="Copperplate Gothic Bold",
        )
        texte(
            270, 110, "%", couleur="white", taille=16, police="Copperplate Gothic Bold"
        )
    if scorev == False and deux == False:
        texte(
            420,
            110,
            "X",
            couleur="white",
            taille=16,
            police="Copperplate Gothic Bold",
            tag="score_total",
        )

    if scorev == True and deux == False:
        texte(
            420,
            110,
            "0",
            couleur="white",
            taille=16,
            police="Copperplate Gothic Bold",
            tag="score_total",
        )

    cercle(545, 90, 5, "red", "red", tag="coeur1")
    cercle(545, 105, 5, "red", "red", tag="coeur2")
    cercle(545, 120, 5, "red", "red", tag="coeur3")

    texte(
        300,
        770,
        "Appuyez sur ECHAP pour quitter",
        couleur="white",
        taille=15,
        police="Copperplate Gothic Bold",
        ancrage="center",
    )


# ------------------------------------Définition des zones-----------------------------------------
historique_positions = []
historique_coin = []
historique_sparks1 = ["Gauche"]
historique_sparks2 = ["Droite"]
historique_sparks3 = ["Bas"]
historique_sparks4 = ["Bas"]
historique_sparks5 = ["Gauche"]
historique_sparks6 = ["Droite"]
historique_virage = []
lst_couleur = [
    "red",
    "green",
    "blue",
    "cyan",
    "magenta",
    "yellow",
    "brown",
    "orange",
    "pink",
    "purple",
    "burlywood",
    "cadetblue",
    "chartreuse",
    "chocolate",
    "coral",
    "cornflowerblue",
    "cornsilk",
    "darkorange",
    "darkseagreen",
    "darkturquoise",
    "deepskyblue",
    "dodgerblue",
    "goldenrod",
    "hotpink",
    "khaki",
    "lightcoral",
    "lightpink",
    "lightsalmon",
    "lightseagreen",
]
trait_joueur_actuel = []
zone_safe = []
zone_safe_temp = []
zone_obstacle = []
zone_polygone = []
zone_polygone_actuelle = []
zone_terrain = []
zone_bas = []
zone_haut = []
zone_gauche = []
zone_droite = []
zone_pomme = []
position_qix = []
coin_apres_tri = []
historique_deplacement = []
coin = [[50, 200], [550, 200], [550, 750], [50, 750]]
historique_zone_safe = []
zone_safe_apres_tri = []

for i in range(0, 550, 5):
    zone_safe.append([50, 200 + i])
    zone_gauche.append([50, 200 + i])
for i in range(0, 550, 5):
    zone_safe.append([550, 200 + i])
    zone_droite.append([550, 200 + i])
for i in range(0, 500, 5):
    zone_safe.append([50 + i, 200])
    zone_haut.append([50 + i, 200])
for i in range(0, 505, 5):
    zone_safe.append([50 + i, 750])
    zone_bas.append([50 + i, 750])

for i in range(200, 750, 5):
    for k in range(50, 550, 5):
        zone_terrain.append([k, i])


def Accueil():
    """
    Cree un menu d'accueil avec un bouton jouer et un bouton quitter. Renvoie True si on appuie sur jouer et False si on appuie sur quitter
    """
    # Cree une fenetre de 800x600 pixels
    cree_fenetre(800, 600)

    while True:
        # Efface le contenu precedent
        efface_tout()

        # Fond en gris
        rectangle(
            0,
            0,
            largeur_fenetre(),
            hauteur_fenetre(),
            couleur="black",
            remplissage="black",
        )
        image(
            400,
            280,
            "ressources/background.png",
            largeur=largeur_fenetre(),
            hauteur=hauteur_fenetre(),
        )

        # Titre en tant qu'image
        # Image du titre
        x_titre = 400
        y_titre = 100
        image(x_titre, y_titre, "ressources/Titre.png", largeur=300, hauteur=120)
        image(600, 400, "ressources/Bonhomme.png", largeur=320, hauteur=170)
        image(400, 550, "ressources/prenom.png", largeur=500, hauteur=30)

        # Bouton "Nouvelle Partie" en bleu
        largeur_bouton = 250
        hauteur_bouton = 50
        x_bouton_nouvelle_partie = (largeur_fenetre() - largeur_bouton) / 2
        y_bouton_nouvelle_partie = 220
        rectangle(
            x_bouton_nouvelle_partie,
            y_bouton_nouvelle_partie,
            x_bouton_nouvelle_partie + largeur_bouton,
            y_bouton_nouvelle_partie + hauteur_bouton,
            couleur="midnightblue",
            epaisseur=7,
        )
        texte(
            largeur_fenetre() / 2,
            y_bouton_nouvelle_partie + hauteur_bouton / 2,
            "Nouvelle Partie",
            couleur="white",
            police="Helvetica",
            taille=24,
            ancrage="center",
        )

        # Bouton "Quitter" en rouge
        x_bouton_quitter = (largeur_fenetre() - largeur_bouton) / 2
        y_bouton_quitter = 300
        rectangle(
            x_bouton_quitter,
            y_bouton_quitter,
            x_bouton_quitter + largeur_bouton,
            y_bouton_quitter + hauteur_bouton,
            couleur="red4",
            epaisseur=5,
        )
        texte(
            largeur_fenetre() / 2,
            y_bouton_quitter + hauteur_bouton / 2,
            "Quitter",
            couleur="white",
            police="Helvetica",
            taille=24,
            ancrage="center",
        )

        # Attente d'un clic
        x, y = attend_clic_gauche()

        # Verifie si le clic est sur "Nouvelle Partie"
        if (
            x_bouton_nouvelle_partie <= x <= x_bouton_nouvelle_partie + largeur_bouton
            and y_bouton_nouvelle_partie
            <= y
            <= y_bouton_nouvelle_partie + hauteur_bouton
        ):
            ferme_fenetre()
            return True

        # Verifie si le clic est sur "Quitter"
        if (
            x_bouton_quitter <= x <= x_bouton_quitter + largeur_bouton
            and y_bouton_quitter <= y <= y_bouton_quitter + hauteur_bouton
        ):
            ferme_fenetre()
            return False


def variantes():
    """
    Cree un menu d'accueil avec un bouton jouer et un bouton quitter. Renvoie True si on appuie sur jouer et False si on appuie sur quitter
    """
    # Cree une fenetre de 800x600 pixels
    cree_fenetre(900, 700)

    while True:
        # Efface le contenu precedent
        efface_tout()

        # Fond en gris

        rectangle(
            0,
            0,
            largeur_fenetre(),
            hauteur_fenetre(),
            couleur="black",
            remplissage="black",
        )
        image(
            450,
            330,
            "ressources/background2.png",
            largeur=largeur_fenetre(),
            hauteur=hauteur_fenetre(),
        )

        largeur_bouton = 200
        hauteur_bouton = 50

        x_bouton_score = 50
        y_bouton_score = 100
        rectangle(
            x_bouton_score,
            y_bouton_score,
            x_bouton_score + largeur_bouton,
            y_bouton_score + hauteur_bouton,
            couleur="yellow",
            epaisseur=5,
            tag="score",
        )
        texte(
            x_bouton_score + 100,
            y_bouton_score + 25,
            "Score",
            couleur="white",
            police="Helvetica",
            taille=20,
            ancrage="center",
            tag="score",
        )

        x_bouton_vitesse = 350
        y_bouton_vitesse = 100
        rectangle(
            x_bouton_vitesse,
            y_bouton_vitesse,
            x_bouton_vitesse + largeur_bouton,
            y_bouton_vitesse + hauteur_bouton,
            couleur="yellow",
            epaisseur=5,
            tag="vitesse",
        )
        texte(
            x_bouton_vitesse + 100,
            y_bouton_vitesse + 25,
            "Vitesse",
            couleur="white",
            police="Helvetica",
            taille=20,
            ancrage="center",
            tag="vitesse",
        )

        x_bouton_obstacle = 650
        y_bouton_obstacle = 100
        rectangle(
            x_bouton_obstacle,
            y_bouton_obstacle,
            x_bouton_obstacle + largeur_bouton,
            y_bouton_obstacle + hauteur_bouton,
            couleur="yellow",
            epaisseur=5,
            tag="obstacle",
        )
        texte(
            x_bouton_obstacle + 100,
            y_bouton_obstacle + 25,
            "Obstacles",
            couleur="white",
            police="Helvetica",
            taille=20,
            ancrage="center",
            tag="obstacle",
        )

        x_bouton_obstacle_aleatoire = 650  # Pour les obstacles aléatoires
        y_bouton_obstacle_aleatoire = 170

        x_bouton_obstacle_predefini = 760  # Pour les obstacles prédéfinis
        y_bouton_obstacle_predefini = 170

        x_bouton_bonus = 50
        y_bouton_bonus = 300
        rectangle(
            x_bouton_bonus,
            y_bouton_bonus,
            x_bouton_bonus + largeur_bouton,
            y_bouton_bonus + hauteur_bouton,
            couleur="yellow",
            epaisseur=5,
            tag="bonus",
        )
        texte(
            x_bouton_bonus + 100,
            y_bouton_bonus + 25,
            "Bonus",
            couleur="white",
            police="Helvetica",
            taille=20,
            ancrage="center",
            tag="bonus",
        )

        x_bouton_bonus_aleatoire = 50  # Pour les bonus aléatoires
        y_bouton_bonus_aleatoire = 370

        x_bouton_bonus_predefini = 160  # Pour les bonus prédéfinis
        y_bouton_bonus_predefini = 370

        x_bouton_2 = 350
        y_bouton_2 = 300
        rectangle(
            x_bouton_2,
            y_bouton_2,
            x_bouton_2 + largeur_bouton,
            y_bouton_2 + hauteur_bouton,
            couleur="yellow",
            epaisseur=5,
            tag="deux",
        )
        texte(
            x_bouton_2 + 100,
            y_bouton_2 + 25,
            "2 joueurs",
            couleur="white",
            police="Helvetica",
            taille=20,
            ancrage="center",
            tag="deux",
        )

        x_bouton_niveau = 650
        y_bouton_niveau = 300
        rectangle(
            x_bouton_niveau,
            y_bouton_niveau,
            x_bouton_niveau + largeur_bouton,
            y_bouton_niveau + hauteur_bouton,
            couleur="yellow",
            epaisseur=5,
            tag="niveau",
        )
        texte(
            x_bouton_niveau + 100,
            y_bouton_niveau + 25,
            "Niveaux",
            couleur="white",
            police="Helvetica",
            taille=20,
            ancrage="center",
            tag="niveau",
        )

        x_choix_niveau1 = 650  # Pour le niveau 1
        y_choix_niveau1 = 370
        x_choix_niveau2 = 725  # Pour le niveau 2
        y_choix_niveau2 = 370
        x_choix_niveau3 = 800  # Pour le niveau 3
        y_choix_niveau3 = 370

        image(480, 470, "ressources/pacman_fantome.png", 900, 550)

        x_bouton_nouvelle_partie = 250
        y_bouton_nouvelle_partie = 550
        rectangle(
            x_bouton_nouvelle_partie,
            y_bouton_nouvelle_partie,
            x_bouton_nouvelle_partie + largeur_bouton,
            y_bouton_nouvelle_partie + hauteur_bouton,
            couleur="midnightblue",
            epaisseur=7,
        )
        texte(
            x_bouton_nouvelle_partie + 100,
            y_bouton_nouvelle_partie + 25,
            "Nouvelle Partie",
            couleur="white",
            police="Helvetica",
            taille=20,
            ancrage="center",
        )

        x_bouton_quitter = 500
        y_bouton_quitter = 550
        rectangle(
            x_bouton_quitter,
            y_bouton_quitter,
            x_bouton_quitter + largeur_bouton,
            y_bouton_quitter + hauteur_bouton,
            couleur="red4",
            epaisseur=5,
        )
        texte(
            x_bouton_quitter + 100,
            y_bouton_quitter + 25,
            "Quitter",
            couleur="white",
            police="Helvetica",
            taille=20,
            ancrage="center",
        )

        start = 0
        scorev = False
        vitesse = False
        obstacle = False
        bonus = False
        deux = False
        niveau = False
        obstacle_aleatoire = False
        obstacle_predefini = False
        niveau1 = False
        niveau2 = False
        niveau3 = False
        bonus_aleatoire = False
        bonus_predefini = False

        while start != True:
            x, y = attend_clic_gauche()
            clic = False

            # Score
            if (
                x_bouton_score <= x <= x_bouton_score + largeur_bouton
                and y_bouton_score <= y <= y_bouton_score + hauteur_bouton
                and scorev == False
                and clic == False
            ):
                clic = True
                scorev = True
                efface("score")
                rectangle(
                    x_bouton_score,
                    y_bouton_score,
                    x_bouton_score + largeur_bouton,
                    y_bouton_score + hauteur_bouton,
                    couleur="green",
                    remplissage="green",
                    tag="score",
                )
                texte(
                    x_bouton_score + 100,
                    y_bouton_score + 25,
                    "Score",
                    couleur="white",
                    police="Helvetica",
                    taille=20,
                    ancrage="center",
                    tag="score",
                )
            if (
                x_bouton_score <= x <= x_bouton_score + largeur_bouton
                and y_bouton_score <= y <= y_bouton_score + hauteur_bouton
                and scorev == True
                and clic == False
            ):
                clic = True
                scorev = False
                efface("score")
                rectangle(
                    x_bouton_score,
                    y_bouton_score,
                    x_bouton_score + largeur_bouton,
                    y_bouton_score + hauteur_bouton,
                    couleur="yellow",
                    epaisseur=5,
                    tag="score",
                )
                texte(
                    x_bouton_score + 100,
                    y_bouton_score + 25,
                    "Score",
                    couleur="white",
                    police="Helvetica",
                    taille=20,
                    ancrage="center",
                    tag="score",
                )

            # Vitesse
            if (
                x_bouton_vitesse <= x <= x_bouton_vitesse + largeur_bouton
                and y_bouton_vitesse <= y <= y_bouton_vitesse + hauteur_bouton
                and vitesse == False
                and clic == False
            ):
                clic = True
                vitesse = True
                efface("vitesse")
                rectangle(
                    x_bouton_vitesse,
                    y_bouton_vitesse,
                    x_bouton_vitesse + largeur_bouton,
                    y_bouton_vitesse + hauteur_bouton,
                    couleur="midnightblue",
                    remplissage="midnightblue",
                    tag="vitesse",
                )
                texte(
                    x_bouton_vitesse + 100,
                    y_bouton_vitesse + 25,
                    "Vitesse",
                    couleur="white",
                    police="Helvetica",
                    taille=20,
                    ancrage="center",
                    tag="vitesse",
                )
            if (
                x_bouton_vitesse <= x <= x_bouton_vitesse + largeur_bouton
                and y_bouton_vitesse <= y <= y_bouton_vitesse + hauteur_bouton
                and vitesse == True
                and clic == False
            ):
                clic = True
                vitesse = False
                efface("vitesse")
                rectangle(
                    x_bouton_vitesse,
                    y_bouton_vitesse,
                    x_bouton_vitesse + largeur_bouton,
                    y_bouton_vitesse + hauteur_bouton,
                    couleur="yellow",
                    epaisseur=5,
                    tag="vitesse",
                )
                texte(
                    x_bouton_vitesse + 100,
                    y_bouton_vitesse + 25,
                    "Vitesse",
                    couleur="white",
                    police="Helvetica",
                    taille=20,
                    ancrage="center",
                    tag="vitesse",
                )

            # Obstacle
            if (
                x_bouton_obstacle <= x <= x_bouton_obstacle + largeur_bouton
                and y_bouton_obstacle <= y <= y_bouton_obstacle + hauteur_bouton
                and obstacle == False
                and clic == False
            ):
                clic = True
                obstacle = True
                obstacle_aleatoire = False
                obstacle_predefini = True
                efface("obstacle")
                rectangle(
                    x_bouton_obstacle,
                    y_bouton_obstacle,
                    x_bouton_obstacle + largeur_bouton,
                    y_bouton_obstacle + hauteur_bouton,
                    couleur="orange",
                    remplissage="orange",
                    tag="obstacle",
                )
                texte(
                    x_bouton_obstacle + 100,
                    y_bouton_obstacle + 25,
                    "Obstacle",
                    couleur="white",
                    police="Helvetica",
                    taille=20,
                    ancrage="center",
                    tag="obstacle",
                )

                x_bouton_obstacle_aleatoire = 650  # Pour les obstacles aléatoires
                y_bouton_obstacle_aleatoire = 170
                rectangle(
                    x_bouton_obstacle_aleatoire,
                    y_bouton_obstacle_aleatoire,
                    x_bouton_obstacle_aleatoire + 90,
                    y_bouton_obstacle_aleatoire + 50,
                    couleur="gray",
                    remplissage="gray",
                    tag="obstacle_aleatoire",
                )
                texte(
                    x_bouton_obstacle_aleatoire + 45,
                    y_bouton_obstacle_aleatoire + 25,
                    "Prédefinis",
                    couleur="black",
                    police="Helvetica",
                    taille=13,
                    ancrage="center",
                    tag="obstacle_aleatoire",
                )

                x_bouton_obstacle_predefini = 760  # Pour les obstacles prédéfinis
                y_bouton_obstacle_predefini = 170
                rectangle(
                    x_bouton_obstacle_predefini,
                    y_bouton_obstacle_predefini,
                    x_bouton_obstacle_predefini + 90,
                    y_bouton_obstacle_predefini + 50,
                    couleur="green",
                    remplissage="green",
                    tag="obstacle_predefini",
                )
                texte(
                    x_bouton_obstacle_predefini + 45,
                    y_bouton_obstacle_predefini + 25,
                    "Aléatoires",
                    couleur="black",
                    police="Helvetica",
                    taille=13,
                    ancrage="center",
                    tag="obstacle_predefini",
                )

            if (
                x_bouton_obstacle_aleatoire <= x <= x_bouton_obstacle_aleatoire + 90
                and y_bouton_obstacle_aleatoire <= y <= y_bouton_obstacle_aleatoire + 50
                and obstacle_predefini == True
                and clic == False
                and obstacle == True
            ):
                clic = True
                obstacle_aleatoire = True
                obstacle_predefini = False
                efface("obstacle_aleatoire")
                rectangle(
                    x_bouton_obstacle_aleatoire,
                    y_bouton_obstacle_aleatoire,
                    x_bouton_obstacle_aleatoire + 90,
                    y_bouton_obstacle_aleatoire + 50,
                    couleur="green",
                    remplissage="green",
                    tag="obstacle_aleatoire",
                )
                texte(
                    x_bouton_obstacle_aleatoire + 45,
                    y_bouton_obstacle_aleatoire + 25,
                    "Prédefinis",
                    couleur="black",
                    police="Helvetica",
                    taille=13,
                    ancrage="center",
                    tag="obstacle_aleatoire",
                )
                efface("obstacle_predefini")
                rectangle(
                    x_bouton_obstacle_predefini,
                    y_bouton_obstacle_predefini,
                    x_bouton_obstacle_predefini + 90,
                    y_bouton_obstacle_predefini + 50,
                    couleur="gray",
                    remplissage="gray",
                    tag="obstacle_predefini",
                )
                texte(
                    x_bouton_obstacle_predefini + 45,
                    y_bouton_obstacle_predefini + 25,
                    "Aléatoires",
                    couleur="black",
                    police="Helvetica",
                    taille=13,
                    ancrage="center",
                    tag="obstacle_predefini",
                )

            if (
                x_bouton_obstacle_predefini <= x <= x_bouton_obstacle_predefini + 90
                and y_bouton_obstacle_predefini <= y <= y_bouton_obstacle_predefini + 50
                and obstacle_aleatoire == True
                and clic == False
                and obstacle == True
            ):
                clic = True
                obstacle_aleatoire = False
                obstacle_predefini = True
                efface("obstacle_predefini")
                rectangle(
                    x_bouton_obstacle_predefini,
                    y_bouton_obstacle_predefini,
                    x_bouton_obstacle_predefini + 90,
                    y_bouton_obstacle_predefini + 50,
                    couleur="green",
                    remplissage="green",
                    tag="obstacle_predefini",
                )
                texte(
                    x_bouton_obstacle_predefini + 45,
                    y_bouton_obstacle_predefini + 25,
                    "Aléatoires",
                    couleur="black",
                    police="Helvetica",
                    taille=13,
                    ancrage="center",
                    tag="obstacle_predefini",
                )
                efface("obstacle_aleatoire")
                rectangle(
                    x_bouton_obstacle_aleatoire,
                    y_bouton_obstacle_aleatoire,
                    x_bouton_obstacle_aleatoire + 90,
                    y_bouton_obstacle_aleatoire + 50,
                    couleur="gray",
                    remplissage="gray",
                    tag="obstacle_aleatoire",
                )
                texte(
                    x_bouton_obstacle_aleatoire + 45,
                    y_bouton_obstacle_aleatoire + 25,
                    "Prédefinis",
                    couleur="black",
                    police="Helvetica",
                    taille=13,
                    ancrage="center",
                    tag="obstacle_aleatoire",
                )

            if (
                x_bouton_obstacle <= x <= x_bouton_obstacle + largeur_bouton
                and y_bouton_obstacle <= y <= y_bouton_obstacle + hauteur_bouton
                and obstacle == True
                and clic == False
            ):
                clic = True
                obstacle = False
                obstacle_predefini = False
                obstacle_aleatoire = False
                efface("obstacle")
                efface("obstacle_aleatoire")
                efface("aleatoire")
                efface("obstacle_predefini")
                efface("predefini")
                rectangle(
                    x_bouton_obstacle,
                    y_bouton_obstacle,
                    x_bouton_obstacle + largeur_bouton,
                    y_bouton_obstacle + hauteur_bouton,
                    couleur="yellow",
                    epaisseur=5,
                    tag="obstacle",
                )
                texte(
                    x_bouton_obstacle + 100,
                    y_bouton_obstacle + 25,
                    "Obstacle",
                    couleur="white",
                    police="Helvetica",
                    taille=20,
                    ancrage="center",
                    tag="obstacle",
                )

            # Bonus
            if (
                x_bouton_bonus <= x <= x_bouton_bonus + largeur_bouton
                and y_bouton_bonus <= y <= y_bouton_bonus + hauteur_bouton
                and bonus == False
                and clic == False
            ):
                clic = True
                bonus = True
                bonus_aleatoire = False
                bonus_predefini = True
                efface("bonus")
                rectangle(
                    x_bouton_bonus,
                    y_bouton_bonus,
                    x_bouton_bonus + largeur_bouton,
                    y_bouton_bonus + hauteur_bouton,
                    couleur="purple",
                    remplissage="purple",
                    tag="bonus",
                )
                texte(
                    x_bouton_bonus + 100,
                    y_bouton_bonus + 25,
                    "Bonus",
                    couleur="white",
                    police="Helvetica",
                    taille=20,
                    ancrage="center",
                    tag="bonus",
                )

                x_bouton_bonus_aleatoire = 50  # Pour les bonus aléatoires
                y_bouton_bonus_aleatoire = 370
                rectangle(
                    x_bouton_bonus_aleatoire,
                    y_bouton_bonus_aleatoire,
                    x_bouton_bonus_aleatoire + 90,
                    y_bouton_bonus_aleatoire + 50,
                    couleur="gray",
                    remplissage="gray",
                    tag="bonus_aleatoire",
                )
                texte(
                    x_bouton_bonus_aleatoire + 45,
                    y_bouton_bonus_aleatoire + 25,
                    "Prédefinis",
                    couleur="black",
                    police="Helvetica",
                    taille=13,
                    ancrage="center",
                    tag="bonus_aleatoire",
                )

                x_bouton_bonus_predefini = 160  # Pour les bonus prédéfinis
                y_bouton_bonus_predefini = 370
                rectangle(
                    x_bouton_bonus_predefini,
                    y_bouton_bonus_predefini,
                    x_bouton_bonus_predefini + 90,
                    y_bouton_bonus_predefini + 50,
                    couleur="green",
                    remplissage="green",
                    tag="bonus_predefini",
                )
                texte(
                    x_bouton_bonus_predefini + 45,
                    y_bouton_bonus_predefini + 25,
                    "Aléatoires",
                    couleur="black",
                    police="Helvetica",
                    taille=13,
                    ancrage="center",
                    tag="bonus_predefini",
                )

            if (
                x_bouton_bonus_aleatoire <= x <= x_bouton_bonus_aleatoire + 90
                and y_bouton_bonus_aleatoire <= y <= y_bouton_bonus_aleatoire + 50
                and bonus_predefini == True
                and clic == False
                and bonus == True
            ):
                clic = True
                bonus_aleatoire = True
                bonus_predefini = False
                efface("bonus_aleatoire")
                rectangle(
                    x_bouton_bonus_aleatoire,
                    y_bouton_bonus_aleatoire,
                    x_bouton_bonus_aleatoire + 90,
                    y_bouton_bonus_aleatoire + 50,
                    couleur="green",
                    remplissage="green",
                    tag="bonus_aleatoire",
                )
                texte(
                    x_bouton_bonus_aleatoire + 45,
                    y_bouton_bonus_aleatoire + 25,
                    "Prédefinis",
                    couleur="black",
                    police="Helvetica",
                    taille=13,
                    ancrage="center",
                    tag="bonus_aleatoire",
                )
                efface("bonus_predefini")
                rectangle(
                    x_bouton_bonus_predefini,
                    y_bouton_bonus_predefini,
                    x_bouton_bonus_predefini + 90,
                    y_bouton_bonus_predefini + 50,
                    couleur="gray",
                    remplissage="gray",
                    tag="bonus_predefini",
                )
                texte(
                    x_bouton_bonus_predefini + 45,
                    y_bouton_bonus_predefini + 25,
                    "Aléatoires",
                    couleur="black",
                    police="Helvetica",
                    taille=13,
                    ancrage="center",
                    tag="bonus_predefini",
                )

            if (
                x_bouton_bonus_predefini <= x <= x_bouton_bonus_predefini + 90
                and y_bouton_bonus_predefini <= y <= y_bouton_bonus_predefini + 50
                and bonus_aleatoire == True
                and clic == False
                and bonus == True
            ):
                clic = True
                bonus_aleatoire = False
                bonus_predefini = True
                efface("bonus_predefini")
                rectangle(
                    x_bouton_bonus_predefini,
                    y_bouton_bonus_predefini,
                    x_bouton_bonus_predefini + 90,
                    y_bouton_bonus_predefini + 50,
                    couleur="green",
                    remplissage="green",
                    tag="bonus_predefini",
                )
                texte(
                    x_bouton_bonus_predefini + 45,
                    y_bouton_bonus_predefini + 25,
                    "Aléatoires",
                    couleur="black",
                    police="Helvetica",
                    taille=13,
                    ancrage="center",
                    tag="bonus_predefini",
                )
                efface("bonus_aleatoire")
                rectangle(
                    x_bouton_bonus_aleatoire,
                    y_bouton_bonus_aleatoire,
                    x_bouton_bonus_aleatoire + 90,
                    y_bouton_bonus_aleatoire + 50,
                    couleur="gray",
                    remplissage="gray",
                    tag="bonus_aleatoire",
                )
                texte(
                    x_bouton_bonus_aleatoire + 45,
                    y_bouton_bonus_aleatoire + 25,
                    "Prédefinis",
                    couleur="black",
                    police="Helvetica",
                    taille=13,
                    ancrage="center",
                    tag="bonus_aleatoire",
                )

            if (
                x_bouton_bonus <= x <= x_bouton_bonus + largeur_bouton
                and y_bouton_bonus <= y <= y_bouton_bonus + hauteur_bouton
                and bonus == True
                and clic == False
            ):
                clic = True
                bonus = False
                efface("bonus")
                efface("bonus_predefini")
                efface("bonus_aleatoire")
                rectangle(
                    x_bouton_bonus,
                    y_bouton_bonus,
                    x_bouton_bonus + largeur_bouton,
                    y_bouton_bonus + hauteur_bouton,
                    couleur="yellow",
                    epaisseur=5,
                    tag="bonus",
                )
                texte(
                    x_bouton_bonus + 100,
                    y_bouton_bonus + 25,
                    "Bonus",
                    couleur="white",
                    police="Helvetica",
                    taille=20,
                    ancrage="center",
                    tag="bonus",
                )

            # 2 joueurs
            if (
                x_bouton_2 <= x <= x_bouton_2 + largeur_bouton
                and y_bouton_2 <= y <= y_bouton_2 + hauteur_bouton
                and deux == False
                and clic == False
            ):
                clic = True
                deux = True
                efface("deux")
                rectangle(
                    x_bouton_2,
                    y_bouton_2,
                    x_bouton_2 + largeur_bouton,
                    y_bouton_2 + hauteur_bouton,
                    couleur="cyan",
                    remplissage="cyan",
                    tag="deux",
                )
                texte(
                    x_bouton_2 + 100,
                    y_bouton_2 + 25,
                    "2 joueurs",
                    couleur="white",
                    police="Helvetica",
                    taille=20,
                    ancrage="center",
                    tag="deux",
                )
            if (
                x_bouton_2 <= x <= x_bouton_2 + largeur_bouton
                and y_bouton_2 <= y <= y_bouton_2 + hauteur_bouton
                and deux == True
                and clic == False
            ):
                clic = True
                deux = False
                efface("deux")
                rectangle(
                    x_bouton_2,
                    y_bouton_2,
                    x_bouton_2 + largeur_bouton,
                    y_bouton_2 + hauteur_bouton,
                    couleur="yellow",
                    epaisseur=5,
                    tag="deux",
                )
                texte(
                    x_bouton_2 + 100,
                    y_bouton_2 + 25,
                    "2 joueurs",
                    couleur="white",
                    police="Helvetica",
                    taille=20,
                    ancrage="center",
                    tag="deux",
                )

            # Niveaux
            if (
                x_bouton_niveau <= x <= x_bouton_niveau + largeur_bouton
                and y_bouton_niveau <= y <= y_bouton_niveau + hauteur_bouton
                and niveau == False
                and clic == False
            ):
                clic = True
                niveau = True
                efface("niveau")
                rectangle(
                    x_bouton_niveau,
                    y_bouton_niveau,
                    x_bouton_niveau + largeur_bouton,
                    y_bouton_niveau + hauteur_bouton,
                    couleur="pink",
                    remplissage="pink",
                    tag="niveau",
                )
                texte(
                    x_bouton_niveau + 100,
                    y_bouton_niveau + 25,
                    "Niveaux",
                    couleur="white",
                    police="Helvetica",
                    taille=20,
                    ancrage="center",
                    tag="niveau",
                )

                x_choix_niveau1 = 650  # Pour le niveau 1
                y_choix_niveau1 = 370
                rectangle(
                    x_choix_niveau1,
                    y_choix_niveau1,
                    x_choix_niveau1 + 50,
                    y_choix_niveau1 + 50,
                    couleur="green",
                    remplissage="green",
                    tag="niveau1",
                )
                texte(
                    x_choix_niveau1 + 25,
                    y_choix_niveau1 + 25,
                    "F",
                    couleur="black",
                    police="Helvetica",
                    taille=13,
                    ancrage="center",
                    tag="niveau1",
                )

                x_choix_niveau2 = 725  # Pour le niveau 2
                y_choix_niveau2 = 370
                rectangle(
                    x_choix_niveau2,
                    y_choix_niveau2,
                    x_choix_niveau2 + 50,
                    y_choix_niveau2 + 50,
                    couleur="orange",
                    remplissage="orange",
                    tag="niveau2",
                )
                texte(
                    x_choix_niveau2 + 25,
                    y_choix_niveau2 + 25,
                    "M",
                    couleur="black",
                    police="Helvetica",
                    taille=13,
                    ancrage="center",
                    tag="niveau2",
                )

                x_choix_niveau3 = 800  # Pour le niveau 3
                y_choix_niveau3 = 370
                rectangle(
                    x_choix_niveau3,
                    y_choix_niveau3,
                    x_choix_niveau3 + 50,
                    y_choix_niveau3 + 50,
                    couleur="red",
                    remplissage="red",
                    tag="niveau3",
                )
                texte(
                    x_choix_niveau3 + 25,
                    y_choix_niveau3 + 25,
                    "D",
                    couleur="black",
                    police="Helvetica",
                    taille=13,
                    ancrage="center",
                    tag="niveau3",
                )

            if (
                x_choix_niveau1 <= x <= x_choix_niveau1 + 50
                and y_choix_niveau1 <= y <= y_choix_niveau1 + 50
                and niveau1 == False
                and clic == False
            ):  # Pour le niveau 1
                clic = True
                niveau1 = True
                niveau2 = False
                niveau3 = False
                efface("niveau1")
                rectangle(
                    x_choix_niveau1,
                    y_choix_niveau1,
                    x_choix_niveau1 + 50,
                    y_choix_niveau1 + 50,
                    couleur="white",
                    remplissage="green",
                    epaisseur=3.5,
                    tag="niveau1",
                )
                texte(
                    x_choix_niveau1 + 25,
                    y_choix_niveau1 + 25,
                    "F",
                    couleur="black",
                    police="Helvetica",
                    taille=13,
                    ancrage="center",
                    tag="niveau1",
                )

                efface("niveau2")
                rectangle(
                    x_choix_niveau2,
                    y_choix_niveau2,
                    x_choix_niveau2 + 50,
                    y_choix_niveau2 + 50,
                    couleur="orange",
                    remplissage="orange",
                    tag="niveau2",
                )
                texte(
                    x_choix_niveau2 + 25,
                    y_choix_niveau2 + 25,
                    "M",
                    couleur="black",
                    police="Helvetica",
                    taille=13,
                    ancrage="center",
                    tag="niveau2",
                )

                efface("niveau3")
                rectangle(
                    x_choix_niveau3,
                    y_choix_niveau3,
                    x_choix_niveau3 + 50,
                    y_choix_niveau3 + 50,
                    couleur="red",
                    remplissage="red",
                    tag="niveau3",
                )
                texte(
                    x_choix_niveau3 + 25,
                    y_choix_niveau3 + 25,
                    "D",
                    couleur="black",
                    police="Helvetica",
                    taille=13,
                    ancrage="center",
                    tag="niveau3",
                )

            if (
                x_choix_niveau2 <= x <= x_choix_niveau2 + 50
                and y_choix_niveau2 <= y <= y_choix_niveau2 + 50
                and niveau2 == False
                and clic == False
            ):  # Pour le niveau 2
                clic = True
                niveau1 = False
                niveau2 = True
                niveau3 = False
                efface("niveau2")
                rectangle(
                    x_choix_niveau2,
                    y_choix_niveau2,
                    x_choix_niveau2 + 50,
                    y_choix_niveau2 + 50,
                    couleur="white",
                    remplissage="orange",
                    epaisseur=3.5,
                    tag="niveau2",
                )
                texte(
                    x_choix_niveau2 + 25,
                    y_choix_niveau2 + 25,
                    "M",
                    couleur="black",
                    police="Helvetica",
                    taille=13,
                    ancrage="center",
                    tag="niveau2",
                )

                efface("niveau1")
                rectangle(
                    x_choix_niveau1,
                    y_choix_niveau1,
                    x_choix_niveau1 + 50,
                    y_choix_niveau1 + 50,
                    couleur="green",
                    remplissage="green",
                    tag="niveau1",
                )
                texte(
                    x_choix_niveau1 + 25,
                    y_choix_niveau1 + 25,
                    "F",
                    couleur="black",
                    police="Helvetica",
                    taille=13,
                    ancrage="center",
                    tag="niveau1",
                )

                efface("niveau3")
                rectangle(
                    x_choix_niveau3,
                    y_choix_niveau3,
                    x_choix_niveau3 + 50,
                    y_choix_niveau3 + 50,
                    couleur="red",
                    remplissage="red",
                    tag="niveau3",
                )
                texte(
                    x_choix_niveau3 + 25,
                    y_choix_niveau3 + 25,
                    "D",
                    couleur="black",
                    police="Helvetica",
                    taille=13,
                    ancrage="center",
                    tag="niveau3",
                )

            if (
                x_choix_niveau3 <= x <= x_choix_niveau3 + 50
                and y_choix_niveau3 <= y <= y_choix_niveau3 + 50
                and niveau3 == False
                and clic == False
            ):  # Pour le niveau 3
                clic = True
                niveau1 = False
                niveau2 = False
                niveau3 = True
                efface("niveau2")
                rectangle(
                    x_choix_niveau2,
                    y_choix_niveau2,
                    x_choix_niveau2 + 50,
                    y_choix_niveau2 + 50,
                    couleur="orange",
                    remplissage="orange",
                    tag="niveau2",
                )
                texte(
                    x_choix_niveau2 + 25,
                    y_choix_niveau2 + 25,
                    "M",
                    couleur="black",
                    police="Helvetica",
                    taille=13,
                    ancrage="center",
                    tag="niveau2",
                )

                efface("niveau1")
                rectangle(
                    x_choix_niveau1,
                    y_choix_niveau1,
                    x_choix_niveau1 + 50,
                    y_choix_niveau1 + 50,
                    couleur="green",
                    remplissage="green",
                    tag="niveau1",
                )
                texte(
                    x_choix_niveau1 + 25,
                    y_choix_niveau1 + 25,
                    "F",
                    couleur="black",
                    police="Helvetica",
                    taille=13,
                    ancrage="center",
                    tag="niveau1",
                )

                efface("niveau3")
                rectangle(
                    x_choix_niveau3,
                    y_choix_niveau3,
                    x_choix_niveau3 + 50,
                    y_choix_niveau3 + 50,
                    couleur="white",
                    remplissage="red",
                    epaisseur=3.5,
                    tag="niveau3",
                )
                texte(
                    x_choix_niveau3 + 25,
                    y_choix_niveau3 + 25,
                    "D",
                    couleur="black",
                    police="Helvetica",
                    taille=13,
                    ancrage="center",
                    tag="niveau3",
                )

            if (
                x_bouton_niveau <= x <= x_bouton_niveau + largeur_bouton
                and y_bouton_niveau <= y <= y_bouton_niveau + hauteur_bouton
                and niveau == True
                and clic == False
            ):
                clic = True
                niveau = False
                niveau1 = False
                niveau2 = False
                niveau3 = False
                efface("niveau1")
                efface("niveau2")
                efface("niveau3")
                efface("niveau")
                rectangle(
                    x_bouton_niveau,
                    y_bouton_niveau,
                    x_bouton_niveau + largeur_bouton,
                    y_bouton_niveau + hauteur_bouton,
                    couleur="yellow",
                    epaisseur=5,
                    tag="niveau",
                )
                texte(
                    x_bouton_niveau + 100,
                    y_bouton_niveau + 25,
                    "Niveaux",
                    couleur="white",
                    police="Helvetica",
                    taille=20,
                    ancrage="center",
                    tag="niveau",
                )

            # Lancer la partie
            if (
                x_bouton_nouvelle_partie
                <= x
                <= x_bouton_nouvelle_partie + largeur_bouton
                and y_bouton_nouvelle_partie
                <= y
                <= y_bouton_nouvelle_partie + hauteur_bouton
            ):
                start = True

            # Quitter
            if (
                x_bouton_quitter <= x <= x_bouton_quitter + largeur_bouton
                and y_bouton_quitter <= y <= y_bouton_quitter + hauteur_bouton
            ):
                ferme_fenetre()

            mise_a_jour()

        ferme_fenetre()
        return (
            scorev,
            vitesse,
            obstacle,
            bonus,
            deux,
            niveau,
            start,
            obstacle_predefini,
            obstacle_aleatoire,
            niveau1,
            niveau2,
            niveau3,
            bonus_aleatoire,
            bonus_predefini,
        )


def placer_pomme():
    x, y = randint(100, 500), randint(250, 700)
    while x % 5 != 0 or y % 5 != 0 or [x, y] in zone_obstacle:
        x, y = randint(100, 500), randint(250, 700)
    return x, y


def time_pour_bonus():
    t = time()
    return t


def echanger_listes(liste1, liste2):
    # Échanger le contenu des listes en utilisant une variable temporaire
    temp = liste1.copy()
    liste1[:] = liste2
    liste2[:] = temp


# -------------------------------------Paramètres du joueur---------------------------------------------------------


def jeu():

    # parametres configures
    with open("ressources/parametres.txt", "r") as fichier:
        # Lire toutes les lignes dans une liste
        lignes = fichier.readlines()

        # Utiliser une comprehension de liste pour appliquer strip() a chaque element
        lignes = [element.strip() for element in lignes]

    # dessin initial du carré
    cx, cy, taille = int(lignes[16]), int(lignes[17]), int(lignes[18])
    if deux == False:
        joueur1(cx - 5, cy - 5, taille, "ressources/Pacman1_haut.png")
    iteration = int(lignes[22])
    vitesse_deplacement = int(lignes[26])
    surface_polygone = int(lignes[30])

    # def QIX
    couleur_qix = "blue"
    xQIX, yQIX = int(lignes[36]), int(lignes[37])
    vitesse_QIX = int(lignes[41])

    # def Sparks
    couleur_sparks = str(lignes[47])
    temps_sparks = 0
    deplacement_sparks = int(lignes[61])
    vitesse_sparks = int(lignes[51])
    cxsparks1, cysparks1, taille = int(lignes[55]), int(lignes[56]), int(lignes[57])
    cxsparks2, cysparks2, taille = int(lignes[55]), int(lignes[56]), int(lignes[57])

    image(
        cxsparks1,
        cysparks1 - 5,
        "ressources/Fantome1.png",
        largeur=taille + 5,
        hauteur=taille + 5,
        tag="sparks1",
    )
    image(
        cxsparks2,
        cysparks2 - 5,
        "ressources/Fantome2.png",
        largeur=taille + 5,
        hauteur=taille + 5,
        tag="sparks2",
    )
    if niveau2 == True or niveau3 == True:
        cxsparks3, cysparks3, taille = 50, 205, int(lignes[57])
        cxsparks4, cysparks4, taille = 550, 205, int(lignes[57])
        image(
            cxsparks3,
            cysparks3 - 5,
            "ressources/Fantome3.png",
            largeur=taille + 5,
            hauteur=taille + 5,
            tag="sparks3",
        )
        image(
            cxsparks4,
            cysparks4 - 5,
            "ressources/Fantome4.png",
            largeur=taille + 5,
            hauteur=taille + 5,
            tag="sparks4",
        )
    if niveau3 == True:
        cxsparks5, cysparks5, taille = 175, 200, int(lignes[57])
        cxsparks6, cysparks6, taille = 425, 200, int(lignes[57])
        image(
            cxsparks5,
            cysparks5 - 5,
            "ressources/Fantome5.png",
            largeur=taille + 5,
            hauteur=taille + 5,
            tag="sparks5",
        )
        image(
            cxsparks6,
            cysparks6 - 5,
            "ressources/Fantome1.png",
            largeur=taille + 5,
            hauteur=taille + 5,
            tag="sparks6",
        )

    xcoin, ycoin = 50, 200
    xsafe, ysafe = 50, 200
    x = 0

    # fin de la configuration par fichier

    Nombre_vie = 3

    # Calcul du nombre de positions possibles pour calcul surface
    largeur = (500 - 50) / 5
    hauteur = (750 - 200) / 5
    nb_positions = largeur * hauteur

    nb_polygone = 0

    temps_bonus = 3
    Invincibilite1 = False  # Passe a true si le joueur 1 prend une pomme
    Invincibilite2 = False  # Passe a true si le joueur 2 prend une pomme

    # Mise en place des obstables
    matobstacles = []
    if obstacle == True:
        if obstacle_predefini == True:
            fichier = "ressources/obstacles.txt"
            # dans le fichier, les parametres des obstacles sont de la forme:
            # x y z,x y z,x y z etc...
            # x et y sont les coordonnees de base, z la taille
            # les espaces et les virgules doivent etre selon ce format
            if os.path.isfile(fichier):
                with open(fichier, "r") as obst:
                    # Lire toutes les lignes dans une liste
                    lignes = obst.readlines()

                    # Utiliser une comprehension de liste pour appliquer strip() a chaque element
                    lignes = [element.strip() for element in lignes]

                    temp2 = lignes[10].split(",")
                    obstacle_list = [
                        list(map(int, coord.split(" "))) for coord in temp2
                    ]
                    matobstacles.extend(obstacle_list)

                for obstacles in matobstacles:
                    rectangle(
                        obstacles[0],
                        obstacles[1],
                        obstacles[0] + obstacles[2],
                        obstacles[1] + obstacles[2],
                        "gray",
                        "gray",
                        tag="obstacle",
                    )

                    for i in range(obstacles[0], obstacles[0] + obstacles[2]):
                        for k in range(obstacles[1], obstacles[1] + obstacles[2]):
                            zone_obstacle.append([i, k])
                obst.close()

        if obstacle_aleatoire == True:
            xobstacle1, yobstacle1, taille_obstacle1 = (
                randint(100, 300),
                randint(380, 580),
                randint(50, 120),
            )
            xobstacle2, yobstacle2, taille_obstacle2 = (
                randint(100, 300),
                randint(380, 580),
                randint(50, 120),
            )
            xobstacle3, yobstacle3, taille_obstacle3 = (
                randint(100, 300),
                randint(380, 580),
                randint(50, 120),
            )
            rectangle(
                xobstacle1,
                yobstacle1,
                xobstacle1 + taille_obstacle1,
                yobstacle1 + taille_obstacle1,
                "gray",
                "gray",
                tag="obstacle1",
            )
            rectangle(
                xobstacle2,
                yobstacle2,
                xobstacle2 + taille_obstacle2,
                yobstacle2 + taille_obstacle2,
                "gray",
                "gray",
                tag="obstacle2",
            )
            rectangle(
                xobstacle3,
                yobstacle3,
                xobstacle3 + taille_obstacle3,
                yobstacle3 + taille_obstacle3,
                "gray",
                "gray",
                tag="obstacle3",
            )

            for i in range(xobstacle1, xobstacle1 + taille_obstacle1):
                for k in range(yobstacle1, yobstacle1 + taille_obstacle1):
                    zone_obstacle.append([i, k])

            for i in range(xobstacle2, xobstacle2 + taille_obstacle2):
                for k in range(yobstacle2, yobstacle2 + taille_obstacle2):
                    zone_obstacle.append([i, k])

            for i in range(xobstacle3, xobstacle3 + taille_obstacle3):
                for k in range(yobstacle3, yobstacle3 + taille_obstacle3):
                    zone_obstacle.append([i, k])

    # Mise en place des pommes

    if bonus == True:
        if bonus_predefini == True:
            pomme1x, pomme1y = placer_pomme()
            pomme2x, pomme2y = placer_pomme()
            pomme3x, pomme3y = placer_pomme()
            pomme4x, pomme4y = placer_pomme()
            pomme5x, pomme5y = placer_pomme()
        else:
            fichier = "ressources/obstacles.txt"
            # dans le fichier, les parametres des obstacles sont de la forme:
            # x
            # y
            # x et y sont les coordonnees des pommes
            if os.path.isfile(fichier):
                with open(fichier, "r") as obst:
                    # Lire toutes les lignes dans une liste
                    lignes = obst.readlines()

                    # Utiliser une comprehension de liste pour appliquer strip() a chaque element
                    lignes = [element.strip() for element in lignes]

                    pomme1x, pomme1y = int(lignes[27]), int(lignes[28])
                    pomme2x, pomme2y = int(lignes[32]), int(lignes[33])
                    pomme3x, pomme3y = int(lignes[37]), int(lignes[38])
                    pomme4x, pomme4y = int(lignes[42]), int(lignes[43])
                    pomme5x, pomme5y = int(lignes[47]), int(lignes[48])

        image(
            pomme1x,
            pomme1y,
            "ressources/Fruit1.png",
            largeur=20,
            hauteur=20,
            tag="pomme1",
        )
        image(
            pomme2x,
            pomme2y,
            "ressources/Fruit2.png",
            largeur=20,
            hauteur=20,
            tag="pomme2",
        )
        image(
            pomme3x,
            pomme3y,
            "ressources/Fruit3.png",
            largeur=20,
            hauteur=20,
            tag="pomme3",
        )
        image(
            pomme4x,
            pomme4y,
            "ressources/Fruit4.png",
            largeur=20,
            hauteur=20,
            tag="pomme4",
        )
        image(
            pomme5x,
            pomme5y,
            "ressources/Fruit5.png",
            largeur=20,
            hauteur=20,
            tag="pomme5",
        )

        zone_pomme.append((pomme1x, pomme1y))
        zone_pomme.append((pomme1x + 5, pomme1y))
        zone_pomme.append((pomme1x, pomme1y + 5))
        zone_pomme.append((pomme1x + 5, pomme1y + 5))

        zone_pomme.append((pomme2x, pomme2y))
        zone_pomme.append((pomme2x + 5, pomme2y))
        zone_pomme.append((pomme2x, pomme2y + 5))
        zone_pomme.append((pomme2x + 5, pomme2y + 5))

        zone_pomme.append((pomme3x, pomme3y))
        zone_pomme.append((pomme3x + 5, pomme3y))
        zone_pomme.append((pomme3x, pomme3y + 5))
        zone_pomme.append((pomme3x + 5, pomme3y + 5))

        zone_pomme.append((pomme4x, pomme4y))
        zone_pomme.append((pomme4x + 5, pomme4y))
        zone_pomme.append((pomme4x, pomme4y + 5))
        zone_pomme.append((pomme4x + 5, pomme4y + 5))

        zone_pomme.append((pomme5x, pomme5y))
        zone_pomme.append((pomme5x + 5, pomme5y))
        zone_pomme.append((pomme5x, pomme5y + 5))
        zone_pomme.append((pomme5x + 5, pomme5y + 5))

        pomme1 = True
        pomme2 = True
        pomme3 = True
        pomme4 = True
        pomme5 = True

    # Mise en place de la vitesse du joueur

    if vitesse == True:
        texte(
            280,
            170,
            "Vitesse traçage:",
            couleur="white",
            taille=15,
            police="Copperplate Gothic Bold",
        )
        texte(
            475,
            170,
            "Lente",
            couleur="green",
            taille=15,
            police="Copperplate Gothic Bold",
            tag="vitesse",
        )
        vitesse_tracage = 5
    else:
        vitesse_tracage = vitesse_deplacement

    touche_V = "v"
    score = 0

    # Mise en place des niveaux
    if niveau1 == True:
        longueur_deplacement_QIX = 6
        vitesse_QIX = 10
    elif niveau2 == True:
        longueur_deplacement_QIX = 9
        vitesse_QIX = 20
        cxsparks3, cysparks3, taille = 50, 205, int(lignes[57])
        cxsparks4, cysparks4, taille = 550, 205, int(lignes[57])
        vitesse_sparks = 2
    elif niveau3 == True:
        longueur_deplacement_QIX = 12
        vitesse_QIX = 30
        cxsparks3, cysparks3, taille = 50, 205, int(lignes[57])
        cxsparks4, cysparks4, taille = 550, 205, int(lignes[57])
        cxsparks5, cysparks5, taille = 175, 200, int(lignes[57])
        cxsparks6, cysparks6, taille = 425, 200, int(lignes[57])
        vitesse_sparks = 2
    else:
        longueur_deplacement_QIX = 6

    # Mise en place du mode 2 joueurs
    if deux == True:
        rectangle(600, 0, 900, 1200, "white", "black", 2)
        cx, cy = 550, 750
        cx2, cy2 = 50, 750
        historique_positions2 = []
        trait_joueur_actuel2 = []
        joueur1(cx - 5, cy - 5, taille, "ressources/Pacman1_haut.png")
        joueur2(cx2 - 5, cy2 - 5, taille, "ressources/Pacman2_haut.png")
        iteration2 = 0
        touche_espace = "m"
        touche_espace2 = "space"
        historique_deplacement2 = []
        historique_virage2 = []
        vitesse_tracage2 = 5
        surface_polygone_joueur1 = 0
        surface_polygone_joueur2 = 0
        touche_V2 = "v"
        score1 = 0
        score2 = 0

        image(300, 100, "ressources/Titre2.png", largeur=250, hauteur=80)

        texte(
            680,
            80,
            "CLAIMED",
            couleur="white",
            taille=20,
            police="Copperplate Gothic Bold",
        )
        texte(
            765,
            110,
            "75 %",
            couleur="white",
            taille=16,
            police="Copperplate Gothic Bold",
        )
        texte(
            735, 110, "%", couleur="white", taille=16, police="Copperplate Gothic Bold"
        )
        texte(
            700,
            110,
            "0",
            couleur="white",
            taille=16,
            police="Copperplate Gothic Bold",
            tag="score_pourcentage",
        )

        texte(
            650,
            200,
            "JOUEUR 1",
            couleur="white",
            taille=20,
            police="Copperplate Gothic Bold",
        )
        texte(
            650,
            250,
            "SCORE :",
            couleur="white",
            taille=16,
            police="Copperplate Gothic Bold",
        )
        if scorev == False:
            texte(
                770,
                250,
                "X",
                couleur="white",
                taille=16,
                police="Copperplate Gothic Bold",
                tag="score_joueur1",
            )
        else:
            texte(
                770,
                250,
                0,
                couleur="white",
                taille=16,
                police="Copperplate Gothic Bold",
                tag="score_joueur1",
            )
        image(750, 340, "ressources/Pacman1_droite.png", largeur=100, hauteur=100)

        ligne(600, 440, 1000, 440, couleur="white")

        texte(
            650,
            500,
            "JOUEUR 2",
            couleur="white",
            taille=20,
            police="Copperplate Gothic Bold",
        )
        texte(
            650,
            550,
            "SCORE :",
            couleur="white",
            taille=16,
            police="Copperplate Gothic Bold",
        )
        if scorev == False:
            texte(
                770,
                550,
                "X",
                couleur="white",
                taille=16,
                police="Copperplate Gothic Bold",
                tag="score_joueur2",
            )
        else:
            texte(
                770,
                550,
                0,
                couleur="white",
                taille=16,
                police="Copperplate Gothic Bold",
                tag="score_joueur2",
            )
        image(750, 640, "ressources/Pacman2_droite.png", largeur=100, hauteur=100)
        Nombre_vie2 = 3
        Invincibilite2 = False
        efface("coeur1")
        efface("coeur2")
        efface("coeur3")
        cercle(850, 250, 5, "red", "red", tag="coeur1")
        cercle(850, 265, 5, "red", "red", tag="coeur2")
        cercle(850, 280, 5, "red", "red", tag="coeur3")

        cercle(850, 550, 5, "red", "red", tag="coeur1_2")
        cercle(850, 565, 5, "red", "red", tag="coeur2_2")
        cercle(850, 580, 5, "red", "red", tag="coeur3_2")
    else:
        touche_espace = "space"

    texte(
        300,
        475,
        "CLIQUEZ POUR COMMENCER",
        couleur="white",
        taille=20,
        police="Copperplate Gothic Bold",
        ancrage="center",
        tag="commencer",
    )

    run = True
    deplacement_sparks = 0

    while run:
        ev = donne_ev()
        tev = type_ev(ev)
        # -------------------------------Déplacement des joueurs sur les bordures du terrain-----------------------------------
        if tev == "ClicGauche":
            efface("commencer")
            deplacement_sparks = int(lignes[61])

        if touche_pressee("Escape"):  # Permet de fermer la fenêtre
            ferme_fenetre()
        # JOUEUR 1
        dx = 0
        dy = 0
        if touche_pressee("Left"):  # Si flèche gauche est pressée
            if [cx - 5, cy] in zone_safe:
                dx = -vitesse_deplacement

        elif touche_pressee("Right"):  # Si flèche droite est pressée
            if [cx + 5, cy] in zone_safe:
                dx = vitesse_deplacement

        elif touche_pressee("Down"):  # Si flèche bas est pressée
            if [cx, cy + 5] in zone_safe:
                dy = vitesse_deplacement

        elif touche_pressee("Up"):  # Si flèche haut est pressée
            if [cx, cy - 5] in zone_safe:
                dy = -vitesse_deplacement

        # JOUEUR 2
        if deux == True:
            dx2 = 0
            dy2 = 0
            if touche_pressee("s"):  # Si flèche bas est pressée
                if [cx2, cy2 + 5] in zone_safe:
                    dy2 = vitesse_deplacement

            elif touche_pressee("q"):  # Si flèche gauche est pressée
                if [cx2 - 5, cy2] in zone_safe:
                    dx2 = -vitesse_deplacement

            elif touche_pressee("d"):  # Si flèche droite est pressée
                if [cx2 + 5, cy2] in zone_safe:
                    dx2 = vitesse_deplacement

            elif touche_pressee("z"):  # Si flèche haut est pressée
                if [cx2, cy2 - 5] in zone_safe:
                    dy2 = -vitesse_deplacement

        # -------------------------------Joueur dans le terrain-----------------------------------
        # JOUEUR 1
        if (touche_pressee(touche_espace)) and (
            touche_pressee("Left")
            or touche_pressee("Right")
            or touche_pressee("Down")
            or touche_pressee("Up")
        ):

            if iteration == 0:
                historique_positions.append([cx, cy])
                iteration += 1
            if (
                touche_pressee("Left")
                and [cx - (5 * (int(vitesse_tracage / 5))), cy] in zone_terrain
                and [cx - (5 * (int(vitesse_tracage / 5))), cy] not in zone_polygone
                and [cx - (5 * (int(vitesse_tracage / 5))), cy] not in zone_obstacle
                and [cx - 10, cy] not in trait_joueur_actuel
            ):  # Si flèche gauche est pressée
                dx = -vitesse_tracage
                ligne(
                    cx,
                    cy,
                    cx - (5 * (int(vitesse_tracage / 5))),
                    cy,
                    "white",
                    2,
                    tag="trait_joueur",
                )
                historique_virage.append(["Gauche", [cx, cy]])
                historique_deplacement.append("Gauche")

                if (
                    historique_virage[len(historique_virage) - 1][0]
                    != historique_virage[len(historique_virage) - 2][0]
                ):  # detecte un changement de direction
                    historique_positions.append([cx, cy])

            elif (
                touche_pressee("Right")
                and [cx + (5 * (int(vitesse_tracage / 5))), cy] in zone_terrain
                and [cx + (5 * (int(vitesse_tracage / 5))), cy] not in zone_polygone
                and [cx + (5 * (int(vitesse_tracage / 5))), cy] not in zone_obstacle
                and [cx + 10, cy] not in trait_joueur_actuel
            ):  # Si flèche droite est pressée
                dx = vitesse_tracage
                ligne(
                    cx,
                    cy,
                    cx + (5 * (int(vitesse_tracage / 5))),
                    cy,
                    "white",
                    2,
                    tag="trait_joueur",
                )
                historique_virage.append(["Droite", [cx, cy]])
                historique_deplacement.append("Droite")

                if (
                    historique_virage[len(historique_virage) - 1][0]
                    != historique_virage[len(historique_virage) - 2][0]
                ):  # detecte un changement de direction
                    historique_positions.append([cx, cy])

            elif (
                touche_pressee("Down")
                and [cx, cy + (5 * (int(vitesse_tracage / 5)))] in zone_terrain
                and [cx, cy + (5 * (int(vitesse_tracage / 5)))] not in zone_polygone
                and [cx, cy + (5 * (int(vitesse_tracage / 5)))] not in zone_obstacle
                and [cx, cy + 10] not in trait_joueur_actuel
            ):  # Si flèche bas est pressée
                dy = vitesse_tracage
                ligne(
                    cx,
                    cy,
                    cx,
                    cy + (5 * (int(vitesse_tracage / 5))),
                    "white",
                    2,
                    tag="trait_joueur",
                )
                historique_virage.append(["Bas", [cx, cy]])
                historique_deplacement.append("Bas")

                if (
                    historique_virage[len(historique_virage) - 1][0]
                    != historique_virage[len(historique_virage) - 2][0]
                ):  # detecte un changement de direction
                    historique_positions.append([cx, cy])

            elif (
                touche_pressee("Up")
                and [cx, cy - (5 * (int(vitesse_tracage / 5)))] in zone_terrain
                and [cx, cy - (5 * (int(vitesse_tracage / 5)))] not in zone_polygone
                and [cx, cy - (5 * (int(vitesse_tracage / 5)))] not in zone_obstacle
                and [cx, cy - 10] not in trait_joueur_actuel
            ):  # Si flèche haut est pressée
                dy = -vitesse_tracage
                ligne(
                    cx,
                    cy - (5 * (int(vitesse_tracage / 5))),
                    cx,
                    cy,
                    "white",
                    2,
                    tag="trait_joueur",
                )
                historique_virage.append(["Haut", [cx, cy]])
                historique_deplacement.append("Haut")

                if (
                    historique_virage[len(historique_virage) - 1][0]
                    != historique_virage[len(historique_virage) - 2][0]
                ):  # detecte un changement de direction
                    historique_positions.append([cx, cy])

            if [cx, cy] not in trait_joueur_actuel:
                trait_joueur_actuel.append(
                    [cx, cy]
                )  # Référence toutes les positions du joueur à l'intérieur du terrain
                if vitesse_tracage == 10 and len(historique_deplacement) > 1:
                    if [cx, cy] in historique_positions:
                        if historique_deplacement[-2] == "Gauche":
                            trait_joueur_actuel.insert(
                                -2,
                                [
                                    historique_virage[-1][1][0] + 5,
                                    historique_virage[-1][1][1],
                                ],
                            )

                        if historique_deplacement[-2] == "Droite":
                            trait_joueur_actuel.insert(
                                -2,
                                [
                                    historique_virage[-1][1][0] - 5,
                                    historique_virage[-1][1][1],
                                ],
                            )
                        if historique_deplacement[-2] == "Haut":
                            trait_joueur_actuel.insert(
                                -2,
                                [
                                    historique_virage[-1][1][0],
                                    historique_virage[-1][1][1] + 5,
                                ],
                            )
                        if historique_deplacement[-2] == "Bas":
                            trait_joueur_actuel.insert(
                                -2,
                                [
                                    historique_virage[-1][1][0],
                                    historique_virage[-1][1][1] - 5,
                                ],
                            )

                    else:

                        if historique_deplacement[-1] == "Gauche":
                            trait_joueur_actuel.insert(-2, [cx + 5, cy])
                        if historique_deplacement[-1] == "Droite":
                            trait_joueur_actuel.insert(-2, [cx - 5, cy])
                        if historique_deplacement[-1] == "Haut":
                            trait_joueur_actuel.insert(-2, [cx, cy + 5])
                        if historique_deplacement[-1] == "Bas":
                            trait_joueur_actuel.insert(-2, [cx, cy - 5])
        # JOUEUR 2

        if deux == True:
            if (touche_pressee(touche_espace2)) and (
                touche_pressee("q")
                or touche_pressee("d")
                or touche_pressee("s")
                or touche_pressee("z")
            ):
                if iteration2 == 0:
                    historique_positions2.append([cx2, cy2])
                    iteration2 += 1

                if (
                    touche_pressee("q")
                    and [cx2 - (5 * (int(vitesse_tracage2 / 5))), cy2] in zone_terrain
                    and [cx2 - (5 * (int(vitesse_tracage2 / 5))), cy2]
                    not in zone_polygone
                    and [cx2 - (5 * (int(vitesse_tracage2 / 5))), cy2]
                    not in zone_obstacle
                    and [cx2 - 10, cy2] not in trait_joueur_actuel2
                ):  # Si flèche gauche est pressée
                    dx2 = -vitesse_tracage2
                    ligne(
                        cx2,
                        cy2,
                        cx2 - (5 * (int(vitesse_tracage2 / 5))),
                        cy2,
                        "white",
                        2,
                        tag="trait_joueur2",
                    )
                    historique_virage2.append(["Gauche", [cx2, cy2]])
                    historique_deplacement2.append("Gauche")

                    if (
                        historique_virage2[len(historique_virage2) - 1][0]
                        != historique_virage2[len(historique_virage2) - 2][0]
                    ):  # detecte un changement de direction
                        historique_positions2.append([cx2, cy2])

                elif (
                    touche_pressee("d")
                    and [cx2 + (5 * (int(vitesse_tracage2 / 5))), cy2] in zone_terrain
                    and [cx2 + (5 * (int(vitesse_tracage2 / 5))), cy2]
                    not in zone_polygone
                    and [cx2 + (5 * (int(vitesse_tracage2 / 5))), cy2]
                    not in zone_obstacle
                    and [cx2 + 10, cy2] not in trait_joueur_actuel2
                ):  # Si flèche droite est pressée
                    dx2 = vitesse_tracage2
                    ligne(
                        cx2,
                        cy2,
                        cx2 + (5 * (int(vitesse_tracage2 / 5))),
                        cy2,
                        "white",
                        2,
                        tag="trait_joueur2",
                    )
                    historique_virage2.append(["Droite", [cx2, cy2]])
                    historique_deplacement2.append("Droite")

                    if (
                        historique_virage2[len(historique_virage2) - 1][0]
                        != historique_virage2[len(historique_virage2) - 2][0]
                    ):  # detecte un changement de direction
                        historique_positions2.append([cx2, cy2])

                elif (
                    touche_pressee("s")
                    and [cx2, cy2 + (5 * (int(vitesse_tracage2 / 5)))] in zone_terrain
                    and [cx2, cy2 + (5 * (int(vitesse_tracage2 / 5)))]
                    not in zone_polygone
                    and [cx2, cy2 + (5 * (int(vitesse_tracage2 / 5)))]
                    not in zone_obstacle
                    and [cx2, cy2 + 10] not in trait_joueur_actuel2
                ):  # Si flèche bas est pressée
                    dy2 = vitesse_tracage2
                    ligne(
                        cx2,
                        cy2,
                        cx2,
                        cy2 + (5 * (int(vitesse_tracage2 / 5))),
                        "white",
                        2,
                        tag="trait_joueur2",
                    )
                    historique_virage2.append(["Bas", [cx2, cy2]])
                    historique_deplacement2.append("Bas")

                    if (
                        historique_virage2[len(historique_virage2) - 1][0]
                        != historique_virage2[len(historique_virage2) - 2][0]
                    ):  # detecte un changement de direction
                        historique_positions2.append([cx2, cy2])

                elif (
                    touche_pressee("z")
                    and [cx2, cy2 - (5 * (int(vitesse_tracage2 / 5)))] in zone_terrain
                    and [cx2, cy2 - (5 * (int(vitesse_tracage2 / 5)))]
                    not in zone_polygone
                    and [cx2, cy2 - (5 * (int(vitesse_tracage2 / 5)))]
                    not in zone_obstacle
                    and [cx2, cy2 - 10] not in trait_joueur_actuel2
                ):  # Si flèche haut est pressée

                    dy2 = -vitesse_tracage2
                    ligne(
                        cx2,
                        cy2 - (5 * (int(vitesse_tracage2 / 5))),
                        cx2,
                        cy2,
                        "white",
                        2,
                        tag="trait_joueur2",
                    )
                    historique_virage2.append(["Haut", [cx2, cy2]])
                    historique_deplacement2.append("Haut")

                    if (
                        historique_virage2[len(historique_virage2) - 1][0]
                        != historique_virage2[len(historique_virage2) - 2][0]
                    ):  # detecte un changement de direction
                        historique_positions2.append([cx2, cy2])

                if [cx2, cy2] not in trait_joueur_actuel2:
                    trait_joueur_actuel2.append(
                        [cx2, cy2]
                    )  # Référence toutes les positions du joueur à l'intérieur du terrain
                    if vitesse_tracage2 == 10 and len(historique_deplacement2) > 1:
                        if [cx2, cy2] in historique_positions2:
                            if historique_deplacement2[-2] == "Gauche":
                                trait_joueur_actuel2.insert(
                                    -2,
                                    [
                                        historique_virage2[-1][1][0] + 5,
                                        historique_virage2[-1][1][1],
                                    ],
                                )
                            if historique_deplacement2[-2] == "Droite":
                                trait_joueur_actuel2.insert(
                                    -2,
                                    [
                                        historique_virage2[-1][1][0] - 5,
                                        historique_virage2[-1][1][1],
                                    ],
                                )
                            if historique_deplacement2[-2] == "Haut":
                                trait_joueur_actuel2.insert(
                                    -2,
                                    [
                                        historique_virage2[-1][1][0],
                                        historique_virage2[-1][1][1] + 5,
                                    ],
                                )
                            if historique_deplacement2[-2] == "Bas":
                                trait_joueur_actuel2.insert(
                                    -2,
                                    [
                                        historique_virage2[-1][1][0],
                                        historique_virage2[-1][1][1] - 5,
                                    ],
                                )

                        else:

                            if historique_deplacement2[-1] == "Gauche":
                                trait_joueur_actuel2.insert(-2, [cx2 + 5, cy2])
                            if historique_deplacement2[-1] == "Droite":
                                trait_joueur_actuel2.insert(-2, [cx2 - 5, cy2])
                            if historique_deplacement2[-1] == "Haut":
                                trait_joueur_actuel2.insert(-2, [cx2, cy2 + 5])
                            if historique_deplacement2[-1] == "Bas":
                                trait_joueur_actuel2.insert(-2, [cx2, cy2 - 5])
        # JOUEUR 1
        if dx != 0 or dy != 0:  # Si le joueur a changé de position
            efface("joueur1")
            cx = cx + dx
            cy = cy + dy
            if touche_pressee("Left"):
                sprite = "ressources/Pacman1_gauche.png"
            if touche_pressee("Right"):
                sprite = "ressources/Pacman1_droite.png"
            if touche_pressee("Up"):
                sprite = "ressources/Pacman1_haut.png"
            if touche_pressee("Down"):
                sprite = "ressources/Pacman1_bas.png"
            joueur1(cx - 5, cy - 5, taille, sprite)

        if ([cx, cy] in zone_safe and len(trait_joueur_actuel) == 1) or (
            [cx, cy] in zone_safe and len(historique_positions) == 1
        ):  # Ne pose pas de problème de tracage de ligne lorsqu'on est dans la zone safe
            historique_positions.clear()
            trait_joueur_actuel.clear()

        # JOUEUR 2
        if deux == True:
            if dx2 != 0 or dy2 != 0:  # Si le joueur a changé de position
                efface("joueur2")
                cx2 = cx2 + dx2
                cy2 = cy2 + dy2
                if touche_pressee("q"):
                    sprite = "ressources/Pacman2_gauche.png"
                if touche_pressee("d"):
                    sprite = "ressources/Pacman2_droite.png"
                if touche_pressee("z"):
                    sprite = "ressources/Pacman2_haut.png"
                if touche_pressee("s"):
                    sprite = "ressources/Pacman2_bas.png"
                joueur2(cx2 - 5, cy2 - 5, taille, sprite)

            if ([cx2, cy2] in zone_safe and len(trait_joueur_actuel2) == 1) or (
                [cx2, cy2] in zone_safe and len(historique_positions2) == 1
            ):  # Ne pose pas de problème de tracage de ligne lorsqu'on est dans la zone safe
                historique_positions2.clear()
                trait_joueur_actuel2.clear()

        # -------------------------------Joueurs mangent des fruits-----------------------------------
        # JOUEUR 1
        if (cx, cy) in zone_pomme:

            if (cx, cy) in zone_pomme[0:3] and pomme1 == True:
                temps = time()
                efface("pomme1")
                pomme1 = False
                Invincibilite1 = True

            if (cx, cy) in zone_pomme[4:7] and pomme2 == True:
                temps = time()
                efface("pomme2")
                pomme2 = False
                Invincibilite1 = True

            if (cx, cy) in zone_pomme[8:11] and pomme3 == True:
                temps = time()
                efface("pomme3")
                pomme3 = False
                Invincibilite1 = True

            if (cx, cy) in zone_pomme[12:15] and pomme4 == True:
                temps = time()
                efface("pomme4")
                pomme4 = False
                Invincibilite1 = True

            if (cx, cy) in zone_pomme[16:19] and pomme5 == True:
                temps = time()
                efface("pomme5")
                pomme5 = False
                Invincibilite1 = True

            t = 0
        # JOUEUR 2
        if deux == True:
            if (cx2, cy2) in zone_pomme:

                if (cx2, cy2) in zone_pomme[0:3] and pomme1 == True:
                    temps = time()
                    efface("pomme1")
                    pomme1 = False
                    Invincibilite2 = True
                    couleur_sparks = "purple"
                    couleur_qix = "purple"

                if (cx2, cy2) in zone_pomme[4:7] and pomme2 == True:
                    temps = time()
                    efface("pomme2")
                    pomme2 = False
                    Invincibilite2 = True
                    couleur_sparks = "purple"
                    couleur_qix = "purple"

                if (cx2, cy2) in zone_pomme[8:11] and pomme3 == True:
                    temps = time()
                    efface("pomme3")
                    pomme3 = False
                    Invincibilite2 = True
                    couleur_sparks = "purple"
                    couleur_qix = "purple"

                if (cx2, cy2) in zone_pomme[12:15] and pomme4 == True:
                    temps = time()
                    efface("pomme4")
                    pomme4 = False
                    Invincibilite2 = True
                    couleur_sparks = "purple"
                    couleur_qix = "purple"

                if (cx2, cy2) in zone_pomme[16:19] and pomme5 == True:
                    temps = time()
                    efface("pomme5")
                    pomme5 = False
                    Invincibilite2 = True
                    couleur_sparks = "purple"
                    couleur_qix = "purple"

                t = 0

            if Invincibilite1 and time() - temps < 3:
                texte(
                    680,
                    400,
                    "Invincibilite",
                    couleur="yellow",
                    taille=16,
                    police="Copperplate Gothic Bold",
                    tag="Invincibilite1",
                )
            else:
                Invincibilite1 = False
                efface("Invincibilite1")

            if Invincibilite2 and time() - temps < 3:
                texte(
                    680,
                    710,
                    "Invincibilite",
                    couleur="yellow",
                    taille=16,
                    police="Copperplate Gothic Bold",
                    tag="Invincibilite2",
                )
            else:
                Invincibilite2 = False
                efface("Invincibilite2")

        else:
            if Invincibilite1 and time() - temps < 3:
                texte(
                    50,
                    170,
                    "Invincibilite",
                    couleur="yellow",
                    taille=16,
                    police="Copperplate Gothic Bold",
                    tag="Invincibilite1",
                )
            else:
                Invincibilite1 = False
                efface("Invincibilite1")
                couleur_sparks = "green"
                couleur_qix = "blue"

        # -------------------------------Changement de vitesse-----------------------------------

        if vitesse == True:

            if touche_pressee(touche_V) and [cx, cy] in zone_safe:
                touche_V = None
                efface("vitesse")

                if vitesse_tracage == 5:
                    vitesse_tracage += 5
                    texte(
                        475,
                        170,
                        "Rapide",
                        couleur="red",
                        taille=15,
                        police="Copperplate Gothic Bold",
                        tag="vitesse",
                    )

                elif vitesse_tracage == 10:
                    vitesse_tracage -= 5
                    texte(
                        475,
                        170,
                        "Lente",
                        couleur="green",
                        taille=15,
                        police="Copperplate Gothic Bold",
                        tag="vitesse",
                    )

            if deux == True:
                if touche_pressee(touche_V2) and [cx2, cy2] in zone_safe:
                    touche_V2 = None
                    efface("vitesse2")

                    if vitesse_tracage2 == 5:
                        vitesse_tracage2 += 5
                        texte(
                            600,
                            170,
                            "Rapide",
                            couleur="red",
                            taille=15,
                            police="Copperplate Gothic Bold",
                            tag="vitesse2",
                        )

                    elif vitesse_tracage2 == 10:
                        vitesse_tracage2 -= 5
                        texte(
                            600,
                            170,
                            "Lente",
                            couleur="green",
                            taille=15,
                            police="Copperplate Gothic Bold",
                            tag="vitesse2",
                        )

        # ------------------------------------CREATION D'UN POLYGONE-----------------------------------------

        # JOUEUR 1
        if deux == True:
            if (
                [cx2, cy2] in zone_safe
                and historique_positions2 != []
                and len(historique_positions2) > 1
                or [cx2, cy2] in zone_safe
                and len(historique_positions2) == 1
                and [cx2, cy2] != historique_positions2[0]
            ):
                possible = True
            else:
                possible = False
        else:
            possible = False

        if (
            [cx, cy] in zone_safe
            and historique_positions != []
            and len(historique_positions) > 1
            or [cx, cy] in zone_safe
            and len(historique_positions) == 1
            and [cx, cy] != historique_positions[0]
        ) or possible == True:
            quel_joueur = 0
            if deux == True:
                if (
                    [cx, cy] in zone_safe
                    and historique_positions != []
                    and len(historique_positions) > 1
                    or [cx, cy] in zone_safe
                    and len(historique_positions) == 1
                    and [cx, cy] != historique_positions[0]
                ):
                    touche_V = "Suppr"
                    touche_espace = None
                    zone_interieure = (
                        []
                    )  # J'initialise cette zone avant les autres pour pouvoir rajouter les coins qui vont être sHautprimés
                    historique_positions.append(
                        [cx, cy]
                    )  # Ajout de la dernière position, celle quand est dans la zone safe
                    if vitesse_tracage == 10:
                        if vitesse_tracage == 10 and len(historique_deplacement) > 1:

                            if historique_deplacement[-1] == "Gauche":
                                trait_joueur_actuel.insert(-2, [cx + 5, cy])
                            if historique_deplacement[-1] == "Droite":
                                trait_joueur_actuel.insert(-2, [cx - 5, cy])
                            if historique_deplacement[-1] == "Haut":
                                trait_joueur_actuel.insert(-2, [cx, cy + 5])
                            if historique_deplacement[-1] == "Bas":
                                trait_joueur_actuel.insert(-2, [cx, cy - 5])
                    quel_joueur = 1

                else:
                    touche_V2 = "v"
                    touche_espace2 = None
                    zone_interieure = (
                        []
                    )  # J'initialise cette zone avant les autres pour pouvoir rajouter les coins qui vont être sHautprimés
                    historique_positions2.append(
                        [cx2, cy2]
                    )  # Ajout de la dernière position, celle quand est dans la zone safe
                    if vitesse_tracage2 == 10:
                        if vitesse_tracage2 == 10 and len(historique_deplacement2) > 1:

                            if historique_deplacement2[-1] == "Gauche":
                                trait_joueur_actuel2.insert(-2, [cx + 5, cy])
                            if historique_deplacement2[-1] == "Droite":
                                trait_joueur_actuel2.insert(-2, [cx - 5, cy])
                            if historique_deplacement2[-1] == "Haut":
                                trait_joueur_actuel2.insert(-2, [cx, cy + 5])
                            if historique_deplacement2[-1] == "Bas":
                                trait_joueur_actuel2.insert(-2, [cx, cy - 5])
                    quel_joueur = 2
            else:
                touche_V = "v"
                touche_espace = None
                zone_interieure = (
                    []
                )  # J'initialise cette zone avant les autres pour pouvoir rajouter les coins qui vont être sHautprimés
                historique_positions.append(
                    [cx, cy]
                )  # Ajout de la dernière position, celle quand est dans la zone safe
                if vitesse_tracage == 10:
                    if vitesse_tracage == 10 and len(historique_deplacement) > 1:

                        if historique_deplacement[-1] == "Gauche":
                            trait_joueur_actuel.insert(-2, [cx + 5, cy])
                        if historique_deplacement[-1] == "Droite":
                            trait_joueur_actuel.insert(-2, [cx - 5, cy])
                        if historique_deplacement[-1] == "Haut":
                            trait_joueur_actuel.insert(-2, [cx, cy + 5])
                        if historique_deplacement[-1] == "Bas":
                            trait_joueur_actuel.insert(-2, [cx, cy - 5])

            # ------------------------------------Tri sens horaire des coins-----------------------------------------
            historique_coin.append("Gauche")
            coin_apres_tri.clear()

            if quel_joueur == 2:
                xAutrePoint, yAutrePoint = (
                    historique_positions2[-1][0],
                    historique_positions2[-1][1],
                )
                historique_positions_choisi = historique_positions2
            else:
                xAutrePoint, yAutrePoint = (
                    historique_positions[-1][0],
                    historique_positions[-1][1],
                )
                historique_positions_choisi = historique_positions

            weight_proximite = 0.3

            point_optimal = min(
                zone_safe,
                key=lambda point: (1 - weight_proximite)
                * ((point[0] - xQIX) ** 2 + (point[1] - yQIX) ** 2)
                + weight_proximite
                * -((point[0] - xAutrePoint) ** 2 + (point[1] - yAutrePoint) ** 2),
            )

            [xcoin, ycoin] = point_optimal

            for i in range(len(zone_safe)):
                dxcoin = 0
                dycoin = 0
                if (
                    [xcoin, ycoin] in coin
                    or [xcoin, ycoin] in historique_positions_choisi
                    or [xcoin, ycoin] in zone_interieure
                ):
                    if [xcoin, ycoin] not in coin_apres_tri:
                        coin_apres_tri.append([xcoin, ycoin])
                if [xcoin - 5, ycoin] in zone_safe and historique_coin[
                    -1
                ] != "Droite":  # gauche
                    dxcoin = -5
                    historique_coin.append("Gauche")
                elif [xcoin, ycoin + 5] in zone_safe and historique_coin[
                    -1
                ] != "Haut":  #  bas
                    dycoin = 5
                    historique_coin.append("Bas")
                elif [xcoin + 5, ycoin] in zone_safe and historique_coin[
                    -1
                ] != "Gauche":  #  droite
                    dxcoin = 5
                    historique_coin.append("Droite")
                elif [xcoin, ycoin - 5] in zone_safe and historique_coin[
                    -1
                ] != "Bas":  #  haut
                    dycoin = -5
                    historique_coin.append("Haut")
                if dxcoin != 0 or dycoin != 0:
                    xcoin += dxcoin
                    ycoin += dycoin

            coin.clear()
            for element in coin_apres_tri:
                coin.append(element)

            # ------------------------------------Tri sens horaire de la zone safe pour référencer la nouvelle-----------------------------------------
            zone_safe_apres_tri.clear()
            historique_zone_safe.append("Gauche")

            [xsafe, ysafe] = point_optimal

            for i in range(len(zone_safe)):
                dxsafe = 0
                dysafe = 0
                if [xsafe, ysafe] not in zone_safe_apres_tri:
                    zone_safe_apres_tri.append([xsafe, ysafe])

                if [xsafe - 5, ysafe] in zone_safe and historique_zone_safe[
                    -1
                ] != "Droite":  # gauche
                    dxsafe = -5
                    historique_zone_safe.append("Gauche")
                elif [xsafe, ysafe + 5] in zone_safe and historique_zone_safe[
                    -1
                ] != "Haut":  #  bas
                    dysafe = 5
                    historique_zone_safe.append("Bas")
                elif [xsafe + 5, ysafe] in zone_safe and historique_zone_safe[
                    -1
                ] != "Gauche":  #  droite
                    dxsafe = 5
                    historique_zone_safe.append("Droite")
                elif [xsafe, ysafe - 5] in zone_safe and historique_zone_safe[
                    -1
                ] != "Bas":  #  haut
                    dysafe = -5
                    historique_zone_safe.append("Haut")
                if dxsafe != 0 or dysafe != 0:
                    xsafe += dxsafe
                    ysafe += dysafe

            # ------------------------------------Délimitation du polygone et mise à jour de la zone safe-----------------------------------------
            for (
                element
            ) in (
                zone_safe
            ):  # Délimite la zone exterieure au cas ou il faut switcher de zone vu que le QIX est dans la mauvaise partie du terrain
                if element not in zone_safe_apres_tri:
                    zone_safe_temp.append(element)

            if quel_joueur == 0 or quel_joueur == 1:
                for element in trait_joueur_actuel:
                    zone_safe_temp.append(element)

            elif quel_joueur == 2:
                for element in trait_joueur_actuel2:
                    zone_safe_temp.append(element)

            # zone_safe_temp.append(historique_positions[-1])

            zone_safe.clear()  # On reinitialise la zone safe
            for (
                element
            ) in (
                zone_safe_apres_tri
            ):  # On ajoute a la zone safe, la zone safe triée en sens horaire
                zone_safe.append(element)

            premier_point = historique_positions_choisi[
                0
            ]  # On delimite le premier et le dernier point du trait du polygone tracé
            dernier_point = historique_positions_choisi[-1]
            coin1_poly = zone_safe.index(premier_point)
            coin2_poly = zone_safe.index(dernier_point)

            if quel_joueur == 2:
                trait_joueur_actuel_choisi = trait_joueur_actuel2
            else:
                trait_joueur_actuel_choisi = trait_joueur_actuel

            if (
                coin2_poly > coin1_poly
            ):  # Enleve la partie de la zone safe à sHautprimer et ajoute le trait joueur à la zone safe
                for element in reversed(zone_safe[coin1_poly + 1 : coin2_poly]):
                    zone_safe.remove(element)
                    zone_safe_temp.append(element)
                    if element in coin:
                        coin.remove(element)
                        zone_interieure.append(element)

                for i in range(len(trait_joueur_actuel_choisi)):
                    if trait_joueur_actuel_choisi[i] not in zone_safe:
                        zone_safe.insert(coin1_poly + i, trait_joueur_actuel_choisi[i])

            else:
                for element in zone_safe[coin2_poly + 1 : coin1_poly]:
                    zone_safe.remove(element)
                    zone_safe_temp.append(element)
                    if element in coin:
                        coin.remove(element)
                        zone_interieure.append(element)

                for i in range(len(trait_joueur_actuel_choisi)):
                    if trait_joueur_actuel_choisi[i] not in zone_safe:
                        zone_safe.insert(coin2_poly + i, trait_joueur_actuel_choisi[i])

            for (
                element
            ) in (
                historique_positions_choisi
            ):  # Ajoute tout les nouveaux coins au polygone à tracer
                zone_interieure.append(element)

            for (
                element
            ) in (
                historique_positions_choisi
            ):  # Ajoute tout les nouveaux coins à la liste des coins
                coin.append(element)

            # ------------------------------------ Surface recouverte par le polygone -----------------------------------------
            n = len(zone_polygone)
            aire = (n * 100) / nb_positions

            surface_polygone += aire
            if deux == True:
                surface_polygone_joueur1 += aire
                surface_polygone_joueur2 += aire
            # ------------- ----------------------- Zone intérieure des polygones -----------------------------------------

            def est_point_dans_polygone(x, y, polygone):
                n = len(polygone)  # Nombre de sommets du polygone
                est_a_l_interieur = False

                for i in range(n):
                    xi, yi = polygone[i]  # Coordonnees du 1er sommet
                    xj, yj = polygone[(i + 1) % n]  # Coordonnées du 2eme sommet

                    condition1 = (yi <= y <= yj) or (
                        yj <= y <= yi
                    )  # Vérifie si les points se trouvent entre les deux extrémités
                    sur_le_bord = (
                        (y == yi and min(xi, xj) <= x <= max(xi, xj))
                        or (y == yj and min(xi, xj) <= x <= max(xi, xj))
                        or (x == xi and min(yi, yj) <= y <= max(yi, yj))
                        or (x == xj and min(yi, yj) <= y <= max(yi, yj))
                    )

                    if condition1 or sur_le_bord:
                        if yi != yj:
                            condition2 = (
                                x > (xj - xi) * (y - yi) / (yj - yi) + xi
                            )  # Vérifie si le rayon horizontal partant du point croise le segment
                        else:
                            condition2 = False

                        if condition2:
                            est_a_l_interieur = (
                                not est_a_l_interieur
                            )  # Si cette condition est vrai, le point est à l'intérieur

                return est_a_l_interieur

            def generer_positions_interieures(polygone):
                xmin = min(p[0] for p in polygone)
                ymin = min(p[1] for p in polygone)
                xmax = max(p[0] for p in polygone)
                ymax = max(p[1] for p in polygone)

                positions_interieures = []

                for x in range(xmin, xmax + 1, 5):
                    for y in range(
                        ymin, ymax + 1, 5
                    ):  # Parcours toutes les coordonnées possibles
                        point = [x, y]

                        if est_point_dans_polygone(x, y, polygone):
                            positions_interieures.append(point)
                return positions_interieures

            for element in generer_positions_interieures(zone_interieure):
                if element not in zone_polygone_actuelle:
                    zone_polygone_actuelle.append(element)

            for element in zone_polygone_actuelle:
                if element in zone_terrain:
                    zone_terrain.remove(element)

            # ------------------------------------Détermine dans quelle partie du terrain se trouve le QIX-----------------------------------------

            if [xQIX, yQIX] in zone_polygone_actuelle:
                echanger_listes(zone_terrain, zone_polygone_actuelle)
                echanger_listes(zone_safe, zone_safe_temp)
                echanger_listes(coin, zone_interieure)

            for element in zone_polygone_actuelle:
                if element in zone_terrain:
                    zone_terrain.remove(element)
                if element not in zone_polygone:
                    zone_polygone.append(element)

            # ------------------------------------Réinitialisation de tout les historiques-----------------------------------------

            if deux == True:
                touche_espace = "m"
                touche_espace2 = "space"
            else:
                touche_espace = "space"

            if quel_joueur == 1 or quel_joueur == 0:
                trait_joueur_actuel.clear()
                iteration = 0
                historique_positions.clear()
                historique_deplacement.clear()

            elif quel_joueur == 2:
                trait_joueur_actuel2.clear()
                iteration2 = 0
                historique_positions2.clear()
                historique_deplacement2.clear()

            zone_safe_temp.clear()
            zone_safe_apres_tri.clear()
            historique_coin.clear()
            coin_apres_tri.clear()

            # ------------------------------------Tracage du polygone--------------------------------------
            couleur_choisie = randint(0, len(lst_couleur) - 1)
            polygone(
                zone_interieure,
                "midnightblue",
                remplissage=lst_couleur[couleur_choisie],
                epaisseur=5,
            )
            lst_couleur.remove(lst_couleur[couleur_choisie])
            if obstacle_predefini == True:
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
            if obstacle_aleatoire == True:
                efface("obstacle1")
                efface("obstacle2")
                efface("obstacle3")
                rectangle(
                    xobstacle1,
                    yobstacle1,
                    xobstacle1 + taille_obstacle1,
                    yobstacle1 + taille_obstacle1,
                    "gray",
                    "gray",
                    tag="obstacle1",
                )
                rectangle(
                    xobstacle2,
                    yobstacle2,
                    xobstacle2 + taille_obstacle2,
                    yobstacle2 + taille_obstacle2,
                    "gray",
                    "gray",
                    tag="obstacle2",
                )
                rectangle(
                    xobstacle3,
                    yobstacle3,
                    xobstacle3 + taille_obstacle3,
                    yobstacle3 + taille_obstacle3,
                    "gray",
                    "gray",
                    tag="obstacle3",
                )
            nb_polygone += 1

            # ------------------------------------Surface conquise en pourcentage-----------------------------------------

            surface_totale = 100 * 110
            surface_polygone = len(zone_polygone)
            surface_polygone_actuel = len(zone_polygone_actuelle)
            zone_polygone_actuelle.clear()
            surface_recouverte = surface_polygone * 100 / surface_totale

            efface("score_pourcentage")
            if deux == True:
                texte(
                    700,
                    110,
                    int(surface_recouverte),
                    couleur="white",
                    taille=16,
                    police="Copperplate Gothic Bold",
                    tag="score_pourcentage",
                )
            else:
                texte(
                    235,
                    110,
                    int(surface_recouverte),
                    couleur="white",
                    taille=16,
                    police="Copperplate Gothic Bold",
                    tag="score_pourcentage",
                )

            # ------------------------------------Score-----------------------------------------
            score_max = 20000
            if deux == True:
                if quel_joueur == 1:
                    if vitesse_tracage == 5:
                        score1 += surface_polygone_actuel * score_max / surface_totale
                    elif vitesse_tracage == 10:
                        score1 += (
                            (surface_polygone_actuel / 2) * score_max / surface_totale
                        )
                    if scorev == True:
                        efface("score_joueur1")
                        texte(
                            770,
                            250,
                            int(score1),
                            couleur="white",
                            taille=16,
                            police="Copperplate Gothic Bold",
                            tag="score_joueur1",
                        )
                if quel_joueur == 2:
                    if vitesse_tracage2 == 5:
                        score2 += surface_polygone_actuel * score_max / surface_totale
                    elif vitesse_tracage2 == 10:
                        score2 += (
                            (surface_polygone_actuel / 2) * score_max / surface_totale
                        )
                    if scorev == True:
                        efface("score_joueur2")
                        texte(
                            770,
                            550,
                            int(score2),
                            couleur="white",
                            taille=16,
                            police="Copperplate Gothic Bold",
                            tag="score_joueur2",
                        )
            else:
                if vitesse_tracage == 5:
                    score += surface_polygone_actuel * score_max / surface_totale
                elif vitesse_tracage == 10:
                    score += (surface_polygone_actuel / 2) * score_max / surface_totale

                if scorev == True:
                    efface("score_total")
                    texte(
                        420,
                        110,
                        int(score),
                        couleur="white",
                        taille=16,
                        police="Copperplate Gothic Bold",
                        tag="score_total",
                    )

            # ------------------------------------Victoire-----------------------------------------
            if deux == True:
                if quel_joueur == 1 or quel_joueur == 2:
                    if surface_recouverte >= 75:
                        efface("coeur3")
                        efface("sparks1")
                        efface("sparks2")
                        efface("sparks3")
                        efface("sparks4")
                        efface("sparks5")
                        efface("sparks6")
                        efface("Fantome_QIX")
                        efface("joueur1")
                        run = False
                        rectangle(50, 200, 550, 750, "white", "black", 3)
                        texte(
                            130,
                            550,
                            "Surface conquise:",
                            couleur="white",
                            taille=20,
                            police="Copperplate Gothic Bold",
                        )
                        texte(
                            420,
                            550,
                            int(surface_recouverte),
                            couleur="blue",
                            taille=20,
                            police="Copperplate Gothic Bold",
                        )
                        texte(
                            460,
                            550,
                            "%",
                            couleur="blue",
                            taille=20,
                            police="Copperplate Gothic Bold",
                        )
                        if scorev == True and score1 > score2:
                            texte(
                                300,
                                450,
                                "JOUEUR 1 À GAGNÉ",
                                couleur="green",
                                taille=30,
                                police="Copperplate Gothic Bold",
                                ancrage="center",
                            )
                            texte(
                                170,
                                470,
                                "Score joueur 1:",
                                couleur="white",
                                taille=20,
                                police="Copperplate Gothic Bold",
                            )
                            texte(
                                450,
                                470,
                                int(score1),
                                couleur="red",
                                taille=20,
                                police="Copperplate Gothic Bold",
                            )
                            texte(
                                170,
                                500,
                                "Score joueur 2:",
                                couleur="white",
                                taille=20,
                                police="Copperplate Gothic Bold",
                            )
                            texte(
                                450,
                                500,
                                int(score2),
                                couleur="red",
                                taille=20,
                                police="Copperplate Gothic Bold",
                            )
                        elif scorev == True and score2 > score1:
                            texte(
                                300,
                                450,
                                "JOUEUR 2 À GAGNÉ",
                                couleur="green",
                                taille=30,
                                police="Copperplate Gothic Bold",
                                ancrage="center",
                            )
                            texte(
                                170,
                                500,
                                "Score joueur 2:",
                                couleur="white",
                                taille=20,
                                police="Copperplate Gothic Bold",
                            )
                            texte(
                                450,
                                500,
                                int(score2),
                                couleur="red",
                                taille=20,
                                police="Copperplate Gothic Bold",
                            )
                            texte(
                                170,
                                470,
                                "Score joueur 1:",
                                couleur="white",
                                taille=20,
                                police="Copperplate Gothic Bold",
                            )
                            texte(
                                450,
                                470,
                                int(score1),
                                couleur="red",
                                taille=20,
                                police="Copperplate Gothic Bold",
                            )
                        else:
                            texte(
                                300,
                                450,
                                "GAGNÉ",
                                couleur="green",
                                taille=40,
                                police="Copperplate Gothic Bold",
                                ancrage="center",
                            )

            else:
                if surface_recouverte >= 75:
                    xQIX, yQIX = 150, 300
                    efface("coeur3")
                    efface("sparks1")
                    efface("sparks2")
                    efface("sparks3")
                    efface("sparks4")
                    efface("sparks5")
                    efface("sparks6")
                    efface("Fantome_QIX")
                    efface("joueur1")
                    run = False
                    rectangle(50, 200, 550, 750, "white", "black", 3)
                    texte(
                        300,
                        450,
                        "GAGNÉ",
                        couleur="green",
                        taille=40,
                        police="Copperplate Gothic Bold",
                        ancrage="center",
                    )
                    if scorev == True:
                        texte(
                            170,
                            470,
                            "Votre score:",
                            couleur="white",
                            taille=20,
                            police="Copperplate Gothic Bold",
                        )
                        texte(
                            370,
                            470,
                            int(score),
                            couleur="red",
                            taille=20,
                            police="Copperplate Gothic Bold",
                        )
                    texte(
                        130,
                        500,
                        "Surface conquise:",
                        couleur="white",
                        taille=20,
                        police="Copperplate Gothic Bold",
                    )
                    texte(
                        420,
                        500,
                        int(surface_recouverte),
                        couleur="blue",
                        taille=20,
                        police="Copperplate Gothic Bold",
                    )
                    texte(
                        460,
                        500,
                        "%",
                        couleur="blue",
                        taille=20,
                        police="Copperplate Gothic Bold",
                    )
            # ------------------------------------Si un joueur se fait enfermer par l'autre-----------------------------------------
            if deux == True:
                if quel_joueur == 2:
                    if ([cx, cy] not in zone_safe and [cx, cy] not in zone_terrain) or [
                        cx,
                        cy,
                    ] in zone_polygone:  # Si le joueur 1 est enfermé par joueur 2
                        cx, cy = cx2, cy2
                        iteration = 0

                        historique_deplacement.clear()
                        trait_joueur_actuel.clear()
                        historique_positions.clear()

                        efface("trait_joueur")
                        efface("joueur1")

                        joueur1(cx - 5, cy - 5, taille, "ressources/Pacman1_haut.png")
                        Nombre_vie -= 1
                        if Nombre_vie == 2:
                            efface("coeur1")
                        if Nombre_vie == 1:
                            efface("coeur2")
                        if Nombre_vie == 0:
                            efface("coeur3")
                            efface("sparks2")
                            efface("sparks1")
                            efface("Fantome_QIX")
                            efface("joueur1")
                            efface("joueur2")
                            texte(
                                300,
                                450,
                                "JOUEUR 2 À GAGNÉ",
                                couleur="green",
                                taille=30,
                                police="Copperplate Gothic Bold",
                                ancrage="center",
                            )
                            if scorev == True:
                                texte(
                                    170,
                                    470,
                                    "Score joueur 1:",
                                    couleur="white",
                                    taille=20,
                                    police="Copperplate Gothic Bold",
                                )
                                texte(
                                    450,
                                    470,
                                    int(score1),
                                    couleur="red",
                                    taille=20,
                                    police="Copperplate Gothic Bold",
                                )
                                texte(
                                    170,
                                    500,
                                    "Score joueur 2:",
                                    couleur="white",
                                    taille=20,
                                    police="Copperplate Gothic Bold",
                                )
                                texte(
                                    450,
                                    500,
                                    int(score2),
                                    couleur="red",
                                    taille=20,
                                    police="Copperplate Gothic Bold",
                                )
                            run = False
                        sleep(0.5)
                else:
                    if (
                        [cx2, cy2] not in zone_safe and [cx2, cy2] not in zone_terrain
                    ) or [
                        cx2,
                        cy2,
                    ] in zone_polygone:  # Si le joueur 2 est enfermé par joueur 1
                        cx2, cy2 = cx, cy
                        iteration2 = 0

                        historique_deplacement2.clear()
                        trait_joueur_actuel2.clear()
                        historique_positions2.clear()

                        efface("trait_joueur2")
                        efface("joueur2")

                        joueur2(cx2 - 5, cy2 - 5, taille, "ressources/Pacman2_haut.png")
                        Nombre_vie2 -= 1
                        if Nombre_vie2 == 2:
                            efface("coeur1_2")
                        if Nombre_vie2 == 1:
                            efface("coeur2_2")
                        if Nombre_vie2 == 0:
                            efface("coeur3_2")
                            efface("sparks2")
                            efface("sparks1")
                            efface("Fantome_QIX")
                            efface("joueur1")
                            efface("joueur2")
                            texte(
                                300,
                                450,
                                "JOUEUR 1 À GAGNÉ",
                                couleur="green",
                                taille=30,
                                police="Copperplate Gothic Bold",
                                ancrage="center",
                            )
                            if scorev == True:
                                texte(
                                    170,
                                    470,
                                    "Score joueur 1:",
                                    couleur="white",
                                    taille=20,
                                    police="Copperplate Gothic Bold",
                                )
                                texte(
                                    450,
                                    470,
                                    int(score1),
                                    couleur="red",
                                    taille=20,
                                    police="Copperplate Gothic Bold",
                                )
                                texte(
                                    170,
                                    500,
                                    "Score joueur 2:",
                                    couleur="white",
                                    taille=20,
                                    police="Copperplate Gothic Bold",
                                )
                                texte(
                                    450,
                                    500,
                                    int(score2),
                                    couleur="red",
                                    taille=20,
                                    police="Copperplate Gothic Bold",
                                )
                            run = False
                        sleep(0.5)

        # ------------------------------------Si un joueur croise la ligne d'un autre joueur -----------------------------------------
        if deux == True:
            if [
                cx,
                cy,
            ] in trait_joueur_actuel2:  # Si le joueur 1 croise la ligne du joueur 2

                if score1 > 0:
                    cx, cy = historique_positions[0][0], historique_positions[0][1]
                else:
                    cx, cy = 550, 750

                iteration = 0

                historique_deplacement.clear()
                trait_joueur_actuel.clear()
                historique_positions.clear()

                efface("trait_joueur")
                efface("joueur1")

                joueur1(cx - 5, cy - 5, taille, "ressources/Pacman1_haut.png")
                Nombre_vie -= 1
                if Nombre_vie == 2:
                    efface("coeur1")
                if Nombre_vie == 1:
                    efface("coeur2")
                if Nombre_vie == 0:
                    efface("coeur3")
                    efface("sparks2")
                    efface("sparks1")
                    efface("Fantome_QIX")
                    efface("joueur1")
                    efface("joueur2")
                    texte(
                        300,
                        450,
                        "JOUEUR 2 À GAGNÉ",
                        couleur="green",
                        taille=30,
                        police="Copperplate Gothic Bold",
                        ancrage="center",
                    )
                    if scorev == True:
                        texte(
                            170,
                            470,
                            "Score joueur 1:",
                            couleur="white",
                            taille=20,
                            police="Copperplate Gothic Bold",
                        )
                        texte(
                            450,
                            470,
                            int(score1),
                            couleur="red",
                            taille=20,
                            police="Copperplate Gothic Bold",
                        )
                        texte(
                            170,
                            500,
                            "Score joueur 2:",
                            couleur="white",
                            taille=20,
                            police="Copperplate Gothic Bold",
                        )
                        texte(
                            450,
                            500,
                            int(score2),
                            couleur="red",
                            taille=20,
                            police="Copperplate Gothic Bold",
                        )
                    run = False
                sleep(0.5)

            if [
                cx2,
                cy2,
            ] in trait_joueur_actuel:  # Si le joueur 2 croise la ligne du joueur 1

                if score2 > 0:
                    cx2, cy2 = historique_positions2[0][0], historique_positions2[0][1]
                else:
                    cx2, cy2 = 50, 750

                iteration2 = 0

                historique_deplacement2.clear()
                trait_joueur_actuel2.clear()
                historique_positions2.clear()

                efface("trait_joueur2")
                efface("joueur2")

                joueur2(cx2 - 5, cy2 - 5, taille, "ressources/Pacman2_haut.png")
                Nombre_vie2 -= 1
                if Nombre_vie2 == 2:
                    efface("coeur1_2")
                if Nombre_vie2 == 1:
                    efface("coeur2_2")
                if Nombre_vie2 == 0:
                    efface("coeur3_2")
                    efface("sparks2")
                    efface("sparks1")
                    efface("Fantome_QIX")
                    efface("joueur1")
                    efface("joueur2")
                    texte(
                        300,
                        450,
                        "JOUEUR 1 À GAGNÉ",
                        couleur="green",
                        taille=30,
                        police="Copperplate Gothic Bold",
                        ancrage="center",
                    )
                    if scorev == True:
                        texte(
                            170,
                            470,
                            "Score joueur 1:",
                            couleur="white",
                            taille=20,
                            police="Copperplate Gothic Bold",
                        )
                        texte(
                            450,
                            470,
                            int(score1),
                            couleur="red",
                            taille=20,
                            police="Copperplate Gothic Bold",
                        )
                        texte(
                            170,
                            500,
                            "Score joueur 2:",
                            couleur="white",
                            taille=20,
                            police="Copperplate Gothic Bold",
                        )
                        texte(
                            450,
                            500,
                            int(score2),
                            couleur="red",
                            taille=20,
                            police="Copperplate Gothic Bold",
                        )
                    run = False
                sleep(0.5)

        # ------------------------------------Définition du QIX-----------------------------------------

        fx = 0
        fy = 0

        if (
            randrange(100) < vitesse_QIX
        ):  # Changer la direction aleatoirement environ 10% du temps
            fx = 5 * randint(-longueur_deplacement_QIX, longueur_deplacement_QIX)
            fy = 5 * randint(-longueur_deplacement_QIX, longueur_deplacement_QIX)

        nouveau_x, nouveau_y = xQIX + fx, yQIX + fy

        # verifie le position de la safe zone
        if (
            [nouveau_x - 20, nouveau_y - 20] not in zone_safe
            and [nouveau_x + 20, nouveau_y + 20] not in zone_safe
            and [nouveau_x - 20, nouveau_y - 20] not in zone_polygone
            and [nouveau_x + 20, nouveau_y + 20] not in zone_polygone
            and [nouveau_x - 20, nouveau_y - 20] not in zone_obstacle
            and [nouveau_x + 20, nouveau_y + 20] not in zone_obstacle
        ):
            # and [nouveau_x-20,nouveau_y-20]  in zone_terrain and [nouveau_x+20,nouveau_y+20] in zone_terrain

            xQIX, yQIX = nouveau_x, nouveau_y

        # Garde de le Qix à l'intérieur du terrain
        if xQIX < 70:
            xQIX = 70
            fx = abs(fx)
        elif xQIX > 530:
            xQIX = 530
            fx = -abs(fx)
        if yQIX < 220:
            yQIX = 220
            fy = abs(fy)
        elif yQIX > 730:
            yQIX = 730
            fy = -abs(fy)

        efface("Fantome_QIX")
        if Invincibilite1 == True or Invincibilite2 == True:
            sprite_actuel_QIX = "ressources/Fantome_fruit.png"
        else:
            sprite_actuel_QIX = "ressources/Fantome_qix.png"

        QIX = image(
            xQIX - 20,
            yQIX - 20,
            sprite_actuel_QIX,
            largeur=40,
            hauteur=40,
            tag="Fantome_QIX",
        )
        for i in range(int(xQIX - 20), int(xQIX + 20)):
            position_qix.append([i, int(yQIX - 20)])
            position_qix.append([i, int(yQIX + 20)])
        for i in range(int(yQIX - 20), int(yQIX + 20)):
            position_qix.append([int(xQIX - 20), i])
            position_qix.append([int(xQIX + 20), i])

        if deux == True:
            for (
                element
            ) in trait_joueur_actuel:  # Si le QIX touche un chemin du joueur 1
                if element in position_qix and Invincibilite1 == False:

                    if score > 0:
                        cx, cy = historique_positions[0][0], historique_positions[0][1]
                    else:
                        if deux == True:
                            cx, cy = 550, 750
                        else:
                            cx, cy = 300, 750
                    iteration = 0

                    historique_deplacement.clear()
                    trait_joueur_actuel.clear()
                    historique_positions.clear()

                    efface("trait_joueur")
                    efface("joueur1")

                    joueur1(cx - 5, cy - 5, taille, "ressources/Pacman1_haut.png")
                    Nombre_vie -= 1
                    if Nombre_vie == 2:
                        efface("coeur1")
                    if Nombre_vie == 1:
                        efface("coeur2")
                    if Nombre_vie == 0:
                        efface("coeur3")
                        efface("sparks2")
                        efface("sparks1")
                        efface("Fantome_QIX")
                        efface("joueur1")
                        efface("joueur2")
                        if deux == False:
                            texte(
                                300,
                                450,
                                "GAME OVER",
                                couleur="red",
                                taille=40,
                                police="Copperplate Gothic Bold",
                                ancrage="center",
                            )
                        else:
                            texte(
                                300,
                                450,
                                "JOUEUR 2 À GAGNÉ",
                                couleur="green",
                                taille=30,
                                police="Copperplate Gothic Bold",
                                ancrage="center",
                            )
                            if scorev == True:
                                texte(
                                    170,
                                    470,
                                    "Score joueur 1:",
                                    couleur="white",
                                    taille=20,
                                    police="Copperplate Gothic Bold",
                                )
                                texte(
                                    450,
                                    470,
                                    int(score1),
                                    couleur="red",
                                    taille=20,
                                    police="Copperplate Gothic Bold",
                                )
                                texte(
                                    170,
                                    500,
                                    "Score joueur 2:",
                                    couleur="white",
                                    taille=20,
                                    police="Copperplate Gothic Bold",
                                )
                                texte(
                                    450,
                                    500,
                                    int(score2),
                                    couleur="red",
                                    taille=20,
                                    police="Copperplate Gothic Bold",
                                )
                        run = False
                    sleep(0.5)
                    break

            for (
                element
            ) in trait_joueur_actuel2:  # Si le QIX touche un chemin du joueur 2
                if element in position_qix and Invincibilite2 == False:

                    if score2 > 0:
                        cx2, cy2 = (
                            historique_positions2[0][0],
                            historique_positions2[0][1],
                        )
                    else:
                        cx2, cy2 = 50, 750
                    iteration2 = 0

                    historique_deplacement2.clear()
                    trait_joueur_actuel2.clear()
                    historique_positions2.clear()

                    efface("trait_joueur2")
                    efface("joueur2")

                    joueur2(cx2 - 5, cy2 - 5, taille, "ressources/Pacman2_haut.png")
                    Nombre_vie2 -= 1
                    if Nombre_vie2 == 2:
                        efface("coeur1_2")
                    if Nombre_vie2 == 1:
                        efface("coeur2_2")
                    if Nombre_vie2 == 0:
                        efface("coeur3_2")
                        efface("sparks2")
                        efface("sparks1")
                        efface("Fantome_QIX")
                        efface("joueur1")
                        efface("joueur2")
                        if deux == False:
                            texte(
                                300,
                                450,
                                "GAME OVER",
                                couleur="red",
                                taille=40,
                                police="Copperplate Gothic Bold",
                                ancrage="center",
                            )
                        else:
                            texte(
                                300,
                                450,
                                "JOUEUR 1 À GAGNÉ",
                                couleur="green",
                                taille=30,
                                police="Copperplate Gothic Bold",
                                ancrage="center",
                            )
                            if scorev == True:
                                texte(
                                    170,
                                    470,
                                    "Score joueur 1:",
                                    couleur="white",
                                    taille=20,
                                    police="Copperplate Gothic Bold",
                                )
                                texte(
                                    450,
                                    470,
                                    int(score1),
                                    couleur="red",
                                    taille=20,
                                    police="Copperplate Gothic Bold",
                                )
                                texte(
                                    170,
                                    500,
                                    "Score joueur 2:",
                                    couleur="white",
                                    taille=20,
                                    police="Copperplate Gothic Bold",
                                )
                                texte(
                                    450,
                                    500,
                                    int(score2),
                                    couleur="red",
                                    taille=20,
                                    police="Copperplate Gothic Bold",
                                )
                        run = False
                    sleep(0.5)
                    break

        else:
            for (
                element
            ) in trait_joueur_actuel:  # Si le QIX touche un chemin du joueur 1
                if element in position_qix and Invincibilite1 == False:

                    if score > 0:
                        cx, cy = historique_positions[0][0], historique_positions[0][1]
                    else:
                        if deux == True:
                            cx, cy = 550, 750
                        else:
                            cx, cy = 300, 750
                    iteration = 0

                    historique_deplacement.clear()
                    trait_joueur_actuel.clear()
                    historique_positions.clear()

                    efface("trait_joueur")
                    efface("joueur1")

                    joueur1(cx - 5, cy - 5, taille, "ressources/Pacman1_haut.png")
                    Nombre_vie -= 1
                    if Nombre_vie == 2:
                        efface("coeur1")
                    if Nombre_vie == 1:
                        efface("coeur2")
                    if Nombre_vie == 0:
                        efface("coeur3")
                        efface("sparks2")
                        efface("sparks1")
                        efface("Fantome_QIX")
                        efface("joueur1")
                        efface("joueur2")
                        if deux == False:
                            texte(
                                300,
                                450,
                                "GAME OVER",
                                couleur="red",
                                taille=40,
                                police="Copperplate Gothic Bold",
                                ancrage="center",
                            )
                        else:
                            texte(
                                300,
                                450,
                                "JOUEUR 2 À GAGNÉ",
                                couleur="green",
                                taille=30,
                                police="Copperplate Gothic Bold",
                                ancrage="center",
                            )
                            if scorev == True:
                                texte(
                                    170,
                                    470,
                                    "Score joueur 1:",
                                    couleur="white",
                                    taille=20,
                                    police="Copperplate Gothic Bold",
                                )
                                texte(
                                    450,
                                    470,
                                    int(score1),
                                    couleur="red",
                                    taille=20,
                                    police="Copperplate Gothic Bold",
                                )
                                texte(
                                    170,
                                    500,
                                    "Score joueur 2:",
                                    couleur="white",
                                    taille=20,
                                    police="Copperplate Gothic Bold",
                                )
                                texte(
                                    450,
                                    500,
                                    int(score2),
                                    couleur="red",
                                    taille=20,
                                    police="Copperplate Gothic Bold",
                                )
                        run = False
                    sleep(0.5)
                    break

        if (
            [cx, cy] in position_qix
            and [cx, cy] not in zone_safe
            and Invincibilite1 == False
        ):  # Si le QIX touche le joueur 1

            if score > 0:
                cx, cy = historique_positions[0][0], historique_positions[0][1]
            else:
                if deux == True:
                    cx, cy = 550, 750
                else:
                    cx, cy = 300, 750
            iteration = 0

            historique_deplacement.clear()
            trait_joueur_actuel.clear()
            historique_positions.clear()

            efface("trait_joueur")
            efface("joueur1")

            joueur1(cx - 5, cy - 5, taille, "ressources/Pacman1_haut.png")
            Nombre_vie -= 1
            if Nombre_vie == 2:
                efface("coeur1")
            if Nombre_vie == 1:
                efface("coeur2")
            if Nombre_vie == 0:
                efface("coeur3")
                efface("sparks2")
                efface("sparks1")
                efface("Fantome_QIX")
                efface("joueur1")
                efface("joueur2")
                if deux == False:
                    texte(
                        300,
                        450,
                        "GAME OVER",
                        couleur="red",
                        taille=40,
                        police="Copperplate Gothic Bold",
                        ancrage="center",
                    )
                else:
                    texte(
                        300,
                        450,
                        "JOUEUR 2 À GAGNÉ",
                        couleur="green",
                        taille=30,
                        police="Copperplate Gothic Bold",
                        ancrage="center",
                    )
                    if scorev == True:
                        texte(
                            170,
                            470,
                            "Score joueur 1:",
                            couleur="white",
                            taille=20,
                            police="Copperplate Gothic Bold",
                        )
                        texte(
                            450,
                            470,
                            int(score1),
                            couleur="red",
                            taille=20,
                            police="Copperplate Gothic Bold",
                        )
                        texte(
                            170,
                            500,
                            "Score joueur 2:",
                            couleur="white",
                            taille=20,
                            police="Copperplate Gothic Bold",
                        )
                        texte(
                            450,
                            500,
                            int(score2),
                            couleur="red",
                            taille=20,
                            police="Copperplate Gothic Bold",
                        )
                run = False
            sleep(0.5)

        if deux == True:
            if (
                [cx2, cy2] in position_qix
                and [cx2, cy2] not in zone_safe
                and Invincibilite2 == False
            ):  # Si le QIX touche le joueur 2
                if score2 > 0:
                    cx2, cy2 = historique_positions2[0][0], historique_positions2[0][1]
                else:
                    cx2, cy2 = 50, 750
                iteration2 = 0

                historique_deplacement2.clear()
                trait_joueur_actuel2.clear()
                historique_positions2.clear()

                efface("trait_joueur2")
                efface("joueur2")

                joueur2(cx2 - 5, cy2 - 5, taille, "ressources/Pacman2_haut.png")
                Nombre_vie2 -= 1
                if Nombre_vie2 == 2:
                    efface("coeur1_2")
                if Nombre_vie2 == 1:
                    efface("coeur2_2")
                if Nombre_vie2 == 0:
                    efface("coeur3_2")
                    efface("sparks2")
                    efface("sparks1")
                    efface("Fantome_QIX")
                    efface("joueur1")
                    efface("joueur2")
                    if deux == False:
                        texte(
                            300,
                            450,
                            "GAME OVER",
                            couleur="red",
                            taille=40,
                            police="Copperplate Gothic Bold",
                            ancrage="center",
                        )
                    else:
                        texte(
                            300,
                            450,
                            "JOUEUR 1 À GAGNÉ",
                            couleur="green",
                            taille=30,
                            police="Copperplate Gothic Bold",
                            ancrage="center",
                        )
                        if scorev == True:
                            texte(
                                170,
                                470,
                                "Score joueur 1:",
                                couleur="white",
                                taille=20,
                                police="Copperplate Gothic Bold",
                            )
                            texte(
                                450,
                                470,
                                int(score1),
                                couleur="red",
                                taille=20,
                                police="Copperplate Gothic Bold",
                            )
                            texte(
                                170,
                                500,
                                "Score joueur 2:",
                                couleur="white",
                                taille=20,
                                police="Copperplate Gothic Bold",
                            )
                            texte(
                                450,
                                500,
                                int(score2),
                                couleur="red",
                                taille=20,
                                police="Copperplate Gothic Bold",
                            )
                    run = False
                sleep(0.5)

        position_qix.clear()

        # -------------------------------------Définition du sparks 1-----------------------------------------
        if temps_sparks % vitesse_sparks == 0:
            dxsparks1 = 0
            dysparks1 = 0
            if [cxsparks1 - 5, cysparks1] in zone_safe and historique_sparks1[
                -1
            ] != "Droite":  # gauche
                dxsparks1 = -deplacement_sparks
                historique_sparks1.append("Gauche")
            elif [cxsparks1, cysparks1 + 5] in zone_safe and historique_sparks1[
                -1
            ] != "Haut":  #  bas
                dysparks1 = deplacement_sparks
                historique_sparks1.append("Bas")
            elif [cxsparks1 + 5, cysparks1] in zone_safe and historique_sparks1[
                -1
            ] != "Gauche":  #  droite
                dxsparks1 = deplacement_sparks
                historique_sparks1.append("Droite")
            elif [cxsparks1, cysparks1 - 5] in zone_safe and historique_sparks1[
                -1
            ] != "Bas":  #  haut
                dysparks1 = -deplacement_sparks
                historique_sparks1.append("Haut")

            if dxsparks1 != 0 or dysparks1 != 0:  # Met à jour sa position
                efface("sparks1")
                cxsparks1 = cxsparks1 + dxsparks1
                cysparks1 = cysparks1 + dysparks1
                if Invincibilite1 == True or Invincibilite2 == True:
                    sprite_actuel = "ressources/Fantome_fruit.png"
                else:
                    sprite_actuel = "ressources/Fantome1.png"
                sparks1(cxsparks1, cysparks1, taille, sprite_actuel)

            # -------------------------------------Définition du sparks 2-----------------------------------------

            dxsparks2 = 0
            dysparks2 = 0

            if [cxsparks2 - 5, cysparks2] in zone_safe and historique_sparks2[
                -1
            ] != "Droite":  # gauche
                dxsparks2 = -deplacement_sparks
                historique_sparks2.append("Gauche")
            elif [cxsparks2, cysparks2 + 5] in zone_safe and historique_sparks2[
                -1
            ] != "Haut":  # bas
                dysparks2 = deplacement_sparks
                historique_sparks2.append("Bas")
            elif [cxsparks2 + 5, cysparks2] in zone_safe and historique_sparks2[
                -1
            ] != "Gauche":  # droite
                dxsparks2 = deplacement_sparks
                historique_sparks2.append("Droite")
            elif [cxsparks2, cysparks2 - 5] in zone_safe and historique_sparks2[
                -1
            ] != "Bas":  # haut
                dysparks2 = -deplacement_sparks
                historique_sparks2.append("Haut")

            if dxsparks2 != 0 or dysparks2 != 0:  # Met à jour sa position
                efface("sparks2")
                cxsparks2 = cxsparks2 + dxsparks2
                cysparks2 = cysparks2 + dysparks2
                if Invincibilite1 == True or Invincibilite2 == True:
                    sprite_actuel = "ressources/Fantome_fruit.png"
                else:
                    sprite_actuel = "ressources/Fantome2.png"
                sparks2(cxsparks2, cysparks2, taille, sprite_actuel)

            # -------------------------------------Définition du sparks 3-----------------------------------------
            if niveau2 == True or niveau3 == True:
                dxsparks3 = 0
                dysparks3 = 0
                if [cxsparks3 - 5, cysparks3] in zone_safe and historique_sparks3[
                    -1
                ] != "Droite":  # gauche
                    dxsparks3 = -deplacement_sparks
                    historique_sparks3.append("Gauche")
                elif [cxsparks3, cysparks3 + 5] in zone_safe and historique_sparks3[
                    -1
                ] != "Haut":  #  bas
                    dysparks3 = deplacement_sparks
                    historique_sparks3.append("Bas")
                elif [cxsparks3 + 5, cysparks3] in zone_safe and historique_sparks3[
                    -1
                ] != "Gauche":  #  droite
                    dxsparks3 = deplacement_sparks
                    historique_sparks3.append("Droite")
                elif [cxsparks3, cysparks3 - 5] in zone_safe and historique_sparks3[
                    -1
                ] != "Bas":  #  haut
                    dysparks3 = -deplacement_sparks
                    historique_sparks3.append("Haut")

                if dxsparks3 != 0 or dysparks3 != 0:  # Met à jour sa position
                    efface("sparks3")
                    cxsparks3 = cxsparks3 + dxsparks3
                    cysparks3 = cysparks3 + dysparks3
                    if Invincibilite1 == True or Invincibilite2 == True:
                        sprite_actuel = "ressources/Fantome_fruit.png"
                    else:
                        sprite_actuel = "ressources/Fantome3.png"
                    sparks3(cxsparks3, cysparks3, taille, sprite_actuel)

                # -------------------------------------Définition du sparks 4-----------------------------------------

                dxsparks4 = 0
                dysparks4 = 0

                if [cxsparks4 - 5, cysparks4] in zone_safe and historique_sparks4[
                    -1
                ] != "Droite":  # gauche
                    dxsparks4 = -deplacement_sparks
                    historique_sparks4.append("Gauche")
                elif [cxsparks4, cysparks4 + 5] in zone_safe and historique_sparks4[
                    -1
                ] != "Haut":  # bas
                    dysparks4 = deplacement_sparks
                    historique_sparks4.append("Bas")
                elif [cxsparks4 + 5, cysparks4] in zone_safe and historique_sparks4[
                    -1
                ] != "Gauche":  # droite
                    dxsparks4 = deplacement_sparks
                    historique_sparks4.append("Droite")
                elif [cxsparks4, cysparks4 - 5] in zone_safe and historique_sparks4[
                    -1
                ] != "Bas":  # haut
                    dysparks4 = -deplacement_sparks
                    historique_sparks4.append("Haut")

                if dxsparks4 != 0 or dysparks4 != 0:  # Met à jour sa position
                    efface("sparks4")
                    cxsparks4 = cxsparks4 + dxsparks4
                    cysparks4 = cysparks4 + dysparks4
                    if Invincibilite1 == True or Invincibilite2 == True:
                        sprite_actuel = "ressources/Fantome_fruit.png"
                    else:
                        sprite_actuel = "ressources/Fantome4.png"
                    sparks4(cxsparks4, cysparks4, taille, sprite_actuel)

            # -------------------------------------Définition du sparks 5-----------------------------------------
            if niveau3 == True:
                dxsparks5 = 0
                dysparks5 = 0
                if [cxsparks5 - 5, cysparks5] in zone_safe and historique_sparks5[
                    -1
                ] != "Droite":  # gauche
                    dxsparks5 = -deplacement_sparks
                    historique_sparks5.append("Gauche")
                elif [cxsparks5, cysparks5 + 5] in zone_safe and historique_sparks5[
                    -1
                ] != "Haut":  #  bas
                    dysparks5 = deplacement_sparks
                    historique_sparks5.append("Bas")
                elif [cxsparks5 + 5, cysparks5] in zone_safe and historique_sparks5[
                    -1
                ] != "Gauche":  #  droite
                    dxsparks5 = deplacement_sparks
                    historique_sparks5.append("Droite")
                elif [cxsparks5, cysparks5 - 5] in zone_safe and historique_sparks5[
                    -1
                ] != "Bas":  #  haut
                    dysparks5 = -deplacement_sparks
                    historique_sparks5.append("Haut")

                if dxsparks5 != 0 or dysparks5 != 0:  # Met à jour sa position
                    efface("sparks5")
                    cxsparks5 = cxsparks5 + dxsparks5
                    cysparks5 = cysparks5 + dysparks5
                    if Invincibilite1 == True or Invincibilite2 == True:
                        sprite_actuel = "ressources/Fantome_fruit.png"
                    else:
                        sprite_actuel = "ressources/Fantome5.png"
                    sparks5(cxsparks5, cysparks5, taille, sprite_actuel)

                # -------------------------------------Définition du sparks 6-----------------------------------------

                dxsparks6 = 0
                dysparks6 = 0

                if [cxsparks6 - 5, cysparks6] in zone_safe and historique_sparks6[
                    -1
                ] != "Droite":  # gauche
                    dxsparks6 = -deplacement_sparks
                    historique_sparks6.append("Gauche")
                elif [cxsparks6, cysparks6 + 5] in zone_safe and historique_sparks6[
                    -1
                ] != "Haut":  # bas
                    dysparks6 = deplacement_sparks
                    historique_sparks6.append("Bas")
                elif [cxsparks6 + 5, cysparks6] in zone_safe and historique_sparks6[
                    -1
                ] != "Gauche":  # droite
                    dxsparks6 = deplacement_sparks
                    historique_sparks6.append("Droite")
                elif [cxsparks6, cysparks6 - 5] in zone_safe and historique_sparks6[
                    -1
                ] != "Bas":  # haut
                    dysparks6 = -deplacement_sparks
                    historique_sparks6.append("Haut")

                if dxsparks6 != 0 or dysparks6 != 0:  # Met à jour sa position
                    efface("sparks6")
                    cxsparks6 = cxsparks6 + dxsparks6
                    cysparks6 = cysparks6 + dysparks6
                    if Invincibilite1 == True or Invincibilite2 == True:
                        sprite_actuel = "ressources/Fantome_fruit.png"
                    else:
                        sprite_actuel = "ressources/Fantome1.png"
                    sparks6(cxsparks6, cysparks6, taille, sprite_actuel)

        temps_sparks += 1

        if [cxsparks1, cysparks1] not in zone_safe:
            historique_sparks1.clear()
            if historique_sparks2[-1] == "Haut":
                historique_sparks1.append("Bas")
            elif historique_sparks2[-1] == "Bas":
                historique_sparks1.append("Haut")
            elif historique_sparks2[-1] == "Gauche":
                historique_sparks1.append("Droite")
            else:
                historique_sparks1.append("Gauche")
            [cxsparks1, cysparks1] = [cxsparks2, cysparks2]

        if [cxsparks2, cysparks2] not in zone_safe:
            historique_sparks2.clear()
            if historique_sparks1[-1] == "Haut":
                historique_sparks2.append("Bas")
            elif historique_sparks1[-1] == "Bas":
                historique_sparks2.append("Haut")
            elif historique_sparks1[-1] == "Gauche":
                historique_sparks2.append("Droite")
            else:
                historique_sparks2.append("Gauche")
            [cxsparks2, cysparks2] = [cxsparks1, cysparks1]

        if niveau2 == True or niveau3 == True:
            if [cxsparks3, cysparks3] not in zone_safe:
                historique_sparks3.clear()
                if historique_sparks4[-1] == "Haut":
                    historique_sparks3.append("Bas")
                elif historique_sparks4[-1] == "Bas":
                    historique_sparks3.append("Haut")
                elif historique_sparks4[-1] == "Gauche":
                    historique_sparks3.append("Droite")
                else:
                    historique_sparks3.append("Gauche")
                [cxsparks3, cysparks3] = [cxsparks4, cysparks4]

            if [cxsparks4, cysparks4] not in zone_safe:
                historique_sparks4.clear()
                if historique_sparks3[-1] == "Haut":
                    historique_sparks4.append("Bas")
                elif historique_sparks3[-1] == "Bas":
                    historique_sparks4.append("Haut")
                elif historique_sparks3[-1] == "Gauche":
                    historique_sparks4.append("Droite")
                else:
                    historique_sparks4.append("Gauche")
                [cxsparks4, cysparks4] = [cxsparks3, cysparks3]

        if niveau3 == True:
            if [cxsparks5, cysparks5] not in zone_safe:
                historique_sparks5.clear()
                if historique_sparks6[-1] == "Haut":
                    historique_sparks5.append("Bas")
                elif historique_sparks6[-1] == "Bas":
                    historique_sparks5.append("Haut")
                elif historique_sparks6[-1] == "Gauche":
                    historique_sparks5.append("Droite")
                else:
                    historique_sparks5.append("Gauche")
                [cxsparks5, cysparks5] = [cxsparks6, cysparks6]

            if [cxsparks6, cysparks6] not in zone_safe:
                historique_sparks6.clear()
                if historique_sparks5[-1] == "Haut":
                    historique_sparks6.append("Bas")
                elif historique_sparks5[-1] == "Bas":
                    historique_sparks6.append("Haut")
                elif historique_sparks5[-1] == "Gauche":
                    historique_sparks6.append("Droite")
                else:
                    historique_sparks6.append("Gauche")
                [cxsparks6, cysparks6] = [cxsparks5, cysparks5]

        # JOUEUR 1
        if (
            [cxsparks1, cysparks1] == [cx, cy] or [cxsparks2, cysparks2] == [cx, cy]
        ) and Invincibilite1 == False:  # Si le Sparks touche le joueur
            historique_positions.clear()

            if [cxsparks1, cysparks1] == [cx, cy]:
                historique_sparks1.clear()
                if historique_sparks2[-1] == "Haut":
                    historique_sparks1.append("Bas")
                elif historique_sparks2[-1] == "Bas":
                    historique_sparks1.append("Haut")
                elif historique_sparks2[-1] == "Gauche":
                    historique_sparks1.append("Droite")
                else:
                    historique_sparks1.append("Gauche")
                [cxsparks1, cysparks1] = [cxsparks2, cysparks2]

            elif [cxsparks2, cysparks2] == [cx, cy]:
                historique_sparks2.clear()
                if historique_sparks1[-1] == "Haut":
                    historique_sparks2.append("Bas")
                elif historique_sparks1[-1] == "Bas":
                    historique_sparks2.append("Haut")
                elif historique_sparks1[-1] == "Gauche":
                    historique_sparks2.append("Droite")
                else:
                    historique_sparks2.append("Gauche")
                [cxsparks2, cysparks2] = [cxsparks1, cysparks1]

            efface("joueur1")
            efface("trait_joueur")
            trait_joueur_actuel.clear()
            efface(QIX)

            joueur1(cx - 5, cy - 5, 10, "ressources/Pacman1_haut.png")
            Nombre_vie -= 1
            if Nombre_vie == 2:
                efface("coeur1")
            if Nombre_vie == 1:
                efface("coeur2")
            if Nombre_vie == 0:
                efface("coeur3")
                efface("sparks3")
                efface("sparks4")
                efface("Fantome_QIX")
                efface("joueur1")
                efface("joueur2")
                if deux == False:
                    texte(
                        300,
                        450,
                        "GAME OVER",
                        couleur="red",
                        taille=40,
                        police="Copperplate Gothic Bold",
                        ancrage="center",
                    )
                else:
                    texte(
                        300,
                        450,
                        "JOUEUR 2 À GAGNÉ",
                        couleur="green",
                        taille=30,
                        police="Copperplate Gothic Bold",
                        ancrage="center",
                    )
                    if scorev == True:
                        texte(
                            170,
                            470,
                            "Score joueur 1:",
                            couleur="white",
                            taille=20,
                            police="Copperplate Gothic Bold",
                        )
                        texte(
                            450,
                            470,
                            int(score1),
                            couleur="red",
                            taille=20,
                            police="Copperplate Gothic Bold",
                        )
                        texte(
                            170,
                            500,
                            "Score joueur 2:",
                            couleur="white",
                            taille=20,
                            police="Copperplate Gothic Bold",
                        )
                        texte(
                            450,
                            500,
                            int(score2),
                            couleur="red",
                            taille=20,
                            police="Copperplate Gothic Bold",
                        )
                run = False
            sleep(0.5)

        if niveau2 == True or niveau3 == True:
            if (
                [cxsparks3, cysparks3] == [cx, cy] or [cxsparks4, cysparks4] == [cx, cy]
            ) and Invincibilite1 == False:
                if [cxsparks3, cysparks3] == [cx, cy]:
                    historique_sparks3.clear()
                    if historique_sparks4[-1] == "Haut":
                        historique_sparks3.append("Bas")
                    elif historique_sparks4[-1] == "Bas":
                        historique_sparks3.append("Haut")
                    elif historique_sparks4[-1] == "Gauche":
                        historique_sparks3.append("Droite")
                    else:
                        historique_sparks3.append("Gauche")
                    [cxsparks3, cysparks3] = [cxsparks4, cysparks4]

                elif [cxsparks4, cysparks4] == [cx, cy]:
                    historique_sparks4.clear()
                    if historique_sparks3[-1] == "Haut":
                        historique_sparks4.append("Bas")
                    elif historique_sparks3[-1] == "Bas":
                        historique_sparks4.append("Haut")
                    elif historique_sparks3[-1] == "Gauche":
                        historique_sparks4.append("Droite")
                    else:
                        historique_sparks4.append("Gauche")
                    [cxsparks4, cysparks4] = [cxsparks3, cysparks3]

                efface("joueur1")
                efface("trait_joueur")
                trait_joueur_actuel.clear()
                efface(QIX)

                joueur1(cx - 5, cy - 5, 10, "ressources/Pacman1_haut.png")
                Nombre_vie -= 1
                if Nombre_vie == 2:
                    efface("coeur1")
                if Nombre_vie == 1:
                    efface("coeur2")
                if Nombre_vie == 0:
                    efface("coeur3")
                    efface("sparks5")
                    efface("sparks6")
                    efface("Fantome_QIX")
                    efface("joueur1")
                    efface("joueur2")
                    if deux == False:
                        texte(
                            300,
                            450,
                            "GAME OVER",
                            couleur="red",
                            taille=40,
                            police="Copperplate Gothic Bold",
                            ancrage="center",
                        )
                    else:
                        texte(
                            300,
                            450,
                            "JOUEUR 2 À GAGNÉ",
                            couleur="green",
                            taille=30,
                            police="Copperplate Gothic Bold",
                            ancrage="center",
                        )
                        if scorev == True:
                            texte(
                                170,
                                470,
                                "Score joueur 1:",
                                couleur="white",
                                taille=20,
                                police="Copperplate Gothic Bold",
                            )
                            texte(
                                450,
                                470,
                                int(score1),
                                couleur="red",
                                taille=20,
                                police="Copperplate Gothic Bold",
                            )
                            texte(
                                170,
                                500,
                                "Score joueur 2:",
                                couleur="white",
                                taille=20,
                                police="Copperplate Gothic Bold",
                            )
                            texte(
                                450,
                                500,
                                int(score2),
                                couleur="red",
                                taille=20,
                                police="Copperplate Gothic Bold",
                            )
                    run = False
                sleep(0.5)

        if niveau3 == True:
            if (
                [cxsparks5, cysparks5] == [cx, cy] or [cxsparks6, cysparks6] == [cx, cy]
            ) and Invincibilite1 == False:
                if [cxsparks5, cysparks5] == [cx, cy]:
                    historique_sparks5.clear()
                    if historique_sparks6[-1] == "Haut":
                        historique_sparks5.append("Bas")
                    elif historique_sparks6[-1] == "Bas":
                        historique_sparks5.append("Haut")
                    elif historique_sparks6[-1] == "Gauche":
                        historique_sparks5.append("Droite")
                    else:
                        historique_sparks5.append("Gauche")
                    [cxsparks5, cysparks5] = [cxsparks6, cysparks6]

                if [cxsparks6, cysparks6] == [cx, cy]:
                    historique_sparks6.clear()
                    if historique_sparks5[-1] == "Haut":
                        historique_sparks6.append("Bas")
                    elif historique_sparks5[-1] == "Bas":
                        historique_sparks6.append("Haut")
                    elif historique_sparks5[-1] == "Gauche":
                        historique_sparks6.append("Droite")
                    else:
                        historique_sparks6.append("Gauche")
                    [cxsparks6, cysparks6] = [cxsparks5, cysparks5]

                efface("joueur1")
                efface("trait_joueur")
                trait_joueur_actuel.clear()
                efface(QIX)
                xQIX, yQIX = 250, 400

                joueur1(cx - 5, cy - 5, 10, "ressources/Pacman1_haut.png")
                Nombre_vie -= 1
                if Nombre_vie == 2:
                    efface("coeur1")
                if Nombre_vie == 1:
                    efface("coeur2")
                if Nombre_vie == 0:
                    efface("coeur3")
                    efface("sparks2")
                    efface("sparks1")
                    efface("Fantome_QIX")
                    efface("joueur1")
                    efface("joueur2")
                    if deux == False:
                        texte(
                            300,
                            450,
                            "GAME OVER",
                            couleur="red",
                            taille=40,
                            police="Copperplate Gothic Bold",
                            ancrage="center",
                        )
                    else:
                        texte(
                            300,
                            450,
                            "JOUEUR 2 À GAGNÉ",
                            couleur="green",
                            taille=30,
                            police="Copperplate Gothic Bold",
                            ancrage="center",
                        )
                        if scorev == True:
                            texte(
                                170,
                                470,
                                "Score joueur 1:",
                                couleur="white",
                                taille=20,
                                police="Copperplate Gothic Bold",
                            )
                            texte(
                                450,
                                470,
                                int(score1),
                                couleur="red",
                                taille=20,
                                police="Copperplate Gothic Bold",
                            )
                            texte(
                                170,
                                500,
                                "Score joueur 2:",
                                couleur="white",
                                taille=20,
                                police="Copperplate Gothic Bold",
                            )
                            texte(
                                450,
                                500,
                                int(score2),
                                couleur="red",
                                taille=20,
                                police="Copperplate Gothic Bold",
                            )
                    run = False
                sleep(0.5)

        # JOUEUR 2
        if deux == True:
            if (
                [cxsparks1, cysparks1] == [cx2, cy2]
                or [cxsparks2, cysparks2] == [cx2, cy2]
            ) and Invincibilite2 == False:  # Si le Sparks touche le joueur
                historique_positions.clear()

                if [cxsparks1, cysparks1] == [cx2, cy2]:
                    historique_sparks1.clear()
                    if historique_sparks2[-1] == "Haut":
                        historique_sparks1.append("Bas")
                    elif historique_sparks2[-1] == "Bas":
                        historique_sparks1.append("Haut")
                    elif historique_sparks2[-1] == "Gauche":
                        historique_sparks1.append("Droite")
                    else:
                        historique_sparks1.append("Gauche")
                    [cxsparks1, cysparks1] = [cxsparks2, cysparks2]

                elif [cxsparks2, cysparks2] == [cx2, cy2]:
                    historique_sparks2.clear()
                    if historique_sparks1[-1] == "Haut":
                        historique_sparks2.append("Bas")
                    elif historique_sparks1[-1] == "Bas":
                        historique_sparks2.append("Haut")
                    elif historique_sparks1[-1] == "Gauche":
                        historique_sparks2.append("Droite")
                    else:
                        historique_sparks2.append("Gauche")
                    [cxsparks2, cysparks2] = [cxsparks1, cysparks1]

                efface("joueur2")
                efface("trait_joueur")
                trait_joueur_actuel.clear()
                efface(QIX)

                joueur2(cx2 - 5, cy2 - 5, 10, "ressources/Pacman2_haut.png")
                Nombre_vie -= 1
                if Nombre_vie == 2:
                    efface("coeur1_2")
                if Nombre_vie == 1:
                    efface("coeur2_2")
                if Nombre_vie == 0:
                    efface("coeur3_2")
                    efface("sparks3")
                    efface("sparks4")
                    efface("Fantome_QIX")
                    efface("joueur1")
                    efface("joueur2")
                    if deux == False:
                        texte(
                            300,
                            450,
                            "GAME OVER",
                            couleur="red",
                            taille=40,
                            police="Copperplate Gothic Bold",
                            ancrage="center",
                        )
                    else:
                        texte(
                            300,
                            450,
                            "JOUEUR 1 À GAGNÉ",
                            couleur="green",
                            taille=30,
                            police="Copperplate Gothic Bold",
                            ancrage="center",
                        )
                        if scorev == True:
                            texte(
                                170,
                                470,
                                "Score joueur 1:",
                                couleur="white",
                                taille=20,
                                police="Copperplate Gothic Bold",
                            )
                            texte(
                                450,
                                470,
                                int(score1),
                                couleur="red",
                                taille=20,
                                police="Copperplate Gothic Bold",
                            )
                            texte(
                                170,
                                500,
                                "Score joueur 2:",
                                couleur="white",
                                taille=20,
                                police="Copperplate Gothic Bold",
                            )
                            texte(
                                450,
                                500,
                                int(score2),
                                couleur="red",
                                taille=20,
                                police="Copperplate Gothic Bold",
                            )
                    run = False
                sleep(0.5)

            if niveau2 == True or niveau3 == True:
                if (
                    [cxsparks3, cysparks3] == [cx2, cy2]
                    or [cxsparks4, cysparks4] == [cx2, cy2]
                ) and Invincibilite2 == False:
                    if [cxsparks3, cysparks3] == [cx2, cy2]:
                        historique_sparks3.clear()
                        if historique_sparks4[-1] == "Haut":
                            historique_sparks3.append("Bas")
                        elif historique_sparks4[-1] == "Bas":
                            historique_sparks3.append("Haut")
                        elif historique_sparks4[-1] == "Gauche":
                            historique_sparks3.append("Droite")
                        else:
                            historique_sparks3.append("Gauche")
                        [cxsparks3, cysparks3] = [cxsparks4, cysparks4]

                    elif [cxsparks4, cysparks4] == [cx2, cy2]:
                        historique_sparks4.clear()
                        if historique_sparks3[-1] == "Haut":
                            historique_sparks4.append("Bas")
                        elif historique_sparks3[-1] == "Bas":
                            historique_sparks4.append("Haut")
                        elif historique_sparks3[-1] == "Gauche":
                            historique_sparks4.append("Droite")
                        else:
                            historique_sparks4.append("Gauche")
                        [cxsparks4, cysparks4] = [cxsparks3, cysparks3]

                    efface("joueur2")
                    efface("trait_joueur")
                    trait_joueur_actuel.clear()
                    efface(QIX)

                    joueur2(cx2 - 5, cy2 - 5, 10, "ressources/Pacman2_haut.png")
                    Nombre_vie -= 1
                    if Nombre_vie == 2:
                        efface("coeur1_2")
                    if Nombre_vie == 1:
                        efface("coeur2_2")
                    if Nombre_vie == 0:
                        efface("coeur3_2")
                        efface("sparks5")
                        efface("sparks6")
                        efface("Fantome_QIX")
                        efface("joueur1")
                        efface("joueur1")
                        efface("joueur2")
                        if deux == False:
                            texte(
                                300,
                                450,
                                "GAME OVER",
                                couleur="red",
                                taille=40,
                                police="Copperplate Gothic Bold",
                                ancrage="center",
                            )
                        else:
                            texte(
                                300,
                                450,
                                "JOUEUR 1 À GAGNÉ",
                                couleur="green",
                                taille=30,
                                police="Copperplate Gothic Bold",
                                ancrage="center",
                            )
                            if scorev == True:
                                texte(
                                    170,
                                    470,
                                    "Score joueur 1:",
                                    couleur="white",
                                    taille=20,
                                    police="Copperplate Gothic Bold",
                                )
                                texte(
                                    450,
                                    470,
                                    int(score1),
                                    couleur="red",
                                    taille=20,
                                    police="Copperplate Gothic Bold",
                                )
                                texte(
                                    170,
                                    500,
                                    "Score joueur 2:",
                                    couleur="white",
                                    taille=20,
                                    police="Copperplate Gothic Bold",
                                )
                                texte(
                                    450,
                                    500,
                                    int(score2),
                                    couleur="red",
                                    taille=20,
                                    police="Copperplate Gothic Bold",
                                )
                        run = False
                    sleep(0.5)

            if niveau3 == True:
                if (
                    [cxsparks5, cysparks5] == [cx2, cy2]
                    or [cxsparks6, cysparks6] == [cx2, cy2]
                ) and Invincibilite2 == False:
                    if [cxsparks5, cysparks5] == [cx2, cy2]:
                        historique_sparks5.clear()
                        if historique_sparks6[-1] == "Haut":
                            historique_sparks5.append("Bas")
                        elif historique_sparks6[-1] == "Bas":
                            historique_sparks5.append("Haut")
                        elif historique_sparks6[-1] == "Gauche":
                            historique_sparks5.append("Droite")
                        else:
                            historique_sparks5.append("Gauche")
                        [cxsparks5, cysparks5] = [cxsparks6, cysparks6]

                    if [cxsparks6, cysparks6] == [cx2, cy2]:
                        historique_sparks6.clear()
                        if historique_sparks5[-1] == "Haut":
                            historique_sparks6.append("Bas")
                        elif historique_sparks5[-1] == "Bas":
                            historique_sparks6.append("Haut")
                        elif historique_sparks5[-1] == "Gauche":
                            historique_sparks6.append("Droite")
                        else:
                            historique_sparks6.append("Gauche")
                        [cxsparks6, cysparks6] = [cxsparks5, cysparks5]

                    efface("joueur2")
                    efface("trait_joueur")
                    trait_joueur_actuel.clear()
                    efface(QIX)
                    xQIX, yQIX = 250, 400

                    joueur2(cx2 - 5, cy2 - 5, 10, "ressources/Pacman2_haut.png")
                    Nombre_vie -= 1
                    if Nombre_vie == 2:
                        efface("coeur1_2")
                    if Nombre_vie == 1:
                        efface("coeur2_2")
                    if Nombre_vie == 0:
                        efface("coeur3_2")
                        efface("sparks2")
                        efface("sparks1")
                        efface("Fantome_QIX")
                        efface("joueur1")
                        efface("joueur2")
                        if deux == False:
                            texte(
                                300,
                                450,
                                "GAME OVER",
                                couleur="red",
                                taille=40,
                                police="Copperplate Gothic Bold",
                                ancrage="center",
                            )
                        else:
                            texte(
                                300,
                                450,
                                "JOUEUR 1 À GAGNÉ",
                                couleur="green",
                                taille=30,
                                police="Copperplate Gothic Bold",
                                ancrage="center",
                            )
                            if scorev == True:
                                texte(
                                    170,
                                    470,
                                    "Score joueur 1:",
                                    couleur="white",
                                    taille=20,
                                    police="Copperplate Gothic Bold",
                                )
                                texte(
                                    450,
                                    470,
                                    int(score1),
                                    couleur="red",
                                    taille=20,
                                    police="Copperplate Gothic Bold",
                                )
                                texte(
                                    170,
                                    500,
                                    "Score joueur 2:",
                                    couleur="white",
                                    taille=20,
                                    police="Copperplate Gothic Bold",
                                )
                                texte(
                                    450,
                                    500,
                                    int(score2),
                                    couleur="red",
                                    taille=20,
                                    police="Copperplate Gothic Bold",
                                )
                        run = False
                    sleep(0.5)

        mise_a_jour()


# -------------------------------------Game Over-----------------------------------------

if __name__ == "__main__":
    # Menu
    menu = Accueil()

    # Si on appuie sur jouer
    if menu == True:
        (
            scorev,
            vitesse,
            obstacle,
            bonus,
            deux,
            niveau,
            start,
            obstacle_aleatoire,
            obstacle_predefini,
            niveau1,
            niveau2,
            niveau3,
            bonus_aleatoire,
            bonus_predefini,
        ) = variantes()
        if start == True:
            fenetre()
            jeu()
            sleep(5)
            ferme_fenetre()
