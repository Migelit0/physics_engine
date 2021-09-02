class Vector:
    def __init__(self, coords: tuple):
        self.coords = coords

    def get_x(self):
        return self.coords[0]

    def get_y(self):
        return self.coords[1]

    def __add__(self, other):   # +
        return Vector((self.coords[0] + other.coords[0], self.coords[1] + other.coords[1]))

    def __iadd__(self, other):  # +=
        return Vector((self.coords[0] + other.coords[0], self.coords[1] + other.coords[1]))

    def __truediv__(self, other: float):    # /num
        x, y = self.coords
        return Vector((x / other, y / other))

    def __mul__(self, other: float):        # *num
        x, y = self.coords
        return Vector((x * other, y * other))

