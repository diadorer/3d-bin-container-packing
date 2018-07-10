import random

from container_packing.dimension import Dimension
from container_packing.largest_area_fit_first_packager import LargestAreaFitFirstPackager
from container_packing.box import Box
from container_packing.box_item import BoxItem



containers = [Dimension.new_instance(50, 80, 5000)]
packager = LargestAreaFitFirstPackager(containers)

products = [
    BoxItem(Box("Foot", 30, 10, 2), 1),
    BoxItem(Box("Head", 33, 30, 3), 1),
    BoxItem(Box("Leg", 17, 5, 5), 1),
    *[BoxItem(Box("Random here", random.randint(1, 50), random.randint(1, 58), random.randint(1, 30)), 1)
      for _ in range(50)]
]

# products = [
#     BoxItem(Box("Random here", 35, 37, 9), 1),
#     BoxItem(Box("Random here", 46, 8, 16), 1),
#     BoxItem(Box("Random here", 24, 31, 10), 1),
#     BoxItem(Box("Random here", 44, 39, 14), 1),
#     BoxItem(Box("Random here", 10, 15, 28), 1),
#     BoxItem(Box("Random here", 49, 4, 23), 1),
#     BoxItem(Box("Random here", 44, 10, 2), 1),
#     BoxItem(Box("Random here", 27, 27, 28), 1),
#     BoxItem(Box("Random here", 47, 19, 25), 1),
#     BoxItem(Box("Random here", 26, 1, 15), 1),
#     BoxItem(Box("Random here", 50, 39, 14), 1),
#     BoxItem(Box("Random here", 22, 37, 16), 1),
#     BoxItem(Box("Random here", 9, 13, 25), 1),
#     BoxItem(Box("Random here", 3, 53, 16), 1),
#     BoxItem(Box("Random here", 10, 18, 25), 1),
#     BoxItem(Box("Random here", 27, 19, 29), 1),
#     BoxItem(Box("Random here", 20, 52, 8), 1),
#     BoxItem(Box("Random here", 26, 3, 5), 1),
#     BoxItem(Box("Random here", 44, 17, 29), 1),
#     BoxItem(Box("Random here", 17, 49, 25), 1),
#     BoxItem(Box("Random here", 48, 35, 11), 1),
#     BoxItem(Box("Random here", 28, 10, 9), 1),
#     BoxItem(Box("Random here", 49, 48, 15), 1),
#     BoxItem(Box("Random here", 38, 1, 12), 1),
#     BoxItem(Box("Random here", 49, 10, 21), 1),
#     BoxItem(Box("Random here", 2, 22, 29), 1),
#     BoxItem(Box("Random here", 24, 44, 3), 1),
#     BoxItem(Box("Random here", 16, 48, 23), 1),
#     BoxItem(Box("Random here", 42, 12, 19), 1),
#     BoxItem(Box("Random here", 38, 53, 10), 1),
#     BoxItem(Box("Random here", 38, 16, 23), 1),
#     BoxItem(Box("Random here", 29, 5, 3), 1),
#     BoxItem(Box("Random here", 44, 54, 14), 1),
#     BoxItem(Box("Random here", 14, 51, 17), 1),
#     BoxItem(Box("Random here", 9, 8, 21), 1),
#     BoxItem(Box("Random here", 15, 37, 1), 1),
#     BoxItem(Box("Random here", 29, 58, 28), 1),
#     BoxItem(Box("Random here", 13, 44, 20), 1),
#     BoxItem(Box("Random here", 43, 48, 19), 1),
#     BoxItem(Box("Random here", 33, 26, 5), 1),
#     BoxItem(Box("Random here", 36, 56, 16), 1),
#     BoxItem(Box("Random here", 38, 48, 18), 1),
#     BoxItem(Box("Random here", 44, 40, 29), 1),
#     BoxItem(Box("Random here", 22, 34, 26), 1),
#     BoxItem(Box("Random here", 36, 18, 17), 1),
#     BoxItem(Box("Random here", 1, 4, 7), 1),
#     BoxItem(Box("Random here", 7, 1, 23), 1),
#     BoxItem(Box("Random here", 21, 8, 5), 1),
#     BoxItem(Box("Random here", 32, 53, 10), 1),
#     BoxItem(Box("Random here", 13, 43, 4), 1),
#     BoxItem(Box("Random here", 26, 33, 7), 1),
#     BoxItem(Box("Random here", 6, 16, 21), 1),
#     BoxItem(Box("Random here", 43, 7, 20), 1),
#     BoxItem(Box("Random here", 12, 17, 30), 1),
#     BoxItem(Box("Random here", 30, 32, 29), 1),
#     BoxItem(Box("Random here", 31, 49, 8), 1),
#     BoxItem(Box("Random here", 49, 35, 12), 1),
#     BoxItem(Box("Random here", 33, 26, 13), 1),
#     BoxItem(Box("Random here", 21, 34, 1), 1),
#     BoxItem(Box("Random here", 47, 32, 21), 1),
#     BoxItem(Box("Random here", 28, 2, 25), 1),
#     BoxItem(Box("Random here", 43, 16, 11), 1),
#     BoxItem(Box("Random here", 16, 58, 18), 1),
#     BoxItem(Box("Random here", 2, 10, 14), 1),
#     BoxItem(Box("Random here", 8, 40, 22), 1),
#     BoxItem(Box("Random here", 21, 4, 27), 1),
#     BoxItem(Box("Random here", 45, 12, 19), 1),
#     BoxItem(Box("Random here", 40, 24, 6), 1),
#     BoxItem(Box("Random here", 13, 20, 15), 1),
#     BoxItem(Box("Random here", 42, 17, 15), 1),
#     BoxItem(Box("Random here", 9, 7, 5), 1),
#     BoxItem(Box("Random here", 41, 38, 15), 1),
#     BoxItem(Box("Random here", 30, 32, 10), 1),
#     BoxItem(Box("Random here", 17, 48, 30), 1),
#     BoxItem(Box("Random here", 32, 14, 21), 1),
#     BoxItem(Box("Random here", 7, 50, 4), 1),
#     BoxItem(Box("Random here", 22, 35, 18), 1),
#     BoxItem(Box("Random here", 16, 5, 4), 1),
#     BoxItem(Box("Random here", 22, 49, 30), 1),
#     BoxItem(Box("Random here", 30, 50, 3), 1),
#     BoxItem(Box("Random here", 11, 4, 10), 1),
#     BoxItem(Box("Random here", 29, 48, 26), 1),
#     BoxItem(Box("Random here", 8, 54, 4), 1),
#     BoxItem(Box("Random here", 29, 30, 2), 1),
#     BoxItem(Box("Random here", 12, 44, 4), 1),
#     BoxItem(Box("Random here", 34, 4, 2), 1),
#     BoxItem(Box("Random here", 18, 36, 28), 1),
#     BoxItem(Box("Random here", 49, 50, 14), 1),
#     BoxItem(Box("Random here", 36, 43, 4), 1),
#     BoxItem(Box("Random here", 45, 40, 21), 1),
#     BoxItem(Box("Random here", 17, 12, 26), 1),
#     BoxItem(Box("Random here", 24, 17, 5), 1),
#     BoxItem(Box("Random here", 11, 24, 9), 1),
#     BoxItem(Box("Random here", 16, 1, 10), 1),
#     BoxItem(Box("Random here", 37, 9, 27), 1),
#     BoxItem(Box("Random here", 44, 21, 10), 1),
#     BoxItem(Box("Random here", 32, 3, 3), 1),
#     BoxItem(Box("Random here", 8, 23, 17), 1),
#     BoxItem(Box("Random here", 20, 3, 3), 1),
#     BoxItem(Box("Random here", 39, 34, 17), 1)
# ]


