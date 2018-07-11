import random

from container_packing.dimension import Dimension
from container_packing.largest_area_fit_first_packager import LargestAreaFitFirstPackager
from container_packing.box import Box
from container_packing.box_item import BoxItem


containers = [Dimension.new_instance(50, 80, 5000)]
packager = LargestAreaFitFirstPackager(containers)

def pack(c):

    products = [
        BoxItem(Box("Random here", random.randint(1, 50), random.randint(1, 58), random.randint(1, 30)), 1)
        for _ in range(c)
    ]

    import time
    begin = time.time()
    match = packager.pack(products)
    print(f'it was only {time.time() - begin} seconds!')
    return match


