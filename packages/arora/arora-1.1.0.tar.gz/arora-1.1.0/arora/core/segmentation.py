import datetime
import math

import pandas as pd
from pandas import DataFrame
from typing import Union, List
import numpy as np
from arora.exceptions import TooLarge, Negative


def segmentation(signals: List[int or float], frequency: float = 250.0, onset: int = 0,
                 duration: int = 30, only_signals: bool = False, time_unit: str = "sec")\
        -> List[List[int or float]] or (List[List[int or float]], pd.DataFrame):
    """
    Function that splits time series data based on the given frequency and duration
    Args:
        signals: list of EEG signals
        frequency: sample frequency of the EEG signals
        onset: start of recording in seconds
        duration: end of recording in seconds
        only_signals: says what the user want to recieve -
        either just an array of signals or a DataFrame included
        time_unit: the unit of time for the duration

    Returns: a list of EEG signals and pandas DataFrame including the beginning and end index of the sample

    """

    if time_unit == "min":
        duration *= 60
    elif time_unit == "hours":
        duration *= 3600

    signal_list = []
    index_dataframe = pd.DataFrame()
    temp_dataframe = pd.DataFrame()
    if onset > len(signals):
        raise TooLarge(onset, len(signals), "Please check your onset parameter")
    if duration > len(signals):
        raise TooLarge(duration, len(signals), "Please check your duration parameter")
    if duration < 0:
        raise Negative(duration, "Please check your duration input")
    if onset < 0:
        raise Negative(onset, "Please check your onset input")

    if only_signals:
        # find the beginning index by transferring time into index using the sampling frequency
        beg_index = int(onset * frequency)

        # find the end index by figuring out the
        end_index = int((onset + duration) * frequency)

        # end index might be out of scope of the list in which case we'll return as much as we can
        if end_index > len(signals):
            print("Warning: Your parameters resulted in a single segment. Tweak your input if you want a different result")

            signal_list.append(signals[beg_index:])

            return signal_list

        while end_index <= len(signals) and beg_index <= len(signals):
            # for _ in range(beg_index, len(signals), end_index):
            signal_list.append(signals[beg_index:end_index])

            onset += duration
            beg_index = end_index
            end_index = int((onset + duration) * frequency)

        if beg_index < len(signals):
            signal_list.append(signals[beg_index:])

        return signal_list

    # find the beginning index by transferring time into index using the sampling frequency
    beg_index = int(onset * frequency)

    # find the end index by figuring out the
    end_index = int((onset + duration) * frequency)

    # end index might be out of scope of the list in which case we'll return as much as we can
    if end_index > len(signals):
        print("Warning: Your parameters resulted in a single segment. Tweak your input if you want a different result")

        signal_list.append(signals[beg_index:])
        end_index = len(signals)
        index_dataframe['beg_index'] = [beg_index]
        index_dataframe['end_index'] = [end_index - 1]

        return signal_list, index_dataframe

    while end_index <= len(signals) and beg_index <= len(signals):
        # for _ in range(beg_index, len(signals), end_index):
        signal_list.append(signals[beg_index:end_index])
        temp_dataframe['beg_index'] = [beg_index]
        temp_dataframe['end_index'] = [end_index - 1]

        index_dataframe = pd.concat([temp_dataframe, index_dataframe],
                                    axis=0,
                                    sort=True,
                                    ignore_index=True)

        onset += duration
        beg_index = end_index
        end_index = int((onset + duration) * frequency)

    if beg_index < len(signals):
        signal_list.append(signals[beg_index:])
        # index_dataframe = pd.concat([temp_dataframe, index_dataframe], sort=False)
    return signal_list, index_dataframe


def epochize(data: List[int or float], channel_names: List[str], epoch_len: int,
             sampling_freq: int or float, start_timestamp: datetime) -> pd.DataFrame:
    """
    Args:
        data: EDF file turned into an array -> pd.DataFrame
        channel_names: The names of the channels to be used -> list[str]
        epoch_len: How long the epoch should be - will be changed to duration later on -> integer
        sampling_freq: The sampling frequency of the data -> float or integer
        start_timestamp: ??? - Will be removed later on

    Returns: A dataframe with the epochs
    """
    # Acknowledgement: Katrín Hera, M.Sc. student

    # Find the length of the signals
    l = len(data)
    # Find the number of data points
    number = int(epoch_len * sampling_freq)
    # initialize the epoch list
    epochs = []
    # add the epochs to the list
    for x in range(0, l, int(epoch_len * sampling_freq)):
        epochs.append(data[x:x + number])
    # initialize a list of timestamps at the beginning of each epoch
    timestamps_epoch_start = []
    for i in range(int(len(data) / (epoch_len * sampling_freq))):
        # make start timestamps for all the subsequent epochs and add to list
        next_timestamp = start_timestamp + datetime.timedelta(seconds=epoch_len * i)
        timestamps_epoch_start.append(next_timestamp)
    # make dataframe with timestamps and epoch
    df: DataFrame = pd.DataFrame()
    df['Epoch start'] = timestamps_epoch_start
    df[channel_names] = epochs  # temporarilly commented out for debugging

    # df['eh_test'] = pd.to_datetime(df['start times'])
    # df = df.set_index('Epoch start')
    return df


def _signal_afc(N: Union[int, float], i: Union[int, float],
                signals: Union[List[Union[int, float]], np.ndarray]):
    R_sum = 0

    for n in range(1, N - i):
        R_sum += signals[n] * signals[n + i]

    R_sum = R_sum * (1 / N)

    return R_sum


def _lp_filter_creation():
    return None


def _est_signal_value(signal, p, a, n):
    the_sum = 0
    for index in range(1, p):
        # TODO: check if the n is smaller than p and make some error handling for that, this should be able to go back in time
        the_sum += a[index] * signal[n - index]
    return -1 * the_sum


def _error_of_signal():
    return


def _calculate_pe_val():
    return None


def _calculate_pe_acf():
    return None


def _calculate_sem():
    return None


def _find_transients():
    # This is part of the feature extraction process
    # for i in range(1, len(EE)):
    #     if T1 * math.mean(EE)
    return


def adaptive_segmentation(signals: Union[List[Union[int, float]], np.ndarray]):
    """
    TODO: Implement the functions and add them to the adaptive segmentations function
    TODO: Document and comment the functions
    TODO: Move find_transients function to some other file
    :param signals:
    :return:
    """
    # Store segment length - Store both the onset and the duration
    # Store signals predictor
    # Store corrective predictor
    N = None or 10  # maybe 50?
    i = None or 666 or 56

    # Step 1:
    # 	a. Compute new signals ACF
    _signal_afc(N, i, signals)

    # 	b. adapt LP filter
    # Step 2:

    return None
