from memory_profiler import memory_usage
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

def main():
    pm = PolygonManager(['red','green','blue'])
    # measure memory usage while running the function
    mem_usage, result = memory_usage((pm.generer_positions_interieures, (poly,)), retval=True, interval=0.01)
    print('Memory snapshots (MB):', mem_usage[:5], '... peak:', max(mem_usage))
    print('Generated positions:', len(result))


if __name__ == '__main__':
    main()
