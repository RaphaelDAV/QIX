#!/usr/bin/env python3
"""
Profile the `Ancien.py` file for a fixed duration (headless stub for `fltk`).

Usage:
    python tools\profile_ancien.py 10 --no-window
"""
from __future__ import annotations

import argparse
import cProfile
import importlib.util
import io
import os
import pstats
import sys
import threading


def load_module(path: str, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def make_fltk_stub():
    import types
    stub = types.ModuleType('fltk')

    def _noop(*a, **k):
        return None

    def _attend_clic_gauche():
        return (0, 0)

    def _attend_ev():
        return (None, None)

    def _attend_fermeture():
        return None

    def _attente(t):
        import time
        time.sleep(t)

    stub.cree_fenetre = _noop
    stub.ferme_fenetre = _noop
    stub.redimensionne_fenetre = _noop
    stub.mise_a_jour = _noop
    stub.ligne = _noop
    stub.fleche = _noop
    stub.polygone = _noop
    stub.rectangle = _noop
    stub.cercle = _noop
    stub.arc = _noop
    stub.point = _noop
    stub.image = _noop
    stub.texte = _noop
    stub.taille_texte = lambda *a, **k: (0, 0)
    stub.efface_tout = _noop
    stub.efface = _noop
    stub.attente = _attente
    stub.capture_ecran = _noop
    stub.touche_pressee = lambda *a, **k: False
    stub.abscisse_souris = lambda: 0
    stub.ordonnee_souris = lambda: 0
    stub.hauteur_fenetre = lambda: 800
    stub.largeur_fenetre = lambda: 600
    stub.donne_ev = _noop
    stub.attend_ev = _attend_ev
    stub.attend_clic_gauche = _attend_clic_gauche
    stub.attend_fermeture = _attend_fermeture
    stub.type_ev = lambda ev: None
    stub.abscisse = lambda ev: None
    stub.ordonnee = lambda ev: None
    stub.touche = lambda ev: ''

    stub.__all__ = [
        'cree_fenetre','ferme_fenetre','redimensionne_fenetre','mise_a_jour',
        'ligne','fleche','polygone','rectangle','cercle','arc','point','image','texte','taille_texte',
        'efface_tout','efface','attente','capture_ecran','touche_pressee','abscisse_souris','ordonnee_souris',
        'hauteur_fenetre','largeur_fenetre','donne_ev','attend_ev','attend_clic_gauche','attend_fermeture',
        'type_ev','abscisse','ordonnee','touche'
    ]

    sys.modules['fltk'] = stub


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('seconds', nargs='?', type=int, default=10,
                        help='Duration to profile (seconds). Ignored with --interactive')
    parser.add_argument('--no-window', action='store_true', help='Run headless (inject fltk stub)')
    parser.add_argument('--no-profile', action='store_true', help='Run without cProfile (just launch game)')
    parser.add_argument('--run', action='store_true', help='Launch the interactive menu/game instead of calling jeu() directly')
    parser.add_argument('--interactive', action='store_true', help='Open the game window and let the user play; profile until the game ends')
    args = parser.parse_args()

    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    script_path = os.path.join(repo_root, 'Ancien.py')


    if args.no_window:
        make_fltk_stub()

    if repo_root not in sys.path:
        sys.path.insert(0, repo_root)

    print(f'Loading {script_path}')
    ancien = load_module(script_path, 'Ancien_module')

    # Prepare some globals used by jeu()
    defaults = dict(
        deux=False,
        scorev=False,
        vitesse=False,
        obstacle=False,
        bonus=False,
        niveau1=False,
        niveau2=False,
        niveau3=False,
        obstacle_predefini=False,
        obstacle_aleatoire=False,
        bonus_predefini=False,
        bonus_aleatoire=False,
    )
    for k, v in defaults.items():
        setattr(ancien, k, v)

    # If user requested to run without profiling, just launch interactive menu/game
    if args.no_profile:
        try:
            # Emulate the script's main flow: Accueil -> variantes -> fenetre -> jeu
            if args.run and hasattr(ancien, 'Accueil'):
                menu = ancien.Accueil()
                if menu and hasattr(ancien, 'variantes'):
                    config = ancien.variantes()
                    if config and isinstance(config, tuple) and len(config) >= 7 and config[6]:
                        # Unpack config into module-level variables expected by jeu()
                        (
                            ancien.scorev,
                            ancien.vitesse,
                            ancien.obstacle,
                            ancien.bonus,
                            ancien.deux,
                            ancien.niveau,
                            ancien.start,
                            ancien.obstacle_predefini,
                            ancien.obstacle_aleatoire,
                            ancien.niveau1,
                            ancien.niveau2,
                            ancien.niveau3,
                            ancien.bonus_aleatoire,
                            ancien.bonus_predefini,
                        ) = config
                        # Create the game window and start the main loop
                        if hasattr(ancien, 'fenetre'):
                            ancien.fenetre()
                        if hasattr(ancien, 'jeu'):
                            ancien.jeu()
                        return
                return
            elif args.run and hasattr(ancien, 'variantes'):
                # If Accueil not present, directly call variantes
                config = ancien.variantes()
                if config and isinstance(config, tuple) and len(config) >= 7 and config[6]:
                    (
                        ancien.scorev,
                        ancien.vitesse,
                        ancien.obstacle,
                        ancien.bonus,
                        ancien.deux,
                        ancien.niveau,
                        ancien.start,
                        ancien.obstacle_predefini,
                        ancien.obstacle_aleatoire,
                        ancien.niveau1,
                        ancien.niveau2,
                        ancien.niveau3,
                        ancien.bonus_aleatoire,
                        ancien.bonus_predefini,
                    ) = config
                    if hasattr(ancien, 'fenetre'):
                        ancien.fenetre()
                    if hasattr(ancien, 'jeu'):
                        ancien.jeu()
                    return
            elif hasattr(ancien, 'jeu'):
                ancien.jeu()
                return
            else:
                print('No entry point found in Ancien.py (tried Accueil, variantes, jeu)')
        except Exception as e:
            print('Exception while running Ancien.py:', e)
        finally:
            return

    # Otherwise run under cProfile and stop after timeout
    prof = cProfile.Profile()
    prof.enable()

    out_prof = os.path.join(repo_root, 'profiling_ancien.prof')
    out_txt = os.path.join(repo_root, 'profiling_ancien_top.txt')

    # Stopper that will dump stats and exit process after timeout
    def stopper():
        try:
            prof.disable()
            prof.dump_stats(out_prof)

            s = io.StringIO()
            ps = pstats.Stats(prof, stream=s).sort_stats('cumtime')
            ps.print_stats(30)
            with open(out_txt, 'w', encoding='utf-8') as f:
                f.write(s.getvalue())
            print(f'Wrote profiling data to: {out_prof}')
            print(f'Wrote top functions to: {out_txt}')
            print(s.getvalue())
        finally:
            # Hard exit
            os._exit(0)

    timer = threading.Timer(args.seconds, stopper)
    timer.daemon = True
    timer.start()

    try:
        # Call jeu(); this will be profiled and terminated by timer
        if args.run and hasattr(ancien, 'Accueil'):
            ancien.Accueil()
        elif args.run and hasattr(ancien, 'variantes'):
            ancien.variantes()
        elif hasattr(ancien, 'jeu'):
            ancien.jeu()
        else:
            print('No jeu() in Ancien.py')
    except SystemExit:
        pass
    except Exception as e:
        # Dump profiler even on exception
        prof.disable()
        prof.dump_stats(out_prof)
        s = io.StringIO()
        ps = pstats.Stats(prof, stream=s).sort_stats('cumtime')
        ps.print_stats(30)
        with open(out_txt, 'w', encoding='utf-8') as f:
            f.write(s.getvalue())
        print('Exception during jeu():', e)
        print(s.getvalue())


if __name__ == '__main__':
    main()
