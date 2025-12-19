import os
import sys
import subprocess
import shutil

this_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(this_dir, '..'))
main_script = os.path.join(project_root, 'avant/QIX_Raphael_DAVIOT_&_Nael_AIT_AISSI.py')
script_basename = os.path.basename(main_script)
expected_lprof = os.path.join(this_dir, script_basename + '.lprof')
stats_dir = os.path.join(project_root, 'stats', 'avant')
os.makedirs(stats_dir, exist_ok=True)
output_lprof = os.path.join(stats_dir, 'project_line_avant.lprof')

if not os.path.exists(main_script):
    print(f"Main script not found: {main_script}")
    sys.exit(1)

kernprof_cmd = shutil.which('kernprof')
if kernprof_cmd is None:
    print('kernprof not found in PATH. Install line_profiler (pip install line_profiler) to get kernprof.')
    sys.exit(1)

print(f"Running: kernprof -l {script_basename} (cwd={this_dir})")
res = subprocess.run([kernprof_cmd, '-l', script_basename], cwd=this_dir)
if res.returncode != 0:
    print('kernprof failed.')
    sys.exit(res.returncode)
    
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