# import time
# begin = time.time()
# match = packager.pack(products)
# print(f'it was only {time.time() - begin} seconds!')



def pack(c):

    products = [
        BoxItem(Box("Random here", random.randint(1, 50), random.randint(1, 58), random.randint(1, 30)), 1)
        for _ in range(c)
    ]
    # print('products is')
    # print(products)

    import time
    begin = time.time()
    # try:
    match = packager.pack(products)
    # except:
    #     print('exception here')
    #     pass
    print(f'it was only {time.time() - begin} seconds!')
    return match
    # print(match.levels)


bug_products = [
    BoxItem(Box(24, 55, 22), 1),
    BoxItem(Box(28, 41, 23), 1),
    BoxItem(Box(11, 44, 22), 1),
    BoxItem(Box(23, 18, 14), 1),
    BoxItem(Box(13, 37, 19), 1)
]

parse_products = lambda a: [(name, w.replace('width=', ''),
                             d.replace('depth=', ''),
                             h.replace('height=', ''),
                             c.replace('count=', '').replace(']', ''))
                            for (name, w, d, h, v, c, *_) in [i.split(', ')
                                                              for i in a.split('BoxItem [Box [name=')[1:]]]

def get_py(items):
    for n, w, d, h, c in items:
        print(f'BoxItem(Box("{n}", {w}, {d}, {h}), {c}),')


def get_java(items):
    for n, w, d, h, c in items:
        print(f'products.add(new BoxItem(new Box("{n}", {w}, {d}, {h}), {c}));')
