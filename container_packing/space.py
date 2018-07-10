from typing import Union

from .dimension import Dimension


class Space(Dimension):

    def __init__(self, parent_or_name_or_w=None, name_or_w: Union[str, int]=None, w: int=None, d: int=None, h: int=None,
                 x: int=None, y: int=None, z: int=None):
        if parent_or_name_or_w is None and name_or_w is None and w is None and d is None and h is None and x is None\
                and y is None and z is None:
            super().__init__()
            return

        if isinstance(parent_or_name_or_w, str):
            w, d, h, x, y, z = name_or_w, w, d, h, x, y
            name = parent_or_name_or_w
            parent = None
        elif isinstance(parent_or_name_or_w, int):
            w, d, h, x, y, z = parent_or_name_or_w, name_or_w, w, d, h, x
            name = None
            parent = None
        else:
            if isinstance(parent_or_name_or_w, Dimension):
                parent = parent_or_name_or_w
            else:
                parent = None

            if isinstance(name_or_w, str):
                name = name_or_w
            else:
                name = None
                w, d, h, x, y, z = name_or_w, w, d, h, x, y

        super().__init__(name, w, d, h)

        self.parent = parent
        self.x, self.y, self.z = x, y, z

        self.remainder = None

    def get_x(self):
        return self.x

    def set_x(self, x):
        self.x = x

    def get_y(self):
        return self.y

    def set_y(self, y):
        self.y = y

    def get_z(self):
        return self.z

    def set_z(self, z):
        self.z = z

    def get_parent(self):
        return self.parent

    def set_parent(self, parent):
        self.parent = parent

    def set_remainder(self, dual):
        self.remainder = dual

    def get_remainder(self):
        return self.remainder

    def __str__(self):
        return f'Space [name={self.name}, {self.x}x{self.y}x{self.z}, width={self.width}, ' \
               f'depth={self.depth}, height={self.height}]'

    def __repr__(self):
        return self.__str__()

    def hash_code(self):
        prime = 31
        result = super().hash_code()
        result = prime * result + (self.parent.hash_code() if self.parent is not None else 0)
        result = prime * result + (self.remainder.hash_code() if self.remainder is not None else 0)
        result = prime * result + self.x
        result = prime * result + self.y
        result = prime * result + self.z
        return result

    def __eq__(self, other):
        # print(f'Space: self={self} ({type(self)}) and \n'
        #       f'other={other} ({type(other)}) and \n'
        #       f'remainder={self.remainder} ({type(self.remainder)})')
        if other is None:
            return False

        # print(
        #     f'super(Dimension, self): {super(Dimension, self)}\n'
        #     f'super(Dimension, other): {super(Dimension, other)}\n'
        # )
        #
        # print(
        #     f'x {self.x == other.x}\n'
        #     f'y {self.y == other.y}\n'
        #     f'z {self.z == other.z}\n'
        #     f'super(Dimension) {super(Dimension, self).__eq__(other)}\n'
        #     f'self.parent {self.parent == other.parent}\n'
        #     f'remainder: \n'
        #     f'\t x: {self.remainder.x == other.remainder.x}\n'
        #     f'\t y: {self.remainder.y == other.remainder.y}\n'
        #     f'\t z: {self.remainder.z == other.remainder.z}\n'
        #     f'\t super(Dimension): {super(Dimension, self.remainder).__eq__(other.remainder)}'
        # )

        return (
            other is not None
            and self.x == other.x
            and self.y == other.y
            and self.z == other.z
            and super(Dimension, self).__eq__(other)
            and self.parent == other.parent
            and (
                self.remainder.x == other.remainder.x
                and self.remainder.y == other.remainder.y
                and self.remainder.z == other.remainder.z
                and super(Dimension, self.remainder).__eq__(other.remainder)
            )
        )
        # if self.hash_code() == obj.hash_code():
        #     return True
        # if super().hash_code() != obj.hash_code():
        #     return False
        # if self.__class__ != obj.__class__:
        #     return False
        #
        # other = Space(obj)
        # if self.parent is None:
        #     if other.parent is not None:
        #         return False
        # elif self.parent != other.parent:
        #     return False
        #
        # if self.remainder is None:
        #     if other is not None:
        #         return False
        # elif self.remainder != other.remainder:
        #     return False
        #
        # if self.x != other.x or self.y != other.y or self.z != other.z:
        #     return False
        #
        # return True

    def copy_from(self, space_or_w, d: int=None, h: int=None,
                  x: int=None, y: int=None, z: int=None):
        if isinstance(space_or_w, Space):
            space = space_or_w
            self.parent = space.parent
            w, d, h, x, y, z = space.width, space.depth, space.height, \
                               space.x, space.y, space.z
        else:
            w = space_or_w

        self.x, self.y, self.z = x, y, z

        self.width, self.depth, self.height = w, d, h
