"""
Headless cProfile runner for the QIX project.
This script executes the `jeu()` function from the main file in a headless, controlled way
by injecting no-op UI functions and a fake `touche_pressee` that triggers Escape after
`N_FRAMES` iterations to stop the loop.

Usage (from project root):
Set `PYTHONPATH` to the project root and run with the venv python, for example:

    $env:PYTHONPATH = 'C:/Users/riche/Desktop/Abdelrahim/QIX'
    .venv/Scripts/python.exe profiling/run_cprofile_project.py

Outputs a short pstats summary to stdout and writes `profiling/project.prof`.
"""
import os
import sys
import runpy
import cProfile
import pstats
from pathlib import Path

# Ensure project root is on sys.path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

TARGET_FILE = PROJECT_ROOT / 'QIX_Raphael_DAVIOT_&_Abdelrahim_RICHE.py'
if not TARGET_FILE.exists():
    print(f"ERROR: can't find {TARGET_FILE}")
    sys.exit(1)

# Load the main script into a fresh namespace WITHOUT executing the
# `if __name__ == "__main__"` block (avoid showing menus / opening GUI).
source = TARGET_FILE.read_text(encoding='utf-8')
ns = {"__name__": "qix_module_for_profiling"}
exec(compile(source, str(TARGET_FILE), 'exec'), ns)

# Provide a dummy canvas object to the real `fltk` module so decorated
# drawing functions don't raise `FenetreNonCree` during headless profiling.
import importlib
try:
    fltk_mod = importlib.import_module('fltk')
except Exception:
    fltk_mod = None

if fltk_mod is not None:
    class _DummyCanvas:
        def __init__(self):
            class _Root:
                def update(self):
                    return None

            class _C:
                def create_line(self, *a, **k):
                    return 0

                def create_polygon(self, *a, **k):
                    return 0

                def create_rectangle(self, *a, **k):
                    return 0

                def create_oval(self, *a, **k):
                    return 0

                def create_text(self, *a, **k):
                    return 0

                def create_image(self, *a, **k):
                    return 0
                
                def delete(self, *a, **k):
                    return None

                def pack(self, *a, **k):
                    return None

                def bind(self, *a, **k):
                    return None

            self.root = _Root()
            self.canvas = _C()
            self.width = 800
            self.height = 600
            self.ev_queue = []
            self.pressed_keys = set()
        def update(self):
            # mimic CustomCanvas.update without delay
            return None

    # Assign dummy to __canevas so @_fenetre_creee checks pass
    try:
        fltk_mod.__canevas = _DummyCanvas()
    except Exception:
        pass
    # Avoid creating real Tk images during headless profiling
    try:
        fltk_mod.image = lambda *a, **k: None
    except Exception:
        pass
    try:
        fltk_mod._load_tk_image = lambda *a, **k: None
    except Exception:
        pass

# Configure headless behavior
N_FRAMES = 400  # Number of iterations before sending Escape
frame = {'i': 0}

# No-op UI primitives (the main file imports these via `from fltk import *`)
ns['texte'] = lambda *a, **k: None
ns['rectangle'] = lambda *a, **k: None
ns['efface'] = lambda *a, **k: None
ns['ferme_fenetre'] = lambda *a, **k: None
ns['creer_fenetre_jeu'] = lambda *a, **k: (800, 600)
ns['creer_interface_complete'] = lambda *a, **k: None
ns['afficher_interface_2_joueurs'] = lambda *a, **k: None
ns['rectangle'] = lambda *a, **k: None
ns['donne_ev'] = lambda : None
ns['type_ev'] = lambda ev: None

# Fake touche_pressee: returns True for Escape after N_FRAMES checks
def fake_touche_pressee(key):
    # Count how many times Escape was checked; when above threshold, signal Escape
    if key == "Escape":
        frame['i'] += 1
        return frame['i'] > N_FRAMES
    # Otherwise simulate no-other-key pressed
    return False

ns['touche_pressee'] = fake_touche_pressee

# Run cProfile on jeu()
prof_file = PROJECT_ROOT / 'profiling' / 'project.prof'
print(f"Running headless cProfile for {N_FRAMES} frames (profiling file: {prof_file})...")
pr = cProfile.Profile()
try:
    pr.enable()
    # Execute the main loop (jeu) from the loaded namespace
    if 'jeu' not in ns:
        print("ERROR: 'jeu' not found in the module namespace")
        sys.exit(1)
    ns['jeu']()
    pr.disable()
except SystemExit:
    # jeu() may call sys.exit or close the window; ignore
    pr.disable()
except Exception as exc:
    pr.disable()
    print(f"Exception while running headless jeu(): {exc!r}")

# Save and print top stats
prof_file.parent.mkdir(parents=True, exist_ok=True)
pr.dump_stats(str(prof_file))
ps = pstats.Stats(pr).strip_dirs().sort_stats('cumtime')
print('\nTop 20 functions by cumulative time:')
ps.print_stats(20)

print('\nSaved profile to:', prof_file)
print('Done.')
