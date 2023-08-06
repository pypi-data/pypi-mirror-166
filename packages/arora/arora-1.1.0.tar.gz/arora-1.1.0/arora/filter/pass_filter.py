from scipy import signal
from typing import List
from arora.exceptions import CutoffValueError


def _butter_pass(
		cutoff: int or float,
		sampling_frequency: int or float,
		btype: str,
		order: int = 5) -> (List, List):
	"""
	Args:
		cutoff: The frequency that is to be filtered through --> integer or float
		sampling_frequency: The frequency of the data --> integer or float
		btype: The order of the filter --> string
		order: The type of filtering --> integer
	Returns:The denominator and the numerator polynomials of the IIR filter --> Numpy ndarray, numpy ndarray
	"""
	nyq = 0.5 * sampling_frequency
	normal_cutoff = cutoff / nyq
	if normal_cutoff <= 0 or normal_cutoff >= 1:
		raise CutoffValueError(normal_cutoff)
	num, denom = signal.butter(order, normal_cutoff, btype=btype, analog=False)
	return list(num), list(denom)


def low_pass_filter(
		signals: List[int or float],
		sampling_frequency: int or float,
		cutoff: int or float,
		order: int = 5) -> List:
	"""
	Performs lowpass filtering on the signals
	Args:
		signals: Array of integers or float
		sampling_frequency: The frequency of the data --> integer or float
		cutoff: The frequency that is to be filtered through --> integer or float
		order: order: The order of the filter --> integer

	Returns: An array of filtered data using the Buttersworth method --> Numpy ndarray

	"""
	b, a = _butter_pass(cutoff, sampling_frequency, btype='lowpass', order=order)
	y = signal.lfilter(b, a, signals)
	return list(y)


def high_pass_filter(
		signals: List[int or float],
		sampling_frequency: int or float,
		cutoff: int or float,
		order: int = 5) -> List:
	"""
	Performs high pass filtering on the signals
	Args:
		signals: Array of integers or float
		sampling_frequency: The frequency of the data --> integer or float
		cutoff: The frequency that is to be filtered through --> integer or float
		order: The order of the filter --> integer

	Returns: An array of filtered data using the Buttersworth method --> Numpy ndarray
	"""
	b, a = _butter_pass(cutoff, sampling_frequency, btype='highpass', order=order)
	y = signal.filtfilt(b, a, signals, axis=0)
	return list(y)


def cheby2_highpass_filtfilt(
		signals: List[int or float],
		sampling_frequency: int or float,
		cutoff: int,
		order: int = 5,
		rs: float = 40.0) -> List:
	"""
	Chebyshev type1 highpass filtering.
	Matias Rusanen, M.Sc., gave us this code
	Args:
		signals: the signals
		sampling_frequency: sampling frequency in Hz
		cutoff: cutoff frequency in Hz
		order: the order of the filter
		rs:
	Returns:
		the filtered signals
	"""
	nyq = 0.5 * sampling_frequency
	norm_cutoff = cutoff / nyq
	if norm_cutoff <= 0 or norm_cutoff >= 1:
		raise CutoffValueError(norm_cutoff)
	sos = signal.cheby2(order, rs, norm_cutoff, btype='highpass', output='sos')
	return list(signal.sosfiltfilt(sos, signals))
