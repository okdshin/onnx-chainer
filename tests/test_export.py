import unittest

import chainer
import chainer.functions as F
import chainer.links as L
import numpy as np
import onnx_chainer


class MLP(chainer.Chain):

    def __init__(self, n_units, n_out):
        super(MLP, self).__init__()
        with self.init_scope():
            self.l1 = L.Convolution2D(None, n_units, 3, 1, 1)
            self.b1 = L.BatchNormalization(n_units)
            self.l2 = L.Linear(None, n_units)

    def __call__(self, x):
        h = self.b1(F.relu(self.l1(x)))
        return self.l2(h)


class TestExport(unittest.TestCase):

    def setUp(self):
        self.model = MLP(3, 5)
        self.x = np.zeros((1, 3, 5, 5), dtype=np.float32)

    def test_export(self):
        model = onnx_chainer.export(self.model, self.x)
        print(model)
