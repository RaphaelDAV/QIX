"""
Line-level profiling for QixManager._is_valid_qix_position using line_profiler API.
Run from project root with PYTHONPATH set to repo root.
"""
import sys
from pathlib import Path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from managers.qix_manager import QixManager

# Minimal qix instance
class DummyQix:
    def __init__(self, x=300, y=300):
        self.x = x
        self.y = y

q = DummyQix(300, 300)
qm = QixManager(q)

# Build representative zones (lists of [x,y])
zone_safe = [[x, 300] for x in range(50, 450, 5)]  # line of safe points
zone_polygone = []
zone_obstacle = []

# line_profiler usage
from line_profiler import LineProfiler
lp = LineProfiler()
lp.add_function(qm._is_valid_qix_position)

CALLS = 400

for _ in range(CALLS):
    # call with representative coordinates
    lp.runcall(qm._is_valid_qix_position, qm.qix.x, qm.qix.y, zone_safe, zone_polygone, zone_obstacle)

# Print results
lp.print_stats()
