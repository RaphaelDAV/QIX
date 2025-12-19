import os
import sys
import subprocess
import shutil

this_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(this_dir, '..'))
main_script = os.path.join(project_root, 'après/QIX_Raphael_DAVIOT_&_Abdelrahim_RICHE.py')
script_basename = os.path.basename(main_script)
expected_lprof = os.path.join(this_dir, script_basename + '.lprof')
stats_dir = os.path.join(project_root, 'stats', 'après')
os.makedirs(stats_dir, exist_ok=True)
output_lprof = os.path.join(stats_dir, 'project_line_après.lprof')

if not os.path.exists(main_script):
    print(f"Main script not found: {main_script}")
    sys.exit(1)

kernprof_cmd = shutil.which('kernprof')
if kernprof_cmd is None:
    print('kernprof not found in PATH. Install line_profiler (pip install line_profiler) to get kernprof.')
    sys.exit(1)

print(f"Running: kernprof -l {script_basename} (cwd={this_dir})")
import tempfile
import textwrap
tmpdir = tempfile.mkdtemp(prefix='fltk_stub_')
stub_file = os.path.join(tmpdir, 'fltk.py')
with open(stub_file, 'w', encoding='utf-8') as f:
    f.write(textwrap.dedent('''
        # Minimal headless stub for fltk used during profiling
        def cree_fenetre(*args, **kwargs):
            return None
        def ferme_fenetre():
            return None
        def mise_a_jour():
            return None
        def image(*args, **kwargs):
            return 0
        def rectangle(*args, **kwargs):
            return 0
        def ligne(*args, **kwargs):
            return 0
        def polygone(*args, **kwargs):
            return 0
        def texte(*args, **kwargs):
            return 0
        def efface(*args, **kwargs):
            return None
        def efface_tout():
            return None
        def attente(t):
            pass
        def touche_pressee(key):
            return lambda k: False
        def hauteur_fenetre():
            return 600
        def largeur_fenetre():
            return 800
    '''))

env = os.environ.copy()
env['PYTHONPATH'] = tmpdir + os.pathsep + env.get('PYTHONPATH', '')
res = subprocess.run([kernprof_cmd, '-l', script_basename], cwd=this_dir, env=env)
if res.returncode != 0:
    print('kernprof failed.')
    try:
        shutil.rmtree(tmpdir)
    except Exception:
        pass
    sys.exit(res.returncode)

try:
    shutil.rmtree(tmpdir)
except Exception:
    pass
    
if os.path.exists(expected_lprof):
    try:
        shutil.move(expected_lprof, output_lprof)
        print(f'Line profile saved to {output_lprof}')
    except Exception as e:
        print('Failed to move lprof file:', e)
        sys.exit(1)
else:
    print('Expected .lprof file not found. kernprof may not have produced output.')
    sys.exit(1)

print('You can inspect the results with `python -m line_profiler <path>` or `kernprof -lv` prints during run.')
