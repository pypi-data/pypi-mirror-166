from typing import List


def get_segment(signals: List[int or float], index1: int, index2: int) -> List[int or float]:
	"""
	Args:
		signals: The signal data
		index1: The start of the epoch
		index2: The end of the epoch

	Returns: An array of segmented data
	"""
	# signal_list = []
	#
	# for i in range(index2 - index1):
	# 	# while index < len(signals)
	# 	signal_list.append(signal[index1 + i])
	# assert index1 < 0 or index2 < 0, print("The index has to be larger than 0")
	if index1 < 0 or index2 < 0:
		raise IndexError("The indices have to be greater than or equal to 0")
	if index2 >= len(signals) or index1 >= len(signals):
		raise IndexError("Either index is too large")
	if index1 >= index2:
		return signals[index2:index1]
	else:
		return signals[index1:index2]
