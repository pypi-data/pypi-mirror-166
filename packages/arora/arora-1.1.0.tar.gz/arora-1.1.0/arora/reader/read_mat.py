from typing import List, Dict, Any
import pandas as pd
import mat4py
import mat73

from dateutil.parser import parse


def read_mat(file: str, types: str) -> (List[int or float], pd.DataFrame):
	"""
	This function is a WIP
	Args:
		file:
		types:

	Returns:

	"""
	# If mat files all have the same format then hardcode how to insert the code into the dataframe and signals list
	allowededf = [
		'digitalMax', 'digitalMin',
		'label', 'duration',
		'physicalMax', 'physicalMin',
		'samples'
	]
	events = [
		'AllScoredEvents', 'ArousalEvents',
		'Desaturation Events', 'RespiratoryEvents'
	]
	hypnogram = [
		'HypnogramCharFixed',
		'HypnogramCharRaw', 'HypnogramKey',
		'HypnogramNum'
	]
	header = {}

	if types == "edf":
		data = mat73.loadmat(file)
		headers, signal = data['header'], data['signals']
		for key, value in headers.items():
			if key in allowededf:
				header[key] = value
		header_df = pd.DataFrame.from_dict(header)
		return signal, header_df
	if types == "scoring":
		# split Hypnogram and Events into two
		# Matrix manipulation for the Events is necessary - Each row in DataFrame represents all
		# the information about the event - Columns: what group of event - time - score of event - event
		# ArousalEvents is a matrix and need to map each event to the time, score and name of event
		# Same with DesaturationEvents and RespiratoryEvents
		# Check if HypnogramCharFixed and HypnogramCharRaw are the same and if so just use one
		# HypnogramKey needs to map the key to the named event and need to be fixed for Bent
		# Map the HypnoGramNum to HypnogramChar - best to just use a DataFrame with both these columns

		data = mat4py.loadmat(file)

		desat = {}
		arousal = {}
		respiratory = {}

		for key, value in data.items():
			if key in events:
				if 'desat' in key.islower():
					desat = _work_desat(data[key])
				if 'arousal' in key.islower():
					arousal = _work_arousal(data[key])
				if "respiratory" in key.islower():
					respiratory = _work_respiratory(data[key])

				# event_dict[key] = value
		if len(respiratory) and len(desat) and len(arousal) != 0:
			scoring = pd.DataFrame([desat, arousal, respiratory])
		else:
			if len(respiratory) != 0:
				scoring = pd.DataFrame([desat, arousal])
			elif len(arousal) != 0:
				scoring = pd.DataFrame([desat, respiratory])
			elif len(respiratory) != 0:
				scoring = pd.DataFrame([desat, arousal])
		# Will return error as there are different lengths of arrays in dict
		# hypno_df = pd.DataFrame.from_dict(hypno_dict)
		return data, scoring

	if types == 'hypnogram':
		return

	return "This function is still a WIP"


# allowedscoring = [
# 	'AllScoredEvents', 'ArousalEvents',
# 	'Desaturation Events', 'HypnogramCharFixed',
# 	'HypnogramCharRaw', 'HypnogramKey',
# 	'HypnogramNum', 'RespiratoryEvents'
# 	#'ReportAHI', 'ReportTST'
# ]


def _is_date(string: str, fuzzy = False) -> Any:
	"""
    Return whether the string can be interpreted as a date.

    :param string: str, string to check for date
    :param fuzzy: bool, ignore unknown tokens in string if True
    """
	try:
		parse(string, fuzzy = fuzzy)
		return True

	except:
		return False


def _work_desat(desat_list: List[List]) -> Dict:
	dictdf = {}

	date_list = []
	event_list = []
	score_list = []

	for index in desat_list:
		for elem in index:

			if _is_date(elem):
				date_list.append(elem)

			elif elem == 'Desat':
				event_list.append(elem)

			elif isinstance(elem, float) and elem > 1:
				score_list.append(elem)

	dictdf['Date'] = date_list
	dictdf['Event'] = event_list
	dictdf['Score'] = score_list
	return dictdf


def _work_arousal(arousal_list: List[List]) -> Dict:
	dictdf = {}

	date_list = []
	event_list = []
	score_list = []

	for index in arousal_list:
		for elem in index:
			if _is_date(elem):
				date_list.append(elem)

			elif isinstance(elem, str):
				event_list.append(elem)

			elif isinstance(elem, float) and elem > 1 or isinstance(elem, int) and elem > 1:
				score_list.append(elem)

	dictdf['Date'] = date_list
	dictdf['Event'] = event_list
	dictdf['Score'] = score_list
	return dictdf


def _work_respiratory(respiratory_list: List[List]) -> Dict:
	dictdf = {}

	date_list = []
	event_list = []
	score_list = []

	for index in respiratory_list:
		for elem in index:
			if _is_date(elem):
				date_list.append(elem)

			elif isinstance(elem, str):
				event_list.append(elem)

			elif isinstance(elem, float) and elem > 1 or isinstance(elem, int) and elem > 1:
				score_list.append(elem)

	dictdf['Date'] = date_list
	dictdf['Event'] = event_list
	dictdf['Score'] = score_list
	return dictdf
