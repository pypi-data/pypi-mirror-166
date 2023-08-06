from typing import List
from scipy import signal


def resample(signals: List[int or float],  old_fs: int, new_fs: int) -> List:
	"""
	Matias gave us the base of this code
	Args:
		signals:
		new_fs:
		old_fs:

	Returns:

	"""
	return list(signal.resample(signals, int((new_fs/old_fs)*len(signals))))
