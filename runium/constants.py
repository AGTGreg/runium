from enum import Enum


TIME_SCALES = {
    'second': 1, 'seconds': 1,
    'minute': 60, 'minutes': 60,
    'hour': 3600, 'hours': 3600,
    'day': 86400, 'days': 86400
}


class CALLBACK_TYPES(Enum):
    ON_FINISHED = 1
    ON_SUCCESS = 2
    ON_ERROR = 3


# The position of fn and updates_result in the callbacks tuple of Task.
# We use constants instead of index numbers for better readability.
FN = 0
UPDATES_RESULT = 1
