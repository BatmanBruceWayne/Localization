import os
import sys
import pickle
import matplotlib.pyplot as plt

from tqdm import tqdm
from mpl_toolkits.mplot3d import Axes3D

from wusn.commons.point import Point
from wusn.commons.config import get_trans_loss


# Cache related
CACHE_DIR = os.path.join(os.path.expanduser('~'), '.wusn_cache')
os.makedirs(CACHE_DIR, exist_ok=True)


class WusnInput:
    def __init__(self, anchors=None, non_anchors=None, width=1500., height=1000., ignore_cache=False):
        if anchors is None:
            anchors = []
        if non_anchors is None:
            non_anchors = []

        self.anchors = anchors
        self.non_anchors = non_anchors
        self.width = width
        self.height = height
        self._loss = None
        self._loss_index = None

        assert len(self.anchors) == len(set(self.anchors))
        assert len(self.non_anchors) == len(set(self.non_anchors))

        if not ignore_cache:
            self.load_cache()

    @property
    def loss_index(self):
        """
        Calculates the loss index matrix (if neccessary)
        :return: A 2-dimensional list containing
        """
        if self._loss_index is None:
            # if self._loss is None:
            #     self.__get_loss()
            # else:
            #     self.__index_from_loss()
            self.__get_loss()

        return self._loss_index

    @property
    def loss(self):
        """
        Calculates the loss dictionary (if neccessary)
        :return: A dictionary with keys (SN, RN) and the transmission loss as value.
        """
        if self._loss is None:
            self.__get_loss()

        return self._loss

    def __index_from_loss(self):
        self._loss_index = []
        for i, sn in enumerate(self.sensors):
            tmp = []
            for j, rn in enumerate(self.relays):
                l = self._loss[(sn, rn)]
                tmp.append(l)
            self._loss_index.append(tmp)

    def __get_loss(self):
        self._loss_index = []
        self._loss = {}
        print('Calculating transmission loss...')
        tsensors = tqdm(self.sensors, desc='Sensor', ncols=100, file=sys.stdout)
        for i, sn in enumerate(tsensors):
            tmp = []
            for j, rn in enumerate(self.relays):
                d_ug, d_ag = t_distances(sn, rn)
                l = get_trans_loss(d_ug, d_ag)
                tmp.append(l)
                self._loss[(sn, rn)] = l
            self._loss_index.append(tmp)

    @property
    def burial_depth(self):
        if len(self.sensors) < 1:
            return None
        else:
            return self.sensors[0].depth

    @property
    def relay_height(self):
        if len(self.relays) < 1:
            return None
        else:
            return self.relays[0].height

    @classmethod
    def from_file(cls, path, ignore_cache=False):
        with open(path, 'rt') as f:
            lines = f.readlines()
            lines = list(map(lambda l: l.strip(), lines))
            # W H
            width = float(lines[0].split(' ')[0])
            height = float(lines[0].split(' ')[1])
            # N M Y
            m = int(lines[1].split(' ')[0])
            n = int(lines[1].split(' ')[1])
            anchors_ = []
            for ln in lines[2:2+m]:
                order, x, y, r = ln.split(' ')
                anchors_.append(Point(float(x), float(y), float(r), int(order)))

            non_anchors_ = []
            for ln in lines[2+m:2+n+m]:
                order, x, y, r = ln.split(' ')
                non_anchors_.append(Point(float(x), float(y), float(r), int(order)))

            return WusnInput(anchors=anchors_, non_anchors=non_anchors_, width=width, height=height, ignore_cache=ignore_cache)

    def __hash__(self):
        return hash((self.width, self.height, self.relay_num,
                     tuple(self.sensors), tuple(self.relays)))

    def cache_losses(self):
        fname = '%s.loss' % hash(self)
        save_path = os.path.join(CACHE_DIR, fname)
        with open(save_path, 'wb') as f:
            pickle.dump(self.loss, f)
        print('Loss matrix saved to %s' % save_path)

    def load_cache(self):
        fname = '%s.loss' % hash(self)
        save_path = os.path.join(CACHE_DIR, fname)
        if os.path.exists(save_path):
            with open(save_path, 'rb') as f:
                self._loss = pickle.load(f)
                print('Loss matrix loaded from %s' % save_path)
        else:
            print('Cache not found')

    def plot(self, axes: Axes3D, **kwargs):
        # Plot all sensors
        sx = list(map(lambda s: s.x, self.sensors))
        sy = list(map(lambda s: s.y, self.sensors))
        sz = list(map(lambda s: -s.depth, self.sensors))
        axes.scatter(sx, sy, sz, c='r', label='Sensors')

        # Plot all relays
        rx = list(map(lambda r: r.x, self.relays))
        ry = list(map(lambda r: r.y, self.relays))
        rz = list(map(lambda r: r.height, self.relays))
        axes.scatter(rx, ry, rz, c='b', label='Relays')

    def to_file(self, path):
        with open(path, 'wt') as f:
            f.write('%f %f\n' % (self.width, self.height))
            f.write('%d %d\n' % (len(self.anchors), len(self.non_anchors)))

            for s in self.anchors:
                f.write('%d %f %f %f\n' % (s.order, s.x, s.y, s.r))
            for p in self.non_anchors:
                f.write('%d %f %f %f\n' % (p.order, p.x, p.y, p.r))
