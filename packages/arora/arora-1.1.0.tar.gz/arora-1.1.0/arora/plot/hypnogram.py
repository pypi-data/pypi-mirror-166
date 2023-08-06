import warnings

import matplotlib
import matplotlib.pyplot as plt
import numpy as np


def plot_hypnogram(
		stages,
		labeldict=None,
		title=None,
		epochlen=30,
		ax=None,
		xlabel=True,
		ylabel=True,
		**kwargs, ):
	"""
	Plot a hypnogram, based on the stages and given labeldict.
	A labeldict should give a mapping which integer belongs to which class
	E.g labeldict = {0: 'Wake', 4:'REM', 1:'S1', 2:'S2', 3:'SWS'}
	The order of the labels on the plot will be determined by the order of the dictionary.
	This dictionary can be infered automatically from the numbers that are present
	in the hypnogram.
	:param stages: An array with different stages annotated as integers
	:param labeldict: An enumeration of labels that correspond to the integers of stages
	:param title: Title of the window
	:param epochlen: How many seconds is one epoch in this annotation
	:param ax: the axis in which we plot
	:param xlabel: Display xlabel ('Time after record start')
	:param ylabel: Display ylabel ('Sleep Stage')
	:param kwargs: additional arguments passed to plt.plot(), e.g. c='red'
	"""

	if labeldict is None:
		if np.max(stages) == 1 and np.min(stages) == 0:
			labeldict = {0: 'W', 1: 'S'}
		elif np.max(stages) == 2 and np.min(stages) == 0:
			labeldict = {0: 'W', 2: 'REM', 1: 'NREM'}
		elif np.max(stages) == 4 and np.min(stages) == 0:
			if 1 in stages:
				labeldict = {0: 'W', 4: 'REM', 1: 'S1', 2: 'S2', 3: 'SWS', }
			else:
				labeldict = {0: 'W', 4: 'REM', 2: 'S2', 3: 'SWS'}
		elif np.max(stages) == 9 and np.min(stages) == 0:
			if 1 in stages:
				labeldict = {0: 'W', 4: 'REM', 1: 'S1', 2: 'S2', 3: 'SWS', 9: 'A'}
			else:
				labeldict = {0: 'W', 4: 'REM', 2: 'S2', 3: 'SWS'}
		else:
			if 1 in stages:
				labeldict = {0: 'W', 4: 'REM', 1: 'S1', 2: 'S2', 3: 'SWS', 5: 'A'}
			else:
				labeldict = {0: 'W', 4: 'REM', 2: 'S2', 3: 'SWS', 5: 'A'}
		if -1 in stages:
			labeldict['ARTEFACT'] = -1

	# check if all stages that are in the hypnogram have a corresponding label in the dict
	for stage in np.unique(stages):
		if stage not in labeldict:
			print('WARNING: {} is in stages, but not in labeldict, stage will be ??'.format(stage))

	# create the label order
	labels = [labeldict[label] for label in labeldict]
	labels = sorted(set(labels), key=labels.index)

	# we iterate through the stages and fetch the label for this stage
	# then we append the position on the plot of this stage via the labels-dict
	x = []
	y = []
	rem_start = []
	rem_end = []
	for i in np.arange(len(stages)):
		s = stages[i]
		label = labeldict.get(s)
		if label is None:
			p = 99
			if '??' not in labels:
				labels.append('??')
		else:
			p = -labels.index(label)

		# make some red line markers for REM, mark beginning and end of REM
		if 'REM' in labels:
			if label == 'REM' and len(rem_start) == len(rem_end):
				rem_start.append(i - 2)
			elif label != 'REM' and len(rem_start) > len(rem_end):
				rem_end.append(i - 1)
		if label == 'REM' and i == len(stages) - 1:
			rem_end.append(i + 1)

		if i != 0:
			y.append(p)
			x.append(i - 1)
		else:
			y.append(p)
			x.append(i)

	assert len(rem_start) == len(rem_end), 'Something went wrong in REM length calculation'

	x = np.array(x)
	y = np.array(y)
	y[y == 99] = y.min() - 1  # make sure Unknown stage is plotted below all else

	if ax is None:
		plt.figure()
		ax = matplotlib.pyplot.gca()
	#formatter = matplotlib.ticker.FuncFormatter(lambda s, x: time.strftime('%H:%M', time.gmtime(s))) # will need to have the time from the start of the epoch and the end - have this as a parameter

	ax.plot(x, y, **kwargs)
	ax.set_xlim(0, x[-1])
	#ax.xaxis.set_major_formatter(formatter)

	ax.set_yticks(np.arange(len(np.unique(labels))) * -1)
	ax.set_yticklabels(labels)
	#ax.set_xticks(np.arange(0, x[-1], 3600))
	#ax.set_xticks(len(stages))

	if xlabel:
		plt.xlabel('Epoch after recording start')
	if ylabel:
		plt.ylabel('Sleep Stage')
	if title is not None:
		ax.set_title(title)

	try:
		warnings.filterwarnings("ignore", message='This figure includes Axes that are not compatible')
		plt.tight_layout()
	except Exception:
		pass

	# plot REM in RED here
	for start, end in zip(rem_start, rem_end):
		height = -labels.index('REM')
		ax.hlines(height, start * epochlen, end * epochlen, color='r', linewidth=4, zorder=99)

	plt.show()

