"""Compare memory profiles before/after optimizations.

Usage (PowerShell):

& .\.venv\Scripts\Activate.ps1
python profiling/compare_memory_profiles.py

It will clone the repository into `profiling_before` if missing, run
`profiling/run_memory_profile_qix.py` in both copies and print a small
report. It also appends the results to `README_MEMORY_OPTIM.md`.
"""
import subprocess
import sys
import shutil
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parents[1]
BEFORE_DIR = ROOT / "profiling_before"

def run_profile(path: Path):
    cmd = [sys.executable, str(path / "profiling" / "run_memory_profile_qix.py")]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    return proc.returncode, proc.stdout, proc.stderr

def parse_output(out: str):
    cur = None
    peak = None
    for line in out.splitlines():
        if line.startswith("Current memory"):
            cur = float(line.split(":")[-1].strip().split()[0])
        if line.startswith("Peak memory"):
            peak = float(line.split(":")[-1].strip().split()[0])
    return cur, peak

def main():
    # clone before if missing
    if not BEFORE_DIR.exists():
        print("Cloning repository to profiling_before for baseline...")
        subprocess.check_call(["git", "clone", ".", str(BEFORE_DIR)])

    print("Running baseline profile (profiling_before)...")
    code_b, out_b, err_b = run_profile(BEFORE_DIR)
    if code_b != 0:
        print("Error running baseline profile:\n", err_b)
        return 1
    cur_b, peak_b = parse_output(out_b)

    print("Running optimized profile (current workspace)...")
    code_a, out_a, err_a = run_profile(ROOT)
    if code_a != 0:
        print("Error running optimized profile:\n", err_a)
        return 1
    cur_a, peak_a = parse_output(out_a)

    report = (
        f"Memory profile comparison ({datetime.now().isoformat()}):\n"
        f"Baseline - Current: {cur_b} MB, Peak: {peak_b} MB\n"
        f"Optimized - Current: {cur_a} MB, Peak: {peak_a} MB\n"
        f"Delta Current: {cur_b - cur_a:.6f} MB, Delta Peak: {peak_b - peak_a:.6f} MB\n"
    )

    print(report)

    # append to README
    readme = ROOT / "README_MEMORY_OPTIM.md"
    with readme.open("a", encoding="utf-8") as f:
        f.write("\n---\n")
        f.write(report)

    return 0

if __name__ == '__main__':
    raise SystemExit(main())
