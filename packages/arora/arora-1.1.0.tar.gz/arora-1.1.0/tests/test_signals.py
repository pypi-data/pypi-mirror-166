import unittest
from random import random
from numpy import mean, median, ndarray, around

from arora import lower_frequency, resample, fourier


class TestSignals(unittest.TestCase):

    def test_lower_min(self):
        r = 1000
        fs = 100
        inp = [round(random()*100, 1) for _ in range(r)]
        out = lower_frequency(inp, new_fs=fs, method='min')
        self.assertEqual(type(out), list)
        self.assertEqual(len(out), r / fs)
        self.assertEqual(min(inp[0:fs]), out[0])
        self.assertEqual(min(inp[-fs:]), out[-1])

    def test_lower_max(self):
        r = 1000
        fs = 100
        inp = [round(random() * 100, 1) for _ in range(r)]
        out = lower_frequency(inp, new_fs=fs, method='max')
        self.assertEqual(type(out), list)
        self.assertEqual(len(out), r / fs)
        self.assertEqual(max(inp[:fs]), out[0])
        self.assertEqual(max(inp[fs * 2:fs * 3]), out[2])

    def test_lower_mean(self):
        r = 1000
        fs = 100
        inp = [round(random() * 100, 1) for _ in range(r)]
        out = lower_frequency(inp, new_fs=fs, method='mean')
        self.assertEqual(type(out), list)
        self.assertEqual(len(out), r / fs)
        self.assertEqual(mean(inp[fs * 2:fs * 3]), out[2])
        self.assertEqual(mean(inp[fs * 4:fs * 5]), out[4])

    def test_lower_median(self):
        r = 1000
        fs = 100
        inp = [round(random() * 100, 1) for _ in range(r)]
        out = lower_frequency(inp, new_fs=fs, method='median')
        self.assertEqual(type(out), list)
        self.assertEqual(len(out), r / fs)
        self.assertEqual(median(inp[fs * 3:fs * 4]), out[3])
        self.assertEqual(median(inp[fs * 6:fs * 7]), out[6])

    def test_resample(self):
        r = 1000
        new_fs = 100
        old_fs = 200
        inp = [round(random() * 100, 1) for _ in range(r)]
        out = resample(inp, old_fs, new_fs)
        self.assertEqual(type(out), list)
        self.assertEqual(len(out), len(inp) * (new_fs / old_fs))
        self.assertNotEqual(inp, out)

    def test_resample_same_freq(self):
        r = 1000
        new_fs = 100
        old_fs = 100
        inp = [round(random() * 100, 1) for _ in range(r)]
        out = [round(x, 1) for x in resample(inp, old_fs, new_fs)]
        self.assertEqual(type(out), list)
        self.assertEqual(len(out), len(inp) * (new_fs / old_fs))
        self.assertEqual(inp, out)

    def test_fourier(self):
        r = 1000
        fs = 200
        inp = [[round(random() * 100, 1) for _ in range(10)] for _ in range(r)]
        out = fourier(inp, fs)
        self.assertEqual(type(out), list)
        for i in range(len(out)):
            self.assertEqual(type(out[i]), ndarray)
            self.assertNotEqual(inp[i], list(out[i]))


if __name__ == '__main__':
    unittest.main()
