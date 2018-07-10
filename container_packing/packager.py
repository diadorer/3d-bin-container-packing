import time
from typing import List

from .binary_search_iterator import BinarySearchIterator
from .container import Container
from .dimension import Dimension
from .box_item import BoxItem
from .space import Space
from .placement import Placement


current_time_in_ms = lambda: round(time.time() * 1000)


class Packager:
    """Logical packager for wrapping preprocessing / optimizations."""

    def __init__(self, containers, rotate_3d: bool=True, binary_search: bool=True):
        self.containers = containers
        self.rotate_3d = rotate_3d
        self.binary_search = binary_search
    #
    # def pack(self, boxes, dimensions=None, deadline: int=None):
    #     pass

    def pack(self, boxes, dimensions=None, deadline: int=None):
        java_long_max_value = 9223372036854775807

        if dimensions is None or isinstance(dimensions, int):
            if isinstance(dimensions, int):
                deadline = dimensions
            else:
                deadline = java_long_max_value

            dimensions = self.filter_containers(boxes)
            return self.pack(boxes, dimensions, deadline)

        if deadline is None:
            deadline = java_long_max_value

        if len(dimensions) == 0:
            return None

        pack = self._adapter(boxes)

        if not self.binary_search or len(dimensions) <= 2 or deadline == java_long_max_value:
            for i in range(len(dimensions)):
                if current_time_in_ms() > deadline:
                    break

                result = pack.pack_adapter(boxes, dimensions[i], deadline)
                if result is not None:
                    return result
        else:
            results: List[Container] = [None] * len(dimensions)
            checked: List[int] = [None] * len(results)

            current = []
            for i in range(len(dimensions)):
                current.append(i)

            iterator = BinarySearchIterator()
            while len(current):
                iterator.reset(len(current)-1, 0)

                try:
                    while iterator.has_next():
                        next_ = iterator.next()
                        mid = current[next_]

                        result = pack.pack_adapter(boxes, dimensions[mid], deadline)

                        checked[mid] = True
                        if result is not None:
                            results[mid] = result

                            iterator.lower()
                        else:
                            iterator.higher()

                        if current_time_in_ms() > deadline:
                            raise StopIteration

                except StopIteration:
                    break

                # halt when have a result, and checked all containers at the lower indexes
                i = 0
                while i < len(current):
                    i += 1
                    integer = current[i]
                    if results[integer] is not None:
                        # remove end items; we already have a better match
                        while len(current) > i:
                            current.pop()

                        break

                    # remove item
                    if checked[integer]:
                        current.pop(integer)
                        i -= 1

            for i in range(len(results)):
                if results[i] is not None:
                    return results[i]

        return None

    def filter_containers(self, boxes):
        """Return a list of containers which can potentially hold the boxes.

        :param boxes: list of boxes,
        :return list of containers."""

        volume = 0
        for box in boxes:
            volume += box.get_box().get_volume() * box.get_count()

        containers_list = []
        for container in self.containers:
            if container.get_volume() < volume or not self.can_hold(container, boxes):
                # discard this container
                continue

            containers_list.append(container)

        return containers_list

    def _adapter(self, boxes):
        raise NotImplementedError('Adapter method is needed to be implemented.')

    def can_hold(self, container_box: Dimension, boxes: List[BoxItem]):
        for box in boxes:
            if self.rotate_3d:
                if not container_box.can_hold_3d(box.get_box()):
                    return False
            else:
                if not container_box.can_hold_2d(box.get_box()):
                    return False

        return True

    @staticmethod
    def get_placements(size: int):
        # each box will at most have a single placement with a space (and its remainder).
        placements = []

        for _ in range(size):
            a = Space()
            b = Space()
            a.set_remainder(b)
            b.set_remainder(a)

            placements.append(Placement(a))

        return placements

