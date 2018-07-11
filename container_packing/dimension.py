from typing import Union


class ClassOrInstanceDescriptor(object):

    def __get__(self, obj, objtype):
        if obj is None:
            return self.class_method.__get__(objtype)
        else:
            return self.instance.__get__(obj)

    def __init__(self, class_method):
        self.class_method = class_method

    def instance(self, instance_method):
        self.instance = instance_method
        return self


class Dimension:

    def __init__(self, name_or_w: Union[str, int]=None, w: int=None, d: int=None, h: int=None):
        if isinstance(name_or_w, int) and isinstance(w, int) and isinstance(d, int):
            w, d, h = name_or_w, w, d
            name = None
        else:
            name = name_or_w

        self.name = name

        self.width = w
        self.depth = d
        self.height = h

        if d is None or w is None or h is None:
            self.volume = 0
        else:
            self.volume = d * w * h

    @staticmethod
    def new_instance(width: int, depth: int, height: int):
        return Dimension(width, depth, height)

    @classmethod
    def decode(cls, size: str):
        dimensions = size.split('x')

        return cls(int(dimensions[0]), int(dimensions[1]), int(dimensions[2]))

    @ClassOrInstanceDescriptor
    def encode(cls, width_or_dto, depth: int=None, height: int=None):
        if isinstance(width_or_dto, cls):
            dto = width_or_dto
            return cls.encode(dto.get_width(), dto.get_depth(), dto.get_height())
        else:
            width = width_or_dto
            return f'{width}x{depth}x{height}'

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    def get_depth(self):
        return self.depth

    def can_hold_3d(self, w_or_dimension, d: int=None, h: int=None):
        """Check whether a dimension fits within the current dimensions, rotated in 3D.

        :param w_or_dimension: the space to fit
        :return True if any rotation of the argument can be placed inside this."""

        if isinstance(w_or_dimension, Dimension):
            dimension = w_or_dimension
            return self.can_hold_3d(dimension.get_width(), dimension.get_depth(),
                                    dimension.get_height())
        else:
            w = w_or_dimension

            if w <= self.width and h <= self.height and d <= self.depth:
                return True

            if h <= self.width and d <= self.height and w <= self.depth:
                return True

            if d <= self.width and w <= self.height and h <= self.depth:
                return True

            if h <= self.width and w <= self.height and d <= self.depth:
                return True

            if d <= self.width and h <= self.height and w <= self.depth:
                return True

            if w <= self.width and d <= self.height and h <= self.depth:
                return True

            return False

    def can_hold_2d(self, w_or_dimension, d: int=None, h: int=None):
        """Check whether a dimension fits within the current object, rotated in 2D."""

        if isinstance(w_or_dimension, self.__class__):
            dimension = w_or_dimension
            return self.can_hold_2d(dimension.get_width(), dimension.get_depth(),
                                    dimension.get_height())
        else:
            w = w_or_dimension

            if h > self.height:
                return False

            return (w <= self.width and d <= self.depth) or \
                   (d <= self.width and w <= self.depth)

    def get_footprint(self):
        return self.width * self.depth

    def is_square_2d(self):
        return self.width == self.depth

    def is_square_3d(self):
        return self.width == self.depth == self.height

    def fits_inside_3d(self, w_or_dimension, d: int=None, h: int=None):
        """Check whether this object fits within a dimension (without rotation).

        :param w_or_dimension: the dimensions to fit within,
        :return True if this can fit within the argument space."""

        if isinstance(w_or_dimension, self.__class__):
            dimension = w_or_dimension
            return self.fits_inside_3d(dimension.get_width(), dimension.get_depth(),
                                       dimension.get_height())
        else:
            w = w_or_dimension

            if w >= self.width and h >= self.height and d >= self.depth:
                return True

            return False

    def can_fit_inside_3d(self, dimension):
        """Check whether this object can fit within a dimension, with 3D rotation.

        :param dimension: the dimensions to fit within
        :return True if this can fit within the argument space in any rotation."""

        return dimension.can_hold_3d(self)

    def can_fit_inside_2d(self, dimension):
        """Check whether this object can fit within a dimension, with 2D rotation.

        :param dimension the dimensions to fit within,
        :return True if this can fit within the argument space in any 2D rotation."""

        return dimension.can_hold_2d(self)

    def get_volume(self):
        return self.volume

    def is_empty(self):
        return self.width <= 0 or self.depth <= 0 or self.height <= 0

    def __str__(self):
        return (f'Dimension [width={self.width}, depth={self.depth}, '
                f'height={self.height}, volume={self.volume}]')

    def __repr__(self):
        return self.__str__()

    @encode.instance
    def encode(self):
        return self.__class__.encode(self.width, self.depth, self.height)

    def get_name(self):
        return self.name

    def hash_code(self):
        prime = 31
        result = 1
        result = prime * result + self.depth
        result = prime * result + self.height
        result = prime * result + 0 if self.name is None else hash(self.name)
        result = prime * result + int(self.volume ^ (self.volume >> 32))
        result = prime * result + self.width
        return result

    counter = 0

    def __eq__(self, other):
        if other is None:
            return None

        return (
            other is not None
            and self.depth == other.depth
            and self.height == other.height
            and self.name == other.name
            and self.volume == other.volume
            and self.width == other.width
        )


Dimension.EMPTY = Dimension(0, 0, 0)
