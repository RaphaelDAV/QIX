"""Module de gestion des menus du jeu QIX"""

from fltk import *
from config.constants import *


class MenuElements:
    """Classe pour gérer les éléments d'interface des menus"""
    
    @staticmethod
    def creer_fond_menu(largeur, hauteur, image_fond):
        """Créer le fond d'un menu"""
        rectangle(0, 0, largeur, hauteur, couleur="black", remplissage="black")
        image(largeur//2, hauteur//2 - 40, image_fond, 
              largeur=largeur, hauteur=hauteur)
    
    @staticmethod
    def creer_bouton(x, y, largeur, hauteur, texte_bouton, couleur="midnightblue", 
                     epaisseur=7, taille_texte=24, tag=None):
        """Créer un bouton avec texte centré"""
        rectangle(x, y, x + largeur, y + hauteur, 
                 couleur=couleur, epaisseur=epaisseur, tag=tag)
        texte(x + largeur//2, y + hauteur//2, texte_bouton,
              couleur="white", police="Helvetica", taille=taille_texte, 
              ancrage="center", tag=tag)
    
    @staticmethod
    def creer_bouton_toggle(x, y, largeur, hauteur, texte_bouton, actif=False, tag=None):
        """Créer un bouton à bascule (activé/désactivé)"""
        if actif:
            couleur = "green"
            remplissage = "green"
            epaisseur = None
        else:
            couleur = "yellow"
            remplissage = None
            epaisseur = 5
            
        rectangle(x, y, x + largeur, y + hauteur,
                 couleur=couleur, remplissage=remplissage, 
                 epaisseur=epaisseur, tag=tag)
        texte(x + largeur//2, y + hauteur//2, texte_bouton,
              couleur="white", police="Helvetica", taille=20,
              ancrage="center", tag=tag)
    
    @staticmethod
    def verifier_clic_bouton(x_clic, y_clic, x_bouton, y_bouton, largeur, hauteur):
        """Vérifier si un clic est dans un bouton"""
        return (x_bouton <= x_clic <= x_bouton + largeur and 
                y_bouton <= y_clic <= y_bouton + hauteur)


def afficher_menu_accueil():
    """
    Affiche le menu d'accueil principal
    
    Returns:
        bool: True pour nouvelle partie, False pour quitter
    """
    # Configuration du menu
    largeur_fenetre = 800
    hauteur_fenetre = 600
    cree_fenetre(largeur_fenetre, hauteur_fenetre)
    
    # Dimensions des boutons
    largeur_bouton = 250
    hauteur_bouton = 50
    
    # Positions des boutons (centrés)
    x_boutons = (largeur_fenetre - largeur_bouton) // 2
    y_nouvelle_partie = 220
    y_quitter = 300
    
    while True:
        efface_tout()
        
        # Fond du menu
        MenuElements.creer_fond_menu(largeur_fenetre, hauteur_fenetre, 
                                    "ressources/background.png")
        
        # Images du menu
        _afficher_elements_accueil()
        
        # Boutons
        MenuElements.creer_bouton(x_boutons, y_nouvelle_partie, largeur_bouton, 
                                 hauteur_bouton, "Nouvelle Partie", "midnightblue")
        MenuElements.creer_bouton(x_boutons, y_quitter, largeur_bouton, 
                                 hauteur_bouton, "Quitter", "red4", 5)
        
        # Gestion des clics
        x, y = attend_clic_gauche()
        
        if MenuElements.verifier_clic_bouton(x, y, x_boutons, y_nouvelle_partie, 
                                           largeur_bouton, hauteur_bouton):
            ferme_fenetre()
            return True
            
        if MenuElements.verifier_clic_bouton(x, y, x_boutons, y_quitter, 
                                           largeur_bouton, hauteur_bouton):
            ferme_fenetre()
            return False


def _afficher_elements_accueil():
    """Afficher les éléments visuels du menu d'accueil"""
    image(400, 100, "ressources/Titre.png", largeur=300, hauteur=120)
    image(600, 400, "ressources/Bonhomme.png", largeur=320, hauteur=170)
    image(400, 550, "ressources/prenom.png", largeur=500, hauteur=30)


def afficher_menu_variantes():
    """
    Affiche le menu de sélection des variantes de jeu
    
    Returns:
        tuple: Configuration complète du jeu sélectionnée
    """
    # Configuration du menu
    largeur_fenetre = 900
    hauteur_fenetre = 700
    cree_fenetre(largeur_fenetre, hauteur_fenetre)
    
    # État des options
    config_jeu = {
        'scorev': False, 'vitesse': False, 'obstacle': False, 'bonus': False,
        'deux': False, 'niveau': False, 'obstacle_aleatoire': False,
        'obstacle_predefini': False, 'niveau1': False, 'niveau2': False,
        'niveau3': False, 'bonus_aleatoire': False, 'bonus_predefini': False
    }
    
    # Positions des boutons
    positions_boutons = _calculer_positions_boutons_variantes()
    
    while True:
        efface_tout()
        
        # Fond du menu
        MenuElements.creer_fond_menu(largeur_fenetre, hauteur_fenetre,
                                    "ressources/background2.png")
        
        # Affichage de tous les boutons
        _afficher_boutons_variantes(positions_boutons, config_jeu)
        
        # Image décorative
        image(480, 470, "ressources/pacman_fantome.png", 900, 550)
        
        # Gestion des clics
        x, y = attend_clic_gauche()
        
        # Traitement des clics
        resultat = _traiter_clic_variantes(x, y, positions_boutons, config_jeu)
        if resultat is not None:
            ferme_fenetre()
            return resultat
        
        mise_a_jour()


