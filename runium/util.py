"""
This module contains helpers that are used internally by Runium.
"""
from runium.constants import TIME_SCALES


def get_seconds(interval):
    """
    Returns seconds which is time * scale.
    If interval is a number or None then it will be returned as is.

    interval: Can be a number or a string in the following format: 'time scale'
    ie: '10 minutes'.
    """
    if type(interval) is str:
        interval_array = interval.split(' ')
        try:
            seconds = int(interval_array[0]) * TIME_SCALES[interval_array[1]]
        except KeyError:
            raise ValueError(
                "Valid time scales are: {}".format(list(TIME_SCALES.keys()))
            )
        except ValueError:
            raise ValueError(
                '''
                Invalid format in time scale. It must include an integer
                followed by a string.
                Try a format like this: '1 minute'.
                '''
            )
        else:
            return seconds

    elif isinstance(interval, (int, float)) or interval is None:
        return interval

    else:
        raise TypeError(
            "Time intervals can only be a string, an integer or a float."
        )
