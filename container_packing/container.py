from typing import Union

from .dimension import Dimension
from .box import Box
from .level import Level, ArrayList
from .placement import Placement


class LevelArrayList(ArrayList):
    item_class = Level


a = {'c': 0}

class Container(Box):

    def __init__(self, name_or_w_or_dimension: Union[Dimension, int, str],
                 w: int=None, d: int=None, h: int=None):

        self.stack_height = 0
        self.levels = LevelArrayList()

        if isinstance(name_or_w_or_dimension, Dimension):
            dimension = name_or_w_or_dimension
            super().__init__(dimension.get_name(), dimension.get_width(),
                             dimension.get_depth(), dimension.get_height())
        elif isinstance(name_or_w_or_dimension, str):
            name = name_or_w_or_dimension
            super().__init__(name, w, d, h)
        else:
            w, d, h = name_or_w_or_dimension, w, d
            super().__init__(w, d, h)

    def add(self, element_or_index_or_placement: Union[Level, int, Placement],
            none_or_element: Level=None):
        if isinstance(element_or_index_or_placement, Level):
            if len(self.levels) != 0:
                self.stack_height += self.current_level_stack_height()

            element = element_or_index_or_placement
            self.levels.add(element)
        elif isinstance(element_or_index_or_placement, Placement):
            placement = element_or_index_or_placement

            self.levels[-1].add(placement)
        else:
            if len(self.levels) != 0:
                self.stack_height += self.current_level_stack_height()

            index, element = element_or_index_or_placement, none_or_element
            self.levels.add(index, element)

    def add_level(self):
        self.add(Level())

    def get_stack_height(self):
        return self.stack_height + self.current_level_stack_height()

    def current_level_stack_height(self):
        if len(self.levels) == 0:
            return 0

        return self.levels[-1].get_height()

    def get_free_space(self):
        space_height = self.height - self.get_stack_height()
        if space_height < 0:
            raise ValueError(f"Remaining free space is negative at {space_height}")

        return Dimension(self.width, self.depth, space_height)

    def get_levels(self):
        return self.levels

    def get(self, level: int, placement: int):
        return self.levels[level][placement]

    def validate_current_level(self):
        self.levels[-1].validate()

    def hash_code(self):
        prime = 31
        result = super().hash_code()
        result = prime * result + self.levels.hash_code() if self.levels else 0
        result = prime * result + self.stack_height
        return result

    def __eq__(self, obj):
        return (
            self.levels == obj.levels
            and self.stack_height == obj.stack_height
        )
        # if self.hash_code() == obj.hash_code():
        #     return True
        # if super().hash_code() != obj.hash_code():
        #     return False
        # if self.__class__ != obj.__class__:
        #     return False

        # other = Container(obj)
        # if self.levels is None:
        #     if other.levels is not None:
        #         return False
        # elif self.levels != other.levels:
        #     return False
        #
        # if self.stack_height != other.stack_height:
        #     return False
        #
        # return True

    def clear(self):
        self.levels.clear()
        self.stack_height = 0

    def get_box_count(self):
        count = 0
        for level in self.levels:
            count += level.size()

        return count



