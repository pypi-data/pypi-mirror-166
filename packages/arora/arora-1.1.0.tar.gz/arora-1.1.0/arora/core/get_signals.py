from typing import List
import mne


def get_signals(file, signalname: str or List[str] = 'all') -> \
		(List[int or float] or List[List[int or float]], List[str] or str):
	"""

	Args:
		file: The edf file that is to be imported
		signalname: The name of the signals that is wanted, can also be a list of signals that are wanted

	Returns: list of all the signals that were requested and list of all the signals in the order of the corresponding
	list of the signals. Will not return always return in the same order as the signalname is in

	"""

	signal = []
	name_signal = []
	# Get the signals and the signal headers from the file
	raw_data = mne.io.read_raw_edf(file)
	data = raw_data.get_data()
	channels = raw_data.ch_names

	# Check if the requested signals is all and return just the recently gathered signals
	if signalname == 'all':
		return data, channels

	index = 0

	# Check if signals name is either list or string
	if type(signalname) == list:
		# Check for duplicates in the list and remove them
		signalname = __check_duplicates_and_remove(signalname)

		for channel in channels:

			# Check if the label is in the parameter signal names
			if channel in signalname:
				# Remove the instance from the list to make the code more efficient
				signalname.remove(channel)
				signal.append(data[index])
				name_signal.append(channel)

			# Check if the list is empty and return the gathered signals
			if len(signalname) <= 0:
				return signal
			index += 1

	elif type(signalname) == str:

		for channel in channels:

			if channel == signalname:
				signal.append(data[index])
				name_signal.append(channel)
			index += 1

	return signal, name_signal


def get_signals_from_list(
		signals: List[int or float],
		channels: List[str],
		signalname: str or List[str] = 'all') -> (List[int or float] or List[List[int or float]], List[str]):
	"""

	Args:
		signals:
		channels:
		signalname:

	Returns:

	"""
	signal = []
	name_signal = []

	if signalname == 'all':
		return signals, channels

	index = 0

	if type(signalname) == list:
		# Check for duplicates in the list and remove them
		signalname = __check_duplicates_and_remove(signalname)

		for channel in channels:

			# Check if the label is in the parameter signal names
			if channel in signalname:
				# Remove the instance from the list to make the code more efficient
				signalname.remove(channel)
				signal.append(signals[index])
				name_signal.append(channel)

			# Check if the list is empty and return the gathered signals
			if len(signalname) <= 0:
				return signal
			index += 1

	elif type(signalname) == str:

		for channel in channels:

			if channel == signalname:
				signal.append(signals[index])
				name_signal.append(channel)
			index += 1

	return signal, name_signal


def __check_duplicates_and_remove(signal):
	"""
	Checks for duplicates and removes them

	Args:
		signal: A list of all signals labels

	Returns: list with all duplicates removed

	"""
	elems = []

	# Loop through the list
	for elem in signal:

		# If the instance is not in the created list insert it into the list
		if elem not in elems:
			elems.append(elem)

	return elems
