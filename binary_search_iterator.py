class BinarySearchIterator:

    def __init__(self, low: int=None, high: int=None):
        self.low = low
        self.high = high
        self.mid = None

    def next(self):
        self.mid = self.low + (self.high - self.low) // 2
        return self.mid

    def lower(self):
        self.high = self.mid - 1

    def higher(self):
        self.high = self.mid + 1

    def has_next(self):
        return self.low <= self.high

    def reset(self, high: int, low: int):
        self.high = high
        self.low = low

    def get_high(self):
        return self.high

    def get_low(self):
        return self.low

    def get_mid(self):
        return self.mid

