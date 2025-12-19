import os
import sys
import subprocess
import glob
import shutil

this_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(this_dir, '..'))
main_script = os.path.join(project_root, 'avant/QIX_Raphael_DAVIOT_&_Nael_AIT_AISSI.py')
script_basename = os.path.basename(main_script)

if not os.path.exists(main_script):
    print(f"Main script not found: {main_script}")
    sys.exit(1)

mprof_cmd = shutil.which('mprof')
if mprof_cmd is None:
    print('mprof not found in PATH. Install memory_profiler (pip install memory-profiler) to get mprof.')
    sys.exit(1)

print(f"Running: mprof run {script_basename} (cwd={this_dir})")
import tempfile
import textwrap

# Create a temporary workspace and copy the main script there so imports resolve to our stub
tmpdir = tempfile.mkdtemp(prefix='fltk_stub_')
copied_script = os.path.join(tmpdir, script_basename)
shutil.copy2(main_script, copied_script)

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

# Run mprof inside tmpdir so imports pick up our stub fltk.py
res = subprocess.run([mprof_cmd, 'run', script_basename], cwd=tmpdir)
if res.returncode != 0:
    print('mprof run failed.')
    try:
        shutil.rmtree(tmpdir)
    except Exception:
        pass
    sys.exit(res.returncode)

candidates = glob.glob(os.path.join(tmpdir, 'mprofile_*.dat'))
if not candidates:
    candidates = glob.glob(os.path.join(this_dir, 'mprofile_*.dat')) or glob.glob(os.path.join(project_root, 'mprofile_*.dat')) or glob.glob(os.path.join(os.getcwd(), 'mprofile_*.dat'))

if not candidates:
    print('No mprofile_*.dat produced. Check mprof output for errors.')
    sys.exit(1)

candidates.sort(key=os.path.getmtime, reverse=True)
src = candidates[0]
stats_dir = os.path.join(project_root, 'stats', 'avant')
os.makedirs(stats_dir, exist_ok=True)
dst = os.path.join(stats_dir, 'project_memory_avant.dat')
try:
    if os.path.abspath(src) != os.path.abspath(dst):
        shutil.move(src, dst)
    print(f'Memory profile saved to {dst}')
except Exception as e:
    print('Failed to move memory profile file:', e)
    sys.exit(1)

try:
    shutil.rmtree(tmpdir)
except Exception:
    pass

print('You can visualise memory traces with `mprof plot <path>` or inspect with memory_profiler utilities.')
