from fltk import *
from config.constants import VIES_INITIALES, GRILLE_PAS, VITESSE_TRACAGE_RAPIDE, FENETRE_CONFIG


def creer_fenetre_jeu(deux):
    """
    Créer et configurer la fenêtre de jeu principale
    
    Args:
        deux (bool): Mode 2 joueurs activé
    """
    # Configuration de la fenêtre depuis les constantes
    largeur_fenetre = FENETRE_CONFIG["largeur"]
    hauteur_fenetre = FENETRE_CONFIG["hauteur"]
    
    # Ajustement pour le mode 2 joueurs
    if deux:
        largeur_fenetre = int(largeur_fenetre * 1.5)
    
    # Zone de jeu depuis les constantes
    x, y = FENETRE_CONFIG["aire_x"], FENETRE_CONFIG["aire_y"]
    xb, yb = FENETRE_CONFIG["aire_xb"], FENETRE_CONFIG["aire_yb"]
    
    # Création de la fenêtre et arrière-plan
    cree_fenetre(largeur_fenetre, hauteur_fenetre)
    rectangle(0, 0, largeur_fenetre, hauteur_fenetre, "white", "black", VITESSE_TRACAGE_RAPIDE)
    image(300, 400, "ressources/background3.png", 
          largeur=largeur_fenetre, hauteur=hauteur_fenetre)
    rectangle(x, y, xb, yb, "midnightblue", "black", VIES_INITIALES)
    
    return largeur_fenetre, hauteur_fenetre


def creer_interface_complete(deux, scorev):
    """
    Créer l'interface utilisateur complète du jeu
    
    Args:
        deux (bool): Mode 2 joueurs activé
        scorev (bool): Affichage du score activé
    """
    # Interface utilisateur (mode solo uniquement)
    if not deux:
        creer_interface_solo(scorev)
    
    # Vies du joueur
    creer_coeurs()
    
    # Message de sortie
    texte(300, 770, "Appuyez sur ECHAP pour quitter",
          couleur="white", taille=15, police="Copperplate Gothic Bold", ancrage="center")


def creer_interface_solo(scorev):
    """
    Créer l'interface pour le mode solo
    
    Args:
        scorev (bool): Affichage du score activé
    """
    # Police commune pour optimiser
    police_standard = "Copperplate Gothic Bold"
    
    # Titre principal
    texte(60, 75, "QIX", couleur="white", taille=45, police=police_standard)
    
    # Section CLAIMED
    texte(230, 80, "CLAIMED", couleur="white", taille=20, police=police_standard)
    texte(315, 110, "75 %", couleur="white", taille=16, police=police_standard)
    texte(235, 110, "0", couleur="white", taille=16, police=police_standard, tag="score_pourcentage")
    
    # Section SCORE
    texte(420, 80, "SCORE", couleur="white", taille=20, police=police_standard)
    
    # Symbole % (utilisé deux fois, optimisé)
    texte(270, 110, "%", couleur="white", taille=16, police=police_standard)
    
    # Score total (conditionnel)
    score_text = "0" if scorev else "X"
    texte(420, 110, score_text, couleur="white", taille=16, police=police_standard, tag="score_total")


def creer_coeurs():
    """
    Créer les indicateurs de vie
    """
    positions_y = [90, 105, 120]
    for i, y in enumerate(positions_y, 1):
        cercle(545, y, GRILLE_PAS, "red", "red", tag=f"coeur{i}")


def mettre_a_jour_score_pourcentage(pourcentage):
    """
    Mettre à jour l'affichage du pourcentage de territoire conquis
    
    Args:
        pourcentage (int): Pourcentage à afficher
    """
    efface("score_pourcentage")
    texte(235, 110, str(pourcentage), couleur="white", taille=16, 
          police="Copperplate Gothic Bold", tag="score_pourcentage")


def mettre_a_jour_score_total(score):
    """
    Mettre à jour l'affichage du score total
    
    Args:
        score (int): Score à afficher
    """
    efface("score_total")
    texte(420, 110, str(score), couleur="white", taille=16, 
          police="Copperplate Gothic Bold", tag="score_total")


def mettre_a_jour_vies(nombre_vies):
    """
    Mettre à jour l'affichage des vies restantes
    
    Args:
        nombre_vies (int): Nombre de vies restantes (1-VIES_INITIALES)
    """
    # Effacer tous les cœurs
    for i in range(1, 4):
        efface(f"coeur{i}")
    
    # Recréer seulement les cœurs correspondant aux vies restantes
    positions_y = [90, 105, 120]
    for i in range(nombre_vies):
        y = positions_y[i]
        cercle(545, y, GRILLE_PAS, "red", "red", tag=f"coeur{i+1}")


def afficher_interface_2_joueurs(scorev=False):
    """Affiche l'interface graphique pour le mode 2 joueurs"""
    from fltk import rectangle, image, texte, ligne, cercle, efface
    
    # Interface de base
    rectangle(600, 0, 900, 1200, "white", "black", 2)
    image(300, 100, "ressources/Titre2.png", largeur=250, hauteur=80)
    
    # Section CLAIMED
    texte(680, 80, "CLAIMED", couleur="white", taille=20, police="Copperplate Gothic Bold")
    texte(765, 110, "75 %", couleur="white", taille=16, police="Copperplate Gothic Bold")
    texte(735, 110, "%", couleur="white", taille=16, police="Copperplate Gothic Bold")
    texte(700, 110, "0", couleur="white", taille=16, police="Copperplate Gothic Bold", tag="score_pourcentage")
    
    # Interface Joueur 1
    texte(650, 200, "JOUEUR 1", couleur="white", taille=20, police="Copperplate Gothic Bold")
    texte(650, 250, "SCORE :", couleur="white", taille=16, police="Copperplate Gothic Bold")
    
    score_affiche = "X" if not scorev else 0
    texte(770, 250, score_affiche, couleur="white", taille=16, police="Copperplate Gothic Bold", tag="score_joueur1")
    
    image(750, 340, "ressources/Pacman1_droite.png", largeur=100, hauteur=100)
    ligne(600, 440, 1000, 440, couleur="white")
    
    # Interface Joueur 2
    texte(650, 500, "JOUEUR 2", couleur="white", taille=20, police="Copperplate Gothic Bold")
    texte(650, 550, "SCORE :", couleur="white", taille=16, police="Copperplate Gothic Bold")
    
    texte(770, 550, score_affiche, couleur="white", taille=16, police="Copperplate Gothic Bold", tag="score_joueur2")
    
    image(750, 640, "ressources/Pacman2_droite.png", largeur=100, hauteur=100)
    
    # Cœurs de vie pour les deux joueurs
    efface("coeur1")
    efface("coeur2")
    efface("coeur3")
    
    # Cœurs Joueur 1
    cercle(850, 250, GRILLE_PAS, "red", "red", tag="coeur1")
    cercle(850, 265, GRILLE_PAS, "red", "red", tag="coeur2")
    cercle(850, 280, GRILLE_PAS, "red", "red", tag="coeur3")
    
    # Cœurs Joueur 2
    cercle(850, 550, GRILLE_PAS, "red", "red", tag="coeur1_2")
    cercle(850, 565, GRILLE_PAS, "red", "red", tag="coeur2_2")
    cercle(850, 580, GRILLE_PAS, "red", "red", tag="coeur3_2")
