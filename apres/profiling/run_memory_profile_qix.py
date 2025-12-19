"""
Measure memory usage while calling QixManager._is_valid_qix_position repeatedly.
Run with: 
$env:PYTHONPATH = 'C:/Users/riche/Desktop/Abdelrahim/QIX'
.venv/Scripts/python.exe profiling/run_memory_profile_qix.py
"""
import sys
from pathlib import Path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from managers.qix_manager import QixManager

class DummyQix:
    def __init__(self, x=300, y=300):
        self.x = x
        self.y = y

q = DummyQix(300, 300)
qm = QixManager(q)

zone_safe = [[x, 300] for x in range(50, 450, 5)]
zone_polygone = []
zone_obstacle = []

import tracemalloc

CALLS = 1000

def workload():
    for _ in range(CALLS):
        qm._is_valid_qix_position(q.x, q.y, zone_safe, zone_polygone, zone_obstacle)

if __name__ == '__main__':
    # Use tracemalloc to sample Python allocation peak (no multiprocessing)
    tracemalloc.start()
    workload()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    print(f"Current memory (MB): {current/1024/1024:.3f}")
    print(f"Peak memory (MB): {peak/1024/1024:.3f}")
