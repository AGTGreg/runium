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

    def __init__(self, concurrency_mode='threads', workers=None):
        self.tasks = {}
        self._executor = ThreadPoolExecutor(workers)

    def run(
        self, task, every=None, times=None, start_in=0,
        kwargs={}, exit_on_exception=True
    ):
        """
        Creates a new Task, adds it to the tasks list and submits it to the
        PoolExecutor.
        Returns the Task object.
        """
        every, times = self.__set_every_times_defaults(every, times)
        current_task = Task(
            task, kwargs, every, times, start_in, exit_on_exception
        )

        future = self._executor.submit(self.__loop, current_task)
        current_task.future = future

        self.tasks[current_task.id] = current_task
        return current_task

    def __loop(self, task):
        """
        Runs a task in :start_in seconds, every :interval seconds for :times
        times.
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


class Task(object):
    """
    This object represents the method that is beeing run by Runium.
    Every time we tell Runnium to run a method, it creates and returns a Task
    object.
    It contains usefull data and methods for Runium and the users and exposes
    the future and the current Thread objects.
    """

    def __init__(
        self, fn, arguments, interval, times, start_in, exit_on_exception
    ):
        self.id = uuid.uuid1().int
        self.fn = fn
        self.arguments = arguments,
        self.interval = get_seconds(interval)
        self.times = times
        self.start_in = get_seconds(start_in)
        self.exit_on_exception = exit_on_exception
        self.callback = None
        self.future = None
        self.thread = None

    def run(self):
        """
        Runs the task. This is a blocking operation. Do not call this method.
        It is called by Runium internally.
        """
        kwargs = self.arguments[0]
        self.thread = threading.current_thread()

        if self.exit_on_exception is False:
            result = None
            try:
                result = self.fn(**kwargs)
            except Exception as err:
                traceback.print_exc()
                self.future.set_exception(err)
                result = err
            finally:
                return result
        else:
            return self.fn(**kwargs)

    # The following methods are wrappers for the future object.
    def cancel(self):
        """
        Attempt to cancel the call. If the call is currently being executed or
        finished running and cannot be cancelled then the method will return
        False, otherwise the call will be cancelled and the method will return
        True.
        """
        return self.future.cancel()

    def cancelled(self):
        """
        Return True if the call was successfully cancelled.
        """
        return self.future.cancelled()

    def running(self):
        """
        Return True if the call is currently being executed and cannot be
        cancelled.
        """
        return self.future.running()

    def done(self):
        """
        Return True if the call was successfully cancelled or finished running.
        """
        return self.future.done()

    def result(self, timeout=None):
        """
        Return the value returned by the call. If the call hasn’t yet completed
        then this method will wait up to timeout seconds. If the call hasn’t
        completed in timeout seconds, then a concurrent.futures.TimeoutError
        will be raised. timeout can be an int or float. If timeout is not
        specified or None, there is no limit to the wait time.

        If the future is cancelled before completing then CancelledError will
        be raised.

        If the call raised, this method will raise the same exception.
        """
        return self.future.result(timeout)

    def exception(self, timeout=None):
        """
        Return the exception raised by the call. If the call hasn’t yet
        completed then this method will wait up to timeout seconds. If the call
        hasn’t completed in timeout seconds, then a
        concurrent.futures.TimeoutError will be raised. timeout can be an int
        or float. If timeout is not specified or None, there is no limit to the
        wait time.

        If the future is cancelled before completing then CancelledError will
        be raised.

        If the call completed without raising, None is returned.
        """
        return self.future.exception(timeout)

    def when_finished(self, callback):
        """
        Attaches the callback onto the future. callback will be called, with
        the future as its only argument, every time the future is cancelled or
        finishes running.

        Added callables are called in the order that they were added and are
        always called in a thread belonging to the process that added them. If
        the callable raises an Exception subclass, it will be logged and
        ignored. If the callable raises a BaseException subclass, the behavior
        is undefined.

        If the future has already completed or been cancelled, callback will be
        called immediately.
        """
        self.callback = callback
        self.future.add_done_callback(callback)
        return self
