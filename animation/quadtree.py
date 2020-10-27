class Point:
    def __init__(self, x, y, data):
        self.x = x
        self.y = y
        self.data = data


class Rectangle:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.left = self.x - self.w
        self.right = self.x + self.w
        self.top = self.y - self.h
        self.bottom = self.y + self.h

    def contains(self, point):
        return self.left < point.x < self.right and self.top < point.y < self.bottom

    def intersects(self, other):
        pass


class Quadtree:
    CAPACITY = 4

    def __init__(self):
        self.points = []
        self.nw = None
        self.ne = None
        self.sw = None
        self.se = None
