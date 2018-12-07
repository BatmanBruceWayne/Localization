import math
import random
import common as cm


class Point:
    """
    An immutable 2D point.
    """
    def __init__(self, x=0., y=0., r=20., order=-1):
        self.x = x
        self.y = y
        self.r = r
        self.order = order

    def distance(self, A):
        return math.sqrt((A.x-self.x)**2 + (A.y-self.y)**2)

    def non_anchors_neighborhood(self, non_anchors):
        self.non_anchors_neibor = [s for s in non_anchors if self.distance(A=s) < self.r]


class Anchor(Point):
    def __init__(self, x=0., y=0., r=20., order=-1):
        super().__init__(x, y, r, order)

class NonAnchor(Point):
    def __init__(self, x=0., y=0., r=20., order=-1):
        super().__init__(x, y, r, order)

class Gen:
    def __init__(self, x_1=-1., y_1=-1., x_2=-1., y_2=-1., type='segment'):
        self.x_1 = x_1
        self.y_1 = y_1
        self.x_2 = x_2
        self.y_2 = y_2
        self.type = type

    def generate_chromosome(self):
        if self.type == 'segment':
            x_max = max(self.x_1, self.x_2)
            x_min = min(self.x_1, self.x_2)
            x = random.uniform(x_min, x_max)
            a, b = cm.defineLine(self.x_1, self.y_1, self.x_2, self.y_2)
            y = a*x + b
            return x,y
        elif self.type == 'circle':
            y = random.uniform(self.y_1-self.x_2, self.y_1+self.x_2)
            X = cm.line_circle_equation(0., y, self.x_1, self.y_1, self.x_2)
            x = X[0]
            return x, y
        else:
            return random.uniform(0., 1500.), random.uniform(0., 1000.)


class Individual:
    def __init__(self, chromosome):
        self.chromosome = chromosome