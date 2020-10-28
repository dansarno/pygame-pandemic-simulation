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
        return not (other.left > self.right or
                    other.right < self.left or
                    other.top > self.bottom or
                    other.bottom < self.top)


class Quadtree:
    CAPACITY = 4

    def __init__(self, boundary):
        self.boundary = boundary
        self.points = []
        self.nw = None
        self.ne = None
        self.sw = None
        self.se = None

    def subdivide(self):
        x = self.boundary.x
        y = self.boundary.y
        half_w = self.boundary.w / 2
        half_h = self.boundary.h / 2
        self.nw = Quadtree(Rectangle(x - half_w, y - half_h, half_w, half_h))
        self.ne = Quadtree(Rectangle(x + half_w, y - half_h, half_w, half_h))
        self.sw = Quadtree(Rectangle(x - half_w, y + half_h, half_w, half_h))
        self.se = Quadtree(Rectangle(x - half_w, y + half_h, half_w, half_h))

    def insert(self, point):
        if not self.boundary.contains(point):
            return False

        if len(self.points) < Quadtree.CAPACITY and not self.nw:
            self.points.append(point)
            return True

        if not self.nw:
            self.subdivide()

        if self.nw.insert(point):
            return True
        if self.ne.insert(point):
            return True
        if self.sw.insert(point):
            return True
        if self.se.insert(point):
            return True

        return False

    def query(self, domain):
        points_in_domain = []

        if not self.boundary.intersects(domain):
            return points_in_domain

        for point in self.points:
            if self.boundary.contains(point):
                points_in_domain.append(point)

        if not self.nw:
            return points_in_domain

        points_in_domain += self.nw.query(domain)
        points_in_domain += self.ne.query(domain)
        points_in_domain += self.sw.query(domain)
        points_in_domain += self.se.query(domain)

        return points_in_domain