def _calculer_positions_boutons_variantes():
    """Calculer les positions de tous les boutons du menu variantes"""
    largeur_bouton = 200
    hauteur_bouton = 50
    
    return {
        'largeur_bouton': largeur_bouton,
        'hauteur_bouton': hauteur_bouton,
        'score': (50, 100),
        'vitesse': (350, 100),
        'obstacle': (650, 100),
        'bonus': (50, 300),
        'deux': (350, 300),
        'niveau': (650, 300),
        'nouvelle_partie': (250, 550),
        'quitter': (500, 550),
        # Sous-options
        'obstacle_predefini': (650, 170, 90, 50),
        'obstacle_aleatoire': (760, 170, 90, 50),
        'bonus_predefini': (50, 370, 90, 50),
        'bonus_aleatoire': (160, 370, 90, 50),
        'niveau1': (650, 370, 50, 50),
        'niveau2': (725, 370, 50, 50),
        'niveau3': (800, 370, 50, 50)
    }


def _afficher_boutons_variantes(positions, config):
    """Afficher tous les boutons du menu variantes"""
    # Boutons principaux - mapping entre positions et config
    boutons_mapping = {
        'score': 'scorev',
        'vitesse': 'vitesse', 
        'obstacle': 'obstacle',
        'bonus': 'bonus',
        'deux': 'deux',
        'niveau': 'niveau'
    }
    
    for pos_key, config_key in boutons_mapping.items():
        x, y = positions[pos_key]
        MenuElements.creer_bouton_toggle(
            x, y, positions['largeur_bouton'], positions['hauteur_bouton'],
            pos_key.capitalize(), config[config_key], pos_key
        )
    
    # Boutons d'action
    x_np, y_np = positions['nouvelle_partie']
    x_q, y_q = positions['quitter']
    MenuElements.creer_bouton(x_np, y_np, positions['largeur_bouton'], 
                             positions['hauteur_bouton'], "Nouvelle Partie", "midnightblue")
    MenuElements.creer_bouton(x_q, y_q, positions['largeur_bouton'], 
                             positions['hauteur_bouton'], "Quitter", "red4", 5)
    
    # Sous-options conditionnelles
    if config['obstacle']:
        _afficher_sous_options_obstacle(positions, config)
    if config['bonus']:
        _afficher_sous_options_bonus(positions, config)
    if config['niveau']:
        _afficher_sous_options_niveau(positions, config)


def _afficher_sous_options_obstacle(positions, config):
    """Afficher les sous-options pour les obstacles"""
    x1, y1, w1, h1 = positions['obstacle_predefini']
    x2, y2, w2, h2 = positions['obstacle_aleatoire']
    
    couleur1 = "green" if config['obstacle_predefini'] else "gray"
    couleur2 = "green" if config['obstacle_aleatoire'] else "gray"
    
    MenuElements.creer_bouton(x1, y1, w1, h1, "Prédéfinis", couleur1, tag="obstacle_predefini")
    MenuElements.creer_bouton(x2, y2, w2, h2, "Aléatoires", couleur2, tag="obstacle_aleatoire")


def _afficher_sous_options_bonus(positions, config):
    """Afficher les sous-options pour les bonus"""
    x1, y1, w1, h1 = positions['bonus_predefini']
    x2, y2, w2, h2 = positions['bonus_aleatoire']
    
    couleur1 = "green" if config['bonus_predefini'] else "gray"
    couleur2 = "green" if config['bonus_aleatoire'] else "gray"
    
    MenuElements.creer_bouton(x1, y1, w1, h1, "Prédéfinis", couleur1, tag="bonus_predefini")
    MenuElements.creer_bouton(x2, y2, w2, h2, "Aléatoires", couleur2, tag="bonus_aleatoire")


def _afficher_sous_options_niveau(positions, config):
    """Afficher les sous-options pour les niveaux"""
    niveaux = [('niveau1', 'F', 'green'), ('niveau2', 'M', 'orange'), ('niveau3', 'D', 'red')]
    
    for niveau, lettre, couleur_base in niveaux:
        x, y, w, h = positions[niveau]
        if config[niveau]:
            rectangle(x, y, x + w, y + h, couleur="white", remplissage=couleur_base, 
                     epaisseur=3.5, tag=niveau)
        else:
            rectangle(x, y, x + w, y + h, couleur=couleur_base, 
                     remplissage=couleur_base, tag=niveau)
        texte(x + w//2, y + h//2, lettre, couleur="black", police="Helvetica", 
              taille=13, ancrage="center", tag=niveau)


