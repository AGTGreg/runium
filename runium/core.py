"""
This is the main module.
"""

import time
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from inspect import signature
import atexit
import uuid
from runium.util import get_seconds


class Runium(object):
    """
    This is the main class that gets instantiated by the user.
    """

    def __init__(self, mode='multithreading', workers=None):
        self.__tasks_list = {}
        self.workers = workers
        self.mode = mode
        if self.mode == 'multiprocessing':
            self._executor = ProcessPoolExecutor(self.workers)
        elif self.mode == "multithreading":
            self._executor = ThreadPoolExecutor(self.workers)
        else:
            raise ValueError(
                'mode can only be multiprocessing or multithreading.'
            )

        atexit.register(self._executor.shutdown)

    def run(
        self, task, every=None, times=None, start_in=0, kwargs={},
        callbacks=None
    ):
        """
        Creates a new Task, adds it to the tasks list and submits it to the
        PoolExecutor.
        Returns the Task object.
        """
        every = get_seconds(every)
        start_in = get_seconds(start_in)
        every, times = self.__set_every_times_defaults(every, times)

        task_id = uuid.uuid4().int
        future = self._executor.submit(
            _run_task,
            task, task_id, every, times, start_in, kwargs
        )

        current_task = _Task(task_id, future, callbacks)
        self.__add_task_to_tasks_list(current_task)

        return current_task

    def __add_task_to_tasks_list(self, task):
        self.__tasks_list[task.id] = task

    def __remove_task_from_tasks_list(self, task_id):
        try:
            del self.__tasks_list[task_id]
        except KeyError:
            pass

    def tasks(self):
        """
        Cleans up and returns the tasks list.
        """
        tasks_to_remove = []
        for task_id, task in self.__tasks_list.items():
            if task.future.done() is True:
                tasks_to_remove.append(task_id)
        for t_id in tasks_to_remove:
            self.__remove_task_from_tasks_list(t_id)

        return self.__tasks_list

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


def _run_task(fn, id, interval, times, start_in, kwargs):
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
            runium_param = _make_runium_param(iterations, times)
            task_result = fn(runium=runium_param, **kwargs)
        else:
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


class _Task(object):
    """
    This object represents the task that will be executed by Runium.
    It encapsulates the future object.
    """
    def __init__(self, id, future, callbacks):
        self.id = id
        self.future = future
        self.callbacks = callbacks
        self.then_run(callbacks)

    def then_run(self, callbacks):
        """
        Attach one or a list of callbacks to the task. If the task is finished
        the callbacks wi be executed imidiately in the order they are
        submitted.
        """
        if callbacks is not None:
            if isinstance(callbacks, list):
                for c in callbacks:
                    self.future.add_done_callback(c)
            else:
                self.future.add_done_callback(callbacks)
        return self

    def result(self, timeout=None):
        return self.future.result(timeout)

    def exception(self, timeout=None):
        return self.future.exception(timeout)

    def get_state(self):
        return self.future._state
