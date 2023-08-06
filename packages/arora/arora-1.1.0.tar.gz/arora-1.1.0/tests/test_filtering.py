import unittest
from random import random

import numpy as np

from arora import bandpass, low_pass_filter, high_pass_filter, upper_lower_signal_envelopes, eeg_freq_bands, cheby2_highpass_filtfilt
from arora.exceptions import CutoffValueError


class TestFiltering(unittest.TestCase):

    def test_low_pass_filter(self):
        r = 1000
        fs = 200
        cutoff = 99
        inp = [random() for _ in range(r)]
        out = low_pass_filter(inp, fs, cutoff)
        self.assertEqual(len(out), r)
        self.assertNotEqual(inp, out)
        self.assertEqual(type(out), list)

        message = "Please check your parameters"
        cutoff = 100
        with self.assertRaises(CutoffValueError) as cx:
            low_pass_filter(inp, fs, cutoff)
            # Your cutoff ({self.cutoff}) value is not in the range 0 < x < 1 -> {self.message}"
            self.assertTrue(
                f"Your cutoff ({cutoff / (0.5 * fs)}) value is not in the range 0 < x < 1 -> {message}" in cx.exception)

    def test_high_pass_filter(self):
        r = 1000
        fs = 200
        cutoff = 50
        inp = [random() for _ in range(r)]
        out = high_pass_filter(inp, fs, cutoff)
        self.assertEqual(len(out), r)
        self.assertNotEqual(inp, out)
        self.assertEqual(type(out), list)

        message = "Please check your parameters"
        cutoff = 100
        with self.assertRaises(CutoffValueError) as cx:
            high_pass_filter(inp, fs, cutoff)
            # Your cutoff ({self.cutoff}) value is not in the range 0 < x < 1 -> {self.message}"
            self.assertTrue(
                f"Your cutoff ({cutoff / (0.5 * fs)}) value is not in the range 0 < x < 1 -> {message}" in cx.exception)

    def test_bandpass(self):
        r = 1000
        inp = [random() for _ in range(r)]
        lower = 99
        upper = 1
        fs = 200
        out = bandpass(inp, fs, lower, upper, 5)
        self.assertEqual(len(out), r)
        self.assertEqual(type(out), list)
        self.assertNotEqual(inp, out)

        message = "Please check your parameters"
        with self.assertRaises(CutoffValueError) as cx:
            lower = 0
            bandpass(inp, fs, lower, upper, 5)
            self.assertTrue(
                f"Your cutoff ({lower / (0.5 * fs)}) value is not in the range 0 < x < 1 -> {message}" in cx.exception)
            lower = 2
            upper = 200
            bandpass(inp, fs, lower, upper, 5)
            self.assertTrue(
                f"Your cutoff ({upper / (0.5 * fs)}) value is not in the range 0 < x < 1 -> {message}" in cx.exception)

    def test_EEG_freqbands(self):
        r = 1000
        fs = 200
        inp = [random() for _ in range(r)]
        out = eeg_freq_bands(inp, fs)
        self.assertEqual(type(out), tuple)
        for i in range(len(out)):
            self.assertEqual(type(out[i]), list)
            self.assertNotEqual(inp, out[i])

    def test_signal_envelopes(self):
        r = 1000
        inp = np.array([random() for _ in range(r)])
        out_upp, out_low = upper_lower_signal_envelopes(inp)
        self.assertEqual(type(out_upp), list)
        self.assertEqual(type(out_low), list)
        self.assertEqual((inp == out_upp).all(), False)
        self.assertEqual((inp == out_low).all(), False)

    def test_cheby_filter(self):
        r = 1000
        fs = 200
        cutoff = 50
        inp = [random() for _ in range(r)]
        out = cheby2_highpass_filtfilt(inp, fs, cutoff)
        self.assertEqual(type(out), list)
        self.assertNotEqual(inp, out)

        message = "Please check your parameters"
        with self.assertRaises(CutoffValueError) as cx:
            cutoff = 200
            cheby2_highpass_filtfilt(inp, fs, cutoff)
            self.assertTrue(
                f"Your cutoff ({cutoff / (0.5 * fs)}) value is not in the range 0 < x < 1 -> {message}" in cx.exception)


if __name__ == '__main__':
    unittest.main()
