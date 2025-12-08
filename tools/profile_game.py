#!/usr/bin/env python3
"""
Profile the QIX game for a fixed duration using cProfile.

Creates `profiling.prof` (raw cProfile data) and `profiling_top.txt`
with the top 30 functions sorted by cumulative time.

Usage:
    python tools\profile_game.py 10
    python tools\profile_game.py 10 --no-window
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


def load_game_module(path: str):
    spec = importlib.util.spec_from_file_location("qix_game", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main():
    parser = argparse.ArgumentParser(description="Profile the QIX game for a few seconds")
    parser.add_argument("seconds", nargs="?", type=int, default=10, help="Duration to profile (seconds)")
    parser.add_argument("--no-window", action="store_true", help="Do not open the game window (headless)")
    args = parser.parse_args()

    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    game_path = os.path.join(repo_root, "QIX_Raphael_DAVIOT_&_Abdelrahim_RICHE.py")

    if not os.path.isfile(game_path):
        print(f"Game file not found: {game_path}", file=sys.stderr)
        sys.exit(2)

    # If running headless, inject a minimal `fltk` stub so the game's top-level
    # imports succeed. The stub is minimal and only provides no-op functions
    # needed by the code to run without a GUI.
    if args.no_window:
        import types
        import sys as _sys

        if 'fltk' not in _sys.modules:
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

            # Expose common names used in the project
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
            stub.touche_pressee = lambda: False
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

            # Make `from fltk import *` produce the names in the namespace when
            # the module is imported. We achieve this by setting __all__ and
            # copying attributes to a simple dict used by the importer.
            stub.__all__ = [
                'cree_fenetre','ferme_fenetre','redimensionne_fenetre','mise_a_jour',
                'ligne','fleche','polygone','rectangle','cercle','arc','point','image','texte','taille_texte',
                'efface_tout','efface','attente','capture_ecran','touche_pressee','abscisse_souris','ordonnee_souris',
                'hauteur_fenetre','largeur_fenetre','donne_ev','attend_ev','attend_clic_gauche','attend_fermeture',
                'type_ev','abscisse','ordonnee','touche'
            ]

            _sys.modules['fltk'] = stub

    # Ensure repo root is on sys.path so package imports like `config` resolve
    if repo_root not in sys.path:
        sys.path.insert(0, repo_root)

    print(f"Loading game from: {game_path}")
    game = load_game_module(game_path)

    # Build a sane default config (level 1, start immediately)
    config = (
        False,  # scorev
        False,  # vitesse
        False,  # obstacle
        False,  # bonus
        False,  # deux (two-player)
        True,   # niveau (enable level selector)
        True,   # start
        False,  # obstacle_predefini
        False,  # obstacle_aleatoire
        True,   # niveau1
        False,  # niveau2
        False,  # niveau3
        False,  # bonus_aleatoire
        False,  # bonus_predefini
    )

    try:
        game.configurer_game_state(config)
    except Exception as e:
        print("Failed to configure game state:", e, file=sys.stderr)

    # Stopper qui fermera la fenêtre proprement après X secondes
    def stop():
        try:
            game.ferme_fenetre_securise()
        except Exception:
            pass

    stopper = threading.Timer(args.seconds, stop)
    stopper.start()

    prof = cProfile.Profile()
    prof.enable()
    try:
        # Create window unless requested otherwise
        if not args.no_window:
            try:
                game.fenetre()
            except Exception as e:
                print("Warning: could not create window:", e, file=sys.stderr)

        # Run the main game loop (will be interrupted by `stop` timer)
        try:
            game.jeu()
        except Exception as e:
            print("Game loop exited with exception:", e, file=sys.stderr)

    finally:
        prof.disable()
        stopper.cancel()

        out_prof = os.path.join(os.getcwd(), "profiling.prof")
        prof.dump_stats(out_prof)

        s = io.StringIO()
        ps = pstats.Stats(prof, stream=s).sort_stats("cumtime")
        ps.print_stats(30)

        out_txt = os.path.join(os.getcwd(), "profiling_top.txt")
        with open(out_txt, "w", encoding="utf-8") as f:
            f.write(s.getvalue())

        print(f"Wrote profiling data to: {out_prof}")
        print(f"Wrote top functions to: {out_txt}")
        print(s.getvalue())


if __name__ == "__main__":
    main()
