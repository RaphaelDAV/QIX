from line_profiler import LineProfiler
from managers.polygon_manager import PolygonManager
from config.constants import GRILLE_PAS

# Build polygon
xmin, ymin, xmax, ymax = 60, 210, 540, 740
poly = []
for x in range(xmin, xmax + 1, GRILLE_PAS):
    poly.append([x, ymin])
for y in range(ymin + GRILLE_PAS, ymax + 1, GRILLE_PAS):
    poly.append([xmax, y])
for x in range(xmax - GRILLE_PAS, xmin - 1, -GRILLE_PAS):
    poly.append([x, ymax])
for y in range(ymax - GRILLE_PAS, ymin, -GRILLE_PAS):
    poly.append([xmin, y])

pm = PolygonManager(['red','green','blue'])
lp = LineProfiler()
lp.add_function(PolygonManager.generer_positions_interieures)
lp.runcall(pm.generer_positions_interieures, poly)
lp.print_stats()
