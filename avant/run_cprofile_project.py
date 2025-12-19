import os
import sys
import runpy
import cProfile
import importlib.util
import types

this_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(this_dir, '..'))
main_script = os.path.join(project_root, 'avant/QIX_Raphael_DAVIOT_&_Nael_AIT_AISSI.py')
stats_dir = os.path.join(project_root, 'stats', 'avant')
os.makedirs(stats_dir, exist_ok=True)
output_file = os.path.join(stats_dir, 'project_cpu_avant.prof')

if not os.path.exists(main_script):
    print(f"Main script not found: {main_script}")
    sys.exit(1)

print(f"Profiling {main_script} with cProfile -> {output_file}")
pr = cProfile.Profile()
old_cwd = os.getcwd()
# Build a minimal in-memory headless stub for `fltk` so the GUI is never opened
def _make_noop(ret=None):
    def f(*a, **k):
        return ret
    return f

fltk_stub = types.ModuleType('fltk')
# functions that may be called by the game; return sensible defaults when needed
no_ret_funcs = ['cree_fenetre', 'ferme_fenetre', 'mise_a_jour', 'efface', 'efface_tout', 'attente']
int_ret_funcs = ['image', 'rectangle', 'ligne', 'polygone', 'texte']
for n in no_ret_funcs:
    setattr(fltk_stub, n, _make_noop(None))
for n in int_ret_funcs:
    setattr(fltk_stub, n, _make_noop(0))
setattr(fltk_stub, 'touche_pressee', _make_noop(lambda k: False))
setattr(fltk_stub, 'hauteur_fenetre', _make_noop(600))
setattr(fltk_stub, 'largeur_fenetre', _make_noop(800))

original_fltk = sys.modules.get('fltk')
try:
    # inject our stub (overrides any real fltk import during the run)
    sys.modules['fltk'] = fltk_stub
    try:
        pr.enable()
        os.chdir(this_dir)
        runpy.run_path(main_script, run_name='__main__')
    finally:
        pr.disable()
        pr.dump_stats(output_file)
        print('Profiling complete.')
        print(f'Profile saved to: {output_file}')
        print('You can inspect the results with `python -m pstats <path>` or using snakeviz <path>')
finally:
    # restore original module if any and cwd
    if original_fltk is not None:
        sys.modules['fltk'] = original_fltk
    else:
        sys.modules.pop('fltk', None)
    os.chdir(old_cwd)
