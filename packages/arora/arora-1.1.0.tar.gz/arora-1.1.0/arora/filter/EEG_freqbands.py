from typing import List
import arora.filter.bandpass


def eeg_freq_bands(eeg_signal: List[int or float], sampling_frequency: float or int,
                   filter_order: float or int = 5) -> (List, List, List, List):
	"""

	Args:
		eeg_signal: One type of signals from the edf file
		sampling_frequency: The sampling frequency of the eeg signals
		filter_order:

	Returns: Four arrays that contain each bandpass of the most common frequencies

	"""
	alpha_lower = 8
	alpha_upper = 14
	beta_lower = 14
	beta_upper = 50
	delta_lower = 0.5
	delta_upper = 4
	theta_lower = 4
	theta_upper = 8
	delta_band = list(arora.bandpass(eeg_signal, sampling_frequency, delta_lower, delta_upper, filter_order))
	theta_band = list(arora.bandpass(eeg_signal, sampling_frequency, theta_lower, theta_upper, filter_order))
	alpha_band = list(arora.bandpass(eeg_signal, sampling_frequency, alpha_lower, alpha_upper, filter_order))
	beta_band = list(arora.bandpass(eeg_signal, sampling_frequency, beta_lower, beta_upper, filter_order))
	return delta_band, theta_band, alpha_band, beta_band
