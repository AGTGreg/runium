"""
This is the main module.
"""

import time
import traceback
from multiprocessing.pool import ThreadPool
import concurrent
from concurrent.futures import ThreadPoolExecutor, wait
from runium.util import get_seconds


class Runium(object):
    """
    This is the main class that gets instantiated by the user.
    """

    def __init__(self, workers=None):
        self.tasks = {}
        self.pool = ThreadPool(workers)
        self._executor = ThreadPoolExecutor(workers)
        self.futures = []

    def run(self, task, every=None, times=None, start_in=0, **kwargs):
        """
        Runs the task asynchronously in its own thread and adds it to the
        tasks dict. Key is the thread's ID.
        """
        try:
            task_args = kwargs['kwargs']
        except KeyError:
            task_args = {}

        # Run 1 time if the times and every interval are not set.
        if every is None and times is None:
            times = 1
            every = 0
        # Loop indefinitely if every interval is set and times is not set.
        if every is not None and times is None:
            times = 0

        current_task = {
            "task": task,
            'kwargs': task_args,
            "interval": get_seconds(every),
            "times": times,
            "start_in": get_seconds(start_in)
        }

        future = self._executor.submit(
            self.__loop,
            current_task['task'], current_task['kwargs'],
            current_task['interval'], current_task['times'],
            current_task['start_in']
        )
        self.futures.append(future)

        return future

    def __loop(self, task, kwargs, interval, times, start_in):
        """
        Runs a task every (interval) seconds for (times) times.
        If times is set to 0 it loops indefinitely.
        """
        loop_count = 0
        task_result = None

        if start_in > 0:
            time.sleep(start_in)

        next_time = time.time() + interval
        while True:
            loop_count += 1
            task_result = self.__run_task(task, kwargs=kwargs)
            if times > 0 and loop_count >= times:
                break
            # Skip tasks if we are behind schedule:
            next_time +=\
                (time.time() - next_time) // interval * interval + interval
            time.sleep(max(0, next_time - time.time()))

        return task_result

    def __run_task(self, task, **kwargs):
        """
        Runs the task. This is called in the loop.
        """
        try:
            task_result = task(**kwargs['kwargs'])
        except Exception:
            traceback.print_exc()
        else:
            return task_result

    def __get_stats(self, loop_count, max_loops, now):
        stats = {}
        stats['loop_count'] = loop_count
        stats['now'] = now
        try:
            stats['loops_remaining'] = (loop_count - max_loops) * (-1)
        except TypeError:
            stats['loops_remaining'] = None
        return stats
