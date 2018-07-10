from .box import Box


class BoxItem:
    """A {@linkplain Box} repeated one or more times. Typically corresponding to an
    order-line, but can also represent multiple products which share the same size."""

    def __init__(self, box: Box=None, count: int=1):
        if box is None:
            return

        self.box = box
        self.count = count

    def get_count(self):
        return self.count

    def set_count(self, count: int):
        self.count = count

    def get_box(self):
        return self.box

    def set_box(self, box: Box):
        self.box = box

    def __str__(self):
        return f'BoxItem [{self.box}, count={self.count}]'

    def __repr__(self):
        return self.__str__()
