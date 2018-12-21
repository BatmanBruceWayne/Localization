from wusn.commons import Individual, NonAnchor
import os
from wusn.commons.point import Point

from simulated_ToA import ToA
import common as cm
from wusn.commons import WusnInput
import math

def from_file_result(path):
    with open(path, 'rt') as f:
        non_anchors_result = []
        lines = f.readlines()
        lines = list(map(lambda l: l.strip(), lines))
        n = int(lines[0].split(' ')[0])
        for ln in lines[1:1+n]:
            order, x, y = ln.split(' ')
            non_anchors_result.append(Point(float(x), float(y), 30., int(order)))
        return non_anchors_result

if __name__ == '__main__':
    path_1 = 'result.test'
    path_2 = ''
    # print('Enter a path to an input/output file to gens.')
    # path_1 = input()
    # print('Enter a path to an input/output file to matrix.')
    # path_2 = input()
    print('Enter a path to an input/output file to data.')
    path_2 = input()

    try:

        if not os.path.exists(path_1) or not os.path.exists(path_2):
            print('No such path exists.')
        try:
            obj = WusnInput.from_file(path_2, True)
        except Exception:
            print('Failed')

        avg_error = 0
        non_anchors = obj.non_anchors
        non_anchors_result = from_file_result(path_1)
        n = len(non_anchors)
        for i in range(n):
            p_1 = non_anchors[i]
            p_2 = non_anchors_result[i]
            avg_error += math.sqrt((p_1.x-p_2.x)**2 + (p_1.y - p_2.y)**2)
        avg_error /= n
        print(avg_error)

    except (KeyboardInterrupt, EOFError):
        print()
