# 🎮 Jeu QIX - Version Refactorisée

**Auteurs :** Raphaël DAVIOT & Abdelrahim RICHE  
**Date de création :** 06/01/2024  
**Dernière mise à jour :** 02/11/2025  
**Version :** 2.0 - Refactorisée & Optimisée

---

## 📋 Description du Jeu

QIX est un jeu classique d'arcade revisité avec une architecture moderne. Le joueur contrôle un personnage (Pac-Man) qui doit conquérir **75% de l'aire de jeu** en dessinant des polygones, tout en évitant le QIX qui se déplace aléatoirement dans l'aire de jeu, ainsi que les Sparks qui patrouillent les bordures.

### 🎯 Objectif
- Remplir 75% de l'aire de jeu en créant des polygones
- Éviter les collisions avec le QIX et les Sparks
- Survivre avec le système de vies limité
- Maximiser son score en fonction de la surface conquise

---

## 🎮 Instructions de Jeu

### 🕹️ Contrôles

#### Joueur 1
- **Déplacement :** Flèches directionnelles (↑↓←→)
- **Traçage :** Barre espace (maintenir enfoncée)
- **Vitesse :** Touche `V` (en zone safe)

#### Joueur 2 (Mode deux joueurs)
- **Déplacement :** ZQSD
- **Traçage :** Touche `M` (maintenir enfoncée)
- **Vitesse :** Touche `V` (en zone safe)

### 📝 Règles de Base
1. Déplacez-vous le long des bordures (zone safe - bleue)
2. Maintenez la barre espace et aventurez-vous dans l'aire de jeu pour tracer
3. Retournez sur les bordures pour fermer un polygone
4. Évitez le QIX (ennemi principal) et les Sparks (ennemis des bordures)
5. Atteignez 75% de surface conquise pour gagner

---

## ✨ Fonctionnalités

### 🎮 Gameplay Principal
- ✅ **Système de polygones** - Création dynamique de formes fermées
- ✅ **QIX intelligent** - IA avec déplacement aléatoire diagonal
- ✅ **Sparks patrouilleurs** - Ennemis suivant les bordures
- ✅ **Système de vies** - Gestion des collisions et game over
- ✅ **Calcul de score** - Basé sur la surface et la vitesse de traçage
- ✅ **Détection de victoire** - Automatique à 75% de surface

### 🎨 Interface & Affichage
- 🖥️ **Interface moderne** - Design épuré avec HUD informatif
- 📊 **Affichage en temps réel** - Score, surface conquise, vies
- 🎯 **Écrans de fin** - Victoire/défaite avec statistiques
- 🌈 **Polygones colorés** - Attribution automatique de couleurs
- 👥 **Interface deux joueurs** - Scores et vies séparés

### 🔧 Modes & Variantes

#### 🏅 Niveaux de Difficulté
- **Niveau 1 (Facile)** : QIX lent, 2 Sparks
- **Niveau 2 (Moyen)** : QIX rapide, 4 Sparks
- **Niveau 3 (Difficile)** : QIX très rapide, 6 Sparks

#### 👥 Mode Multijoueur
- **2 joueurs simultanés** - Compétition en temps réel
- **Mécaniques d'interaction** :
  - Enfermement de l'adversaire (perte de vie)
  - Croisement de traits (perte de vie)
  - Scores séparés et interface dédiée

#### ⚡ Variantes de Gameplay
- **Mode vitesse** - Changement de vitesse de traçage (lente/rapide)
- **Obstacles** - Éléments fixes ajoutant de la difficulté
- **Bonus/Power-ups** - Invincibilité temporaire (3 secondes)
- **Affichage score** - Activation/désactivation du HUD score

### 🛠️ Système de Configuration
- **Menu de variantes** - Sélection des options avant la partie
- **Configuration prédéfinie** - Obstacles et bonus depuis fichiers
- **Configuration aléatoire** - Génération procédurale d'éléments
- **Paramètres sauvegardés** - Persistance des préférences


## 💾 Installation & Lancement

### 📋 Prérequis
- **Python 3.8+** installé sur votre système
- **Bibliothèque FLTK** pour Python

### 🔧 Installation

#### Option 1 : Installation automatique
```bash
# Cloner le projet
git clone [URL_DU_REPO]
cd QIX_Raphael_DAVIOT_Abdelrahim_RICHE

# Installer les dépendances
pip install fltk
```

#### Option 2 : Installation manuelle FLTK
```bash
# Ubuntu/Debian
sudo apt-get install python3-fltk

# Windows
pip install fltk

# macOS
brew install fltk
pip install fltk
```

### 🚀 Lancement du Jeu

#### Méthode 1 : Double-clic
```
Double-cliquez sur QIX_Raphael_DAVIOT_&_Abdelrahim_RICHE.py
```

#### Méthode 2 : Terminal/Invite de commandes
```bash
# Windows (PowerShell/CMD)
cd "chemin\vers\le\dossier"
python QIX_Raphael_DAVIOT_&_Abdelrahim_RICHE.py

# Linux/macOS (Terminal)
cd /chemin/vers/le/dossier
python3 QIX_Raphael_DAVIOT_&_Abdelrahim_RICHE.py
```

### 📁 Structure des Fichiers Requis
Assurez-vous que le dossier `ressources/` contient :
- 🎮 Sprites des joueurs (Pacman1_*.png, Pacman2_*.png)
- 👻 Sprites des ennemis (Fantome*.png)
- 🍎 Sprites des bonus (Fruit*.png)
- 🖼️ Images d'arrière-plan (background*.png)
- 📄 Fichiers de configuration (obstacles.txt)

---

## 🎮 Guide de Jeu Détaillé

### 🏁 Démarrage
1. **Menu principal** - Choisissez "Jouer" ou "Quitter"
2. **Menu variantes** - Configurez votre partie :
   - Mode 1 ou 2 joueurs
   - Niveau de difficulté (1-3)
   - Options : vitesse, obstacles, bonus, scores
3. **Lancement** - Cliquez pour commencer !

### 🎯 Stratégies de Jeu
- **🛡️ Sécurité d'abord** - Restez en zone safe quand c'est possible
- **⚡ Vitesse optimale** - Tracé rapide = moins de points mais plus sûr
- **🎨 Grands polygones** - Plus de surface = plus de points
- **👁️ Surveillance** - Gardez un œil sur QIX et les Sparks
- **🚀 Bonus intelligents** - Profitez de l'invincibilité pour des zones risquées

### 🏆 Conseils Avancés
- En mode 2 joueurs, utilisez les mécaniques d'enfermement
- Les obstacles peuvent être des alliés (protection contre le QIX)
- La vitesse lente donne plus de points mais augmente les risques
- Planifiez vos polygones pour optimiser l'espace


## 👥 Crédits & Remerciements

**Développeurs Principaux :**
- 👨‍💻 **Raphaël DAVIOT** 
- 👨‍💻 **Abdelrahim RICHE**

**Technologies Utilisées :**
- 🐍 **Python 3.8+** - Langage principal
- 🎨 **FLTK** - Interface graphique et rendu
- 🏗️ **Architecture OOP** - Design patterns et modularité

**Inspiration :**
- 🎮 Jeu original **QIX** (Taito, 1981)
- 🏛️ **Principes SOLID** - Architecture logicielle
- 📚 **Clean Code** - Bonnes pratiques de développement


---

**🎮 Amusez-vous bien avec QIX ! 🎮**

*Projet réalisé avec passion par des étudiants en informatique* 💻✨