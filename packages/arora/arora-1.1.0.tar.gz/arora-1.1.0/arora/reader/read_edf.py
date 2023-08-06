import pandas as pd
import mne


def read_edf(file: str, method: str = 'dict') -> dict or pd.DataFrame:
	"""
	:param file:
	:param method:
	:return:
	"""
	if not isinstance(file, str):
		print("The file parameter needs to be a file path in string format")

	raw_data = mne.io.read_raw_edf(file)
	edf_data = raw_data.get_data()
	channels = raw_data.ch_names

	if len(channels) > len(edf_data):
		print("This data has too many channels compared to the data given")
	elif len(channels) < len(edf_data):
		print("This data has too few channels compared to the data given")

	data = {channels[i]: list(edf_data[i]) for i in range(len(channels))}

	if method == 'df':
		df_data = pd.DataFrame.from_dict(data)
		df_data['Frequency'] = raw_data.info['sfreq']
		return df_data
	if method == 'dict':
		data['Frequency'] = raw_data.info['sfreq']

	return data
