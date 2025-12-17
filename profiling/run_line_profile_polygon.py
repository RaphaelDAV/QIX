from line_profiler import LineProfiler
from config.constants import GRILLE_PAS
from managers.polygon_manager import PolygonManager

# Build polygon as before
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

pm = PolygonManager(['red', 'green', 'blue'])

lp = LineProfiler()
# add the bound method to the profiler
lp.add_function(pm._est_point_dans_polygone)
# run the heavy function under the profiler
lp.runcall(pm.generer_positions_interieures, poly)
# print results
lp.print_stats()
