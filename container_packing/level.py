from .placement import Placement


class ArrayList(list):
    """Imitation of java's ArrayList."""

    item_class = None

    def add(self, arg_a, arg_b=None):
        if arg_b is None:
            item = arg_a
            self.append(item)
        else:
            index, item = arg_a, arg_b
            self.insert(index, item)

    def remove(self, item_or_index):
        if isinstance(item_or_index, self.item_class):
            item = item_or_index
        else:
            index = item_or_index
            item = self[index]

        self.remove(item)

    def contains(self, item):
        return item in self

    def size(self):
        return len(self)

    def hash_code(self):
        return hash(self)


class Level(ArrayList):

    item_class = Placement

    def get_height(self):
        height = 0

        for placement in self:
            box = placement.get_box()
            if box.get_height() > height:
                height = box.get_height()

        return height

    def validate(self):
        """Check whether placement is valid, i.e. no overlaps."""

        for i in range(len(self)):
            for j in range(len(self)):
                if j == i:
                    if not self[i].intercepts(self[j]):
                        raise ValueError
                else:
                    if self[i].intercepts(self[j]):
                        raise ValueError(f'{i} ({self[i]}) vs {j} ({self[j]})')
