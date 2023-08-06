"""
types.py - Type checkers useful for sanity checking arguments
"""

class TypeTuple:
    def __init__(self, len=None, item_type=None):
        self.len = len
        self.item_type = item_type
    def check(self, vs):
        if not isinstance(vs, tuple):
            raise TypeError("must be a tuple")
        if self.len is not None and len(vs) != self.len:
            raise TypeError(f"expected a {self.len}-tuple")
        if self.item_type is not None:
            for i, v in enumerate(vs):
                try:
                    self.item_type.check(v)
                except TypeError as e:
                    raise TypeError(f"on index {i}: {str(e)}")

class TypeInt:
    def __init__(self, min=None, max=None):
        self.min = min
        self.max = max
    def check(self, v):
        if not isinstance(v, int):
            raise TypeError("must be an integer")
        if self.min is not None and v < self.min:
            raise TypeError(f"must be at least {self.min}")
        if self.max is not None and v > self.max:
            raise TypeError(f"must be at most {self.max}")

class TypeFloat:
    def __init__(self, min=None, max=None):
        self.min = min
        self.max = max
    def check(self, v):
        if not isinstance(v, float):
            raise TypeError("must be a float")
        if self.min is not None and v < self.min:
            raise TypeError(f"must be at least {self.min}")
        if self.max is not None and v > self.max:
            raise TypeError(f"must be at most {self.max}")

class TypeBool:
    def __init__(self):
        pass
    def check(self, v):
        if not isinstance(v, bool):
            raise TypeError("must be a bool")
