"""
This is the main module.
"""

import time
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from inspect import signature
import atexit
from runium.util import get_seconds


class Runium(object):
    """
    This is the main class that gets instantiated by the user.
    """

    def __init__(self, concurrency_mode='multithreading', workers=None):
        self.tasks = {}
        self.workers = workers
        self.concurrency_mode = concurrency_mode
        if self.concurrency_mode == 'multiprocessing':
            self._executor = ProcessPoolExecutor(self.workers)
        else:
            self._executor = ThreadPoolExecutor(self.workers)

        atexit.register(self._executor.shutdown)

    def run(
        self, task, every=None, times=None, start_in=0, kwargs={},
        callback=None
    ):
        """
        Creates a new Task, adds it to the tasks list and submits it to the
        PoolExecutor.
        Returns the Task object.
        """
        every = get_seconds(every)
        start_in = get_seconds(start_in)
        every, times = self.__set_every_times_defaults(every, times)

        future = self._executor.submit(
            _run_task,
            task, every, times, start_in, kwargs
        )

        if callback is not None:
            future.add_done_callback(callback)

        return future

    def __set_every_times_defaults(self, every, times):
        """
        Sets the :every and :times properties to sensible defaults if one or
        any of them are not set.
        Sets defaults so that Runium will:
            Run the task one time if the :times and :every interval are not
            set.
            Loop indefinitely if :every is set and :times is not set.
        """
        if every is None and times is None:
            times = 1
            every = 0
        elif every is not None and times is None:
            times = 0
        elif every is None and times is not None:
            every = 0
        return every, times


def _run_task(fn, interval, times, start_in, kwargs):
    """
    Runs the task, optionally for :times every :every seconds in :start_in
    seconds.
    This is blocking and is meant to be called by Runium in a new Thread or
    Process.
    """
    task_result = None
    iterations = 0

    if start_in > 0:
        time.sleep(start_in)

    next_time = time.time() + interval
    while True:
        iterations += 1

        # Runium will pass some stats and functions in the callable's runium
        # attribute.
        if 'runium' in signature(fn).parameters.keys():
            kwargs['runium'] = _make_runium_param(iterations, times)

        task_result = fn(**kwargs)

        if times > 0 and iterations >= times:
            break

        # Skip tasks if we are behind schedule:
        if interval > 0:
            next_time +=\
                (time.time() - next_time) // interval * interval + interval
            time.sleep(max(0, next_time - time.time()))

    return task_result


def _make_runium_param(iterations, times):
    """
    Creates and returns a dict with runium specific stats and functions that
    can be accessed from within the task.
    """
    context = {
        'iterations': iterations,
        'iterations_remaining': times - iterations
    }
    return context
