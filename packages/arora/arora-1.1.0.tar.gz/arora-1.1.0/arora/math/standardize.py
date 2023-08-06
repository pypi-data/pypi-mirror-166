import numpy as np
from typing import List


def standardize(epoch: List[int or float]) -> List:
	"""
	Matias gave us this code
	Z-score normalization for the signals.
	Args:
		epoch: An epoch of some signal
	Returns: Z-score normalized epoch
	"""
	return list((epoch - np.mean(epoch)) / np.std(epoch))
