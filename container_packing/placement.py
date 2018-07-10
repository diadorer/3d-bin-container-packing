from .space import Space
from .box import Box


class Placement:
    """Placement as in box in a space.

    The box does not necessarily fill the whole space."""

    def __init__(self, space: Space, box: Box=None):
        self.space = space
        self.box = box

    def get_space(self):
        return self.space

    def set_space(self, space: Space):
        self.space = space

    def get_box(self):
        return self.box

    def set_box(self, box: Box):
        self.box = box

    def __str__(self):
        return f'Placement [{self.space.get_x()}x{self.space.get_y()}x{self.space.get_z()},' \
               f'width={self.box.get_width()}, depth={self.box.get_depth()}, ' \
               f'height={self.box.get_height()}]'

    def __repr__(self):
        return self.__str__()

    def get_center_x(self):
        return self.space.get_x() + self.box.get_width() // 2

    def get_center_y(self):
        return self.space.get_y() + self.box.get_depth() // 2

    def intercepts(self, placement):
        return self.intercepts_x(placement) and self.intercepts_y(placement)

    def intercepts_y(self, placement):
        start_y = self.space.get_y()
        end_y = start_y + self.box.get_depth() - 1

        if start_y <= placement.get_space().get_y() <= end_y:
            return True

        if start_y <= placement.get_space().get_y() + placement.get_box().get_depth() - 1 \
                <= end_y:
            return True

        return False

    def intercepts_x(self, placement):
        start_x = self.space.get_x()
        end_x = start_x + self.box.get_width() - 1

        if start_x <= placement.get_space().get_x() <= end_x:
            return True

        if start_x <= placement.get_space().get_x() + placement.get_box().get_width() - 1 \
                <= end_x:
            return True

        return False
