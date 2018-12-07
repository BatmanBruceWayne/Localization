import math
import random

import os
from prompt_toolkit import prompt
from prompt_toolkit.history import InMemoryHistory

from wusn.commons import WusnOutput, WusnInput, Gen, NonAnchor
import common as cm

class ToA:
    def __init__(self, error=1., max_width=1500., max_height=1000.):
        self.error = error
        self.max_width = max_width
        self.max_height = max_height
        self.matrix = []
        self.gens = []

    def ToA_distance(self, A, B):
        d = math.sqrt((A.x-B.x)**2 + (A.y-B.y)**2)
        return (d + random.uniform(-self.error, self.error))

    def distance_matrix(self, anchors, non_anchors):
        m = len(anchors)
        n = len(non_anchors)
        for i in range(m+n):
            row = []
            for j in range(n+m):
                row.append(-1.)
            self.matrix.append(row)
        for i in range(n):
            s = non_anchors[i]
            for j in range(i+1, n):
                p = non_anchors[j]
                if s.distance(p) < s.r or p.distance(s) < p.r:
                    self.matrix[m+i][m+j] = self.ToA_distance(s, p)
                    self.matrix[m+j][m+i] = self.matrix[m+i][m+j]
            for j in range(m):
                p = anchors[j]
                if s.distance(p) < s.r or p.distance(s) < p.r:
                    self.matrix[m+i][j] = self.ToA_distance(s, p)
                    self.matrix[j][m+i] = self.matrix[m+i][j]

    def uniform_point(self, gen):
        if gen.type == 'segment':
            x_max = max(gen.x_1, gen.x_2)
            x_min = min(gen.x_1, gen.x_2)
            x = random.uniform(x_min, x_max)
            a, b = cm.defineLine(gen.x_1, gen.y_1, gen.x_2, gen.y_2)
            y = a * x + b
            return x, y
        elif gen.type == 'circle':
            y = random.uniform(gen.y_1-gen.x_2, gen.y_1+gen.x_2)
            X = cm.line_circle_equation(0., y, gen.x_1, gen.y_1, gen.x_2)
            x = X[0]
            return x, y
        else:
            return random.uniform(0., self.max_width), random.uniform(0., self.max_height)

    def simulated_location(self, target, be):
        if(len(be)==3):
            D = [self.matrix[be[0].order][target.order], self.matrix[be[1].order][target.order], self.matrix[be[2].order][target.order]]
            for index in range(3):
                pre = index
                next = (index+1)%3
                tmp = (index+2)%3
                A, B = cm.find_radical_axis(be[pre].x, be[pre].y, D[pre], be[next].x, be[next].y, D[next])
                quadratic = cm.line_circle_equation(A, B, be[pre].x, be[pre].y, D[pre])
                if quadratic != "No solution!":
                    x_0, x_1 = quadratic[0], quadratic[1]
                    y_0 = A*x_0 + B
                    y_1 = A*x_1 + B
                    x_3, y_3 = x_0, y_0
                    if cm.Euclide_distance(x_0, y_0, be[tmp].x, be[tmp].y) > cm.Euclide_distance(x_1, y_1, be[tmp].x, be[tmp].y):
                        x_3, y_3 = x_1, y_1
                    x_near, y_near = cm.find_near_point(x_3, y_3, be[tmp].x, be[tmp].y, D[tmp])
                    return Gen(x_3, y_3, x_near, y_near, 'segment')
            M, N = cm.defineLine(be[pre].x, be[pre].y, be[next].x, be[next].y)
            x_inter, y_inter = cm.find_intersection_two_lines(A, B, M, N)
            near_x, near_y = cm.find_near_point(x_inter, y_inter, be[tmp].x, be[tmp].y, D[tmp])

            return Gen(x_inter, y_inter, near_x, near_y, 'segment')
        elif len(be) == 2:
            D = [self.matrix[be[0].order][target.order], self.matrix[be[1].order][target.order]]
            a, b = cm.find_radical_axis(be[0].x, be[0].y, D[0], be[1].x, be[1].y, D[1])
            quadratic = cm.line_circle_equation(a, b, be[0].x, be[0].y, D[0])
            if quadratic != "No solution!":
                x_0 = quadratic[0]
                x_1 = quadratic[1]
                y_0 = a*x_0 + b
                y_1 = a*x_1 + b
                return Gen(x_0, y_0, x_1, y_1, 'segment')
            near_x_0, near_y_0 = cm.find_near_point(be[0].x, be[0].y, be[1].x, be[1].y, D[1])
            near_x_1, near_y_1 = cm.find_near_point(be[1].x, be[1].y, be[0].x, be[0].y, D[0])
            return Gen(near_x_0, near_y_0, near_x_1, near_y_1, 'segment')
        elif len(be) == 1:
            D = self.matrix[be[0].order][target.order]
            return Gen(x_1=be[0].x, y_1=be[0].y, x_2=D, type='circle')
        else:
            return Gen(type='plane')

    def run_ToA(self, anchors, non_anchors):
        self.gens = [0]*len(non_anchors)
        C = []
        self.distance_matrix(anchors, non_anchors)

        while len(non_anchors) != 0:
            old_length = len(non_anchors)

            for s in non_anchors:
                beacons = []
                for k in anchors:
                    if self.matrix[k.order][s.order] != -1.:
                        beacons.append(k)
                    if len(beacons) == 3:
                        break
                if len(beacons) < 3 and len(C) > 0:
                    for h in C:
                        if self.matrix[h.order][s.order] != -1.:
                            beacons.append(h)
                        if len(beacons) == 3:
                            break
                if len(beacons) == 3:
                    gen = self.simulated_location(s, beacons)
                    self.gens[s.order-len(anchors)] = gen
                    simulated_s = self.uniform_point(gen)
                    C.append(NonAnchor(x=simulated_s[0], y=simulated_s[1], r=50., order=s.order))
                    non_anchors.remove(s)
            if len(non_anchors) == old_length:
                break
        while len(non_anchors) != 0:
            old_length = len(non_anchors)
            for s in non_anchors:
                beacons = []
                for k in anchors:
                    if self.matrix[k.order][s.order] != -1.:
                        beacons.append(k)
                    if len(beacons) == 2:
                        break
                if len(beacons) < 2 and len(C) > 0:
                    for h in C:
                        if self.matrix[h.order][s.order] != -1.:
                            beacons.append(h)
                        if len(beacons) == 2:
                            break
                if len(beacons) == 2:
                    gen = self.simulated_location(s, beacons)
                    self.gens[s.order-len(anchors)] = gen
                    simulated_s = self.uniform_point(gen)
                    C.append(NonAnchor(x=simulated_s[0], y=simulated_s[1], r=50., order=s.order))
                    non_anchors.remove(s)
            if len(non_anchors) == old_length:
                break
        while len(non_anchors) != 0:
            old_length = len(non_anchors)
            for s in non_anchors:
                beacons = []
                for k in anchors:
                    if self.matrix[k.order][s.order] != -1.:
                        beacons.append(k)
                    if len(beacons) == 1:
                        break
                if len(beacons) < 1 and len(C) > 0:
                    for h in C:
                        if self.matrix[h.order][s.order] != -1.:
                            beacons.append(h)
                        if len(beacons) == 1:
                            break
                if len(beacons) == 1:
                    gen = self.simulated_location(s, beacons)
                    self.gens[s.order-len(anchors)] = gen
                    simulated_s = self.uniform_point(gen)
                    C.append(NonAnchor(x=simulated_s[0], y=simulated_s[1], r=50., order=s.order))
                    non_anchors.remove(s)
            if len(non_anchors) == old_length:
                break
        for s in non_anchors:
            gen = self.simulated_location(s, [])
            self.gens[s.order - len(anchors)] = gen

    def to_file(self, path_1, path_2):
        with open(path_1, 'wt') as f:
            f.write('%d\n' % len(self.gens))
            for r in self.gens:
                f.write('%s %f %f %f %f\n' % (r.type, r.x_1, r.y_1, r.x_2, r.y_2))
        with open(path_2, 'wt') as f:
            for row in self.matrix:
                for column in row:
                    f.write('%f ' % (column))

    def from_file_gens(cls, path):
        with open(path, 'rt') as f:
            lines = f.readlines()
            lines = list(map(lambda l: l.strip(), lines))
            number = int(lines[0])
            gens = []
            for ln in lines[1:1+number]:
                type, x_1, y_1, x_2, y_2 = ln.split(' ')
                gens.append(Gen(float(x_1), float(y_1), float(x_2), float(y_2), 100., type))
            return gens

    def from_file_matrix(cls, path):
        with open(path, 'rt') as f:
            lines = f.readlines()
            lines = list(map(lambda l: l.strip(), lines))
            matrix = []
            for ln in lines:
                row = ln.split(' ')
                R = [float(c) for c in row]
                matrix.append(R)
            return matrix

if __name__ == '__main__':
    history = InMemoryHistory()

    print('Enter a path to an input/output file to view its plot.')
    print('Ctrl+C or Ctrl+D to exit.')

    try:
        while True:
            path = prompt('> ', history=history)
            if not os.path.exists(path):
                print('No such path exists.')
                continue

            try:
                if path.endswith('.test'):
                    obj = WusnInput.from_file(path, True)
                else:
                    obj = WusnOutput.from_text_file(path)
            except Exception:
                print('Failed!')
                continue

            anchors = obj.anchors
            non_anchors = obj.non_anchors
            ToA_obj = ToA(1., obj.width, obj.height)
            ToA_obj.run_ToA(anchors, non_anchors)
            ToA_obj.to_file('gens.test', 'matrix.test')
            print('Save Gens successfully!')

    except (KeyboardInterrupt, EOFError):
        print()