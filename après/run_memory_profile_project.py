import os
import sys
import subprocess
import glob
import shutil

this_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(this_dir, '..'))
main_script = os.path.join(project_root, 'après/QIX_Raphael_DAVIOT_&_Abdelrahim_RICHE.py')
script_basename = os.path.basename(main_script)

if not os.path.exists(main_script):
    print(f"Main script not found: {main_script}")
    sys.exit(1)

mprof_cmd = shutil.which('mprof')
if mprof_cmd is None:
    print('mprof not found in PATH. Install memory_profiler (pip install memory-profiler) to get mprof.')
    sys.exit(1)

print(f"Running: mprof run {script_basename} (cwd={this_dir})")
res = subprocess.run([mprof_cmd, 'run', script_basename], cwd=this_dir)
if res.returncode != 0:
    print('mprof run failed.')
    sys.exit(res.returncode)

candidates = glob.glob(os.path.join(this_dir, 'mprofile_*.dat'))
if not candidates:
    candidates = glob.glob(os.path.join(project_root, 'mprofile_*.dat')) or glob.glob(os.path.join(os.getcwd(), 'mprofile_*.dat'))

if not candidates:
    print('No mprofile_*.dat produced. Check mprof output for errors.')
    sys.exit(1)

candidates.sort(key=os.path.getmtime, reverse=True)
src = candidates[0]
stats_dir = os.path.join(project_root, 'stats', 'après')
os.makedirs(stats_dir, exist_ok=True)
dst = os.path.join(stats_dir, 'project_memory_après.dat')
try:
    if os.path.abspath(src) != os.path.abspath(dst):
        shutil.move(src, dst)
    print(f'Memory profile saved to {dst}')
except Exception as e:
    print('Failed to move memory profile file:', e)
    sys.exit(1)

print('You can visualise memory traces with `mprof plot <path>` or inspect with memory_profiler utilities.')
