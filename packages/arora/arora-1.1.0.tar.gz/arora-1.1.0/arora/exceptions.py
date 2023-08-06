class TooLarge(Exception):
    """
    Raised when the value is too large
    Args:
        onset: The onset of the signal
        len_signal: The length of the signal
        message: Explanation of the error
    """

    def __init__(self, onset, len_signal, message="Please check the parameters"):
        self.onset = onset
        self.len_signal = len_signal
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"{self.onset} is larger than the length ({self.len_signal}) -> {self.message}"


class Negative(Exception):
    """
    Raised when the value is negative
    Args:
        onset: The onset of the signal
        message: Explanation of the error
    """

    def __init__(self, onset, message="Please check the parameters"):
        self.onset = onset
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"{self.onset} is negative and thus unable to be used -> {self.message}"


class CutoffValueError(Exception):
    """
    Raised when the cutoff value is not in the range 0 < x < 1
    Args:
        :cutoff: Cutoff value
        :message: Explanation of the error
    """

    def __int__(self, cutoff, message="Please check your parameters"):
        self.cutoff = cutoff
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"Your cutoff ({self.cutoff}) value is not in the range 0 < x < 1 -> {self.message}"
