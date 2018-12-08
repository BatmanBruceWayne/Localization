from argparse import ArgumentParser

import random
import os
# import numpy as np

from wusn.commons import WusnInput, Point


def parse_arguments():
    parser = ArgumentParser()

    parser.add_argument('-o', '--output-dir', default='data')
    parser.add_argument('-c', '--count', type=int, default=5)
    parser.add_argument('-W', '--width', type=float, default=1500.)
    parser.add_argument('-H', '--height', type=float, default=1000.)
    parser.add_argument('-N', '--anchors', type=int, default=20)
    parser.add_argument('-M', '--non_anchors', type=int, default=80)
    # parser.add_argument('-Y', type=int, default=20)
    parser.add_argument('-radius', type=float, default=100.)

    return parser.parse_args()


def uniform_point(max_width, max_height):
    return random.uniform(0., max_width), random.uniform(0., max_height)


def uniform_anchors(width, height, M):
    anchors = []
    for i in range(M):
        x, y = uniform_point(width, height)
        sn = Point(x=x, y=y, r=100., order=i)
        while sn in anchors:
            x, y = uniform_point(width, height)
            sn = Point(x=x, y=y, r=100., order=i)
        anchors.append(sn)
    return anchors

def uniform_non_anchors(width, height, N, M):
    non_anchors = []
    for i in range(N):
        x, y = uniform_point(width, height)
        rn = Point(x=x, y=y, r=100., order=i+M)
        while rn in non_anchors:
            x, y = uniform_point(width, height)
            rn = Point(x=x, y=y, r=100., order=i+M)
        non_anchors.append(rn)
    return non_anchors

GENS = {
    'rr': (uniform_anchors, uniform_non_anchors),
    # 'rhr': (uniform_sensors, uniform_half_relays),
}


if __name__ == '__main__':
    args = parse_arguments()
    count = 1
    for name, (fn_s, fn_r) in GENS.items():
        for i in range(args.count):
            anchors_ = fn_s(args.width, args.height, args.anchors)
            non_anchors_ = fn_r(args.width, args.height, args.non_anchors, args.anchors)
            inp = WusnInput(anchors=anchors_, non_anchors=non_anchors_, width=args.width, height=args.height, ignore_cache=True)

            fname = '%s-%03d.test' % (name, i + 1)
            path = os.path.join(args.output_dir, fname)
            print('Saving test case %d to %s' % (count, path))
            count += 1
            inp.to_file(path)