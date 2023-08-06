import random
import unittest
from math import ceil

from arora import get_segment, segment_fs


class TestSegmentation(unittest.TestCase):
    def test_get_segment(self):
        inp = [random.random() for _ in range(1000)]
        i1 = 200
        i2 = 300
        out = get_segment(inp, i1, i2)
        self.assertEqual(type(out), list)
        self.assertEqual(len(out), i2 - i1)
        self.assertEqual(out, inp[i1:i2])

        out2 = get_segment(inp, i2, i1)
        self.assertEqual(type(out2), list)
        self.assertEqual(len(out2), i2 - i1)
        self.assertEqual(out, inp[i1:i2])

    def test_get_segment_index_error(self):
        inp = [random.random() for _ in range(1000)]

        # either index is negative
        self.assertRaises(IndexError, get_segment, inp, -1, 3)
        self.assertRaises(IndexError, get_segment, inp, 302, -62)

        # index is larger than length of list
        self.assertRaises(IndexError, get_segment, inp, 200, 1005)
        self.assertRaises(IndexError, get_segment, inp, 1000, 3000)

    def test_segment_fs(self):
        r = 10000
        inp = [random.random() for _ in range(r)]
        fs = 200
        out = segment_fs(inp, fs)
        self.assertEqual(type(out), list)
        self.assertEqual(len(out), r / fs)
        for elem in out:
            self.assertEqual(type(elem), list)
            self.assertEqual(len(elem), fs)

    def test_segment_fs_odd_fs(self):
        r = 10000
        inp = [random.random() for _ in range(r)]
        fs = 300
        out = segment_fs(inp, fs)
        self.assertEqual(type(out), list)
        self.assertEqual(len(out), ceil(r / fs))
        self.assertGreater(fs, len(out[-1]))


if __name__ == '__main__':
    unittest.main()
