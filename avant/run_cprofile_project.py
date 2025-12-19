import os
import sys
import runpy
import cProfile
import importlib.util

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
try:
    os.chdir(this_dir)
    try:
        import fltk as _real_fltk
    except Exception:
        stub_path = os.path.join(this_dir, 'fltk_headless.py')
        if os.path.exists(stub_path):
            spec = importlib.util.spec_from_file_location('fltk', stub_path)
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            sys.modules['fltk'] = mod
    pr.enable()
    runpy.run_path(main_script, run_name='__main__')
finally:
    try:
        pr.disable()
        pr.dump_stats(output_file)
        print('Profiling complete.')
        print(f'Profile saved to: {output_file}')
        print('You can inspect the results with `python -m pstats <path>` or using snakeviz <path>')
    finally:
        os.chdir(old_cwd)
