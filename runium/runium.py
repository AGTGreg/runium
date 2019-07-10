"""
This is the main module.
"""

import time
import traceback
from concurrent.futures import ThreadPoolExecutor
import threading
import uuid
from runium.util import get_seconds


class Runium(object):
    """
    This is the main class that gets instantiated by the user.
    """

    def __init__(self, workers=None):
        self.tasks = {}
        self._executor = ThreadPoolExecutor(workers)

    def run(self, task, every=None, times=None, start_in=0, kwargs={}):
        """
        Runs the task asynchronously in its own thread and adds it to the
        tasks dict with a unique UUID.
        """
        every, times = self.__set_every_times_defaults(every, times)
        current_task = Task(task, kwargs, every, times, start_in)
        future = self._executor.submit(self.__loop, current_task)
        current_task.future = future
        self.tasks[current_task.id] = current_task
        return future

    def __loop(self, task):
        """
        Runs a task every (interval) seconds for (times) times.
        If times is set to 0 it loops indefinitely.
        """
        loop_count = 0
        task_result = None
        interval = task.interval

        if task.start_in > 0:
            time.sleep(task.start_in)

        next_time = time.time() + interval
        while True:
            loop_count += 1
            task_result = task.run()
            if task.times > 0 and loop_count >= task.times:
                break
            # Skip tasks if we are behind schedule:
            next_time +=\
                (time.time() - next_time) // interval * interval + interval
            time.sleep(max(0, next_time - time.time()))

        self.__remove_task_from_list(task.id)
        return task_result

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
            every = 0.01
        return every, times

    def __remove_task_from_list(self, task_id):
        try:
            del self.tasks[task_id]
        except KeyError:
            pass

    def __get_stats(self, loop_count, max_loops, now):
        stats = {}
        stats['loop_count'] = loop_count
        stats['now'] = now
        try:
            stats['loops_remaining'] = (loop_count - max_loops) * (-1)
        except TypeError:
            stats['loops_remaining'] = None
        return stats


class Task(object):
    def __init__(self, fn, arguments, interval, times, start_in):
        self.id = uuid.uuid1().int
        self.fn = fn
        self.arguments = arguments,
        self.interval = get_seconds(interval)
        self.times = times
        self.start_in = get_seconds(start_in)
        self.future = None

    def run(self):
        """
        Runs the task. This is called in the loop.
        """
        try:
            result = self.fn(**self.arguments[0])
        except Exception as err:
            traceback.print_exc()
            return err
        else:
            return result
