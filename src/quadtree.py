from pygame import draw, Rect, Surface
from src.helpers import draw_rect_border


class QuadTree:
    def __init__(self, boundary: Rect, capacity: int = 4) -> None:
        self.boundary = boundary
        self.capacity = capacity
        self.divided = False
        self.points = []

    def pointCount(self):
        pointsLen = len(self.points)
        if not self.divided:
            return pointsLen
        else:
            pointsLen += self.northEast.pointCount()
            pointsLen += self.northWest.pointCount()
            pointsLen += self.southEast.pointCount()
            pointsLen += self.southWest.pointCount()
        return pointsLen

    def draw(self, surface: Surface):
        draw_rect_border(surface, self.boundary, (255, 255, 255))

        if self.divided:
            self.northEast.draw(surface)
            self.northWest.draw(surface)
            self.southEast.draw(surface)
            self.southWest.draw(surface)

    def insert(self, point):
        if not self.boundary.collidepoint(point.x, point.y):
            return False

        if len(self.points) < self.capacity:
            self.points.append(point)
            return True
        else:
            if not self.divided:
                self.subdivide()

            if self.northEast.insert(point):
                return True
            elif self.northWest.insert(point):
                return True
            elif self.southEast.insert(point):
                return True
            elif self.southWest.insert(point):
                return True

    def query(self, area: Rect):
        found = []
        if not self.boundary.colliderect(area):
            return found

        for p in self.points:
            if area.collidepoint(p.x, p.y):
                found.append(p)

        if self.divided:
            found.extend(self.northWest.query(area))
            found.extend(self.northEast.query(area))
            found.extend(self.southWest.query(area))
            found.extend(self.southEast.query(area))

        return found

    def subdivide(self):
        x = self.boundary.x
        y = self.boundary.y
        w = self.boundary.width
        h = self.boundary.height

        #  NW | NE
        # ----+----
        #  SW | SE

        nw = Rect(x, y, w / 2, h / 2)
        ne = Rect(x + w / 2, y, w / 2, h / 2)
        sw = Rect(x, y + h / 2, w / 2, h / 2)
        se = Rect(x + w / 2, y + h / 2, w / 2, h / 2)

        self.northWest = QuadTree(boundary=nw, capacity=self.capacity)
        self.northEast = QuadTree(boundary=ne, capacity=self.capacity)
        self.southWest = QuadTree(boundary=sw, capacity=self.capacity)
        self.southEast = QuadTree(boundary=se, capacity=self.capacity)

        self.divided = True