def _traiter_clic_variantes(x, y, positions, config):
    """Traiter les clics dans le menu variantes"""
    # Mapping entre positions et config
    boutons_mapping = {
        'score': 'scorev',
        'vitesse': 'vitesse', 
        'obstacle': 'obstacle',
        'bonus': 'bonus',
        'deux': 'deux',
        'niveau': 'niveau'
    }
    
    for pos_key, config_key in boutons_mapping.items():
        x_btn, y_btn = positions[pos_key]
        if MenuElements.verifier_clic_bouton(x, y, x_btn, y_btn, 
                                           positions['largeur_bouton'], 
                                           positions['hauteur_bouton']):
            _basculer_option_principale(config_key, config)
            return None
    
    # Vérifier sous-options
    if config['obstacle']:
        if _traiter_clic_sous_options_obstacle(x, y, positions, config):
            return None
    
    if config['bonus']:
        if _traiter_clic_sous_options_bonus(x, y, positions, config):
            return None
    
    if config['niveau']:
        if _traiter_clic_sous_options_niveau(x, y, positions, config):
            return None
    
    # Vérifier boutons d'action
    x_np, y_np = positions['nouvelle_partie']
    if MenuElements.verifier_clic_bouton(x, y, x_np, y_np, 
                                       positions['largeur_bouton'], 
                                       positions['hauteur_bouton']):
        return _construire_resultat_config(config)
    
    x_q, y_q = positions['quitter']
    if MenuElements.verifier_clic_bouton(x, y, x_q, y_q, 
                                       positions['largeur_bouton'], 
                                       positions['hauteur_bouton']):
        return None  # Quitter sera géré par ferme_fenetre()
    
    return None


def _basculer_option_principale(option, config):
    """Basculer une option principale et gérer les dépendances"""
    config[option] = not config[option]
    
    # Gestion des sous-options
    if option == 'obstacle':
        if config[option]:
            config['obstacle_predefini'] = True
            config['obstacle_aleatoire'] = False
        else:
            config['obstacle_predefini'] = False
            config['obstacle_aleatoire'] = False
    
    elif option == 'bonus':
        if config[option]:
            config['bonus_predefini'] = True
            config['bonus_aleatoire'] = False
        else:
            config['bonus_predefini'] = False
            config['bonus_aleatoire'] = False
    
    elif option == 'niveau':
        if not config[option]:
            config['niveau1'] = False
            config['niveau2'] = False
            config['niveau3'] = False


def _traiter_clic_sous_options_obstacle(x, y, positions, config):
    """Traiter les clics sur les sous-options d'obstacle"""
    x1, y1, w1, h1 = positions['obstacle_predefini']
    x2, y2, w2, h2 = positions['obstacle_aleatoire']
    
    if MenuElements.verifier_clic_bouton(x, y, x1, y1, w1, h1):
        config['obstacle_predefini'] = True
        config['obstacle_aleatoire'] = False
        return True
    
    if MenuElements.verifier_clic_bouton(x, y, x2, y2, w2, h2):
        config['obstacle_predefini'] = False
        config['obstacle_aleatoire'] = True
        return True
    
    return False


def _traiter_clic_sous_options_bonus(x, y, positions, config):
    """Traiter les clics sur les sous-options de bonus"""
    x1, y1, w1, h1 = positions['bonus_predefini']
    x2, y2, w2, h2 = positions['bonus_aleatoire']
    
    if MenuElements.verifier_clic_bouton(x, y, x1, y1, w1, h1):
        config['bonus_predefini'] = True
        config['bonus_aleatoire'] = False
        return True
    
    if MenuElements.verifier_clic_bouton(x, y, x2, y2, w2, h2):
        config['bonus_predefini'] = False
        config['bonus_aleatoire'] = True
        return True
    
    return False


def _traiter_clic_sous_options_niveau(x, y, positions, config):
    """Traiter les clics sur les sous-options de niveau"""
    niveaux = ['niveau1', 'niveau2', 'niveau3']
    
    for niveau in niveaux:
        x_btn, y_btn, w, h = positions[niveau]
        if MenuElements.verifier_clic_bouton(x, y, x_btn, y_btn, w, h):
            # Désactiver tous les niveaux puis activer celui cliqué
            for n in niveaux:
                config[n] = False
            config[niveau] = True
            return True
    
    return False


def _construire_resultat_config(config):
    """Construire le tuple de résultat de configuration"""
    return (
        config['scorev'], config['vitesse'], config['obstacle'], config['bonus'],
        config['deux'], config['niveau'], True,  # start = True
        config['obstacle_predefini'], config['obstacle_aleatoire'],
        config['niveau1'], config['niveau2'], config['niveau3'],
        config['bonus_aleatoire'], config['bonus_predefini']
    )