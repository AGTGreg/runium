"""
This is the main module.
"""

import time
import traceback
import threading
from concurrent import futures
from concurrent.futures import ThreadPoolExecutor
from runium.util import get_seconds


class Runium(object):
    """
    This is the main class that gets instantiated by the user.
    """

    def __init__(self):
        self.tasks = {}

    def run(self, task, every=None, times=None, **kwargs):
        """
        Runs the task in a new thread and adds it to the tasks dict. Key is the
        thread's ID.
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
            "times": times
        }

        # # With an executor
        # future = None
        # executor = ThreadPoolExecutor(max_workers=5)

        # # with ThreadPoolExecutor(max_workers=5) as executor:
        # future = executor.submit(
        #     self.__loop,
        #     current_task['task'], current_task['kwargs'],
        #     current_task['interval'], current_task['times']
        # )
        # executor.shutdown(wait=False)
        # return future.result()

        # With simple threads
        task_th = threading.Thread(
            target=self.__loop, args=(
                current_task['task'], current_task['kwargs'],
                current_task['interval'], current_task['times']
            ))
        task_th.start()

        current_task['thread'] = task_th
        self.tasks[task_th.ident] = current_task
        return task_th

    def __loop(self, task, kwargs, interval, times):
        """
        Runs a task every (interval) seconds for (times) times.
        If times is set to 0 it loops indefinitely.
        Passes the stats and any **kwargs the task may have.
        """
        next_time = time.time() + interval
        loop_count = 0
        task_result = None
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
