from typing import List, Union

from container_packing.dimension import Dimension
from container_packing.largest_area_fit_first_packager import LargestAreaFitFirstPackager
from container_packing.box import Box
from container_packing.box_item import BoxItem


def pack_products_into_restrictions(products: List[tuple],
                                    restrictions: tuple) -> Union[tuple, None]:
    """Pack product into container with given restrictions.

    :param products: list with tuples of width, depth and height of product,
    :param restrictions: tuple with width, depth and height of container,
    :return: tuple with minimal width, depth and height of container
        that can hold all products or None if there is no container with
        given restrictions."""

    container_x, container_y, container_z = restrictions
    containers = [Dimension.new_instance(container_x, container_y, container_z)]
    packager = LargestAreaFitFirstPackager(containers)

    box_items = [BoxItem(Box(x, y, z)) for x, y, z in products]
    match = packager.pack(box_items)

    if not match:
        return None

    # calculating width, depth and height of gotten container
    max_width = max_depth = max_height = 0
    for levels_by_height in match.levels:
        for level in levels_by_height:
            max_width = max(level.space.x + level.box.width, max_width)
            max_depth = max(level.space.y + level.box.depth, max_depth)

            if levels_by_height is match.levels[-1]:
                max_height = max(level.space.z + level.box.height, max_height)

    return max_width, max_depth, max_height
