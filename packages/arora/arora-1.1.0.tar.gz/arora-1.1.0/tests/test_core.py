import unittest
from random import random
import pandas as pd

from arora.core import segmentation, epochize, get_signals
from arora.exceptions import TooLarge, Negative


class TestCore(unittest.TestCase):
    def test_segmentation_wo_df_even_index(self):
        fs = 250
        d = 30
        inp = [random() for _ in range(15000)]
        out = segmentation(inp, only_signals=True, duration=d)
        for elem in out:
            self.assertEqual(len(elem), len(inp) / len(out))
            self.assertEqual(type(elem), list)
        self.assertEqual(type(out), list)
        self.assertEqual(len(out), len(inp) / (fs * d))
        # self.assertEqual(type((len(inp) / (fs * d))), int)

    def test_segmentation_wo_df_one_segment(self):
        fs = 250
        d = 30
        inp = [random() for _ in range(6000)]
        out = segmentation(inp, only_signals=True, duration=d)
        for elem in out:
            self.assertEqual(type(elem), list)
        self.assertEqual(type(out), list)
        self.assertNotEqual(len(out), len(inp) / (fs * d))
        self.assertEqual(out[0], inp)

    def test_segmentation_w_df(self):
        fs = 250
        d = 30
        inp = [random() for _ in range(15000)]
        out, df_out = segmentation(inp, duration=d)
        for i, elem in enumerate(reversed(out)):
            self.assertEqual(len(elem), len(inp) / len(out))
            self.assertEqual(type(elem), list)
            self.assertEqual(elem, inp[df_out['beg_index'].iloc[i]:df_out['end_index'].iloc[i] + 1])
        self.assertEqual(type(out), list)
        self.assertEqual(type(df_out), pd.DataFrame)
        self.assertEqual(len(df_out), len(out))
        self.assertEqual(len(out), len(inp) / (fs * d))

    def test_segmentation_w_df_one_segment(self):
        fs = 250
        d = 30
        inp = [random() for _ in range(6000)]
        out, df_out = segmentation(inp, duration=d)
        self.assertEqual(out[0], inp[df_out['beg_index'].iloc[0]:df_out['end_index'].iloc[0] + 1])
        self.assertEqual(type(out), list)
        self.assertEqual(type(df_out), pd.DataFrame)
        self.assertEqual(len(df_out), len(out))

    def test_segmentation_different_time_units(self):
        fs = 250
        d = 30
        inp_mins = [random() for _ in range(6000)]
        inp_hour = [random() for _ in range(6000)]

        out_mins = segmentation(inp_mins, only_signals=True)
        out_hour = segmentation(inp_hour, only_signals=True)

        self.assertEqual(type(out_mins), list)
        self.assertEqual(type(out_hour), list)
        self.assertNotEqual(len(out_mins), len(inp_mins) / (fs * d))
        self.assertNotEqual(len(out_hour), len(inp_hour) / (fs * d))

    def test_segmentation_errors(self):
        ons_message = "Please check your onset parameter"
        dur_message = "Please check your duration parameter"
        inp = [1, 2, 3, 4]
        onset = 5
        duration = 5
        with self.assertRaises(TooLarge) as cx:
            segmentation(inp, onset=onset)
            self.assertTrue(f"{onset} is larger than the length ({len(inp)}) -> {ons_message}" in cx.exception)
            segmentation(inp, duration=duration)
            self.assertTrue(f"{duration} is larger than the length ({len(inp)}) -> {dur_message}" in cx.exception)

        onset = -1
        duration = -1
        with self.assertRaises(Negative) as cx:
            segmentation(inp, onset=onset, duration=3)
            self.assertTrue(f"{onset} is negative and thus unable to be used -> {ons_message}" in cx.exception)
            segmentation(inp, duration=duration)
            self.assertTrue(f"{duration} is negative and thus unable to be used -> {dur_message}" in cx.exception)


if __name__ == '__main__':
    unittest.main()
