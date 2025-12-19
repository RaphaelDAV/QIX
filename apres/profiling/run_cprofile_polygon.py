import cProfile
import pstats
import io
from managers.polygon_manager import PolygonManager
from config.constants import GRILLE_PAS

# Build a large polygon: rectangle perimeter with step GRILLE_PAS
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

pr = cProfile.Profile()
pr.enable()
# run the heavy function
positions = pm.generer_positions_interieures(poly)
pr.disable()

s = io.StringIO()
ps = pstats.Stats(pr, stream=s).sort_stats('cumtime')
ps.print_stats(30)
print(s.getvalue())
print('Generated positions:', len(positions))
