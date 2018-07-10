"""
Fit boxes into container, i.e. perform bin packing to a single container.

Thread-safe implementation.
"""

from typing import List

from .packager import Packager, current_time_in_ms
from .dimension import Dimension
from .container import Container
from .box_item import BoxItem
from .box import Box
from .space import Space
from .placement import Placement


class LargestAreaFitFirstPackager(Packager):

    def __init__(self, containers: List[Dimension], rotate_3d: bool=True,
                 footprint_first: bool=True, binary_search: bool=True):
        """Constructor

        :param containers: list of containers
        :param rotate_3d: whether boxes can be rotated in all three directions
            (two directions otherwise)
        :param footprint_first: start with box which has the largest footprint.
            If not, the highest box is first.
        :param binary_search: if true, the packager attempts to find the best box given
            a binary search. Upon finding a container that can hold the boxes, given time,
            it also tries to find a better match."""

        super().__init__(containers, rotate_3d, binary_search)

        self.footprint_first: bool = footprint_first

    def pack_adapter(self, items: List[BoxItem], dimension: Dimension=None, deadline: int=None):
        """Return a container which holds all the boxes in the argument

        :param items: list of boxes to fit in a container
        :param dimension: the container to fit within
        :param deadline: the system time in millis at which the search should be aborted
        :return: null if no match, or deadline reached."""

        container_products = []

        for item in items:
            box = item.get_box()
            container_products.append(box)
            for i in range(1, item.get_count()):
                container_products.append(box.clone())

        holder = Container(dimension)

        free_space = dimension

        while container_products:
            if current_time_in_ms() > deadline:
                # fit2d below might have returned due to deadline
                break

            # choose the box with the largest surface area, that fits
            # if the same then the one with minimum height

            # use a special case for boxes with full height
            current_box, current_index = None, -1

            full_height = False
            for i in range(len(container_products)):
                box = container_products[i]

                if self.rotate_3d:
                    fits = box.rotate_largest_footprint_3d(free_space)
                else:
                    fits = box.fit_rotate_2d(free_space)
                if fits:
                    if current_box is None:
                        current_box, current_index = box, i

                        full_height = box.get_height() == free_space.get_height()
                    else:
                        if full_height:
                            if box.get_height() == free_space.get_height():
                                if current_box.get_footprint() < box.get_footprint():
                                    current_box, current_index = box, i
                        else:
                            if box.get_height() == free_space.get_height():
                                full_height = True

                                current_box, current_index = box, i
                            elif self.footprint_first:
                                if current_box.get_footprint() < box.get_footprint():
                                    current_box, current_index = box, i
                                elif current_box.get_footprint() == box.get_footprint() \
                                        and current_box.get_height() < box.get_height():
                                    current_box, current_index = box, i
                            else:
                                if current_box.get_height() < box.get_height():
                                    current_box, current_index = box, i
                                elif current_box.get_height() == box.get_height() \
                                        and current_box.get_footprint() < box.get_footprint():
                                    current_box, current_index = box, i

                else:
                    # no fit in the current container within the remaining space
                    # try the next container

                    return None

            # current box should have the optimal orientation already
            # create a space which holds the full level
            level_space = Space(
                dimension.get_width(),
                dimension.get_depth(),
                current_box.get_height(),
                0,
                0,
                holder.get_stack_height()
            )
            holder.add_level()
            container_products.pop(current_index)

            # print('before fit free space.levels is:', holder.levels)
            self.fit_2d(container_products, holder, current_box, level_space, deadline)
            # print('after fit free space.levels is:', holder.levels)

            free_space = holder.get_free_space()

        return holder

    def remove_identical(self, container_products: List[Box], current_box: Box):
        """Remove from list, more explicit implementation than {@linkplain List#remove} with no equals.

        :param container_products: list of products,
        :param current_box: item to remove."""

        for i in range(len(container_products)):
            if container_products[i] == current_box:
                container_products.pop(i)

                return

        raise ValueError

    counter = 1

    def fit_2d(self, container_products: List[Box], holder: Container, used_space: Box,
               free_space: Space, deadline: int):
        #
        # print(f'call fit2d with params '
        #       # f'\n container_products: {container_products}\n'
        #       f'holder: {holder} \n used_space: {used_space} \n '
        #       f'free_space: {free_space}')

        # self.counter += 1
        # if self.counter < 20:
            # print('levels is:', holder.levels)

        if self.rotate_3d:
            # minimize footprint
            used_space.fit_rotate_3d_smallest_footprint(free_space)

        # add used space box now, but possibly rotate later - this depends on the actual
        # remaining free space selected further down
        # there is up to possible 4 free spaces, 2 in which the used space box is rotated
        holder.add(Placement(free_space, used_space))

        if len(container_products) == 0:
            # no additional boxes
            # just make sure the used space fits in the free space
            used_space.fit_rotate_2d(free_space)

            return

        if current_time_in_ms() > deadline:
            return

        spaces = self.get_free_spaces(free_space, used_space)

        next_placement = self.best_volume_placement(container_products, spaces)
        if next_placement is None:
            # no additional boxes
            # just make sure the used space fits in the free space
            used_space.fit_rotate_2d(free_space)

            return

        # check whether the selected free space requires the used space box to be rotated
        # print(f'largest area call rotate2d {next_placement.get_space()}')
        # print(f'largest area call rotate2d [2] {spaces[2]}')
        # print(f'largest area call rotate2d [3] {spaces[3]}')
        # print(f'largest area call rotate2d == {next_placement.get_space() == spaces[3]}')
        if next_placement.get_space() == spaces[2] or next_placement.get_space() == spaces[3]:
            # the desired space implies that we rotate the used space box
            used_space.rotate_2d()

        # holder.validate_current_level()  # uncomment for debugging

        self.remove_identical(container_products, next_placement.get_box())

        # attempt to fit in the remaining (usually smaller) space first

        # stack in the 'sibling' space – the space left over between the used box
        # and the selected free space
        remainder = next_placement.get_space().get_remainder()
        if not remainder.is_empty():
            box = self.best_volume(container_products, remainder)
            if box is not None:
                self.remove_identical(container_products, box)

                self.fit_2d(container_products, holder, box, remainder, deadline)

        # fit the next box in the selected free space
        self.fit_2d(container_products, holder, next_placement.get_box(),
                    next_placement.get_space(), deadline)

        # TODO: use free spaces between box and level, if any

    def get_free_spaces(self, free_space: Space, used: Box):
        # Two free spaces, on each rotation of the used space.
        # Height is always the same, used box is assumed within free space height.
        # First:
        # ........................  ........................  .............
        # .                      .  .                      .  .           .
        # .                      .  .                      .  .           .
        # .          A           .  .          A           .  .           .
        # .                      .  .                      .  .           .
        # .                B     .  .                      .  .    B      .
        # ............           .  ........................  .           .
        # .          .           .                            .           .
        # .          .           .                            .           .
        # ........................                            .............
        #
        # Second:
        #
        # ........................   ........................  ..................
        # .                      .   .                      .  .                .
        # .          C           .   .         C            .  .                .
        # .                      .   .                      .  .                .
        # .......                .   ........................  .                .
        # .     .       D        .                             .        D       .
        # .     .                .                             .                .
        # .     .                .                             .                .
        # .     .                .                             .                .
        # ........................                             ..................
        #
        # So there is always a 'big' and a 'small' leftover area (the small is not shown).

        free_spaces: List[Space] = [None] * 4
        if free_space.get_width() >= used.get_width() \
                and free_space.get_depth() >= used.get_depth():
            # if B is empty, then it is sufficient to work with A and the other way around

            # B
            if free_space.get_width() > used.get_width():
                right = Space(
                    free_space.get_width() - used.get_width(),
                    free_space.get_depth(),
                    free_space.get_height(),
                    free_space.get_x() + used.get_width(),
                    free_space.get_y(),
                    free_space.get_z()
                )
                right_remainder = Space(
                    used.get_width(),
                    free_space.get_depth() - used.get_depth(),
                    free_space.get_height(),
                    free_space.get_x(),
                    free_space.get_y() + used.get_depth(),
                    free_space.get_z()
                )
                right.set_remainder(right_remainder)
                right_remainder.set_remainder(right)
                free_spaces[0] = right

            # A
            if free_space.get_depth() > used.get_depth():
                top = Space(
                    free_space.get_width(),
                    free_space.get_depth() - used.get_depth(),
                    free_space.get_height(),
                    free_space.get_x(),
                    free_space.get_y() + used.get_depth(),
                    free_space.get_height()
                )
                top_remainder = Space(
                    free_space.get_width() - used.get_width(),
                    used.get_depth(),
                    free_space.get_height(),
                    free_space.get_x() + used.get_width(),
                    free_space.get_y(),
                    free_space.get_z()
                )
                top.set_remainder(top_remainder)
                top_remainder.set_remainder(top)
                free_spaces[1] = top

        if free_space.get_width() >= used.get_depth() and free_space.get_depth() >= used.get_width():
            # if D is empty, then it is sufficient to work with C and the other way around

            # D
            if free_space.get_width() > used.get_depth():
                right = Space(
                    free_space.get_width() - used.get_depth(),
                    free_space.get_depth(),
                    free_space.get_height(),
                    free_space.get_x() + used.get_depth(),
                    free_space.get_y(),
                    free_space.get_height()
                )
                right_remainder = Space(
                    used.get_depth(),
                    free_space.get_depth() - used.get_width(),
                    free_space.get_height(),
                    free_space.get_x(),
                    free_space.get_y() + used.get_width(),
                    free_space.get_z()
                )
                right.set_remainder(right_remainder)
                right_remainder.set_remainder(right)
                free_spaces[2] = right

            # C
            if free_space.get_depth() > used.get_width():
                top = Space(
                    free_space.get_width(),
                    free_space.get_depth() - used.get_width(),
                    free_space.get_height(),
                    free_space.get_x(),
                    free_space.get_y() + used.get_width(),
                    free_space.get_height()
                )
                top_remainder = Space(
                    free_space.get_width() - used.get_depth(),
                    used.get_width(),
                    free_space.get_height(),
                    free_space.get_x() + used.get_depth(),
                    free_space.get_y(),
                    free_space.get_z()
                )
                top.set_remainder(top_remainder)
                top_remainder.set_remainder(top)
                free_spaces[3] = top

        return free_spaces

    def best_volume(self, container_products: List[Box], space: Space):
        best_box = None
        for box in container_products:

            if self.rotate_3d:
                if box.can_fit_inside_3d(space):
                    if best_box is None:
                        best_box = box

                        best_box.fit_rotate_3d_smallest_footprint(space)
                    elif best_box.get_volume() < box.get_volume():
                        best_box = box

                        best_box.fit_rotate_3d_smallest_footprint(space)
                    elif best_box.get_volume() == box.get_volume():
                        # determine lowest fit
                        box.fit_rotate_3d_smallest_footprint(space)

                        if box.get_footprint() < best_box.get_footprint():
                            best_box = box

            else:
                if box.can_fit_inside_2d(space):
                    if best_box is None:
                        best_box = box
                    elif best_box.get_volume() < box.get_volume():
                        best_box = box
                    elif best_box.get_volume() == box.get_volume():
                        # TODO: use the aspect ratio in some meaningful way
                        pass

        return best_box

    def best_volume_placement(self, container_products: List[Box], spaces: List[Space]):
        best_box = None
        best_space = None
        for space in spaces:
            if space is None:
                continue

            for box in container_products:
                if self.rotate_3d:
                    if box.can_fit_inside_3d(space):
                        if best_box is None:
                            best_box, best_space = box, space

                            best_box.fit_rotate_3d_smallest_footprint(best_space)
                        elif best_box.get_volume() < box.get_volume():
                            best_box, best_space = box, space

                            best_box.fit_rotate_3d_smallest_footprint(best_space)
                        elif best_box.get_volume() == box.get_volume():
                            # determine lowest fit
                            box.fit_rotate_3d_smallest_footprint(space)

                            if box.get_footprint() < best_box.get_footprint():
                                best_box, best_space = box, space

                            # TODO: if all else is equal, which free space is preferred?
                else:
                    if box.can_fit_inside_2d(space):
                        if best_box is None:
                            best_box, best_space = box, space
                        elif best_box.get_volume() < box.get_volume():
                            best_box, best_space = box, space
                        # TODO: use the aspect ratio in some meaningful way

                        # TODO: if all else is equal, which free space is preferred?

        if best_box is not None:
            return Placement(best_space, best_box)

        return None

    def _adapter(self, boxes):
        return self
